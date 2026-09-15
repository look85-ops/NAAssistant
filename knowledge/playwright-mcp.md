# Playwright MCP — браузерный инструмент для opencode

## Что это
Локальный headless-браузер (Chromium) через MCP-сервер `@playwright/mcp` от Microsoft. Позволяет ассистенту открывать страницы (включая JS-сайты как hh.ru), читать контент, заполнять формы, делать скриншоты.

## Как установлено (2026-09-08)
- `npm install -g @playwright/mcp` — версия из npm registry
- `npx playwright install chromium` — Chromium v1243 (npm/Playwright)
- `pip install playwright` + `python -m playwright install chromium` — Chromium v1234 (Python/Playwright)
- **Важно:** npm и Python используют разные версии Chromium в `%LOCALAPPDATA%\ms-playwright\`. Обе установлены для надёжности.

## Конфигурация в opencode
В `~/.config/opencode/opencode.jsonc` → секция `mcp`:

```jsonc
"playwright": {
  "type": "local",
  "command": ["C:/Users/marcenuk/AppData/Roaming/npm/playwright-mcp.cmd", "--headless", "--browser", "chromium", "--caps", "vision", "--isolated"],
  "enabled": true
}
```

Аргументы:
- `--headless` — без GUI (экономия памяти)
- `--browser chromium` — свой Chromium, не требует системного Chrome
- `--caps vision` — поддержка скриншотов
- `--isolated` — сессия в памяти, не пишет на диск

## Smoke-test пройден (2026-09-08)
- Статический сайт: `https://example.com` — заголовок "Example Domain", текст получен
- JS-сайт: `https://hh.ru` — полный контент (вакансии, компании, интерактивные элементы), `networkidle` отработал

## Грабли
- Кириллица в консоли PowerShell ломает вывод. Пиши результат в UTF-8 файл и читай его.
- `npx` / `npm` в PowerShell блокируются ExecutionPolicy — используй `cmd /c "npm ..."`.

## Сценарии использования
1. Research дайджестов «Радар L&D» и «Сигнал» — GitHub trending, HN, JS-новостные сайты
2. Мониторинг вакансий hh.ru / rabota.by — открыть, прочитать, возможно заполнить фильтры
3. Проверка портфолио/бустера — открыть в браузере
4. Скриншоты — через `--caps vision`
