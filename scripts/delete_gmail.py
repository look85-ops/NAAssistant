"""Удаление (в корзину) рекламных/шумовых писем из входящих Gmail по отправителю.

MOVE в корзину — обратимо 30 дней. --dry-run только показывает, что удалит.
Запуск: py scripts/delete_gmail.py --days 21 [--dry-run]
"""
import argparse
import email.header
import imaplib
import os
import sys
from datetime import datetime, timedelta

FROM_KEYS = ["ozon", "englex", "yclients", "teatrtruda", "garagemca", "форма"]
TRASH = "[Gmail]/&BBoEPgRABDcEOAQ9BDA-"


def dec(s):
    if not s:
        return ""
    out = []
    for txt, enc in email.header.decode_header(s):
        if isinstance(txt, bytes):
            out.append(txt.decode(enc or "utf-8", errors="replace"))
        else:
            out.append(txt)
    return "".join(out).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=21)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        sys.exit("GMAIL_APP_PASSWORD не задан.")

    M = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=30)
    M.login("look85@gmail.com", password)
    M.select("INBOX")

    since = (datetime.now() - timedelta(days=args.days)).strftime("%d-%b-%Y")
    typ, data = M.uid("SEARCH", None, "SINCE", since)
    if typ != "OK":
        sys.exit(f"SEARCH fail: {typ}")

    uids = data[0].split()
    to_move = []
    for uid in uids:
        typ, md = M.uid("FETCH", uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])")
        if typ != "OK":
            continue
        part1 = md[0][1] if md and isinstance(md[0], tuple) else b""
        msg = email.message_from_bytes(part1)
        frm = dec(msg.get("From", ""))
        subj = dec(msg.get("Subject", ""))
        if any(k in frm.lower() for k in FROM_KEYS):
            to_move.append((uid.decode(), frm, subj))

    if not to_move:
        print("Ничего не найдено для удаления.")
        M.logout()
        return

    print(f"# Найдено к перемещению в корзину: {len(to_move)}")
    for uid, frm, subj in to_move:
        print(f"  {frm[:42]:<42} | {subj[:60]}")

    if args.dry_run:
        print("\n[DRY-RUN] ничего не удалял. Убери --dry-run для реального перемещения.")
        M.logout()
        return

    for uid, frm, subj in to_move:
        typ, resp = M.uid("STORE", uid, "+X-GM-LABELS", "\\Trash")
        if typ == "OK":
            print(f"  ✓ в корзину: {frm[:40]} | {subj[:50]}")
        else:
            print(f"  ✗ ошибка: {frm[:40]} -> {resp}")

    M.logout()
    print(f"\nГотово. Перемещено: {len(to_move)}.")


if __name__ == "__main__":
    main()