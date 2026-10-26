import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

header_fill = PatternFill(start_color='5B4A3F', end_color='5B4A3F', fill_type='solid')
header_font_white = Font(bold=True, size=11, color='FFFFFF')
title_font = Font(bold=True, size=14)
subtitle_font = Font(bold=True, size=12)
accent_font = Font(bold=True, color='7A3B2E')
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


# Лист 1: Капсула (избранное)
ws1 = wb.active
ws1.title = 'Капсула из избранного'

ws1.cell(row=1, column=1, value='Капсула из избранного: тихий статус').font = title_font
ws1.merge_cells('A1:F1')

headers1 = ['№', 'Вещь', 'Бренд', 'Цвет', 'Состав', 'Цена, ₽']
for i, h in enumerate(headers1, 1):
    ws1.cell(row=3, column=i, value=h)
style_header(ws1, 3, len(headers1))

data1 = [
    [1, 'Лонгслив Flint', '12 STOREEZ', 'синий', 'хлопок 100%, контрастные нити', 7800],
    [2, 'Брюки NATURE CORDUROY', 'Jack Wolfskin', 'чёрный', 'вельвет, орг. хлопок 100%', 11988],
    [3, 'Кардиган', 'Luisa Wang', 'шоколад', 'шерсть 100%', 10221],
    [4, 'Футболка JENNI', 'Mango', 'мультиколор', 'полиэстер 59%, лиоцелл 25%', 2380],
    [5, 'Джемпер PBBBOSCO', 'Pennyblack', 'серый', 'шерсть 80%, полиамид 20%', 16915],
    [6, 'Свитшот (флис)', 'Levi\'s', 'серый', 'хлопок 80%, полиэстер 20%', 9027],
    [7, 'Рубашка', '2Mood', 'белый', 'хлопок 58%, полиамид 37%', 8991],
]
for i, row in enumerate(data1):
    for j, val in enumerate(row):
        ws1.cell(row=4+i, column=j+1, value=val)

total = sum(r[5] for r in data1)
tr = 4 + len(data1)
ws1.cell(row=tr, column=2, value='ИТОГО').font = Font(bold=True)
ws1.cell(row=tr, column=3, value='7 вещей').font = Font(bold=True)
ws1.cell(row=tr, column=6, value=total).font = Font(bold=True, color='008000')
for c in range(1, len(headers1)+1):
    ws1.cell(row=tr, column=c).border = thin_border

style_data(ws1, 4, tr-1, len(headers1))
auto_width(ws1, len(headers1))

# Лист 2: Луки
ws2 = wb.create_sheet('Луки')

ws2.cell(row=1, column=1, value='5 луков из капсулы').font = title_font
ws2.merge_cells('A1:C1')

headers2 = ['Лук', 'Состав', 'Настроение']
for i, h in enumerate(headers2, 1):
    ws2.cell(row=3, column=i, value=h)
style_header(ws2, 3, len(headers2))

data2 = [
    ['Куратор', 'рубашка 2Mood + вельвет Jack Wolfskin + кардиган Luisa Wang на плечах', 'статус без логотипов'],
    ['Серый на сером', 'джемпер Pennyblack + свитшот Levi\'s слоем + вельвет', 'тонально, дорого'],
    ['Студия выходного', 'свитшот Levi\'s + вельвет + синий лонгслив под него', 'расслабленно, кежуал'],
    ['Цветовая точка', 'футболка Mango + чёрный вельвет + кардиган', 'принт как акцент'],
    ['Тёплый низ', 'синий лонгслив + вельвет + шоколадный кардиган', 'шоколад + синий'],
]
for i, row in enumerate(data2):
    for j, val in enumerate(row):
        ws2.cell(row=4+i, column=j+1, value=val)

style_data(ws2, 4, 3+len(data2), len(headers2))
auto_width(ws2, len(headers2), max_w=55)

# Лист 3: Цветовой акцент
ws3 = wb.create_sheet('Цветовой акцент')

ws3.cell(row=1, column=1, value='Цветовой акцент: зелёный').font = title_font
ws3.merge_cells('A1:C1')

headers3 = ['Решение', 'Позиция', 'Как работает']
for i, h in enumerate(headers3, 1):
    ws3.cell(row=3, column=i, value=h)
style_header(ws3, 3, len(headers3))

data3 = [
    ['Лучший выбор', 'Arny Praht TIPSY 2.0, зелёная сумка — 7 482 ₽', 'Полужёсткая форма добавляет взрослую графичность; зелёный работает с шоколадом, чёрным, синим и серым'],
    ['Мягкий тест', 'Labbra, зелёный платок — 2 083 ₽', 'Шерсть 30% и вискоза 70%; можно носить на шее, под воротом или на ручке сумки'],
    ['Уже есть', 'Mango JENNI, серо-синяя полоска', 'Это новая нейтраль, а не активный цвет; поддерживает синий лонгслив'],
    ['Лук 1', 'Mango + чёрный вельвет + шоколадный кардиган', 'Цветной, но собранный'],
    ['Лук 2', 'Mango + серый джемпер Pennyblack', 'Футболка выглядывает воротом или нижним слоем'],
    ['Лук 3', 'Mango + белая рубашка 2Mood', 'Футболка под расстёгнутой рубашкой получает воздух'],
    ['Не брать пока', 'Зелёный джемпер', 'Ещё один верх будет слишком обычным; акцент лучше сделать аксессуаром'],
]
for i, row in enumerate(data3):
    for j, val in enumerate(row):
        ws3.cell(row=4+i, column=j+1, value=val)
        if j == 0 and row[0] == 'Не брать пока':
            ws3.cell(row=4+i, column=j+1).font = accent_font

style_data(ws3, 4, 3+len(data3), len(headers3))
auto_width(ws3, len(headers3), max_w=55)

output_path = os.path.join('wardrobe', '2026-10-12_арт-дирекшн-капсула-v2.xlsx')
wb.save(output_path)
print('OK: ' + output_path + ' size=' + str(os.path.getsize(output_path)))
