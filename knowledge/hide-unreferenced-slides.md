## Скрытие неиспользуемых слайдов по сценарию

**Проблема:** В презентации есть слайды, которые не упоминаются в сценарии (устаревший контент). Сценарий — источник истины.

**Процесс:**
1. Извлечь все ссылки «Слайд № X» из сценария (.docx) через regex
2. Собрать номера оригинальных слайдов (1–N), которые НЕ встречаются в ссылках
3. Вычислить актуальные позиции с учётом вставленных слайдов: `current_pos = orig_n + count_of_insertions_before(orig_n)`
4. Добавить `show="0"` в XML этих слайдов

**Инструмент:** работа через `zipfile` (не python-pptx) — модификация XML напрямую в ZIP без перепаковки всего файла. Это в ~50x быстрее.

**Реализация:** `scripts/hide_unreferenced_slides.py`

**Команда для повторения:**
```python
# 1. Извлечь референсы из сценария
import re
links = set()
for m in re.finditer(r'Слайд\s*№\s*(\d+)', scenario_text):
    links.add(int(m.group(1)))

# 2. Найти неиспользуемые
unused = [n for n in range(1, total_slides+1) if n not in links]

# 3. Скрыть через zipfile
with zipfile.ZipFile(pptx_path, 'r') as zin:
    with zipfile.ZipFile(tmp, 'w') as zout:
        for item in zin.infolist():
            data = zin.read(item)
            if re.match(r'ppt/slides/slide(\d+)\.xml', item.filename):
                n = int(m.group(1))
                if n in unused:
                    root = etree.fromstring(data)
                    root.set('show', '0')
                    data = etree.tostring(root, ...)
            zout.writestr(item, data)
```

**Важно:** python-pptx save на больших файлах (1.4+ GB) медленный и может таймаутить. Для hide используем только zipfile.
