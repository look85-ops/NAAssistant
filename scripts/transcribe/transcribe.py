#!/usr/bin/env python
"""Транскрибация аудио/видео через faster-whisper.

Запуск (из корня проекта):
    py -3 scripts/transcribe/transcribe.py "путь/к/файлу.mp3" [ещё_файлы...]

Опции:
    --model      модель Whisper (tiny|base|small|medium|large-v3). По умолчанию medium.
    --language   язык (например ru, en). По умолчанию ru.
    --out        папка для результата. По умолчанию рядом с исходным файлом.
    --txt        дополнительно писать чистый текст в .txt (да/нет). По умолчанию да.

Результат: рядом с исходником создаётся
    имя_файла.transcript.md   — расшифровка с таймкодами
    имя_файла.transcript.txt  — сплошной текст (если включено)

Первая модель medium (~1.5 ГБ) качается при первом запуске — это разово.
"""

import argparse
import sys
from pathlib import Path

try:
    from faster_whisper import WhisperModel
except ImportError:
    sys.exit(
        "faster-whisper не установлен.\n"
        "Установи: scripts/transcribe/.venv/Scripts/python.exe -m pip install faster-whisper"
    )


def fmt_ts(seconds: float) -> str:
    """Секунды -> строку MM:SS или HH:MM:SS."""
    s = int(round(seconds))
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"


def _safe_print(s: str):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


def transcribe_file(model, path: Path, language: str, out_dir: Path, write_txt: bool):
    _safe_print(f"\n=== {path.name} ===")
    segments, info = model.transcribe(str(path), language=language)

    lines = []
    for seg in segments:
        ts = f"[{fmt_ts(seg.start)}–{fmt_ts(seg.end)}]"
        text = seg.text.strip()
        lines.append((ts, text))

    if not lines:
        _safe_print("\nНичего не распознано. Возможно, в файле нет речи.")
        return

    stem = path.stem
    md_path = out_dir / f"{stem}.transcript.md"
    md_lines = ["# Расшифровка: " + path.name, ""]
    for ts, text in lines:
        md_lines.append(f"{ts} {text}")
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    if write_txt:
        txt_path = out_dir / f"{stem}.transcript.txt"
        txt_path.write_text("\n".join(t for _, t in lines) + "\n", encoding="utf-8")

    _safe_print(f"Сегментов: {len(lines)}  ->  {md_path}")


def main():
    ap = argparse.ArgumentParser(description="Транскрибация аудио через faster-whisper")
    ap.add_argument("files", nargs="+", help="файлы аудио/видео")
    ap.add_argument("--model", default="medium",
                    help="модель Whisper (tiny, base, small, medium, large-v3)")
    ap.add_argument("--language", default="ru", help="язык, напр. ru, en, auto")
    ap.add_argument("--out", default=None, help="папка для результата")
    ap.add_argument("--txt", action="store_true", default=True, help="писать .txt")
    ap.add_argument("--no-txt", dest="txt", action="store_false", help="не писать .txt")
    args = ap.parse_args()

    lang = None if args.language == "auto" else args.language

    print(f"Загружаю модель '{args.model}' (первый раз может качать)...")
    model = WhisperModel(args.model, device="cpu", compute_type="float32")
    print("Модель готова.")

    for f in args.files:
        p = Path(f).expanduser().resolve()
        if not p.exists():
            print(f"[пропуск] не найден: {p}")
            continue
        out_dir = Path(args.out).resolve() if args.out else p.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        transcribe_file(model, p, lang, out_dir, args.txt)

    print("\nГотово.")


if __name__ == "__main__":
    main()