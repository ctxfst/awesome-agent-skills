---
skill: internal-linking
source: Illyism/seo-skills
path: seo/internal-linking
commit: 99d51a33db135cf278c7e61cf3dd1b502e2390b4
url: https://github.com/Illyism/seo-skills/tree/99d51a33db135cf278c7e61cf3dd1b502e2390b4/seo/internal-linking
license: missing
description: Runs reverse internal linking ("traffic-to-money routing") in the user's repo, editing high-traffic informational posts in place to pass contextual links and prefilled tool callouts to `/pricing`, `/use-cases/*`, `/vs/*`, and `/tools/*`, and ships a before/after inbound-link table. Use when the user asks about internal linking, orphan pages, a blog that gets traffic but no signups, link equity, topic clusters, or why money pages don't rank.
trust: T3
category: seo
has_scripts: true
network: true
needs_secrets: false
---

# Internal Linking

## When
Runs reverse internal linking ("traffic-to-money routing") in the user's repo, editing high-traffic informational posts in place to pass contextual links and prefilled tool callouts to `/pricing`, `/use-cases/*`, `/vs/*`, and `/tools/*`, and ships a before/after inbound-link table. Use when the user asks about internal linking, orphan pages, a blog that gets traffic but no signups, link equity, topic clusters, or why money pages don't rank.

## Material
missing

## Done
Every run ends with:

1. `scripts/internal-link-graph.mjs` and `seo/internal-link-graph.json` (before and after runs).
2. In-place edits to SOURCE posts: contextual links and 1 callout each.
3. New or fixed hub/index pages and breadcrumbs.
4. `seo/internal-links-report.md` with the before/after table and remaining orphans.

## Requires
missing

## Replaces
missing

## Not for
missing
