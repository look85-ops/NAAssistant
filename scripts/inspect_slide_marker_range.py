"""Write slide texts and scenario marker contexts for a numbered range."""

import argparse
import re
import zipfile
from xml.etree import ElementTree as ET


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
MARKER = re.compile(r"^Слайд(\s*№\s*\d*)?\s*$")


def paragraph_text(paragraph):
    return "".join(node.text or "" for node in paragraph.iter(f"{W}t")).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("docx")
    parser.add_argument("pptx")
    parser.add_argument("output")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()

    with zipfile.ZipFile(args.docx) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    paragraphs = [paragraph_text(node) for node in root.iter(f"{W}p")]
    marker_positions = [
        index for index, value in enumerate(paragraphs) if MARKER.match(value)
    ]

    with zipfile.ZipFile(args.pptx) as archive:
        slide_names = [
            name
            for name in archive.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        ]
        slide_names.sort(key=lambda name: int(re.search(r"\d+", name).group()))
        slides = {}
        for name in slide_names:
            number = int(re.search(r"slide(\d+)", name).group(1))
            if args.start <= number <= args.end:
                slide = ET.fromstring(archive.read(name))
                slides[number] = "".join(
                    node.text or "" for node in slide.iter(f"{A}t")
                ).strip()

    lines = []
    marker_start = args.start - 1
    for offset, slide_number in enumerate(range(args.start, args.end + 1)):
        marker_number = marker_start + offset
        position = marker_positions[marker_number]
        next_position = marker_positions[marker_number + 1]
        context = " ".join(
            value for value in paragraphs[position + 1 : next_position] if value
        )
        lines.extend(
            [
                f"PAIR {marker_number} -> SLIDE {slide_number}",
                f"SCENARIO: {context[:500]}",
                f"SLIDE: {slides[slide_number][:500]}",
                "",
            ]
        )

    with open(args.output, "w", encoding="utf-8") as output:
        output.write("\n".join(lines))


if __name__ == "__main__":
    main()
