#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

import yaml

ROOT = Path(__file__).resolve().parents[2]


def public_git_environment():
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    return environment


def run_git(repo, *args):
    subprocess.run(
        ["git", "-c", "credential.helper=", "-C", str(repo), *args],
        check=True,
        env=public_git_environment(),
    )


def materialize(source, cache):
    local_path = source.get("local_path")
    if local_path:
        repo_root = Path(local_path).expanduser().resolve()
        if not repo_root.is_dir():
            raise FileNotFoundError(f"Local source is not a directory: {repo_root}")
        return repo_root
    destination = cache / source["repo"]
    if not (destination / ".git").exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "-c", "credential.helper=", "clone", "--depth", "1", "--no-checkout", f"https://github.com/{source['repo']}.git", str(destination)],
            check=True,
            env=public_git_environment(),
        )
    commit = source["commit"]
    probe = subprocess.run(
        ["git", "-c", "credential.helper=", "-C", str(destination), "cat-file", "-e", f"{commit}^{{commit}}"],
        check=False,
        env=public_git_environment(),
    )
    if probe.returncode:
        run_git(destination, "fetch", "--depth", "1", "origin", commit)
    run_git(destination, "checkout", "--detach", commit)
    return destination


def frontmatter(path):
    raw = path.read_text(encoding="utf-8-sig")
    match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", raw, re.S)
    if not match:
        return {}
    try:
        value = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return value if isinstance(value, dict) else {}


NON_SCRIPT_SUFFIXES = {
    ".adoc", ".avi", ".bmp", ".css", ".csv", ".doc", ".docx", ".gif", ".gz",
    ".htm", ".html", ".ico", ".jpeg", ".jpg", ".json", ".markdown", ".md",
    ".mov", ".mp3", ".mp4", ".pdf", ".png", ".ppt", ".pptx", ".rst", ".svg",
    ".tar", ".text", ".toml", ".tsv", ".txt", ".wav", ".webm", ".webp", ".xls",
    ".xlsx", ".yaml", ".yml", ".zip",
}


def contains_scripts(directory):
    scripts = directory / "scripts"
    if scripts.is_dir() and any(path.is_file() for path in scripts.rglob("*")):
        return True
    for path in directory.rglob("*"):
        if path.name == "SKILL.md" or path.suffix.casefold() in NON_SCRIPT_SUFFIXES:
            continue
        if path.is_file() and os.access(path, os.X_OK):
            return True
    return False


def collect(repo_root, source):
    records = []
    skipped = {"missing": 0, "short": 0, "name": 0}
    errors = []
    for skill_md in sorted(repo_root.rglob("SKILL.md")):
        if ".git" in skill_md.parts:
            continue
        try:
            if not skill_md.is_file():
                errors.append(f"{skill_md}: not a file")
                continue
            metadata = frontmatter(skill_md)
        except (OSError, UnicodeError) as exc:
            errors.append(f"{skill_md}: {exc}")
            continue
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            skipped["missing"] += 1
            continue
        directory = skill_md.parent
        relative = directory.relative_to(repo_root).as_posix()
        name = metadata.get("name")
        if not isinstance(name, str) or not name.strip():
            name = directory.name
        name = name.strip()
        normalized_name = re.sub(r"[\s-]+", "", name).casefold()
        normalized_description = re.sub(r"[\s-]+", "", description.strip()).casefold()
        if normalized_description == normalized_name:
            skipped["name"] += 1
            continue
        if len(re.sub(r"\s+", "", description)) < 40:
            skipped["short"] += 1
            continue
        description = re.sub(r"\s+", " ", description).strip()
        source_name = source["repo"]
        skill_id = f"{source_name}/{relative}" if relative != "." else source_name
        encoded_relative = quote(relative, safe="/")
        url = f"https://github.com/{source_name}/tree/{source['commit']}"
        raw_url = f"https://raw.githubusercontent.com/{source_name}/{source['commit']}"
        if relative != ".":
            url += f"/{encoded_relative}"
            raw_url += f"/{encoded_relative}"
        raw_url += "/SKILL.md"
        records.append({
            "id": skill_id,
            "name": name,
            "description": description,
            "source": source_name,
            "path": relative,
            "commit": source["commit"],
            "url": url,
            "raw_url": raw_url,
            "kind": source["kind"],
            "has_scripts": contains_scripts(directory),
        })
    return records, skipped, errors


def description_key(record):
    return re.sub(r"\s+", "", record["description"]).casefold()


def record_priority(record, sources):
    source = sources[record["source"]]
    return (
        0 if record["kind"] == "official" else 1,
        -int(source.get("stars", 0)),
        record["id"].casefold(),
        record["id"],
    )


def main():
    parser = argparse.ArgumentParser(description="Collect Skill names and descriptions into a catalog")
    parser.add_argument("--sources", default=str(ROOT / "sources.yaml"))
    parser.add_argument("--cache", default=str(Path.home() / ".cache" / "awesome-agent-skills" / "src"))
    parser.add_argument("--out", default=str(ROOT / "catalog" / "skills.json"))
    args = parser.parse_args()
    source_file = Path(args.sources).expanduser().resolve()
    cache = Path(args.cache).expanduser().resolve()
    output = Path(args.out).expanduser().resolve()
    document = yaml.safe_load(source_file.read_text(encoding="utf-8"))
    sources = document.get("sources") if isinstance(document, dict) else None
    if not isinstance(sources, list) or not sources:
        raise ValueError(f"No sources found in {source_file}")
    collected = {}
    total_skipped = {"missing": 0, "short": 0, "name": 0}
    empty_sources = []
    failed_sources = []
    unreadable_files = 0
    for source in sources:
        try:
            repo_root = materialize(source, cache)
            records, skipped, errors = collect(repo_root, source)
        except (OSError, UnicodeError, subprocess.CalledProcessError) as exc:
            failed_sources.append(source["repo"])
            print(f"{source['repo']}: fetch or collection failed; continuing ({exc})")
            continue
        duplicate_count = 0
        for record in records:
            if record["id"] in collected:
                duplicate_count += 1
                continue
            collected[record["id"]] = record
        for reason in total_skipped:
            total_skipped[reason] += skipped[reason]
        unreadable_files += len(errors)
        for error in errors:
            print(f"{source['repo']}: unreadable SKILL.md skipped: {error}")
        if not records:
            empty_sources.append(source["repo"])
        print(
            f"{source['repo']}: {len(records) - duplicate_count} Skills, "
            f"{duplicate_count} duplicate IDs, "
            f"{skipped['missing']} missing, {skipped['short']} short, {skipped['name']} name-only"
        )

    source_map = {source["repo"]: source for source in sources}
    catalog = {}
    descriptions = set()
    duplicate_descriptions = 0
    for record in sorted(collected.values(), key=lambda item: record_priority(item, source_map)):
        key = description_key(record)
        if key in descriptions:
            duplicate_descriptions += 1
            continue
        descriptions.add(key)
        catalog[record["id"]] = record

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps([catalog[key] for key in sorted(catalog)], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, output)
    print(f"Wrote {len(catalog)} Skills to {output}")
    print(f"Removed {duplicate_descriptions} Skills with duplicate normalized descriptions")
    print(f"Skipped {total_skipped['missing']} Skills without description")
    print(f"Skipped {total_skipped['short']} Skills with descriptions under 40 non-whitespace characters")
    print(f"Skipped {total_skipped['name']} Skills whose descriptions only restate the name")
    print(f"Unreadable SKILL.md entries: {unreadable_files}")
    print(f"Sources with 0 Skills: {len(empty_sources)}")
    for repo in empty_sources:
        print(f"  0 Skills: {repo}")
    print(f"Sources that could not be fetched or collected: {len(failed_sources)}")
    for repo in failed_sources:
        print(f"  Fetch/collection failed: {repo}")


if __name__ == "__main__":
    main()
