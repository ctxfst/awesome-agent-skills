# Validation results

English | [繁體中文](RESULTS.zh-TW.md)

This file summarizes three rounds of experiments: retrieval, asking a question after seeing candidates, and rewriting descriptions on the author side. The numbers come from `experiment/report.json`, `experiment/ask/report-*.json`, and the picks in `experiment/desc/` as scored by `score.py`. The rounds used separate samples, so hit rates from different rounds should not be compared as if they came from the same queries.

## 1. Retrieval: description, full document, job-line card, BM25

75 queries, 15 in each of five categories. A embeds the original description; B embeds the first 4,000 characters of `SKILL.md`; C embeds the job-line card; D runs BM25 over the full `SKILL.md`.

| Condition | Recall@5 | Top-1 hit rate | Near-miss rate |
|---|---:|---:|---:|
| A: description | 0.827 | 0.453 | 0.307 |
| B: first 4,000 characters of SKILL.md | 0.867 | 0.467 | 0.280 |
| C: job-line card | 0.773 | 0.493 | 0.227 |
| D: BM25 | 0.480 | 0.293 | 0.080 |

Top-1 hit rate by category:

| Category | A | B | C | D |
|---|---:|---:|---:|---:|
| API development | 0.667 | 0.667 | 0.667 | 0.333 |
| Frontend design | 0.200 | 0.267 | 0.333 | 0.267 |
| SEO | 0.600 | 0.667 | 0.667 | 0.467 |
| Social media publishing | 0.400 | 0.333 | 0.467 | 0.333 |
| Test automation | 0.400 | 0.400 | 0.333 | 0.067 |

Conclusion: C has the highest top-1 hit rate but the lowest Recall@5, and it does not lead in every category. B has the highest Recall@5. D has the lowest near-miss rate, but its other retrieval metrics are clearly weaker. We cannot claim that job-line cards beat descriptions or full documents overall.

Limitations: only 75 queries; the near-miss rate only checks whether the first result is a labeled near miss; candidates within a category are very similar; the job-line cards were mostly extracted from upstream text by fixed rules, so the results describe this implementation only, not hand-written cards in general.

## 2. Asking: direct search versus a question after seeing candidates

20 vague requests. `direct` is the original vague request. `targeted` adds the user's answer to a question written after reading the job-line cards. `raw_targeted` adds the answer to a question written from the original descriptions only. `generic` adds the answer to a fixed generic question. `full_intent` gives the complete request directly, as a reference upper bound.

| Condition | Arm | Recall@5 | Top-1 hit rate | Near-miss rate |
|---|---|---:|---:|---:|
| A: description | direct | 0.850 | 0.500 | 0.250 |
| A | targeted | 1.000 | 0.750 | 0.200 |
| A | raw_targeted | 1.000 | 0.750 | 0.100 |
| A | generic | 0.900 | 0.800 | 0.150 |
| A | full_intent | 0.950 | 0.700 | 0.050 |
| B: first 4,000 characters of SKILL.md | direct | 0.950 | 0.400 | 0.300 |
| B | targeted | 0.950 | 0.650 | 0.250 |
| B | raw_targeted | 1.000 | 0.700 | 0.200 |
| B | generic | 0.900 | 0.700 | 0.150 |
| B | full_intent | 0.850 | 0.650 | 0.100 |
| C: job-line card | direct | 0.800 | 0.450 | 0.100 |
| C | targeted | 0.950 | 0.700 | 0.200 |
| C | raw_targeted | 0.900 | 0.700 | 0.050 |
| C | generic | 0.800 | 0.650 | 0.200 |
| C | full_intent | 0.900 | 0.800 | 0.100 |
| D: BM25 | direct | 0.200 | 0.100 | 0.100 |
| D | targeted | 0.500 | 0.300 | 0.050 |
| D | raw_targeted | 0.450 | 0.100 | 0.000 |
| D | generic | 0.400 | 0.200 | 0.150 |
| D | full_intent | 1.000 | 0.800 | 0.050 |

Conclusion: under C, the top-1 hit rate rises from 0.45 for direct search to 0.70 for both targeted and raw_targeted. Questions written from the original descriptions did as well as questions written from job-line cards, so the product does not need job-line cards. The generic question also does well in some conditions, so not all of the gain can be credited to analyzing how candidates differ.

Limitations: only 20 requests; the answers were produced by a model playing the user; the text of full_intent differs in distribution from the request-plus-answer queries, so more information does not guarantee a better rank in every arm; adding correct answers does not necessarily lower the near-miss rate; no usable score threshold was found.

## 3. Author side: rewriting descriptions

Each upstream description was kept as is (`original`), rewritten as a six-slot paragraph (`sixslot`), or rewritten with general writing guidance (`generic`). The comparison measures how well a model picks the right Skill from the candidate descriptions. It does not rebuild the embedding index.

75 regular queries:

| Description version | Top-1 hit rate | Near-miss rate | Top-3 hit rate |
|---|---:|---:|---:|
| original | 0.880 | 0.040 | 0.987 |
| sixslot | 0.867 | 0.027 | 0.973 |
| generic | 0.893 | 0.040 | 0.987 |

20 vague queries:

| Description version | Top-1 hit rate | Near-miss rate | Top-3 hit rate |
|---|---:|---:|---:|
| original | 0.900 | 0.100 | 1.000 |
| sixslot | 0.800 | 0.200 | 1.000 |
| generic | 0.850 | 0.150 | 1.000 |

Conclusion: the six-slot rewrite did not improve this selection task. Against original, sixslot won 5 and lost 6 on regular queries and won 0 and lost 2 on vague queries. The generic rewrite gave no consistent advantage either. The six slots can only be offered as a writing checklist; we cannot claim they improve retrieval or selection.

Limitations: this round tested a model choosing after reading descriptions, not the six-slot text used as a new embedding index; rewrite quality and how much information the upstream description carries affect the results; with only 20 vague queries, small numbers of cases can swing the difference.
