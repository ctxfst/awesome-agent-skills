---
skill: kql
source: microsoft/skills
path: .github/skills/kql
commit: b35d2c60fac796bfd2cfd14ad3f550c73e92d9bb
url: https://github.com/microsoft/skills/tree/b35d2c60fac796bfd2cfd14ad3f550c73e92d9bb/.github/skills/kql
license: MIT
description: >-
  KQL language expertise for writing correct, efficient Kusto Query Language queries. Covers syntax gotchas, join patterns, dynamic types, datetime pitfalls, regex patterns, serialization, memory management, result-size discipline, and advanced functions (geo, vector, graph). USE THIS SKILL whenever writing, debugging, or reviewing KQL queries — even simple ones — because the gotchas section prevents the most common errors that waste tool calls and cause expensive retry cascades. Trigger on: KQL, Kusto, ADX, Azure Data Explorer, Fabric Real-Time Intelligence, EventHouse, Log Analytics, log analysis, data exploration, time series, anomaly detection, summarize, where clause, join, extend, project, let statement, parse operator, extract function, any mention of pipe-forward query syntax.
trust: T1
has_scripts: false
network: false
needs_secrets: false
---

# Write, debug, or review efficient KQL queries

## When
Use whenever writing, debugging, or reviewing KQL for Azure Data Explorer, Fabric Real-Time Intelligence, EventHouse, Log Analytics, Microsoft Sentinel, log analysis, time series, or anomaly detection.

## Material
A KQL query or analysis goal, relevant table schemas and column types, data volumes, time ranges, and any query error messages. Examples can optionally run against the public Kusto help cluster.

## Done
A syntactically correct, efficient query with dynamic columns cast where required, safe join cardinality, pre-filtering before aggregation, bounded result sizes, valid datetime literals, and specific error-based fixes.

## Requires
A KQL-compatible data source for execution; query writing and review can use the documented patterns without network access. The public help cluster is optional for runnable examples.

## Replaces
Switching to Python or an unrelated query strategy after a KQL error instead of fixing the specific syntax or escaping problem.

## Not for
missing
