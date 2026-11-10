import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

BASE = Path(__file__).resolve().parent
PYTHON = BASE / ".venv" / "Scripts" / "python.exe"
SCRIPT = BASE / "transcribe.py"

MODELS = ["tiny", "base", "small", "medium", "large-v3"]
LANG = {"Русский": "ru", "Английский": "en", "Авто": "auto"}

AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".ogg", ".flac", ".mp4", ".webm", ".mov", ".aac", ".wma")


def shorten_path(p: str, max_len: int = 60) -> str:
    if len(p) <= max_len:
        return p
    return "..." + p[-(max_len - 3):]


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Транскрибация аудио (Whisper)")
        root.geometry("680x420")
        root.minsize(600, 380)

        self.files = []
        self.proc = None
        self.q = queue.Queue()

        frm = ttk.Frame(root, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Файлы для расшифровки:").grid(row=0, column=0, sticky="w")
        self.btn_add = ttk.Button(frm, text="Добавить файлы…", command=self.add_files)
        self.btn_add.grid(row=1, column=0, sticky="w", pady=(4, 8))

        self.listbox = tk.Listbox(frm, height=6)
        self.listbox.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 8))
        self.btn_clear = ttk.Button(frm, text="Очистить", command=self.clear_files)
        self.btn_clear.grid(row=3, column=0, sticky="w")

        ttk.Label(frm, text="Модель:").grid(row=4, column=0, sticky="w", pady=(8, 0))
        self.model_var = tk.StringVar(value="medium")
        self.model_box = ttk.Combobox(frm, textvariable=self.model_var, values=MODELS, state="readonly", width=12)
        self.model_box.grid(row=5, column=0, sticky="w")

        ttk.Label(frm, text="Язык:").grid(row=4, column=1, sticky="w", pady=(8, 0))
        self.lang_var = tk.StringVar(value="Русский")
        self.lang_box = ttk.Combobox(frm, textvariable=self.lang_var, values=list(LANG), state="readonly", width=12)
        self.lang_box.grid(row=5, column=1, sticky="w", padx=(8, 0))

        ttk.Label(frm, text=("Модель medium качается при первом запуске (~1.5 ГБ, разово).\n"
                             "Результат появляется рядом с исходным файлом: .md с таймкодами, .txt сплошным текстом."),
                  foreground="#666").grid(row=6, column=0, columnspan=3, sticky="w", pady=(12, 8))

        self.btn_start = ttk.Button(frm, text="▶  Расшифровать", command=self.start)
        self.btn_start.grid(row=7, column=0, sticky="w", pady=(0, 8))

        self.status = ttk.Label(frm, text="Готово к работе.", foreground="#333")
        self.status.grid(row=8, column=0, columnspan=3, sticky="w")

        self.progress = ttk.Progressbar(frm, mode="indeterminate")
        self.progress.grid(row=9, column=0, columnspan=3, sticky="ew", pady=(8, 0))

        frm.columnconfigure(0, weight=1)

        # drag & drop
        try:
            root.tk.call("package", "require", "tkdnd")
            root.tk.call("tkdnd::drop_target", "register", self.listbox, "DND_Files")
            root.tk.call("bind", self.listbox, "<<Drop>>", self._on_drop)
        except tk.TclError:
            pass

        self.root.after(100, self._poll_queue)

    def add_files(self):
        paths = filedialog.askopenfilenames(
            title="Выберите аудио/видео",
            filetypes=[("Аудио и видео", "*.mp3 *.wav *.m4a *.ogg *.flac *.mp4 *.webm *.mov *.aac *.wma"),
                       ("Все файлы", "*.*")])
        for p in paths:
            if p not in self.files:
                self.files.append(p)
        self._refresh_list()

    def _on_drop(self, event):
        added = self.root.tk.splitlist(event.data)
        for p in added:
            p = p.strip()
            if p and os.path.isfile(p) and p not in self.files:
                self.files.append(p)
        self._refresh_list()

    def clear_files(self):
        self.files.clear()
        self._refresh_list()

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for p in self.files:
            self.listbox.insert(tk.END, shorten_path(p))

    def start(self):
        if self.proc and self.proc.poll() is None:
            messagebox.showinfo("Занято", "Уже идёт расшифровка. Подожди окончания.")
            return
        if not self.files:
            messagebox.showwarning("Нет файлов", "Добавь хотя бы один файл.")
            return
        if not PYTHON.exists():
            messagebox.showerror("Нет окружения", f"Не найден {PYTHON}. Проверь установку .venv.")
            return

        model = self.model_var.get()
        lang = LANG[self.lang_var.get()]
        cmd = [str(PYTHON), str(SCRIPT), "--model", model, "--language", lang, "--txt", *self.files]

        self.btn_start.config(state="disabled")
        self.status.config(text=f"Загружаю модель '{model}' и распознаю…")
        self.progress.start(12)

        def run():
            env = os.environ.copy()
            env["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, encoding="utf-8", errors="replace", env=env, cwd=str(BASE.parent.parent))
            self.proc = p
            for line in p.stdout:
                self.q.put(line.rstrip())
            p.wait()
            self.q.put(("__DONE__", p.returncode))

        threading.Thread(target=run, daemon=True).start()

    def _poll_queue(self):
        try:
            while True:
                item = self.q.get_nowait()
                if isinstance(item, tuple) and item[0] == "__DONE__":
                    self._finish(item[1])
                else:
                    line = item
                    if any(k in line for k in ("MD  ->", "TXT ->", "Сегментов")):
                        self.status.config(text=line)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)

    def _finish(self, code):
        self.progress.stop()
        self.btn_start.config(state="normal")
        if code == 0:
            self.status.config(text="✅ Готово. Файлы .md и .txt рядом с исходниками.", foreground="#1a7f37")
        else:
            self.status.config(text=f"⚠ Ошибка (код {code}). См. консоль.", foreground="#b32222")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()