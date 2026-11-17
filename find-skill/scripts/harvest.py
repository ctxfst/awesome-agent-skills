#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def run_git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True)


def materialize(source, cache):
    local_path = source.get("local_path")
    if local_path:
        return Path(local_path).expanduser().resolve()
    destination = cache / source["repo"]
    if not (destination / ".git").exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", f"https://github.com/{source['repo']}.git", str(destination)],
            check=True,
        )
    commit = source["commit"]
    probe = subprocess.run(
        ["git", "-C", str(destination), "cat-file", "-e", f"{commit}^{{commit}}"],
        check=False,
    )
    if probe.returncode:
        run_git(destination, "fetch", "origin", commit)
    run_git(destination, "checkout", "--detach", commit)
    return destination


def frontmatter(path):
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", raw, re.S)
    if not match:
        return {}
    try:
        value = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return value if isinstance(value, dict) else {}


def contains_scripts(directory):
    scripts = directory / "scripts"
    if scripts.is_dir() and any(path.is_file() for path in scripts.rglob("*")):
        return True
    for path in directory.rglob("*"):
        if path.is_file() and os.access(path, os.X_OK):
            return True
    return False


def collect(repo_root, source):
    records = []
    skipped = 0
    for skill_md in sorted(repo_root.rglob("SKILL.md")):
        if ".git" in skill_md.parts:
            continue
        metadata = frontmatter(skill_md)
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            skipped += 1
            continue
        directory = skill_md.parent
        relative = directory.relative_to(repo_root).as_posix()
        name = metadata.get("name")
        if not isinstance(name, str) or not name.strip():
            name = directory.name
        description = re.sub(r"\s+", " ", description).strip()
        source_name = source["repo"]
        skill_id = f"{source_name}/{relative}" if relative != "." else source_name
        url = f"https://github.com/{source_name}/tree/{source['commit']}"
        if relative != ".":
            url += f"/{relative}"
        records.append({
            "id": skill_id,
            "name": name.strip(),
            "description": description,
            "source": source_name,
            "path": relative,
            "commit": source["commit"],
            "url": url,
            "kind": source["kind"],
            "has_scripts": contains_scripts(directory),
        })
    return records, skipped


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
    catalog = {}
    total_skipped = 0
    for source in sources:
        repo_root = materialize(source, cache)
        records, skipped = collect(repo_root, source)
        duplicate_count = 0
        for record in records:
            if record["id"] in catalog:
                duplicate_count += 1
                continue
            catalog[record["id"]] = record
        total_skipped += skipped
        print(
            f"{source['repo']}: {len(records) - duplicate_count} Skills, "
            f"{duplicate_count} duplicate IDs, {skipped} without description"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps([catalog[key] for key in sorted(catalog)], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, output)
    print(f"Wrote {len(catalog)} Skills to {output}")
    print(f"Skipped {total_skipped} Skills without description")


if __name__ == "__main__":
    main()
