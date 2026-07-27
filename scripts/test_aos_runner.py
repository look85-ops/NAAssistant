import os
import sys

sys.path.insert(0, r'C:\Users\marcenuk\Desktop\Новый проект')
from scripts.aos_analyzer.core import (
    calc_metrics,
    detect_anomalies,
    detect_score_cols,
    detect_social_desirability,
    read_data,
)

print('core imported OK')
import pandas as pd
df = pd.read_csv(r'C:\Users\marcenuk\Desktop\Новый проект\scripts\test_aos.csv', sep=';', encoding='utf-8-sig')
cols = detect_score_cols(df)
print(f'Columns: {cols}')
metrics = calc_metrics(df, cols)
print(f'Metrics: {len(metrics)} questions')
for m in metrics:
    print(f'  {m["question"]}: mean={m["mean"]:.2f}, nps={m["nps"]:.1f}, n_unique={m["n_unique"]}')
anomalies = detect_anomalies(metrics)
print(f'Anomalies: {len(anomalies)}')
sv = detect_social_desirability(metrics)
print(f'Social verdict: {sv["verdict"]}')
print('ALL OK')
