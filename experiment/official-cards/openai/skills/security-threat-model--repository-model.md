---
skill: security-threat-model
source: openai/skills
path: skills/.curated/security-threat-model
commit: 49f948faa9258a0c61caceaf225e179651397431
url: https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-threat-model
license: Apache-2.0
description: Repository-grounded threat modeling that enumerates trust boundaries, assets, attacker capabilities, abuse paths, and mitigations, and writes a concise Markdown threat model. Trigger only when the user explicitly asks to threat model a codebase or path, enumerate threats/abuse paths, or perform AppSec threat modeling. Do not trigger for general architecture summaries, code review, or non-security design work.
trust: T1
has_scripts: false
network: false
needs_secrets: false
---

# Write a repository-grounded threat model with evidence-backed abuse paths

## When
Use when the user explicitly asks to threat model a repository or path, enumerate threats or abuse paths, or perform AppSec threat modeling.

## Material
A repository root and in-scope paths, intended usage and deployment context when known, repository evidence, the bundled prompt template, and user clarification of assumptions that affect scope or priority.

## Done
A concise Markdown file named after the repository or directory, covering components, trust boundaries, assets, entry points, attacker capabilities, prioritized abuse paths, existing and recommended mitigations, assumptions, and open questions.

## Requires
Repository evidence for architectural claims and the bundled output contract in references/prompt-template.md. Material assumptions must be validated with the user before the final report, or explicitly retained when unanswered.

## Replaces
Generic security checklists whose components, controls, threats, and mitigations are not tied to concrete repository evidence.

## Not for
General architecture summaries, ordinary code review, non-security design work, or a language-specific security best-practices report.
