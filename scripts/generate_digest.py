import os, json, sys, re
from datetime import datetime
from urllib.request import Request, urlopen

API_KEY = (os.environ.get("BOTHUB_API_KEY") or "").strip()
API_URL = os.environ.get("BOTHUB_API_URL", "https://openai.bothub.chat/v1/chat/completions")
if not API_KEY:
    print("BOTHUB_API_KEY not set")
    sys.exit(1)

MODELS = ["gpt-4o-mini", "claude-sonnet-4-20250514", "gemini-2.0-flash"]
OUTPUT_DIR = "career/posts/digest"
ISSUE_NUM = 3
TODAY = datetime.now()
DATE_STR = TODAY.strftime("%Y-%m-%d")
MONTH_STR = TODAY.strftime("%B %Y")

os.makedirs(OUTPUT_DIR, exist_ok=True)

SYSTEM_PROMPT = """Ты — методист и edtech-аналитик, пишешь дайджест L&D × AI для русскоязычных L&D-специалистов.

Структура строгая, без отклонений:

## Кейс недели (120–180 слов, с цифрами)
Реальная история внедрения AI в L&D: компания, что сделали, как мерили, результат.

## Инструмент под задачу (40–60 слов)
«Если надо сделать X — попробуй Y». 1 инструмент = 1 задача.

## Метрика/фреймворк (40–60 слов)
Один показатель или подход к измерению обучения.

## 3 ссылки
1. Статья/исследование — почему важно (1 строка)
2. Инструмент/репозиторий — почему важно (1 строка)  
3. Материал/кейс — почему важно (1 строка)

## Рекомендация (1 конкретное действие на неделю)
Закончи рекомендацией в 1-2 предложения, с конкретным действием.

Важно: пиши по-русски, без канцелярита, без эмодзи, без «в эпоху цифровизации»."""

USER_PROMPT = f"""Напиши выпуск #{ISSUE_NUM} дайджеста L&D × AI за {MONTH_STR}.
Темы: AI-инструменты для L&D, оценочные практики, проектирование обучения, edtech-рынок.
Ориентируйся на реальные продукты и компании (Workera, Degreed, LinkedIn Learning, Coursera, Docebo, 360Learning, Sana Labs и т.д.)."""

def call_api():
    errors = []
    for model in MODELS:
        try:
            data = json.dumps({
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": USER_PROMPT}
                ],
                "temperature": 0.7,
                "max_tokens": 3000
            }).encode()
            req = Request(API_URL,
                          data=data,
                          headers={
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

def md_to_html(md_text):
    parts = md_text.split("## ")
    blocks = []
    for p in parts[1:]:
        lines = p.strip().split("\n")
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        blocks.append((title, body))
    return blocks

def extract_recommendation(blocks):
    for title, body in blocks:
        if "Рекомендация" in title:
            body_clean = re.sub(r'^\*+|\*+$', '', body).strip()
            return body_clean
    return ""

def build_html(content_md):
    blocks = md_to_html(content_md)
    rec = extract_recommendation(blocks)
    
    sections_html = ""
    for title, body in blocks:
        if "Рекомендация" in title:
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
<title>[Дайджест #{ISSUE_NUM}] {blocks[0][1][:80].split(chr(10))[0] if blocks else ""}</title>
<meta name="description" content="Дайджест L&D × AI: {blocks[0][1][:120].replace(chr(10), ' ') if blocks else ''}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://look85-ops.github.io/NAAssistant/career/posts/digest/digest-{DATE_STR}.html">
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
  h1 {{ font-size: 26px; font-weight: 700; margin-bottom: 8px; letter-spacing: -0.3px; }}
  .date {{ font-size: 14px; color: #6b7280; margin-bottom: 32px; }}
  .section {{ margin-top: 32px; }}
  .section h2 {{ font-size: 18px; font-weight: 600; margin-bottom: 8px; }}
  .section p {{ font-size: 15px; color: #374151; }}
  .section ul {{ padding-left: 20px; font-size: 15px; color: #374151; }}
  .section li {{ margin-bottom: 8px; }}
  .recommendation {{ background: #f3f4f6; border-left: 3px solid #1A1A1A; padding: 16px; border-radius: 6px; font-size: 15px; line-height: 1.7; }}
  .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; font-size: 13px; color: #6b7280; text-align: center; }}
  .footer a {{ color: #1A1A1A; }}
</style>
</head>
<body>
<div class="container">
  <h1>Дайджест L&D × AI #{ISSUE_NUM}</h1>
  <div class="date">{DATE_STR}</div>
{sections_html}
{rec_html}
  <div class="footer">
    Дайджест L&D × AI — раз в неделю о том, что реально работает.<br>
    <a href="https://look85-ops.github.io/NAAssistant/career/posts/digest/">Все выпуски →</a>
  </div>
</div>
</body>
</html>"""

def update_index(new_file):
    idx_path = os.path.join(OUTPUT_DIR, "index.html")
    link_html = f'<li><a href="{new_file}">#{ISSUE_NUM} — {DATE_STR}</a></li>\n'
    
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "<ul>" in content:
            content = content.replace("<ul>", "<ul>\n" + link_html, 1)
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        html = f"""<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Дайджест L&D × AI — все выпуски</title></head>
<body style="font-family:Inter;max-width:640px;margin:40px auto;line-height:1.6">
<h1>Дайджест L&D × AI</h1>
<p>Все выпуски:</p>
<ul>{link_html}</ul>
</body>
</html>"""
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(html)

print(f"Generating digest #{ISSUE_NUM}...")
md_content = call_api()
html_content = build_html(md_content)
file_name = f"digest-{DATE_STR}.html"
file_path = os.path.join(OUTPUT_DIR, file_name)
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)
update_index(file_name)
print(f"Saved {file_path}")
