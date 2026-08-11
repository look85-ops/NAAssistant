# АОС — {{PROGRAM}}, {{WAVE_LABEL}}

**Дата анализа:** {{DATE}}
**Волна:** {{WAVE_LABEL}}
**Выгрузка:** `{{SOURCE_FILE}}`
**Анкет:** {{N_TOTAL}} (из {{N_RAW}} строк выгрузки)
**Целевая аудитория:** {{AUDIENCE}}

**Качество данных:** `{{VERDICT}}` — {{VERDICT_REASON}}

---

## 1. Ключевые цифры

| Метрика | Среднее | NPS | Распределение (Сторонники / Нейтр / Критики) |
|---|---|---|---|
| **{{TOP_QUESTION}}** | {{TOP_MEAN}} | {{TOP_NPS}}% | {{TOP_SEG}} |
| **{{ORG_QUESTION}}** | {{ORG_MEAN}} | {{ORG_NPS}}% | {{ORG_SEG}} |
| **Средний балл по форматам** | {{AVG_MEAN}} | — | — |

**Целевой NPS программы: {{TARGET_NPS}} → Уровень NPS волны: {{WAVE_NPS}}%**

### Рейтинг сессий (средний балл)

| # | Сессия | Средний балл |
|---|---|---|
| 1 | {{SESSION}} | **{{SCORE}}** |
| 2 | {{SESSION}} | **{{SCORE}}** |
| 3 | {{SESSION}} | **{{SCORE}}** |
| ... | ... | ... |

**Самый низкий балл — {{MIN_SESSION}} ({{MIN_SCORE}}).** {{MIN_NOTE}}

---

## 2. Ожидания участников

| Категория | Кол-во | Доля |
|---|---|---|
| Превзошла ожидания | {{N_ABOVE}} | {{PCT_ABOVE}}% |
| Соответствовало ожиданиям | {{N_MATCH}} | {{PCT_MATCH}}% |
| Не соответствовало | {{N_BELOW}} | {{PCT_BELOW}}% |

**Вывод:** {{EXPECTATION_NOTE}}

---

## 3. Аномалии и качество данных

{{ANOMALIES}} <!-- список: тип, вопрос, деталь, severity -->

---

## 4. Топ-3 вывода

### 4.1. {{TOP1_TITLE}}
{{TOP1_BODY}}

### 4.2. {{TOP2_TITLE}}
{{TOP2_BODY}}

### 4.3. {{TOP3_TITLE}}
{{TOP3_BODY}}

---

## 5. Цитаты

> {{QUOTE}} — {{AUTHOR}}

> {{QUOTE}} — {{AUTHOR}}

---

## 6. Три правки

### Правка 1: {{EDIT1_TITLE}}
**Проблема:** {{EDIT1_PROBLEM}}
**Действие:** {{EDIT1_ACTION}}
**Метрика:** {{EDIT1_METRIC}}

### Правка 2: {{EDIT2_TITLE}}
**Проблема:** {{EDIT2_PROBLEM}}
**Действие:** {{EDIT2_ACTION}}
**Метрика:** {{EDIT2_METRIC}}

### Правка 3: {{EDIT3_TITLE}}
**Проблема:** {{EDIT3_PROBLEM}}
**Действие:** {{EDIT3_ACTION}}
**Метрика:** {{EDIT3_METRIC}}

---

## 7. A/B-гипотеза

**Название:** {{AB_NAME}}

**Гипотеза:** {{AB_HYPOTHESIS}}

**Дизайн:**
- Контроль: {{AB_CONTROL}}
- Вариант: {{AB_TREATMENT}}
- Рандомизация: {{AB_RANDOMIZATION}}
- Валидация прокси: {{AB_METRICS}}

**Ожидаемый эффект:** {{AB_EXPECTED}}

---

## 8. Инсайты для knowledge/

1. {{INSIGHT_1}}
2. {{INSIGHT_2}}
3. {{INSIGHT_3}}