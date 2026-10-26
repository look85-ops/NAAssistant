import os, smtplib, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

BODY = """Добрый день!

Меня зовут Наталья Марценюк — главный методист Корпоративного университета ОАО «РЖД».

Более 10 лет в корпоративном обучении и развитии образовательных систем.
В настоящее время отвечаю за портфель программ развития профессиональных компетенций руководителей (от 2-х до 310 ак.ч.)
NPS флагманской программы: 9,7 из 10.

Веду полный цикл работы с бизнес-заказчиком: от анализа потребностей и проектирования до запуска и оценки эффективности.
Ранее работала в ПАО «Сбербанк», где отвечала за образовательные решения по блоку «Транзакционные продукты» трайба «СберБизнес» (9 000+ сотрудников).

В начале декабря переезжаю из Москвы в Минск по семейным обстоятельствам и рассматриваю возможности продолжить работу в сфере корпоративного обучения.

Буду рада короткому разговору, чтобы обсудить, чем мой опыт может быть полезен вашей компании.

Резюме прилагаю.
Портфолио: https://look85-ops.github.io/NAAssistant/portfolio/

С уважением,
Наталья Марценюк
+7 903 973-98-30 | look85@gmail.com | Telegram: @mrk_natalia"""

RESUME = Path(r"C:\Users\marcenuk\Desktop\Резюме_Марценюк Наталья.pdf")

for name, email in [("МТбанк", "HRanketa@mtbank.by")]:
    msg = MIMEMultipart()
    msg["From"] = "look85@gmail.com"
    msg["To"] = email
    msg["Subject"] = "Специалист по обучению и развитию — возможное сотрудничество"
    msg.attach(MIMEText(BODY, "plain", "utf-8"))
    if RESUME.exists():
        with open(RESUME, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{RESUME.name}"')
            msg.attach(part)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login("look85@gmail.com", os.environ["GMAIL_APP_PASSWORD"])
        s.send_message(msg)
    print(f"{name}: OK")