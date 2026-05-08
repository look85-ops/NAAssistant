#!/usr/bin/env python3
# -*- coding: ascii -*-


import argparse
import csv
import os
from pathlib import Path
from typing import Dict, List, Tuple


METRIC_COLUMNS = [
    'Преподаватель понятно излагает материал',
    'Во время обучения Вы чувствовали себя включенным в работу',
    'Преподаватель качественно и полно отвечает на вопросы участников',
    'Обучение было для меня интересным',
    'Знания и навыки, полученные в ходе обучения, имеют практическую применяемость',
]

# Some datasets might use slightly different header spelling for the last column
FALLBACK_LAST = 'Знания и навыки, полученные в ходе обучения, имеют практическую применимость'


def parse_number(val: str) -> float:
    if val is None:
        return float('nan')
    s = val.strip().replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return float('nan')


def read_csv_numbers(path: Path) -> Tuple[Dict[str, List[float]], int]:
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        headers = reader.fieldnames or []
        cols = METRIC_COLUMNS.copy()
        if METRIC_COLUMNS[-1] not in headers and FALLBACK_LAST in headers:
            cols[-1] = FALLBACK_LAST
        values: Dict[str, List[float]] = {c: [] for c in cols if c in headers}
        rows = 0
        for row in reader:
            rows += 1
            for c in values.keys():
                val = parse_number(row.get(c, ''))
                if val == val:  # not NaN
                    values[c].append(val)
    return values, rows


def avg(xs: List[float]) -> float:
    if not xs:
        return float('nan')
    return sum(xs) / len(xs)


def format_float(x: float) -> str:
    if x != x:
        return '—'
    return f"{x:.2f}"


def scan_inputs(input_path: Path) -> List[Path]:
    if input_path.is_file():
        return [input_path]
    out: List[Path] = []
    for p in sorted(input_path.glob('*.csv')):
        out.append(p)
    return out


def build_report(files: List[Path]) -> str:
    per_file: List[Tuple[str, Dict[str, float], int]] = []
    overall: Dict[str, List[float]] = {}
    total_rows = 0
    for file in files:
        values, rows = read_csv_numbers(file)
        total_rows += rows
        avgs = {k: avg(v) for k, v in values.items()}
        # aggregate
        for k, v in values.items():
            overall.setdefault(k, []).extend(v)
        per_file.append((file.name, avgs, rows))

    overall_avg = {k: avg(v) for k, v in overall.items()}

    lines: List[str] = []
    lines.append('# Базовый замер AOS (черновой)')
    lines.append('')
    lines.append(f'Файлов: {len(files)}; Ответов (строк): ~{total_rows}')
    lines.append('')
    lines.append('## Средние значения по всем файлам')
    for k, v in overall_avg.items():
        lines.append(f'- {k}: {format_float(v)}')
    lines.append('')
    lines.append('## По файлам')
    for name, avgs, rows in per_file:
        lines.append(f'### {name} (строк: ~{rows})')
        for k, v in avgs.items():
            lines.append(f'- {k}: {format_float(v)}')
        lines.append('')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to CSV file or directory with CSV files')
    parser.add_argument('--out', default=str(Path('docs') / 'aos' / 'reports' / 'baseline-raw.md'))
    args = parser.parse_args()

    input_path = Path(args.path)
    files = scan_inputs(input_path)
    if not files:
        raise SystemExit('No CSV files found')
    report = build_report(files)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding='utf-8')
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
