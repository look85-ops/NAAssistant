"""Сканирование hh.ru — удалённые L&D вакансии."""
import requests, re, json, time
from urllib.parse import quote
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

QUERIES = [
    "руководитель обучения и развития",
    "методист обучение",
    "корпоративное обучение",
    "T&D обучение персонал",
    "продюсер образовательный",
    "head of learning",
    "L&D специалист",
]

LND = [
    "обучен", "тренер", "тренинг", "методист", "преподава",
    "развитие персонала", "адаптация", "онбординг", "edtech",
    "корпоративн", "learning", "training", "l&d", "t&d",
    "hr business partner", "кадровый резерв", "наставник",
    "оценка персонала", "дистанционное обучение",
    "head of learning",
]
EXCL = [
    "водитель", "бухгалтер", "врач", "программист", "разработчик",
    "сварщик", "кассир", "продавец", "уборщик", "повар",
    "менеджер по продажам", "sales manager",
]

results = {}
for q in QUERIES:
    try:
        url = f"https://hh.ru/search/vacancy?text={quote(q)}&schedule=remote&items_on_page=20&order_by=publication_time"
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
        salaries = re.findall(
            r'<span[^>]*data-qa="vacancy-serp__vacancy-compensation"[^>]*>(.*?)</span>',
            text, re.DOTALL,
        )
        addresses = re.findall(
            r'<span[^>]*data-qa="vacancy-serp__vacancy-address"[^>]*>(.*?)</span>',
            text, re.DOTALL,
        )

        for i, (href, title_raw) in enumerate(cards[:20]):
            title = re.sub(r"<[^>]+>", "", title_raw).strip()
            company = re.sub(r"<[^>]+>", "", companies[i]).strip() if i < len(companies) else ""
            salary = re.sub(r"<[^>]+>", "", salaries[i]).strip() if i < len(salaries) else ""
            address = re.sub(r"<[^>]+>", "", addresses[i]).strip() if i < len(addresses) else ""
            full_url = f"https://hh.ru{href}" if href.startswith("/") else href

            txt = (title + " " + company).lower()
            if any(ex in txt for ex in EXCL):
                continue
            if not any(kw in txt for kw in LND):
                continue
            if full_url in results:
                continue

            results[full_url] = {
                "title": title,
                "company": company,
                "salary": salary,
                "location": address,
                "url": full_url,
            }
        time.sleep(0.5)
    except Exception as e:
        pass

vac_list = sorted(results.values(), key=lambda v: v.get("salary", "") or "")
out = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "count": len(results),
    "vacancies": vac_list,
}

outpath = r"C:\Users\marcenuk\Desktop\Новый проект\career\market\monitor_hh_ru_remote_2026-10-02.json"
import os
os.makedirs(os.path.dirname(outpath), exist_ok=True)
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Found {len(results)} remote L&D vacancies:")
for v in vac_list:
    s = v.get("salary", "") or "—"
    loc = v.get("location", "")
    print(f"  {v['title']}")
    print(f"    {v['company']} | {s} | {loc}")
    print(f"    {v['url']}")
    print()