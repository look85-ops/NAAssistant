import sys, os
sys.path.insert(0, r'C:\Users\marcenuk\Desktop\Новый проект')
from scripts.aos_analyzer.core import read_data, detect_score_cols, calc_metrics, detect_anomalies, detect_social_desirability
print('core imported OK')
import pandas as pd
df = pd.read_csv(r'C:\Users\marcenuk\Desktop\Новый проект\scripts\test_aos.csv', sep=';', encoding='utf-8-sig')
cols = detect_score_cols(df)
print('Columns: %s' % cols)
metrics = calc_metrics(df, cols)
print('Metrics: %d questions' % len(metrics))
for m in metrics:
    print('  %s: mean=%.2f, nps=%.1f, n_unique=%d' % (m['question'], m['mean'], m['nps'], m['n_unique']))
anomalies = detect_anomalies(metrics)
print('Anomalies: %d' % len(anomalies))
sv = detect_social_desirability(metrics)
print('Social verdict: %s' % sv['verdict'])
print('ALL OK')
