# Skills Audit — 06.07.2026

## Репозитории

| Репо | Skills | Статус |
|------|--------|--------|
| NAAssistant | .opencode/agent (7), .opencode/command (17) | ✅ Основной |
| methodist-booster | .opencode/agent (7), .opencode/command (19) | ✅ Основной |
| methodist-booster-pro | — | ⚠️ Пустой |
| digital-garden | — | ⚠️ Пустой |
| amalgamma | — | ⚠️ Пустой |
| shelter | — | ⚠️ Пустой |
| context-map | — | ✅ Дайджест |
| ld-botassistant | — | ⚠️ Пустой |
| cucpo-assistant | — | ⚠️ Пустой |
| metod_buster | — | ⚠️ Пустой |

## Внешние источники (ADOPTED_SKILLS.md)

| Источник | Статус | Риск |
|----------|--------|------|
| obra/superpowers | ✅ Используется | low |
| anthropics/skills (pdf/docx/xlsx) | ✅ Используется | low |
| anthropics/frontend-design | ✅ Используется | low |
| coreyhaines31/marketingskills | ✅ Используется | low |
| muratcankoylan/context-engineering | ✅ Принципы | low |
| anthropics/webapp-testing | ✅ Используется | low |
| lackeyjb/playwright-skill | ⚠️ Опциональный | low |
| anthropics/skill-creator | ✅ Используется | low |

## Внутренние скиллы

| Скилл | Где | Статус |
|-------|-----|--------|
| learning-designer | .opencode/agent/ | ✅ Активный |
| CODE_QUALITY.md | docs/skills/ | ✅ Активный |
| WEB_SCRAPING.md | docs/skills/ | ✅ Активный |
| ADOPTED_SKILLS.md | docs/skills/ | ✅ Документация |
| AUDIT_TEMPLATE.md | docs/skills/ | ✅ Шаблон |
| CLAUDE_AUDIT.md | docs/skills/ | ✅ Аудит |
| DYNAMIC_CONTEXT.md | docs/skills/ | ✅ Контекст |
| HOOKS.md | docs/skills/ | ✅ Хуки |
| NVIDIA_NIM.md | docs/skills/ | ✅ API |
| SHELL_GUARDS.md | docs/skills/ | ✅ Безопасность |

## Новые команды (из внешних источников)

| Команда | Источник | Статус |
|---------|----------|--------|
| /grill-me | mattpocock/skills | ✅ Установлена |
| /tdd | mattpocock/skills | ✅ Установлена |
| /code-review | mattpocock/skills | ✅ Установлена |
| /copywriting | marketingskills | ✅ Установлена |
| /social | marketingskills | ✅ Установлена |
| /content-strategy | marketingskills | ✅ Установлена |
| /skills-audit | nvidia/skillspector | ✅ Установлена |

## Рекомендации

1. **Пустые репо** — рассмотреть удаление или архивацию: methodist-booster-pro, digital-garden, amalgamma, shelter, ld-botassistant, cucpo-assistant, metod_buster
2. **Дублирование** — NAAssistant и methodist-booster имеют идентичные структуры .opencode. Проверить, нужен ли methodist-booster как отдельный репо
3. **Безопасность** — все внешние скиллы ссылаются на проверенные источники (anthropics, obra, coreyhaines31). Рекомендую проверять обновления раз в квартал
4. **Новые команды** — 7 команд из mattpocock/marketingskills установлены в локальный проект. Нужно синхронизировать с NAAssistant на GitHub
