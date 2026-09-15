"""Report where slide_batch images occur relative to scenario text."""

import argparse
import os
import zipfile

from lxml import etree


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_R = "http://schemas.openxmlformats.org/package/2006/relationships"


def text(paragraph):
    return "".join(
        node.text or "" for node in paragraph.findall(f".//{{{W}}}t")
    ).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("docx")
    parser.add_argument("output")
    args = parser.parse_args()

    with zipfile.ZipFile(args.docx) as archive:
        document = etree.fromstring(archive.read("word/document.xml"))
        rels = etree.fromstring(archive.read("word/_rels/document.xml.rels"))

    targets = {
        relationship.get("Id"): relationship.get("Target")
        for relationship in rels.findall(f"{{{PKG_R}}}Relationship")
    }
    paragraphs = list(document.iter(f"{{{W}}}p"))
    last_text = ""
    last_marker = ""
    lines = []
    for position, paragraph in enumerate(paragraphs):
        value = text(paragraph)
        if value:
            last_text = value
            if value.startswith("Слайд"):
                last_marker = value
        for blip in paragraph.findall(f".//{{{A}}}blip"):
            rel_id = blip.get(f"{{{R}}}embed")
            target = targets.get(rel_id, "")
            if "slide_batch_" not in target:
                continue
            slide = os.path.basename(target).replace("slide_batch_", "").replace(".png", "")
            lines.append(
                f"slide={slide} paragraph={position} marker={last_marker!r} "
                f"preceding_text={last_text[:180]!r} target={target}"
            )

    with open(args.output, "w", encoding="utf-8") as output:
        output.write("\n".join(lines))
    print(f"reported={len(lines)}")


if __name__ == "__main__":
    main()
