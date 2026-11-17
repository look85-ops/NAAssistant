# -*- coding: utf-8 -*-
"""
Шаг 1. Экспорт слайдов презентации в PNG через PowerPoint COM.

Использование:
    py 1_render.py

Настрой в блоке CONFIG ниже пути к .pptx и папку для PNG.
Экспорт идёт 2500x1406 (16:9), как эталон в сценариях П+Путь.
"""
import os
import sys
import pythoncom
import win32com.client

# === CONFIG ===
PPTX = r"путь\к\управляющей_презентации.pptx"
OUT_DIR = r"путь\к\папке_для_png"
W, H = 2500, 1406
# ==============

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    pythoncom.CoInitialize()
    pp = win32com.client.Dispatch('PowerPoint.Application')
    try:
        pres = pp.Presentations.Open(PPTX, ReadOnly=-1, Untitled=-1, WithWindow=-1)
        total = pres.Slides.Count
        done = 0
        for n in range(1, total + 1):
            out = os.path.join(OUT_DIR, 'slide%03d.png' % n)
            pres.Slides.Item(n).Export(out, 'PNG', W, H)
            done += 1
        pres.Close()
        print('OK: отрендерено %d слайдов -> %s' % (done, OUT_DIR))
    finally:
        pp.Quit()

if __name__ == '__main__':
    main()