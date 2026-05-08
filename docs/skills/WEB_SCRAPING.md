# Web Scraping Skill

Универсальный скрапинг веб-страниц для agent workflow.

## Philosophy

- **Public data only** — никаких私人 данных без согласия.
- **Respect robots.txt** — проверять перед скрапом.
- **Rate limit** — max 1 req/sec.
- **Parse, don't scrape full** — извлекать только нужное.

## Когда использовать

- Analyzing job postings (hh, rabota.by)
- Research competitors, market
- Content aggregation for posts

## Инструменты

| Инструмент | Когда | Пример |
|---|---|---|
| `requests + bs4` | Статические HTML | hh.ru listings |
| `playwright` | SPA / JS-rendered | LinkedIn, rabota.by |
| `webfetch` | Quick + markdown | Простой контент |

## Cheatsheet

```python
# Basic: requests + bs4
from requests import get
from bs4 import BeautifulSoup

url = "https://example.com"
html = get(url, headers={"User-Agent": "Mozilla/5.0"}).text
soup = BeautifulSoup(html, "html.parser")
text = soup.get_text(separator="\n", strip=True)

# Playwright (SPA)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    page = p.chromium.new_page()
    page.goto(url, wait_until="networkidle")
    html = page.content()
    page.close()
```

## Output formats

- `markdown` — основной (webfetch по умолчанию)
- `json` — структурированный (вакансии, цены)
- `text` — plain text

## Decision rules

| Тип страницы | Инструмент | Depth |
|---|---|---|
| Простой контент | webfetch | 1 req |
| Listings / catalogs | requests + bs4 | paginated |
| Auth-protected | playwright | careful |
| API available | requests → JSON | prefer |

## Практические примеры

### Вакансии hh.ru

```python
url = "https://hh.ru/search/vacancy?text=python&area=1"
# Важно: User-Agent, не too aggressive
```

### LinkedIn Company

```python
# Только public profile, не парсить приватные данные
# Использовать LinkedIn API если доступен
```

## Guardrails

- ❌ Не собирать личные данные без согласия
- ❌ Не обходить auth/protected pages
- ❌ Не сохранять пароли/токены в код
- ✓ Использовать официальные API где можно
- ✓ Кэшировать результаты

## Интеграция в workflow

1. Определить тип страницы
2. Попробовать webfetch (fastest)
3. Если не работает → requests + bs4
4. Если JS-rendered → playwright
5. Результат в markdown для контекста

---

**Adoption**: используется в `career-architect` (анализ вакансий), `post-writer` (research).