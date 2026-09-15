"""Insert slide PNGs after free DOCX markers without resaving the document."""

import argparse
import copy
import json
import os
import re
import tempfile
import zipfile

from lxml import etree


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
PKG_R = "http://schemas.openxmlformats.org/package/2006/relationships"
IMAGE_REL = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
)
MARKER = re.compile(r"^Слайд(\s*№\s*\d*)?\s*$")


def paragraph_text(paragraph):
    return "".join(
        node.text or "" for node in paragraph.findall(f".//{{{W}}}t")
    ).strip()


def image_blips(element):
    return element.findall(f".//{{{A}}}blip")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("slide_dir")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--mapping")
    parser.add_argument("--donor-docx", help="DOCX with existing slide images to clone formatting from")
    args = parser.parse_args()

    with zipfile.ZipFile(args.source) as source:
        names = source.namelist()
        document = etree.fromstring(source.read("word/document.xml"))
        relationships = etree.fromstring(source.read("word/_rels/document.xml.rels"))

        paragraphs = list(document.iter(f"{{{W}}}p"))
        markers = [
            (position, paragraph)
            for position, paragraph in enumerate(paragraphs)
            if MARKER.match(paragraph_text(paragraph))
        ]
        occupied = []
        free = []
        donor = None
        for marker_index, (position, paragraph) in enumerate(markers):
            next_position = (
                markers[marker_index + 1][0]
                if marker_index + 1 < len(markers)
                else len(paragraphs)
            )
            between_paragraphs = paragraphs[position + 1 : next_position]
            between = [
                blip
                for candidate in between_paragraphs
                for blip in image_blips(candidate)
            ]
            if between:
                occupied.append(paragraph)
                if donor is None:
                    donor = next(
                        candidate
                        for candidate in between_paragraphs
                        if image_blips(candidate)
                    )
            else:
                free.append(paragraph)

        if donor is None and args.donor_docx:
            with zipfile.ZipFile(args.donor_docx) as donor_zip:
                donor_root = etree.fromstring(donor_zip.read("word/document.xml"))
            donor = next(
                (p for p in donor_root.iter(f"{{{W}}}p") if image_blips(p)),
                None,
            )
            if donor is None:
                raise ValueError("Donor DOCX has no image paragraphs")

        if donor is None:
            raise ValueError(
                "No existing slide image paragraph found for cloning. "
                "Use --donor-docx to provide a DOCX with slide images."
            )

        if args.mapping:
            with open(args.mapping, encoding="utf-8") as mapping_file:
                raw_mapping = json.load(mapping_file)["map"]
            mapping = [
                (int(marker_index), slide_numbers)
                for marker_index, slide_numbers in raw_mapping.items()
            ]
        else:
            count = args.end - args.start + 1
            if len(free) < count:
                raise ValueError(f"Need {count} free markers, found {len(free)}")
            free_positions = {
                paragraph: marker_index
                for marker_index, (_, paragraph) in enumerate(markers)
                if paragraph in free
            }
            mapping = [
                (free_positions[free[offset]], [slide_number])
                for offset, slide_number in enumerate(range(args.start, args.end + 1))
            ]

        numeric_rel_ids = []
        for relationship in relationships:
            match = re.fullmatch(r"rId(\d+)", relationship.get("Id", ""))
            if match:
                numeric_rel_ids.append(int(match.group(1)))
        next_rel_id = max(numeric_rel_ids, default=0) + 1

        doc_pr_ids = [
            int(node.get("id"))
            for node in document.findall(f".//{{{WP}}}docPr")
            if (node.get("id") or "").isdigit()
        ]
        next_doc_pr_id = max(doc_pr_ids, default=0) + 1

        additions = {}
        inserted = []
        for marker_index, slide_numbers in mapping:
            if marker_index >= len(markers):
                raise ValueError(f"Marker index {marker_index} outside {len(markers)} markers")
            marker_position, marker = markers[marker_index]
            next_position = (
                markers[marker_index + 1][0]
                if marker_index + 1 < len(markers)
                else len(paragraphs)
            )
            block_paragraphs = paragraphs[marker_position + 1 : next_position]
            insertion_point = next(
                (candidate for candidate in reversed(block_paragraphs) if image_blips(candidate)),
                marker,
            )
            for slide_number in slide_numbers:
                png_path = os.path.join(args.slide_dir, f"slide_{slide_number:03d}.png")
                if not os.path.exists(png_path):
                    raise FileNotFoundError(png_path)

                media_name = f"slide_batch_{slide_number:03d}.png"
                archive_name = f"word/media/{media_name}"
                while archive_name in names or archive_name in additions:
                    media_name = "new_" + media_name
                    archive_name = f"word/media/{media_name}"

                rel_id = f"rId{next_rel_id}"
                next_rel_id += 1
                relationship = etree.Element(f"{{{PKG_R}}}Relationship")
                relationship.set("Id", rel_id)
                relationship.set("Type", IMAGE_REL)
                relationship.set("Target", f"media/{media_name}")
                relationships.append(relationship)

                image_paragraph = copy.deepcopy(donor)
                blips = image_blips(image_paragraph)
                if len(blips) != 1:
                    raise ValueError(
                        f"Expected one image in donor paragraph, found {len(blips)}"
                    )
                blips[0].set(f"{{{R}}}embed", rel_id)
                for node in image_paragraph.findall(f".//{{{WP}}}docPr"):
                    node.set("id", str(next_doc_pr_id))
                    next_doc_pr_id += 1

                insertion_point.addnext(image_paragraph)
                insertion_point = image_paragraph
                with open(png_path, "rb") as image:
                    additions[archive_name] = image.read()
                inserted.append((marker_index, slide_number, rel_id, archive_name))

        replacements = {
            "word/document.xml": etree.tostring(
                document, xml_declaration=True, encoding="UTF-8", standalone=True
            ),
            "word/_rels/document.xml.rels": etree.tostring(
                relationships, xml_declaration=True, encoding="UTF-8", standalone=True
            ),
        }

        output_parent = os.path.dirname(os.path.abspath(args.output))
        fd, temp_path = tempfile.mkstemp(suffix=".docx", dir=output_parent)
        os.close(fd)
        try:
            with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target:
                for name in names:
                    target.writestr(name, replacements.get(name, source.read(name)))
                for name, data in additions.items():
                    target.writestr(name, data)
            os.replace(temp_path, args.output)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    print(f"occupied_before={len(occupied)} free_before={len(free)} inserted={len(inserted)}")
    for marker_index, slide_number, rel_id, archive_name in inserted:
        print(f"free[{marker_index}] <- slide {slide_number} ({rel_id}, {archive_name})")


if __name__ == "__main__":
    main()
