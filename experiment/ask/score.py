#!/usr/bin/env python3
"""Score the follow-up-question test: direct vs generic question vs targeted question vs full intent (upper bound)."""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; EXP = HERE.parent
gold = {x["id"]: x for x in json.loads((HERE / "vague-gold.json").read_text())}
ans = {x["id"]: x for x in json.loads((HERE / "answers.json").read_text())}
vague = {x["id"]: x for x in json.loads((EXP / "vague-queries.json").read_text())}
raw_path = HERE / "raw-answers.json"
raw = {x["id"]: x for x in json.loads(raw_path.read_text())} if raw_path.exists() else None
arms = {
    "direct": lambda i: vague[i]["query"],
    "generic": lambda i: vague[i]["query"] + "\n" + ans[i]["generic_answer"],
    "targeted": lambda i: vague[i]["query"] + ("\n" + ans[i]["targeted_answer"] if ans[i].get("targeted_answer") else ""),
    "full_intent": lambda i: vague[i]["true_intent"],
}
if raw:
    arms["raw_targeted"] = lambda i: vague[i]["query"] + ("\n" + raw[i]["answer"] if raw[i].get("answer") else "")
summary = {}
for arm, make in arms.items():
    g = []
    for i, x in gold.items():
        y = dict(x); y["query"] = make(i)
        y.pop("needs_review", None); y.pop("evidence", None)
        g.append(y)
    gp = HERE / f"gold-{arm}.json"; gp.write_text(json.dumps(g, ensure_ascii=False, indent=1))
    rp = HERE / f"report-{arm}.json"
    subprocess.run([sys.executable, str(EXP / "evaluate.py"), "--gold", str(gp), "--out", str(rp)], check=True, stdout=subprocess.DEVNULL)
    r = json.loads(rp.read_text())
    summary[arm] = {c: r["conditions"][c]["overall"] for c in "ABCD"}
    summary[arm]["_queries"] = r["queries"]
print("arm          cond  R@5   top1  nearmiss")
for arm in arms:
    for c in "ABCD":
        o = summary[arm][c]
        print(f"{arm:12} {c}     {o['recall_at_5']:.2f}  {o['top1_accuracy']:.2f}  {o['near_miss_top1_rate'] if o['near_miss_top1_rate'] is not None else float('nan'):.2f}")
# paired targeted vs generic / direct on C
def hits(arm, c):
    return [q["conditions"][c][0]["card_id"] in set(q["expected"]) for q in summary[arm]["_queries"]]
for c in "ABC":
    for other in ("direct", "generic") + (("raw_targeted",) if raw else ()):
        t, o = hits("targeted", c), hits(other, c)
        print(f"{c}: targeted vs {other}: wins {sum(a and not b for a,b in zip(t,o))}, losses {sum(b and not a for a,b in zip(t,o))}")
