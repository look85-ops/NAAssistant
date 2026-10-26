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

> ⚠️ **Устарело (2026-10).** Скрипты добавления/удаления слайдов через COM
> (`pptx_com.py`, `pptx_pipeline.py`, `insert_slides_batch.py`, `catalog_types.py`,
> `word_pages.py`, `parse_scenario_xml.py`) работают плохо и **перемещены в
> `attic/obsolete-slide-scripts/`**. Рабочий пайплайн направления
> «презентация → сценарий» (нумерация «Слайд №N» + скрины) описан в
> `knowledge/pptx/scenario-slide-autonumbering.md` — рендер → TF-IDF+DTW-сопоставление
> → вставка через `lxml`+`zipfile`. Постоянных скриптов для этого направления нет —
> пересоздаются разово в `%TEMP%\opencode\` под каждую пару файлов.

## Генерация контента

| Скрипт | Что делает |
|---|---|
| `generate_digest.py` | Пайплайн «L&D×AI Дайджест» через API |
| `generate_summary_v6.py` | Сборка итогового .docx из сводки |
| `gen_lib_v4.py` | Генерация библиотеки протоколов из HTML |
| `course_scenario_pipeline.py` | AI-пайплайн: сценарий (docx) → чистый сценарий Markdown |
| `llm_gateway.py` | Единая точка доступа к LLM для NM.ASSISTANT |
| `update_decisions.py` | Обновление строки в `logs/decisions.md` |

## Вакансии и поиск работы

| Скрипт | Что делает |
|---|---|
| `vacancy_monitor.py` | Мониторинг вакансий hh.ru с отправкой отчёта на email |
| `scan_companies.py` | Сканирование компаний по заданным критериям |
| `collect_vacancies.py` | Сбор вакансий с hh.ru по фильтрам |
| `quick_monitor.py` | Быстрый мониторинг вакансий (облегчённая версия) |
| `login_hh.py` | Авторизация на hh.ru через Playwright |
| `login_hh_monitor.py` | Поддержание сессии hh.ru для мониторинга |
| `save_results.py` | Сохранение/форматирование результатов поиска |

## Email-рассылки

| Скрипт | Что делает |
|---|---|
| `send_cold_emails.py` | Отправка холодных писем через Gmail SMTP |

## Excel и планирование

| Скрипт | Что делает |
|---|---|
| `create_excel_plan.py` | Создание Excel-плана (учебные программы, расписания) |
| `gen_apartments.py` | Генерация Excel-таблицы квартир (поиск жилья в Минске) |
| `plan.py` | Утилита планирования задач |

## Проверка текста

| Скрипт | Что делает |
|---|---|
| `fix_typos.py` | Ищет и исправляет опечатки в docx (копия рядом `_fixed`, оригинал не трогает) |
