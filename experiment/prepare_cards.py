#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiment"
SOURCES = EXPERIMENT / "sources"

REPOS = {
    "lambdatest": ("lambdatest-agent-skills", "LambdaTest/agent-skills"),
    "hig": ("raintree-hig-doctor", "raintree-technology/hig-doctor"),
    "mobbin": ("mobbin-skills", "mobbin/skills"),
    "ibelick": ("ibelick-ui-skills", "ibelick/ui-skills"),
    "illyism": ("illyism-seo-skills", "Illyism/seo-skills"),
    "dreammis": ("dreammis-social-auto-upload", "dreammis/social-auto-upload"),
    "postiz": ("gitroomhq-postiz-agent", "gitroomhq/postiz-agent"),
    "upload-post": ("upload-post-upload-post-skill", "Upload-Post/upload-post-skill"),
}

LIST_REPOS = {
    "voltagent-awesome-agent-skills": "VoltAgent/awesome-agent-skills",
    "composio-awesome-claude-skills": "ComposioHQ/awesome-claude-skills",
    "behisecc-awesome-claude-skills": "BehiSecc/awesome-claude-skills",
}

SELECTION = {
    "api-development": [
        ("lambdatest", f"api-skill/{name}") for name in (
            "api-analyzer", "api-documentation", "api-compliance", "api-ratelimit-helper",
            "api-to-testcase-generator", "api-sdk-generator", "api-security-patterns", "api-mocking",
            "api-versioning-helper", "api-integration-helper", "api-health-monitoring",
            "api-inference-from-files", "popular-api-fetcher", "graphql-grpc-helper",
            "openapi-spec-generator", "api-designer", "ai-based-api",
        )
    ] + [
        ("lambdatest", "api-skill/postman/postman-testcase-generator"),
        ("lambdatest", "api-skill/postman/postman-to-newman"),
        ("lambdatest", "api-skill/newman/newman-report-analyzer"),
    ],
    "frontend-design": [
        ("hig", f"skills/{name}") for name in (
            "hig-project-context", "hig-platforms", "hig-patterns", "hig-foundations", "hig-inputs",
            "hig-technologies", "hig-components-status", "hig-components-menus", "hig-components-controls",
            "hig-components-layout", "hig-components-content", "hig-components-search",
            "hig-components-system", "hig-components-dialogs",
        )
    ] + [
        ("hig", "plugin/skills/hig-doctor-audit"),
        ("mobbin", "skills/redesign-screen"),
        ("ibelick", "skills/improve-ui"),
        ("ibelick", "skills/baseline-ui"),
        ("ibelick", "skills/create-design-md"),
        ("ibelick", "skills/fixing-accessibility"),
    ],
    "seo": [("illyism", f"seo/{name}") for name in (
        "reddit-serp", "linkdr", "directory-submissions", "dataforseo-serp", "ai-seo-report",
        "seo-roast", "proof-kb", "ahrefs-research", "honest-link-outreach", "blog-refresher",
        "domain-migration", "vs-and-alternatives", "blitz-seo", "internal-linking", "block-ai-scrapers",
        "awesome-tools", "seo-autopilot", "content-coverage", "seo-title-optimization", "aiseotracker",
    )],
    "social-media-publishing": [("dreammis", f"skills/{name}") for name in (
        "social-auto-upload", "alipay-upload", "baijiahao-upload", "bilibili-upload", "dayu-upload",
        "douyin-upload", "facebook-upload", "hupu-upload", "instagram-upload", "kuaishou-upload",
        "meta-upload", "tencent-upload", "tiktok-upload", "weibo-upload", "xiaohongshu-upload",
        "xueqiu-upload", "youtube-upload", "zhihu-upload",
    )] + [
        ("postiz", "skills/postiz"),
        ("upload-post", "."),
    ],
    "test-automation": [("lambdatest", name) for name in (
        "appium-skill", "cypress-skill", "playwright-skill", "selenium-skill", "jest-skill",
        "vitest-skill", "mocha-skill", "jasmine-skill", "karma-skill", "junit-5-skill",
        "testng-skill", "pytest-skill", "unittest-skill", "rspec-skill", "cucumber-skill",
        "behave-skill", "robot-framework-skill", "webdriverio-skill", "detox-skill", "flutter-testing-skill",
    )],
}

SECTION_HEADINGS = {
    "Material": {
        "input", "inputs", "input material", "input materials", "material", "materials", "source material",
        "source materials", "required input", "required inputs",
    },
    "Done": {
        "output", "outputs", "output format", "deliverable", "deliverables", "result", "results",
        "expected output", "expected outputs", "expected result", "expected results", "success criteria",
        "done", "completion criteria", "final output", "response format",
    },
    "Requires": {
        "requirements", "prerequisites", "dependencies", "setup", "environment", "installation", "configuration",
        "authentication", "required tools", "tools and setup", "environment variables", "required environment",
    },
    "Replaces": {"replaces", "current way", "manual workflow", "manual alternative"},
    "Not for": {
        "not for", "when not to use", "do not use", "do not use this skill", "out of scope", "exclusions",
        "boundaries", "limitations",
    },
}

SOCIAL_NAMES = {
    "social-auto-upload": "the supported social platforms",
    "alipay-upload": "Alipay Life Services",
    "baijiahao-upload": "Baijiahao",
    "bilibili-upload": "Bilibili",
    "dayu-upload": "Dayuhao",
    "douyin-upload": "Douyin",
    "facebook-upload": "Facebook profiles",
    "hupu-upload": "Hupu",
    "instagram-upload": "Instagram",
    "kuaishou-upload": "Kuaishou",
    "meta-upload": "Facebook Pages",
    "tencent-upload": "WeChat Channels",
    "tiktok-upload": "TikTok",
    "weibo-upload": "Weibo",
    "xiaohongshu-upload": "Xiaohongshu",
    "xueqiu-upload": "Xueqiu",
    "youtube-upload": "YouTube",
    "zhihu-upload": "Zhihu",
}


def commit(local_dir):
    return subprocess.run(
        ["git", "-C", str(SOURCES / local_dir), "rev-parse", "HEAD"],
        check=True, text=True, capture_output=True,
    ).stdout.strip()


def split_document(raw):
    match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", raw, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a mapping")
    return metadata, raw[match.end():]


def normalize_heading(value):
    value = re.sub(r"^[\W_]+", "", value.lower())
    value = re.sub(r"^\d+(?:\.\d+)*\s*", "", value)
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def clean_section(value):
    value = re.sub(r"```.*?```", "", value, flags=re.S)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\n{3,}", "\n\n", value).strip()
    if len(value) <= 1600:
        return value
    shortened = value[:1600].rsplit(" ", 1)[0].rstrip()
    return shortened + "…"


def extract_sections(body):
    headings = list(re.finditer(r"^(#{1,6})\s+(.+?)\s*$", body, re.M))
    extracted = {name: [] for name in SECTION_HEADINGS}
    for index, match in enumerate(headings):
        heading = normalize_heading(match.group(2))
        level = len(match.group(1))
        end = len(body)
        for following in headings[index + 1:]:
            if len(following.group(1)) <= level:
                end = following.start()
                break
        for section, accepted in SECTION_HEADINGS.items():
            if heading in accepted:
                text = clean_section(body[match.end():end])
                if text:
                    extracted[section].append(text)
    return {name: "\n\n".join(parts) if parts else "missing" for name, parts in extracted.items()}


def description_fallbacks(description):
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", description)) if part.strip()]
    candidates = [sentence for sentence in sentences if not re.match(r"(?i)^(use|trigger|also use)\b.*\b(when|whenever|on)\b", sentence)]
    done = [sentence for sentence in candidates if re.search(
        r"(?i)\b(generates?|creates?|produces?|writes?|returns?|outputs?|delivers?|builds?|converts?|extracts?|ships?|publishes?|schedules?|audits?|reviews?|analy[sz]es?|repairs?|fixes|tests?|automates?)\b",
        sentence,
    )]
    material = [sentence for sentence in candidates if re.search(
        r"(?i)\b(inputs?|files?|code(?:base)?|screenshots?|notes?|content|requirements?|repository|site|url|documents?|images?|videos?|existing)\b",
        sentence,
    )]
    not_for = [sentence for sentence in candidates if re.search(
        r"(?i)\b(not for|does not|do not|out of scope|instead)\b", sentence,
    )]
    return {
        "Material": " ".join(material[:2]) if material else "missing",
        "Done": " ".join(done[:2]) if done else "missing",
        "Not for": " ".join(not_for[:2]) if not_for else "missing",
    }


def find_license(skill_dir, repo_dir, metadata):
    value = metadata.get("license")
    if isinstance(value, str) and value.strip() and "complete terms" not in value.lower():
        return value.strip()
    candidates = list(skill_dir.glob("LICENSE*")) + list(repo_dir.glob("LICENSE*"))
    for path in candidates:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")[:5000].lower()
        if "apache license" in text:
            return "Apache-2.0"
        if "mit license" in text or "mit-0" in text:
            return "MIT"
        if "mozilla public license" in text:
            return "MPL-2.0"
        if "gnu general public license" in text:
            return "GPL"
        return path.name
    return "missing"


def social_job(name):
    platform = SOCIAL_NAMES[name]
    if name == "social-auto-upload":
        return (
            "Route social content to the correct publishing workflow",
            "Use when publishing or scheduling videos, articles, or image-text posts on one or more supported social platforms and the target platform must be selected explicitly.",
        )
    return (
        f"Publish or schedule content on {platform}",
        f"Use when publishing or scheduling content on {platform} through social-auto-upload.",
    )


def make_card(category, repo_key, relative_path):
    local_dir, source = REPOS[repo_key]
    repo_dir = SOURCES / local_dir
    skill_dir = (repo_dir / relative_path).resolve()
    skill_path = skill_dir / "SKILL.md"
    raw = skill_path.read_text(encoding="utf-8")
    metadata, body = split_document(raw)
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"{skill_path}: missing description")
    description = description.strip()
    name = str(metadata.get("name") or skill_dir.name)
    title_match = re.search(r"^#\s+([^#\n].+)$", body, re.M)
    title = str(metadata.get("displayName") or (title_match.group(1).strip() if title_match else name))
    when = description
    if repo_key == "dreammis":
        title, when = social_job(name)
    sections = extract_sections(body)
    fallbacks = description_fallbacks(description)
    for section, value in fallbacks.items():
        if sections[section] == "missing":
            sections[section] = value
    languages = metadata.get("languages")
    if isinstance(languages, list) and languages:
        language_text = "Documented languages: " + ", ".join(str(language) for language in languages)
        sections["Requires"] = language_text if sections["Requires"] == "missing" else sections["Requires"] + "\n\n" + language_text
    source_path = "." if relative_path == "." else Path(relative_path).as_posix()
    pinned = commit(local_dir)
    url = f"https://github.com/{source}/tree/{pinned}" + ("" if source_path == "." else "/" + quote(source_path))
    scripts_dir = skill_dir / "scripts"
    lower = raw.lower()
    card_metadata = {
        "skill": name,
        "source": source,
        "path": source_path,
        "commit": pinned,
        "url": url,
        "license": find_license(skill_dir, repo_dir, metadata),
        "description": description,
        "trust": "T3",
        "category": category,
        "has_scripts": scripts_dir.is_dir() and any(path.is_file() for path in scripts_dir.rglob("*")),
        "network": bool(re.search(r"https?://|\bapi\b|oauth|online|cloud|download|\bcurl\b|\bnpx\b", lower)),
        "needs_secrets": bool(re.search(r"api[_ -]?key|access[_ -]?key|\btoken\b|oauth|credential|\bsecret\b|\bpassword\b|authenticate|login", lower)),
    }
    filename = f"{local_dir}--{name}.md"
    card_id = f"{category}/{filename[:-3]}"
    text = yaml.safe_dump(card_metadata, sort_keys=False, allow_unicode=False, width=1000).strip()
    text = f"---\n{text}\n---\n\n# {title}\n\n## When\n{when}\n\n"
    text += "\n\n".join(f"## {section}\n{sections[section]}" for section in SECTION_HEADINGS) + "\n"
    return {
        "card_id": card_id,
        "category": category,
        "source": source,
        "path": source_path,
        "commit": pinned,
        "url": url,
        "filename": filename,
        "text": text,
        "filled_slots": sum(value != "missing" for value in sections.values()) + 1,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if {category: len(items) for category, items in SELECTION.items()} != {
        category: 20 for category in SELECTION
    }:
        raise ValueError("Each category must select exactly 20 Skills")
    selected = [make_card(category, repo, path) for category, items in SELECTION.items() for repo, path in items]
    identities = [(card["source"], card["path"]) for card in selected]
    if len(set(identities)) != 100 or len({card["card_id"] for card in selected}) != 100:
        raise ValueError("Selected Skills and card IDs must be unique")
    if args.check:
        print(json.dumps({
            "categories": {category: len(items) for category, items in SELECTION.items()},
            "cards": len(selected),
            "slot_fill_counts": {str(count): sum(card["filled_slots"] == count for card in selected) for count in range(1, 7)},
        }, indent=2))
        return
    cards_dir = EXPERIMENT / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    if any(cards_dir.glob("*.md")) or any(cards_dir.glob("*/*.md")):
        raise ValueError("experiment/cards is not empty; frozen cards will not be overwritten")
    for card in selected:
        path = cards_dir / card["category"] / card["filename"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(card["text"], encoding="utf-8")
        card["sha256"] = hashlib.sha256(card["text"].encode("utf-8")).hexdigest()
        del card["text"]
        del card["filename"]
        del card["filled_slots"]
    (EXPERIMENT / "manifest.json").write_text(
        json.dumps({"frozen": True, "card_count": len(selected), "cards": selected}, indent=2) + "\n",
        encoding="utf-8",
    )
    (EXPERIMENT / "cards.sha256").write_text(
        "".join(f"{card['sha256']}  {card['card_id']}.md\n" for card in selected), encoding="utf-8"
    )
    source_records = []
    for local_dir, source in LIST_REPOS.items():
        source_records.append({"role": "community-list", "source": source, "commit": commit(local_dir)})
    for local_dir, source in REPOS.values():
        source_records.append({"role": "skill-source", "source": source, "commit": commit(local_dir)})
    (EXPERIMENT / "sources.json").write_text(json.dumps(source_records, indent=2) + "\n", encoding="utf-8")
    print(f"Froze {len(selected)} cards in {cards_dir}")


if __name__ == "__main__":
    main()
