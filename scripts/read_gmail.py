"""Чтение входящих Gmail по IMAP — сводка писем для ручной классификации.

Только чтение (BODY.PEEK), ничего не удаляет и не меняет флаги.
Запуск: py scripts/read_gmail.py [--days N] [--mailbox INBOX]
"""
import argparse
import email.header
import imaplib
import os
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime


def dec(s):
    if not s:
        return ""
    parts = email.header.decode_header(s)
    out = []
    for txt, enc in parts:
        if isinstance(txt, bytes):
            try:
                out.append(txt.decode(enc or "utf-8", errors="replace"))
            except Exception:
                out.append(txt.decode("utf-8", errors="replace"))
        else:
            out.append(txt)
    return "".join(out).strip()


def parse_one(part0, part1):
    """part0 — info строка (bytes), part1 — body (bytes)."""
    info = part0.decode("utf-8", "replace")
    labels = []
    m = re.search(r"X-GM-LABELS \(([^)]*)\)", info)
    if m:
        labels = [t.strip('"') for t in m.group(1).split() if t.strip('"')]
    size = 0
    m = re.search(r"RFC822\.SIZE (\d+)", info)
    if m:
        size = int(m.group(1))

    from_addr = subject = date = ""
    if part1:
        msg = email.message_from_bytes(part1)
        from_addr = dec(msg.get("From", ""))
        subject = dec(msg.get("Subject", ""))
        date_str = msg.get("Date", "")
        try:
            date = parsedate_to_datetime(date_str).strftime("%d.%m.%y %H:%M")
        except Exception:
            date = date_str
    return from_addr, subject, date, labels, size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=21)
    ap.add_argument("--mailbox", default="INBOX")
    ap.add_argument("--limit", type=int, default=250)
    args = ap.parse_args()

    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        sys.exit("GMAIL_APP_PASSWORD не задан.")

    M = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=30)
    M.login("look85@gmail.com", password)
    M.select(args.mailbox, readonly=True)

    since = (datetime.now() - timedelta(days=args.days)).strftime("%d-%b-%Y")
    typ, data = M.uid("SEARCH", None, "SINCE", since)
    if typ != "OK":
        sys.exit(f"SEARCH fail: {typ}")

    uids = data[0].split()
    total = len(uids)
    uids = uids[-args.limit:]

    rows = []
    for uid in uids:
        typ, msg_data = M.uid(
            "FETCH", uid,
            "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)] X-GM-LABELS RFC822.SIZE)",
        )
        if typ != "OK" or not msg_data:
            continue
        part0 = b""
        part1 = b""
        for item in msg_data:
            if isinstance(item, tuple) and isinstance(item[0], bytes):
                part0 = item[0]
                part1 = item[1] if isinstance(item[1], bytes) else b""
                break
        from_addr, subject, date, labels, size = parse_one(part0, part1)
        cat = [l.split("/")[-1] for l in labels if l.startswith("CATEGORY_") or l in ("Spam", "Important")]
        rows.append((date, from_addr, subject, ",".join(cat) or "-", size))

    rows.sort(key=lambda r: r[0], reverse=True)
    print(f"# ВСЕГО писем за {args.days} дн.: {total} (показываю {len(rows)})\n")
    for date, frm, subj, cat, size in rows:
        print(f"{date} | {frm[:42]:<42} | {cat:<20} | {subj[:75]}")
    print(f"\n# Всего показано: {len(rows)}")

    c = Counter()
    for r in rows:
        if "PROMOTIONS" in r[3]:
            c["Promo (рассылки)"] += 1
        elif "SOCIAL" in r[3]:
            c["Соцсети"] += 1
        elif "UPDATES" in r[3]:
            c["Уведомления/транзакции"] += 1
        elif "PERSONAL" in r[3]:
            c["Личное"] += 1
        elif "Spam" in r[3]:
            c["Спам"] += 1
        else:
            c["Без категории"] += 1
    print("\n# Категории Gmail:")
    for k, v in c.most_common():
        print(f"  {k}: {v}")

    M.logout()


if __name__ == "__main__":
    main()