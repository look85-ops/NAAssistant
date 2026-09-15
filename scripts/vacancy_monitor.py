"""
Мониторинг вакансий для рынка РБ (Минск).
Проверяет rabota.by, praca.by, belmeta.com раз в 3 дня — отправляет подборку на email.
Запуск: python scripts/vacancy_monitor.py
Можно поставить в Windows Task Scheduler на каждые 3 дня.
"""

import os
import sys
import json
import smtplib
import re
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path

import requests

# ====== CONFIG ======
EMAIL_FROM = "look85@gmail.com"
EMAIL_TO = "look85@gmail.com"
# Gmail app password — set in .env as GMAIL_APP_PASSWORD
SEEN_FILE = Path(__file__).parent.parent / "logs" / "vacancy_seen.json"
REPORT_FILE = Path(__file__).parent.parent / "career" / "market" / f"monitor_{datetime.now().strftime('%Y-%m-%d')}.md"

KEYWORDS = [
    "обучение и развитие персонала",
    "менеджер по обучению",
    "специалист по обучению",
    "корпоративное обучение",
    "бизнес-тренер",
    "training and development",
    "L&D",
    "методист",
    "онбординг",
    "edtech",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ====== SEARCH FUNCTIONS ======

def search_rabota_by():
    """rabota.by — прямой парсинг поисковой выдачи (без JS)."""
    results = []
    for kw in KEYWORDS[:5]:
        try:
            url = f"https://rabota.by/search/vacancy?text={requests.utils.quote(kw)}&area=1002&items_on_page=20"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue

            text = resp.text
            # Extract vacancy cards: title + link + company + snippet
            cards = re.findall(
                r'<a[^>]*data-qa="serp-item__title"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                text, re.DOTALL
            )
            companies = re.findall(
                r'<a[^>]*data-qa="vacancy-serp__vacancy-employer"[^>]*>(.*?)</a>',
                text, re.DOTALL
            )
            snippets = re.findall(
                r'<div[^>]*data-qa="vacancy-serp__vacancy_snippet_responsibility"[^>]*>(.*?)</div>',
                text, re.DOTALL
            )
            salary_raw = re.findall(
                r'<span[^>]*data-qa="vacancy-serp__vacancy-compensation"[^>]*>(.*?)</span>',
                text, re.DOTALL
            )

            for i, (href, title) in enumerate(cards[:20]):
                title = re.sub(r"<[^>]+>", "", title).strip()
                company = re.sub(r"<[^>]+>", "", companies[i]).strip() if i < len(companies) else ""
                snippet = re.sub(r"<[^>]+>", "", snippets[i]).strip() if i < len(snippets) else ""
                salary = re.sub(r"<[^>]+>", "", salary_raw[i]).strip() if i < len(salary_raw) else ""
                full_url = f"https://rabota.by{href}" if href.startswith("/") else href

                results.append({
                    "source": "rabota.by",
                    "title": title,
                    "company": company,
                    "salary": salary,
                    "url": full_url,
                    "snippet": snippet[:300] if snippet else "",
                    "keyword": kw,
                })
            time.sleep(1)  # вежливость
        except Exception as e:
            print(f"  rabota.by error ({kw}): {e}")
    return results


def search_belmeta():
    """belmeta.com — агрегатор, парсим страницу поиска."""
    results = []
    for kw in KEYWORDS[:3]:
        try:
            url = f"https://belmeta.com/vacancy?search={requests.utils.quote(kw)}&city=минск"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue

            text = resp.text
            # belmeta structure: vacancy cards with h2 > a
            cards = re.findall(
                r'<h2[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                text, re.DOTALL
            )
            companies = re.findall(
                r'<span[^>]*class="[^"]*company[^"]*"[^>]*>(.*?)</span>',
                text, re.DOTALL
            )
            salaries = re.findall(
                r'<span[^>]*class="[^"]*salary[^"]*"[^>]*>(.*?)</span>',
                text, re.DOTALL
            )

            for i, (href, title) in enumerate(cards[:15]):
                title = re.sub(r"<[^>]+>", "", title).strip()
                company = re.sub(r"<[^>]+>", "", companies[i]).strip() if i < len(companies) else ""
                salary = re.sub(r"<[^>]+>", "", salaries[i]).strip() if i < len(salaries) else ""

                results.append({
                    "source": "belmeta.com",
                    "title": title,
                    "company": company,
                    "salary": salary,
                    "url": href if href.startswith("http") else f"https://belmeta.com{href}",
                    "keyword": kw,
                })
            time.sleep(1)
        except Exception as e:
            print(f"  belmeta.com error ({kw}): {e}")
    return results


def search_praca_by():
    """praca.by — прямой парсинг."""
    results = []
    for kw in KEYWORDS[:3]:
        try:
            url = f"https://praca.by/search/?query={requests.utils.quote(kw)}&city=минск"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue

            text = resp.text
            cards = re.findall(
                r'<a[^>]*class="[^"]*vacancy-title[^"]*"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                text, re.DOTALL
            )
            companies = re.findall(
                r'<span[^>]*class="[^"]*company-name[^"]*"[^>]*>(.*?)</span>',
                text, re.DOTALL
            )

            for i, (href, title) in enumerate(cards[:15]):
                title = re.sub(r"<[^>]+>", "", title).strip()
                company = re.sub(r"<[^>]+>", "", companies[i]).strip() if i < len(companies) else ""

                results.append({
                    "source": "praca.by",
                    "title": title,
                    "company": company,
                    "salary": "",
                    "url": href if href.startswith("http") else f"https://praca.by{href}",
                    "keyword": kw,
                })
            time.sleep(1)
        except Exception as e:
            print(f"  praca.by error ({kw}): {e}")
    return results


# ====== FILTER & DEDUPLICATE ======

def is_relevant(vacancy: dict) -> bool:
    """Проверяет, что вакансия относится к L&D/обучению/HR."""
    title_lower = vacancy.get("title", "").lower()
    snippet_lower = vacancy.get("snippet", "").lower()

    # exclude явно не-L&D роли
    exclude = ["водитель", "бухгалтер", "врач", "программист", "разработчик",
               "сварщик", "строитель", "кассир", "продавец", "уборщик", "повар",
               "менеджер по продажам", "sales manager", "менеджер по закупкам"]
    for ex in exclude:
        if ex in title_lower:
            return False

    # include L&D-related
    include = ["обучен", "тренер", "тренинг", "методист", "преподава",
               "развитие персонала", "адаптация", "онбординг", "edtech",
               "корпоративн", "learning", "training", "инструктор",
               "коуч", "facilitator", "наставник", "hr-менеджер",
               "специалист по персоналу", "кадровый", "аттестация",
               "менеджер по персоналу", "hr business partner",
               "оценка персонала", "hr manager", "hr specialist",
               "менеджер проектов обучен", "l&d", "t&d"]

    text = title_lower + " " + snippet_lower
    return any(inc in text for inc in include)


def deduplicate(vacancies: list[dict], seen: set) -> list[dict]:
    """Убираем дубли по URL и уже виденные."""
    new = []
    seen_urls = {v.get("url", "") for v in vacancies if v.get("url")}
    duplicates_in_batch = set()
    for v in vacancies:
        url = v.get("url", "")
        if not url or url in seen or url in duplicates_in_batch:
            continue
        duplicates_in_batch.add(url)
        new.append(v)
    return new


def update_seen(new_vacancies: list[dict], seen_data: dict) -> dict:
    """Добавляет URL новых вакансий в seen-файл, чистит старые (>30 дней)."""
    if SEEN_FILE.exists():
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            seen_data = json.load(f)

    today = datetime.now().isoformat()
    for v in new_vacancies:
        url = v.get("url", "")
        if url:
            seen_data[url] = today

    # clean old (>30 days)
    cutoff = (datetime.now() - timedelta(days=30)).isoformat()
    cleaned = {url: d for url, d in seen_data.items() if d > cutoff}

    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    return cleaned


# ====== REPORT GENERATION ======

def generate_report(new_vacancies: list[dict]) -> str:
    """Генерирует markdown-отчёт."""
    today = datetime.now().strftime("%d.%m.%Y")
    lines = [
        f"# Мониторинг вакансий — Минск (РБ)",
        f"",
        f"**Дата:** {today}",
        f"**Новых вакансий:** {len(new_vacancies)}",
        f"**Источники:** rabota.by, praca.by, belmeta.com",
        f"",
        f"---",
        f"",
    ]

    if not new_vacancies:
        lines.append("Новых вакансий не найдено. Рынок тихий.")
        return "\n".join(lines)

    # Group by source
    by_source = {}
    for v in new_vacancies:
        src = v.get("source", "other")
        by_source.setdefault(src, []).append(v)

    for src, vacs in sorted(by_source.items()):
        lines.append(f"## {src} ({len(vacs)})")
        lines.append("")
        for v in vacs:
            title = v.get("title", "—")
            company = v.get("company", "")
            salary = v.get("salary", "")
            url = v.get("url", "")
            snippet = v.get("snippet", "")

            line = f"- **{title}**"
            if company:
                line += f" — *{company}*"
            if salary:
                line += f" — {salary}"
            lines.append(line)
            if snippet:
                lines.append(f"  _{snippet}_")
            lines.append(f"  [Открыть]({url})")
            lines.append("")
        lines.append("")

    return "\n".join(lines)


# ====== EMAIL ======

def send_email(report_md: str, vacancy_count: int):
    """Отправляет отчёт через Gmail SMTP (опционально)."""
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        print("GMAIL_APP_PASSWORD not set — skipping email, report saved to file only.")
        return False

    # ... same as before ...

    today = datetime.now().strftime("%d.%m.%Y")
    subject = f"Мониторинг вакансий Минск — {today} ({vacancy_count} новых)"

    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject

    # Plain text fallback (strip markdown)
    plain = re.sub(r"[*#_\[\]]", "", report_md)
    msg.attach(MIMEText(plain, "plain", "utf-8"))

    # HTML with basic formatting
    html = report_md
    html = re.sub(r"^# (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"_(.+?)_", r"<em>\1</em>", html)
    html = re.sub(r"\[Открыть\]\(([^)]+)\)", r'<a href="\1">Открыть &rarr;</a>', html)
    html = re.sub(r"^- (.+)$", r"<li>\1</li>", html, flags=re.MULTILINE)
    html = f"<html><body style='font-family:Arial,sans-serif;max-width:700px'>{html}</body></html>"
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, password)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print(f"Email sent to {EMAIL_TO}")
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


# ====== MAIN ======

def main():
    print(f"=== Vacancy Monitor — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")

    # Load seen URLs
    seen_data = {}
    if SEEN_FILE.exists():
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            seen_data = json.load(f)
    seen_urls = set(seen_data.keys())
    print(f"Seen URLs loaded: {len(seen_urls)}")

    # Search all sources
    print("Searching rabota.by...")
    rabota = search_rabota_by()
    print(f"  Found: {len(rabota)} raw")

    print("Searching belmeta.com...")
    belmeta = search_belmeta()
    print(f"  Found: {len(belmeta)} raw")

    print("Searching praca.by...")
    praca = search_praca_by()
    print(f"  Found: {len(praca)} raw")

    all_raw = rabota + belmeta + praca

    # Filter relevant
    relevant = [v for v in all_raw if is_relevant(v)]
    print(f"Relevant (L&D-filtered): {len(relevant)}")

    # Deduplicate
    new = deduplicate(relevant, seen_urls)
    print(f"New vacancies: {len(new)}")

    if new:
        # Save seen
        update_seen(new, seen_data)

        # Generate report
        report = generate_report(new)

        # Save to file
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved: {REPORT_FILE}")

        # Send email
        send_email(report, len(new))
    else:
        print("No new vacancies today.")

    print("Done.")


if __name__ == "__main__":
    main()
