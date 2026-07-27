# Skill: Digest — Context Map v2

Геополитический дайджест для переезжающих в Беларусь из РФ.

## Триггер

- `/digest` — ручной запуск в чате
- GitHub Actions: раз в неделю, ПН в 06:00 UTC (cron: `0 6 * * 1`)
- `workflow_dispatch` в Actions

## Output Contract (LAWs для дайджеста)

Каждый выпуск следует правилам из `docs/process/output-contract-template.md`:

- **BADGE** — первая строка: `🌐 Context Map v{VERSION} · synced {YYYY-MM-DD}`
- **LAW 1** — Нет блока источников в конце (ссылки внутри текста)
- **LAW 2** — Нет выдуманных заголовков (только 7 стандартных разделов)
- **LAW 5** — Каждый факт со ссылкой `[Название](URL)`
- **LAW 6** — Голос сообщества: Reddit/Polymarket/X цитаты вплетены в нарратив
- **LAW 7** — Footer с метриками: сколько источников, какие платформы

## Что изменилось в v2

| Было (v1) | Стало (v2) |
|---|---|
| Только DuckDuckGo (15-25 ссылок) | DDG + Reddit сообщества + Polymarket маркеты |
| 10 хардкодных запросов | Pre-flight: динамическая подстройка запросов |
| Пост-обработка чинит кривые ссылки | Output contract: ссылки правильные с первого раза |
| Mon/Wed (2 раза в неделю) | Раз в неделю (ПН) |
| Нет community voices | Reddit-комментарии + Polymarket odds в каждом выпуске |
| Нет footer-а | Footer с составом: откуда данные, сколько всего |

## Pre-Flight перед запуском

Перед каждым запуском (ручным или cron) проверяется `docs/process/pre-flight-template.md`:

1. **Источники:** DDG доступен? Reddit JSON отвечает? Polymarket Gamma API жив?
2. **Запросы:** не устарели? не keyword trap?
3. **API-ключи:** DS_API_KEY, GH_TOKEN валидны?

## Структура дайджеста (7 разделов)

1. **Обзорная карта** — тренд, риск, возможность (2-3 абзаца, привязанных к переезду)
2. **Поле боя** — РФ / РБ / Украина / Мир
3. **Слабые сигналы** — 3-5 edge signals
4. **Устойчивые паттерны** — что подтверждается 3+ периодов
5. **Влияние на решения** — работа / недвижимость / деньги / отрасли
6. **Сценарии на 1-3 мес** — базовый / эскалация / деэскалация
7. **Дополнительно** — слепое пятно

Новый: в каждом разделе могут быть цитаты из Reddit и Polymarket odds.

## Источники (v2)

| Источник | Тип | API | Ключ? |
|---|---|---|---|
| DuckDuckGo | Новости | ddgs | Нет |
| Reddit (r/belarus, r/geopolitics, r/ukraine, r/europe) | Community | reddit.com/.json | Нет |
| Polymarket | Prediction markets | gamma-api.polymarket.com | Нет |
| DeepSeek V3 | Synthesis | bothub.ru | DS_API_KEY |
| Llama 3.3 70B (fallback) | Synthesis | GitHub Models | GH_TOKEN |

## Формат ссылок (строго)

- Каждый абзац — минимум одна ссылка `[Название](полный URL с https://)`
- Community цитаты: `u/name` или `@handle` или `Polymarket: X%`
- Никаких голых `[N]`, `(url)`, `[Name]url`
- Все ссылки `target="_blank" rel="noopener"` в HTML

## Footer

В конце каждого выпуска — блок "Как собиралось":

```
📊 Дайджест собран из: {N} новостей (DDG) + {M} обсуждений (Reddit) + {K} маркетов (Polymarket)
🕐 {timestamp}
📎 Raw: artifacts/{date}.html
```

## Валидация (validate_digest v2)

- Все markdown-ссылки имеют `https://`
- Нет голых `[N]` рефов
- Нет code fence-обёртки
- Badge присутствует на первой строке (если сохраняется .md)
- Footer присутствует
- Community voices: если Reddit/Polymarket вернули данные, они отражены в тексте

## Deploy

Пуш в main → GitHub Actions генерирует дайджест → коммитит в `index.html` + `artifacts/` → GH Pages обновляется.
