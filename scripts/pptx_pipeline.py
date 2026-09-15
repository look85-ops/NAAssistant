# -*- coding: utf-8 -*-
"""
Единый CLI-конвейер раскладки управляющих презентаций по сценарию (П+Путь/П+Энергия).

Две фазы (между ними презентация уходит к дизайнеру):

Фаза A — сценарий → презентация (актуализация, правки до дизайнера):
    parse    scenario.docx → scenario.json   (XML для >50MB, Word COM для малых)
    catalog  pres.pptx     → catalog.json    (python-pptx; копия на латинский путь)
    diff     scenario.json + catalog.json → diff.md (добавить/исправить/скрыть)
    update   pres.pptx + operations.json → правки через COM (clone/edit/hide)
    layout   pres.pptx + target_order.txt → перестановка по карте (COM MoveTo)
    validate pres.pptx [--map] [--orig] → отчёт: count/hidden/порядок/smoke

Фаза B — презентация → сценарий (после дизайнера):
    export   pres.pptx outdir [--range] → PNG слайдов (COM Export)
    insert   scenario.docx out.docx slide_dir → PNG по меткам «Слайд» (по контенту, без номеров)

Процесс «сценарий с нуля» (generate) — задел, не реализован.

Принципы (knowledge/pptx-layout-workflow.md, pptx-scenario-layout.md):
- сценарий — единственный источник истины; ориентация по контенту, не по номерам
- новые слайды — только клонированием образца (COM), не с нуля
- layout — от конца к началу (MoveTo), чтобы позиции не сбивались
- кириллица: результаты писать в UTF-8-файлы, консоль Windows 5.1 ломает вывод
- python-pptx не дружит с кириллицей в путях → рабочая копия на латинский temp-путь

Usage:
    python pptx_pipeline.py parse <scenario.docx> <scenario.json>
    python pptx_pipeline.py catalog <pres.pptx> <catalog.json>
    python pptx_pipeline.py diff <scenario.json> <catalog.json> [-o diff.md]
    python pptx_pipeline.py update <pres.pptx> <operations.json> [--backup]
    python pptx_pipeline.py layout <pres.pptx> <target_order.txt> [--backup]
    python pptx_pipeline.py validate <pres.pptx> [--map target_order.txt] [--orig orig.pptx] [-o report.txt]
    python pptx_pipeline.py export <pres.pptx> <outdir> [--range 1-20] [--visible]
    python pptx_pipeline.py insert <scenario.docx> <result.docx> <slide_dir> [--width-cm 8.8]
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PYTHON = os.environ.get('PYTHON_EXE', sys.executable)
TEMP = os.environ.get('TEMP', tempfile.gettempdir())
WORK = os.path.join(TEMP, 'opencode', 'pipeline')
os.makedirs(WORK, exist_ok=True)

# команда запуска наших же python-скриптов с сохранением окружения
BASE_CMD = [PYTHON]


def latin_copy(path, name):
    """Копирует большой файл на латинский путь (python-pptx ломается на кириллице)."""
    dst = os.path.join(WORK, name)
    shutil.copy2(path, dst)
    return dst


def run(cmd, timeout=3600):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
    if r.returncode != 0:
        sys.stderr.write('CMD FAILED: %s\n' % ' '.join(cmd))
        sys.stderr.write(r.stdout[-4000:] + r.stderr[-4000:])
        sys.exit(1)
    return r.stdout


# ── parse ─────────────────────────────────────────────────────────────
def cmd_parse(args):
    docx, out = args.scenario, args.output
    size_mb = os.path.getsize(docx) / 1e6
    if size_mb > 50:
        # XML-парсер: большие docx Word COM не открывает (виснет)
        src = latin_copy(docx, 'scenario.docx')
        run(BASE_CMD + [os.path.join(HERE, 'parse_scenario_xml.py'), src, out])
    else:
        src = latin_copy(docx, 'scenario.docx')
        run(BASE_CMD + [os.path.join(HERE, 'word_pages.py'), src, out])
    print('parse ok ->', out)


# ── catalog ───────────────────────────────────────────────────────────
def cmd_catalog(args):
    pptx, out = args.presentation, args.output
    src = latin_copy(pptx, 'pres.pptx')
    run(BASE_CMD + [os.path.join(HERE, 'catalog_types.py'), src, out])
    print('catalog ok ->', out)


# ── diff ──────────────────────────────────────────────────────────────
def cmd_diff(args):
    out = args.output or os.path.join(WORK, 'diff.md')
    run(BASE_CMD + [os.path.join(HERE, 'pptx_diff.py'), '--scenario', args.scenario,
                    '--catalog', args.catalog, '-o', out])
    print('diff ok ->', out)


# ── update ────────────────────────────────────────────────────────────
def cmd_update(args):
    pptx, ops_path = args.presentation, args.operations
    if not os.path.exists(args.operations):
        sys.exit('operations.json not found: %s' % ops_path)
    src = latin_copy(pptx, 'pres_work.pptx')
    if args.backup:
        shutil.copy2(pptx, pptx + '.backup_' + __import__('time').strftime('%Y%m%d_%H%M%S') + '.pptx')
    ops = json.load(open(ops_path, encoding='utf-8'))
    # подключаем pptx_com как модуль рядом
    sys.path.insert(0, HERE)
    import pptx_com as pc
    app, pres = pc.open_pptx(src)
    log = ['=== update ===', 'ops: %d' % len(ops.get('operations', []))]
    report = apply_operations(pres, ops.get('operations', []), log)
    pc.close_pptx(app, pres, save=True)
    shutil.copy2(src, pptx)
    log += report
    write_log(args.log, log) if args.log else sys.stdout.write('\n'.join(log) + '\n')


def apply_operations(pres, operations, log):
    """Выполняет [clone/edit/hide] из operations.json. Формат — как pptx-scenario-layout."""
    import pptx_com as pc
    report = []
    done_c, done_e, done_h = 0, 0, 0
    for op in operations:
        kind = op.get('op')
        try:
            if kind == 'clone':
                idx = op.get('from')
                new_idx = pc.duplicate_slide(pres, idx)
                clone = pres.Slides.Item(new_idx)
                for old, new in (op.get('replace') or {}).items():
                    if old in ' '.join(clone_slide_text(clone)):
                        pc.replace_text_in_slide(clone, {old: new})
                if op.get('tag'):
                    pc.add_tag(clone, op['tag'])
                if 'to' in op and op['to'] != new_idx:
                    pres.Slides.Item(new_idx).MoveTo(op['to'])
                done_c += 1
                report.append('clone %s -> pos %s ok' % (idx, op.get('to', new_idx)))
            elif kind == 'edit':
                slide = find_slide(pres, op)
                if slide is None:
                    report.append('EDIT FAIL: not found %s' % op.get('find'))
                    continue
                pc.replace_text_in_slide(slide, op.get('replace') or {})
                if op.get('tag'):
                    pc.add_tag(slide, op['tag'])
                done_e += 1
                report.append('edit ok')
            elif kind == 'hide':
                slide = find_slide(pres, op)
                if slide is None:
                    report.append('HIDE FAIL: not found %s' % op.get('find'))
                    continue
                pc.hide_slide(pres, slide_number(pres, slide))
                done_h += 1
                report.append('hide ok')
        except Exception as ex:
            report.append('%s FAIL: %s' % (kind, ex))
    report.append('SUMMARY: clone=%d edit=%d hide=%d' % (done_c, done_e, done_h))
    return report


def clone_slide_text(slide):
    texts = []
    for i in range(1, slide.Shapes.Count + 1):
        shp = slide.Shapes.Item(i)
        try:
            if shp.HasTextFrame and shp.TextFrame.HasText == -1:
                texts.append(shp.TextFrame.TextRange.Text or '')
        except Exception:
            pass
    return texts


def find_slide(pres, op):
    import pptx_com as pc
    if op.get('slide'):
        try:
            return pres.Slides.Item(int(op['slide']))
        except Exception:
            return None
    sub = op.get('find')
    for i in range(1, pres.Slides.Count + 1):
        s = pres.Slides.Item(i)
        if any(sub in t for t in clone_slide_text(s)):
            return s
    return None


def slide_number(pres, slide):
    for i in range(1, pres.Slides.Count + 1):
        if pres.Slides.Item(i).SlideID == slide.SlideID:
            return i
    return None


# ── layout ────────────────────────────────────────────────────────────
def cmd_layout(args):
    pptx, map_file = args.presentation, args.map
    src = latin_copy(pptx, 'pres_layout.pptx')
    if args.backup:
        shutil.copy2(pptx, pptx + '.backup_' + __import__('time').strftime('%Y%m%d_%H%M%S') + '.pptx')
    target = read_map(map_file)
    sys.path.insert(0, HERE)
    import pptx_com as pc
    app, pres = pc.open_pptx(src)
    total = pres.Slides.Count
    assert len(target) == total, 'map=%d != slides=%d' % (len(target), total)
    assert sorted(target) == list(range(1, total + 1)), 'map not a permutation: %s' % sorted(target)

    # фиксируем SlideID исходных слайдов до каких-либо движений
    sid_of = {}  # исходный порядковый номер → SlideID
    for i in range(1, total + 1):
        sid_of[i] = pres.Slides.Item(i).SlideID

    def cur_pos(slide_id):
        for i in range(1, pres.Slides.Count + 1):
            if pres.Slides.Item(i).SlideID == slide_id:
                return i
        return None

    moved = 0
    # карта: target[i-1] = исходный номер, который должен стать позицией i.
    # обрабатываем от конца к началу, чтобы позиции < i не сбивались
    for i in range(total, 0, -1):
        want_src = target[i - 1]
        cur = cur_pos(sid_of[want_src])
        if cur == i:
            continue
        pres.Slides.Item(cur).MoveTo(i)
        moved += 1
    pc.close_pptx(app, pres, save=True)
    shutil.copy2(src, pptx)
    print('layout ok: %d/%d moved, total=%d' % (moved, total, total))


def read_map(path):
    out = []
    with open(path, encoding='utf-8') as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith('#'):
                continue
            try:
                out.append(int(ln.split()[0]))
            except ValueError:
                continue
    return out


# ── validate ──────────────────────────────────────────────────────────
def cmd_validate(args):
    pptx = args.presentation
    out_path = args.output or os.path.join(WORK, 'validate_report.txt')
    size_mb = os.path.getsize(pptx) / 1e6
    if size_mb > 60:
        # гигантские файлы не тянем в python-pptx надёжно — smoke через COM
        report = validate_com(pptx, args)
    else:
        report = validate_pptx(pptx, args)
    txt = '\n'.join(report)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(txt)
    print('validate report ->', out_path)
    print('\n'.join(report))


def validate_pptx(pptx, args):
    src = latin_copy(pptx, 'pres_val.pptx')
    from pptx import Presentation
    prs = Presentation(src)
    report = []
    report.append('count=%d' % len(prs.slides._sldIdLst))
    blanks = sum(1 for s in prs.slides if not any(sh.has_text_frame and sh.text_frame.text.strip() for sh in s.shapes if not sh.has_chart))
    report.append('blank_like=%d' % blanks)
    if args.map:
        target = read_map(args.map)
        report.append('map=%d matches=%s' % (len(target), len(target) == len(prs.slides._sldIdLst)))
    if args.orig:
        report.append('orig_present=%s' % os.path.exists(args.orig))
    return report


def validate_com(pptx, args):
    sys.path.insert(0, HERE)
    import pptx_com as pc
    app, pres = pc.open_pptx(pptx)
    total = pres.Slides.Count
    report = ['count=%d' % total]
    hidden = sum(1 for i in range(1, total + 1)
                 if pres.Slides.Item(i).SlideShowTransition.Hidden == -1)
    report.append('hidden=%d' % hidden)
    pc.close_pptx(app, pres, save=False)
    return report


# ── export (Фаза B) ───────────────────────────────────────────────────
def cmd_export(args):
    pptx, outdir = args.presentation, args.outdir
    os.makedirs(outdir, exist_ok=True)
    import win32com.client
    pp = win32com.client.Dispatch('PowerPoint.Application')
    pp.Visible = True
    try:
        prs = pp.Presentations.Open(pptx, WithWindow=False)
        lo, hi = 1, prs.Slides.Count
        if args.range:
            lo_s, hi_s = args.range.split('-')
            lo, hi = int(lo_s), int(hi_s)
        n = 0
        for sn in range(lo, hi + 1):
            out = os.path.join(outdir, 'slide_%03d.png' % sn)
            if not os.path.exists(out):
                prs.Slides(sn).Export(out, 'PNG')
                n += 1
        prs.Close()
        print('export ok: %d slides -> %s' % (n, outdir))
    finally:
        pp.Quit()


# ── insert (Фаза B) ───────────────────────────────────────────────────
def cmd_insert(args):
    from docx import Document
    from docx.shared import Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    import zipfile
    from lxml import etree

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    wp = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
    bl = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    MRK = re_compile_slide_marker()

    doc = Document(args.scenario)
    slide_files = sorted(os.listdir(args.slide_dir))
    pngs = [f for f in slide_files if f.lower().endswith('.png')]

    free = []
    tbl_tag = '{%s}tbl' % ns['w']
    p_tag = '{%s}p' % ns['w']
    # Word can put scenario rows into nested tables. Iterate every table
    # element, but only paragraphs whose nearest table is the current one.
    tables = list(doc.element.body.iter(tbl_tag))
    for table_elem in tables:
        rows = list(table_elem.findall('./{%s}tr' % ns['w']))
        for row in rows:
            cells = list(row.findall('./{%s}tc' % ns['w']))
            if len(cells) <= 4:
                continue
            tc = cells[4]
            ps = [p for p in tc.iter(p_tag)
                  if next((a for a in p.iterancestors(tbl_tag)), None) is table_elem]
            for pi, p_elem in enumerate(ps):
                txt = ''.join(x.text or '' for x in p_elem.findall('.//{%s}t' % ns['w'])).strip()
                if not MRK.match(txt):
                    continue
                has_img = (pi + 1 < len(ps)) and (
                    ps[pi + 1].findall('.//{%s}inline' % wp) or
                    ps[pi + 1].findall('.//{%s}blip' % bl))
                if has_img and args.replace_existing:
                    # Rebuild from the current presentation rather than
                    # preserving stale images from an earlier version.
                    ps[pi + 1].getparent().remove(ps[pi + 1])
                    has_img = False
                if not has_img:
                    free.append((table_elem, p_elem))

    # Optional physical-slide mapping for designer-added continuations.
    # Format: {"extra_after": {"139": [140], "175": [178, 179, 180]}}
    insert_map = {}
    if args.insert_map:
        with open(args.insert_map, encoding='utf-8') as f:
            insert_map = json.load(f).get('extra_after', {})

    extra_after = {int(k): list(v) for k, v in insert_map.items()}
    extra_numbers = set(n for values in extra_after.values() for n in values)
    assignments = []
    used = set()
    next_slide = 1
    for ordinal, (_, pe) in enumerate(free, 1):
        while next_slide in extra_numbers:
            next_slide += 1
        slide_no = next_slide
        next_slide += 1
        if slide_no <= len(pngs):
            assignments.append((pe, pngs[slide_no - 1]))
            used.add(slide_no)
        for extra_no in extra_after.get(ordinal, []):
            if 1 <= extra_no <= len(pngs) and extra_no not in used:
                assignments.append((pe, pngs[extra_no - 1]))
                used.add(extra_no)

    # Preserve the original sequential fallback when no map is supplied.
    if not insert_map:
        assignments = [(pe, pngs[i]) for i, (_, pe) in enumerate(free) if i < len(pngs)]

    planned = len(assignments)

    from collections import defaultdict
    bc = defaultdict(list)
    for pe, fn in assignments:
        table_elem = find_table_of_elem(doc, pe)
        bc[table_elem].append((pe, fn))

    ins = 0
    for table_elem, items in reversed(list(bc.items())):
        cps = list(table_elem.findall('.//{%s}p' % ns['w']))
        grouped = defaultdict(list)
        for pe, fn in items:
            if pe in cps:
                grouped[cps.index(pe)].append((pe, fn))
        for pos in sorted(grouped, reverse=True):
            pe = grouped[pos][0][0]
            # Insert in reverse because each new paragraph is added directly
            # after the marker (or the previously inserted image).
            for _, fn in reversed(grouped[pos]):
                p = os.path.join(args.slide_dir, fn)
                if not os.path.exists(p):
                    continue
                np = doc.add_paragraph()
                np.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run_ = np.add_run()
                run_.add_picture(p, width=Cm(float(args.width_cm)))
                pe.addnext(np._element)
                pe = np._element
                ins += 1

    doc.save(args.result)
    print('insert ok: %d images, planned=%d, remaining markers=%d' %
          (ins, planned, max(0, len(free) - ins)))


def find_table_of_elem(doc, pe):
    # lxml may return a different wrapper for the same document tree, so
    # compare the actual table ancestor instead of getroottree() identity.
    cur = pe
    while cur is not None:
        if cur.tag == '{%s}tbl' % 'http://schemas.openxmlformats.org/wordprocessingml/2006/main':
            return cur
        cur = cur.getparent()
    return doc.element.body


def re_compile_slide_marker():
    import re
    return re.compile(r'^Слайд(\s*№\s*\d+)?\s*$')


def write_log(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


# ── CLI ───────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description='ПП+Путь: конвейер раскладки презентаций по сценарию')
    sub = ap.add_subparsers(dest='cmd')

    p = sub.add_parser('parse', help='docx → scenario.json')
    p.add_argument('scenario'); p.add_argument('output'); p.set_defaults(fn=cmd_parse)

    p = sub.add_parser('catalog', help='pptx → catalog.json')
    p.add_argument('presentation'); p.add_argument('output'); p.set_defaults(fn=cmd_catalog)

    p = sub.add_parser('diff', help='scenario.json + catalog.json → diff.md')
    p.add_argument('scenario'); p.add_argument('catalog')
    p.add_argument('-o', '--output', default=None); p.set_defaults(fn=cmd_diff)

    p = sub.add_parser('update', help='команды clone/edit/hide через COM')
    p.add_argument('presentation'); p.add_argument('operations')
    p.add_argument('--backup', action='store_true')
    p.add_argument('--log', default=None); p.set_defaults(fn=cmd_update)

    p = sub.add_parser('layout', help='перестановка по карте target_order.txt')
    p.add_argument('presentation'); p.add_argument('map')
    p.add_argument('--backup', action='store_true'); p.set_defaults(fn=cmd_layout)

    p = sub.add_parser('validate', help='проверки после правок')
    p.add_argument('presentation')
    p.add_argument('--map', default=None); p.add_argument('--orig', default=None)
    p.add_argument('-o', '--output', default=None); p.set_defaults(fn=cmd_validate)

    p = sub.add_parser('export', help='слайды → PNG (Фаза B)')
    p.add_argument('presentation'); p.add_argument('outdir')
    p.add_argument('--range', default=None); p.set_defaults(fn=cmd_export)

    p = sub.add_parser('insert', help='PNG по меткам «Слайд» в docx (Фаза B)')
    p.add_argument('scenario'); p.add_argument('result'); p.add_argument('slide_dir')
    p.add_argument('--width-cm', default='8.8')
    p.add_argument('--insert-map', default=None,
                   help='JSON-карта продолжений: extra_after={marker ordinal: [physical slide numbers]}')
    p.add_argument('--replace-existing', action='store_true',
                   help='удалить старую картинку после маркера и вставить актуальный PNG')
    p.set_defaults(fn=cmd_insert)

    args = ap.parse_args()
    if not getattr(args, 'fn', None):
        ap.print_help()
        sys.exit(1)
    args.fn(args)


if __name__ == '__main__':
    main()
