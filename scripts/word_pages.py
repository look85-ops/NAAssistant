# -*- coding: utf-8 -*-
"""
Open docx via Word COM, walk paragraphs and record:
- page number, text, font color of first colored run (if any).
Usage: python word_pages.py <input.docx> <output.json>
"""
import json
import os
import sys
import time

if len(sys.argv) >= 3:
    DOCX = sys.argv[1]
    OUT = sys.argv[2]
else:
    DOCX = r"C:\Users\marcenuk\Desktop\П+Путь_М1_Организация хозяйства пути_26\М1_Д1_26\Сценарий_М1Д1_26.docx"
    OUT = r"C:\Users\marcenuk\AppData\Local\Temp\opencode\scenario_pages.json"

import win32com.client as win32
from win32com.client import constants

wdActiveEndPageNumber = 3

def is_blueish(c):
    if c is None or c < 0:
        return False
    r = c & 0xFF
    g = (c >> 8) & 0xFF
    b = (c >> 16) & 0xFF
    if b >= 120 and b > r + 20 and b >= g - 10:
        return True
    return False

def main():
    word = win32.gencache.EnsureDispatch("Word.Application")
    word.Visible = False
    word.ScreenUpdating = False
    print("opening", DOCX)
    doc = word.Documents.Open(DOCX, ReadOnly=True)
    print("opened; repaginating")
    doc.Repaginate()
    total_pages = doc.ComputeStatistics(2)
    print("pages:", total_pages)

    results = []
    paragraphs = doc.Paragraphs
    n = paragraphs.Count
    print("paragraphs:", n)
    for i in range(1, n + 1):
        p = paragraphs.Item(i)
        rng = p.Range
        text = rng.Text
        if not text or text.strip() == "":
            continue
        page = rng.Information(wdActiveEndPageNumber)
        color = None
        try:
            color = rng.Font.Color
        except Exception:
            color = None
        blue_marks = []
        if color == 9999999:
            l = rng.End - rng.Start
            step = max(1, l // 20)
            pos = rng.Start
            while pos < rng.End:
                sub = doc.Range(pos, min(pos + step, rng.End))
                c = sub.Font.Color
                if c != 9999999 and is_blueish(c):
                    blue_marks.append((sub.Start, sub.End))
                pos += step
            has_blue = len(blue_marks) > 0
            style_color = "mixed"
        else:
            has_blue = is_blueish(color)
            style_color = color

        results.append({
            "idx": i,
            "page": int(page),
            "text": text.rstrip("\r\x07\x0b"),
            "has_blue": bool(has_blue),
            "color": style_color if isinstance(style_color, str) else int(style_color),
        })
        if i % 200 == 0:
            print(f"...{i}/{n} p{page}")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"total_pages": total_pages, "items": results}, f, ensure_ascii=False, indent=1)
    print("saved", OUT)

    doc.Close(SaveChanges=False)
    word.Quit()

if __name__ == "__main__":
    main()
