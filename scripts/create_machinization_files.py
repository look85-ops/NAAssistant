from pathlib import Path
from copy import deepcopy
import zipfile

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.drawing.image import Image as XLImage
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


SOURCE = Path(r"C:\Users\marcenuk\Desktop\1. Белобородов А. Машинизация.pptx")
WORK = Path(r"C:\Users\marcenuk\Desktop\Новый проект\tmp\machinization")
WORK.mkdir(parents=True, exist_ok=True)
IMAGE = WORK / "excel_source.png"
EXCEL = SOURCE.parent / "1. Белобородов А. Машинизация_данные_слайда_6.xlsx"
PRESENTATION = SOURCE.parent / "1. Белобородов А. Машинизация_с_вариантом_слайда_6.pptx"


def extract_image():
    with zipfile.ZipFile(SOURCE) as archive:
        IMAGE.write_bytes(archive.read("ppt/media/image8.png"))


def make_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Расшифровка"
    ws.sheet_view.showGridLines = False

    title = "План-график работ по комплексному содержанию пути в 2026 г."
    ws.merge_cells("A1:J1")
    ws["A1"] = title
    ws["A1"].font = Font(name="Arial", size=14, bold=True, color="FFFFFF")
    ws["A1"].fill = PatternFill("solid", fgColor="005B8F")
    ws["A1"].alignment = Alignment(horizontal="center")

    headers = ["Регион", "ПЧ", "Название направления, перегона, станции", "Км, ПК от–до", "Путь", "Тип скрепления", "Объем работ, км", "Объем работ, тыс. м3", "Начало", "Окончание"]
    for col, value in enumerate(headers, 1):
        cell = ws.cell(3, col, value)
        cell.font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    rows = [
        [3, 14, "ТАЙГА, МР", "премо-отпр.", 45, "КБ", 0.20, 0.934, "06–13", ""],
        [3, 15, "ТАЙГА, МР", "премо-отпр.", 46, "КБ", 0.20, 0.927, "01–08", ""],
        [3, 16, "ТАЙГА, МР", "премо-отпр.", 47, "КБ", 0.20, 0.953, "02–09", ""],
        [3, 17, "БЕРИКУЛЬСКАЯ", "премо-отпр.", 4, "КБ", 0.20, 0.674, "26–02", ""],
        [3, 18, "АНИССЕВСКАЯ", "премо-отпр.", 4, "КБ", 0.20, 0.964, "17–23", ""],
        [3, 19, "МЕРЕТЬ", "премо-отпр.", 6, "КБ", 0.20, 1.029, "23–30", ""],
        [2, 20, "МЕРЕТЬ", "премо-отпр.", 8, "КБ", 0.20, 1.002, "24–30", ""],
        [2, 21, "МЕЖДУРЕЧЕНСК А.", "премо-отпр.", 8, "КБ", 0.20, 0.895, "13–19", ""],
        [2, 22, "ПРЕДКОМБИНАТ", "премо-отпр.", 7, "КБ-65Ш", 0.20, 0.605, "28–04", ""],
        [2, 23, "БИРЮЛИНСКАЯ", "премо-отпр.", 5, "КБ", 0.20, 0.826, "06–12", ""],
        [1, 24, "КОМБИНАТСКАЯ, ГАЗ", "пройной", 6, "КБ", 0.20, 0.744, "24–01", ""],
        [1, 25, "КОМБИНАТСКАЯ, ГАЗ", "пройной", 7, "КБ", 0.20, 0.627, "26–03", ""],
        [1, 26, "КАРАСУК", "деповский", 106, "КБ", 0.18, "", "14–19", ""],
        [1, 27, "КАРАСУК", "ходовой", "106а", "КБ", 0.42, "", "14–19", ""],
    ]
    for row in rows:
        ws.append(row)
    for row in ws.iter_rows(min_row=4, max_row=17):
        for cell in row:
            cell.font = Font(name="Arial", size=10)
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            cell.border = Border(bottom=Side(style="thin", color="B7C9D6"))

    total_row = 18
    ws.cell(total_row, 1, "ИТОГО КРС")
    ws.cell(total_row, 3, "Укладка рельс")
    ws.cell(total_row, 7, 5.556)
    ws.cell(total_row, 8, 10.686)
    ws.cell(total_row, 9, 9.533)
    ws.cell(total_row, 10, 5.337)
    for cell in ws[total_row]:
        cell.font = Font(name="Arial", size=10, bold=True)
        cell.fill = PatternFill("solid", fgColor="FFF2A6")
        cell.border = Border(top=Side(style="medium", color="7F6000"), bottom=Side(style="thin", color="7F6000"))

    widths = [10, 8, 28, 16, 8, 14, 14, 18, 12, 12]
    for i, width in enumerate(widths, 1):
        ws.column_dimensions[chr(64 + i)].width = width
    ws.freeze_panes = "A4"
    ws.auto_filter.ref = "A3:J17"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0

    source = wb.create_sheet("Исходный скрин")
    source.sheet_view.showGridLines = False
    source["A1"] = "Исходное изображение слайда 6"
    source["A1"].font = Font(name="Arial", size=14, bold=True)
    source.add_image(XLImage(str(IMAGE)), "A3")

    wb.save(EXCEL)


def add_text(slide, text, x, y, w, h, size=12, bold=False, color="1F2937", align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = "Arial"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor.from_string(color)
    return box


def add_card(slide, x, y, w, h, label, value, accent="005B8F"):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(245, 248, 251)
    shape.line.color.rgb = RGBColor(215, 225, 233)
    add_text(slide, label, x + 0.12, y + 0.08, w - 0.24, 0.25, 9, False, "607286")
    add_text(slide, value, x + 0.12, y + 0.30, w - 0.24, 0.4, 20, True, accent)


def make_slide_variant():
    prs = Presentation(str(SOURCE))
    base = prs.slides[5]
    new_slide = prs.slides.add_slide(base.slide_layout)
    for shape in base.shapes:
        if shape.shape_type == 13:
            continue
        new_slide.shapes._spTree.insert_element_before(deepcopy(shape.element), "p:extLst")

    # Cover the inherited screenshot and build a readable summary in its place.
    panel = new_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(1.95), Inches(12.65), Inches(5.10))
    panel.fill.solid()
    panel.fill.fore_color.rgb = RGBColor(255, 255, 255)
    panel.line.color.rgb = RGBColor(220, 228, 235)

    add_text(new_slide, "Вариант оформления: план-график работ на 2026 год", 0.75, 2.10, 11.3, 0.42, 19, True, "005B8F")
    add_text(new_slide, "Крупные показатели вынесены отдельно, перечень объектов оставлен в компактной таблице", 0.75, 2.53, 11.3, 0.30, 10, False, "607286")

    add_card(new_slide, 0.75, 2.95, 2.35, 0.95, "Объем по графику, км", "5,556")
    add_card(new_slide, 3.30, 2.95, 2.35, 0.95, "Объем работ, тыс. м³", "10,686")
    add_card(new_slide, 5.85, 2.95, 2.35, 0.95, "Период планирования", "2026")
    add_card(new_slide, 8.40, 2.95, 3.60, 0.95, "Типовой вид работ", "комплексное содержание", accent="C00000")

    headers = ["Регион / ПЧ", "Объект", "Путь", "Скрепление", "Объем, км", "Период"]
    data = [
        ["3 / 14", "Тайга, МР", "45", "КБ", "0,20", "06–13"],
        ["3 / 15", "Тайга, МР", "46", "КБ", "0,20", "01–08"],
        ["3 / 16", "Тайга, МР", "47", "КБ", "0,20", "02–09"],
        ["3 / 17", "Берикульская", "4", "КБ", "0,20", "26–02"],
        ["3 / 18", "Аниссевская", "4", "КБ", "0,20", "17–23"],
        ["3 / 19", "Мереть", "6", "КБ", "0,20", "23–30"],
    ]
    x0, y0 = 0.75, 4.16
    widths = [1.25, 3.05, 0.75, 1.25, 1.35, 1.30]
    row_h = 0.38
    for r, row in enumerate([headers] + data):
        x = x0
        for c, value in enumerate(row):
            cell = new_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y0 + r * row_h), Inches(widths[c]), Inches(row_h))
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(31, 78, 121) if r == 0 else (RGBColor(242, 246, 249) if r % 2 else RGBColor(255, 255, 255))
            cell.line.color.rgb = RGBColor(210, 220, 228)
            add_text(new_slide, str(value), x + 0.04, y0 + r * row_h + 0.01, widths[c] - 0.08, row_h - 0.02, 9 if r else 8, r == 0, "FFFFFF" if r == 0 else "263746", PP_ALIGN.CENTER if c != 1 else PP_ALIGN.LEFT)
            x += widths[c]

    add_text(new_slide, "Полная расшифровка таблицы и исходный скрин сохранены в отдельном Excel-файле.", 0.75, 6.72, 11.4, 0.24, 8, False, "607286")
    slide_ids = prs.slides._sldIdLst
    new_id = slide_ids[-1]
    slide_ids.remove(new_id)
    slide_ids.insert(6, new_id)
    prs.save(PRESENTATION)


if __name__ == "__main__":
    extract_image()
    make_excel()
    make_slide_variant()
    print(EXCEL)
    print(PRESENTATION)
