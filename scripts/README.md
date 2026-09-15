# Каталог скриптов

Как пользоваться: не пиши скрипт заново — сначала ищи здесь. Запуск через `py scripts/<имя>.py`.

## AOS (обработка обратной связи)

| Скрипт | Что делает |
|---|---|
| `aos_wave_report.py` | Главный: формирует отчёт по волне AOS по шаблону `docs/aos/reports/TEMPLATE_wave.md` |
| `analyze_m2_aos.py` | Разовый анализ волны M2 по Excel |
| `read_aos_m2.py` | Читает xlsx-файлы из папки AOS M2 |
| `test_runner.py` | Тест-прогон `aos_analyzer.core` |
| `test_aos.csv` | Тестовые данные для прогона |

## Веб-поиск

| Скрипт | Что делает |
|---|---|
| `websearch.py` | Поиск через DuckDuckGo Lite (без API, бесплатно, работает из РФ) — **основной** |

## Работа с документами

| Скрипт | Что делает |
|---|---|
| `read_doc.py` | Читает .docx / .pdf / .pptx и выводит текст в stdout или .md |
| `convert_md_to_docx.py` | Конвертация .md → .docx (стиль L&DxAI) |
| `convert_signal_to_docx.py` | Конвертация дайджеста «Сигнал» .md → .docx (в `knowledge/signal/`) |
| `build_resume_docx.py` | Резюме .md → .docx с акцентным цветом |

## PowerPoint

| Скрипт | Что делает |
|---|---|
| `pptx_pipeline.py` | **Единый CLI-конвейер раскладки по сценарию** (Фаза A: parse/catalog/diff/update/layout/validate; Фаза B: export/insert) |
| `pptx_tool.py` | Создание/редактирование pptx через python-pptx |
| `pptx_diff.py` | Сверка «сценарий ↔ презентация» по слайдам (внутри `pptx_pipeline.py diff`) |
| `pptx_com.py` | COM-библиотека правок слайдов (clone/edit/hide/tag/textbox/table) |
| `parse_scenario_xml.py` | Парсинг docx-сценария через XML (для файлов > 50 МБ) |
| `word_pages.py` | Парсинг docx-сценария через Word COM (для малых файлов) |
| `catalog_types.py` | Каталогизация слайдов pptx по типу |
| `insert_slides_batch.py` | Вставка слайдов в свободные маркеры (ручная конфигурация в шапке) |

### pptx_pipeline.py — примеры

```powershell
$env:PYTHONIOENCODING="utf-8"
& "C:\Users\marcenuk\AppData\Local\Python\bin\python.exe" scripts\pptx_pipeline.py parse  scenario.docx scenario.json
& "C:\Users\marcenuk\AppData\Local\Python\bin\python.exe" scripts\pptx_pipeline.py catalog pres.pptx catalog.json
& "C:\Users\marcenuk\AppData\Local\Python\bin\python.exe" scripts\pptx_pipeline.py diff  scenario.json catalog.json -o diff.md
& "C:\Users\marcenuk\AppData\Local\Python\bin\python.exe" scripts\pptx_pipeline.py update pres.pptx operations.json --backup
& "C:\Users\marcenuk\AppData\Local\Python\bin\python.exe" scripts\pptx_pipeline.py layout pres.pptx target_order.txt --backup
& "C:\Users\marcenuk\AppData\Local\Python\bin\python.exe" scripts\pptx_pipeline.py validate pres.pptx [-o report.txt]
& "C:\Users\marcenuk\AppData\Local\Python\bin\python.exe" scripts\pptx_pipeline.py export  pres.pptx slides_dir [--range 1-20]
& "C:\Users\marcenuk\AppData\Local\Python\bin\python.exe" scripts\pptx_pipeline.py insert  scenario.docx result.docx slides_dir
```

Порядок работы для одного дня:
1. **Фаза A** (сценарий → презентация, до дизайнера): `parse` → `catalog` → `diff` (план: добавить/исправить/скрыть) → `update` (clone/edit/hide) → `layout` (порядок по карте) → `validate`.
2. **Пауза**: презентация уходит к дизайнеру.
3. **Фаза B** (презентация → сценарий, после дизайнера): `export` (слайды → PNG) → `insert` (PNG по меткам «Слайд» в docx, по контенту, без номеров).

## Генерация контента

| Скрипт | Что делает |
|---|---|
| `generate_digest.py` | Пайплайн «L&D×AI Дайджест» через API |
| `generate_summary_v6.py` | Сборка итогового .docx из сводки |
| `gen_lib_v4.py` | Генерация библиотеки протоколов из HTML |
| `course_scenario_pipeline.py` | AI-пайплайн: сценарий (docx) → чистый сценарий Markdown |
| `llm_gateway.py` | Единая точка доступа к LLM для NM.ASSISTANT |
| `update_decisions.py` | Обновление строки в `logs/decisions.md` |

## Проверка текста

| Скрипт | Что делает |
|---|---|
| `fix_typos.py` | Ищет и исправляет опечатки в docx (копия рядом `_fixed`, оригинал не трогает) |
