#!/usr/bin/env python3
"""Build one selection file per arm: all 100 anonymized descriptions + the 75 main queries (no categories, no answers)."""
import json, random
from pathlib import Path
D = Path(__file__).resolve().parent; EXP = D.parent
queries = json.loads((EXP / "queries.json").read_text())
random.seed(5); order = list(range(len(queries))); random.shuffle(order)
qs = [{"qid": f"q{n+1:02d}", "query": queries[i]["query"]} for n, i in enumerate(order)]
json.dump({f"q{n+1:02d}": queries[i]["id"] for n, i in enumerate(order)}, open(D / "qmap.json", "w"), indent=1)
for arm in ("original", "sixslot", "generic"):
    descs = {x["sid"]: x["description"] for x in json.loads((D / f"{arm}.json").read_text())}
    assert len(descs) == 100, arm
    json.dump({"skills": [{"sid": s, "description": descs[s]} for s in sorted(descs)], "queries": qs},
              open(D / f"select-{arm}.json", "w"), ensure_ascii=False, indent=1)
    print(arm, "avg len", sum(map(len, descs.values())) // 100)
