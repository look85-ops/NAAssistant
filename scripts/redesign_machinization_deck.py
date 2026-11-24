from pathlib import Path
from io import BytesIO
import re

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


SOURCE = Path(r"C:\Users\marcenuk\Desktop\АП_Модуль 3\Проекты\1_Машинизация.pptx")
OUTPUT = SOURCE.parent / "_пример_оформления" / "1_Машинизация_расширенная_через_дизайнер.pptx"
# Use the Academy's standard 16:9 canvas, with enough room for readable source copy.
W, H = 13.333, 7.5
NAVY = RGBColor(0, 49, 98)
INK = RGBColor(27, 35, 44)
MUTED = RGBColor(96, 108, 121)
PAPER = RGBColor(229, 234, 239)
WHITE = RGBColor(255, 255, 255)
BLUE2 = RGBColor(55, 108, 151)
LINE = RGBColor(191, 203, 214)


def text(slide, value, x, y, w, h, size=14, color=INK, bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear(); tf.word_wrap = True; tf.margin_left = Inches(.06); tf.margin_right = Inches(.06)
    tf.margin_top = Inches(.03); tf.margin_bottom = Inches(.03); tf.vertical_anchor = MSO_ANCHOR.TOP
    p = tf.paragraphs[0]; p.alignment = align; p.space_after = Pt(2); p.line_spacing = 1.03
    r = p.add_run(); r.text = value; r.font.name = "Mont"; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color
    return box


def text_chunks(slide, value, x, y, w, h, size=11, color=INK, gap=0.06, max_chars=125):
    """Render long source copy as separate editable blocks instead of one wall."""
    paragraphs = [part.strip() for part in value.replace("\r", "").split("\n") if part.strip()]
    expanded = []
    for paragraph in paragraphs:
        sentence = paragraph
        while len(sentence) > max_chars:
            cut = max(sentence.rfind(" ", 0, max_chars), sentence.rfind(",", 0, max_chars), int(max_chars * .65))
            expanded.append(sentence[:cut].strip())
            sentence = sentence[cut:].strip()
        expanded.append(sentence)
    paragraphs = expanded
    if not paragraphs:
        return
    item_h = max(0.18, min(0.78, (h - gap * max(0, len(paragraphs) - 1)) / len(paragraphs)))
    for i, paragraph in enumerate(paragraphs):
        text(slide, paragraph, x, y + i * (item_h + gap), w, item_h, size, color)


def add_notes(slide, note):
    notes = slide.notes_slide.notes_text_frame
    notes.text = note


def rect(slide, x, y, w, h, color, radius=False, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                                   Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid(); shape.fill.fore_color.rgb = color
    if line:
        shape.line.color.rgb = line
    else:
        shape.line.fill.background()
    return shape


def add_image(slide, blob, x, y, w, h):
    slide.shapes.add_picture(BytesIO(blob), Inches(x), Inches(y), Inches(w), Inches(h))


def source_data():
    src = Presentation(SOURCE)
    data = []
    for slide in src.slides:
        texts = [sh.text.strip() for sh in slide.shapes if hasattr(sh, "text_frame") and sh.text.strip()]
        images = [sh.image.blob for sh in slide.shapes if sh.shape_type == 13]
        data.append((texts, images))
    return data


def chrome(prs, title, number, dark=False):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide, 0, 0, W, H, NAVY if dark else PAPER)
    rect(slide, 0, 0, .14, H, NAVY)
    text(slide, title, .48, .14, 11.9, .52, 18, WHITE if dark else NAVY, True)
    text(slide, f"АКАДЕМИЯ ПУТИ  •  {number:02d}", 10.8, H - .45, 2.1, .3, 10, RGBColor(185, 198, 210), True, PP_ALIGN.RIGHT)
    add_notes(slide, f"Слайд {number}. Материалы и формулировки сохранены из исходной презентации. Проверить цифры и финальные формулировки перед защитой.")
    return slide


def small_body(slide, values, x, y, w, h, size=11):
    if values:
        value = values if isinstance(values, str) else "\n".join(values)
        text(slide, value, x, y, w, h, size, INK)


def build():
    data = source_data()
    prs = Presentation(); prs.slide_width = Inches(W); prs.slide_height = Inches(H)

    # 1. Title: keep title and subtitle, use the two source images as a restrained background pair.
    vals, imgs = data[0]
    s = chrome(prs, "", 1, True)
    if len(imgs) >= 1: add_image(s, imgs[0], 7.35, .75, 2.1, 1.45)
    if len(imgs) >= 2: add_image(s, imgs[1], 7.35, 2.38, 2.1, 1.45)
    text(s, vals[0] if vals else "", .65, .72, 6.2, .4, 13, RGBColor(194, 210, 224), True)
    text(s, vals[1] if len(vals) > 1 else "", .65, 1.45, 6.3, 1.0, 29, WHITE, True)
    text_chunks(s, vals[2] if len(vals) > 2 else "", .7, 2.75, 6.5, 2.35, 11, RGBColor(216, 225, 234))
    text(s, "ПРОЕКТНАЯ РАБОТА", .7, 4.82, 3, .35, 10, RGBColor(194, 210, 224), True)

    # 2. Context: convert the long list into a two-column reading path.
    vals, _ = data[1]; s = chrome(prs, vals[0] if vals else "Контекст", 2)
    text(s, vals[1] if len(vals) > 1 else "", .55, .82, 8.85, 1.55, 15, NAVY, True)
    rect(s, .55, 1.75, 4.3, 3.0, WHITE, True)
    rect(s, 5.15, 1.75, 4.3, 3.0, NAVY, True)
    left = vals[2:6]; right = vals[6:]
    text_chunks(s, "\n".join(f"• {v}" for v in left), .78, 2.05, 3.85, 2.45, 11)
    text_chunks(s, "\n".join(f"• {v}" for v in right), 5.38, 2.05, 3.85, 2.45, 11)

    # 3. Context continuation: long source lists get their own breathing room.
    s = chrome(prs, "Контекст проекта: что нужно изменить", 3)
    text(s, "Ожидаемый результат машинизации", .55, .82, 8.8, .42, 17, NAVY, True)
    continuation = vals[6:]
    for i, value in enumerate(continuation):
        y = 1.48 + i * .78
        rect(s, .65, y + .04, .16, .16, NAVY, True)
        text_chunks(s, value, .98, y - .02, 8.15, .62, 11, INK)

    # 3. Metrics: preserve every metric text, give the numbers a clear stage.
    vals, _ = data[2]; s = chrome(prs, vals[0] if vals else "Исходные показатели", 4)
    text(s, vals[1] if len(vals) > 1 else "", .55, .82, 8.6, .65, 13, MUTED)
    chunks = vals[2:]
    for i in range(4):
        x = .55; y = 1.55 + i * 1.35
        rect(s, x, y, 11.5, .82, WHITE, True)
        if chunks:
            value = chunks[i * 2] if i * 2 < len(chunks) else ""
            label = chunks[i * 2 + 1] if i * 2 + 1 < len(chunks) else ""
            text(s, value, x + .22, y + .16, 2.4, .48, 21, NAVY, True)
            text(s, label, x + 2.85, y + .16, 9.8, 1.55, 11, MUTED)

    # 4. Idea: split the original long process description instead of shrinking it.
    vals, _ = data[3]; source_process = vals[1] if len(vals) > 1 else ""
    parts = [part.strip() for part in source_process.split("\n") if part.strip()]
    s = chrome(prs, vals[0] if vals else "Идея проекта", 5, True)
    text(s, parts[0] if parts else "", .72, 1.15, 8.4, 2.15, 16, WHITE)
    text(s, "Ключевая мысль проекта", .75, 3.15, 4, .36, 10, RGBColor(194, 210, 224), True)
    text(s, vals[2] if len(vals) > 2 else "", .75, 3.62, 8.15, 1.5, 14, RGBColor(216, 225, 234))

    s = chrome(prs, "Как работает мобильный комплекс", 6)
    text_chunks(s, "\n".join(parts[1:4]), .7, .95, 8.55, 3.85, 10, INK)

    s = chrome(prs, "Как работает мобильный комплекс: продолжение", 7)
    text_chunks(s, "\n".join(parts[4:]), .7, .95, 8.55, 3.85, 10, INK)

    # 5. Equipment: preserve all nine photos in a clean contact sheet and move long captions under it.
    vals, imgs = data[4]; s = chrome(prs, vals[0] if vals else "Оборудование", 8)
    text(s, vals[1] if len(vals) > 1 else "", .55, .78, 8.9, .6, 12, MUTED)
    photo_w, photo_h = 1.72, 1.03
    for i, blob in enumerate(imgs[:5]):
        x = .62 + (i % 5) * 1.83; y = 1.36
        add_image(s, blob, x, y, photo_w, photo_h)
    captions = vals[2:]
    text_chunks(s, "\n".join(captions[:3]), .65, 3.05, 8.75, 3.35, 10, max_chars=320)

    # 7. Equipment continuation: the remaining photographs and specifications are readable here.
    s = chrome(prs, "Оборудование: характеристики", 9)
    for i, blob in enumerate(imgs[5:9]):
        add_image(s, blob, .7 + i * 2.28, 1.0, 2.05, 1.35)
    text_chunks(s, "\n".join(captions[3:7]), .72, 2.8, 8.65, 3.45, 10, max_chars=220)

    s = chrome(prs, "Оборудование: характеристики, продолжение", 10)
    text_chunks(s, "\n".join(captions[7:]), .72, .95, 8.65, 5.35, 10, INK, max_chars=220)

    # 6. Preserve the single source image and title as a visual pause.
    vals, imgs = data[5]; s = chrome(prs, vals[0] if vals else "Техника", 11, True)
    if imgs: add_image(s, imgs[0], 5.85, .82, 3.3, 3.65)
    text(s, vals[0] if vals else "", .72, 1.45, 4.5, .7, 25, WHITE, True)
    text(s, "Крупный визуальный слайд для объяснения конкретного решения.", .75, 2.55, 4.35, .65, 14, RGBColor(216, 225, 234))

    # 7. Economics: original calculation lines become a readable vertical story.
    vals, imgs = data[6]; s = chrome(prs, vals[0] if vals else "Расчёт затрат", 12)
    for i, value in enumerate(vals[1:]):
        y = .95 + i * .86
        rect(s, .62, y, .12, .28, NAVY, True)
        text(s, value, .94, y - .01, 7.7, .82, 11 if i < 4 else 15, NAVY if i == 3 else INK)
    for i, blob in enumerate(imgs[:4]):
        add_image(s, blob, 8.15 + (i % 2) * .82, 1.0 + (i // 2) * .82, .7, .7)

    # 8. Table: retain the actual table as a full-width, readable object.
    vals, _ = data[7]; s = chrome(prs, vals[0] if vals else "Расходы", 13)
    text(s, vals[1] if len(vals) > 1 else "", .55, .82, 8.8, .65, 14, NAVY, True)
    source = Presentation(SOURCE).slides[7]
    table = next((sh for sh in source.shapes if sh.has_table), None)
    if table:
        rows, cols = len(table.table.rows), len(table.table.columns)
        out = s.shapes.add_table(rows, cols, Inches(.6), Inches(1.55), Inches(8.8), Inches(2.7)).table
        for r in range(rows):
            for c in range(cols):
                out.cell(r, c).text = table.table.cell(r, c).text
                out.cell(r, c).fill.solid(); out.cell(r, c).fill.fore_color.rgb = NAVY if r == 0 else WHITE
                for p in out.cell(r, c).text_frame.paragraphs:
                    for run in p.runs:
                        run.font.name = "Mont"; run.font.size = Pt(10); run.font.color.rgb = WHITE if r == 0 else INK
                        run.font.bold = r == 0

    # 9. Effect: three claims plus the source text, not a wall of text.
    vals, _ = data[8]; s = chrome(prs, vals[0] if vals else "Экономический эффект", 14)
    text(s, vals[1] if len(vals) > 1 else "", .6, .84, 8.7, .85, 20, NAVY, True)
    text(s, vals[2] if len(vals) > 2 else "", .65, 1.62, 8.5, .6, 13, MUTED)
    rect(s, .65, 2.25, 8.7, 1.15, WHITE, True)
    text_chunks(s, vals[3] if len(vals) > 3 else "", .9, 2.55, 8.2, .85, 12, INK)
    text(s, "Вывод проекта", .65, 4.15, 3, .25, 10, NAVY, True)
    text_chunks(s, vals[4] if len(vals) > 4 else "", .65, 4.5, 8.3, .8, 14, NAVY, True)

    # 10. Finish: retain final phrase and make it stage-ready.
    vals, _ = data[9]; s = chrome(prs, "", 15, True)
    text(s, vals[-1] if vals else "", .75, 1.65, 8.3, 1.1, 30, WHITE, True)
    text(s, "Спасибо за внимание", .78, 4.7, 5, .35, 14, RGBColor(216, 225, 234))

    OUTPUT.parent.mkdir(exist_ok=True)
    prs.save(OUTPUT)
    original = Presentation(SOURCE)
    result = Presentation(OUTPUT)
    source_images = sum(1 for sl in original.slides for sh in sl.shapes if sh.shape_type == 13)
    result_images = sum(1 for sl in result.slides for sh in sl.shapes if sh.shape_type == 13)
    print(f"saved={OUTPUT}")
    print(f"slides={len(result.slides)} source_images={source_images} result_images={result_images}")


if __name__ == "__main__":
    build()
