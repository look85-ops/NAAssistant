
import sys
import markdown
from docx import Document
from docx.shared import Inches

def convert_md_to_docx(md_file_path, docx_file_path):
    """
    Converts a Markdown file to a DOCX document, preserving basic formatting.
    """
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html = markdown.markdown(md_content)

    document = Document()

    # This is still a simplified conversion. 
    # A more robust solution would involve parsing the HTML tree.
    # For now, this handles basic cases.
    for line in html.split('\n'):
        if line.startswith('<h1>') and line.endswith('</h1>'):
            document.add_heading(line[4:-5], level=1)
        elif line.startswith('<h2>') and line.endswith('</h2>'):
            document.add_heading(line[4:-5], level=2)
        elif line.startswith('<h3>') and line.endswith('</h3>'):
            document.add_heading(line[4:-5], level=3)
        elif line.startswith('<ul>') or line.startswith('<li>'):
             # Simplified list handling
            clean_line = line.replace('<ul>', '').replace('</ul>', '').replace('<li>', '').replace('</li>', '').strip()
            if clean_line:
                document.add_paragraph(clean_line, style='List Bullet')
        elif line.startswith('<p>') and line.endswith('</p>'):
            document.add_paragraph(line[3:-4])
        elif line.strip():
            document.add_paragraph(line)

    document.save(docx_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_md_to_docx.py <input.md> <output.docx>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_md_to_docx(input_file, output_file)
    print(f"Successfully converted {input_file} to {output_file}")
