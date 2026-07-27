"""DuckDuckGo search via HTML (no API key, no cost)."""

import requests, html, re, sys, json, time
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}


def search(query: str, max_results: int = 8) -> list[dict]:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    text = resp.text

    results = []
    for article in re.finditer(
        r'<h2 class="result__title">(.*?)</h2>.*?'
        r'<a class="result__a" href="(.*?)".*?>(.*?)</a>.*?'
        r'<a class="result__snippet".*?>(.*?)</a>',
        text,
        re.DOTALL,
    ):
        title = html.unescape(re.sub(r"<.*?>", "", article.group(1)).strip())
        url = html.unescape(article.group(2))
        snippet = html.unescape(re.sub(r"<.*?>", "", article.group(4)).strip())
        results.append({"title": title, "url": url, "snippet": snippet})
        if len(results) >= max_results:
            break

    return results


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Query: ")
    results = search(query)
    print(json.dumps(results, ensure_ascii=False, indent=2))
