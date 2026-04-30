## `/pr-summary`

Краткое саммари pull request с использованием GitHub CLI и динамической инъекции контекста.

Основано на стандарте `docs/skills/DYNAMIC_CONTEXT.md`. Безопасность — см. `docs/skills/SHELL_GUARDS.md`.

### Вход
- URL PR или номер PR в текущем репозитории.

### Требования
- Установлен и авторизован GitHub CLI: `gh auth login`
- Включено выполнение `!<command>` (флаг `disableSkillShellExecution` должен быть выключен)

### Шаблон промпта (инъекция)

```
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context

- PR diff: `!gh pr diff <PR>`
- PR comments: `!gh pr view <PR> --comments`
- Changed files: `!gh pr diff <PR> --name-only`

## Your task

Summarize this pull request:
- Outline the scope and intent of changes
- Highlight risky areas and breaking changes
- Note tests/docs updates and gaps
- Provide a brief, actionable changelog
```

Где `<PR>` — номер или URL. При необходимости добавь флаг `--repo <owner/repo>`.

### Безопасность
- Разрешены только `gh pr diff/view` и опции чтения.
- Вывод ограничивается по размеру и может быть обрезан.
- Секреты маскируются по шаблонам.

### Пример запуска
`/pr-summary 123`
или
`/pr-summary https://github.com/owner/repo/pull/123`
