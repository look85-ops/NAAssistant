"""Web search via DuckDuckGo Lite HTML (free, no API key, works from RF)."""

import requests, re, json, sys
from urllib.parse import quote_plus, unquote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html",
}


def search(query: str, max_results: int = 8) -> list[dict]:
    url = f"https://lite.duckduckgo.com/lite/?q={quote_plus(query)}"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    if resp.status_code != 200:
        return []

    text = resp.text
    results = []

    # Find all result blocks: number → link → snippet
    # Pattern: <a rel="nofollow" href="URL">TITLE</a> then next table row has snippet
    links = re.findall(
        r'<a rel="nofollow" href="([^"]+)">(.*?)</a>',
        text,
        re.DOTALL,
    )

    # Get all table cells with content after links
    snippets = re.findall(
        r'<td class="result-snippet">(.*?)</td>',
        text,
        re.DOTALL,
    )

    for i, (url, title) in enumerate(links):
        if i >= max_results:
            break
        # Decode HTML entities in title
        title = re.sub(r"<[^>]+>", "", title).strip()
        title = requests.utils.unquote(title) if "%" in title else title
        snippet = snippets[i] if i < len(snippets) else ""
        snippet = re.sub(r"<[^>]+>", "", snippet).strip()
        results.append({
            "title": title,
            "url": unquote(url),
            "snippet": snippet,
        })

    return results


def search_multi(queries: list[str], max_per_query: int = 5) -> dict[str, list[dict]]:
    """Run multiple searches in parallel (simple sequential)."""
    return {q: search(q, max_per_query) for q in queries}


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Query: ")
    results = search(query)
    print(json.dumps(results, ensure_ascii=False, indent=2))
