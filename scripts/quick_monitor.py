"""Мониторинг rabota.by — свежие L&D вакансии Минска."""
import requests, re, json, time
from urllib.parse import quote
from datetime import datetime
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

QUERIES = [
    "обучение и развитие персонала",
    "менеджер по обучению",
    "корпоративное обучение",
    "методист обучение",
    "руководитель образовательных проектов",
    "бизнес тренер корпоративный",
    "T&D обучение",
]

LND_KW = [
    "обучен", "тренер", "тренинг", "методист", "преподава",
    "развитие персонала", "адаптация", "онбординг", "edtech",
    "корпоративн", "learning", "training", "l&d", "t&d",
    "hr business partner", "кадровый резерв", "наставник",
    "оценка персонала", "дистанционное обучение",
]
EXCL = [
    "водитель", "бухгалтер", "врач", "программист", "разработчик",
    "сварщик", "кассир", "продавец", "уборщик", "повар",
    "менеджер по продажам", "sales manager",
]

BASE = Path(__file__).parent.parent
SEEN_FILE = BASE / "logs" / "vacancy_seen.json"
OUT_FILE = BASE / "career" / "market" / f"monitor_{datetime.now().strftime('%Y-%m-%d')}.json"

# Load seen URLs
seen = {}
if SEEN_FILE.exists():
    try:
        seen = json.loads(SEEN_FILE.read_text(encoding="utf-8"))
    except:
        pass
seen_urls = set(seen.keys())

all_vacs = {}

for q in QUERIES:
    try:
        url = f"https://rabota.by/search/vacancy?text={quote(q)}&area=1002&items_on_page=20&order_by=publication_time"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            continue
        text = resp.text

        cards = re.findall(
            r'<a[^>]*data-qa="serp-item__title"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
            text, re.DOTALL,
        )
        companies = re.findall(
            r'<a[^>]*data-qa="vacancy-serp__vacancy-employer"[^>]*>(.*?)</a>',
            text, re.DOTALL,
        )
        snippets = re.findall(
            r'<div[^>]*data-qa="vacancy-serp__vacancy_snippet_responsibility"[^>]*>(.*?)</div>',
            text, re.DOTALL,
        )
        salaries = re.findall(
            r'<span[^>]*data-qa="vacancy-serp__vacancy-compensation"[^>]*>(.*?)</span>',
            text, re.DOTALL,
        )

        for i, (href, title_raw) in enumerate(cards[:20]):
            title = re.sub(r"<[^>]+>", "", title_raw).strip()
            company = re.sub(r"<[^>]+>", "", companies[i]).strip() if i < len(companies) else ""
            snippet = re.sub(r"<[^>]+>", "", snippets[i]).strip() if i < len(snippets) else ""
            salary = re.sub(r"<[^>]+>", "", salaries[i]).strip() if i < len(salaries) else ""
            full_url = f"https://rabota.by{href}" if href.startswith("/") else href

            # Skip hh.ru cross-listings
            if "hh.ru" in full_url:
                continue

            # L&D filter
            txt = (title + " " + snippet).lower()
            if any(ex in txt for ex in EXCL):
                continue
            if not any(kw in txt for kw in LND_KW):
                continue

            if full_url in seen_urls:
                continue

            all_vacs[full_url] = {
                "title": title,
                "company": company,
                "salary": salary,
                "snippet": snippet[:250],
                "url": full_url,
            }

        time.sleep(0.5)
    except Exception as e:
        print(f"  ERR {q}: {e}")

# Mark as seen
for url in all_vacs:
    seen[url] = datetime.now().isoformat()

# Save
result = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "count": len(all_vacs),
    "vacancies": list(all_vacs.values()),
}
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
SEEN_FILE.write_text(json.dumps(seen, ensure_ascii=False, indent=2), encoding="utf-8")

# Print summary
print(f"Found {len(all_vacs)} new L&D vacancies:")
for v in list(all_vacs.values())[:15]:
    s = v.get("salary", "")
    sal = f" ({s})" if s else ""
    print(f"  - {v['title']} | {v['company']}{sal}")
    print(f"    {v['snippet'][:120]}")
    print(f"    {v['url']}")
    print()