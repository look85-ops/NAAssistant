import sys, os
sys.path.insert(0, r'C:\Users\marcenuk\Desktop\Новый проект')
from scripts.aos_analyzer.core import read_data, detect_score_cols, calc_metrics, detect_anomalies, detect_social_desirability
print('core imported OK')
df = read_data(r'C:\Users\marcenuk\Desktop\Новый проект\scripts\test_aos.csv')
cols = detect_score_cols(df)
print('Columns: ' + str(cols))
metrics = calc_metrics(df, cols)
print('Metrics: ' + str(len(metrics)) + ' questions')
for m in metrics:
    print(m['question'] + ': mean=' + str(m['mean']) + ', nps=' + str(m['nps']) + ', n_unique=' + str(m['n_unique']))
anomalies = detect_anomalies(metrics)
print('Anomalies: ' + str(len(anomalies)))
sv = detect_social_desirability(metrics)
print('Social verdict: ' + sv['verdict'])
print('ALL OK')