# Python script to update decisions.md
import os

path = 'C:\\Users\\marcenuk\\Desktop\\Новый проект\\logs\\decisions.md'

# Read the file with UTF-8 encoding
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the M3 AOS entry and replace it
new_lines = []
for line in lines:
    if '2026-07-01' in line and 'AOС' in line and 'Академия Пути' in line:
        # Replace this line with the updated version
        new_lines.append('- 2026-07-01 (АОС, Академия Пути): NPS 94.1% (цель 9.1 — перевыполнен). Средняя форматов 9.63. Лучшие: Мелихов (10.0), Залива (10.0). Единственный risk-flag: Манюгина (8.18, М3), Дорофеев (8.12, М2) — оба преподавателя из вуза (effect "чужой"). Решения: (1) не замена, а интеграция спикеров через наставников/адаптацию под ЦА; (2) не новый шаблон эконом. обоснования, а практический разбор с наставником; (3) усиление ТБ-брифинга перед промышленными экскурсиями. Отчёт: `docs/aos/reports/2026-07-01-m3-akademiya.md`.\\n')
    else:
        new_lines.append(line)

# Write back to file
with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Successfully updated decisions.md with M2+М3 combined entry')
