#!/usr/bin/env python3
import argparse
import importlib.util
import json
import math
import os
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiment"
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


def tokenize(text):
    return re.findall(r"[a-z0-9_]+|[\u3400-\u9fff]", text.lower())


def load_indexes():
    indexes = {}
    for condition, name in CONDITIONS.items():
        directory = INDEXES / f"{condition}-{name}"
        cards = json.loads((directory / "cards.json").read_text(encoding="utf-8"))
        meta = json.loads((directory / "meta.json").read_text(encoding="utf-8"))
        item = {"directory": directory, "cards": cards, "meta": meta, "ids": [card["card_id"] for card in cards]}
        if condition == "D":
            item["bm25"] = json.loads((directory / "bm25.json").read_text(encoding="utf-8"))
        else:
            with np.load(directory / "vectors.npz", allow_pickle=False) as data:
                if [str(value) for value in data["ids"]] != item["ids"]:
                    raise ValueError(f"{condition}: vector and card order differ")
                item["vectors"] = data["raw"]
        indexes[condition] = item
    reference = indexes["A"]["ids"]
    if any(index["ids"] != reference for index in indexes.values()):
        raise ValueError("All four indexes must contain the same cards in the same order")
    configs = {(index["meta"]["embed_url"], index["meta"]["embed_model"]) for key, index in indexes.items() if key != "D"}
    if len(configs) != 1:
        raise ValueError("A, B, and C must use the same embedding endpoint and model")
    return indexes


def bm25_scores(index, query):
    data = index["bm25"]
    scores = np.zeros(len(index["cards"]), dtype=np.float64)
    count = len(scores)
    average = data["average_doc_length"]
    k1, b = data["k1"], data["b"]
    for term in dict.fromkeys(tokenize(query)):
        postings = data["postings"].get(term, [])
        if not postings:
            continue
        idf = math.log(1 + (count - len(postings) + 0.5) / (len(postings) + 0.5))
        for document, frequency in postings:
            length = data["doc_lengths"][document]
            denominator = frequency + k1 * (1 - b + b * length / average)
            scores[document] += idf * frequency * (k1 + 1) / denominator
    return scores


def ranking(index, condition, query, query_vector):
    scores = bm25_scores(index, query) if condition == "D" else index["vectors"] @ query_vector
    order = np.argsort(-scores, kind="stable")[:5]
    return [
        {"card_id": index["ids"][position], "score": float(scores[position])}
        for position in order
    ]


def metrics(details, indices):
    if not indices:
        raise ValueError("Cannot calculate metrics for an empty category")
    near_miss_queries = sum(bool(details[index]["near_misses"]) for index in indices)
    return {
        "queries": len(indices),
        "recall_at_5": sum(details[index]["recall_hit"] for index in indices) / len(indices),
        "top1_accuracy": sum(details[index]["top1_hit"] for index in indices) / len(indices),
        "near_miss_top1_rate": (
            sum(details[index]["near_miss_top1"] for index in indices) / near_miss_queries
            if near_miss_queries else None
        ),
        "near_miss_top1_count": sum(details[index]["near_miss_top1"] for index in indices),
        "queries_with_near_misses": near_miss_queries,
    }


def validate_gold(gold, known_ids, known_categories):
    if not isinstance(gold, list) or not gold:
        raise ValueError("Gold file must contain a non-empty JSON list")
    for number, item in enumerate(gold, 1):
        if not isinstance(item, dict):
            raise ValueError(f"Gold item {number} must be an object")
        if not isinstance(item.get("query"), str) or not item["query"].strip():
            raise ValueError(f"Gold item {number} needs a non-empty query")
        if item.get("category") not in known_categories:
            raise ValueError(f"Gold item {number} has an unknown category")
        expected, near_misses = item.get("expected"), item.get("near_misses")
        if not isinstance(expected, list) or not expected or not all(isinstance(value, str) for value in expected):
            raise ValueError(f"Gold item {number} needs a non-empty expected list")
        if not isinstance(near_misses, list) or not all(isinstance(value, str) for value in near_misses):
            raise ValueError(f"Gold item {number} needs a near_misses list")
        unknown = (set(expected) | set(near_misses)) - known_ids
        if unknown:
            raise ValueError(f"Gold item {number} references unknown card IDs: {sorted(unknown)}")
        if set(expected) & set(near_misses):
            raise ValueError(f"Gold item {number} overlaps expected and near_misses")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", required=True)
    parser.add_argument("--env", default=str(ROOT.parent / ".env"))
    parser.add_argument("--cache", default=str(INDEXES / "query-cache.json"))
    parser.add_argument("--out")
    args = parser.parse_args()
    indexes = load_indexes()
    known_ids = set(indexes["A"]["ids"])
    known_categories = {card["category"] for card in indexes["A"]["cards"]}
    gold = json.loads(Path(args.gold).read_text(encoding="utf-8"))
    validate_gold(gold, known_ids, known_categories)
    finder = load_finder()
    finder.load_env(args.env)
    config = {
        "embed_url": os.environ.get("SKILL_FINDER_EMBED_URL", finder.DEFAULT_EMBED_URL),
        "embed_model": os.environ.get("SKILL_FINDER_EMBED_MODEL", finder.DEFAULT_EMBED_MODEL),
    }
    indexed_config = (indexes["A"]["meta"]["embed_url"], indexes["A"]["meta"]["embed_model"])
    if (config["embed_url"], config["embed_model"]) != indexed_config:
        raise ValueError(
            "Query embedding endpoint/model differs from A/B/C: "
            f"index={indexed_config}, query={(config['embed_url'], config['embed_model'])}"
        )
    query_vectors = finder.embed(
        [item["query"] for item in gold], Path(args.cache), config, "query"
    )
    details = {condition: [] for condition in CONDITIONS}
    for item in gold:
        for condition, index in indexes.items():
            results = ranking(index, condition, item["query"], query_vectors[item["query"]])
            ids = [result["card_id"] for result in results]
            expected, near_misses = set(item["expected"]), set(item["near_misses"])
            details[condition].append({
                "results": results,
                "recall_hit": bool(set(ids) & expected),
                "top1_hit": bool(ids and ids[0] in expected),
                "near_miss_top1": bool(ids and ids[0] in near_misses),
                "near_misses": item["near_misses"],
            })
    categories = defaultdict(list)
    for index, item in enumerate(gold):
        categories[item["category"]].append(index)
    report = {
        "gold": str(Path(args.gold).resolve()),
        "query_count": len(gold),
        "conditions": {},
        "queries": [],
    }
    for condition in CONDITIONS:
        report["conditions"][condition] = {
            "method": CONDITIONS[condition],
            "overall": metrics(details[condition], list(range(len(gold)))),
            "categories": {
                category: metrics(details[condition], indices)
                for category, indices in sorted(categories.items())
            },
        }
    for index, item in enumerate(gold):
        report["queries"].append({
            "query": item["query"],
            "category": item["category"],
            "expected": item["expected"],
            "near_misses": item["near_misses"],
            "conditions": {condition: details[condition][index]["results"] for condition in CONDITIONS},
        })
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
