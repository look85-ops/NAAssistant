import json
import zipfile
import sys
from lxml import etree

SRC = sys.argv[1]
OUT = sys.argv[2]

NSMAP = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

def is_blueish(hex_color):
    """hex_color like '0070C0' or '2E75B6' etc."""
    if not hex_color or hex_color == 'auto' or hex_color == '000000':
        return False
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except (ValueError, IndexError):
        return False
    # Blue-ish: b >= 120 and b > r+20 and b >= g-10 (similar to word_pages logic)
    return b >= 120 and b > r + 20 and b >= g - 10

def get_run_color(rpr):
    """Extract color val from w:rPr/w:color"""
    color_el = rpr.find('.//w:color', NSMAP)
    if color_el is not None:
        return color_el.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', 'auto')
    return None

def extract_text_with_color(xml_content):
    """Parse document.xml and extract paragraphs with text and blue detection."""
    tree = etree.fromstring(xml_content)
    results = []
    
    for p in tree.iterfind('.//w:p', NSMAP):
        para_text = []
        has_blue = False
        
        for r in p.iterfind('.//w:r', NSMAP):
            rpr = r.find('w:rPr', NSMAP)
            color_val = get_run_color(rpr) if rpr is not None else None
            
            run_text_parts = []
            for t in r.iterfind('.//w:t', NSMAP):
                if t.text:
                    run_text_parts.append(t.text)
            run_text = ''.join(run_text_parts)
            
            if color_val and is_blueish(color_val):
                has_blue = True
            
            para_text.append(run_text)
        
        full_text = ''.join(para_text).strip()
        if not full_text:
            continue
        
        results.append({
            "text": full_text,
            "has_blue": bool(has_blue),
        })
    
    return results

with zipfile.ZipFile(SRC) as z:
    xml_content = z.read('word/document.xml')

results = extract_text_with_color(xml_content)

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump({"total": len(results), "items": results}, f, ensure_ascii=False, indent=1)

print(f"saved {len(results)} paragraphs to {OUT}")
