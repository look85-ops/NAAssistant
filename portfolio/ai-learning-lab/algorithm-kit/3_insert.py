# -*- coding: utf-8 -*-
"""
Шаг 3. Вставка номеров «Слайд №N» и скриншотов в сценарий.

Читает mapping.json (из шага 2), для каждой плашки:
  - ставит текст «Слайд №N»;
  - вставляет новый абзац со скрином (5,5 см по высоте, 16:9) сразу после плашки.

Работает через lxml + zipfile (НЕ python-docx.save) — форматирование не ломается.
Перед запуском открой mapping.json и поправь явные несовпадения (слабые/None).

Использование:
    py 3_insert.py

Настрой CONFIG ниже.
"""
import io
import re
import sys
import os
import json
import zipfile
import shutil
from lxml import etree

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# === CONFIG ===
DOCX = r"путь\к\сценарию.docx"
SLIDES = r"путь\к\папке_для_png"      # та же, куда рендерил 1_render.py
MAPPING = r"mapping.json"
CX = '3519176'   # ширина 16:9 ≈ 9.78 см
CY = '1980000'   # высота 5.5 см
# ==============

W_URI = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W = '{' + W_URI + '}'
REL_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
PIC = 'http://schemas.openxmlformats.org/drawingml/2006/picture'

def main():
    rows = json.load(open(MAPPING, encoding='utf-8'))['rows']
    mapping = {r['idx']: r['slide'] for r in rows if r['slide'] is not None}

    with zipfile.ZipFile(DOCX) as z:
        entries = {n: z.read(n) for n in z.namelist()}
    root = etree.fromstring(entries['word/document.xml'])
    paras = list(root.iter(W + 'p'))

    def ptext(p):
        return ''.join(t.text or '' for t in p.iter(W + 't')).strip()

    rels_path = 'word/_rels/document.xml.rels'
    rels_root = etree.fromstring(entries[rels_path])
    existing_ids = [int(re.sub(r'\D', '', r.get('Id'))) for r in rels_root if re.search(r'\d', r.get('Id', ''))]
    next_rid = [max(existing_ids) + 1]
    def new_rid():
        rid = 'rId%d' % next_rid[0]
        next_rid[0] += 1
        return rid

    inserted = 0
    for i, p in enumerate(paras):
        if i not in mapping:
            continue
        n = mapping[i]
        if not ptext(p).startswith('Слайд'):
            continue
        ts = [t for t in p.iter(W + 't')]
        if ts:
            ts[0].text = 'Слайд №' + str(n)
            for t in ts[1:]:
                t.text = ''

        src_png = os.path.join(SLIDES, 'slide%03d.png' % n)
        if not os.path.exists(src_png):
            print('WARN: нет PNG для слайда %d (пропущен)' % n)
            continue

        media_name = 'media/slide%03d.png' % n
        if ('word/' + media_name) not in entries:
            entries['word/' + media_name] = open(src_png, 'rb').read()

        rid = new_rid()
        rel = etree.SubElement(rels_root, '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')
        rel.set('Id', rid)
        rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
        rel.set('Target', media_name)

        doc_id = 300000 + inserted
        drawing_xml = ('<w:drawing xmlns:w="%s" xmlns:wp="%s" xmlns:a="%s" xmlns:pic="%s" xmlns:r="%s">'
                       '<wp:inline distT="0" distB="0" distL="0" distR="0">'
                       '<wp:extent cx="%s" cy="%s"/><wp:effectExtent l="0" t="0" r="0" b="8890"/>'
                       '<wp:docPr id="%d" name="Рисунок %d"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
                       '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>'
                       '<pic:nvPicPr><pic:cNvPr id="%d" name=""/><pic:cNvPicPr/></pic:nvPicPr>'
                       '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
                       '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%s" cy="%s"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
                       '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing>') % (
            W_URI, WP, A, PIC, REL_NS, CX, CY, doc_id, doc_id, doc_id, rid, CX, CY)

        drawing = etree.fromstring(drawing_xml)
        run = etree.Element(W + 'r')
        rpr = etree.SubElement(run, W + 'rPr')
        etree.SubElement(rpr, W + 'noProof')
        run.append(drawing)

        newp = etree.Element(W + 'p')
        ppr_src = p.find(W + 'pPr')
        if ppr_src is not None:
            newp.append(etree.fromstring(etree.tostring(ppr_src)))
        newp.append(run)
        p.addnext(newp)
        inserted += 1

    entries['word/document.xml'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    entries[rels_path] = etree.tostring(rels_root, xml_declaration=True, encoding='UTF-8', standalone=True)

    tmp = DOCX + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as out:
        for name, data in entries.items():
            out.writestr(name, data)
    shutil.move(tmp, DOCX)
    print('OK: вставлено номеров и скринов — %d, файл сохранён' % inserted)

if __name__ == '__main__':
    main()