from copy import deepcopy
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


SOURCE = Path(r"C:\Users\marcenuk\Desktop\АП_Модуль 3\Проекты\1_Машинизация.pptx")
OUT_DIR = SOURCE.parent / "_пример_оформления"
OUTPUT = OUT_DIR / "1_Машинизация_полная_версия_по_шаблону.pptx"

NAVY = RGBColor(0, 49, 98)
INK = RGBColor(26, 31, 38)
MUTED = RGBColor(91, 103, 117)
PAPER = RGBColor(229, 234, 239)
WHITE = RGBColor(255, 255, 255)
LINE = RGBColor(190, 201, 212)


def rgb_fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def add_rect(slide, x, y, w, h, color, rounded=False):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    rgb_fill(shape, color)
    return shape


def set_run(run, color, size=None, bold=False):
    run.font.name = "Mont"
    run.font.color.rgb = color
    if size:
        run.font.size = Pt(size)
    run.font.bold = bold


def restyle_text(shape, slide_height):
    if not hasattr(shape, "text_frame") or not shape.text.strip():
        return
    top = shape.top / 914400
    height = shape.height / 914400
    is_header = top < 0.7
    is_footer = top > slide_height - 0.7 and len(shape.text.strip()) < 4
    for paragraph in shape.text_frame.paragraphs:
        paragraph.space_after = Pt(3)
        paragraph.line_spacing = 1.05
        for run in paragraph.runs:
            if is_header:
                set_run(run, WHITE, 19, True)
            elif is_footer:
                set_run(run, NAVY, 9, True)
            else:
                length = len(run.text.strip())
                size = 16 if length < 80 else 12
                set_run(run, INK, size, False)
    shape.text_frame.word_wrap = True


def style_source():
    OUT_DIR.mkdir(exist_ok=True)
    prs = Presentation(SOURCE)
    width = prs.slide_width / 914400
    height = prs.slide_height / 914400

    for index, slide in enumerate(prs.slides, start=1):
        # Preserve every original object; only add a visual frame around it.
        background = slide.background
        background.fill.solid()
        background.fill.fore_color.rgb = PAPER

        title_candidates = [
            sh for sh in slide.shapes
            if hasattr(sh, "text_frame") and sh.text.strip() and sh.top / 914400 < 0.7
        ]
        title = min(title_candidates, key=lambda sh: sh.top) if title_candidates else None

        # Put the title into the supplied Academy template's blue title band.
        add_rect(slide, 0, 0, width, 0.64, NAVY)
        add_rect(slide, 0, 0, 0.14, height, NAVY)
        if title:
            title.left = Inches(0.42)
            title.top = Inches(0.11)
            title.width = Inches(width - 0.8)
            title.height = Inches(0.38)

        for shape in slide.shapes:
            if shape is title:
                continue
            restyle_text(shape, height)
            if shape.shape_type == 1 and not hasattr(shape, "text_frame"):
                # Existing geometric elements become quieter support shapes.
                try:
                    shape.fill.fore_color.rgb = WHITE
                    shape.line.color.rgb = LINE
                except (AttributeError, ValueError):
                    pass

        # A restrained footer makes the six-team series feel like one Academy event.
        footer = slide.shapes.add_textbox(Inches(width - 2.6), Inches(height - 0.34), Inches(2.2), Inches(0.16))
        footer.text_frame.clear()
        p = footer.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        run = p.add_run()
        run.text = f"АКАДЕМИЯ ПУТИ  •  {index:02d}"
        set_run(run, MUTED, 8, True)

    prs.save(OUTPUT)
    source_images = sum(1 for slide in Presentation(SOURCE).slides for shape in slide.shapes if shape.shape_type == 13)
    result = Presentation(OUTPUT)
    result_images = sum(1 for slide in result.slides for shape in slide.shapes if shape.shape_type == 13)
    print(f"saved={OUTPUT}")
    print(f"slides={len(result.slides)} source_images={source_images} result_images={result_images}")


if __name__ == "__main__":
    style_source()
