"""V2 — мониторинг вакансий hh.ru по расширенному каталогу (Москва + Минск)."""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

PROFILE = r"C:\Users\marcenuk\Desktop\Новый проект\scripts\browser-state\hh-profile-monitor"
OUTPUT = Path(r"C:\Users\marcenuk\Desktop\Новый проект\career\market")

# Каталог поисков: (запрос, area, label)
# area: 113=Москва, 1002=Минск
SEARCHES = [
    # Москва + удалёнка
    ("руководитель образовательных проектов", 113, "MK_рукОбрПроектов"),
    ("обучение и развитие персонала", 113, "MK_обучРазвитие"),
    ("руководитель учебного центра", 113, "MK_учебЦентр"),
    ("специалист по обучению", 113, "MK_спецОбуч"),
    ("корпоративное обучение", 113, "MK_корпОбуч"),
    ("T&D обучение персонал", 113, "MK_TD"),
    ("HR бизнес-партнер обучение", 113, "MK_HRBP"),
    ("продюсер образовательный обучение", 113, "MK_продюсер"),
    ("менеджер по обучению", 113, "MK_менОбуч"),
    ("кадровый резерв развитие", 113, "MK_кадрРезерв"),
    ("дополнительное образование ДПО", 113, "MK_ДПО"),
    ("оценка и развитие персонала", 113, "MK_оценкаРазвит"),
    ("learning manager обучение", 113, "MK_learnMgr"),
    ("методист обучение", 113, "MK_методист"),
    # Минск + удалёнка
    ("руководитель образовательных проектов", 1002, "MN_рукОбрПроектов"),
    ("обучение и развитие персонала", 1002, "MN_обучРазвитие"),
    ("руководитель учебного центра", 1002, "MN_учебЦентр"),
    ("специалист по обучению", 1002, "MN_спецОбуч"),
    ("корпоративное обучение", 1002, "MN_корпОбуч"),
    ("T&D обучение персонал", 1002, "MN_TD"),
    ("HR бизнес-партнер обучение", 1002, "MN_HRBP"),
    ("продюсер образовательный обучение", 1002, "MN_продюсер"),
    ("менеджер по обучению", 1002, "MN_менОбуч"),
    ("кадровый резерв развитие", 1002, "MN_кадрРезерв"),
    ("дополнительное образование ДПО", 1002, "MN_ДПО"),
    ("оценка и развитие персонала", 1002, "MN_оценкаРазвит"),
    ("learning manager обучение", 1002, "MN_learnMgr"),
    ("методист обучение", 1002, "MN_методист"),
]


def text(el, d=""):
    try: return el.text_content().strip()
    except: return d


def href(el, d=""):
    try: return el.get_attribute("href") or d
    except: return d


def collect():
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, headless=True, viewport={"width": 1280, "height": 900}
        )
        results = {}

        for query, area, label in SEARCHES:
            page = ctx.new_page()
            page.set_default_timeout(15000)
            url = f"https://hh.ru/search/vacancy?text={query}&area={area}&schedule=remote&items_on_page=100&ored_clusters=true"
            try:
                page.goto(url, timeout=30000)
                page.wait_for_load_state("domcontentloaded")
                try: page.wait_for_selector('[data-qa="vacancy-serp__vacancy"]', timeout=8000)
                except: pass
                time.sleep(1)

                cards = page.locator('[data-qa="vacancy-serp__vacancy"]')
                n = cards.count()
                if n == 0:
                    # Проверим, может страница пустая (нет вакансий)
                    body_text = text(page.locator("body"))
                    results[label] = {"n": 0, "v": [], "info": body_text[:200]}
                    print(f"  {label}: 0", flush=True)
                else:
                    print(f"  {label}: {n}", flush=True)
                    vacs = []
                    for i in range(min(n, 50)):  # макс 50 на запрос
                        c = cards.nth(i)
                        t = c.locator('[data-qa="serp-item__title"]').first
                        vacs.append({
                            "t": text(t),
                            "url": href(t),
                            "emp": text(c.locator('[data-qa="vacancy-serp__vacancy-employer"]').first),
                            "sal": text(c.locator('[data-qa^="vacancy-serp__vacancy-compensation"]').first),
                            "loc": text(c.locator('[data-qa="vacancy-serp__vacancy-address"]').first),
                            "resp": text(c.locator('[data-qa="vacancy-serp__vacancy_snippet_responsibility"]').first),
                        })
                    results[label] = {"n": n, "v": vacs}
            except Exception as e:
                print(f"  {label}: ERR {e}", flush=True)
                results[label] = {"n": 0, "v": [], "err": str(e)}
            try: page.close(run_before_unload=False)
            except: pass

        ctx.close()

    # Сохраняем
    ts = time.strftime("%Y-%m-%d")
    outpath = OUTPUT / f"monitor_{ts}.json"
    outpath.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(r["n"] for r in results.values())
    print(f"\nСохранено: {outpath} | Всего: {total} вакансий", flush=True)
    return total


if __name__ == "__main__":
    collect()