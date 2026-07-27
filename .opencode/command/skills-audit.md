## `/skills-audit`

Список установленных skills (project/global) с подсчётом строк и файлов, чтобы определить кандидатов на сжатие и устранение пересечений.

### Требования
- Windows PowerShell доступен.
- Опционально: переменная окружения `SKILLS_GLOBAL_DIR` — путь к глобальным skills.

### Запуск

В корне репозитория:

```
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/skills-audit.ps1
```

JSON-вывод:

```
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/skills-audit.ps1 -AsJson
```

### Вывод
- Таблица по проектным и глобальным skills: имя, путь, количество файлов, суммарные строки.
- Подсказка: пересмотреть самые «тяжёлые» skills на предмет краткости, пересечений и токен-эффективности.

### Следующие шаги
- Для фиксации решений используй формат: краткое описание проблемы + принятое решение в `logs/decisions.md`.
