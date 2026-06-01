import os
import urllib.request
import urllib.parse
import ssl
import re
import sys
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

CRITERIA = {
    "keywords": [
        "instructional design", "instructional designer", "методист",
        "edtech", "L&D", "learning and development",
        "project manager", "проджект менеджер",
        "AI обучение", "training manager",
        "learning experience",
    ],
    "exclude": [
        "продаж", "sales manager", "продавец",
        "менеджер по работе с клиентами", "account manager",
        "егэ", "олимпиад", "школ", "школьник",
        "детск", "ребенк", "ребёнк", "репетитор",
        "подготовк", "maths", "mathematics",
        "английск", "english", "language",
        "1с", "1с:", "бухгалтер",
    ],
    "boost": [
        "корпоративн", "adult", "l&d", "learning & development",
        "training", "взросл", "hr", "td",
        "персонал", "edtech", "обучение сотрудник",
        "корпор университет", "развитие персонала",
        "learning experience", "instructional",
        "педагогический дизайн",
    ],
    "salary_from": 200000,
}
AREA_RU = 113
AREA_BY = 16

RESUME_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "career", "resume", "current.md"
)


def fetch(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
        return r.read().decode("utf-8", errors="replace")


def load_resume_keywords(path):
    """Извлекает ключевые термины из резюме для оценки соответствия."""
    if not os.path.exists(path):
        print(f"  [warn] Резюме не найдено: {path}", file=sys.stderr)
        return set()
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    keywords = set()
    in_section = False
    for line in text.split("\n"):
        s = line.strip()
        if "Ключевые компетенции" in s or "Навыки" in s:
            in_section = True
            continue
        if in_section and s.startswith("- "):
            for t in re.sub(r'[,/;]', ' ', s[2:]).split():
                t = t.strip().lower()
                if len(t) > 2:
                    keywords.add(t)
        elif in_section and s and not s.startswith("- "):
            in_section = False
    role_terms = ["instructional design", "instructional designer", "методист",
                  "l&d", "learning and development", "enablement",
                  "edtech", "training", "онбординг"]
    for t in role_terms:
        keywords.add(t.lower())
    print(f"  [info] Загружено ключевых слов из резюме: {len(keywords)}", file=sys.stderr)
    return keywords


def resume_match_score(v, resume_keywords):
    """Процент совпадения ключевых слов резюме с названием и описанием вакансии."""
    if not resume_keywords:
        return 0.0
    text = (v["title"] + " " + v.get("desc", "")).lower()
    match_count = sum(1 for kw in resume_keywords if kw in text)
    return round(match_count / len(resume_keywords) * 100, 1)


def parse_hh(html, source, schedule_label=""):
    vacancies = []
    cards = re.split(r'data-qa="vacancy-serp__vacancy"', html)[1:]
    for card in cards:
        # Find the title link
        m = re.search(r'data-qa="serp-item__title-text"[^>]*>\s*([^<]+)\s*<', card)
        if not m:
            continue
        title = m.group(1).strip()

        m = re.search(r'href="(https?://[^"]+/vacancy/\d+[^"]*)"', card)
        link = m.group(1) if m else ""

        # Extract plain text for salary, company, etc.
        text = re.sub(r'<[^>]+>', '\n', card)
        text = re.sub(r'\s*\n\s*', '\n', text)
        lines = [l.strip() for l in text.split('\n') if l.strip()]

        salary = ""
        company = ""
        city = ""
        for i, line in enumerate(lines):
            # Salary detection: "XXX – YYY" then next line "₽"
            if re.search(r'\d[\d\u202f]', line) and i + 1 < len(lines) and lines[i + 1] == "₽":
                salary = line + " " + lines[i + 1]
            # Company detection: line after "месяц" or similar
            if line in ("до вычета налогов", "после вычета налогов", "за месяц"):
                if i + 1 < len(lines) and lines[i + 1] not in ("до вычета налогов", "после вычета налогов", "Опыт", "Выплаты:"):
                    if i + 1 < len(lines):
                        company = lines[i + 1]

        # Fallback: find company after "Выплаты:" line
        if not company:
            for i, line in enumerate(lines):
                if line.startswith("Выплаты:") and i + 1 < len(lines):
                    company = lines[i + 1]
                    break

        # Find city
        for line in lines:
            if line in ("Москва", "Санкт-Петербург", "Минск") or any(city_name in line for city_name in ["Москва", "Санкт-Петербург", "Минск"]):
                if len(line) < 50:
                    city = line

        vacancies.append({
            "title": title,
            "url": link,
            "salary": salary,
            "company": company,
            "city": city,
            "desc": "",
            "source": source,
            "schedule": schedule_label,
        })
    return vacancies


def search_hh(keywords, area, schedule="", salary=""):
    vacancies = []
    for kw in keywords:
        params = {"text": kw, "area": area, "per_page": 20, "search_field": "name", "no_magic": "true"}
        if schedule:
            params["schedule"] = schedule
        if salary:
            params["salary"] = salary
        url = "https://hh.ru/search/vacancy?" + urllib.parse.urlencode(params)
        try:
            html = fetch(url)
            parsed = parse_hh(html, "hh.ru", schedule)
            vacancies.extend(parsed)
            if len(vacancies) >= 100:
                break
        except Exception as e:
            print(f"  [warn] hh.ru '{kw}': {e}", file=sys.stderr)
    return vacancies


def search_rabotaby(keywords, area, salary=""):
    vacancies = []
    for kw in keywords:
        params = {"text": kw, "area": area, "per_page": 20, "search_field": "name", "no_magic": "true"}
        if salary:
            params["salary"] = salary
        url = "https://rabota.by/search/vacancy?" + urllib.parse.urlencode(params)
        try:
            html = fetch(url)
            parsed = parse_hh(html, "rabota.by")
            vacancies.extend(parsed)
            if len(vacancies) >= 100:
                break
        except Exception as e:
            print(f"  [warn] rabota.by '{kw}': {e}", file=sys.stderr)
    return vacancies


def is_excluded(v):
    text = (v["title"] + " " + v.get("desc", "")).lower()
    return any(k in text for k in CRITERIA["exclude"])


def score(v, resume_keywords=None):
    s = 0.0
    tl = v["title"].lower()
    for b in CRITERIA["boost"]:
        if b in tl:
            s += 3
    if resume_keywords:
        s += resume_match_score(v, resume_keywords) * 0.3
    return s


def dedup(vs):
    seen = set()
    return [v for v in vs if v["title"].lower().strip() + v.get("company", "").lower().strip() not in seen and not seen.add(v["title"].lower().strip() + v.get("company", "").lower().strip())]


def main():
    print("=" * 72)
    print("  Поиск вакансий: Instructional Designer / PM / L&D x AI")
    print("  Критерии: от 200k, без продаж, удалёнка (РФ) / гибрид (РБ)")
    print(f"  {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("=" * 72)

    resume_keywords = load_resume_keywords(RESUME_PATH)

    print("\n→ РФ (удалёнка): hh.ru...")
    ru = search_hh(CRITERIA["keywords"], AREA_RU, schedule="remote", salary=CRITERIA["salary_from"])
    print(f"  Найдено: {len(ru)}")

    print("\n→ РБ (гибрид/офис): rabota.by...")
    by = search_rabotaby(CRITERIA["keywords"], AREA_BY, salary=CRITERIA["salary_from"])
    print(f"  Найдено: {len(by)}")

    all_v = [v for v in ru + by if not is_excluded(v)]
    all_v = dedup(all_v)

    for v in all_v:
        v["match"] = resume_match_score(v, resume_keywords) if resume_keywords else 0.0

    all_v.sort(key=lambda v: score(v, resume_keywords), reverse=True)

    top = all_v[:10]

    if not top:
        print("\n  Вакансий не найдено. Попробуй расширить ключевые слова.")
        return

    print(f"\n  Топ {len(top)} (по релевантности резюме)\n")
    for i, v in enumerate(top, 1):
        print(f"  {i:2d}. [{v['match']:4.1f}%] {v['title']}")
        print(f"      {v['source']} | {v['salary'] or 'з/п не указана'} | {v.get('company', '')}")

    html_lines = [
        "<!DOCTYPE html><html lang='ru'><head><meta charset='UTF-8'>"
        "<title>Подборка вакансий</title>"
        "<style>"
        "body{font-family:system-ui,sans-serif;max-width:800px;margin:40px auto;padding:0 20px}"
        "h1{font-size:1.3rem}"
        ".meta{color:#666;font-size:.85rem;margin-bottom:24px}"
        ".header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}"
        ".btn{display:inline-flex;align-items:center;gap:6px;padding:8px 20px;background:#1a73e8;color:#fff;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;text-decoration:none}"
        ".btn:hover{background:#1557b0}"
        ".btn:active{transform:scale(.97)}"
        ".vac{margin-bottom:20px;padding:16px;border:1px solid #e0e0e0;border-radius:8px}"
        ".vac:hover{background:#f8f9fa}"
        ".vac .title{font-size:1.05rem;font-weight:600}"
        ".vac .title a{color:#1a73e8;text-decoration:none}"
        ".vac .title a:hover{text-decoration:underline}"
        ".vac .meta-line{color:#555;font-size:.9rem;margin-top:4px}"
        ".match{display:inline-block;background:#e6f4ea;color:#137333;font-size:.75rem;padding:2px 8px;border-radius:4px;margin-right:4px;font-weight:600}"
        ".tag{display:inline-block;background:#e8f0fe;color:#1a73e8;font-size:.75rem;padding:2px 8px;border-radius:4px;margin-right:4px}"
        "</style></head><body>"
        f"<div class='header'>"
        f"<h1 style='margin:0'>Подборка вакансий</h1>"
        f"<a href='.' class='btn'>Обновить</a>"
        f"</div>"
        f"<div class='meta'>{datetime.now().strftime('%d.%m.%Y %H:%M')} | {len(all_v)} всего, показано {len(top)} по релевантности резюме</div>"
    ]

    for i, v in enumerate(top, 1):
        tag = "hh.ru" if v['source'] == 'hh.ru' else "rabota.by"
        parts = [f"<span class='tag'>{tag}</span>", f"<span class='match'>{v['match']:.0f}% совпадение</span>"]
        if v["salary"]:
            parts.append(v["salary"])
        if v["company"]:
            parts.append(v["company"])
        if v["city"]:
            parts.append(v["city"])

        html_lines.append(
            f"<div class='vac'>"
            f"<div class='title'><a href='{v['url']}' target='_blank'>{v['title']}</a></div>"
            f"<div class='meta-line'>{' | '.join(parts)}</div>"
            f"</div>"
        )

    html_lines.append("</body></html>")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(script_dir, "..")
    out_file = os.path.join(docs_dir, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

    print(f"\n  HTML: file://{out_file}")


if __name__ == "__main__":
    main()
