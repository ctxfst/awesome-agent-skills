---
skill: podcast-generation
source: microsoft/skills
path: .github/skills/podcast-generation
commit: b35d2c60fac796bfd2cfd14ad3f550c73e92d9bb
url: https://github.com/microsoft/skills/tree/b35d2c60fac796bfd2cfd14ad3f550c73e92d9bb/.github/skills/podcast-generation
license: MIT
description: Generate AI-powered podcast-style audio narratives using Azure OpenAI's GPT Realtime Mini model via WebSocket. Use when building text-to-speech features, audio narrative generation, podcast creation from content, or integrating with Azure OpenAI Realtime API for real audio output. Covers full-stack implementation from React frontend to Python FastAPI backend with WebSocket streaming.
trust: T1
has_scripts: true
network: true
needs_secrets: true
---

# Build a podcast-style audio narrative with Azure OpenAI Realtime

## When
Use when building text-to-speech features, generating podcast-style audio narratives from content, or integrating Azure OpenAI Realtime audio output into a React and FastAPI application.

## Material
Text content or a prompt to narrate, an Azure OpenAI Realtime deployment, and the application backend and frontend that will stream and play the audio.

## Done
A real audio narrative streamed as PCM chunks with transcript events, converted to 24 kHz, 16-bit mono WAV and returned as base64 audio for browser playback.

## Requires
Network access, AZURE_OPENAI_AUDIO_API_KEY, AZURE_OPENAI_AUDIO_ENDPOINT, AZURE_OPENAI_AUDIO_DEPLOYMENT, the OpenAI SDK with WebSocket support, and the bundled pcm_to_wav.py conversion script.

## Replaces
missing

## Not for
missing
