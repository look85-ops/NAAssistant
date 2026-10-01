---
type: source
title: Внешние источники для дайджеста и исследований
description: "Референсные репозитории и инструменты для дайджеста и multi-source research"
tags: [digest, research, sources, last30days]
timestamp: 2026-07-10
---

# Внешние источники

## last30days-skill

**Ссылка:** https://github.com/mvanhorn/last30days-skill
**Версия:** v3.11.1 (51K ★, июль 2026)
**Автор:** Matt Van Horn (@mvanhorn)

**Что даёт:** AI-agent skill для multi-source исследования — собирает посты и обсуждения с Reddit, X, YouTube, TikTok, HN, Polymarket, GitHub и веба за последние 30 дней, синтезирует привязанный к источникам саммари.

**Ключевые механики, взятые в проект:**

| Механика | Применение |
|---|---|
| Evidence clustering | Группировка фактов по темам + score + source diversity — в system prompt дайджеста |
| Signal-weighted ranking | Practitioner > Expert > Mention — для рекомендаций |
| Pre-flight checklist (10 параметров) | `docs/process/pre-flight-template.md` |
| Keyword trap detection (5 классов) | Прежде чем запустить поиск — проверь топик |
| Category-peer expansion | Для продукта — добавить 2-3 соседних сабреддита |
| Community voice weaving (LAW 9) | Вплести Reddit/X/Polymarket цитаты в нарратив |
| Output contract (10 LAWs) | `docs/process/output-contract-template.md` |
| Footer pass-through | Блок метрик в конце дайджеста |
| Stale-clone protection | Step 0: проверь, не устарел ли SKILL.md |
| Platform-aware citation (LAW 8) | Ссылки по-разному для Claude Code vs GitHub Pages |

**Паттерны, которые стоит пересматривать:** pre-flight чеклист перед каждой research-командой, output contract для каждого вывода, self-check перед отправкой.
