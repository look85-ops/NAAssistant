# Бустер методиста — деплой и запуск

Этот пакет — статический (HTML/JS/CSS). Работает локально, на GitHub Pages и на Netlify.

## Файлы
- `index.html` — редирект на `game.html`
- `game.html` — приложение (Иванов, Активности, Карты, Аудит, Видение)
- `netlify.toml` — конфиг для отдельного Netlify‑сайта (в этой папке)
- `netlify/functions/chat.js` — серверная функция для OpenRouter

## Локально
Откройте `game.html` в браузере.

## GitHub Pages
1. Репозиторий: добавьте `index.html` и `game.html` в корень
2. Settings → Pages → Deploy from a branch → `main` (root)
3. Ссылка: `https://<user>.github.io/<repo>/`

Примечание: на GH Pages серверных функций нет, поэтому секция «Активности» будет работать в fallback‑режиме (статичная база).

## Netlify (отдельный сайт, не трогая портфолио)
1. Создайте новый сайт в Netlify (используйте отдельный проект; старый `methodbus` удалён как дубликат)
2. Подключите репозиторий `metod_buster` или загрузите папку `methodist-booster`
3. Build command: пусто; Publish directory: `.` (в этой папке есть `netlify.toml`)
4. Site settings → Build & deploy → Environment → Add variable:
   - Name: `OPENROUTER_KEY`
   - Value: ваш ключ OpenRouter
5. Деплой. Домен будет вида `https://<имя>.netlify.app`

## Проверка
- Вкладки переключаются
- «🎭 Иванов»: клики меняют здоровье
- «⚡ Активности»: при деплое на Netlify — AI через `/.netlify/functions/chat`; при ошибке — статично
- «🎴 Карты»: вытягивает карту
- «🔍 Аудит»: выдаёт вердикт — обучение нужно/не нужно
- «🎯 Видение»: 7 шагов, итоговый документ (копируется в буфер)
