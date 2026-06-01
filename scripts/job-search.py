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

KEYWORDS_METHODIST = [
    "методист", "instructional designer", "instructional design",
    "педагогический дизайн", "методическая разработка",
]

KEYWORDS_LEAD = [
    "L&D", "learning and development", "head of learning",
    "learning manager", "l&d lead", "enablement manager",
    "learning partner", "business partner l&d",
    "training manager", "learning experience",
    "AI обучение", "edtech",
    "руководител", "lead", "head of",
    "менеджер по обучению", "менеджер по развитию",
    "специалист по обучению", "специалист по развитию",
    "продюсер", "training & development",
]

KEYWORDS_ALL = list(dict.fromkeys(KEYWORDS_METHODIST + KEYWORDS_LEAD + [
    "корпоративное обучение", "развитие персонала",
]))

EXCLUDE = [
    "продаж", "sales manager", "продавец",
    "менеджер по работе с клиентами", "account manager",
    "егэ", "олимпиад", "школ", "школьник",
    "детск", "ребенк", "ребёнк", "репетитор",
    "подготовк", "maths", "mathematics",
    "английск", "english", "language",
    "1с", "1с:", "бухгалтер",
    "рекрутер", "подбор персонала", "executive search",
    "hr bp", "hr-менеджер", "hr менеджер", "hr -",
    "менеджер по персоналу", "специалист по подбору",
    "менеджер по работе с персоналом",
]

BOOST = [
    "корпоративн", "adult", "l&d", "learning & development",
    "training", "взросл", "hr", "td",
    "персонал", "edtech", "обучение сотрудник",
    "корпор университет", "развитие персонала",
    "learning experience", "instructional",
    "педагогический дизайн",
]

SALARY_FROM = 200000
AREA_RU = 113
AREA_BY = 16

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.join(SCRIPT_DIR, "..")
RESUME_METHODIST = os.path.join(REPO_DIR, "career", "resume", "current-methodist.md")
RESUME_LEAD = os.path.join(REPO_DIR, "career", "resume", "current.md")


def fetch(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
        return r.read().decode("utf-8", errors="replace")


def load_resume_keywords(path):
    if not os.path.exists(path):
        print(f"  [warn] Резюме не найдено: {path}", file=sys.stderr)
        return {"positive": set(), "negative": set()}
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    positive = set()
    in_section = False
    for line in text.split("\n"):
        s = line.strip()
        if "Ключевые компетенции" in s or "Навыки" in s:
            in_section = True
            continue
        if in_section and s.startswith("- "):
            phrase = s[2:].strip().lower()
            words = phrase.split()
            if len(words) >= 2:
                positive.add(phrase)
        elif in_section and s and not s.startswith("- "):
            in_section = False

    core = ["instructional design", "instructional designer", "методист",
            "l&d", "learning and development", "learning experience",
            "enablement", "онбординг", "customer education",
            "learning analytics", "microlearning",
            "педагогический дизайн", "role-based треки", "матрица компетенций",
            "tot", "training of trainers", "skills gap analysis",
            "корпоративный университет",
            "learning & development", "развитие персонала",
            "обучение сотрудников", "обучение персонала",
            "андрагогика", "e-learning", "ипр", "траектории обучения"]
    for t in core:
        positive.add(t.lower())

    negative = {"crm", "crm-маркетолог",
                "продаж", "account manager",
                "product marketing", "smm", "seo",
                "таргетолог", "контекстная",
                "рекрутер", "подбор персонала",
                "executive search", "hr bp"}
    print(f"  [info] Загружено: {len(positive)} позитивных, {len(negative)} негативных", file=sys.stderr)
    return {"positive": positive, "negative": negative}


def resume_match_score(v, kw_data):
    if not kw_data or not isinstance(kw_data, dict) or not kw_data.get("positive"):
        return 0.0
    text = (v["title"] + " " + v.get("desc", "")).lower()
    positive = kw_data["positive"]
    negative = kw_data["negative"]
    pos = sum(1 for kw in positive if kw in text)
    neg = sum(1 for kw in negative if kw in text)
    raw = (pos - neg * 2) / len(positive) * 100
    return round(max(raw, 0), 1)


def parse_hh(html, source, schedule_label=""):
    vacancies = []
    cards = re.split(r'data-qa="vacancy-serp__vacancy"', html)[1:]
    for card in cards:
        m = re.search(r'data-qa="serp-item__title-text"[^>]*>\s*([^<]+)\s*<', card)
        if not m:
            continue
        title = m.group(1).strip()

        m = re.search(r'href="(https?://[^"]+/vacancy/\d+[^"]*)"', card)
        link = m.group(1) if m else ""

        text = re.sub(r'<[^>]+>', '\n', card)
        text = re.sub(r'\s*\n\s*', '\n', text)
        lines = [l.strip() for l in text.split('\n') if l.strip()]

        salary = ""
        company = ""
        city = ""
        for i, line in enumerate(lines):
            if re.search(r'\d[\d\u202f]', line) and i + 1 < len(lines) and lines[i + 1] == "\u20bd":
                salary = line + " " + lines[i + 1]
            if line in ("до вычета налогов", "после вычета налогов", "за\u00a0месяц"):
                if i + 1 < len(lines) and lines[i + 1] not in ("до вычета налогов", "после вычета налогов", "Опыт", "Выплаты:"):
                    if i + 1 < len(lines):
                        company = lines[i + 1]

        if not company:
            for i, line in enumerate(lines):
                if line.startswith("Выплаты:") and i + 1 < len(lines):
                    company = lines[i + 1]
                    break

        for line in lines:
            if line in ("\u041c\u043e\u0441\u043a\u0432\u0430", "\u0421\u0430\u043d\u043a\u0442-\u041f\u0435\u0442\u0435\u0440\u0431\u0443\u0440\u0433", "\u041c\u0438\u043d\u0441\u043a") or any(city_name in line for city_name in ["\u041c\u043e\u0441\u043a\u0432\u0430", "\u0421\u0430\u043d\u043a\u0442-\u041f\u0435\u0442\u0435\u0440\u0431\u0443\u0440\u0433", "\u041c\u0438\u043d\u0441\u043a"]):
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
    return any(k in text for k in EXCLUDE)


def classify(v, resume_methodist_kw, resume_lead_kw):
    tl = v["title"].lower()
    methodist_score = sum(3 for kw in KEYWORDS_METHODIST if kw in tl)
    lead_score = sum(3 for kw in KEYWORDS_LEAD if kw in tl)

    if "методист" in tl or "instructional" in tl or "педагогический дизайн" in tl:
        methodist_score += 10
    if "l&d" in tl or "lead" in tl.split() or "руководител" in tl or "training manager" in tl:
        lead_score += 10

    if methodist_score > lead_score:
        return "methodist"
    elif lead_score > methodist_score:
        return "lead"
    elif methodist_score == lead_score and methodist_score > 0:
        return "lead"
    else:
        if resume_methodist_kw and resume_lead_kw:
            ms = resume_match_score(v, resume_methodist_kw)
            ls = resume_match_score(v, resume_lead_kw)
            tiebreaker = "lead" if ls > ms else "methodist"
            return tiebreaker
        return "lead"


def score(v, resume_keywords):
    s = 0.0
    tl = v["title"].lower()
    for b in BOOST:
        if b in tl:
            s += 3
    if resume_keywords and resume_keywords.get("positive"):
        s += resume_match_score(v, resume_keywords) * 0.3
    return s


def dedup(vs):
    seen = set()
    return [v for v in vs if v["title"].lower().strip() + v.get("company", "").lower().strip() not in seen and not seen.add(v["title"].lower().strip() + v.get("company", "").lower().strip())]


def render_vacancy_html(v, tag_prefix=""):
    tag = "hh.ru" if v['source'] == 'hh.ru' else "rabota.by"
    parts = [f"<span class='tag'>{tag}</span>"]
    if v["salary"]:
        parts.append(v["salary"])
    if v["company"]:
        parts.append(v["company"])
    if v["city"]:
        parts.append(v["city"])
    return (
        f"<div class='vac'>"
        f"<div class='title'><a href='{v['url']}' target='_blank'>{v['title']}</a></div>"
        f"<div class='meta-line'>{' | '.join(parts)}</div>"
        f"</div>"
    )


def main():
    print("=" * 72)
    print("  Поиск вакансий: два трека — Методист / L&D Lead")
    print("  Критерии: удалёнка (РФ) / гибрид (РБ)")
    print(f"  {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("=" * 72)

    resume_methodist_kw = load_resume_keywords(RESUME_METHODIST)
    resume_lead_kw = load_resume_keywords(RESUME_LEAD)

    print("\n→ РФ (удалёнка): hh.ru...")
    ru = search_hh(KEYWORDS_ALL, AREA_RU, schedule="remote", salary=SALARY_FROM)
    print(f"  Найдено: {len(ru)}")

    print("\n→ РБ (гибрид/офис, от 200k): rabota.by...")
    by_top = search_rabotaby(KEYWORDS_ALL, AREA_BY, salary=SALARY_FROM)
    print(f"  Найдено: {len(by_top)}")

    print("\n→ РБ (все зарплаты): rabota.by...")
    by_all = search_rabotaby(KEYWORDS_ALL, AREA_BY, salary="")
    print(f"  Найдено: {len(by_all)}")

    all_v = [v for v in ru + by_top + by_all if not is_excluded(v)]
    all_v = dedup(all_v)

    for v in all_v:
        v["class"] = classify(v, resume_methodist_kw, resume_lead_kw)

    methodist_v = [v for v in all_v if v["class"] == "methodist"]
    lead_v = [v for v in all_v if v["class"] == "lead"]

    for v in methodist_v:
        v["match"] = resume_match_score(v, resume_methodist_kw) if resume_methodist_kw.get("positive") else 0.0
    for v in lead_v:
        v["match"] = resume_match_score(v, resume_lead_kw) if resume_lead_kw.get("positive") else 0.0

    methodist_v.sort(key=lambda v: score(v, resume_methodist_kw), reverse=True)
    lead_v.sort(key=lambda v: score(v, resume_lead_kw), reverse=True)

    top_m = methodist_v[:7]
    top_l = lead_v[:7]

    print(f"\n  Методист / Instructional Designer — {len(methodist_v)} вакансий")
    for i, v in enumerate(top_m, 1):
        print(f"  {i:2d}. [{v['match']:4.1f}%] {v['title']}")

    print(f"\n  L&D Lead / Руководитель — {len(lead_v)} вакансий")
    for i, v in enumerate(top_l, 1):
        print(f"  {i:2d}. [{v['match']:4.1f}%] {v['title']}")

    html_lines = [
        "<!DOCTYPE html><html lang='ru'><head><meta charset='UTF-8'>"
        "<title>Подборка вакансий — два трека</title>"
        "<style>"
        "body{font-family:system-ui,sans-serif;max-width:1100px;margin:40px auto;padding:0 20px}"
        "h1{font-size:1.3rem}"
        ".meta{color:#666;font-size:.85rem;margin-bottom:24px}"
        ".header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}"
        ".btn{display:inline-flex;align-items:center;gap:6px;padding:8px 20px;background:#1a73e8;color:#fff;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;text-decoration:none}"
        ".btn:hover{background:#1557b0}"
        ".columns{display:grid;grid-template-columns:1fr 1fr;gap:24px}"
        "@media(max-width:700px){.columns{grid-template-columns:1fr}}"
        ".col{padding:0}"
        ".col h2{font-size:1.1rem;margin:0 0 12px 0;padding-bottom:8px;border-bottom:2px solid #e0e0e0}"
        ".col h2 .count{color:#666;font-size:.85rem;font-weight:400}"
        ".col.h-methodist h2{border-color:#1a73e8}"
        ".col.h-lead h2{border-color:#e8710a}"
        ".vac{margin-bottom:12px;padding:12px;border:1px solid #e0e0e0;border-radius:8px}"
        ".vac:hover{background:#f8f9fa}"
        ".vac .title{font-size:.95rem;font-weight:600}"
        ".vac .title a{color:#1a73e8;text-decoration:none}"
        ".vac .title a:hover{text-decoration:underline}"
        ".vac .meta-line{color:#555;font-size:.8rem;margin-top:4px}"
        ".tag{display:inline-block;background:#e8f0fe;color:#1a73e8;font-size:.75rem;padding:2px 8px;border-radius:4px;margin-right:4px}"
        "</style></head><body>"
        f"<div class='header'>"
        f"<h1 style='margin:0'>Подборка вакансий</h1>"
        f"<a href='.' class='btn' title='Обновить'>Обновить</a>"
        f"</div>"
        f"<div class='meta'>{datetime.now().strftime('%d.%m.%Y %H:%M')} | "
        f"{len(methodist_v)} методист + {len(lead_v)} lead = {len(all_v)} всего "
        f"| Показано топ-7 в каждом треке</div>"
        f"<div class='columns'>"
    ]

    html_lines.append("<div class='col h-methodist'>")
    html_lines.append(f"<h2>Методист / Instructional Designer <span class='count'>({len(methodist_v)})</span></h2>")
    for v in top_m:
        html_lines.append(render_vacancy_html(v))
    html_lines.append("</div>")

    html_lines.append("<div class='col h-lead'>")
    html_lines.append(f"<h2>L&D Lead / Руководитель <span class='count'>({len(lead_v)})</span></h2>")
    for v in top_l:
        html_lines.append(render_vacancy_html(v))
    html_lines.append("</div>")

    html_lines.append("</div></body></html>")

    search_dir = os.path.join(REPO_DIR, "search")
    os.makedirs(search_dir, exist_ok=True)
    out_file = os.path.join(search_dir, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

    print(f"\n  HTML: file://{out_file}")
    print(f"  URL: https://look85-ops.github.io/NAAssistant/search/")


if __name__ == "__main__":
    main()
