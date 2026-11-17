---
skill: define-goal
source: openai/skills
path: skills/.curated/define-goal
commit: 49f948faa9258a0c61caceaf225e179651397431
url: https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/define-goal
license: Apache-2.0
description: Help the user define a concrete, measurable goal before starting work, especially when they ask to use the goal tool, create a goal, set an objective, clarify success criteria, or turn a fuzzy intention into a quantitative outcome. Use this skill for goal creation and goal refinement only; it does not manage durable snapshots, decision logs, or long-running execution artifacts.
trust: T1
has_scripts: false
network: false
needs_secrets: false
---

# Turn a fuzzy intention into a measurable goal with explicit completion evidence

## When
Use before starting work when the user asks to create or refine a goal, set an objective, clarify success criteria, or turn a fuzzy intention into a measurable outcome.

## Material
The user's intention, the artifact or behavior involved, available validation methods, scope boundaries, and any active goal state returned by get_goal.

## Done
A concise objective naming the concrete outcome, verification evidence, quantitative or binary success threshold, relevant scope bounds, and a stop condition. create_goal is called only after this quality bar is met.

## Requires
Access to get_goal and create_goal when a durable goal is actually requested. Ordinary implementation work should be done directly instead of forcing goal creation.

## Replaces
Pure activity goals such as make progress, keep investigating, improve things, or work on a topic without a verifiable outcome.

## Not for
Ordinary implementation without an explicit goal request, or management of durable snapshots, decision logs, ledgers, resume files, and long-running execution artifacts.
