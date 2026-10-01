"""
Отправка 9 холодных писем через Gmail SMTP — 5 октября 2026.
Интервал между письмами: ~8 минут (9 писем за ~72 минуты, окно 9:05–10:30).

Запуск: python scripts/send_cold_emails.py
Можно запустить заранее — скрипт дождётся 9:05.
"""
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime

# ----- CONFIG -----
FROM = "look85@gmail.com"
PASSWORD = "lkgn vymg wunx dlsd"
RESUME = Path(r"C:\Users\marcenuk\Desktop\Резюме_Марценюк Наталья.pdf")
SUBJECT = "Специалист по обучению и развитию — возможное сотрудничество"
TARGET_TIME = (9, 5)  # 09:05

IT_BODY = """Добрый день!

Меня зовут Наталья Марценюк — главный методист Корпоративного университета ОАО «РЖД».

Более 10 лет в корпоративном обучении и развитии образовательных систем.
В настоящее время отвечаю за портфель программ развития профессиональных компетенций руководителей (от 2-х до 310 ак.ч.)
NPS флагманской программы: 9,7 из 10.

Веду полный цикл работы с бизнес-заказчиком: от анализа потребностей и проектирования до запуска и оценки эффективности.
В работе активно использую AI-инструменты: аналитика обратной связи, генерация учебных сценариев, создание презентаций и внутренних сервисов.
Прошла курс по созданию IT-продуктов с помощью AI-агентов (ScrumTrek).

В начале декабря переезжаю из Москвы в Минск по семейным обстоятельствам и рассматриваю возможности продолжить работу в сфере корпоративного обучения.

Буду рада короткому разговору, чтобы обсудить, чем мой опыт может быть полезен вашей компании.
С 11 по 14 октября включительно буду в Минске и готова к очной встрече.

Резюме прилагаю.
Портфолио: https://look85-ops.github.io/NAAssistant/portfolio/

С уважением,
Наталья Марценюк
+7 903 973-98-30 | look85@gmail.com | Telegram: @mrk_natalia"""

BANK_BODY = """Добрый день!

Меня зовут Наталья Марценюк — главный методист Корпоративного университета ОАО «РЖД».

Более 10 лет в корпоративном обучении и развитии образовательных систем.
В настоящее время отвечаю за портфель программ развития профессиональных компетенций руководителей (от 2-х до 310 ак.ч.)
NPS флагманской программы: 9,7 из 10.

Веду полный цикл работы с бизнес-заказчиком: от анализа потребностей и проектирования до запуска и оценки эффективности.
Ранее работала в ПАО «Сбербанк», где отвечала за образовательные решения по блоку «Транзакционные продукты» трайба «СберБизнес» (9 000+ сотрудников).

В начале декабря переезжаю из Москвы в Минск по семейным обстоятельствам и рассматриваю возможности продолжить работу в сфере корпоративного обучения.

Буду рада короткому разговору, чтобы обсудить, чем мой опыт может быть полезен вашей компании.
С 11 по 14 октября включительно буду в Минске и готова к очной встрече.

Резюме прилагаю.
Портфолио: https://look85-ops.github.io/NAAssistant/portfolio/

С уважением,
Наталья Марценюк
+7 903 973-98-30 | look85@gmail.com | Telegram: @mrk_natalia"""

COMPANIES = [
    ("EPAM", "ask@epam.com", IT_BODY),
    ("IBA Group", "resume@iba.by", IT_BODY),
    ("ITransition", "hh@itransition.com", IT_BODY),
    ("Innowise", "job@innowise.com", IT_BODY),
    ("LogicLike", "hr@logiclike.com", IT_BODY),
    ("Белагропромбанк", "hr@belapb.by", BANK_BODY),
    ("ВТБ Беларусь", "HR@vtb-bank.by", BANK_BODY),
    ("Беларусбанк", "info@belarusbank.by", BANK_BODY),
    ("БНБ-Банк", "customer@bnb.by", BANK_BODY),
]

INTERVAL = 8 * 60  # 8 минут между письмами


def create_message(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # Attach resume PDF
    if RESUME.exists():
        with open(RESUME, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{RESUME.name}"',
            )
            msg.attach(part)

    return msg


def send_one(server, name, email, body):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {name} → {email} ... ", end="", flush=True)
    try:
        msg = create_message(email, SUBJECT, body)
        server.send_message(msg)
        print("OK")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def main():
    # Wait until target time
    now = datetime.now()
    target = now.replace(hour=TARGET_TIME[0], minute=TARGET_TIME[1], second=0, microsecond=0)
    if now < target:
        wait = (target - now).total_seconds()
        print(f"Жду до {target.strftime('%H:%M')} ({wait/60:.0f} мин)...")
        time.sleep(wait)

    print(f"\n=== Старт рассылки: {datetime.now().strftime('%H:%M:%S')} ===\n")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(FROM, PASSWORD)

        ok = fail = 0
        for i, (name, email, body) in enumerate(COMPANIES):
            if i > 0:
                print(f"Пауза {INTERVAL//60} мин...")
                time.sleep(INTERVAL)

            if send_one(server, name, email, body):
                ok += 1
            else:
                fail += 1

        print(f"\n=== Готово: {ok} отправлено, {fail} ошибок ===\n")
        print(f"Завершено: {datetime.now().strftime('%H:%M:%S')}")


if __name__ == "__main__":
    main()