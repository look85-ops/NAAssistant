# Playwright + MS Edge в opencode

## Конфиг (opencode.json)
```json
{
  "mcp": {
    "playwright": {
      "type": "local",
      "command": ["npx.cmd", "-y", "@playwright/mcp@latest", "--browser", "msedge"],
      "enabled": true
    }
  }
}
```

## Важно
- Используется `npx.cmd` (не `npx`) — обход PowerShell Execution Policy
- `--browser msedge` — запускает системный MS Edge, не Chromium
- Профиль хранится в `%USERPROFILE%\AppData\Local\ms-playwright\mcp-msedge-{hash}` — сохраняется между сессиями
- `--user-data-dir` к основному профилю Edge не работает: Edge выдаёт «неподдерживаемый флаг командной строки»
- `--extension` не работает: playwright-mcp ищет расширение только в Chrome, не в Edge
- Перезапуск opencode обязателен после правки конфига