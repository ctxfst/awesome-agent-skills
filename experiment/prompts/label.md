# Independent gold-labeling task

You are the labeling model. You are neither the card author nor the query writer.

Use only the query text and the supplied upstream `SKILL.md` documents. Do not open or request job-line cards, card metadata, card hashes, descriptions extracted into cards, indexes, rankings, evaluation reports, or smoke-test data.

## Input bundle

For each category, the orchestrator will provide:

- The category ID and its entries from `experiment/queries.json`.
- Every candidate as an arbitrary `candidate_id`, its upstream source reference, and the complete raw upstream `SKILL.md` content.

The `candidate_id` is only an output identifier. It is not evidence about suitability. Judge only from the query and the upstream `SKILL.md` text. Do not use file names or repository reputation as a substitute for reading the document.

## Label each query

Read all candidate `SKILL.md` documents for the query's category and identify:

- `expected`: every candidate whose documented scope can satisfy the request. Multiple candidates are allowed. Include a candidate only when its required input, job, and output are compatible with the query.
- `near_misses`: candidates that look relevant by topic or wording but cannot satisfy the request because of their documented input, output, platform, scope, prerequisites, or explicit exclusions.

Do not treat a lower-quality or less-preferred valid solution as a near miss. Do not invent capabilities that are absent from the upstream document. Do not label a candidate as both expected and near miss. If no candidate is suitable, mark the query for orchestrator review instead of guessing an answer.

Preserve the original `id`, `category`, and `query` exactly. Add `expected` and `near_misses` lists containing `candidate_id` values. A short evidence note per listed candidate may be added as `evidence`, keyed by `candidate_id`, but it must quote or point to the upstream `SKILL.md` text.

Write the combined result to `experiment/gold.json` as a JSON list. Do not run retrieval or evaluation. Do not modify the queries, any Skill source, or any other file.

After writing, validate that every label references a supplied candidate, expected and near misses are disjoint, and every category has all 15 queries labeled. Leave the separate human spot-check of 20 labels to the orchestrator.
