import os
import re
import sys
import json
import random
from datetime import datetime, timezone
from pathlib import Path

import requests

POSTS_DIR = Path(__file__).resolve().parent.parent / "career" / "posts"
API_FILE = Path(__file__).resolve().parent.parent / "API.txt"

LND_TOPICS = [
    ("AI в обучении", "как ИИ меняет роль методиста, а не заменяет его"),
    ("L&D метрики", "что реально измерять в обучении, а не для галочки"),
    ("Проектирование обучения", "почему хороший сценарий важнее хорошей платформы"),
    ("ИИ-инструменты для L&D", "ChatGPT, Claude, генерация контента — что работает"),
    ("Карьера в L&D", "как расти методисту и куда"),
    ("Ошибки в обучении", "что я перестала делать в сценариях и почему"),
    ("Мотивация взрослых", "почему «чтобы сдали тест» — не мотивация"),
    ("Тренды EdTech 2026", "что реально дошло до корпоративного обучения"),
    ("Методист и ИИ", "как я использую нейросети в работе над курсами"),
    ("Коммуникация с экспертами", "как вытащить знания из головы предметника"),
]

WEEKS = [
    "практический инструмент или лайфхак",
    "личная история с выводом",
    "анализ тренда или новости",
    "рефлексия: ошибка + урок",
]

def get_week_number():
    jan1 = datetime.now(timezone.utc).replace(month=1, day=1, hour=0, minute=0, second=0)
    days_since = (datetime.now(timezone.utc) - jan1).days
    return (days_since // 7) + 1

def get_api_backend():
    key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("LLM_KEY")
    if key:
        return "deepseek", key

    if API_FILE.exists():
        for line in API_FILE.read_text("utf-8").strip().split("\n"):
            line = line.strip()
            if ":" in line and line.startswith("deepseek"):
                parts = line.split(":", 1)
                return parts[0], parts[1]

    bothub_url = os.environ.get("BOTHUB_URL", "https://openai.bothub.chat/v1")
    bothub_key = os.environ.get("BOTHUB_KEY")
    if bothub_key:
        return bothub_url, bothub_key

    print("[linkedin] no API key found")
    sys.exit(1)

def call_llm(prompt):
    model_key, key = get_api_backend()
    if "bothub" in model_key or "chat" in model_key:
        url = f"{model_key}/chat/completions" if not model_key.startswith("http") else f"{model_key.rstrip('/')}/chat/completions"
    else:
        url = "https://api.deepseek.com/v1/chat/completions"
        model_key = "deepseek-chat"

    if not url.endswith("/chat/completions"):
        url = url.rstrip("/") + "/chat/completions"

    payload = {
        "model": "deepseek-chat-v3-0324",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9,
        "max_tokens": 800,
        "top_p": 0.95,
    }
    headers = {"Authorization": f"Bearer {key}"}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=180)
        if resp.status_code >= 400:
            raise RuntimeError(f"HTTP {resp.status_code}")
        data = resp.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        print(f"[linkedin] LLM call failed: {e}")
        return ""

def generate_post():
    week = get_week_number()
    topic_title, topic_seed = LND_TOPICS[week % len(LND_TOPICS)]
    style = WEEKS[week // len(LND_TOPICS) % len(WEEKS)]

    prompt = f"""Write a LinkedIn post in Russian for an L&D professional who works at the intersection of learning design and AI.

Topic: {topic_title} — {topic_seed}
Style: {style}

Guidelines:
- Hook in the first 2 lines
- Personal voice, not corporate
- 800-1200 chars
- 2-3 short paragraphs
- One provocative or useful insight
- No emojis
- Hashtags at the end: 3-5 relevant ones (in Russian)
- End with a question or CTA for comments

Write the post draft. First line is the post title (not published, just for reference)."""

    result = call_llm(prompt)
    if not result:
        print("[linkedin] empty response")
        return

    lines = result.strip().split("\n")
    title = lines[0].strip().strip("#").strip()
    body = "\n".join(lines[1:]).strip() if len(lines) > 1 else result

    today = datetime.now(timezone.utc)
    filename = f"{today.strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')[:50]}.md"
    full_path = POSTS_DIR / filename

    content = f"# {title}\n\n{body}\n\n---\n*Generated for week {week}*\n"
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding="utf-8")
    print(f"[linkedin] saved: {filename}")

if __name__ == "__main__":
    generate_post()
