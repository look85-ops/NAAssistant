# Amalgama — заявка на 2nd Aion Digital Art Prize (2026–2027)

> Дедлайн: 1 марта 2027, 23:59 GMT. Онлайн, worldwide, любой возраст. Взнос ¥3 000 (~$19). Язык подачи — английский. Подача: ссылка на видео (Google Drive/YouTube/Vimeo) + описание работы через форму Ise-Shima Art Company.

---

## Artist statement

Amalgama is a witness without memory.

Every four hours it reads a real headline from the BBC or NPR, pulls that one signal out of the news stream, and answers it — not with an illustration, but with a non-figurative composition written directly in HTML and CSS. A state, not a picture. The previous reflection disappears; only the current one exists.

The piece stands between two facts. The machine reads the world and registers its pressure, yet it does not understand what it reads. That gap — reading without comprehending — is the work itself. Amalgama does not make sense of the news. It witnesses it, once, and lets it go.

I am the author of the work. The idea, the concept of the machine-as-witness, and the structure of the system are mine — they are the work's core. I set the process in motion and then observe and study what it produces. The machine's autonomous cycles are the work itself: it takes headlines at random and answers each one on its own, fully responsible for the result. My assistant writes the code that carries the idea out.

## Work statement (for the submission)

An autonomous work, presented as a live web page with a video documentation.

Over 200 cycles and running, Amalgama has been reading the news every four hours. Each cycle produces a fullscreen composition in a browser: rhythm, silence, scale and materiality, with a quiet procedural ambient layer. There is no archive shown to the viewer — only the current reflection exists. What you open is always one moment, already on its way to being replaced.

The medium is code itself: the LLM writes the composition directly into the page. No image model, no fixed template. The submitted video shows four consecutive cycles, cross-faded, so the viewer sees not "the best of" but the process — one reflection turning into the next.

---

## AI disclosure (обязательное по правилам Aion)

> Правило: "works made solely by AI are not accepted. If you use AI, explain how it was used."

### Что является авторским вкладом (человек)

- **Идея и концепт:** «машина-свидетель без памяти» — постановка вопроса «что машина видит, читая новости, и не понимая»; выбор назвать это свидетельствованием, а не иллюстрацией.
- **Архитектура системы:** двухфазный процесс (сначала текстовое осмысление — вес/ритм/состояние/тишина, затем перевод в композицию), ритм 4 часа, отсутствие архива для зрителя, «только текущая рефлексия существует».
- **Среда:** HTML/CSS как холст — выбор «код как краска» задан автором.

### Роль AI (инструмент)

- LLM выполняет **интерпретацию** (перевод заголовка в композицию) и **генерацию кода** (один `<div>` с инлайн-CSS).
- LLM **не выбирает тему** и **не определяет концепт** — он получает фиксированный заголовок от системы и фиксированные намерения от промпта.
- Всё остальное (скрипт `curator.py`, RSS-парсинг, публикация, звуковой слой) — написано человеком.

### Процесс (честная последовательность)

1. RSS (BBC/NPR) → случайный заголовок.
2. Фаза 1 — LLM пишет короткую текстовую рефлексию (вес/ритм/состояние/чего нет).
3. Фаза 2 — LLM переводит эту рефлексию в HTML/CSS-композицию.
4. Скрипт публикует на GitHub Pages; каждые 4 часа — новый цикл, старый заменяется.
5. Зритель не видит архива — только текущая рефлексия.

### Вывод для жюри (готовить в поле формы, коротко)

The work is AI-assisted, not AI-made: the concept ("machine-as-witness without memory") and the system design are the artist's. The artist set the idea in motion and then observes and studies the result; the machine is fully responsible for what it produces. There is no curatorial selection of headlines — the system takes them at random, and the model answers each one on its own.

---

## Поле формы «Briefly describe the artwork» (готовый текст)

Amalgama is a witness without memory. Every four hours it reads a real headline from the BBC or NPR, chosen at random, and answers it not with an illustration but with a non-figurative composition written directly in HTML and CSS. First the system reflects on the headline in words — its weight, its rhythm, its silence — then it turns that feeling into a fullscreen composition in the browser. The previous reflection disappears; only the current one exists. The machine reads the world and registers its pressure, yet it does not understand what it reads — that gap is the work itself. The concept and the system design are the artist's; the artist set the process in motion and now observes it. The machine takes headlines at random and is fully responsible for what it produces.

Video documentation: [LINK TO GOOGLE DRIVE]
Live work: https://look85-ops.github.io/amalgamma
Source and full description: https://github.com/look85-ops/amalgamma

---

## Описание работы для формы (название / год / техника / размеры)

- **Title:** Amalgama — a witness without memory
- **Artist:** Natalia Martseniuk
- **Year:** 2026
- **Technique:** Autonomous AI-assisted system, generative HTML/CSS, real-time RSS data, single-channel video documentation
- **Dimensions:** Variable; live web page (any screen), video 1920 × 1080
- **Links:** live `look85-ops.github.io/amalgamma` · source `github.com/look85-ops/amalgamma`

---

## Чек-лист подачи

- [x] Artist statement + work statement
- [x] AI disclosure (авторский вклад vs инструмент)
- [x] Видео-документация: `projects/amalgama/aion-submission-2026-11-11.mp4` (4 цикла, кросс-фейд)
- [x] Живой URL + репозиторий
- [ ] Загрузить видео на Google Drive / YouTube / Vimeo (публичная ссылка для жюри)
- [ ] Отправить форму через Ise-Shima Art Company (`en.iseshimaart.com/digitalartprize`)
- [ ] Оплатить взнос ¥3 000 (card/PayPal)
- [ ] Держать ссылку доступной жюри до 5 мая 2027

**План подачи: 21–23 ноября 2026** (Наташа в Минске, будет возможность оплатить взнос). Дедлайн — 1 марта 2027, так что запас есть, но подаём заранее.

## Что помнить

- **Не "solely AI"**: в поле описания обязательно фраза про авторство (см. выше «AI-assisted, not AI-made»).
- **Ссылка аудио**: амбиент-слой в видео идёт по клику — если в записи звук есть, ок; если нет, не проблема (video может быть без звука).
- **Ownership**: copyright остаётся у автора; репо/live-URL, введённые в форму, будут опубликованы при награде — оставить или убрать на твоё усмотрение.
