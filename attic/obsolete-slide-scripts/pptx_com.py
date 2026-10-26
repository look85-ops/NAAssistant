# -*- coding: utf-8 -*-
"""
pptx_com.py — операции над презентацией через PowerPoint COM.

Плюсы: PowerPoint сам корректно клонирует всё — layout, темы, rels, темы,
шрифты. Никакие XML-манипуляции не нужны.

Минусы: требуется установленный PowerPoint и разрешение COM.

Основные функции:
- open_pptx(path)  → (app, presentation)
- close_pptx(app, pres, save=True)
- duplicate_slide(pres, src_idx_1based) → new_idx (новый слайд появляется
  на позиции src+1, возвращаем его 1-based номер)
- move_slide(pres, from_idx, to_idx)
- hide_slide(pres, idx)
- unhide_slide(pres, idx)
- set_shape_text_by_hint(slide, first_line_hint, new_lines)
- replace_text_in_slide(slide, dict)  # старая подстрока → новая
- add_tag(slide, text)                # красная метка "Новый"/"Изменено"
- remove_tag(slide)
- get_slide_size(pres) → (width_pt, height_pt) в пунктах (PPT hardcoded pt)
- add_table_slide(pres, after_idx, title, header, rows, tag="Новый")
  — комплексная сборка контентного слайда с заголовком и таблицей
    через клонирование указанного шаблона.
"""
import time
import win32com.client as win32
import win32com.client.dynamic as dynamic
import pythoncom

# msoTriState
msoTrue = -1
msoFalse = 0

# constants
ppLayoutBlank = 12

TAG_NAME = "SVC_TAG"


def open_pptx(path):
    pythoncom.CoInitialize()
    try:
        app = win32.gencache.EnsureDispatch("PowerPoint.Application")
    except Exception:
        app = win32.Dispatch("PowerPoint.Application")
    try:
        pres = app.Presentations.Open(path, ReadOnly=False, WithWindow=False)
    except Exception:
        app.Visible = True
        pres = app.Presentations.Open(path, ReadOnly=False)
    return app, pres


def close_pptx(app, pres, save=True):
    if save:
        pres.Save()
    pres.Close()
    app.Quit()


def duplicate_slide(pres, src_idx_1based):
    """
    Дублирует слайд, возвращает 1-based индекс нового слайда.
    PowerPoint кладёт дубликат сразу после исходного.
    """
    src = pres.Slides.Item(src_idx_1based)
    src.Duplicate()  # возвращает SlideRange, но новый — src_idx+1
    return src_idx_1based + 1


def move_slide(pres, from_idx, to_idx):
    """
    Перемещает слайд. to_idx — целевая позиция после перемещения (1-based).
    """
    if from_idx == to_idx:
        return
    pres.Slides.Item(from_idx).MoveTo(to_idx)


def hide_slide(pres, idx):
    pres.Slides.Item(idx).SlideShowTransition.Hidden = msoTrue


def unhide_slide(pres, idx):
    pres.Slides.Item(idx).SlideShowTransition.Hidden = msoFalse


def iter_shapes(slide):
    for i in range(1, slide.Shapes.Count + 1):
        yield slide.Shapes.Item(i)


def find_shape_by_first_line(slide, substring):
    for shp in iter_shapes(slide):
        if not shp.HasTextFrame:
            continue
        if shp.TextFrame.HasText != msoTrue:
            continue
        text = shp.TextFrame.TextRange.Text or ""
        first = next((line for line in text.splitlines() if line.strip()), "")
        if substring in first:
            return shp
    return None


def set_shape_text_by_hint(slide, first_line_hint, new_text):
    """
    Находит фигуру по первой строке, заменяет весь её текст.
    Форматирование первого символа сохраняется, потому что PowerPoint
    при замене TextRange.Text применяет свойства нулевого run.
    """
    shp = find_shape_by_first_line(slide, first_line_hint)
    if shp is None:
        return False
    tf = shp.TextFrame.TextRange
    # Заменяем "родным" способом
    tf.Text = new_text
    return True


def replace_text_in_slide(slide, replacements):
    """dict: старая подстрока → новая. Применяется ко всем фигурам."""
    for shp in iter_shapes(slide):
        if not shp.HasTextFrame:
            continue
        if shp.TextFrame.HasText != msoTrue:
            continue
        text = shp.TextFrame.TextRange.Text or ""
        new_text = text
        for old, new in replacements.items():
            if old in new_text:
                new_text = new_text.replace(old, new)
        if new_text != text:
            shp.TextFrame.TextRange.Text = new_text


def add_tag(slide, text="Новый", rgb=(200, 40, 40)):
    """
    Добавляет метку в правом верхнем углу. Размер в пунктах.
    slide.master.Width / slide.master.Height недоступны в этом COM API,
    поэтому берём из презентации.
    """
    pres = slide.Parent  # Presentation
    slide_w_pt = pres.PageSetup.SlideWidth
    # slide_h_pt = pres.PageSetup.SlideHeight
    w_pt = 200
    h_pt = 50
    left = slide_w_pt - w_pt - 30
    top = 20
    # msoTextOrientationHorizontal = 1
    tb = slide.Shapes.AddTextbox(1, left, top, w_pt, h_pt)
    tb.Name = TAG_NAME + "_" + text
    tr = tb.TextFrame.TextRange
    tr.Text = text
    tr.Font.Size = 28
    tr.Font.Bold = msoTrue
    tr.Font.Italic = msoTrue
    tr.Font.Color.RGB = rgb[0] | (rgb[1] << 8) | (rgb[2] << 16)
    tr.ParagraphFormat.Alignment = 3  # ppAlignRight
    return tb


def remove_tag(slide):
    to_del = []
    for shp in iter_shapes(slide):
        try:
            if shp.Name and shp.Name.startswith(TAG_NAME):
                to_del.append(shp)
        except Exception:
            continue
    for shp in to_del:
        shp.Delete()


def find_slide_by_text(pres, substring):
    for i in range(1, pres.Slides.Count + 1):
        s = pres.Slides.Item(i)
        for shp in iter_shapes(s):
            if not shp.HasTextFrame:
                continue
            if shp.TextFrame.HasText != msoTrue:
                continue
            text = shp.TextFrame.TextRange.Text or ""
            if substring in text:
                return i
    return None


def add_textbox(slide, left_pt, top_pt, w_pt, h_pt, text, size=24, bold=False,
                rgb=(0, 0, 0), align=1):
    """align: 1=left, 2=center, 3=right"""
    tb = slide.Shapes.AddTextbox(1, left_pt, top_pt, w_pt, h_pt)
    tr = tb.TextFrame.TextRange
    tr.Text = text
    tr.Font.Size = size
    tr.Font.Bold = msoTrue if bold else msoFalse
    tr.Font.Color.RGB = rgb[0] | (rgb[1] << 8) | (rgb[2] << 16)
    tr.ParagraphFormat.Alignment = align
    tb.TextFrame.WordWrap = msoTrue
    return tb


def add_table(slide, left_pt, top_pt, w_pt, h_pt, data,
              header_rgb=(30, 30, 90), header_fg=(255, 255, 255),
              first_col_rgb=(230, 230, 245)):
    """
    Настоящая PowerPoint-таблица.
    data: list of rows; шапка = data[0].
    """
    rows = len(data)
    cols = len(data[0])
    table_shape = slide.Shapes.AddTable(rows, cols, left_pt, top_pt, w_pt, h_pt)
    table = table_shape.Table
    # Ширины столбцов: первый 35%, остальные — поровну.
    if cols == 2:
        table.Columns.Item(1).Width = w_pt * 0.35
        table.Columns.Item(2).Width = w_pt * 0.65
    for ri, row in enumerate(data, start=1):
        for ci, text in enumerate(row, start=1):
            cell = table.Cell(ri, ci)
            tf = cell.Shape.TextFrame.TextRange
            tf.Text = text
            if ri == 1:
                tf.Font.Bold = msoTrue
                tf.Font.Size = 22
                tf.Font.Color.RGB = header_fg[0] | (header_fg[1] << 8) | (header_fg[2] << 16)
                cell.Shape.Fill.ForeColor.RGB = header_rgb[0] | (header_rgb[1] << 8) | (header_rgb[2] << 16)
            else:
                tf.Font.Size = 16 if ci == 1 else 14
                tf.Font.Bold = msoTrue if ci == 1 else msoFalse
                if ci == 1:
                    cell.Shape.Fill.ForeColor.RGB = first_col_rgb[0] | (first_col_rgb[1] << 8) | (first_col_rgb[2] << 16)
    return table_shape
