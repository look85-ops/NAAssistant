# Code Quality Skill

Цель: единый интерфейс верификации кода перед коммитом/пушем.

## Philosophy

- Проверки должны быть **fast fail** — падают быстро и понятно.
- Один язык — один набор проверок (не все сразу).
- Результат = exit code + краткий summary.

## Языки и проверки

### Python

| Инструмент | Команда | Что проверяет |
|---|---|---|
| ruff | `ruff check .` | Стиль, ошибки |
| mypy | `mypy .` | Типы |
| pytest | `pytest .` | Тесты |

### JavaScript/TypeScript

| Инструмент | Команда | Что проверяет |
|---|---|---|
| eslint | `eslint .` | Стиль |
| tsc --noEmit | `tsc --noEmit` | Типы |
| vitest | `vitest run` | Тесты |

### HTML/CSS

| Инструмент | Команда | Что проверяет |
|---|---|---|
| html-validate | `html-validate .` | Валидность |
| stylelint | `stylelint .` | CSS стиль |

### Markdown

| Инструмент | Команда | Что проверяет |
|---|---|---|
| markdownlint | `markdownlint .` | Структура |

## Workflow

```
1. Detect language(s) in project
2. Run language-specific checks in parallel
3. Aggregate results
4. If any fail → block with summary
5. If all pass → allow proceed
```

## Fail Output Format

```
❌ LINT FAILED
 ruff: 3 errors (E501, E702)
 mypy: 1 error (missing type)

✓ All checks passed
```

## Decision Rules

- **1+ fail** → блок, не коммитить.
- **Warnings only** → разрешить, но предупредить.
- **Unknown language** → пропустить (не блокировать).

## Priority

1. Ruff/mypy для Python (основной стек Наташи)
2. ESLint/tsc для TS
3. Остальное — по необходимости

---

**Adoption**: используется в `/finish-task` и перед каждым коммитом.