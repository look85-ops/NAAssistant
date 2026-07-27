"""Web search via public SearXNG instances (no API key, free, works from RF)."""

import requests, json, sys, time
from urllib.parse import quote_plus

INSTANCES = [
    "https://searx.be",
    "https://search.sapti.me",
    "https://searx.space",
    "https://northboot.xyz",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}


def search(query: str, max_results: int = 8) -> list[dict]:
    for instance in INSTANCES:
        try:
            url = f"{instance}/search?q={quote_plus(query)}&format=json&language=ru-RU&categories=general"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                continue
            data = resp.json()
            results = []
            for r in data.get("results", []):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("content", ""),
                })
                if len(results) >= max_results:
                    break
            if results:
                return results
        except Exception:
            continue
    return []


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Query: ")
    results = search(query)
    print(json.dumps(results, ensure_ascii=False, indent=2))
