# /quality-gate — предкоммитный чеклист артефактов

Расширенная версия `/verify`. verify проверяет только линтеры. quality-gate добавляет проверку Critical Assets и контентных артефактов.

## Когда вызывать

- Перед коммитом в main
- Перед `/finish-task`, если задача трогала Critical Assets
- Когда задача меняла > 3 файлов

## Что проверяет

### 1. Линтеры и типы
{то же что /verify — ruff, mypy, eslint, tsc}

### 2. Critical Assets (5 артефактов из AGENTS.md)
- [ ] portfolio/index.html — открывается, нет битых ссылок
- [ ] methodist-booster/ — не сломан
- [ ] portfolio/message-accidental_1.html — цел
- [ ] garden/ — деплой работает (если трогали)
- [ ] amalgama/ — цикл не нарушен (если трогали)

### 3. Связанные артефакты (автоопределение)
- Если трогали `docs/BACKLOG.md` → проверить, что нет дубликатов ID
- Если трогали `knowledge/` → проверить, что index.md актуален
- Если трогали `.opencode/agent/` или `.opencode/command/` → проверить консистентность с AGENTS.md
- Если трогали `career/` → проверить резюме/профиль на битые ссылки

### 4. Git hygiene
- [ ] Нет staged secrets (.env, ключи, пароли)
- [ ] Нет staged мусора (.DS_Store, tmp, node_modules)
- [ ] Коммит-сообщение соответствует формату

## Вывод

Чеклист с ✅/❌ по каждому пункту. Если есть ❌ — блок коммита, предложение фикса.

## Аргументы

- `/quality-gate` — все проверки
- `/quality-gate --critical-only` — только Critical Assets + git hygiene
- `/quality-gate --skip-lint` — пропустить линтеры (если уже прошли /verify)
