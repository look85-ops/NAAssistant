# Эталон урока — дизайн-система и структура (09.2026)

**Эталонный файл:** `portal/course/module-01-technical-minimum/lesson-01-terminal.html`

## CSS-переменные
--olive #474a1a, --terracotta #b05a2e, --muted #737366, --border #e0ded8, --surface #f4f4ef, --ink #2b2b1a, --light #fafaf8

## Структура страницы (порядок)

1. **Header** — fixed, rgba(255,255,255,0.97), blur, logo + навигация
2. **Hero** — surface фон, olive-полоса 4px снизу, водяной знак, mod-tag, h1, meta (без времени), outcomes (вертикальный список, без заголовка)
3. **Hero-cta** — отдельный блок МЕЖДУ hero и первым разделом, внутри .content, surface фон + olive border + чип «➤ Прямо сейчас»
4. **Разделы** — section-hd с data-num (водяной знак 220px), h2 БЕЗ номеров («Зачем это L&D-специалисту», «Что такое командная строка»)
5. **Метафоры** — .metaphor, border-left 3px olive, italic, формат «Метафора. ...»
6. **Инсайты** — .insight, border-left 4px olive
7. **Pull-quote** — border-left 3px terracotta, крупный italic
8. **Margin-note** — inline-блок с surface-фоном, border-left 3px olive (без float)
9. **Micro-prac** — light фон, чип «➤ Попробуйте»
10. **Interim** — surface фон, uppercase h3 «Промежуточный итог»
11. **Episode** — full-width olive, padding 80px, водяной знак 380px
12. **Geo-div** — линия + terracotta квадрат, margin 80px 0
13. **Шпаргалка** — .cheatsheet с чипом «Шпаргалка», ОДИН блок, таблицы
14. **Практика** — full-width surface, details/accordion + done-btn + localStorage
15. **Чек-лист** — .insight
16. **Артефакт урока** — структура папок/файлов
17. **Челлендж на завтра** — .open-loop, dashed terracotta
18. **Что дальше** — «На следующем уроке»
19. **Навигация** — .nav-bottom, ← назад / вперёд →, к оглавлению
20. **Footer**

## Что УДАЛЕНО
- TOC (содержание)
- Рефлексия (.reflect)
- «После урока вы сможете» заголовок (остался только список)
- Время в meta
- «Неделя» → «Урок»
- Номера в h2
- Дубль шпаргалки (#cheatsheet-keep)
- border-left на hero (заменён на surface-фон + olive-полоса снизу)

## CSS-правила
- body: font-weight 400, overflow-x:hidden
- .content p: text-wrap:pretty, hyphens:auto, orphans:2, widows:2
- Таблицы: thead th uppercase, olive bottom-border 2px, zebra
- Code: olive left-border 2px, monospace
- НЕТ: border-radius (кроме .toc .dot — не используется), теней, градиентов, justify
- @media 768px, prefers-reduced-motion

## JS
- Progress bar по скроллу
- Done-btn восстановление из localStorage (ключи ex1-exN)