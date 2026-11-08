# -*- coding: utf-8 -*-
"""Convert Отчёт.md to a simple Word document."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Отчёт.md"
OUT = Path(r"C:\Users\Godzilla\Desktop\Отчёт_обновлённый.docx")


def clean_line(text: str) -> str:
    text = text.replace("—", ": ")
    text = text.replace("«", '"').replace("»", '"')
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r":\s*:", ":", text)
    return text


def setup_document() -> Document:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(3)
    section.right_margin = Cm(1.5)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(14)
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    normal.paragraph_format.first_line_indent = Cm(1.25)
    return doc


def style_run(run, size=14, bold=False):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.font.bold = bold


def add_heading(doc: Document, text: str, level: int):
    p = doc.add_heading(clean_line(text), level=level)
    for run in p.runs:
        style_run(run, size=16 if level == 0 else 14, bold=True)
    p.paragraph_format.first_line_indent = Cm(0)
    if level == 0:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return p


def add_paragraph(doc: Document, text: str):
    p = doc.add_paragraph(clean_line(text))
    for run in p.runs:
        style_run(run)
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    return p


def add_bullet(doc: Document, text: str):
    p = doc.add_paragraph(clean_line(text), style="List Bullet")
    for run in p.runs:
        style_run(run)
    p.paragraph_format.first_line_indent = Cm(0)
    return p


def add_number(doc: Document, text: str):
    p = doc.add_paragraph(clean_line(text), style="List Number")
    for run in p.runs:
        style_run(run)
    p.paragraph_format.first_line_indent = Cm(0)
    return p


def parse_cells(line: str) -> list[str]:
    return [clean_line(cell) for cell in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\s*\|?[\s:|-]+\|[\s:|-|]*", line))


def add_table(doc: Document, rows: list[list[str]]) -> None:
    if not rows:
        return
    table = doc.add_table(rows=1, cols=len(rows[0]))
    table.style = "Table Grid"
    header_cells = table.rows[0].cells
    for idx, value in enumerate(rows[0]):
        header_cells[idx].text = value
        for run in header_cells[idx].paragraphs[0].runs:
            style_run(run, size=11, bold=True)
    for row in rows[1:]:
        cells = table.add_row().cells
        for idx, value in enumerate(row):
            cells[idx].text = value
            for run in cells[idx].paragraphs[0].runs:
                style_run(run, size=11)
    doc.add_paragraph()


def add_image(doc: Document, alt_text: str, image_ref: str) -> None:
    image_path = ROOT / image_ref
    if not image_path.exists():
        add_paragraph(doc, f"[Изображение отсутствует: {alt_text}]")
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(image_path), width=Cm(15.5))
    caption = doc.add_paragraph(clean_line(alt_text))
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.paragraph_format.first_line_indent = Cm(0)
    for run in caption.runs:
        style_run(run, size=12)


def convert(src: Path, out: Path) -> None:
    doc = setup_document()
    lines = src.read_text(encoding="utf-8").splitlines()

    index = 0
    while index < len(lines):
        raw = lines[index].rstrip()
        if not raw.strip():
            index += 1
            continue

        if raw.startswith("# ") and not raw.startswith("## "):
            add_heading(doc, raw[2:].strip(), 0)
        elif raw.startswith("## "):
            add_heading(doc, raw[3:].strip(), 1)
        elif raw.startswith("### "):
            add_heading(doc, raw[4:].strip(), 2)
        elif re.match(r"^\d+\.\s", raw):
            add_number(doc, re.sub(r"^\d+\.\s*", "", raw))
        elif raw.startswith("- "):
            add_bullet(doc, raw[2:].strip())
        elif raw.startswith("![") and "](" in raw and raw.endswith(")"):
            alt_text, image_ref = raw[2:].split("](", 1)
            add_image(doc, alt_text, image_ref[:-1])
        elif raw.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].rstrip().startswith("|"):
                candidate = lines[index].rstrip()
                if not is_table_separator(candidate):
                    table_lines.append(parse_cells(candidate))
                index += 1
            add_table(doc, table_lines)
            continue
        else:
            add_paragraph(doc, raw.strip())
        index += 1

    doc.save(out)


if __name__ == "__main__":
    convert(SRC, OUT)
    print("Saved report document.")
