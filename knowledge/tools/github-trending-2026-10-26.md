# GitHub Trending — 26.10.2026

Источник: github.com/trending (daily), 26.10.2026.

## Мета-наблюдение

В списке «Built by» почти каждого репо — ИИ-агенты: Claude, Codex, Cursor, opencode. Значимая часть трендовых репо 2026 года сама собрана агентами. Мы в том же мире.

## Тренды и их применимость

| Репо | ★ | Что | Пригодится? |
|---|---|---|---|
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 47.6k | Skill для coding-агента: многофазный security-аудит с machine-readable находками | **Да** — образец для наших `.opencode/skills/` (рядом с prompt-injection-defense) |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 34.8k | Anti-AI-slop design skill для Claude Code/Cursor/Codex | **Да** — болевая точка portfolio/booster: «не безликий ИИ-дизайн» |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 88.3k | Design language «чтобы AI-harness стал лучше в дизайне» | **Да** — совпадает с нашим skill `impeccable`, усилить |
| [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | 87.6k | Полностью локальная замена ElevenLabs: клонирование голоса, озвучка, дубляж, диктовка, 646 языков | **Возможно** — озвучка курсов + твоя режиссура видео (БГАИ) |
| [makecindy/cindy](https://github.com/makecindy/cindy) | 5.5k | Открытый AI-агент «из коробки» | Референс агентной архитектуры |
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | 21.5k | Universal SEO skill: 26 под-скиллов + 19 субагентов | **Маргинально** — продвижение портфолио, вдохновить структуру skills |
| [coollabsio/coolify](https://github.com/coollabsio/coolify) | 64.8k | Self-hosted PaaS (замена Vercel/Heroku), деплой статики и 360+ сервисов | **Возможно** — если захотим уйти с платных/лимитных хостингов booster/portal |
| [JetBrains/thinkrail](https://github.com/JetBrains/thinkrail) | 2.2k | Лёгкая IDE с агентами | Нет |
| [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | 115k | Multi-agent LLM-фреймворк для трейдинга | **Нет** — не наша тема, не цепляться |
| [pollen-robotics/microduck](https://github.com/pollen-robotics/microduck) | 12k | Робот-уточка | Нет |
| [Renhuai123/ziwei-doushu](https://github.com/Renhuai123/ziwei-doushu) | 8.1k | Астрология цзы-вэй | Нет |

## Выводы для нас

1. **Волна — «skills для coding-агентов».** hallmark (дизайн), security-audit-skill, claude-seo — всё это «скиллы», которые вставляются в Claude Code/Cursor/Codex. Прямо наш формат `.opencode/skills/`. Стоит подсмотреть паттерны: как они структурируют knowledge внутри skill.
2. **Anti-AI-slop дизайн** — два репо в топе (hallmark + impeccable) про то, чтобы ИИ-агенты не выдавали безликий дизайн. Совпадает с нашей имаккулат-скиллой — значит направление верное, можно сверить подход.
3. **Локальная генерация голоса (VoiceStudio)** — дешевеет озвучка. Потенциал для озвучки курсов и видео без подписок.
4. **Что НЕ брать:** TradingAgents (не наша сфера), роботы/астрология (шум), thinkrail (лишняя IDE).

### Кандидаты в бэклог (на твоё решение)
- Сверить наш `impeccable` с hallmark/impeccable — забрать недостающие приёмы (🟡).
- VoiceStudio — тест озвучки для курса/видео (🟡, лёгкий эксперимент).