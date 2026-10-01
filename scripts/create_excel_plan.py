"""Создаёт Excel-таблицу с планом откликов и холодных писем по 24 компаниям."""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Load scan results
with open(r"C:\Users\marcenuk\Desktop\Новый проект\career\market\company_scan_2026-09-25.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Known response history
history = {
    "Альфа-Банк": "2 отказа (адаптация, методист)",
    "ТД Комплект": "просмотрен (AI-проекты)",
    "TutorOnline": "отказ (Head of Courses)",
}

wb = Workbook()
ws = wb.active
ws.title = "План откликов"

# Styles
header_font = Font(bold=True, color="FFFFFF", size=11)
header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
yellow_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
gray_fill = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
wrap = Alignment(wrap_text=True, vertical="top")
thin_border = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"), bottom=Side(style="thin")
)

# Headers
headers = ["N", "Компания", "Сфера", "L&D вакансии на rabota.by", "История откликов",
           "Действие", "Приоритет", "Контакты/Сайт карьеры"]
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    cell.border = thin_border

# Column widths
widths = [4, 22, 12, 45, 30, 22, 12, 45]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w

# Sort companies: Banks first, then IT, EdTech, Telecom, Industry
sphere_order = {"банки": 0, "IT": 1, "EdTech": 2, "телеком": 3, "ритейл": 4, "пром": 5}
sorted_companies = sorted(data.items(), key=lambda x: sphere_order.get(x[1].get("sphere", ""), 99))

# Priority logic
high_priority = ["Альфа-Банк", "ВТБ", "EPAM", "IBA Group", "ITransition", "TutorOnline", "Skillbox", "А1"]
medium_priority = ["Белагропромбанк", "Беларусбанк", "Andersen", "Innowise", "LogicLike", "Lerna", "Fix Price", "Пеленг", "ТД Комплект"]

row = 2
for i, (name, info) in enumerate(sorted_companies, 1):
    sphere = info.get("sphere", "")
    lnd_count = info.get("lnd_count", 0)
    vacancies = info.get("vacancies", [])
    
    # Build L&D vacancies string
    lnd_vacs = [v for v in vacancies if v.get("lnd")]
    lnd_text = "\n".join([f"• {v['title']}" for v in lnd_vacs]) if lnd_vacs else "—"
    
    # History
    hist = history.get(name, "—")
    
    # Determine action
    if name in history and "отказ" in hist.lower():
        action = "Пропустить (отказ)"
        fill = gray_fill
    elif lnd_vacs:
        action = "Откликнуться"
        fill = green_fill
    else:
        action = "Холодное письмо"
        fill = yellow_fill
    
    # Priority
    if name in history and "отказ" in hist.lower():
        prio = "—"
    elif name in high_priority:
        prio = "HIGH"
    elif name in medium_priority:
        prio = "MEDIUM"
    else:
        prio = "LOW"
    
    # Career site
    career_sites = {
        "Белагропромбанк": "belapb.by → Вакансии",
        "Альфа-Банк": "rabota.alfabank.by",
        "Беларусбанк": "belarusbank.by → Карьера",
        "ВТБ": "vtb.by → Карьера",
        "БНБ-Банк": "bnb.by → Вакансии",
        "EPAM": "epa.ms/careers | training.ru",
        "IBA Group": "ibagroup.by → Карьера",
        "ITransition": "itransition.by → Вакансии",
        "Andersen": "andersenlab.com → Careers",
        "Innowise": "innowise.com → Careers",
        "IDF Technology": "idf.technology → Вакансии",
        "Team.Inno": "team-inno.by → Вакансии",
        "Пеленг": "peleng.by → Вакансии",
        "Атлант-М": "atlantm.by → Карьера",
        "OMA": "oma.by → Вакансии",
        "Alutech": "alutech.by → Карьера",
        "Примвэй": "primway.by → Вакансии",
        "LogicLike": "logiclike.com → Вакансии",
        "Lerna": "lerna.by → Вакансии",
        "TutorOnline": "tutoronline.ru → Карьера",
        "Skillbox": "skillbox.ru → Карьера",
        "А1": "a1.by → Карьера",
        "Fix Price": "fix-price.com → Карьера",
        "ТД Комплект": "tdkomplekt.by → Вакансии",
    }
    
    vals = [i, name, sphere, lnd_text, hist, action, prio, career_sites.get(name, "")]
    for col, val in enumerate(vals, 1):
        cell = ws.cell(row=row, column=col, value=val)
        cell.border = thin_border
        cell.alignment = wrap
        cell.fill = fill
    row += 1

# Add summary section
row += 2
ws.cell(row=row, column=1, value="ИТОГО").font = Font(bold=True, size=12)
row += 1
summary_data = [
    ("Откликнуться (есть L&D вакансия)", sum(1 for _, info in sorted_companies if info.get("lnd_count", 0) > 0 and info.get("name", "") not in ["Альфа-Банк", "TutorOnline"])),
    ("Холодное письмо (нет L&D вакансий)", sum(1 for _, info in sorted_companies if info.get("lnd_count", 0) == 0)),
    ("Пропустить (отказ в истории)", sum(1 for name, _ in sorted_companies if name in history and "отказ" in history[name].lower())),
]
for label, count in summary_data:
    ws.cell(row=row, column=1, value=label).font = Font(bold=True)
    ws.cell(row=row, column=2, value=count)
    row += 1

# Freeze pane
ws.freeze_panes = "A2"

# Auto-filter
ws.auto_filter.ref = f"A1:H{row - 4}"

outpath = r"C:\Users\marcenuk\Desktop\План_откликов_24_компании.xlsx"
wb.save(outpath)
print(f"Saved: {outpath}")