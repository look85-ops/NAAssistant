# Gmail SMTP — отправка писем с look85@gmail.com

## Учётные данные
- **Email:** look85@gmail.com
- **Пароль приложения:** в `.env`, переменная `GMAIL_APP_PASSWORD` (НЕ хранить в этом файле)
- **SMTP:** smtp.gmail.com:465 (SSL)

## Как отправлять
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()
msg['From'] = 'look85@gmail.com'
msg['To'] = 'recipient@example.com'
msg['Subject'] = 'Тема'
msg.attach(MIMEText('Тело письма', 'plain', 'utf-8'))

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
    s.login('look85@gmail.com', os.environ['GMAIL_APP_PASSWORD'])
    s.send_message(msg)
```

## Ограничения
- Gmail SMTP не поддерживает отложенную отправку (scheduled send)
- Для отложки — скрипт с `time.sleep()` или Windows Task Scheduler
- Лимит Gmail: ~500 писем/день

## Подтверждённые получатели (Антон и др.)
- Отправка работает, пароль приложения активен
- Тестовое письмо 29.09.2026 — успешно

## Чтение почты (IMAP) — как проверять входящие и спам

Скрипты для чтения, только чтение (BODY.PEEK), ничего не удаляют:
- `scripts/read_gmail.py` — сводка входящих: `py scripts/read_gmail.py --days N --mailbox <PAПКА>`
- `scripts/delete_gmail.py` — очистка шума по отправителю (осторожно, с `--dry-run`)

### Запуск (Windows PowerShell)
```powershell
$env:GMAIL_APP_PASSWORD = (Select-String -Path .env -Pattern '^GMAIL_APP_PASSWORD\s*=\s*(.+)$').Matches.Groups[1].Value.Trim().Trim('"').Trim("'")
$env:PYTHONIOENCODING="utf-8"
py -X utf8 scripts/read_gmail.py --days 14 --mailbox INBOX
```

### Крипт-нюансы (важно, иначе ловишь ошибки)
1. **Кодировка вывода.** Консоль Windows в cp1251 — кириллица и эмодзи падают с `UnicodeEncodeError: 'charmap' codec can't encode`. Фикс: `-X utf8` + `$env:PYTHONIOENCODING="utf-8"` (обе).
2. **Имя спам-папки.** `INBOX` = входящие, но спам — НЕ `[Gmail]/Spam`. У Gmail русская локаль, поэтому папка закодирована UTF-7. Узнать список папок:
```powershell
py -X utf8 -c "import imaplib,os; M=imaplib.IMAP4_SSL('imap.gmail.com',993); M.login('look85@gmail.com',os.environ['GMAIL_APP_PASSWORD']); [print(repr(x)) for x in M.list()[1]]"
```
Спам = `[Gmail]/&BCEEPwQwBDw-` (метка `\Junk`). Sent = `[Gmail]/&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-`.
3. **`SEARCH illegal in state`** — значит неверное имя папки, `select()` не сработал. Решается п.2.
4. Пароль берём из `.env` (не хардкодить в файлах знаний).

## Файлы
- `.env` — GMAIL_APP_PASSWORD
- `scripts/vacancy_monitor.py` — пример использования для мониторинга вакансий
- `scripts/send_cold_emails.py` — скрипт для массовой отправки холодных писем (5 октября 2026)