#!/usr/bin/env python3
import json
from pathlib import Path
D = Path(__file__).resolve().parent; EXP = D.parent
import sys
V = len(sys.argv) > 1 and sys.argv[1] == "vague"
mapping = json.loads((D / "mapping.json").read_text())
qmap = json.loads((D / ("vmap.json" if V else "qmap.json")).read_text())
gold = {x["id"]: x for x in json.loads((EXP / ("ask/vague-gold.json" if V else "gold.json")).read_text())}
N = len(qmap)
res = {}
for arm in ("original", "sixslot", "generic"):
    p = D / (f"vpicks-{arm}.json" if V else f"picks-{arm}.json")
    if not p.exists(): continue
    picks = {x["qid"]: x for x in json.loads(p.read_text())}
    hit = near = hit3 = 0; per = {}
    for qid, gid in qmap.items():
        g = gold[gid]; pk = picks[qid]
        first = mapping.get(pk["choice"]); top3 = [mapping.get(s) for s in pk.get("top3", [])]
        h = first in g["expected"]; hit += h; near += first in g["near_misses"]; hit3 += bool(set(top3) & set(g["expected"]))
        per[qid] = h
        c = g["category"]; per.setdefault("_" + c, []).append(h)
    res[arm] = per
    print(f"{arm:9} top1 {hit/N:.2f}  near-miss {near/N:.2f}  in-top3 {hit3/N:.2f}  " +
          "  ".join(f"{k[1:5]}:{sum(v)/len(v):.2f}" for k, v in per.items() if k.startswith("_")))
if "original" in res:
    for arm in ("sixslot", "generic"):
        if arm in res:
            a, b = res[arm], res["original"]
            print(f"{arm} vs original: wins {sum(a[q] and not b[q] for q in qmap)}, losses {sum(b[q] and not a[q] for q in qmap)}")
    if "sixslot" in res and "generic" in res:
        a, b = res["sixslot"], res["generic"]
        print(f"sixslot vs generic: wins {sum(a[q] and not b[q] for q in qmap)}, losses {sum(b[q] and not a[q] for q in qmap)}")
