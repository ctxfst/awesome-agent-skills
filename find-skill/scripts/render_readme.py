#!/usr/bin/env python3
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
START = "<!-- CATALOG:START -->"
END = "<!-- CATALOG:END -->"


def main():
    records = json.loads((ROOT / "catalog" / "skills.json").read_text(encoding="utf-8"))
    groups = defaultdict(list)
    for record in records:
        groups[record["source"]].append(record)
    lines = []
    for source in sorted(groups, key=str.lower):
        lines.extend([f"### {source}", ""])
        for record in sorted(groups[source], key=lambda item: item["id"].lower()):
            description = " ".join(record["description"].splitlines()).strip()
            lines.append(f"- **{record['name']}** — {description} ([source]({record['url']}))")
        lines.append("")
    for readme in (ROOT / "README.md", ROOT / "README.zh-TW.md"):
        text = readme.read_text(encoding="utf-8")
        if START not in text or END not in text:
            raise ValueError(f"{readme.name}: catalog markers are missing")
        before, remainder = text.split(START, 1)
        _, after = remainder.split(END, 1)
        updated = before + START + "\n" + "\n".join(lines) + END + after
        readme.write_text(updated, encoding="utf-8")
        print(f"Rendered {len(records)} Skills from {len(groups)} sources into {readme.name}")


if __name__ == "__main__":
    main()
