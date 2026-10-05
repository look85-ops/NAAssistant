import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Kvartiry_Minsk'

headers = [
    'Ссылка', 'Стоимость (BYN)', 'Комнат', 'Общая м²', 'Жилая м²',
    'Адрес', 'Этаж', 'Балкон/Лоджия', 'Метро', 'Источник', 'Баллы', 'Примечание'
]

header_font = Font(bold=True, size=11)
header_fill = PatternFill(start_color='D9EAD3', end_color='D9EAD3', fill_type='solid')
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

for col, name in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=name)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center', wrap_text=True)

data = [
    # === ТОП (проходят все критерии: не 1-й, не 4-5/5, балкон/лоджия) ===
    ['https://re.kufar.by/vi/1082940630', 445500, 3, 69, 43,
     'Белинского 9 ❌ СКАМ', '8/9', 'Балкон (2 шт!)', 'Парк Челюскинцев ~10мин', 'kufar.by', 'скам',
     '❌ СКАМ 05.10.2026! Не связываться.'],
    ['https://re.kufar.by/vi/1084392138', 423177, 3, 68.2, 41.2,
     'Мележа 4', '3/9', 'Балкон', 'Московская ~10мин', 'kufar.by', 310,
     '🥈 Кирпич, капремонт 2024. К 2028 своя станция метро — лучшая инвестиция.'],
    ['https://re.kufar.by/vi/1079997288', 437994, 3, 68.1, 48.1,
     'Калиновского 48к2', '6/9', 'Лоджия', 'Восток ~5-10мин', 'kufar.by', 309,
     '🥉 Капремонт 2025! Панорамный вид на водную систему. Лес рядом. ТОРГ!'],
    ['https://re.kufar.by/vi/1085489171', 475000, 3, 77.6, 45.1,
     'Пташука 1 (Лошица)', '7/17', 'Лоджия', 'Лошица (метро строит.)', 'kufar.by', 295,
     'Вид на реку Свислочь! Лошицкий парк. Умный дом 2017г.'],
    ['https://re.kufar.by/vi/1085990680', 438000, 3, 68.8, 48.3,
     'Калиновского 48к1', '8/9', 'Лоджия', 'Восток ~10мин', 'kufar.by', 279,
     'Тот же дом, что 48к2. Капремонт, утеплённый фасад. Ухоженный двор.'],
    ['https://realt.by/sale-flats/object/4234207/', 562352, 4, 103, 60,
     'Сер.Лес 9 (Зел.Гавань)', '7/8', 'Своб.планировка', 'нет (нужна машина)', 'realt.by', 267,
     '🌲 4к, 103м², 3 санузла! Природный заказник. СВЕРХ бюджета, но если мужу лес — это оно.'],
    ['https://re.kufar.by/vi/1066322172', 323985, 3, 60.4, 38.6,
     'Логойский тракт 4', '5/9', 'Лоджия', 'Московская ~20мин', 'kufar.by', 253,
     'Бюджетный вход. Требует ремонта. Севастопольский парк рядом.'],
    ['https://realt.by/sale-flats/object/4218448/', 475000, 3, 66.8, 45.3,
     'Калиновского 54/3', '7/20', 'Лоджия застекл.', 'Восток ~800м', 'realt.by', 252,
     'Монолит, с мебелью. Вид на храм.'],
    ['https://re.kufar.by/vi/1085336904', 354000, 3, 61, 45.7,
     'Славинского 31', '3/5', 'Лоджия застекл.', 'Восток', 'kufar.by', 251,
     'С мебелью, косметический ремонт. Панель 1969.'],

    # === ИСКЛЮЧЕНО МУЖЕМ: 4-5 этаж в 5-этажке ===
    ['https://realt.by/sale-flats/object/4236187/', 404225, 3, 60.6, 45.9,
     'Независимости 135', '4/5 ❌', 'Балкон', 'Восток ~4 мин', 'realt.by', 'искл',
     'Исключено: 4-й этаж в пятиэтажке. А жаль — 4 мин до метро, хороший вариант.'],
    ['https://realt.by/sale-flats/object/4178217/', 475380, 3, 62.94, 44.42,
     'Восточная 22/2', '4/5 ❌', 'Лоджия', 'Академия наук ~7мин', 'realt.by', 'искл',
     'Исключено: 4-й этаж в пятиэтажке. Кирпич, капремонт, жалко терять.'],
    ['https://realt.by/sale-flats/object/4010027/', 370000, 3, 59, 46.7,
     'Берестянская 15', '5/5 ❌', 'Балкон', 'Якуба Коласа ~7мин', 'realt.by', 'искл',
     'Исключено: последний этаж пятиэтажки. Золотая горка, жалко!'],

    # === 1-Й ЭТАЖ (отдельно) ===
    ['https://realt.by/sale-flats/object/4159954/', 453882, 3, 81.6, 59.3,
     'Подлесная 4', '1/16', 'Лоджия', 'Восток', 'realt.by', '1эт',
     'Новостройка 2024, лес, монолит. Математически лучший вариант, но 1-й этаж.'],
    ['https://realt.by/sale-flats/object/4235057/', 489000, 3, 78.9, 44,
     'Навуковая 8', '1/8', 'Лоджия застекл.', 'Борисовский тракт', 'realt.by', '1эт',
     'Новостройка 2025, панель. 1-й этаж.'],

    # === ONLINER (балкон не подтверждён) ===
    ['https://r.onliner.by/pk/apartments/1282012', 496000, 3, 74, 52.2,
     'Якуба Коласа 65', '8/8', '?', 'Якуба Коласа', 'onliner.by', '?',
     'Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1284298', 450000, 4, 59.2, 41.9,
     'Куйбышева 101', '5/5', '?', 'Якуба Коласа', 'onliner.by', '?',
     '4-КОМНАТНАЯ! Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1258995', 427404, 3, 62.1, 40,
     'Сурганова 86', '3/9', '?', 'Академия наук', 'onliner.by', '?',
     'Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1283965', 442000, 3, 61.8, 39.3,
     'Сурганова 57', '6/9', '?', 'Академия наук', 'onliner.by', '?',
     'Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1282268', 390000, 3, 58.5, 42.3,
     'Куйбышева 46', '8/9', '?', 'Якуба Коласа', 'onliner.by', '?',
     'Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1264602', 461590, 3, 67.9, 41.9,
     'М.Богдановича 102', '2/9', '?', 'Академия наук', 'onliner.by', '?',
     'Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1281648', 356500, 3, 60.8, 45.7,
     'Седых 50', '2/5', '?', 'Восток', 'onliner.by', '?',
     'Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1279957', 376700, 3, 50.2, 34,
     'Славинского 13', '3/5', '?', 'Восток', 'onliner.by', '?',
     'Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1282900', 419739, 3, 54.9, 33.5,
     'Слесарная 4', '4/5', '?', 'Автозаводская', 'onliner.by', '?',
     'Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1273538', 427326, 3, 61.6, 38,
     'Нахимова 19', '9/9', '?', 'Автозаводская', 'onliner.by', '?',
     'Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1283154', 357000, 3, 61.2, 38.9,
     'Менделеева 30', '7/9', '?', 'Академия наук', 'onliner.by', '?',
     'Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1269736', 331700, 3, 60.4, 38.6,
     'Логойский тракт 4', '5/9', '?', 'Восток', 'onliner.by', '?',
     'Проверить балкон'],
    ['https://r.onliner.by/pk/apartments/1283527', 423177, 3, 68.2, 41.2,
     'Мележа 4', '3/9', '?', 'Академия наук', 'onliner.by', '?',
     'Проверить балкон'],

    # === В ТАБЛИЦЕ ===
    ['https://realt.by/sale-flats/object/4023808/', 417560, 3, 62.2, 41, '', '', '', '', 'realt.by', '?',
     '[Было в таблице изначально]'],
]

gold_fill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
green_fill = PatternFill(start_color='D9EAD3', end_color='D9EAD3', fill_type='solid')

for row_idx, row_data in enumerate(data, 2):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        if col_idx == 1:
            cell.font = Font(color='0000FF', underline='single')
        if col_idx == 2:
            cell.number_format = '# ##0'
            cell.alignment = Alignment(horizontal='right')
        if col_idx == 11 and isinstance(value, (int, float)):
            cell.alignment = Alignment(horizontal='center')
            cell.font = Font(bold=True, size=12)
            if value >= 300:
                cell.fill = green_fill
            elif value >= 250:
                cell.fill = gold_fill
        if isinstance(value, str) and ('искл' in value or '1эт' in value):
            cell.alignment = Alignment(horizontal='center')
            cell.font = Font(color='FF0000', bold=True, size=12)
        if isinstance(value, str) and '❌' in value:
            cell.font = Font(color='FF0000', bold=True)
        if isinstance(value, str) and '1-Й ЭТАЖ' in value:
            cell.font = Font(color='FF0000', bold=True)

widths = [50, 16, 8, 12, 12, 28, 10, 20, 26, 12, 9, 55]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

ws.freeze_panes = 'A2'
ws.auto_filter.ref = f'A1:L{len(data)+1}'

filepath = r'C:\Users\marcenuk\Desktop\Квартиры_Минск.xlsx'
wb.save(filepath)
print(f'OK: {filepath}')
print(f'Rows: {len(data)}')