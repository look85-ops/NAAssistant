# GitHub Trending — 01.10.2026

Источники: GitHub API (новые репо сентября 2026), github.com/topics/ai-agents.

## Главная волна: JEV-модели и «быстрые решения»

Вместо дорогого LLM для каждого шага — одна быстрая модель выдаёт yes/no/score за один проход. Экономия токенов 50–95%.

| Репо | ★ | Что |
|---|---|---|
| [laya](https://github.com/NandhaKishorM/laya) | 29.5k | System 1 decision engine: typed choices, score, yes/no за один forward-pass, 100+ языков |
| [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast) | 21.6k | Самый быстрый и дешёвый web-агент |
| [jaredpalmer/kev](https://github.com/jaredpalmer/kev) | 8.1k | Jev-модели на Qwen3.5/3.8, можно запускать локально |
| [tamaratran/fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) | 7.2k | Плагин Claude Code: сжатие контекста через Jev вместо саммари |

## Agent Harness Engineering

Тренд: не писать агентов с нуля, а собирать harness (упряжь) — скиллы + память + инстинкты + песочницы.

| Репо | ★ | Что | Пригодится? |
|---|---|---|---|
| [ECC](https://github.com/affaan-m/ECC) | 270k | Harness: skills, instincts, memory для Claude Code/Codex/Cursor | Идеи для нашего AGENTS.md + субагентов |
| [hermes-agent](https://github.com/NousResearch/hermes-agent) | 250k | Агент, который растёт с тобой | Референс самообучающегося агента |
| [ponytail](https://github.com/DietrichGebert/ponytail) | 150k | «Думай как самый ленивый сеньор» — меньше кода | Идеология совпадает с нашим «убирай лишнее» |
| [claude-mem](https://github.com/thedotmack/claude-mem) | 95.1k | Постоянная память между сессиями для Claude Code/OpenCode/Gemini | **Прямой кандидат:** решает нашу задачу памяти между сессиями |
| [ruflo](https://github.com/ruvnet/ruflo) | 73.6k | Agent harness, multi-player swarms, федерация | Референс архитектуры субагентов |
| [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 76.3k | Коллекция скиллов для Claude Code | Подсмотреть паттерны для `.opencode/skills/` |

## Инструменты и платформы

| Репо | ★ | Что | Пригодится? |
|---|---|---|---|
| [OmniRoute](https://github.com/diegosouzapw/OmniRoute) | 71.9k | Бесплатный AI-шлюз: 1 endpoint → 359 провайдеров, 150+ бесплатных | Пробовать модели без отдельных подписок |
| [orca](https://github.com/stablyai/orca) | 82.7k | IDE для параллельного запуска агентов | Если дойдём до «роя» агентов |
| [m3e-canvas](https://github.com/lnkiai/m3e-canvas) | 8.5k | Дизайн в браузере → промпт для AI-разработчика | Ускорение дизайна для portal/portfolio |
| [ZCode](https://github.com/zai-org/ZCode) | 7.2k | Z.ai coding agent harness | Референс архитектуры |
| [jev-chat-jarvis](https://github.com/jev-chat/jev-chat-jarvis) | 7.2k | Мобильный ассистент для чатов (QQ/X/Telegram) | Идея: AI-ассистент в мессенджере |

## Стабильные лидеры ai-agents

| Репо | ★ | Что |
|---|---|---|
| [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 241k | Всё — плагин. DSH-экосистема |
| [firecrawl](https://github.com/firecrawl/firecrawl) | 187k | Web data API для AI-агентов |
| [langchain](https://github.com/langchain-ai/langchain) | 147k | Платформа агентов |
| [graphify](https://github.com/Graphify-Labs/graphify) | 123k | Codebase → knowledge graph (аналог нашего Codebase Memory MCP) |
| [browser-use](https://github.com/browser-use/browser-use) | 117k | Агенты в браузере |
| [gemini-cli](https://github.com/google-gemini/gemini-cli) | 107k | Gemini в терминале |
| [deer-flow](https://github.com/bytedance/deer-flow) | 83.3k | SuperAgent на часы работы (ByteDance) |

## Выводы для нас

### Что взять
1. **claude-mem** — самый прямой кандидат: память между сессиями для OpenCode/Claude Code. Альтернатива нашему ручному progressive disclosure.
2. **fast-jev-compaction** — автоматическое сжатие контекста без потери смысла. Решит проблему распухания контекста в длинных сессиях.
3. **OmniRoute** — бесплатный доступ к 150+ моделям. Полезно для тестирования разных LLM.

### Что НЕ надо
- Не ставить тяжёлые серверные штуки (RAGFlow, LangChain) — наш файловый стек дешевле
- Не гнаться за multi-agent swarm'ами — сначала порядок в том, что есть
- ECC и ponytail — брать идеи, не запускать