#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
GITHUB_REPO = re.compile(
    r"https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)",
    re.IGNORECASE,
)
RESERVED_OWNERS = {
    "about", "account", "advisories", "apps", "blog", "codespaces", "collections",
    "contact", "copilot", "customer-stories", "developer", "developers", "docs",
    "edu", "education", "enterprise", "enterprises", "events", "explore", "features",
    "issues", "join", "legal", "login", "marketplace", "new", "notifications",
    "open-source", "organizations", "orgs", "partners", "premium", "pricing",
    "professional-services", "pulls", "resources", "search", "security", "sessions",
    "settings", "signup", "site", "solutions", "sponsors", "stars", "support",
    "teams", "topics", "trending", "user-attachments", "users",
}


def public_git_environment():
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    return environment


def git(*args, cwd=None):
    return subprocess.run(
        ["git", "-c", "credential.helper=", *map(str, args)],
        cwd=cwd,
        env=public_git_environment(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


def extract_repositories(readme):
    repositories = {}
    for match in GITHUB_REPO.finditer(readme):
        owner, repo = match.groups()
        if owner.casefold() in RESERVED_OWNERS:
            continue
        if repo.casefold().endswith(".git"):
            repo = repo[:-4]
        repo = repo.rstrip(".")
        if not repo:
            continue
        name = f"{owner}/{repo}"
        repositories.setdefault(name.casefold(), name)
    return sorted(repositories.values(), key=str.casefold)


def materialize_list(listing, cache):
    destination = cache / listing["repo"]
    if not (destination / ".git").exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        git(
            "clone", "--depth", "1", "--no-checkout",
            f"https://github.com/{listing['repo']}.git", destination,
        )
    commit = listing["commit"]
    probe = subprocess.run(
        ["git", "-C", str(destination), "cat-file", "-e", f"{commit}^{{commit}}"],
        env=public_git_environment(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if probe.returncode:
        git("-C", destination, "fetch", "--depth", "1", "origin", commit)
    git("-C", destination, "checkout", "--detach", commit)
    return find_readme(destination)


def find_readme(directory):
    matches = sorted(
        (path for path in directory.iterdir() if path.is_file() and path.name.casefold() == "readme.md"),
        key=lambda path: path.name.casefold(),
    )
    if not matches:
        raise FileNotFoundError(f"README.md not found in {directory}")
    return matches[0]


def deduplicate_sources(sources):
    unique = []
    seen = set()
    for source in sources:
        key = source["repo"].casefold()
        if key in seen:
            continue
        seen.add(key)
        unique.append(source)
    return unique, len(sources) - len(unique)


def default_branch_commit(repository):
    result = git("ls-remote", f"https://github.com/{repository}.git", "HEAD")
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) == 2 and fields[1] == "HEAD" and re.fullmatch(r"[0-9a-fA-F]{40}", fields[0]):
            return fields[0]
    raise RuntimeError("default branch HEAD was not returned")


def error_summary(exc):
    if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
        return exc.stderr.strip().splitlines()[-1][:300]
    return str(exc)[:300]


def main():
    parser = argparse.ArgumentParser(description="Add GitHub repositories linked by pinned awesome lists")
    parser.add_argument("--sources", default=str(ROOT / "sources.yaml"))
    parser.add_argument("--cache", default=str(Path.home() / ".cache" / "awesome-agent-skills" / "lists"))
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    source_path = Path(args.sources).expanduser().resolve()
    cache = Path(args.cache).expanduser().resolve()
    document = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    sources = document.get("sources") if isinstance(document, dict) else None
    listings = document.get("awesome_lists") if isinstance(document, dict) else None
    if not isinstance(sources, list) or not isinstance(listings, list) or not listings:
        raise ValueError(f"Expected sources and awesome_lists in {source_path}")

    sources[:], duplicate_sources = deduplicate_sources(sources)
    existing = {entry["repo"].casefold() for entry in sources}
    existing.update(entry["repo"].casefold() for entry in listings)
    discovered = {}
    failed_lists = []
    for listing in listings:
        try:
            readme = materialize_list(listing, cache)
            repositories = extract_repositories(readme.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, subprocess.CalledProcessError) as exc:
            failed_lists.append(listing["repo"])
            print(f"{listing['repo']}: list fetch failed; continuing ({error_summary(exc)})")
            continue
        added = 0
        for repository in repositories:
            key = repository.casefold()
            if key not in existing and key not in discovered:
                discovered[key] = repository
                added += 1
        print(f"{listing['repo']}: {len(repositories)} repositories linked, {added} new")

    unavailable = []
    resolved = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(default_branch_commit, repo): repo for repo in discovered.values()}
        for future in as_completed(futures):
            repository = futures[future]
            try:
                commit = future.result()
            except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
                unavailable.append(repository)
                print(f"{repository}: skipped as unavailable or private ({error_summary(exc)})")
                continue
            resolved.append({"repo": repository, "commit": commit, "kind": "community"})
            print(f"{repository}: {commit}")

    sources.extend(sorted(resolved, key=lambda entry: entry["repo"].casefold()))
    if resolved or duplicate_sources:
        temporary = source_path.with_suffix(".yaml.tmp")
        temporary.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        os.replace(temporary, source_path)
    print(f"Added {len(resolved)} sources to {source_path}")
    print(f"Removed {duplicate_sources} duplicate sources")
    print(f"Skipped {len(unavailable)} unavailable or private repositories")
    for repository in sorted(unavailable, key=str.casefold):
        print(f"  Unavailable/private: {repository}")
    print(f"Awesome lists that could not be fetched: {len(failed_lists)}")
    for repository in sorted(failed_lists, key=str.casefold):
        print(f"  List fetch failed: {repository}")


if __name__ == "__main__":
    main()
