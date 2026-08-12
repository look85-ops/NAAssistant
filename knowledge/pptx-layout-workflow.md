# Алгоритм: раскладка презентации по сценарию (полный SOP)

Проверено на М1Д4 и М3Д1. Для каждого модуля «Профессионал+. Путь»
и «Академия пути», где нужно синхронизировать управляющую презентацию
со сценарием (вынести голубой контент на слайды, вставить новые слайды,
скрыть неиспользуемые).

**Входные данные:** управляющая презентация `.pptx` + сценарий `.docx`
(с маркерами «Слайд №N» и голубым текстом для нового контента).

---

## Этап 0 — Подготовка окружения

1. Скопировать `.pptx` во временную папку с ЛАТИНСКИМ путём
   (python-pptx не дружит с кириллицей в путях):
   ```
   copy src.pptx → %TEMP%\opencode\m3dx\pres_orig.pptx
   ```

2. Скопировать туда же сценарий `.docx`:
   ```
   copy scenario.docx → %TEMP%\opencode\m3dx\scenario.docx
   ```

3. Рабочий файл — всегда копия. Оригинал не трогать.

4. Обязательные инструменты в `%TEMP%\opencode\`:
   - `pptx_com.py` — COM-операции (open, close, duplicate_slide, move_slide,
     hide_slide, add_textbox, add_tag, remove_tag)
   - Скрипты этапа 1 (см. ниже) — хранить рядом или писать по шаблону

---

## Этап 1 — Парсинг сценария (извлечение маркеров)

**Проблема:** Word COM виснет на .docx >50MB. Решение: открыть как ZIP,
достать `word/document.xml`, парсить lxml.

```python
# parse_scenario.py — ключевая логика
import zipfile, lxml.etree as ET

with zipfile.ZipFile('scenario.docx') as z:
    xml = z.read('word/document.xml')
tree = ET.fromstring(xml)

# Пространства имён
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# Цвет шрифта: w:rPr/w:color/@w:val
# Голубой = '0070C0'. Красный для «Примечание:» — игнорировать.

# Маркер = короткий параграф (≤60 символов), начинающийся с «Слайд»
# Всё остальное с «Слайд» в тексте — не маркер, а контент.

# Собираем структуру:
# [
#   {
#     "marker": "Слайд №1" | "Слайд 20" (без №) | "Слайд" (без номера),
#     "ap": true/false,  # если маркер содержит «М2Д1», «М1Д2» и т.п.
#     "lines": [{"t": "...", "blue": true/false}, ...]
#   },
#   ...
# ]
```

**На выходе:** `scenario_slides.json` — список из ~275 маркеров с их
контентом и флагом голубого.

---

## Этап 2 — Каталогизация презентации

Использовать python-pptx (не COM — COM даёт битый текст для TextBox type 17).

```python
# catalog.py — перебор слайдов через python-pptx
from pptx import Presentation
prs = Presentation('pres_orig.pptx')

for i, slide in enumerate(prs.slides, 1):
    info = {
        'n': i,
        'layout': slide.slide_layout.name,
        'texts': []
    }
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                t = para.text.strip()
                if t:
                    info['texts'].append(t)
```

**На выходе:** `catalog.json` — 250 слайдов: `n, layout, type, texts[]`.

---

## Этап 3 — Построение карты соответствий

### 3a. Сборка номерных маркеров
```python
# build_map.py
for marker in scenario_slides:
    if marker is numbered ("Слайд №N" or "Слайд N"):
        num = parse_number(marker)
        # find matching slide in catalog by num (primary key)
        # if no exact match (e.g. unnumbered "Слайд N" без №),
        #   try content matching with fallback
```

### 3b. Классификация позиций
- **USE** — маркер ссылается на существующий слайд (cat_n)
- **NEW** — маркер «Слайд» без номера с голубым контентом → новый слайд
- **APHOLE** — маркер с ap=true («Слайд N – М2Д1») → дырка для АП

### 3c. Определение списков
```python
# Из карты:
new_slides = [m for m in map if m.kind == 'NEW']        # 25 шт.
blue_additions = {num: lines for numbered markers with blue content}  # 20 шт.
hide_list = [n for n in 1..250 if n not in used_cat_numbers]  # 17 шт.
ap_holes = [m for m in map if m.kind == 'APHOLE']       # 3 шт.
```

**На выходе:** `target_map.json` (275 позиций: 247 USE + 25 NEW + 3 APHOLE),
`edit_data.json` (blue_additions + new_slides content).

---

## Этап 4 — Определение шаблонов для клонирования

### 4a. Выбор шаблонов
Из COM-дампа (структура форм) выбираем слайды-образцы:
| Тип | Шаблон | Layout | Признак |
|---|---|---|---|
| QUESTION | slide 4 | «Опрос. Модуль 1 (вопрос)» | TextBox 13,16,17,15 |
| DISCUSS | slide 29 | «fbv вопрос» | TPlaceholder2 «Дискуссия» |
| SELFWORK | slide 30 | «fbv вопрос» | TPlaceholder1 «Работаем в 4 подгруппах» |
| CONTENT | slide 33 | content | TPlaceholder3 (title) + TPlaceholder1 (body) |

### 4b. Захват SlideID шаблонов (НЕ по тексту!)
**ВАЖНО:** COM возвращает битый текст для TextBox (type 17), но корректный
для TextPlaceholder (type 14). Поэтому идентифицируем шаблоны по SlideID:
```python
tpl_ids = {
    'question': pres.Slides.Item(4).SlideID,
    'discuss':  pres.Slides.Item(29).SlideID,
    'selfwork': pres.Slides.Item(30).SlideID,
    'content':  pres.Slides.Item(33).SlideID,
}
```

### 4c. Проверка клона (урок №10)
Перед массовым созданием — тест-клон 1 шаблона, проверка структуры форм,
заполнение текстом, smoke-сохранение. Убедиться что Shape.Count и имена
форм сохраняются.

---

## Этап 5 — Карта вставки новых слайдов

### 5a. Якоря (anchors)
Для каждого нового слайда: **anchor** = номер предыдущего нумерованного
маркера в сценарии. Слайд вставляется ПОСЛЕ этого номера (на позицию anchor+1).

```python
# Порядок — по сценарию. Например:
insertions = [
    (5,   'question', lines),  # после Слайда №5
    (5,   'question', lines),  # ещё один после №5
    (21,  'discuss',  lines),  # после №21
    (21,  'content',  lines),  # North Star после №21
    ...
]
```

### 5b. Порядок обработки
**Строго по убыванию якоря (descending anchors).**
Внутри одного якоря — в ОБРАТНОМ порядке желаемой последовательности.

Причина: вставка на позицию N+1 не затрагивает позиции < N+1.
При обработке от большего якоря к меньшему — позиции стабильны.
Обратный порядок внутри якоря даёт правильную финальную последовательность.

```python
insertions.sort(key=lambda x: (-x['anchor'], -x['scenario_idx']))
for spec in insertions:
    clone_template → fill → tag → MoveTo(anchor+1)
```

---

## Этап 6 — COM-правки (порядок критичен!)

### Порядок операций:
1. **Голубые дополнения** — ПЕРВЫМИ (индексы слайдов ещё == оригинальным номерам)
2. **Новые слайды** — ВТОРЫМИ (клоны + заполнение + MoveTo; после них индексы смещаются)
3. **Скрытие неиспользуемых** — ТРЕТЬИМИ (индексы уже финальные)

Если перепутать порядок (новые слайды до голубых дополнений) — голубой текст
попадёт на неправильные слайды (индексы съехали).

### Заполнение клонов:
- QUESTION: TextBox 13 = заголовок, TextBox 16 = вопрос, TextBox 17 = инструкция
- DISCUSS: TextPlaceholder2 = «Обсудим:», TextBox 23 = текст обсуждения
- SELFWORK: TextPlaceholder1 = контент
- CONTENT: TextPlaceholder3 = заголовок, TextPlaceholder1 = тело

После заполнения — `add_tag(clone, 'Новый')`.

### Голубые дополнения:
```python
pc.add_textbox(slide, 50, 40, 850, 120, text, size=14, rgb=(0,112,192))
pc.add_tag(slide, 'Изменено')
```
Текст — синим цветом (0070C0), позиция — верх слайда, чтобы не мешать
основному контенту. Наташа при визуальной проверке сольёт с дизайном.

### Скрытие:
```python
pc.hide_slide(pres, slide_number)
```

---

## Этап 7 — Валидация

```python
# 1. Count
total = pres.Slides.Count
# expected = orig_count - len(hide) + len(new)
# М3Д1: 250 - 17 + 25 = 258 visible (275 total incl. hidden)

# 2. Hidden count
for i in range(1, total+1):
    if pres.Slides.Item(i).SlideShowTransition.Hidden == -1:
        hidden += 1

# 3. Tag count
# «Новый» tags == len(new_slides)  (25)
# «Изменено» tags == len(blue_additions)  (20)

# 4. Spot-check: несколько слайдов на правильных позициях
# Проверить текст голубых дополнений на смещённых позициях
```

---

## Этап 8 — Сохранение и передача

1. `pres.Save()` + `pres.Close()` + `app.Quit()`
2. Скопировать результат на рабочий стол (или куда скажет Наташа)
3. В отчёте указать:
   - что сделано (N новых, M голубых, K скрыто)
   - АП-дырки (оставлены, вставляет Наташа вручную)
   - что требует визуальной проверки (новые слайды, голубые дополнения)
4. Записать решение в `logs/decisions.md`

---

## Чек-лист для следующего модуля

- [ ] Скопировать .pptx и .docx в латинский temp
- [ ] Запустить parse_scenario.py → scenario_slides.json
- [ ] Запустить catalog.py → catalog.json
- [ ] Запустить build_map.py → target_map.json
- [ ] Сформировать edit_data.json (blue_additions + new_slides)
- [ ] Определить шаблоны (QUESTION/DISCUSS/SELFWORK/CONTENT) через COM-дамп
- [ ] Тест-клон 1 шаблона
- [ ] Написать apply_edits.py по шаблону
- [ ] Запустить, проверить лог
- [ ] Валидация (count, hidden, tags, spot-check)
- [ ] Скопировать результат на рабочий стол

**Эталонный скрипт:** `C:\Users\marcenuk\AppData\Local\Temp\opencode\apply_edits.py`
**COM-библиотека:** `C:\Users\marcenuk\AppData\Local\Temp\opencode\pptx_com.py`
**Данные М3Д1 (референс):** `C:\Users\marcenuk\AppData\Local\Temp\opencode\m3d1_v2\`
