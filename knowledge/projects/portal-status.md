# Статус портала (2026-09-15)

## Готово
- **Главная** `portal/index.html` — hero, манифест (терракотовый full-width), фото, 3 карточки продуктов (тёмная оливковая / светлая с акцентом / призрачная), футер
- **Курс** `portal/course/index.html` — hero, 4 модуля (М1-М3 с ссылками на уроки, М4 «бонусный модуль · отдельная оплата»)
- **9 уроков (старая вёрстка)** — автоматическая конвертация MD→HTML, плоский текст
- **1 урок (новая вёрстка)** `portal/course/module-02-ai-from-prompt-to-product/lesson-01-llm-internals.html` — дизайн с ритмом: прогресс-бар, водяной знак, мини-TOC, метафоры, практика full-width surface, шпаргалка, геометрические разделители, навигация
- **Дизайн-токены** `portal/styles/tokens.css`
- **PRODUCT.md** в корне

## Не готово
- **Блог** `portal/blog/` — F-086
- **Интеграция Бустера** — F-087
- **Тиражирование нового дизайна уроков** — ждёт правок Наташи по пилотному уроку
- **Хостинг / домен** — не решён

## Структура файлов
```
portal/
├── index.html
├── styles/tokens.css
├── styles/base.css
├── hero-final.html
├── hero-variants.html
├── course/
│   ├── index.html
│   ├── module-01-technical-minimum/
│   │   ├── lesson-01-terminal.html  (старая)
│   │   ├── lesson-02-git.html       (старая)
│   │   └── lesson-03-api.html       (старая)
│   ├── module-02-ai-from-prompt-to-product/
│   │   ├── lesson-01-llm-internals.html (★ НОВАЯ)
│   │   ├── lesson-02-rag.html       (старая)
│   │   ├── lesson-03-agents.html    (старая)
│   │   └── lesson-04-fine-tuning.html (старая)
│   └── module-03-ai-strategy-and-roi/
│       ├── lesson-01-ai-readiness.html (старая)
│       └── lesson-02-roi-roadmap.html  (старая)
└── blog/  (пусто)
```

## Платное
- М4 «Позиционирование и портфолио» — 100% платный
- Гайд по AI-агентам (305 строк) — платное дополнение к М2
- Глубокие протоколы Бустера — платный блок (F-006)