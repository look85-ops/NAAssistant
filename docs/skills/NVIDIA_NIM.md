# NVIDIA NIM (OpenAI-compatible) — Pilot Setup

## Why
- Free access to >50 models (Llama, Gemma, Mistral, DeepSeek, GLM, MiniMax).
- OpenAI-compatible endpoints; easy switch for our tooling.

## Setup
- Get API key: https://build.nvidia.com
- Environment:
  - `NVIDIA_API_KEY=<your key>`
  - Base URL: `https://integrate.api.nvidia.com/v1`

## Models To Test
- `meta/llama-3.1-8b-instruct` (PR summaries)
- `deepseek-ai/deepseek-v4` (RU writing)
- `minimaxai/minimax-m2.7` or `thudm/glm-4.7` (RU analysis)

## cURL Example
```
curl -X POST "https://integrate.api.nvidia.com/v1/chat/completions" \
 -H "Authorization: Bearer $NVIDIA_API_KEY" \
 -H "Content-Type: application/json" \
 -d '{
   "model": "meta/llama-3.1-8b-instruct",
   "messages": [{"role":"user","content":"Summarize: <text>"}]
 }'
```

## Acceptance Criteria (F-029)
- Key obtained; endpoint configured
- Test script added and 3 models validated
- Quality/latency compared on 3 prompts
- Decision recorded in `logs/decisions.md`

## Fallback: OpenRouter (when NVIDIA is unavailable)
- Base URL: `https://openrouter.ai/api/v1`
- Env: `OPENROUTER_API_KEY`
- Defaults used in pilot:
  - EN PR summary: `meta-llama/llama-3.1-8b-instruct`
  - RU drafts/analysis: `deepseek/deepseek-chat`
  - Notes: use strict prompts for concise RU output; measure latency for each call
