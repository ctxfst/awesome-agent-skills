#!/usr/bin/env python3
"""Build the asker's input: each vague query with its top-8 job-line cards (condition C). No true_intent."""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP))
import evaluate as ev

idx = ev.load_indexes()["C"]
finder = ev.load_finder(); finder.load_env(str(EXP.parent.parent / ".env"))
config = {"embed_url": idx["meta"]["embed_url"], "embed_model": idx["meta"]["embed_model"]}
vague = json.loads((EXP / "vague-queries.json").read_text())
vecs = finder.embed([v["query"] for v in vague], EXP / "indexes/query-cache.json", config, "query")
out = []
for v in vague:
    scores = idx["vectors"] @ vecs[v["query"]]
    top = scores.argsort()[::-1][:8]
    cands = []
    for i in top:
        cid = idx["ids"][i]
        text = (EXP / "cards" / f"{cid}.md").read_text()
        body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S).strip()
        cands.append({"card_id": cid, "score": round(float(scores[i]), 4), "card": body})
    out.append({"id": v["id"], "query": v["query"], "candidates": cands})
(HERE / "asker-input.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print("wrote", len(out))
