#!/usr/bin/env python3
import os, sys, json, re, requests
from datetime import datetime, date

BOTHUB_URL = os.environ.get("BOTHUB_URL", "https://openai.bothub.chat/v1/chat/completions")
API_KEY_DATA = os.environ.get("EITHER_API_KEY", "")

if not API_KEY_DATA:
    api_txt = os.path.join(os.path.dirname(__file__), "API.txt")
    if os.path.exists(api_txt):
        with open(api_txt) as f:
            API_KEY_DATA = f.read().strip()

lines = [l.strip() for l in API_KEY_DATA.strip().split("\n") if l.strip()]
models = {}
for line in lines:
    parts = line.split(":", 1)
    if len(parts) == 2:
        models[parts[0]] = parts[1]

MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat-v3-0324")
API_KEY = models.get(MODEL, models.get("deepseek-chat", ""))
if not API_KEY:
    API_KEY = lines[0].split(":", 1)[-1].strip() if lines else ""

if not API_KEY:
    print("No API key found")
    sys.exit(1)

signs = ["Овен","Телец","Близнецы","Рак","Лев","Дева","Весы","Скорпион","Стрелец","Козерог","Водолей","Рыбы"]
today = date.today()
months = ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"]

prompt = f"""Ты — астролог с отличным чувством юмора (офисный/IT юмор с элементами абсурда). Сегодня {today.day} {months[today.month-1]} {today.year}.

Напиши 12 коротких гороскопов для всех знаков зодиака. Темы: офис, IT, работа, коллеги, дедлайны, кофе. Тон: добрый, заряжающий, с лёгким юмором и долей абсурда. Без сарказма и негатива.

Для КАЖДОГО знака нужно 3 поля:
- "body": предсказание дня (1 предложение, обращение на «ты», офисная/IT тематика, при этом слегка абсурдное — будто законы физики слегка перестали работать, но в хорошем смысле)
- "twist": неожиданный поворот (1 предложение, с юмором и абсурдом, про что-то приятное, нелогичное, забавное)
- "advice": совет дня (1 короткое предложение, позитивное, про кофе/чай/отдых/странные ритуалы)

Пример ингредиентов абсурда (не копируй, а вдохновляйся): клавиатура сама печатает код, кофеварка предсказывает будущее, файлы сортируются силой мысли, принтер печатает только хорошие новости, офисный стул стал креслом-качалкой, баги сами себя фиксят.

Также напиши один общий "vibe" — короткую фразу-настройку на день для всей команды (1 предложение, вдохновляюще, с ноткой абсурда).

Ответ дай строго в формате JSON без markdown-обёртки:
{{"vibe": "...", "predictions": [{{"sign": "Овен", "body": "...", "twist": "...", "advice": "..."}}, ...]}}

Знаки по порядку: {", ".join(signs)}."""

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
payload = {
    "model": MODEL,
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.8,
    "max_tokens": 2500,
}

try:
    resp = requests.post(BOTHUB_URL, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
except Exception as e:
    print(f"API error: {e}")
    sys.exit(1)

json_match = re.search(r'\{[\s\S]*\}', content)
if json_match:
    content = json_match.group()

try:
    result = json.loads(content)
except json.JSONDecodeError as e:
    print(f"JSON parse error: {e}")
    print(f"Raw: {content[:500]}")
    sys.exit(1)

if "predictions" not in result or len(result["predictions"]) != 12:
    print(f"Invalid predictions count: {len(result.get('predictions', []))}")
    sys.exit(1)

result["date"] = today.isoformat()
result["generated_at"] = datetime.utcnow().isoformat() + "Z"

out = os.path.join(os.path.dirname(__file__), "data.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"OK — {today.isoformat()} saved to data.json")
