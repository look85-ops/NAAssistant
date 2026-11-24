from pathlib import Path
import shutil

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


SOURCE = Path(r"C:\Users\marcenuk\Desktop\АП_Модуль 3\Проекты\1_Машинизация.pptx")
OUT_DIR = SOURCE.parent / "_пример_оформления"
OUTPUT = OUT_DIR / "1_Машинизация_пример_дизайна_по_шаблону.pptx"

NAVY = RGBColor(0, 49, 98)
INK = RGBColor(24, 24, 27)
MUTED = RGBColor(104, 108, 119)
PAPER = RGBColor(229, 234, 239)
WHITE = RGBColor(255, 255, 255)
ORANGE = RGBColor(0, 49, 98)
BLUE = RGBColor(0, 49, 98)
PALE_ORANGE = RGBColor(229, 234, 239)
PALE_BLUE = RGBColor(229, 234, 239)


def add_text(slide, text, x, y, w, h, size=20, color=INK, bold=False,
             font="Mont", align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.02)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def rect(slide, x, y, w, h, fill, radius=False, line=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line or fill
    return shape


def base(prs, title, section, number):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide, 0, 0, 13.333, 7.5, PAPER)
    rect(slide, 0, 0, 0.18, 7.5, ORANGE)
    add_text(slide, section.upper(), 0.7, 0.38, 4.8, 0.25, 9, ORANGE, True)
    add_text(slide, title, 0.7, 0.76, 11.3, 0.7, 27, NAVY, True)
    add_text(slide, f"АКАДЕМИЯ ПУТИ  •  {number:02d}", 10.6, 7.05, 2.0, 0.18, 8, MUTED, True, align=PP_ALIGN.RIGHT)
    return slide


def bullet(slide, text, x, y, w, accent=ORANGE, size=17):
    rect(slide, x, y + 0.1, 0.12, 0.12, accent, True)
    add_text(slide, text, x + 0.28, y, w - 0.28, 0.52, size, INK)


def metric(slide, value, label, x, y, w, fill=WHITE, value_color=NAVY):
    rect(slide, x, y, w, 1.35, fill, True)
    add_text(slide, value, x + 0.18, y + 0.18, w - 0.36, 0.48, 26, value_color, True)
    add_text(slide, label, x + 0.18, y + 0.78, w - 0.36, 0.38, 11, MUTED)


def main():
    OUT_DIR.mkdir(exist_ok=True)
    shutil.copy2(SOURCE, OUT_DIR / "1_Машинизация_исходник.pptx")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide, 0, 0, 13.333, 7.5, NAVY)
    rect(slide, 0, 0, 0.25, 7.5, ORANGE)
    add_text(slide, "АКАДЕМИЯ ПУТИ  •  ЧЕРНОВОЙ ДИЗАЙН-ПРИМЕР", 0.8, 0.62, 7.0, 0.3, 10, ORANGE, True)
    add_text(slide, "Машинизация\nтекущего содержания", 0.8, 1.5, 8.2, 1.8, 38, WHITE, True)
    add_text(slide, "Как перейти от ручного труда к управляемой технологии\nи получить эффект для участка", 0.85, 4.25, 6.8, 0.8, 19, RGBColor(213, 222, 231))
    rect(slide, 9.15, 1.25, 3.25, 4.45, PALE_ORANGE, True)
    add_text(slide, "28,1\nмлн ₽", 9.5, 2.0, 2.55, 1.2, 34, NAVY, True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    add_text(slide, "экономический эффект\nна 1 км", 9.5, 3.55, 2.55, 0.65, 15, INK, True, align=PP_ALIGN.CENTER)
    add_text(slide, "1", 12.1, 6.85, 0.4, 0.25, 10, RGBColor(213, 222, 231), True, align=PP_ALIGN.RIGHT)

    slide = base(prs, "Зачем менять подход", "Контекст", 2)
    add_text(slide, "Сегодня результат зависит от ручного труда, доступности людей и разрозненной техники.", 0.72, 1.7, 11.6, 0.6, 22, NAVY, True)
    bullet(slide, "Увеличить производительность и сократить время выполнения работ", 1.0, 2.75, 5.4)
    bullet(slide, "Снизить зависимость от дефицита квалифицированного персонала", 1.0, 3.55, 5.4)
    bullet(slide, "Перевести обслуживание на понятный и измеримый процесс", 1.0, 4.35, 5.4)
    rect(slide, 7.35, 2.35, 4.45, 3.15, NAVY, True)
    add_text(slide, "Главный вопрос", 7.75, 2.8, 3.5, 0.3, 11, ORANGE, True)
    add_text(slide, "Как сделать больше\nтем же ресурсом?", 7.75, 3.35, 3.4, 1.2, 27, WHITE, True)

    slide = base(prs, "Точка старта в цифрах", "Проблема", 3)
    add_text(slide, "Исходные показатели из рабочей презентации команды", 0.72, 1.52, 7.5, 0.35, 15, MUTED)
    metric(slide, "537 км", "объём работ", 0.75, 2.15, 2.75, PALE_BLUE, BLUE)
    metric(slide, "93%", "доля механизированных работ", 3.75, 2.15, 2.75, PALE_ORANGE, ORANGE)
    metric(slide, "40%", "экономия времени", 6.75, 2.15, 2.75, PALE_BLUE, BLUE)
    metric(slide, "798 ед.", "парк / объём техники", 9.75, 2.15, 2.75, PALE_ORANGE, ORANGE)
    add_text(slide, "Проблема не в отсутствии отдельных решений, а в том, что они пока не собраны в единый технологический контур.", 0.8, 4.55, 11.4, 0.8, 24, NAVY, True)

    slide = base(prs, "Решение: собрать технологический контур", "Подход", 4)
    add_text(slide, "Три элемента должны работать как одна система", 0.72, 1.5, 8.0, 0.4, 17, MUTED)
    for x, title, text, fill, accent in [
        (0.8, "Техника", "подбор машин\nпод задачу", PALE_ORANGE, ORANGE),
        (4.55, "Технология", "единый порядок\nвыполнения работ", PALE_BLUE, BLUE),
        (8.3, "Контроль", "измеримый результат\nи обратная связь", RGBColor(232, 235, 229), RGBColor(77, 117, 72)),
    ]:
        rect(slide, x, 2.35, 3.2, 2.5, fill, True)
        rect(slide, x + 0.3, 2.72, 0.62, 0.1, accent)
        add_text(slide, title, x + 0.3, 3.1, 2.55, 0.45, 22, NAVY, True)
        add_text(slide, text, x + 0.3, 3.75, 2.55, 0.72, 17, INK)
    add_text(slide, "Не просто купить машину, а изменить способ работы.", 1.2, 5.8, 10.5, 0.5, 22, ORANGE, True, align=PP_ALIGN.CENTER)

    slide = base(prs, "Комплект техники под задачу", "Решение", 5)
    add_text(slide, "В исходнике перечислены четыре группы оборудования. В финале стоит оставить по одной сильной мысли на каждую.", 0.72, 1.5, 11.4, 0.55, 16, MUTED)
    items = [("01", "Машина для выправки", "точность и скорость работ"), ("02", "Комплекс для очистки", "единый цикл обслуживания"), ("03", "Машина для балласта", "снижение ручных операций"), ("04", "Дополнительная техника", "закрытие вспомогательных задач")]
    for i, (num, title, text) in enumerate(items):
        x = 0.8 + (i % 2) * 6.0
        y = 2.35 + (i // 2) * 1.65
        add_text(slide, num, x, y, 0.6, 0.42, 18, ORANGE, True)
        add_text(slide, title, x + 0.8, y - 0.02, 4.6, 0.38, 19, NAVY, True)
        add_text(slide, text, x + 0.8, y + 0.48, 4.6, 0.32, 14, MUTED)
        rect(slide, x + 0.8, y + 1.05, 4.6, 0.02, RGBColor(214, 220, 226))

    slide = base(prs, "Экономика одного километра", "Эффект", 6)
    add_text(slide, "Сравниваем затраты не только на покупку, но и на весь цикл работы", 0.72, 1.5, 10.8, 0.4, 17, MUTED)
    metric(slide, "3 206 162 ₽", "затраты на 1 км по расчёту команды", 0.85, 2.25, 5.55, PALE_ORANGE, ORANGE)
    metric(slide, "28,1 млн ₽", "экономический эффект на 1 км", 6.95, 2.25, 5.55, NAVY, WHITE)
    add_text(slide, "В финальной версии важно показать формулу расчёта и период окупаемости отдельным слайдом или в приложении.", 1.15, 4.65, 11.0, 0.7, 20, NAVY, True, align=PP_ALIGN.CENTER)

    slide = base(prs, "Что меняется после внедрения", "Результат", 7)
    for y, title, text, accent in [(2.0, "Быстрее", "меньше времени на единицу работы", ORANGE), (3.25, "Стабильнее", "меньше зависимости от ручного труда", BLUE), (4.5, "Прозрачнее", "результат можно измерять и сравнивать", RGBColor(77, 117, 72))]:
        rect(slide, 0.9, y, 0.28, 0.62, accent, True)
        add_text(slide, title, 1.55, y - 0.02, 2.5, 0.35, 22, NAVY, True)
        add_text(slide, text, 4.2, y + 0.02, 7.2, 0.32, 17, INK)
    add_text(slide, "Ценность проекта — в переходе от отдельных машин к новой норме работы.", 0.9, 6.05, 11.3, 0.5, 22, ORANGE, True, align=PP_ALIGN.CENTER)

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide, 0, 0, 13.333, 7.5, NAVY)
    rect(slide, 0, 0, 0.25, 7.5, ORANGE)
    add_text(slide, "ФИНАЛЬНЫЙ ТЕЗИС", 0.85, 0.8, 4.0, 0.3, 10, ORANGE, True)
    add_text(slide, "Машинизация — это не про отдельную технику.\nЭто про управляемый результат.", 0.85, 2.0, 10.8, 1.5, 34, WHITE, True)
    add_text(slide, "Черновой дизайн-пример. Содержание, цифры и формулировки требуют финальной сверки командой.", 0.88, 5.65, 10.5, 0.5, 13, RGBColor(213, 222, 231))
    add_text(slide, "8", 12.1, 6.85, 0.4, 0.25, 10, RGBColor(213, 222, 231), True, align=PP_ALIGN.RIGHT)

    prs.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
