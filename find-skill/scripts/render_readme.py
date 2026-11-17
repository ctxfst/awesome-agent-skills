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
    for readme in (ROOT / "README.md", ROOT / "README.zh-TW.md"):
        chinese = readme.name == "README.zh-TW.md"
        if chinese:
            lines = [
                f"完整目錄共 **{len(records)} 個 Skill，來自 {len(groups)} 個來源**。",
                "每筆包含名稱、description、固定 commit、安裝來源連結與原文連結；完整資料見 "
                "[catalog/skills.json](catalog/skills.json)。",
                "",
            ]
        else:
            lines = [
                f"The full catalog contains **{len(records)} Skills from {len(groups)} sources**.",
                "Each entry includes its name, description, pinned commit, source URL, and raw URL. "
                "See [catalog/skills.json](catalog/skills.json) for the complete data.",
                "",
            ]
        for source in sorted(groups, key=str.lower):
            count = len(groups[source])
            if chinese:
                label = f"{count} 個 Skill"
            else:
                label = f"{count} Skill" if count == 1 else f"{count} Skills"
            lines.append(f"- [{source}](https://github.com/{source}) — {label}")
        lines.append("")
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
