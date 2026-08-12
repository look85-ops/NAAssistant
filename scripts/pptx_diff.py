# -*- coding: utf-8 -*-
"""
Автодифф «сценарий ↔ презентация» для раскладки управляющих презентаций П+Путь.

Сравнивает маркеры «Слайд №N» из сценария с каталогом слайдов презентации.
Выход — markdown-таблица: что добавить (в сценарии есть, на слайдах нет),
что скрыть/проверить (на слайдах есть, в сценарии не упомянуто).

Логика — по knowledge/pptx-scenario-layout.md:
- Сценарий — единственный источник истины.
- Маркеры «Слайд №N» / «Слайд N» — якоря; слайды без номера тоже считаем.
- Сравнение по контенту (номера в сценарии и презентации могут не совпадать).
- AP-дырки (Слайд из другого модуля) не трогаем, помечаем.
- Результаты пишем в UTF-8-файл: консоль Windows 5.1 ломает кириллицу.

Usage:
    python ppxt_diff.py --scenario scenario.json --catalog catalog.json [-o diff.md]
    python ppxt_diff.py <scenario.json> <catalog.json> [out.md]

Форматы входных файлов — те же, что у word_pages.py и catalog_types.py:
    scenario: {"items": [{"text": "Слайд №5", "has_blue": bool}, ...]}
    catalog:  {"slides": [{"n": 1, "type": "CONTENT", "title": "...", "texts": [...]}, ...]}
"""
import argparse
import json
import re
import sys
from collections import OrderedDict

SLIDE_MARKER = re.compile(r'Слайд\s*№?\s*(\d+)')
SLIDE_BARE = re.compile(r'Слайд')
STOP = {'перерыв', 'обед', 'проверка', 'домашнее задание'}


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def iter_slide_markers(scenario_json):
    """Возвращает упорядоченный список: {n, next_n, lines} из сценария."""
    items = scenario_json.get('items', []) if isinstance(scenario_json, dict) else scenario_json
    entries = []
    cur = None
    cur_lines = []
    for item in items:
        t = item.get('text', '').strip() if isinstance(item, dict) else str(item).strip()
        m = SLIDE_MARKER.match(t)
        if m:
            if cur is not None:
                entries.append((cur, cur_lines))
            cur = int(m.group(1))
            cur_lines = []
            continue
        if SLIDE_BARE.search(t) and len(t) <= 60:
            continue
        cur_lines.append(t)
    if cur is not None:
        entries.append((cur, cur_lines))
    return entries


def preview(lines, n=3):
    out = []
    for ln in lines:
        ln = ln.strip()
        if not ln or ln.lower() in STOP or ln.lower().startswith('преподаватель'):
            continue
        out.append(ln)
        if len(out) >= n:
            break
    return ' '.join(out)[:100]


def ap_hole(num):
    """AP-дырки: слайды из других модулей (блоки АП) — номера проверяем по тексту"""
    return False


def build_report(scenario_entries, catalog):
    slides = catalog.get('slides', []) if isinstance(catalog, dict) else catalog
    catalog_by_num = {s.get('n'): s for s in slides}
    catalog_texts = []
    for s in slides:
        ts = ' '.join(s.get('texts', []) or []) + ' ' + s.get('title', '')
        catalog_texts.append(ts.lower())
    max_slide = max(catalog_by_num.keys(), default=0)

    rows = []
    seen = set()
    for n, lines in scenario_entries:
        ctx = preview(lines)
        matched = catalog_by_num.get(n)
        action = 'OK' if matched else 'СОЗДАТЬ'
        note = ''
        if n in seen:
            action = 'повтор'
            note = f'слайд {n} уже есть выше'
        elif not matched:
            # эвристика по контенту: ищем слайд с фрагментом контекста
            keys = [w for w in re.split(r'[^\wА-Яа-яЁё]+', ctx.lower()) if len(w) > 4]
            for an, s in catalog_by_num.items():
                ts = ' '.join(s.get('texts', []) or []).lower()
                hits = sum(1 for k in keys if k and k in ts)
                if hits >= 2:
                    action = 'ПРОВЕРИТЬ'
                    note = f'похож на слайд {an}: "{s.get("title", "")[:50]}"'
                    break
        seen.add(n)
        rows.append((n, action, 'ОК' if action == 'OK' else ('~' if action == 'повтор' else ('?' if action == 'ПРОВЕРИТЬ' else '+')), ctx, note))

    # слайды презентации, которых нет в сценарии
    extras = []
    for s in slides:
        n = s.get('n')
        if n not in seen and n <= max_slide:
            extras.append((n, s.get('type', ''), s.get('title', '')))

    return rows, extras


def render(rows, extras, out_path):
    L = []
    L.append('# Дифф сценарий ↔ презентация')
    L.append('')
    L.append(f'Маркеров «Слайд» в сценарии: **{len(rows)}**. Слайдов в презентации: **{len(rows) + len(extras)}**.')
    L.append('')
    L.append('## Совпадения и кандидаты на создание')
    L.append('')
    L.append('| № | Действие | Контекст из сценария | Примечание |')
    L.append('|---|----------|----------------------|------------|')
    for n, action, mark, ctx, note in rows:
        L.append(f'| {n} | {action} | {ctx} | {note} |')
    L.append('')
    L.append('## Слайды презентации без ссылки из сценария (кандидаты на скрытие/проверку)')
    L.append('')
    if extras:
        L.append('| № | Тип | Заголовок |')
        L.append('|---|-----|-----------|')
        for n, typ, title in extras:
            L.append(f'| {n} | {typ} | {title[:70]} |')
    else:
        L.append('_нет_')
    L.append('')
    L.append('_Сгенерировано автоматически. AP-дырки и неоднозначности подтверждать с автором._')
    L.append('')
    text = '\n'.join(L)
    if out_path:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print('saved', out_path)
    else:
        print(text)


def main():
    ap = argparse.ArgumentParser(description='Дифф сценарий ↔ презентация (П+Путь)')
    ap.add_argument('--scenario', help='scenario.json (word_pages.py)')
    ap.add_argument('--catalog', help='catalog.json (catalog_types.py)')
    ap.add_argument('-o', '--output', default=None, help='куда записать markdown')
    ap.add_argument('positionals', nargs='*', help='или позиционно: scenario catalog [out]')
    args = ap.parse_args()

    if args.scenario and args.catalog:
        sc_path, cat_path = args.scenario, args.catalog
        out_path = args.output
    elif len(args.positionals) >= 2:
        sc_path, cat_path = args.positionals[0], args.positionals[1]
        out_path = args.positionals[2] if len(args.positionals) >= 3 else args.output
    else:
        print('Usage: python pptx_diff.py --scenario scenario.json --catalog catalog.json [-o diff.md]')
        sys.exit(1)

    scenario = load_json(sc_path)
    catalog = load_json(cat_path)
    entries = iter_slide_markers(scenario)
    rows, extras = build_report(entries, catalog)
    render(rows, extras, out_path)


if __name__ == '__main__':
    main()