#!/usr/bin/env python3
"""
Context Map v2 — geopolitics digest for those relocating to Minsk or already there.
Multi-source: DDG news + Reddit communities + Polymarket prediction markets.
Output contract: badge, inline links, community voices, footer.
"""

import os
import sys
import re
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from ddgs import DDGS
import markdown as md_lib

VERSION = "2.0"

API_KEY = os.environ.get("DS_API_KEY", os.environ.get("GH_TOKEN", ""))
if not API_KEY:
    print("FATAL: DS_API_KEY or GH_TOKEN not set")
    sys.exit(1)

BASE_URL = "https://openai.bothub.ru/v1"
FALLBACK_URL = "https://models.inference.ai.azure.com"
MODEL = "deepseek-chat"
FALLBACK_MODEL = "Meta-Llama-3.3-70B-Instruct"

BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_BLOCKLIST = [
    "ria.ru", "tass.ru", "rt.com", "ukraina.ru", "life.ru",
    "kremlin.ru", "sputnik", "news-front", "rusvesna",
    "pravda.ru", "rublacklist", "mil.ru", "function.mil.ru",
    "censor.net", "patrioty.org.ua", "ukrinform.ua",
    "vz.ru", "iz.ru", "rg.ru", "1tv.ru", "russia.tv",
    "vesti.ru", "gov.ru", "mid.ru",
]

SEARCH_QUERIES = [
    "Россия Украина война новости 2026",
    "экономика Россия санкции 2026",
    "курс рубля доллар евро 2026",
    "Беларусь экономика новости 2026",
    "Минск недвижимость цены 2026",
    "работа Беларусь IT вакансии 2026",
    "Украина война экономика 2026",
    "нефть цены геополитика 2026",
    "санкции Европа США Россия 2026",
    "релокация Беларусь из России 2026",
]

REDDIT_SUBS = [
    "belarus", "geopolitics", "ukraine", "europe", "AskARussian",
]

POLYMARKET_KEYWORDS = [
    "Russia-Ukraine", "ceasefire", "peace", "sanctions",
    "ruble", "oil", "NATO", "EU",
]

SYSTEM_PROMPT = """Ты — аналитический ассистент Context Map v2. Составляешь дайджест для Наташи, планирующей переезд в Минск из РФ. Наташа — L&D специалист (не программист), поэтому объясняй экономические термины встроенно, без сносок.

Формат: Markdown. Дата: {date}

OUTPUT CONTRACT — строго соблюдай:

1. BADGE: первая строка дайджеста — «🌐 Context Map v2.0 · synced {date}». Ничего над ней.
2. БЕЗ блока «Источники:» в конце. Все ссылки — внутри текста.
3. ТОЛЬКО 7 разделов структуры (ниже). Никаких выдуманных заголовков.
4. В каждом абзаце — минимум 1 ссылка [Название](полный URL с https://).
5. Вплетай голос сообщества: цитируй Reddit-комментарии (u/name) и Polymarket (X%).
6. Никаких длинных тире — только короткое с пробелами: « - ».
7. В каждом разделе хотя бы один абзац содержит реальную цитату или цифру из источников.

СТРУКТУРА ДАЙДЖЕСТА:

# Context Map — Дайджест {date_short}

## 1. Обзорная карта
Ключевой тренд. Главный риск. Главная возможность. (2-3 абзаца, привязанных к переезду)

## 2. Поле боя
### РФ (санкции, экономика, курс рубля — только что влияет на жизнь)
### РБ (работа, недвижимость, экономика, визы — фокус на переезд)
### Украина (ход войны, экономика — косвенные эффекты)
### Мир (нефть, ставки, геополитика)

## 3. Слабые сигналы
3-5 edge signals — неочевидное, что может изменить расклад. Используй данные Polymarket, Reddit и новости.

## 4. Устойчивые паттерны
Что подтверждается 3+ периодов подряд. Ссылайся на динамику Polymarket и повторяющиеся темы в Reddit.

## 5. Влияние на решения (важнейший раздел — пиши развёрнуто, с цифрами и конкретикой)
### Работа: з/п в Минске по твоему профилю (L&D/edTech, не чистый IT), тренды найма, удалёнка vs офис
### Недвижимость: цены/аренда в Минске, ипотека, прогноз на квартал
### Деньги: какой валюте/инструменту доверять, инфляция, лимиты переводов
### Отрасли: что растёт (IT/edTech/АПК) и что угасает (нефтегаз/логистика РФ) — влияние на карьеру

## 6. Сценарии на 1-3 мес
3 варианта: базовый / эскалация / деэскалация. К каждому — триггеры и влияние на переезд.
Polymarket odds можно использовать как вероятности сценариев.

## 7. Дополнительно
Слабый сигнал или слепое пятно, которое стоит отследить.

ОБЩИЕ ПРАВИЛА:
- Лаконично: макс 3 абзаца на раздел
- Без воды: никаких «важно отметить», «следует подчеркнуть»
- Нет данных — прочерк (—)
- Тон: спокойный, аналитический, ноль паники и хайпа
- ГОЛОС СООБЩЕСТВА: если Reddit или Polymarket вернули данные — обязательно вплети в нарратив 2+ цитаты/цифры"""


def is_blocked(url: str) -> bool:
    domain = urlparse(url).netloc.lower()
    for blocked in SOURCE_BLOCKLIST:
        if blocked in domain:
            return True
    return False


def search_news() -> list[dict]:
    seen = set()
    results = []
    with DDGS() as ddgs:
        for query in SEARCH_QUERIES:
            try:
                for r in ddgs.text(query, max_results=3):
                    url = r.get("href", "")
                    if url and url not in seen and not is_blocked(url):
                        seen.add(url)
                        results.append({
                            "title": r.get("title", ""),
                            "snippet": r.get("body", ""),
                            "url": url,
                            "source": "ddg",
                        })
            except Exception as e:
                print(f"Search fail '{query}': {e}")
    print(f"[DDG] {len(results)} unique items")
    return results


def search_reddit() -> list[dict]:
    results = []
    headers = {"User-Agent": "context-map/2.0"}
    for sub in REDDIT_SUBS:
        try:
            url = f"https://www.reddit.com/r/{sub}/hot/.json?limit=5"
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                continue
            data = resp.json()
            for post in data.get("data", {}).get("children", []):
                p = post["data"]
                results.append({
                    "title": p.get("title", ""),
                    "snippet": p.get("selftext", "")[:300] if p.get("selftext") else p.get("url", ""),
                    "url": f"https://reddit.com{p.get('permalink', '')}",
                    "score": p.get("score", 0),
                    "comments": p.get("num_comments", 0),
                    "subreddit": sub,
                    "source": f"reddit/r/{sub}",
                })
        except Exception as e:
            print(f"  Reddit r/{sub} fail: {e}")
    print(f"[Reddit] {len(results)} posts from {len(REDDIT_SUBS)} subs")
    return results


def search_polymarket() -> list[dict]:
    results = []
    for kw in POLYMARKET_KEYWORDS:
        try:
            url = "https://gamma-api.polymarket.com/events"
            params = {"tag": kw, "limit": 3, "closed": "false"}
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code != 200:
                continue
            events = resp.json()
            for ev in events:
                title = ev.get("title", "")
                markets = ev.get("markets", [])
                for m in markets:
                    outcome = m.get("outcomePrices", [])
                    volume = m.get("volume", "0")
                    results.append({
                        "title": title,
                        "outcome": m.get("question", title),
                        "prices": outcome,
                        "volume": volume,
                        "url": f"https://polymarket.com/event/{ev.get('slug', '')}",
                        "source": "polymarket",
                    })
        except Exception as e:
            print(f"  Polymarket '{kw}' fail: {e}")
    print(f"[Polymarket] {len(results)} markets")
    return results


def build_context(ddg: list[dict], reddit: list[dict], polymarket: list[dict]) -> str:
    lines = []

    lines.append("## НОВОСТИ (DuckDuckGo)\n")
    for i, r in enumerate(ddg, 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"{r['snippet']}\n")

    if reddit:
        lines.append("\n## ОБСУЖДЕНИЯ (Reddit)\n")
        for i, r in enumerate(reddit, 1):
            score_str = f" [+{r['score']}]" if r.get("score") else ""
            cmt_str = f" ({r['comments']} комм.)" if r.get("comments") else ""
            lines.append(f"[{i}] r/{r['subreddit']}{score_str}{cmt_str}: {r['title']}")
            if r['snippet']:
                lines.append(f"{r['snippet'][:200]}")
            lines.append("")

    if polymarket:
        lines.append("\n## ПРОГНОЗЫ (Polymarket)\n")
        for i, m in enumerate(polymarket, 1):
            prices = m.get("prices", [])
            pct = ""
            if prices and len(prices) > 0:
                try:
                    pct = f" — {float(prices[0])*100:.0f}%"
                except (ValueError, TypeError):
                    pass
            lines.append(f"[{i}] {m['outcome']}{pct}")
            lines.append(f"Объём: ${m.get('volume', '0')}")
            lines.append("")

    lines.append("\n---\n")
    lines.append("## ИСТОЧНИКИ ДЛЯ ЦИТИРОВАНИЯ (используй ТОЛЬКО эти URL):\n")
    for i, r in enumerate(ddg, 1):
        lines.append(f"{i}. {r['url']} — {r['title'][:60]}")
    offset = len(ddg)
    for i, r in enumerate(reddit, offset + 1):
        lines.append(f"{i}. {r['url']} — r/{r['subreddit']}: {r['title'][:60]}")
    offset = offset + len(reddit)
    for i, m in enumerate(polymarket, offset + 1):
        lines.append(f"{i}. {m['url']} — Polymarket: {m['outcome'][:60]}")

    return "\n".join(lines)


def call_llm(context: str) -> str:
    today = datetime.now()
    date_full = today.strftime("%d.%m.%Y")
    date_short = today.strftime("%d.%m.%Y")
    system = SYSTEM_PROMPT.format(date=date_full, date_short=date_short)
    gh_key = os.environ.get("GH_TOKEN", "")

    endpoints = [
        {"url": f"{BASE_URL}/chat/completions", "key": API_KEY, "model": MODEL},
    ]
    if gh_key:
        endpoints.append({"url": f"{FALLBACK_URL}/chat/completions", "key": gh_key, "model": FALLBACK_MODEL})

    last_error = None
    for ep in endpoints:
        try:
            resp = requests.post(
                ep["url"],
                headers={
                    "Authorization": f"Bearer {ep['key']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": ep["model"],
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": context},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 16000,
                },
                timeout=180,
            )
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                model_used = ep["model"]
                print(f"LLM ({model_used}): {usage.get('prompt_tokens','?')} in / {usage.get('completion_tokens','?')} out")
                return content
            last_error = f"API {resp.status_code}"
            print(f"  {ep['model']}: {last_error}, trying next...")
        except Exception as e:
            last_error = str(e)
            print(f"  {ep['model']}: {last_error}, trying next...")

    raise Exception(f"All APIs failed: {last_error}")


def post_process_md(md: str) -> str:
    md = md.strip()
    if md.startswith("```"):
        first = md.find("\n") + 1 if "\n" in md else 3
        last = md.rfind("```")
        md = md[first:last].strip()

    md = md.replace("Что я могла упустить", "Дополнительно")
    md = md.replace("Что я упустила", "Дополнительно")
    md = md.replace("Что можно упустить", "Дополнительно")

    bare_refs = re.findall(r'\[\d+\]', md)
    if bare_refs:
        print(f"WARNING: {len(bare_refs)} bare [N] refs stripped")
        md = re.sub(r'\[\d+\]', '', md)

    md = re.sub(r'(?<=\d),(?=\d{3})', '\u2009', md)

    def linkify_url(match):
        num = match.group(1)
        url = match.group(2).strip()
        if not url.startswith("http"):
            url = "https://" + url
        domain = urlparse(url).netloc.replace("www.", "")
        return f"{num}. [{domain}]({url})"

    md = re.sub(r'^(\d+)\.\s+(https?://\S+)', linkify_url, md, flags=re.MULTILINE)
    md = re.sub(r'^(\d+)\.\s+([a-zA-Z0-9][^\s]+\.[a-zA-Z]{2,}\S*)', linkify_url, md, flags=re.MULTILINE)

    md = re.sub(r'\(https?://([^\s)]+)\)', r'[\1](\1)', md)
    md = re.sub(r'\(([a-zA-Z0-9][^\s)]*\.[a-zA-Z]{2,}[^\s)]*)\)', r'[\1](https://\1)', md)

    def bracket_ref_link(m):
        name = m.group(1)
        url = m.group(2).strip().rstrip(",.!?;:")
        if not url.startswith("http"):
            url = "https://" + url
        return f"[{name}]({url})"

    md = re.sub(r'\[([^\]]+)\]\[([a-zA-Z0-9][^\]]*\.[^\]]+)\]', bracket_ref_link, md)

    def bracket_link(m):
        name = m.group(1)
        url = m.group(2).strip().rstrip(",.!?;:")
        if not url.startswith("http"):
            url = "https://" + url
        return f"[{name}]({url})"

    md = re.sub(r'\[([^\]]+)\](\s*https?://\S+)', bracket_link, md)
    md = re.sub(r'\[([^\]]+)\](\s*[a-zA-Z0-9][^\s]*\.[a-zA-Z]{2,}\S*)', bracket_link, md)

    def bare_url_link(m):
        url = m.group(1).strip()
        domain = urlparse(url).netloc.replace("www.", "")
        if not domain:
            domain = url.split("/")[2] if "://" in url else url.split("/")[0]
        return f"[{domain}]({url})"

    md = re.sub(r'^\s*(https?://\S+)', bare_url_link, md, flags=re.MULTILINE)

    def ensure_https(m):
        text = m.group(1)
        url = m.group(2)
        if not url.startswith("http") and not url.startswith("#") and not url.startswith("/"):
            url = "https://" + url
        return f"[{text}]({url})"

    md = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', ensure_https, md)

    return md


def enforce_output_contract(md: str, n_ddg: int, n_reddit: int, n_poly: int) -> str:
    """LAW checks and enforcement before HTML generation."""

    today = datetime.now().strftime("%d.%m.%Y")

    if not md.startswith("🌐"):
        md = f"🌐 Context Map v{VERSION} · synced {today}\n\n" + md

    md = re.sub(r'——', ' - ', md)
    md = re.sub(r'—', ' - ', md)
    md = re.sub(r'–', ' - ', md)

    sources_total = n_ddg + n_reddit + n_poly
    parts = []
    if n_ddg:
        parts.append(f"{n_ddg} новостей (DDG)")
    if n_reddit:
        parts.append(f"{n_reddit} обсуждений (Reddit)")
    if n_poly:
        parts.append(f"{n_poly} маркетов (Polymarket)")
    sources_str = " + ".join(parts) if parts else "0"

    gen_ts = datetime.now().strftime("%d.%m.%Y %H:%M UTC")
    footer = (
        f"\n\n---\n"
        f"📊 Дайджест собран из {sources_str}\n"
        f"🕐 Сгенерирован {gen_ts}\n"
        f"🧠 Context Map v{VERSION}\n"
    )
    md = md.rstrip() + footer

    return md


def validate_digest(md: str) -> list[str]:
    issues = []

    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', md):
        url = m.group(2)
        if not url.startswith("http") and not url.startswith("#") and not url.startswith("/"):
            issues.append(f"Link '{m.group(1)}' missing protocol: {url}")

    bare = re.findall(r'\[\d+\]', md)
    if bare:
        issues.append(f"{len(bare)} bare [N] refs remain")

    bare_paren = re.findall(r'\(https?://[^\s)]+\)', md)
    if bare_paren:
        issues.append(f"{len(bare_paren)} bare URLs in parens remain")

    if md.strip().startswith("```"):
        issues.append("Code fence still wrapping output")

    if not md.strip().startswith("🌐"):
        issues.append("Missing badge (output contract LAW 1)")

    if "📊 Дайджест собран из" not in md:
        issues.append("Missing footer (output contract LAW 7)")

    if issues:
        print("VALIDATION ISSUES:")
        for i in issues:
            print(f"  ! {i}")
    else:
        print("Validation: OK")
    return issues


def md_to_html(md: str) -> str:
    body = md_lib.markdown(md, extensions=["extra"])
    body = body.replace('<a href="', '<a target="_blank" rel="noopener" href="')

    today = datetime.now()
    months = ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"]
    date_ru = f"{today.day} {months[today.month-1]} {today.year}"
    gen_ts = today.strftime("%d.%m.%Y %H:%M UTC")
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Context Map — {today.strftime('%d.%m.%Y')}</title>
<style>
:root {{
  --bg: #faf9f7; --text: #1a1a1a; --text2: #6b7280;
  --border: #e5e7eb; --accent: #2563eb; --accent2: #1d4ed8;
  --w: 720px;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans",sans-serif;
  background:var(--bg);color:var(--text);line-height:1.75;font-size:17px;padding:2rem 1rem;
}}
.container{{max-width:var(--w);margin:0 auto}}
header{{margin-bottom:2.5rem;padding-bottom:1.5rem;border-bottom:1px solid var(--border)}}
header h1{{font-size:1.75rem;font-weight:700;letter-spacing:-0.02em}}
header .meta{{margin-top:0.5rem;font-size:0.875rem;color:var(--text2)}}
header .desc{{margin-top:1rem;font-size:0.9rem;color:var(--text2);line-height:1.5}}
h2{{font-size:1.35rem;margin-top:2.5rem;margin-bottom:0.75rem;font-weight:600}}
h3{{font-size:1.1rem;margin-top:1.5rem;margin-bottom:0.5rem;font-weight:600;color:var(--accent)}}
p{{margin-bottom:1rem}}
a{{color:var(--accent);text-decoration:underline;text-underline-offset:2px}}
a:hover{{color:var(--accent2)}}
ul,ol{{margin-bottom:1rem;padding-left:1.5rem}}
li{{margin-bottom:0.25rem}}
hr{{border:none;border-top:1px solid var(--border);margin:2rem 0}}
blockquote{{border-left:3px solid var(--accent);padding-left:1rem;margin:1rem 0;color:var(--text2)}}
code{{background:var(--border);padding:0.15rem 0.4rem;border-radius:4px;font-size:0.875em}}
.disclaimer{{margin-top:2.5rem;padding:1rem 1.25rem;background:#fef3cd;border-left:4px solid #f59e0b;border-radius:4px;font-size:0.85rem;color:#92400e;line-height:1.5}}
footer{{margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid var(--border);font-size:0.8rem;color:var(--text2)}}
.footer-block{{margin-top:2rem;padding:1rem;background:#f3f4f6;border-radius:4px;font-size:0.85rem;color:var(--text2);line-height:1.6}}
</style>
</head>
<body>
<div class="container">
<header>
  <h1>Context Map</h1>
  <div class="meta">{date_ru} · дайджест для переезжающих и переехавших в Беларусь из РФ</div>
  <p class="desc">Дайджест собирает геополитический контекст из новостей, Reddit-обсуждений и Polymarket-прогнозов: 7 разделов от обзорной карты до сценариев развития. Основа — мировые источники, проанализированные ИИ. Не замена консультации.</p>
</header>
<main>
{body}
</main>
<div class="disclaimer">
  <p>Сгенерировано AI. Ключевые цифры и факты рекомендуем перепроверять по первоисточникам. Не является инвестиционной или юридической консультацией.</p>
</div>
<footer>
  <p>Context Map — автоматический дайджест для принятия решений.</p>
  <p style="margin-top:0.25rem;font-size:0.75rem;color:var(--text2)">Сгенерирован {gen_ts}</p>
</footer>
</div>
</body>
</html>"""
    return html


def save(html: str):
    date_str = datetime.now().strftime("%Y-%m-%d")

    idx = BASE_DIR / "index.html"
    idx.write_text(html, encoding="utf-8")
    print(f"index.html ({len(html)} bytes)")

    ad = BASE_DIR / "artifacts"
    ad.mkdir(exist_ok=True)
    ap = ad / f"{date_str}.html"
    ap.write_text(html, encoding="utf-8")
    print(f"artifacts/{date_str}.html")


def main():
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"Context Map v{VERSION} — {today}")

    print("[Pre-Flight] Starting multi-source collection...")

    ddg = search_news()
    reddit = search_reddit()
    polymarket = search_polymarket()

    if not ddg and not reddit and not polymarket:
        print("No data from any source, saving empty digest")
        html = md_to_html("🌐 Context Map — нет данных\n\nНи один источник не вернул данных в этом цикле.")
        save(html)
        return

    context = build_context(ddg, reddit, polymarket)
    total_sources = len(ddg) + len(reddit) + len(polymarket)
    print(f"Context: {len(context)} chars / {total_sources} sources")

    md = call_llm(context)
    print(f"Digest raw: {len(md)} chars")

    md = post_process_md(md)
    md = enforce_output_contract(md, len(ddg), len(reddit), len(polymarket))
    validate_digest(md)

    html = md_to_html(md)
    save(html)
    print(f"[Done] Context Map v{VERSION} — {total_sources} sources across 3 platforms")


if __name__ == "__main__":
    main()
