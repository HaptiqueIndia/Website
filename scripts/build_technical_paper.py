#!/usr/bin/env python3
"""Build the canonical ROOT technical concept paper DOCX."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import pathlib
import sys
import tempfile
import zipfile
from collections.abc import Iterable, Sequence

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor, Twips


ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from paper.root_technical_paper import (  # noqa: E402
    CLAIMS,
    CONTROLLED_DISCLOSURES,
    DOCUMENT,
    EVIDENCE_STATUSES,
    FORBIDDEN_COPY,
    PROTOCOLS,
    REFERENCES,
    REVISION_HISTORY,
    SECTIONS,
)


TOKENS = {
    "page_mm": (210, 297),
    "margins_mm": (20, 20, 20, 20),
    "header_footer_mm": 10,
    "content_width_dxa": 9638,
    "font": "Arial",
    "body_pt": 10,
    "body_after_pt": 5,
    "body_line_spacing": 1.18,
    "title_pt": 28,
    "h1_pt": 16,
    "h2_pt": 13,
    "h3_pt": 11.5,
    "ink": "20201F",
    "muted": "676761",
    "coral": "D85F48",
    "line": "D7D4CD",
    "light_fill": "F2F1ED",
}

OUTPUT_PATH = ROOT / "output" / "docx" / "ROOT-Technical-Concept-Paper-D0.1.docx"
TABLE_INDENT_DXA = 120
CELL_MARGINS_DXA = {"top": 80, "bottom": 80, "start": 120, "end": 120}

DISPLAY_HEADINGS = {
    "abstract": "Abstract",
    "room-level-problem": "1. The room-level problem",
    "architecture": "2. System architecture",
    "connectivity": "3. Connectivity and local-control boundary",
    "sensing": "4. Sensing and infrared interface",
    "placement": "5. Placement and installation boundary",
    "claim-register": "6. Claim and evidence register",
    "evaluation": "7. Evaluation methodology",
    "limitations": "8. Limitations, privacy, and safety boundary",
    "company": "9. Company and document position",
    "references": "References",
    "revision-history": "Revision history",
    "appendix-a": "Appendix A. Controlled disclosures",
}

EVIDENCE_DEFINITIONS = {
    "Cited background": "A statement supported by an identified external source.",
    "Implemented prototype behavior": (
        "A status reserved for behavior demonstrated by a revision-linked prototype record; "
        "no claim in D0.1 is assigned this status."
    ),
    "Hypothesis / design target": "An intended behavior or bounded design thesis that remains unmeasured.",
    "Planned evaluation": "A claim framed as a protocol and acceptance decision to be completed later.",
}


def _rgb(hex_value: str) -> RGBColor:
    return RGBColor.from_string(hex_value)


def _ensure_child(parent, tag: str):
    child = parent.find(qn(tag))
    if child is None:
        child = OxmlElement(tag)
        parent.append(child)
    return child


def set_run_font(
    run,
    *,
    name: str = TOKENS["font"],
    size: float | None = None,
    color: str | None = None,
    bold: bool | None = None,
    italic: bool | None = None,
) -> None:
    """Set a run font in both python-docx and explicit OOXML font slots."""

    run.font.name = name
    r_pr = run._element.get_or_add_rPr()
    r_fonts = r_pr.rFonts
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.insert(0, r_fonts)
    for slot in ("ascii", "hAnsi", "eastAsia", "cs"):
        r_fonts.set(qn(f"w:{slot}"), name)
    if size is not None:
        run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = _rgb(color)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def _set_style_font(style, size: float, color: str, *, bold: bool = False, italic: bool = False) -> None:
    style.font.name = TOKENS["font"]
    style.font.size = Pt(size)
    style.font.color.rgb = _rgb(color)
    style.font.bold = bold
    style.font.italic = italic
    r_pr = style._element.get_or_add_rPr()
    r_fonts = r_pr.rFonts
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.insert(0, r_fonts)
    for slot in ("ascii", "hAnsi", "eastAsia", "cs"):
        r_fonts.set(qn(f"w:{slot}"), TOKENS["font"])


def configure_styles(document: Document) -> None:
    """Apply the A4 engineering-report style-sheet overrides."""

    styles = document.styles

    normal = styles["Normal"]
    _set_style_font(normal, TOKENS["body_pt"], TOKENS["ink"])
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(TOKENS["body_after_pt"])
    normal.paragraph_format.line_spacing = TOKENS["body_line_spacing"]
    normal.paragraph_format.widow_control = True

    title = styles["Title"]
    _set_style_font(title, TOKENS["title_pt"], TOKENS["ink"], bold=True)
    title.paragraph_format.space_before = Pt(0)
    title.paragraph_format.space_after = Pt(10)
    title.paragraph_format.line_spacing = 1.0
    title.paragraph_format.keep_with_next = True
    title_p_pr = title._element.get_or_add_pPr()
    title_border = title_p_pr.find(qn("w:pBdr"))
    if title_border is not None:
        title_p_pr.remove(title_border)

    subtitle = styles["Subtitle"]
    _set_style_font(subtitle, 13, TOKENS["muted"])
    subtitle.paragraph_format.space_before = Pt(0)
    subtitle.paragraph_format.space_after = Pt(18)
    subtitle.paragraph_format.line_spacing = 1.1
    subtitle.paragraph_format.keep_with_next = True

    heading_tokens = (
        ("Heading 1", TOKENS["h1_pt"], TOKENS["coral"], 18, 8),
        ("Heading 2", TOKENS["h2_pt"], TOKENS["ink"], 14, 6),
        ("Heading 3", TOKENS["h3_pt"], TOKENS["muted"], 10, 5),
    )
    for style_name, size, color, before, after in heading_tokens:
        style = styles[style_name]
        _set_style_font(style, size, color, bold=True)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.line_spacing = 1.05
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.widow_control = True
        p_pr = style._element.get_or_add_pPr()
        contextual_spacing = p_pr.find(qn("w:contextualSpacing"))
        if contextual_spacing is not None:
            p_pr.remove(contextual_spacing)

    caption = styles["Caption"]
    _set_style_font(caption, 8.5, TOKENS["muted"], bold=True)
    caption.paragraph_format.space_before = Pt(6)
    caption.paragraph_format.space_after = Pt(4)
    caption.paragraph_format.line_spacing = 1.0
    caption.paragraph_format.keep_with_next = True

    if "Cover Kicker" not in styles:
        styles.add_style("Cover Kicker", WD_STYLE_TYPE.PARAGRAPH)
    kicker = styles["Cover Kicker"]
    _set_style_font(kicker, 9, TOKENS["coral"], bold=True)
    kicker.paragraph_format.space_before = Pt(0)
    kicker.paragraph_format.space_after = Pt(12)
    kicker.paragraph_format.keep_with_next = True

    if "Lead" not in styles:
        styles.add_style("Lead", WD_STYLE_TYPE.PARAGRAPH)
    lead = styles["Lead"]
    _set_style_font(lead, 10.5, TOKENS["muted"], italic=True)
    lead.paragraph_format.space_before = Pt(0)
    lead.paragraph_format.space_after = Pt(7)
    lead.paragraph_format.line_spacing = TOKENS["body_line_spacing"]
    lead.paragraph_format.keep_with_next = True

    if "Table Text" not in styles:
        styles.add_style("Table Text", WD_STYLE_TYPE.PARAGRAPH)
    table_text = styles["Table Text"]
    _set_style_font(table_text, 8.1, TOKENS["ink"])
    table_text.paragraph_format.space_before = Pt(0)
    table_text.paragraph_format.space_after = Pt(1.5)
    table_text.paragraph_format.line_spacing = 1.05
    table_text.paragraph_format.widow_control = True

    if "Contents Entry" not in styles:
        styles.add_style("Contents Entry", WD_STYLE_TYPE.PARAGRAPH)
    toc = styles["Contents Entry"]
    _set_style_font(toc, 9.5, TOKENS["ink"])
    toc.paragraph_format.space_before = Pt(0)
    toc.paragraph_format.space_after = Pt(3)
    toc.paragraph_format.line_spacing = 1.05


def add_field(paragraph, field_code: str, placeholder: str = "1") -> None:
    """Append a simple Word field with stable cached display text."""

    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = f" {field_code} "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")

    run = paragraph.add_run()
    set_run_font(run, size=8, color=TOKENS["muted"])
    run._r.append(begin)
    run._r.append(instruction)
    run._r.append(separate)
    cached = paragraph.add_run(placeholder)
    set_run_font(cached, size=8, color=TOKENS["muted"])
    end_run = paragraph.add_run()
    set_run_font(end_run, size=8, color=TOKENS["muted"])
    end_run._r.append(end)


def _populate_header(header) -> None:
    header_p = header.paragraphs[0]
    header_p.clear()
    header_p.paragraph_format.space_after = Pt(0)
    run = header_p.add_run(f"ROOT | Room-level AC comfort | {DOCUMENT['revision']}")
    set_run_font(run, size=8, color=TOKENS["muted"], bold=True)


def _populate_footer(footer) -> None:
    footer_p = footer.paragraphs[0]
    footer_p.clear()
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_p.paragraph_format.space_before = Pt(0)
    prefix = footer_p.add_run(
        f"{DOCUMENT['document_id']}  |  {DOCUMENT['publication_status']}  |  Page "
    )
    set_run_font(prefix, size=8, color=TOKENS["muted"])
    add_field(footer_p, "PAGE")
    tail = footer_p.add_run(" of ")
    set_run_font(tail, size=8, color=TOKENS["muted"])
    add_field(footer_p, "NUMPAGES")


def _set_page_furniture(section) -> None:
    section.header.is_linked_to_previous = False
    _populate_header(section.header)
    section.footer.is_linked_to_previous = False
    _populate_footer(section.footer)


def configure_section(section) -> None:
    """Set deterministic A4 portrait geometry and running page furniture."""

    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width = Mm(TOKENS["page_mm"][0])
    section.page_height = Mm(TOKENS["page_mm"][1])
    top, right, bottom, left = TOKENS["margins_mm"]
    section.top_margin = Mm(top)
    section.right_margin = Mm(right)
    section.bottom_margin = Mm(bottom)
    section.left_margin = Mm(left)
    section.header_distance = Mm(TOKENS["header_footer_mm"])
    section.footer_distance = Mm(TOKENS["header_footer_mm"])
    _set_page_furniture(section)


def set_cell_margins(cell, **margins_dxa: int) -> None:
    """Set explicit Word cell margins."""

    resolved = dict(CELL_MARGINS_DXA)
    resolved.update({key: int(value) for key, value in margins_dxa.items()})
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = _ensure_child(tc_pr, "w:tcMar")
    for side in ("top", "bottom", "start", "end"):
        node = _ensure_child(tc_mar, f"w:{side}")
        node.set(qn("w:w"), str(resolved[side]))
        node.set(qn("w:type"), "dxa")


def _set_dxa_width(parent, tag: str, width: int) -> None:
    node = _ensure_child(parent, tag)
    node.set(qn("w:type"), "dxa")
    node.set(qn("w:w"), str(int(width)))


def set_fixed_table_geometry(table, column_widths_dxa: Sequence[int]) -> None:
    """Synchronize tblW, tblInd, tblGrid, and every tcW in DXA."""

    widths = [int(width) for width in column_widths_dxa]
    if not widths or any(width <= 0 for width in widths):
        raise ValueError("table column widths must be positive")
    if sum(widths) != TOKENS["content_width_dxa"]:
        raise ValueError("table column widths must sum to the A4 content width")

    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl_pr = table._tbl.tblPr
    _set_dxa_width(tbl_pr, "w:tblW", sum(widths))
    indent = _ensure_child(tbl_pr, "w:tblInd")
    indent.set(qn("w:type"), "dxa")
    indent.set(qn("w:w"), str(TABLE_INDENT_DXA))
    layout = _ensure_child(tbl_pr, "w:tblLayout")
    layout.set(qn("w:type"), "fixed")

    borders = _ensure_child(tbl_pr, "w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = _ensure_child(borders, f"w:{edge}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), "4")
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), TOKENS["line"])

    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)

    for index, width in enumerate(widths):
        table.columns[index].width = Twips(width)
    for row in table.rows:
        row.height = None
        for index, cell in enumerate(row.cells):
            cell.width = Twips(widths[index])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            _set_dxa_width(cell._tc.get_or_add_tcPr(), "w:tcW", widths[index])
            set_cell_margins(cell)


def _allocate_widths(weights: Sequence[float]) -> list[int]:
    total = TOKENS["content_width_dxa"]
    weight_total = float(sum(weights))
    widths = [int(round(total * weight / weight_total)) for weight in weights]
    widths[-1] += total - sum(widths)
    return widths


def _mark_repeating_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    marker = tr_pr.find(qn("w:tblHeader"))
    if marker is None:
        marker = OxmlElement("w:tblHeader")
        tr_pr.append(marker)
    marker.set(qn("w:val"), "true")


def _shade_cell(cell, fill: str) -> None:
    shading = _ensure_child(cell._tc.get_or_add_tcPr(), "w:shd")
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:color"), "auto")
    shading.set(qn("w:fill"), fill)


def _format_table(table) -> None:
    _mark_repeating_header(table.rows[0])
    for row_index, row in enumerate(table.rows):
        tr_pr = row._tr.get_or_add_trPr()
        if tr_pr.find(qn("w:cantSplit")) is None:
            tr_pr.append(OxmlElement("w:cantSplit"))
        for cell in row.cells:
            if row_index == 0:
                _shade_cell(cell, TOKENS["light_fill"])
            for paragraph in cell.paragraphs:
                paragraph.style = "Table Text"
                for run in paragraph.runs:
                    set_run_font(
                        run,
                        size=8.1,
                        color=TOKENS["ink"],
                        bold=row_index == 0,
                    )


def _add_table(
    document: Document,
    caption: str,
    headers: Sequence[str],
    rows: Iterable[Sequence[str]],
    weights: Sequence[float],
) -> None:
    caption_p = document.add_paragraph(caption, style="Caption")
    caption_p.paragraph_format.keep_with_next = True
    table = document.add_table(rows=1, cols=len(headers))
    for index, header in enumerate(headers):
        table.rows[0].cells[index].text = str(header)
    for values in rows:
        row = table.add_row()
        for index, value in enumerate(values):
            row.cells[index].text = str(value)
    set_fixed_table_geometry(table, _allocate_widths(weights))
    _format_table(table)
    after = document.add_paragraph()
    after.paragraph_format.space_after = Pt(2)


def _add_heading(document: Document, text: str, level: int = 1) -> None:
    paragraph = document.add_paragraph(text, style=f"Heading {level}")
    paragraph.paragraph_format.keep_with_next = True
    paragraph.paragraph_format.space_before = Pt({1: 18, 2: 14, 3: 10}[level])
    paragraph.paragraph_format.space_after = Pt({1: 8, 2: 6, 3: 5}[level])


def _add_section_copy(document: Document, section: dict, display_heading: str) -> None:
    _add_heading(document, display_heading)
    lead = document.add_paragraph(section["title"], style="Lead")
    lead.paragraph_format.keep_with_next = True
    for text in section["paragraphs"]:
        document.add_paragraph(text)


def _create_numbering(document: Document) -> dict[str, int]:
    numbering = document.part.numbering_part.element
    abstract_ids = [
        int(node.get(qn("w:abstractNumId")))
        for node in numbering.findall(qn("w:abstractNum"))
    ]
    num_ids = [int(node.get(qn("w:numId"))) for node in numbering.findall(qn("w:num"))]
    next_abstract = max(abstract_ids, default=0) + 1
    next_num = max(num_ids, default=0) + 1
    result: dict[str, int] = {}

    for kind, num_format, level_text in (
        ("bullet", "bullet", "•"),
        ("decimal", "decimal", "%1."),
    ):
        abstract = OxmlElement("w:abstractNum")
        abstract.set(qn("w:abstractNumId"), str(next_abstract))
        multi = OxmlElement("w:multiLevelType")
        multi.set(qn("w:val"), "singleLevel")
        abstract.append(multi)
        level = OxmlElement("w:lvl")
        level.set(qn("w:ilvl"), "0")
        start = OxmlElement("w:start")
        start.set(qn("w:val"), "1")
        level.append(start)
        fmt = OxmlElement("w:numFmt")
        fmt.set(qn("w:val"), num_format)
        level.append(fmt)
        text = OxmlElement("w:lvlText")
        text.set(qn("w:val"), level_text)
        level.append(text)
        justification = OxmlElement("w:lvlJc")
        justification.set(qn("w:val"), "left")
        level.append(justification)
        p_pr = OxmlElement("w:pPr")
        tabs = OxmlElement("w:tabs")
        tab = OxmlElement("w:tab")
        tab.set(qn("w:val"), "num")
        tab.set(qn("w:pos"), "540")
        tabs.append(tab)
        p_pr.append(tabs)
        ind = OxmlElement("w:ind")
        ind.set(qn("w:left"), "540")
        ind.set(qn("w:hanging"), "270")
        p_pr.append(ind)
        level.append(p_pr)
        r_pr = OxmlElement("w:rPr")
        r_fonts = OxmlElement("w:rFonts")
        r_fonts.set(qn("w:ascii"), TOKENS["font"])
        r_fonts.set(qn("w:hAnsi"), TOKENS["font"])
        r_pr.append(r_fonts)
        level.append(r_pr)
        abstract.append(level)
        numbering.append(abstract)

        num = OxmlElement("w:num")
        num.set(qn("w:numId"), str(next_num))
        abstract_ref = OxmlElement("w:abstractNumId")
        abstract_ref.set(qn("w:val"), str(next_abstract))
        num.append(abstract_ref)
        numbering.append(num)
        result[kind] = next_num
        next_abstract += 1
        next_num += 1
    return result


def _add_list_item(document: Document, text: str, num_id: int) -> None:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(4)
    paragraph.paragraph_format.line_spacing = TOKENS["body_line_spacing"]
    p_pr = paragraph._p.get_or_add_pPr()
    num_pr = _ensure_child(p_pr, "w:numPr")
    ilvl = _ensure_child(num_pr, "w:ilvl")
    ilvl.set(qn("w:val"), "0")
    num_id_node = _ensure_child(num_pr, "w:numId")
    num_id_node.set(qn("w:val"), str(num_id))
    run = paragraph.add_run(text)
    set_run_font(run, size=TOKENS["body_pt"], color=TOKENS["ink"])


def add_cover(document: Document) -> None:
    """Add a restrained, left-aligned editorial cover."""

    spacer = document.add_paragraph()
    spacer.paragraph_format.space_after = Pt(78)
    kicker = document.add_paragraph("TECHNICAL CONCEPT PAPER", style="Cover Kicker")
    kicker.alignment = WD_ALIGN_PARAGRAPH.LEFT
    title = document.add_paragraph(DOCUMENT["title"], style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    subtitle = document.add_paragraph(DOCUMENT["subtitle"], style="Subtitle")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.LEFT

    statement = document.add_paragraph()
    statement.paragraph_format.space_before = Pt(18)
    statement.paragraph_format.space_after = Pt(56)
    run = statement.add_run(
        "A developer-preview architecture and evaluation plan for bounded local room-comfort control."
    )
    set_run_font(run, size=11, color=TOKENS["ink"])

    metadata = document.add_paragraph()
    metadata.paragraph_format.space_before = Pt(0)
    metadata.paragraph_format.space_after = Pt(4)
    first = metadata.add_run(f"{DOCUMENT['document_id']}  |  {DOCUMENT['revision']}")
    set_run_font(first, size=10, color=TOKENS["ink"], bold=True)
    detail = document.add_paragraph()
    detail.paragraph_format.space_before = Pt(0)
    detail.paragraph_format.space_after = Pt(3)
    detail_run = detail.add_run(
        f"{DOCUMENT['publication_status']}  |  Issued {DOCUMENT['issue_date']}"
    )
    set_run_font(detail_run, size=9, color=TOKENS["muted"])
    owner = document.add_paragraph()
    owner.paragraph_format.space_before = Pt(0)
    owner_run = owner.add_run(DOCUMENT["owner"])
    set_run_font(owner_run, size=9, color=TOKENS["muted"])
    document.add_page_break()


def _toc_page(toc_page_map: dict[str, int] | None, key: str, heading: str) -> int | None:
    if toc_page_map is None:
        return None
    candidates = (key, heading, heading.split(".", 1)[0])
    for candidate in candidates:
        if candidate in toc_page_map:
            return int(toc_page_map[candidate])
    return None


def add_front_matter(document: Document) -> None:
    """Add document control, contents, and nomenclature front matter."""

    _add_heading(document, "Document control")
    control_rows = (
        ("Document ID", DOCUMENT["document_id"]),
        ("Revision", DOCUMENT["revision"]),
        ("Publication status", DOCUMENT["publication_status"]),
        ("Owner", DOCUMENT["owner"]),
        ("Technical reviewer", DOCUMENT["technical_reviewer"]),
        ("Issue date", DOCUMENT["issue_date"]),
        ("Last reviewed", DOCUMENT["last_reviewed"]),
        ("Evidence cutoff", DOCUMENT["evidence_cutoff"]),
        ("Hardware revision", DOCUMENT["hardware_revision"]),
        ("Firmware revision", DOCUMENT["firmware_revision"]),
    )
    _add_table(document, "Table 1. Document-control register.", ("Field", "Controlled value"), control_rows, (1.6, 4.9))

    document.add_page_break()
    _add_heading(document, "Contents")
    for key in (
        "abstract",
        "room-level-problem",
        "architecture",
        "connectivity",
        "sensing",
        "placement",
        "claim-register",
        "evaluation",
        "limitations",
        "company",
        "references",
        "revision-history",
        "appendix-a",
    ):
        heading = DISPLAY_HEADINGS[key]
        paragraph = document.add_paragraph(style="Contents Entry")
        paragraph.paragraph_format.tab_stops.add_tab_stop(Mm(170), WD_TAB_ALIGNMENT.RIGHT)
        paragraph.add_run(heading)
        if key == "appendix-a" or heading[:1].isdigit():
            mapped_page = _toc_page(getattr(document, "_root_toc_page_map", None), key, heading)
            if mapped_page is not None:
                paragraph.add_run(f"\t{mapped_page}")

    _add_heading(document, "Nomenclature and evidence status")
    nomenclature_rows = [
        ("AC", "Air conditioner."),
        ("IR", "Infrared command learning or transmission."),
        ("RSSI", "Bluetooth received signal strength; a coarse and environment-dependent input."),
        ("ROOT", "The proposed room-comfort controller described by this paper."),
    ]
    nomenclature_rows.extend((status, EVIDENCE_DEFINITIONS[status]) for status in EVIDENCE_STATUSES)
    _add_table(
        document,
        "Table 2. Nomenclature and evidence-status taxonomy.",
        ("Term or status", "Meaning in this revision"),
        nomenclature_rows,
        (2.0, 4.5),
    )
    document.add_page_break()


def _claim_rows() -> list[tuple[str, ...]]:
    rows = []
    for claim in CLAIMS:
        revision = (
            f"HW/FW: {claim['hardware_revision']}\n"
            f"Claim rev.: {claim['revision']}"
        )
        evidence = f"{claim['evidence_id']}\n{claim['evidence_date']}"
        wording = f"{claim['wording']}\nOwner: {claim['owner']} | Review: {claim['review_date']}"
        rows.append((claim["id"], claim["status"], claim["scope"], revision, evidence, wording))
    return rows


def _protocol_rows() -> list[tuple[str, ...]]:
    rows = []
    for protocol in PROTOCOLS:
        basis = f"{protocol['conditions']}\nComparator / ground truth: {protocol['comparator_ground_truth']}"
        outcomes = (
            "Primary: " + "; ".join(protocol["primary_outcomes"]) +
            "\nSecondary: " + "; ".join(protocol["secondary_outcomes"])
        )
        planning = (
            f"Interval: {protocol['sample_interval']} | Trials: {protocol['repeated_trials']}\n"
            f"Acceptance: {protocol['acceptance_criterion']} | Missing data: {protocol['exclusions_missing_data']}\n"
            f"Uncertainty: {protocol['uncertainty']} | Artifact: {protocol['retained_evidence_artifact']}\n"
            f"HW/FW: {protocol['hardware_revision']} / {protocol['firmware_revision']}\n"
            f"Report: {protocol['reporting_requirements']}"
        )
        rows.append((protocol["id"], f"{protocol['claim_id']}\n{protocol['title']}", basis, outcomes, planning))
    return rows


def add_technical_body(document: Document, numbering: dict[str, int]) -> None:
    """Add canonical technical sections, claim register, and evaluation protocols."""

    by_id = {section["id"]: section for section in SECTIONS}
    _add_section_copy(document, by_id["abstract"], DISPLAY_HEADINGS["abstract"])
    _add_section_copy(document, by_id["room-level-problem"], DISPLAY_HEADINGS["room-level-problem"])
    _add_section_copy(document, by_id["architecture"], DISPLAY_HEADINGS["architecture"])
    _add_heading(document, "Proposed control sequence", 2)
    for item in (
        "Sense temperature, humidity, and a bounded room-presence context near the occupied location.",
        "Estimate context without treating coarse proximity as a safety-relevant or irreversible signal.",
        "Decide locally within bounded setpoints, bounded command rates, manual override, and neutral fallback targets.",
        "Transmit a learned IR adjustment without treating the emitted command as confirmed AC state.",
    ):
        _add_list_item(document, item, numbering["decimal"])

    _add_section_copy(document, by_id["connectivity"], DISPLAY_HEADINGS["connectivity"])
    _add_section_copy(document, by_id["sensing"], DISPLAY_HEADINGS["sensing"])
    _add_section_copy(document, by_id["placement"], DISPLAY_HEADINGS["placement"])

    _add_heading(document, DISPLAY_HEADINGS["claim-register"])
    document.add_paragraph(
        "The register below separates cited background, unmeasured design targets, and planned evaluations. "
        "It contains no claim assigned to Implemented prototype behavior."
    )
    _add_table(
        document,
        "Table 3. Claim and evidence register.",
        ("ID", "Status", "Scope", "Revision basis", "Evidence", "Controlled wording"),
        _claim_rows(),
        (0.6, 1.15, 1.2, 1.3, 1.15, 2.1),
    )

    _add_section_copy(document, by_id["evaluation"], DISPLAY_HEADINGS["evaluation"])
    _add_heading(document, "Protocol-wide reporting rules", 2)
    for item in (
        "Identify prototype hardware and firmware revisions, conditions, comparator, ground truth, sample interval, and repeated trials.",
        "Fix primary and secondary outcomes, acceptance criteria, exclusions, missing-data handling, and uncertainty before testing.",
        "Retain evidence artifacts and report trial counts, negative results, protocol deviations, data location, and analysis version.",
        "Keep simulator outputs distinct from measured results.",
    ):
        _add_list_item(document, item, numbering["bullet"])
    _add_table(
        document,
        "Table 4. Planned evaluation protocol register.",
        ("Protocol", "Claim / title", "Conditions and comparator", "Outcomes", "Pre-registered planning contract"),
        _protocol_rows(),
        (0.95, 1.0, 1.4, 1.2, 1.95),
    )

    _add_section_copy(document, by_id["limitations"], DISPLAY_HEADINGS["limitations"])
    _add_section_copy(document, by_id["company"], DISPLAY_HEADINGS["company"])


def _reference_rows() -> list[tuple[str, ...]]:
    rows = []
    for reference in REFERENCES:
        creator = ", ".join(reference.get("authors", ())) or reference.get("organization", "")
        publication = f"{reference['publisher']} ({reference['publication_date']})"
        access = f"{reference['url']}\nAccessed {reference['access_date']}"
        rows.append((reference["id"], creator, reference["title"], publication, access))
    return rows


def add_back_matter(document: Document) -> None:
    """Add references, revision history, and controlled-disclosure appendix."""

    by_id = {section["id"]: section for section in SECTIONS}
    _add_section_copy(document, by_id["references"], DISPLAY_HEADINGS["references"])
    _add_table(
        document,
        "Table 5. Numbered reference register.",
        ("ID", "Author or organization", "Title", "Publication", "Locator and access"),
        _reference_rows(),
        (0.65, 1.65, 1.85, 1.0, 1.35),
    )

    _add_section_copy(document, by_id["revision-history"], DISPLAY_HEADINGS["revision-history"])
    revision_rows = [
        (
            item["revision"],
            item["issue_date"],
            item["owner"],
            item["reviewer"],
            item["evidence_cutoff"],
            item["summary"],
        )
        for item in REVISION_HISTORY
    ]
    _add_table(
        document,
        "Table 6. Revision history.",
        ("Revision", "Issue date", "Owner", "Reviewer", "Evidence cutoff", "Summary"),
        revision_rows,
        (0.7, 0.95, 1.3, 1.0, 1.0, 1.55),
    )

    document.add_page_break()
    _add_heading(document, DISPLAY_HEADINGS["appendix-a"])
    document.add_paragraph(
        "These controlled disclosures preserve the product's intended-use, safety, company, privacy, and omission boundaries."
    )
    disclosure_rows = [
        (
            item["id"],
            item["disclosure_type"],
            item["exact_wording"],
            item["source_or_approval_record"],
            item["owner"],
            f"Approved: {item['approval_date']}\nNext review: {item['next_review_date']}",
        )
        for item in CONTROLLED_DISCLOSURES
    ]
    _add_table(
        document,
        "Table 7. Controlled-disclosure register.",
        ("ID", "Type", "Exact wording", "Source / approval", "Owner", "Review control"),
        disclosure_rows,
        (0.55, 1.05, 2.1, 1.1, 0.85, 0.85),
    )


def _model_strings(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [text for nested in value.values() for text in _model_strings(nested)]
    if isinstance(value, (tuple, list)):
        return [text for nested in value for text in _model_strings(nested)]
    return []


def _validate_model() -> None:
    """Fail closed if the canonical content crosses a controlled-copy boundary."""

    corpus = "\n".join(
        _model_strings(
            (
                DOCUMENT,
                EVIDENCE_STATUSES,
                SECTIONS,
                CLAIMS,
                CONTROLLED_DISCLOSURES,
                REFERENCES,
                PROTOCOLS,
                REVISION_HISTORY,
            )
        )
    ).lower()
    for phrase in FORBIDDEN_COPY:
        if phrase.lower() in corpus:
            raise ValueError(f"forbidden copy in canonical model: {phrase}")
    if "Implemented prototype behavior" in {claim["status"] for claim in CLAIMS}:
        raise ValueError("D0.1 must not contain an implemented-prototype claim")


def _set_document_properties(document: Document) -> None:
    properties = document.core_properties
    timestamp = dt.datetime(2026, 8, 25, tzinfo=dt.timezone.utc)
    properties.title = DOCUMENT["title"]
    properties.subject = DOCUMENT["subtitle"]
    properties.author = DOCUMENT["owner"]
    properties.last_modified_by = DOCUMENT["owner"]
    properties.keywords = "ROOT, room comfort, split air conditioner, infrared control"
    properties.created = timestamp
    properties.modified = timestamp
    settings = document.settings._element
    update_fields = settings.find(qn("w:updateFields"))
    if update_fields is None:
        update_fields = OxmlElement("w:updateFields")
        settings.append(update_fields)
    update_fields.set(qn("w:val"), "true")


def _normalize_docx_archive(source_path: pathlib.Path, normalized_path: pathlib.Path) -> None:
    """Repack with a fixed ZIP timestamp so repeated builds are byte-stable."""

    fixed_time = (2026, 8, 25, 0, 0, 0)
    with zipfile.ZipFile(source_path, "r") as source, zipfile.ZipFile(
        normalized_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as target:
        for name in source.namelist():
            original = source.getinfo(name)
            info = zipfile.ZipInfo(name, fixed_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = original.external_attr
            info.internal_attr = original.internal_attr
            info.create_system = original.create_system
            target.writestr(info, source.read(name))


def build_docx(
    output_path: pathlib.Path,
    toc_page_map: dict[str, int] | None = None,
) -> pathlib.Path:
    """Build the canonical DOCX and atomically replace ``output_path``."""

    _validate_model()
    output_path = pathlib.Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    document = Document()
    document.settings.odd_and_even_pages_header_footer = False
    configure_styles(document)
    for section in document.sections:
        configure_section(section)
    _set_document_properties(document)
    document._root_toc_page_map = toc_page_map
    numbering = _create_numbering(document)

    add_cover(document)
    add_front_matter(document)
    add_technical_body(document, numbering)
    add_back_matter(document)

    raw_fd, raw_name = tempfile.mkstemp(prefix=f".{output_path.stem}-", suffix=".raw.docx", dir=output_path.parent)
    os.close(raw_fd)
    normalized_fd, normalized_name = tempfile.mkstemp(
        prefix=f".{output_path.stem}-", suffix=".normalized.docx", dir=output_path.parent
    )
    os.close(normalized_fd)
    raw_path = pathlib.Path(raw_name)
    normalized_path = pathlib.Path(normalized_name)
    try:
        document.save(raw_path)
        _normalize_docx_archive(raw_path, normalized_path)
        os.replace(normalized_path, output_path)
    finally:
        for temporary in (raw_path, normalized_path):
            if temporary.exists():
                temporary.unlink()
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docx-only", action="store_true", help="Build only the canonical DOCX.")
    parser.add_argument("--output", type=pathlib.Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    result = build_docx(args.output)
    print(result)


if __name__ == "__main__":
    main()
