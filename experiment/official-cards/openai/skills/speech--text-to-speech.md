---
skill: speech
source: openai/skills
path: skills/.curated/speech
commit: 49f948faa9258a0c61caceaf225e179651397431
url: https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/speech
license: Apache-2.0
description: Use when the user asks for text-to-speech narration or voiceover, accessibility reads, audio prompts, or batch speech generation via the OpenAI Audio API; run the bundled CLI (`scripts/text_to_speech.py`) with built-in voices and require `OPENAI_API_KEY` for live calls. Custom voice creation is out of scope.
trust: T1
has_scripts: true
network: true
needs_secrets: true
---

# Generate narration or voice prompts from exact text

## When
Use for text-to-speech narration, voiceovers, accessibility reads, audio prompts, and single or batch speech generation through the OpenAI Audio API.

## Material
Exact input text, desired built-in voice, delivery style, output format, and constraints. Batch work uses one temporary JSONL job per output.

## Done
Spoken audio saved at the requested output paths, with important clips checked for intelligibility, pacing, pronunciation, and constraint adherence, plus the final text, instructions, and flags recorded.

## Requires
Network access, OPENAI_API_KEY set locally, the OpenAI Python SDK, and the bundled text_to_speech.py CLI. Input is limited to 4096 characters per request and the CLI caps requests at 50 per minute.

## Replaces
missing

## Not for
Custom voice creation.
