import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
header_font_white = Font(bold=True, size=11, color='FFFFFF')
title_font = Font(bold=True, size=14)
subtitle_font = Font(bold=True, size=12)
money_font_green = Font(bold=True, color='008000')
warn_font = Font(italic=True, color='999999')
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

def style_header(ws, row, cols):
    for col in range(1, cols+1):
        cell = ws.cell(row=row, column=col)
        cell.font = header_font_white
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', wrap_text=True)
        cell.border = thin_border

def style_data(ws, start_row, end_row, cols):
    for r in range(start_row, end_row+1):
        for c in range(1, cols+1):
            cell = ws.cell(row=r, column=c)
            cell.border = thin_border
            cell.alignment = Alignment(wrap_text=True, vertical='top')

def auto_width(ws, cols, min_w=8, max_w=45):
    for col in range(1, cols+1):
        max_len = min_w
        for row in ws.iter_rows(min_col=col, max_col=col, values_only=False):
            for cell in row:
                if cell.value:
                    lines = str(cell.value).split('\n')
                    for line in lines:
                        max_len = max(max_len, min(len(line) + 2, max_w))
        ws.column_dimensions[get_column_letter(col)].width = max_len


# ============ Лист 1: Все избранное ============
ws1 = wb.active
ws1.title = 'Все избранное'

ws1.cell(row=1, column=1, value='Избранное Lamoda — полный обзор').font = title_font
ws1.cell(row=2, column=1, value='20 позиций | ~285 000 ₽ | 06.10.2026').font = Font(size=10, color='666666')
ws1.merge_cells('A1:H1')
ws1.merge_cells('A2:H2')

headers1 = ['№', 'Бренд', 'Название', 'Цена, ₽', 'Цвет', 'Категория', 'Рейтинг', 'Ссылка']
for i, h in enumerate(headers1, 1):
    ws1.cell(row=4, column=i, value=h)
style_header(ws1, 4, len(headers1))

data1 = [
    [1, 'Marc O\'Polo', 'Брюки баррел (вельвет)', 14952, 'Чёрный', 'Брюки Plus Size', '4.8 (14)', ''],
    [2, 'Снежная Королева', 'Бомбер', 14571, 'Хаки', 'Верхняя одежда', '—', ''],
    [3, 'Marc O\'Polo', 'Жилет меховой', 15800, 'Бордовый', 'Жилет', '—', ''],
    [4, 'Marc O\'Polo', 'Джинсы', 18041, 'Синий', 'Джинсы', '—', ''],
    [5, 'iBlues', 'Кардиган IBLTENEBRE', 20060, '—', 'Кардиган (premium)', '—', ''],
    [6, 'Fred Perry', 'Свитшот', 13592, 'Синий', 'Свитшот', '—', ''],
    [7, '2Mood', 'Рубашка', 8991, '—', 'Рубашка', '4.4 (11)', ''],
    [8, 'Nume', 'Рубашка', 4943, '—', 'Рубашка', '—', ''],
    [9, 'U.S. Polo Assn.', 'Свитшот Lamoda Exclusive', 7120, '—', 'Свитшот', '—', ''],
    [10, '12 STOREEZ', 'Лонгслив Flint', 7800, '—', 'Лонгслив (premium)', '—', ''],
    [11, 'Luisa Wang', 'Кардиган Lamoda Online Exclusive', 10221, '—', 'Кардиган', '—', ''],
    [12, 'Pennyblack', 'Свитер PBBALGA', 20485, '—', 'Свитер (premium)', '—', ''],
    [13, 'Annemore', 'Поло', 10540, '—', 'Поло', '—', ''],
    [14, 'Lusio', 'Джемпер Lamoda Online Exclusive', 14990, '—', 'Джемпер', '—', ''],
    [15, 'Lusio', 'Поло Lamoda Online Exclusive', 15990, '—', 'Поло', '—', ''],
    [16, 'G.E.Y.I.M', 'Брюки вельветовые', 7440, 'Чёрный', 'Брюки', '4.9 (42)', ''],
    [17, 'Levi\'s', 'Свитшот', 8495, '—', 'Свитшот', '4.8 (15)', ''],
    [18, 'Pennyblack', 'Джемпер PBBBOSCO', 16915, '—', 'Джемпер (premium)', '—', ''],
    [19, 'Emka', 'Полупальто Lamoda Exclusive', 39990, 'Чёрный', 'Верхняя одежда', '—', ''],
    [20, 'Maison David', 'Пальто двубортное', 19346, 'Бежевый', 'Верхняя одежда', '—', ''],
]

for i, row_data in enumerate(data1):
    for j, val in enumerate(row_data):
        ws1.cell(row=5+i, column=j+1, value=val)

# Mark empty links
link_col = len(headers1)
for i in range(len(data1)):
    cell = ws1.cell(row=5+i, column=link_col)
    if not cell.value:
        cell.value = 'уточнить на Lamoda'
        cell.font = warn_font

style_data(ws1, 5, 4+len(data1), len(headers1))
auto_width(ws1, len(headers1))

# ============ Лист 2: Основной вариант ============
ws2 = wb.create_sheet('Основной вариант')

ws2.cell(row=1, column=1, value='Основной вариант: осенняя капсула').font = title_font
ws2.cell(row=2, column=1, value='Сумма: 82 574 ₽ | Остаток: 17 426 ₽').font = Font(bold=True, size=11, color='008000')
ws2.merge_cells('A1:G1')
ws2.merge_cells('A2:G2')

headers2 = ['№', 'Бренд', 'Название', 'Цена, ₽', 'Цвет', 'Назначение', 'Ссылка']
for i, h in enumerate(headers2, 1):
    ws2.cell(row=4, column=i, value=h)
style_header(ws2, 4, len(headers2))

data2 = [
    [1, 'Maison David', 'Пальто двубортное', 19346, 'Бежевый', 'Верхняя одежда — must have на осень', ''],
    [2, 'Marc O\'Polo', 'Джинсы', 18041, 'Синий', 'База, качественный деним', ''],
    [3, 'G.E.Y.I.M', 'Брюки вельветовые', 7440, 'Чёрный', 'Второй низ, рейтинг 4.9, плотная ткань', ''],
    [4, 'Fred Perry', 'Свитшот', 13592, 'Синий', 'Спорт-шик, знаковый бренд', ''],
    [5, 'Luisa Wang', 'Кардиган', 10221, '—', 'Женственность без облегания', ''],
    [6, '2Mood', 'Рубашка', 8991, '—', 'Универсальный верх', ''],
    [7, 'Nume', 'Рубашка', 4943, '—', 'База, свежая коллекция', ''],
]

for i, row_data in enumerate(data2):
    for j, val in enumerate(row_data):
        ws2.cell(row=5+i, column=j+1, value=val)

link_col2 = len(headers2)
for i in range(len(data2)):
    ws2.cell(row=5+i, column=link_col2, value='уточнить на Lamoda').font = warn_font

row_total = 5 + len(data2)
ws2.cell(row=row_total, column=2, value='ИТОГО').font = Font(bold=True)
ws2.cell(row=row_total, column=3, value='7 вещей').font = Font(bold=True)
ws2.cell(row=row_total, column=4, value=82574).font = money_font_green
for c in range(1, len(headers2)+1):
    ws2.cell(row=row_total, column=c).border = thin_border

style_data(ws2, 5, row_total-1, len(headers2))
auto_width(ws2, len(headers2))

# Бонус-строка
rb = row_total + 2
ws2.cell(row=rb, column=1, value='Бонус').font = subtitle_font
ws2.cell(row=rb+1, column=2, value='12 STOREEZ')
ws2.cell(row=rb+1, column=3, value='Лонгслив Flint')
ws2.cell(row=rb+1, column=4, value=7800)
ws2.cell(row=rb+1, column=6, value='Итого с бонусом: 90 374 ₽')
ws2.cell(row=rb+1, column=7, value='уточнить на Lamoda').font = warn_font
for c in range(1, len(headers2)+1):
    ws2.cell(row=rb+1, column=c).border = thin_border

# ============ Лист 3: Альтернативный вариант ============
ws3 = wb.create_sheet('Альтернативный вариант')

ws3.cell(row=1, column=1, value='Альтернативный вариант: спорт-шик с акцентом').font = title_font
ws3.cell(row=2, column=1, value='Сумма: 86 140 ₽ | Остаток: 13 860 ₽').font = Font(bold=True, size=11, color='008000')
ws3.merge_cells('A1:G1')
ws3.merge_cells('A2:G2')

for i, h in enumerate(headers2, 1):
    ws3.cell(row=4, column=i, value=h)
style_header(ws3, 4, len(headers2))

data3 = [
    [1, 'Снежная Королева', 'Бомбер', 14571, 'Хаки', 'Верхняя одежда sport-chic, скидка 41%', ''],
    [2, 'Marc O\'Polo', 'Джинсы', 18041, 'Синий', 'База', ''],
    [3, 'G.E.Y.I.M', 'Брюки вельветовые', 7440, 'Чёрный', 'Второй низ', ''],
    [4, 'Lusio', 'Джемпер', 14990, '—', 'Тёплый джемпер, Lamoda Exclusive', ''],
    [5, 'Levi\'s', 'Свитшот', 8495, '—', 'Спорт-шик, рейтинг 4.8', ''],
    [6, 'Annemore', 'Поло', 10540, '—', 'Спорт-шик, скидка 47%', ''],
    [7, 'U.S. Polo Assn.', 'Свитшот Lamoda Exclusive', 7120, '—', 'Ещё спорт-шик, выгодная цена', ''],
    [8, 'Nume', 'Рубашка', 4943, '—', 'База', ''],
]

for i, row_data in enumerate(data3):
    for j, val in enumerate(row_data):
        ws3.cell(row=5+i, column=j+1, value=val)

for i in range(len(data3)):
    ws3.cell(row=5+i, column=link_col2, value='уточнить на Lamoda').font = warn_font

row_total3 = 5 + len(data3)
ws3.cell(row=row_total3, column=2, value='ИТОГО').font = Font(bold=True)
ws3.cell(row=row_total3, column=3, value='8 вещей').font = Font(bold=True)
ws3.cell(row=row_total3, column=4, value=86140).font = money_font_green
for c in range(1, len(headers2)+1):
    ws3.cell(row=row_total3, column=c).border = thin_border

style_data(ws3, 5, row_total3-1, len(headers2))
auto_width(ws3, len(headers2))

# ============ Лист 4: На потом ============
ws4 = wb.create_sheet('На потом')

ws4.cell(row=1, column=1, value='Что остаётся в избранном').font = title_font
ws4.merge_cells('A1:E1')

headers4 = ['Бренд', 'Название', 'Цена, ₽', 'Почему не вошло', 'Ссылка']
for i, h in enumerate(headers4, 1):
    ws4.cell(row=3, column=i, value=h)
style_header(ws4, 3, len(headers4))

data4 = [
    ['Marc O\'Polo', 'Брюки баррел (вельвет)', 14952, 'Дороже G.E.Y.I.M (7 440 ₽). Альтернатива на будущее', ''],
    ['Marc O\'Polo', 'Жилет меховой', 15800, 'Нишевая вещь, не база. Можно вернуться позже', ''],
    ['iBlues', 'Кардиган IBLTENEBRE', 20060, 'Дорого. Luisa Wang (10 221 ₽) — бюджетная альтернатива', ''],
    ['12 STOREEZ', 'Лонгслив Flint', 7800, 'Можно добавить в основной вариант при желании', ''],
    ['Pennyblack', 'Свитер PBBALGA', 20485, 'Premium-цена не оправдана при бюджете 100 т.р.', ''],
    ['Pennyblack', 'Джемпер PBBBOSCO', 16915, 'Premium-сегмент, не приоритет', ''],
    ['Lusio', 'Поло', 15990, 'Дороже аналогичного Annemore (10 540 ₽)', ''],
    ['Emka', 'Полупальто', 39990, '40% бюджета на одну вещь — неоптимально', ''],
]

for i, row_data in enumerate(data4):
    for j, val in enumerate(row_data):
        ws4.cell(row=4+i, column=j+1, value=val)

for i in range(len(data4)):
    ws4.cell(row=4+i, column=len(headers4), value='уточнить на Lamoda').font = warn_font

style_data(ws4, 4, 4+len(data4)-1, len(headers4))
auto_width(ws4, len(headers4), max_w=55)

# ============ Сохраняем ============
output_path = os.path.join('wardrobe', '2026-10-06_optimal-shopping.xlsx')
wb.save(output_path)
print('OK: ' + output_path + ' size=' + str(os.path.getsize(output_path)))