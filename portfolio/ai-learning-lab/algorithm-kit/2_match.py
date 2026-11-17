# -*- coding: utf-8 -*-
"""
Шаг 2. Сопоставление плашек «Слайд» со слайдами презентации.

Метод: TF-IDF + косинусное сходство + монотонное выравнивание (DTW).
Отдаёт mapping.json (плашка-индекс -> номер слайда) и match_report.txt.

Использование:
    py 2_match.py

Настрой CONFIG ниже. После прогона прочитай match_report.txt.
"""
import io
import re
import sys
import math
import json
import zipfile
from lxml import etree

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# === CONFIG ===
PPTX = r"путь\к\управляющей_презентации.pptx"
DOCX = r"путь\к\сценарию.docx"
OUT_MAP = r"mapping.json"
OUT_REPORT = r"match_report.txt"
# ==============

A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def tokens(s):
    s = s.lower()
    s = re.sub(r'[^a-zа-яё0-9 ]+', ' ', s)
    return [t for t in s.split() if len(t) > 1 and not t.isdigit()]

def main():
    # слайды
    with zipfile.ZipFile(PPTX) as z:
        names = sorted([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)],
                       key=lambda n: int(re.search(r'(\d+)', n).group()))
        slide_texts = {}
        for n in names:
            num = int(re.search(r'(\d+)', n).group(1))
            r = etree.fromstring(z.read(n))
            slide_texts[num] = ' '.join(t.text.strip() for t in r.iter(A + 't') if t.text and t.text.strip())

    # плашки
    with zipfile.ZipFile(DOCX) as z:
        root = etree.fromstring(z.read('word/document.xml'))
    paras = list(root.iter(W + 'p'))
    def ptext(p):
        return ''.join(t.text or '' for t in p.iter(W + 't')).strip()
    plaque = [i for i, p in enumerate(paras) if ptext(p).startswith('Слайд')]
    def ctx(i, cap=10):
        ts = []
        for q in paras[i+1:i+1+cap]:
            s = ptext(q)
            if s.startswith('Слайд'):
                break
            ts += tokens(s)
        return ts
    plaque_ctx = [ctx(i) for i in plaque]

    # TF-IDF
    N = len(slide_texts)
    df = {}
    for num, txt in slide_texts.items():
        for t in set(tokens(txt)):
            df[t] = df.get(t, 0) + 1
    def idf(t):
        return math.log((N + 1) / (df.get(t, 0) + 1)) + 1.0
    slide_vec = {}
    for num, txt in slide_texts.items():
        v = {}
        for t in tokens(txt):
            v[t] = v.get(t, 0) + 1
        tot = sum(x * x for x in v.values()) ** 0.5 or 1.0
        slide_vec[num] = {t: (c / tot) * idf(t) for t, c in v.items()}
    plaque_vec = []
    for toks in plaque_ctx:
        v = {}
        for t in toks:
            v[t] = v.get(t, 0) + 1
        tot = sum(x * x for x in v.values()) ** 0.5 or 1.0
        plaque_vec.append({t: (c / tot) * idf(t) for t, c in v.items()})
    def cos(a, b):
        return sum(w * b.get(x, 0) for x, w in a.items())

    slide_list = sorted(slide_vec.keys())
    Pn = len(plaque_vec)
    Sn = len(slide_list)
    GAP = -8.0

    import numpy as np
    dp = np.full((Pn+1, Sn+1), -1e9)
    back = np.zeros((Pn+1, Sn+1), dtype=np.int8)
    dp[0, :] = 0.0
    for i in range(1, Pn+1):
        for j in range(1, Sn+1):
            sim = cos(plaque_vec[i-1], slide_vec[slide_list[j-1]])
            diag = dp[i-1, j-1] + sim
            reuse = dp[i-1, j] + sim
            skip = dp[i, j-1] + GAP
            if diag >= reuse and diag >= skip:
                dp[i, j] = diag; back[i, j] = 1
            elif reuse >= skip:
                dp[i, j] = reuse; back[i, j] = 2
            else:
                dp[i, j] = skip; back[i, j] = 3
    i, j = Pn, Sn
    mapping = {}
    while i > 0 and j > 0:
        m = back[i, j]
        if m == 1:
            mapping[plaque[i-1]] = slide_list[j-1]; i -= 1; j -= 1
        elif m == 2:
            mapping[plaque[i-1]] = slide_list[j-1]; i -= 1
        else:
            j -= 1
    while i > 0:
        mapping[plaque[i-1]] = None; i -= 1

    rows = []
    for k, pi in enumerate(plaque):
        n = mapping.get(pi)
        sc = cos(plaque_vec[k], slide_vec[n]) if n else 0.0
        rows.append({'idx': pi, 'slide': n, 'score': round(sc, 2)})

    json.dump({'rows': rows}, open(OUT_MAP, 'w', encoding='utf-8'), ensure_ascii=False)

    # отчёт
    lines = []
    lines.append('Плашек: %d, слайдов: %d\n' % (Pn, Sn))
    byscore = {'сильная (>=12)': 0, 'средняя (6-12)': 0, 'слабая (3-6)': 0, 'никакая (<3)': 0}
    for r in rows:
        if r['slide'] is None: byscore['никакая (<3)'] += 1
        elif r['score'] >= 12: byscore['сильная (>=12)'] += 1
        elif r['score'] >= 6: byscore['средняя (6-12)'] += 1
        elif r['score'] >= 3: byscore['слабая (3-6)'] += 1
        else: byscore['никакая (<3)'] += 1
    lines.append('Оценка сопоставления: %s' % json.dumps(byscore, ensure_ascii=False))
    lines.append('')
    mono = all(r['slide'] is None or (rows[k-1]['slide'] is None or r['slide'] >= rows[k-1]['slide']) for k, r in enumerate(rows) if k > 0)
    lines.append('Монотонность номеров: %s' % mono)
    lines.append('')
    lines.append('Плашки без уверенного соответствия (score < 3) — вставить номер вручную или оставить пустым:')
    for r in rows:
        if r['slide'] is None or r['score'] < 3:
            c = ' '.join(ctx(r['idx'], 4))[:80]
            lines.append('  idx=%d -> %s | %s' % (r['idx'], r['slide'], c))

    open(OUT_REPORT, 'w', encoding='utf-8').write('\n'.join(lines))
    print('OK: mapping -> %s, отчёт -> %s' % (OUT_MAP, OUT_REPORT))

if __name__ == '__main__':
    main()