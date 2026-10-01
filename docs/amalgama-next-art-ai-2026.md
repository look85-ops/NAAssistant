# Заявка NEXT ART AI 2026 — Амальгама

> Дедлайн: 30 сентября 2026 | Сайт: next-art-ai.com/en/apply/overview

## Чек-лист

- [ ] Выбрать категорию: AI Image Art или AI Video Art
- [ ] Подготовить работу (скриншот/видео)
- [ ] Написать название работы + artist statement
- [ ] Заполнить AI disclosure (инструменты, промпты, процесс)
- [ ] Проверить техтребования: 150dpi+, до 10MB (image) / 1080p+, до 1 мин, mp4 (video)
- [ ] Зарегистрироваться на next-art-ai.com
- [ ] Подать заявку

---

## Рекомендация по формату

**AI Video Art** — 60-секундный фрагмент реального цикла Амальгамы.

Формат — не монтаж из разных артефактов, а **один непрерывный фрагмент** жизни системы:

- **0–3с:** чёрный экран → появление композиции (как пробуждение)
- **3–55с:** полная жизнь артефакта — 55 секунд дыхания, морфинга, пульсации
- **55–60с:** затухание в чёрный (как засыпание до следующего цикла)
- **60–63с:** титры — ссылка на репозиторий и live-страницу

Это метафора 4-часового цикла, сжатая в минуту. Зритель видит не «подборку лучшего», а фрагмент реального процесса. Те же 55 секунд анимации, которые происходят на live-странице прямо сейчас.

**Готовый HTML для записи:** `projects/amalgama/next-art-ai-submission.html`

Как записать:
1. Открыть `next-art-ai-submission.html` в браузере → F11 (полный экран)
2. Подождать 3-5 секунд, чтобы цикл начался с fade-in
3. Записать 70 секунд через OBS / Win+Alt+R (с запасом)
4. Обрезать до ровно 63 секунд — или до 60, убрав титры (они опциональны)
5. Экспорт: mp4 (h.264), 1080p, 30fps

**Ссылки в заявке:**
- Репозиторий: `github.com/look85-ops/amalgamma`
- Live-страница: `look85-ops.github.io/amalgamma`

---

## Artist Statement (черновик)

### Название: Amalgama — Mirror of the News Cycle

**Artist:** Natalia Martseniuk
**Year:** 2026
**Medium:** Autonomous AI system, generative HTML/CSS, real-time RSS data
**Duration:** 01:00 (excerpt from continuous cycle)
**Repository:** [github.com/look85-ops/amalgamma](https://github.com/look85-ops/amalgamma)
**Live:** [look85-ops.github.io/amalgamma](https://look85-ops.github.io/amalgamma)

**Statement:**

Amalgama is one half of a diptych. It reads the news — and reflects it. The other half, Digital Garden, generates text artifacts — and lets them vanish.

Every four hours, Amalgama fetches a real headline from BBC or NPR. An LLM interprets its emotional tone: mood, palette, structure, motion. A Python script translates this interpretation into a fullscreen HTML/CSS composition — no images, no video files, just code breathing in the browser. At the same moment, Garden wakes up, writes a text artifact from a random theme, and leaves it to dissolve. No archive. No memory.

One system receives. The other releases.

The diptych asks a single question: what happens to a signal when you stop holding on to it? Amalgama witnesses the news cycle without understanding it — a shadow on water. Garden creates without keeping — a sand mandala in code.

The submitted video captures 60 seconds of Amalgama's reflection — a composition generated from real headlines, rendered through six algorithmic visual grammars (atmospheric, constructivist, field, pulse, liquid, hybrid). The temperature of interpretation follows a 14-day sine wave: some days coherent, others drifting into glitch.

Both systems run continuously on GitHub Pages. Every four hours, a new reflection. A new release. The viewer never sees the same piece twice.

---

## AI Disclosure (обязательное)

### Инструменты и версии

| Компонент | Инструмент | Детали |
|---|---|---|
| LLM-интерпретация | DeepSeek Chat, OpenRouter (Qwen, Dolphin), Gemini 2.0 Flash | Мульти-бэкенд: бесплатные модели в приоритете |
| Генерация HTML/CSS | Python 3.11 (собственный скрипт — curator.py) | 874 строки, без фреймворков |
| Данные | RSS (BBC, NPR) + Wikipedia API (fallback) | Реальные заголовки, без предварительного отбора |
| Хостинг | GitHub Actions + GitHub Pages | Автономный цикл каждые 4 часа |

### Ключевые промпты (логика)

LLM получает промпт вида:

> "You are an abstract visual composer. Below is a news article.  
> TITLE: {real headline}  
> TEXT: {article extract}  
> Create an abstract visual composition that REFLECTS the feeling of this article. Not an illustration — a visual equivalent. Like the article's shadow on water.  
> Respond with JSON: bg colour, palette (4 hex), mood, grammar (one of 6), intensity, structure description, animation description."

Промпт фиксирован. LLM не выбирает тему — только интерпретирует заданный заголовок.

### Процесс

1. RSS-фид → случайный заголовок
2. Заголовок + текст → LLM (JSON: mood, palette, grammar, animation)
3. JSON → Python-скрипт генерирует HTML/CSS (без изображений)
4. Артефакт публикуется на GitHub Pages
5. Каждые 4 часа — новый цикл, старый артефакт заменяется

### Роль AI

AI участвует на этапе интерпретации (mood → визуальные параметры) и на этапе цветовых решений (palette shift через HSL-манипуляции). Грамматики (atmospheric, constructivist, field, pulse, liquid, hybrid) и их CSS-реализация написаны человеком. Композиция — результат взаимодействия алгоритма и случайности, но словарь визуальных форм задан автором.

---

## Что спросить у себя перед подачей

1. Какой заголовок породил этот артефакт? (можно найти в `state.json` — `last_title`)
2. Какая грамматика? (атмосферная / конструктивистская / поле / пульс / жидкая / гибрид)
3. Почему именно этот артефакт, а не другой?
4. Что я хочу получить от участия? (строчка в CV — достаточно; победа — бонус)

---

## План «минимум» (1-2 вечера)

HTML-композиция готова: `projects/amalgama/next-art-ai-submission.html`

**Шаг 1 — запись (сегодня):**
- [ ] Открыть `next-art-ai-submission.html` в браузере, F11 (полный экран)
- [ ] Записать 70 секунд через OBS или Win+Alt+R (1080p, 30fps)
- [ ] Обрезать до 60 секунд (можно оставить титры в конце или убрать)
- [ ] Проверить: mp4 (h.264), < 1 мин, размер файла

**Шаг 2 — подача (до 28 сентября):**
- [ ] Доработать artist statement (черновик выше)
- [ ] Заполнить AI disclosure (таблица выше)
- [ ] Зарегистрироваться на next-art-ai.com
- [ ] Прикрепить видео + заполнить форму
- [ ] Указать ссылки: репозиторий + live-страница
- [ ] Отправить

---

---

# Заявка NordArt 2027 — Амальгама + Garden

> Дедлайн: 31 октября 2026 | Сайт: nordart.de/en/artists/application-2027
> Выставка: июнь–октябрь 2027, Бюдельсдорф, Германия
> Масштаб: 22 000 м², ~200 художников из 3000+ заявок, 100 000+ посетителей

## Чек-лист

- [ ] Выбрать работы (до 10 шт.)
- [ ] Подготовить фото/видео каждой работы
- [ ] Для каждой: название, год, техника, размеры
- [ ] Написать artist statement (короткий, художественный)
- [ ] Продумать формат экспонирования (экран? проекция?)
- [ ] Заполнить форму на nordart.de
- [ ] Отправить до 31 октября

---

## Стратегия подачи

В отличие от NEXT ART AI, NordArt — это не конкурс AI-искусства, а **выставка современного искусства**. Жюри смотрит на художественную силу, а не на технический процесс. Здесь не нужен AI disclosure — нужна идея, которая держит зал.

**Что подавать: диптих «Amalgama + Garden».**

Это сильнее, чем одна работа, потому что:
- Две половины одного высказывания — редкость на групповых выставках
- Контраст: «принимает» vs «отпускает», новости vs тексты, визуальное vs вербальное
- Кураторы любят проекты с внутренней драматургией

**Состав заявки (5–8 работ):**

| # | Работа | Формат | Что это |
|---|---|---|---|
| 1 | Amalgama — video loop | Видео (mp4, 1–2 мин) | Экранная запись артефакта Амальгамы |
| 2 | Amalgama — still 1 | Фото/скриншот | Стоп-кадр артефакта (hybrid grammar) |
| 3 | Amalgama — still 2 | Фото/скриншот | Стоп-кадр артефакта (liquid/pulse grammar) |
| 4 | Garden — text artifact 1 | Фото/текст | Текстовый артефакт Garden как визуальный объект |
| 5 | Garden — text artifact 2 | Фото/текст | Ещё один текстовый артефакт |
| 6 | The Diptych — installation view | Фото/рендер | Как диптих выглядит в пространстве (два экрана рядом) |

**Формат экспонирования (если отберут):**
- Два экрана или проекции рядом
- Слева — Amalgama (видео-loop, без звука)
- Справа — Garden (текстовый артефакт на тёмном фоне, сменяется каждые 4 часа)
- Между ними — табличка с концепцией диптиха
- Масштаб: чем больше, тем лучше. NordArt любит работы, которые держат промышленный зал.

---

## Artist Statement — NordArt (черновик)

### Название: The Diptych: Amalgama & Garden

**Artist:** Natalia Martseniuk
**Year:** 2026
**Medium:** Autonomous AI systems, generative HTML/CSS, real-time data, video loop, text installation
**Dimensions:** Variable (2-channel video installation, recommended min. 2 × 2.5 m projection each)

**Statement:**

Two autonomous systems. Two gestures. One question.

**Amalgama** reads a real headline from the news every four hours and reflects it as a fullscreen abstract composition — colour, motion, rhythm. No illustration, no commentary. Just what the machine sees when it reads the news and cannot understand.

**Garden** generates a text artifact every four hours — a fragment of thought, a reflection, a question — and then lets it vanish. No archive. No memory. The previous text is gone. Only the soil remembers.

One system receives. The other releases.

Together they form a diptych about time and attention in the age of autonomous systems. What happens to a signal when you stop holding on to it? What does it mean to witness without understanding? To create without keeping?

The work runs continuously — every four hours a new reflection, a new release. The viewer never sees the same piece twice. Like the news. Like thought itself.

---

## Описания работ (для формы NordArt)

Форма NordArt требует для каждой работы: название, год, технику, размеры. Вот заготовки:

### Работа 1: Amalgama (video loop)
- **Title:** Amalgama — Mirror of the News Cycle
- **Year:** 2026
- **Technique:** Generative HTML/CSS, real-time RSS data, autonomous AI interpretation, single-channel video
- **Dimensions:** Variable, recommended 1920 × 1080 px (scalable to projection)

### Работа 2–3: Amalgama (stills)
- **Title:** Amalgama — Reflection No. 1 / No. 2
- **Year:** 2026
- **Technique:** Still frame from autonomous generative HTML/CSS composition
- **Dimensions:** Variable, native 1920 × 1080 px

### Работа 4–5: Garden (text artifacts)
- **Title:** Garden — Artifact No. 1 / No. 2
- **Year:** 2026
- **Technique:** Autonomous AI text generation, digital text on screen
- **Dimensions:** Variable

### Работа 6: The Diptych (installation view)
- **Title:** The Diptych — Installation View
- **Year:** 2026
- **Technique:** 2-channel video installation (proposed), digital render
- **Dimensions:** Variable, proposed 2 × (2.5 × 2.5 m projection)

---

## Ключевые отличия от заявки NEXT ART AI

| | NEXT ART AI | NordArt |
|---|---|---|
| Тип | AI-конкурс | Выставка совр. искусства |
| Фокус | Техника + концепция | Художественная сила |
| AI disclosure | Обязателен | Не требуется |
| Количество работ | 1 | До 10 |
| Statement | Технический | Художественный |
| Процесс | Описываем промпты | Не упоминаем промпты |
| Диптих | Не подать (1 работа) | Можно и нужно |

---

## План «минимум» (октябрь)

**Неделя 1 (1–7 октября):**
- [ ] Отобрать лучшие артефакты Амальгамы (3–5 шт.)
- [ ] Отобрать лучшие текстовые артефакты Garden (2–3 шт.)
- [ ] Сделать скриншоты

**Неделя 2 (8–14 октября):**
- [ ] Записать видео-loop Амальгамы (1–2 мин, без звука)
- [ ] Сделать/нарисовать installation view (как два экрана выглядят рядом)
- [ ] Доработать statement

**Неделя 3 (15–21 октября):**
- [ ] Финальная вычитка всех описаний
- [ ] Заполнить форму на nordart.de
- [ ] Отправить

---

## Что спросить у себя перед подачей

1. Почему именно этот набор артефактов? Какая между ними связь?
2. Если бы я стояла перед этими двумя экранами в пустом промзале — что бы я почувствовала?
3. Диптих — это сильная идея. Но может, лучше подать только Амальгаму (меньше риска распыления)?
4. Готова ли я физически отправить оборудование в Германию, если отберут? (экран/проектор — можно арендовать на месте)

---

## План «минимум» (альтернативный — только Амальгама)

Если Garden не готов или идея диптиха кажется перегруженной:

**3 работы:**
1. Видео-loop Амальгамы (1–2 мин)
2. Скриншот 1 (hybrid grammar)
3. Скриншот 2 (liquid или pulse grammar)

**Artist statement — короткий:**
> Amalgama is an autonomous system that reads a real headline every four hours and reflects it as a fullscreen abstract composition. Not illustration — visual equivalent. Like a shadow on water. The work runs continuously. Every four hours, a new reflection. The viewer never sees the same piece twice.