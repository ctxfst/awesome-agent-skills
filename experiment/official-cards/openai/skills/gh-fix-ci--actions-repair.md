---
skill: gh-fix-ci
source: openai/skills
path: skills/.curated/gh-fix-ci
commit: 49f948faa9258a0c61caceaf225e179651397431
url: https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci
license: Apache-2.0
description: Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions; use `gh` to inspect checks and logs, summarize failure context, draft a fix plan, and implement only after explicit approval. Treat external providers (for example Buildkite) as out of scope and report only the details URL.
trust: T1
has_scripts: true
network: true
needs_secrets: true
---

# Diagnose and repair failing GitHub Actions PR checks

## When
Use when a user asks to debug or fix failing GitHub pull request checks that run in GitHub Actions.

## Material
A repository path, an optional PR number or URL or the current branch PR, and access to the failing GitHub Actions checks and logs.

## Done
Failure names, run URLs, and concise log snippets are summarized; a fix plan is approved before implementation; approved changes and tests are summarized; and relevant checks are rechecked.

## Requires
Network access, the GitHub CLI authenticated with suitable repository and workflow scopes, and optionally the bundled inspect_pr_checks.py helper. Implementation requires explicit user approval.

## Replaces
missing

## Not for
Buildkite or other external check providers; only report their details URL. Do not implement a fix before explicit approval.
