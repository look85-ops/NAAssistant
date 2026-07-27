import os, json, sys, re
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

API_KEY = (os.environ.get("BOTHUB_API_KEY") or "").strip()
API_URL = os.environ.get("BOTHUB_API_URL", "https://openai.bothub.chat/v1/chat/completions")
if not API_KEY:
    print("BOTHUB_API_KEY not set")
    sys.exit(1)

SIGNAL_DIR = "knowledge/signal"
OUTPUT_DIR = "career/posts/digest"
MODELS = ["gpt-4o-mini", "claude-sonnet-4-20250514", "gemini-2.0-flash"]

MONTHS_RU = ["января","февраля","марта","апреля","мая","июня",
              "июля","августа","сентября","октября","ноября","декабря"]

def find_latest_signal():
    md_files = sorted(Path(SIGNAL_DIR).glob("*.md"))
    if not md_files:
        print("No signal markdown files found")
        sys.exit(1)
    return md_files[-1]

def call_llm(signal_text):
    signal_date = find_latest_signal().stem
    try:
        dt = datetime.strptime(signal_date, "%Y-%m-%d")
        display_date = f"{dt.day} {MONTHS_RU[dt.month-1]} {dt.year}"
    except:
        display_date = signal_date

    system_prompt = """Ты — методист и edtech-аналитик, пишешь дайджест L&D × AI для русскоязычных L&D-специалистов.

Ниже — сырой дайджест (Signal) с фактами, данными и источниками за неделю. Твоя задача: превратить его в читаемый, структурированный выпуск дайджеста.

Структура (строго):
## Кейс недели (120-180 слов)
Один главный сюжет из Signal — самый важный для L&D. Цифры, компания, вывод. ОБЯЗАТЕЛЬНО со ссылкой на источник из Signal.

## Инструмент под задачу (40-60 слов)
«Если надо сделать X — попробуй Y». Берёшь инструмент из Signal.

## Рынок / Карьера (40-60 слов)
Один ключевой факт из Signal про рынок или карьеру.

## Творчество / Проекты (40-60 слов)
Один вдохновляющий сюжет из Signal.

## Рекомендация (1-2 предложения)
Конкретное действие на неделю, основанное на Signal.

Правила:
- Каждый факт должен быть из Signal — не выдумывай.
- Источники — только те, что в Signal.
- Пиши по-русски, без канцелярита, без «в эпоху цифровизации».
- Без эмодзи."""

    user_prompt = f"""Ниже — Signal #{signal_date}. Сделай из него выпуск дайджеста L&D × AI.

SIGNAL:
{signal_text}

Дата выпуска: {display_date}"""

    errors = []
    for model in MODELS:
        try:
            data = json.dumps({
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }).encode()
            req = Request(API_URL, data=data, headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            })
            resp = json.loads(urlopen(req).read())
            return resp["choices"][0]["message"]["content"]
        except Exception as e:
            errors.append(f"{model}: {e}")
            continue
    print("All models failed.")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

def build_html(md_text, signal_date):
    try:
        dt = datetime.strptime(signal_date, "%Y-%m-%d")
        display_date = f"{dt.day} {MONTHS_RU[dt.month-1]} {dt.year}"
    except:
        display_date = signal_date

    parts = md_text.split("## ")
    blocks = []
    for p in parts[1:]:
        lines = p.strip().split("\n")
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        blocks.append((title, body))

    rec = ""
    sections_html = ""
    for title, body in blocks:
        if "Рекомендация" in title:
            rec = re.sub(r'^\*+|\*+$', '', body).strip()
            continue
        body_html = body.replace("\n", "<br>")
        sections_html += f"""  <div class="section">
    <h2>{title}</h2>
    <p>{body_html}</p>
  </div>
"""

    rec_html = f"""  <div class="section">
    <h2>Рекомендация</h2>
    <div class="recommendation">
      {rec.replace(chr(10), '<br>')}
    </div>
  </div>""" if rec else ""

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Дайджест L&D × AI — {display_date}</title>
<meta name="description" content="L&D × AI дайджест: рынок EdTech, AI-инструменты, карьера, переезд в Минск">
<link rel="canonical" href="https://look85-ops.github.io/NAAssistant/career/posts/digest/digest-{signal_date}.html">
<meta name="theme-color" content="#1A1A1A">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
    background: #f4f2ee; color: #1A1A1A; padding: 40px 20px;
    line-height: 1.6; -webkit-font-smoothing: antialiased;
  }}
  .container {{ max-width: 680px; margin: 0 auto; background: #fff; border-radius: 12px; padding: 40px 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
  h1 {{ font-size: 24px; font-weight: 700; margin-bottom: 4px; letter-spacing: -0.3px; }}
  .date {{ font-size: 14px; color: #6b7280; margin-bottom: 24px; }}
  .section {{ margin-top: 28px; }}
  .section h2 {{ font-size: 17px; font-weight: 600; margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid #e5e7eb; }}
  .section p {{ font-size: 14.5px; color: #374151; line-height: 1.7; }}
  .section ul {{ padding-left: 20px; font-size: 14.5px; color: #374151; }}
  .section li {{ margin-bottom: 6px; }}
  .recommendation {{ background: #f3f4f6; border-left: 3px solid #1A1A1A; padding: 16px; border-radius: 6px; font-size: 14.5px; line-height: 1.7; }}
  .footer {{ margin-top: 36px; padding-top: 20px; border-top: 1px solid #e5e7eb; font-size: 13px; color: #6b7280; text-align: center; }}
</style>
</head>
<body>
<div class="container">
  <h1>Дайджест L&D × AI</h1>
  <div class="date">{display_date}</div>
{sections_html}
{rec_html}
  <div class="footer">
    На основе <a href="https://look85-ops.github.io/NAAssistant/knowledge/signal/{signal_date}">Signal</a> — еженедельный брифинг L&D × AI
  </div>
</div>
</body>
</html>"""

def main():
    signal_path = find_latest_signal()
    signal_date = signal_path.stem
    print(f"Reading signal: {signal_path}")

    md_text = signal_path.read_text(encoding="utf-8")
    print("Generating digest via LLM...")
    content = call_llm(md_text)

    html = build_html(content, signal_date)

    out_name = f"digest-{signal_date}.html"
    out_path = Path(OUTPUT_DIR) / out_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"Saved {out_path}")

if __name__ == "__main__":
    main()
