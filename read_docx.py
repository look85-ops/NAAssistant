import zipfile
import xml.etree.ElementTree as ET
import sys

filepath = r"C:\Users\marcenuk\Desktop\Новый проект\Пост для линкедин 1.docx"

try:
    with zipfile.ZipFile(filepath, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs = []
    for p in root.findall('.//w:p', ns):
        texts = []
        for t in p.findall('.//w:t', ns):
            if t.text:
                texts.append(t.text)
        if texts:
            paragraphs.append(''.join(texts))
    
    text = '\n'.join(paragraphs)
    
    with open(r"C:\Users\marcenuk\Desktop\Новый проект\post_content.txt", "w", encoding="utf-8") as out:
        out.write(text)
    
    print(f"SUCCESS: {len(text)} chars extracted")
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
