import os, re, sys
from datetime import datetime
from pathlib import Path

SIGNAL_DIR = "knowledge/signal"
OUTPUT_DIR = "career/posts/digest"

def find_latest_signal():
    md_files = sorted(Path(SIGNAL_DIR).glob("*.md"))
    if not md_files:
        print("No signal markdown files found")
        sys.exit(1)
    return md_files[-1]

def parse_signal(text):
    lines = text.strip().split("\n")
    title = ""
    sections = []  # [(section_title, [items])]
    sources = ""
    warnings = ""
    current_section = None
    current_items = []
    in_meta = False

    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            title = line.lstrip("# ").strip()
        elif line.startswith("## "):
            if current_section:
                sections.append((current_section, current_items))
            current_section = line.lstrip("## ").strip()
            current_items = []
            in_meta = False
        elif line.startswith("---"):
            in_meta = True
        elif in_meta:
            if line.startswith("_") and line.endswith("_") and "Источники" in line:
                sources = line.strip("_").strip()
            elif line.startswith("_") and line.endswith("_"):
                warnings = line.strip("_").strip()
        elif line.strip() and current_section:
            current_items.append(line.strip())

    if current_section:
        sections.append((current_section, current_items))

    return title, sections, sources, warnings

def item_to_html(item):
    item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
    item = re.sub(r'_(.+?)_', r'<em>\1</em>', item)
    if item.startswith("- "):
        item = item[2:]
    return f"    <li>{item}</li>"

MONTHS_RU = ["января","февраля","марта","апреля","мая","июня",
              "июля","августа","сентября","октября","ноября","декабря"]

def build_html(title, sections, sources, warnings, signal_path):
    date_str = signal_path.stem  # YYYY-MM-DD
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        display_date = f"{dt.day} {MONTHS_RU[dt.month-1]} {dt.year}"
    except:
        display_date = date_str

    sections_html = ""
    for sec_title, items in sections:
        items_html = "\n".join(item_to_html(it) for it in items if it)
        sections_html += f"""  <div class="section">
    <h2>{sec_title}</h2>
    <ul>
{items_html}
    </ul>
  </div>
"""

    footer_parts = []
    if sources:
        footer_parts.append(f'<p class="sources">{sources}</p>')
    if warnings:
        footer_parts.append(f'<p class="warning">{warnings}</p>')
    footer_html = "\n    ".join(footer_parts)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Сигнал #1 — {display_date}</title>
<meta name="description" content="L&D × AI дайджест: рынок EdTech, AI-инструменты, карьера, переезд в Минск">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://look85-ops.github.io/NAAssistant/career/posts/digest/digest-{date_str}.html">
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
  .section ul {{ list-style: none; padding: 0; }}
  .section li {{
    font-size: 14.5px; color: #374151; margin-bottom: 10px; padding-left: 16px;
    position: relative; line-height: 1.65;
  }}
  .section li::before {{ content: "\\2022"; position: absolute; left: 0; color: #9ca3af; }}
  .section li strong {{ color: #1A1A1A; }}
  .section li em {{ color: #6b7280; font-size: 13px; }}
  .footer {{ margin-top: 36px; padding-top: 20px; border-top: 1px solid #e5e7eb; font-size: 13px; color: #6b7280; }}
  .sources {{ margin-bottom: 6px; }}
  .warning {{ color: #d97706; font-size: 13px; }}
</style>
</head>
<body>
<div class="container">
  <h1>{title}</h1>
  <div class="date">{display_date}</div>
{sections_html}
  <div class="footer">
{footer_html}
  </div>
</div>
</body>
</html>"""

def main():
    signal_path = find_latest_signal()
    print(f"Reading signal: {signal_path}")

    md_text = signal_path.read_text(encoding="utf-8")
    title, sections, sources, warnings = parse_signal(md_text)

    html = build_html(title, sections, sources, warnings, signal_path)

    date_str = signal_path.stem
    out_name = f"digest-{date_str}.html"
    out_path = Path(OUTPUT_DIR) / out_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"Saved {out_path}")

if __name__ == "__main__":
    main()
