"""
aos_wave_report.py — генератор отчёта волны AOS по шаблону docs/aos/reports/TEMPLATE_wave.md.

Переиспользует aos_analyzer.core (метрики, аномалии, качество данных).
Цифры и структуру заполняет автоматически; разделы вывода оставляет заглушками для аналитика.

Использование:
  python scripts/aos_wave_report.py --input FILE.csv --program "П+Путь" --wave "М1, 23.01.2026" --audience "..." --out PATH.md
"""

import argparse
import sys
import os
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "projects", "aos-analyzer"))

from aos_analyzer.core import (
    read_data, detect_score_cols, calc_metrics,
    detect_anomalies, detect_social_desirability,
)


def _na_ok(value):
    return "—" if value is None else value


def main():
    parser = argparse.ArgumentParser(description="Генератор отчёта волны AOS")
    parser.add_argument("--input", required=True, help="CSV/XLSX с данными волны")
    parser.add_argument("--program", default="AOS", help="Название программы")
    parser.add_argument("--wave", default="", help="Ярлык волны (например, М3, 01.07.2026)")
    parser.add_argument("--audience", default="", help="Целевая аудитория")
    parser.add_argument("--out", required=True, help="Путь результирующего .md")
    args = parser.parse_args()

    df = read_data(args.input)
    score_cols = detect_score_cols(df)

    if not score_cols:
        print("Нет колонок-оценок (1-10). Файл не обработан.")
        sys.exit(1)

    metrics = calc_metrics(df, score_cols)
    anomalies = detect_anomalies(metrics)
    verdict = detect_social_desirability(metrics)

    n_total = df.shape[0]
    n_respondents = max(m["n"] for m in metrics)

    avg_mean = sum(m["mean"] for m in metrics) / len(metrics)
    avg_nps = sum(m["nps"] for m in metrics) / len(metrics)
    avg_std = sum(m["std"] for m in metrics) / len(metrics)

    sv = verdict["verdict"]
    sv_reason = verdict.get("reason", "")
    if sv != "clean":
        sig = "; ".join(verdict.get("signals", []))
        sv_reason = f"{sig}. {sv_reason}" if sig else sv_reason

    worst = min(metrics, key=lambda m: m["mean"])
    best = max(metrics, key=lambda m: m["mean"])

    wave = f", {args.wave}" if args.wave else ""

    lines = []
    lines.append(f"# АОС — {args.program}{wave}")
    lines.append("")
    lines.append(f"**Дата анализа:** {date.today().isoformat()}")
    lines.append(f"**Волна:** {args.wave if args.wave else 'без ярлыка'}")
    lines.append(f"**Выгрузка:** `{os.path.basename(args.input)}`")
    lines.append(f"**Анкет:** {n_respondents} (из {n_total} строк выгрузки)")
    if args.audience:
        lines.append(f"**Целевая аудитория:** {args.audience}")
    lines.append("")
    lines.append(f"**Качество данных:** `{sv}` — {sv_reason}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Ключевые цифры")
    lines.append("")
    lines.append("| Метрика | Среднее | NPS (9–10 минус 1–6) | Распределение (Сторонники / Нейтр / Критики) |")
    lines.append("|---|---|---|---|")
    for m in metrics:
        seg = m["segment"]
        lines.append(
            f"| {m['question']} | {m['mean']} | {m['nps']}% "
            f"| {seg['promoters']} / {seg['passives']} / {seg['detractors']} |"
        )
    lines.append("")
    lines.append(f"**Средний балл по форматам: {avg_mean:.2f}**, средний SD {avg_std:.2f}, средний NPS {avg_nps:.1f}%.")
    lines.append("")
    lines.append("### Рейтинг сессий (по среднему баллу)")
    lines.append("")
    lines.append("| # | Сессия | Средний балл |")
    lines.append("|---|---|---|")
    for i, m in enumerate(sorted(metrics, key=lambda x: -x["mean"]), start=1):
        lines.append(f"| {i} | {m['question']} | **{m['mean']}** |")
    lines.append("")
    lines.append(f"**Самый низкий балл — {worst['question']} ({worst['mean']}).** {worst['segment']['detractors']} критик(ов).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Ожидания участников")
    lines.append("")
    lines.append("_(заполнить по открытым вопросам: категории «превзошла / соответствовало / не соответствовало», доли)._")
    lines.append("")
    lines.append("## 3. Аномалии и качество данных")
    lines.append("")
    if anomalies:
        for a in anomalies:
            icon = {"high": "[!]", "medium": "[?]", "info": "[i]"}.get(a.get("severity"), "[i]")
            lines.append(f"- {icon} **{a['question']}**: {a['detail']}")
    else:
        lines.append("- Аномалий не обнаружено.")
    lines.append("")
    lines.append(f"Контекст: лучший вопрос «{best['question']}» ({best['mean']}), худший — «{worst['question']}» ({worst['mean']}).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Топ-3 вывода")
    lines.append("")
    lines.append("### 4.1. ")
    lines.append("### 4.2. ")
    lines.append("### 4.3. ")
    lines.append("")
    lines.append("## 5. Цитаты")
    lines.append("")
    lines.append("> ")
    lines.append("> ")
    lines.append("")
    lines.append("## 6. Три правки")
    lines.append("")
    lines.append("### Правка 1: ")
    lines.append("**Проблема:** ")
    lines.append("**Действие:** ")
    lines.append("**Метрика:** ")
    lines.append("")
    lines.append("### Правка 2: ")
    lines.append("**Проблема:** ")
    lines.append("**Действие:** ")
    lines.append("**Метрика:** ")
    lines.append("")
    lines.append("### Правка 3: ")
    lines.append("**Проблема:** ")
    lines.append("**Действие:** ")
    lines.append("**Метрика:** ")
    lines.append("")
    lines.append("## 7. A/B-гипотеза")
    lines.append("")
    lines.append("**Название:** ")
    lines.append("**Гипотеза:** ")
    lines.append("**Дизайн:** ")
    lines.append("**Ожидаемый эффект:** ")
    lines.append("")
    lines.append("## 8. Инсайты для knowledge/")
    lines.append("")
    lines.append("1. ")
    lines.append("2. ")
    lines.append("3. ")

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"OK: {args.out}")


if __name__ == "__main__":
    main()