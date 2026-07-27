---
type: reference
title: GitHub репозитории look85-ops
description: "Список всех репозиториев организации look85-ops с назначением и статусом"
tags: [github, infra, repos]
timestamp: 2026-07-08
---

# GitHub Репозитории (look85-ops)

Актуально: 2026-07-08

## Основные репо

| Репо | Назначение | Статус |
|------|------------|--------|
| NAAssistant | Центральный репозиторий, все скиллы и команды. Содержит methodist-booster как поддиректорию | ✅ Основной |
| methodist-booster | Отдельный репозиторий на GitHub, локально — поддиректория NAAssistant | ✅ Отдельный репо |
| context-map | Дайджест для переезда в РБ | ✅ Активный |

## Всегда рабочие (не архивировать!)

| Репо | Назначение | Сайт |
|------|------------|------|
| digital-garden | AI-сад искусства, генерация артефактов каждые 4ч | look85-ops.github.io/digital-garden/ |
| shelter | Тёплая страница с пушистым существом | look85-ops.github.io/shelter/ |
| amalgamma | AI-проект (Python + HTML) | — |

**Правило:** Эти три репо НИКОГДА не архивировать. Они должны всегда работать.

## Архивированные

methodist-booster-pro, ld-botassistant, cucpo-assistant, metod_buster

## Структура skills

```
.opencode/
├── agent/     # Агенты (career-architect, learning-designer, и т.д.)
├── command/   # Команды (/grill-me, /tdd, /social, и т.д.)
docs/skills/   # Документация скиллов
scripts/       # Скрипты (skills-audit.ps1, verify.ps1)
```

## Внешние источники

- mattpocock/skills — инженерные скиллы (158k ⭐)
- coreyhaines31/marketingskills — маркетинговые скиллы (36.8k ⭐)
- nvidia/skillspector — аудит безопасности (12.1k ⭐)
- obra/superpowers — методология разработки
- anthropics/skills — обработка файлов, frontend, тестирование

## Токен доступа

Хранится в `C:\Users\NaMk\Desktop\Проект\ghtoken.txt`
