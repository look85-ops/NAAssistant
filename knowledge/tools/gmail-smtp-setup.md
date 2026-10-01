# Gmail SMTP — отправка писем с look85@gmail.com

## Учётные данные
- **Email:** look85@gmail.com
- **Пароль приложения:** `lkgn vymg wunx dlsd` (из `.env`, переменная `GMAIL_APP_PASSWORD`)
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
    s.login('look85@gmail.com', 'lkgn vymg wunx dlsd')
    s.send_message(msg)
```

## Ограничения
- Gmail SMTP не поддерживает отложенную отправку (scheduled send)
- Для отложки — скрипт с `time.sleep()` или Windows Task Scheduler
- Лимит Gmail: ~500 писем/день

## Подтверждённые получатели (Антон и др.)
- Отправка работает, пароль приложения активен
- Тестовое письмо 29.09.2026 — успешно

## Файлы
- `.env` — GMAIL_APP_PASSWORD
- `scripts/vacancy_monitor.py` — пример использования для мониторинга вакансий
- `scripts/send_cold_emails.py` — скрипт для массовой отправки холодных писем (5 октября 2026)