#!/usr/bin/env python3
"""Дневной гороскоп: LLM → data.json. Использует общий llm_gateway."""
import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
SCRIPTS = BASE.parent.parent / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from llm_gateway import LLMGateway  # noqa: E402

MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat-v3-0324")

SIGNS = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
         "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля",
          "августа", "сентября", "октября", "ноября", "декабря"]

SCHEMA = {"vibe": ("str", True, None), "predictions": ("list", True, None)}
PREDICTION_SCHEMA = {
    "sign": ("str", True, None),
    "body": ("str", True, None),
    "twist": ("str", True, None),
    "advice": ("str", True, None),
}


def build_prompt():
    today = date.today()
    return f"""Ты — астролог с отличным чувством юмора (офисный/IT юмор с элементами абсурда). Сегодня {today.day} {MONTHS[today.month - 1]} {today.year}.

Напиши 12 коротких гороскопов для всех знаков зодиака. Темы: офис, IT, работа, коллеги, дедлайны, кофе. Тон: добрый, заряжающий, с лёгким юмором и долей абсурда. Без сарказма и негатива.

Для КАЖДОГО знака нужно 3 поля:
- "body": предсказание дня (1 предложение, обращение на «ты», офисная/IT тематика, при этом слегка абсурдное — будто законы физики слегка перестали работать, но в хорошем смысле)
- "twist": неожиданный поворот (1 предложение, с юмором и абсурдом, про что-то приятное, нелогичное, забавное)
- "advice": совет дня (1 короткое предложение, позитивное, про кофе/чай/отдых/странные ритуалы)

Пример ингредиентов абсурда (не копируй, а вдохновляйся): клавиатура сама печатает код, кофеварка предсказывает будущее, файлы сортируются силой мысли, принтер печатает только хорошие новости, офисный стул стал креслом-качалкой, баги сами себя фиксят.

Также напиши один общий "vibe" — короткую фразу-настройку на день для всей команды (1 предложение, вдохновляюще, с ноткой абсурда).

Ответ дай строго в формате JSON без markdown-обёртки:
{{"vibe": "...", "predictions": [{{"sign": "Овен", "body": "...", "twist": "...", "advice": "..."}}, ...]}}

Знаки по порядку: {", ".join(SIGNS)}."""


def main():
    gateway = LLMGateway()
    gateway.auto_configure(base_dir=BASE)

    if not gateway.providers:
        print("No API keys found (API.txt / env)", file=sys.stderr)
        sys.exit(1)

    result = gateway.call_json(
        build_prompt(),
        schema=SCHEMA,
        item_schema=PREDICTION_SCHEMA,
        model=MODEL,
        temperature=0.8,
        max_tokens=2500,
    )

    if result is None:
        print("API error: no valid response from any provider", file=sys.stderr)
        sys.exit(1)

    preds = result.get("predictions", [])
    signs = {p.get("sign") for p in preds if isinstance(p, dict)}
    if len(preds) != 12 or signs != set(SIGNS):
        print(f"Invalid predictions: {len(preds)} signs {sorted(signs)}", file=sys.stderr)
        sys.exit(1)

    today = date.today()
    result["date"] = today.isoformat()
    result["generated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    out = BASE / "data.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK — {today.isoformat()} saved to data.json")


if __name__ == "__main__":
    main()
