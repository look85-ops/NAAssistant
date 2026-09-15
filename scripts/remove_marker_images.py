"""Remove image paragraphs immediately following DOCX slide markers."""

import argparse
import re

from docx import Document


NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS_WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
MARKER = re.compile(r"^Слайд(\s*№\s*\d*)?\s*$")


def text(element):
    return "".join(
        node.text or "" for node in element.findall(f".//{{{NS_W}}}t")
    ).strip()


def has_image(element):
    return bool(
        element.findall(f".//{{{NS_WP}}}inline")
        or element.findall(f".//{{{NS_A}}}blip")
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    args = parser.parse_args()

    document = Document(args.source)
    removed = 0
    for paragraph in list(document.element.body.iter(f"{{{NS_W}}}p")):
        if not MARKER.match(text(paragraph)):
            continue
        following = paragraph.getnext()
        if following is not None and has_image(following):
            following.getparent().remove(following)
            removed += 1

    document.save(args.output)
    print(f"removed={removed}")


if __name__ == "__main__":
    main()
