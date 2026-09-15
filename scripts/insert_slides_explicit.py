"""Вставка слайдов по явному соответствию «свободный маркер → номер слайда».

Работает поверх существующего DOCX (не пересобирает с нуля): находит все
свободные маркеры «Слайд», берёт из JSON-карты номера слайдов и вставляет
соответствующие PNG сразу после маркера.

Карта: {"map": {<индекс_свободного_маркера_с_нуля>: [номера слайдов в порядке вставки]}}
"""
import argparse
import json
import os

from docx import Document
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

NS_W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS_WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def _text(elem):
    return ''.join(x.text or '' for x in elem.findall('.//{%s}t' % NS_W)).strip()


def _has_img(par):
    return bool(par.findall('.//{%s}inline' % NS_WP) or par.findall('.//{%s}blip' % NS_A))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('docx')
    ap.add_argument('slide_dir')
    ap.add_argument('mapping')
    ap.add_argument('--width-cm', default='8.8')
    args = ap.parse_args()

    with open(args.mapping, encoding='utf-8') as f:
        mapping = json.load(f)['map']

    doc = Document(args.docx)
    tbl_tag = '{%s}tbl' % NS_W
    p_tag = '{%s}p' % NS_W
    import re
    mrk = re.compile(r'^Слайд(\s*№\s*\d*)?\s*$')

    free = []
    for table_elem in doc.element.body.iter(tbl_tag):
        rows = table_elem.findall('./{%s}tr' % NS_W)
        for row in rows:
            cells = row.findall('./{%s}tc' % NS_W)
            if len(cells) <= 4:
                continue
            tc = cells[4]
            ps = [p for p in tc.iter(p_tag)
                  if next((a for a in p.iterancestors(tbl_tag)), None) is table_elem]
            for pi, pe in enumerate(ps):
                txt = _text(pe)
                if not mrk.match(txt):
                    continue
                has = (pi + 1 < len(ps)) and _has_img(ps[pi + 1])
                if not has:
                    free.append((table_elem, pe, pi))

    slide_files = sorted(f for f in os.listdir(args.slide_dir) if f.lower().endswith('.png'))
    width = Cm(float(args.width_cm))

    ins = 0
    # process markers from the end of the document to keep indices stable
    for idx_str, slide_nums in mapping.items():
        idx = int(idx_str)
        if idx >= len(free):
            continue
        table_elem, pe, pi = free[idx]
        png_paths = [os.path.join(args.slide_dir, 'slide_%03d.png' % n) for n in slide_nums]
        png_paths = [p for p in png_paths if os.path.exists(p)]
        # insert in reverse so each new paragraph lands right after the marker
        for p in reversed(png_paths):
            np = doc.add_paragraph()
            np.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = np.add_run()
            run.add_picture(p, width=width)
            pe.addnext(np._element)
            ins += 1

    doc.save(args.docx)
    print('inserted %d images' % ins)


if __name__ == '__main__':
    main()
