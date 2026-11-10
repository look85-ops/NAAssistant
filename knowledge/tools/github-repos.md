---
type: reference
title: GitHub репозитории look85-ops
description: "Список всех репозиториев организации look85-ops с назначением и статусом"
tags: [github, infra, repos]
timestamp: 2026-10-27
---

# GitHub Репозитории (look85-ops)

Актуально: 2026-10-27. Всего 13 репозиториев (9 активных, 4 архивированных).

## Активные репозитории

| Репо | Назначение | Последний push |
|------|------------|----------------|
| NAAssistant | Центральный репозиторий: скиллы, команды, агенты, знания. Содержит methodist-booster и portfolio как поддиректории | 2026-10-26 |
| digital-garden | AI-сад искусства, генерация артефактов каждые 4ч | 2026-10-27 |
| amalgamma | AI-зеркало: отражает заголовки BBC/NPR как абстрактные HTML/CSS-композиции | 2026-10-27 |
| vo-dvore | «Во дворе» — дворовые игры по QR-коду на детской площадке | 2026-10-23 |
| methodist-booster | Бустер методиста — 5-6 инструментов для L&D-методологов | 2026-10-19 |
| context-map | Геополитический дайджест для переезда РФ → РБ | 2026-10-12 |
| pptx-scenario-layout | Обновление master-дек PowerPoint из сценария урока (clone/replace/hide/reorder/validate) | 2026-08-18 |
| aos-analyzer | AOS (After Oral Session) — анализатор анкет: CSV/Excel → метрики + аномалии + дашборд + AI-рекомендации | 2026-07-24 |
| shelter | Тёплая страница с пушистым существом | 2026-06-30 |

## Всегда рабочие (не архивировать!)

| Репо | Назначение | Сайт |
|------|------------|------|
| digital-garden | AI-сад искусства | look85-ops.github.io/digital-garden/ |
| shelter | Тёплая страница | look85-ops.github.io/shelter/ |
| amalgamma | AI-зеркало | — |

**Правило:** Эти три репо НИКОГДА не архивировать. Они должны всегда работать.

## Архивированные

| Репо | Назначение |
|------|------------|
| methodist-booster-pro | Ранняя pro-версия Бустера |
| metod_buster | Ранняя версия Бустера |
| cucpo-assistant | Ассистент ЦУКПО |
| ld-botassistant | L&D бот-ассистент |

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
