#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiment"
CARDS = EXPERIMENT / "cards"
INDEXES = EXPERIMENT / "indexes"
CONDITIONS = {
    "A": "description",
    "B": "skill-md-4000",
    "C": "job-line-card",
    "D": "bm25",
}


def load_finder():
    spec = importlib.util.spec_from_file_location("find_skill", ROOT / "find-skill/scripts/find.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_cards():
    manifest = json.loads((EXPERIMENT / "manifest.json").read_text(encoding="utf-8"))
    if not manifest.get("frozen"):
        raise ValueError("Cards are not marked frozen")
    expected_hashes = {}
    for line in (EXPERIMENT / "cards.sha256").read_text(encoding="utf-8").splitlines():
        digest, card_path = line.split("  ", 1)
        expected_hashes[card_path] = digest
    cards = []
    for entry in manifest["cards"]:
        card_path = entry["card_id"] + ".md"
        raw = (CARDS / card_path).read_text(encoding="utf-8")
        if hashlib.sha256(raw.encode("utf-8")).hexdigest() != expected_hashes[card_path]:
            raise ValueError(f"Frozen card changed: {card_path}")
        match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", raw, re.S)
        if not match:
            raise ValueError(f"Missing card frontmatter: {card_path}")
        metadata = yaml.safe_load(match.group(1))
        body = raw[match.end():].strip()
        local_dir = entry["card_id"].split("/", 1)[1].split("--", 1)[0]
        skill_path = EXPERIMENT / "sources" / local_dir / entry["path"] / "SKILL.md"
        skill_md = skill_path.read_text(encoding="utf-8")
        cards.append({
            "card_id": entry["card_id"],
            "category": entry["category"],
            "source": entry["source"],
            "path": entry["path"],
            "commit": entry["commit"],
            "url": entry["url"],
            "description": metadata["description"],
            "job_line": body,
            "skill_md": skill_md,
        })
    if len(cards) != 100:
        raise ValueError("The experiment requires exactly 100 cards")
    return cards


def embedded_text(card, condition):
    if condition == "A":
        return card["description"]
    if condition == "B":
        return card["skill_md"][:4000]
    if condition == "C":
        return card["job_line"]
    raise ValueError(condition)


def public_card(card):
    return {key: value for key, value in card.items() if key not in ("job_line", "skill_md")}


def tokenize(text):
    return re.findall(r"[a-z0-9_]+|[\u3400-\u9fff]", text.lower())


def build_bm25(cards, out):
    tokenized = [tokenize(card["skill_md"]) for card in cards]
    postings = {}
    lengths = []
    for index, tokens in enumerate(tokenized):
        lengths.append(len(tokens))
        counts = {}
        for token in tokens:
            counts[token] = counts.get(token, 0) + 1
        for token, frequency in counts.items():
            postings.setdefault(token, []).append([index, frequency])
    (out / "bm25.json").write_text(json.dumps({
        "postings": postings,
        "doc_lengths": lengths,
        "average_doc_length": sum(lengths) / len(lengths),
        "k1": 1.5,
        "b": 0.75,
    }, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "meta.json").write_text(json.dumps({
        "condition": "D",
        "method": CONDITIONS["D"],
        "text_source": "full-skill-md",
        "tokenizer": "latin-number-underscore words and CJK unigrams",
        "card_count": len(cards),
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default=str(ROOT.parent / ".env"))
    args = parser.parse_args()
    cards = load_cards()
    INDEXES.mkdir(parents=True, exist_ok=True)
    finder = load_finder()
    finder.load_env(args.env)
    config = {
        "embed_url": os.environ.get("SKILL_FINDER_EMBED_URL", finder.DEFAULT_EMBED_URL),
        "embed_model": os.environ.get("SKILL_FINDER_EMBED_MODEL", finder.DEFAULT_EMBED_MODEL),
    }
    for condition in ("D", "A", "B", "C"):
        out = INDEXES / f"{condition}-{CONDITIONS[condition]}"
        out.mkdir(parents=True, exist_ok=True)
        (out / "cards.json").write_text(
            json.dumps([public_card(card) for card in cards], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        if condition == "D":
            build_bm25(cards, out)
            print(f"Built D BM25 with {len(cards)} full SKILL.md documents")
            continue
        texts = [embedded_text(card, condition) for card in cards]
        vectors = finder.embed(texts, out / "cache/embeddings.json", config, "document")
        matrix = np.stack([vectors[text] for text in texts])
        np.savez_compressed(out / "vectors.npz", ids=np.array([card["card_id"] for card in cards]), raw=matrix)
        (out / "meta.json").write_text(json.dumps({
            "condition": condition,
            "method": CONDITIONS[condition],
            **config,
            "dimension": int(matrix.shape[1]),
            "card_count": len(cards),
            "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        }, indent=2) + "\n", encoding="utf-8")
        print(f"Built {condition} {CONDITIONS[condition]} with {len(cards)} cards using {config['embed_model']}")


if __name__ == "__main__":
    main()
