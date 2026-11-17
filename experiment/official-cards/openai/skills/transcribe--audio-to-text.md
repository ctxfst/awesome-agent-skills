---
skill: transcribe
source: openai/skills
path: skills/.curated/transcribe
commit: 49f948faa9258a0c61caceaf225e179651397431
url: https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/transcribe
license: Apache-2.0
description: Transcribe audio files to text with optional diarization and known-speaker hints. Use when a user asks to transcribe speech from audio/video, extract text from recordings, or label speakers in interviews or meetings.
trust: T1
has_scripts: true
network: true
needs_secrets: true
---

# Transcribe recordings with optional speaker labels

## When
Use when transcribing speech from audio or video, extracting text from recordings, or labeling speakers in interviews and meetings.

## Material
Audio file paths, desired text, json, or diarized_json response format, an optional language hint, and optional known-speaker reference clips.

## Done
A transcript saved at the requested output path, validated for transcription quality, speaker labels when requested, and segment boundaries.

## Requires
Network access, OPENAI_API_KEY set locally, the OpenAI Python package, and the bundled transcribe_diarize.py CLI. Diarization uses gpt-4o-transcribe-diarize; fast text defaults to gpt-4o-mini-transcribe.

## Replaces
missing

## Not for
missing
