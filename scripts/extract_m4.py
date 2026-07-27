import sys, os
sys.stdout.reconfigure(encoding='utf-8')
try:
    from docx import Document
    base = r'C:\Users\marcenuk\Desktop\АП_Модуль 4'
    files = ['2848р_от_26_12_2025_Паводок+ледоход_новая.docx', 'MBWA.docx']
    for fname in files:
        path = os.path.join(base, fname)
        if not os.path.exists(path):
            print(f'=== {fname} === NOT FOUND')
            continue
        try:
            doc = Document(path)
            text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
            print(f'=== {fname} ({len(text)} chars) ===')
            print(text[:3000])
            print()
        except Exception as e:
            print(f'=== {fname} === ERROR: {e}')
except ImportError:
    print('python-docx not installed. Install: pip install python-docx')
