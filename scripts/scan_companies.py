"""Массовая проверка компаний на rabota.by — ищет L&D вакансии."""
import requests, json, re, time
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

COMPANIES = {
    # Банки
    "Белагропромбанк": "банки",
    "Альфа-Банк": "банки",
    "Беларусбанк": "банки",
    "ВТБ": "банки",
    "БНБ-Банк": "банки",
    # IT
    "EPAM": "IT",
    "IBA Group": "IT",
    "ITransition": "IT",
    "Andersen": "IT",
    "Innowise": "IT",
    "IDF Technology": "IT",
    "Team.Inno": "IT",
    # Промышленность
    "Пеленг": "пром",
    "Атлант-М": "пром",
    "OMA": "пром",
    "Alutech": "пром",
    "Примвэй": "пром",
    # EdTech
    "LogicLike": "EdTech",
    "Lerna": "EdTech",
    "TutorOnline": "EdTech",
    "Skillbox": "EdTech",
    # Телеком/ритейл
    "А1": "телеком",
    "Fix Price": "ритейл",
    "ТД Комплект": "ритейл",
}

LND_KEYWORDS = [
    "обучен", "тренер", "тренинг", "методист", "преподава",
    "развитие персонала", "адаптация", "онбординг", "edtech",
    "корпоративн", "learning", "training", "инструктор",
    "l&d", "t&d", "hr-менеджер", "hr business partner",
    "менеджер по персоналу", "учебный центр", "кадровый резерв",
    "развитие талантов", "наставник", "оценка персонала",
    "дистанционное обучение", "HRD", "hr director",
    "руководитель отдела обучения", "head of learning",
]

EXCLUDE = ["водитель", "бухгалтер", "врач", "программист", "разработчик",
           "сварщик", "кассир", "продавец", "уборщик", "повар",
           "менеджер по продажам", "sales manager", "менеджер по закупкам"]


def is_lnd(title, snippet):
    text = (title + " " + snippet).lower()
    for ex in EXCLUDE:
        if ex in text:
            return False
    return any(kw in text for kw in LND_KEYWORDS)


def search_company(name):
    """Ищет вакансии компании на rabota.by в Минске."""
    results = []
    try:
        url = f"https://rabota.by/search/vacancy?text={quote(name)}&area=1002&items_on_page=20"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return {"count": 0, "vacancies": [], "error": f"HTTP {resp.status_code}"}

        text = resp.text

        # Extract vacancy cards
        cards = re.findall(
            r'<a[^>]*data-qa="serp-item__title"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
            text, re.DOTALL
        )
        snippets = re.findall(
            r'<div[^>]*data-qa="vacancy-serp__vacancy_snippet_responsibility"[^>]*>(.*?)</div>',
            text, re.DOTALL
        )
        companies_found = re.findall(
            r'<a[^>]*data-qa="vacancy-serp__vacancy-employer"[^>]*>(.*?)</a>',
            text, re.DOTALL
        )

        for i, (href, title_raw) in enumerate(cards[:20]):
            title = re.sub(r"<[^>]+>", "", title_raw).strip()
            snippet = re.sub(r"<[^>]+>", "", snippets[i]).strip() if i < len(snippets) else ""
            company = re.sub(r"<[^>]+>", "", companies_found[i]).strip() if i < len(companies_found) else ""
            full_url = f"https://rabota.by{href}" if href.startswith("/") else href

            # Check if company matches (case-insensitive)
            if name.lower() in company.lower() or name.lower() in title.lower():
                is_lnd_match = is_lnd(title, snippet)
                results.append({
                    "title": title,
                    "company": company,
                    "url": full_url,
                    "lnd": is_lnd_match,
                    "snippet": snippet[:200]
                })

        return {"count": len(cards), "vacancies": results, "lnd_count": sum(1 for r in results if r["lnd"])}
    except Exception as e:
        return {"count": 0, "vacancies": [], "error": str(e)}


if __name__ == "__main__":
    all_results = {}
    for name, sphere in COMPANIES.items():
        print(f"Checking: {name} ({sphere})...", end=" ")
        res = search_company(name)
        all_results[name] = {**res, "sphere": sphere}
        lnd = res.get("lnd_count", 0)
        total = res.get("count", 0)
        err = res.get("error", "")
        print(f"total={total}, L&D={lnd}" + (f", ERR={err}" if err else ""))
        time.sleep(0.5)

    # Save JSON
    outpath = r"C:\Users\marcenuk\Desktop\Новый проект\career\market\company_scan_2026-09-25.json"
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {outpath}")