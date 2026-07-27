import os

import pandas as pd

files = os.listdir(r'C:\Users\marcenuk\Desktop\АП_Модуль 2\Рейтинг_М2')
for f in files:
    if 'АОС' in f and f.endswith('.xlsx'):
        print(f'Found: {f}')
        filepath = os.path.join(r'C:\Users\marcenuk\Desktop\АП_Модуль 2\Рейтинг_М2', f)
        try:
            df = pd.read_excel(filepath)
            print(f'Shape: {df.shape}')
            print(f'Columns: {list(df.columns)}')
            print(df.head(3).to_string())
            print('---')
            print(df.dtypes)
        except Exception as e:
            print(f'Error: {e}')