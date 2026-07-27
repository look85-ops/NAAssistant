"""Debug DuckDuckGo HTML structure."""

import requests
from urllib.parse import quote_plus

url = f'https://html.duckduckgo.com/html/?q={quote_plus("AI corporate training")}'
resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, timeout=15)

with open('debug_ddg.html', 'w', encoding='utf-8') as f:
    f.write(resp.text)
print('Saved, length:', len(resp.text))

# Find all result__ URLs
import re
for m in re.finditer(r'class="result__', resp.text):
    start = max(0, m.start() - 100)
    end = min(len(resp.text), m.end() + 300)
    print('---')
    print(resp.text[start:end])
    print('---')
    break  # just first one
