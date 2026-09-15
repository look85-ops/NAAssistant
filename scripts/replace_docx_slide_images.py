"""Replace a contiguous range of slide images inside a DOCX."""
import argparse
import os
import tempfile
import zipfile
from lxml import etree

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('docx')
    ap.add_argument('output')
    ap.add_argument('slide_dir')
    ap.add_argument('--start', type=int, required=True)
    ap.add_argument('--end', type=int, required=True)
    args = ap.parse_args()

    with zipfile.ZipFile(args.docx) as src:
        names = src.namelist()
        document = etree.fromstring(src.read('word/document.xml'))
        rels = etree.fromstring(src.read('word/_rels/document.xml.rels'))
        rel_by_id = {r.get('Id'): r for r in rels}
        blips = document.xpath('.//a:blip', namespaces=NS)
        expected = args.end - args.start + 1
        if args.start < 1 or args.end < args.start or args.end > len(blips):
            raise ValueError(f'range {args.start}-{args.end} outside {len(blips)} images')

        replacements = {}
        for position in range(args.start, args.end + 1):
            blip = blips[position - 1]
            rel_id = blip.get('{%s}embed' % NS['r'])
            rel = rel_by_id.get(rel_id)
            if rel is None:
                raise ValueError(f'missing relationship {rel_id} at image {position}')
            # ZIP member names always use forward slashes, including on Windows.
            target_name = os.path.normpath(
                os.path.join('word', rel.get('Target'))
            ).replace(os.sep, '/')
            png = os.path.join(args.slide_dir, f'slide_{position:03d}.png')
            if not os.path.exists(png):
                raise FileNotFoundError(png)
            replacements[target_name] = open(png, 'rb').read()

        parent = os.path.dirname(os.path.abspath(args.output))
        fd, temp_path = tempfile.mkstemp(suffix='.docx', dir=parent)
        os.close(fd)
        try:
            with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as dst:
                for name in names:
                    data = replacements.get(name, src.read(name))
                    dst.writestr(name, data)
            os.replace(temp_path, args.output)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    print(f'replaced {expected} images: {args.start}-{args.end}')


if __name__ == '__main__':
    main()
