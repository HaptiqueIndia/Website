# ROOT Canonical Technical Paper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce an editable A4 DOCX and a visually verified, print-ready PDF that serve as the canonical D0.1 ROOT technical concept paper while retaining the existing HTML as a companion-only reader.

**Architecture:** A Python content module holds publication metadata, sections, claims, references, disclosures, and evaluation protocols as the single authoring source for the canonical document. A deterministic python-docx builder applies an explicit A4 engineering-report token map, creates the DOCX, and uses the bundled render workflow to emit the canonical PDF. Python structural tests inspect DOCX/PDF content and geometry; the existing Node production-boundary test prevents HTML, DOCX, PDF, and paper-specific markers from entering `dist/`.

**Tech Stack:** Bundled Python 3, python-docx, Pillow, lxml, pypdf, pdfplumber, LibreOffice through the Documents renderer, Poppler, Node.js built-in test runner.

**Spec:** `docs/superpowers/specs/2026-08-25-root-whitepaper-design.md`

## Global Constraints

- Canonical PDF: `output/pdf/ROOT-Technical-Concept-Paper-D0.1.pdf`.
- Editable source: `output/docx/ROOT-Technical-Concept-Paper-D0.1.docx`.
- Companion reader: `whitepaper.html`, explicitly labelled `Companion web edition`.
- All artifacts use document ID `ROOT-TCP-001`, revision `D0.1`, issue date `25 August 2026`, evidence cutoff `25 August 2026`, status `Developer preview`, owner `Haptique Electronics Pvt. Ltd.`, and reviewer `Not yet assigned`.
- A4 portrait: 210 x 297 mm; margins 20 mm; header/footer distance 10 mm; usable width 170 mm / 9638 DXA.
- Base style: Arial 10 pt, 1.18 line spacing, 5 pt after; title 28 pt; Heading 1 16 pt; Heading 2 13 pt; Heading 3 11.5 pt.
- Colors: ink `#20201F`, muted `#676761`, coral `#D85F48`, line `#D7D4CD`, light fill `#F2F1ED`, white `#FFFFFF`.
- Use ASCII hyphens only; do not introduce U+2011, U+2013, or U+2014.
- Do not add Panasonic recognition or patent wording without verified evidence.
- Do not report prototype performance; evidence statuses remain `Cited background`, `Hypothesis / design target`, `Planned evaluation`, or controlled disclosure.
- The PDF, DOCX, and HTML remain excluded from `dist/`.
- Use the bundled runtime paths:
  - Python: `/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
  - Node: `/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`
  - Document skill root: `/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/documents/skills/documents`
  - PDF skill root: `/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/pdf/skills/pdf`

---

## File Structure

- Create `paper/root_technical_paper.py`: immutable publication content, metadata, claim register, references, and protocol definitions.
- Create `scripts/build_technical_paper.py`: DOCX builder, style/token setup, section/figure/table assembly, field insertion, and output orchestration.
- Create `tests/test_technical_paper.py`: content, DOCX structure, PDF geometry/text, metadata, and publication-boundary tests.
- Create `output/docx/ROOT-Technical-Concept-Paper-D0.1.docx`: editable canonical source artifact.
- Create `output/pdf/ROOT-Technical-Concept-Paper-D0.1.pdf`: canonical review artifact.
- Modify `whitepaper.html`: label the page as the companion web edition.
- Modify `tests/whitepaper.test.mjs`: require the companion label and canonical metadata parity.
- Modify `tests/production-boundary.test.mjs`: reject DOCX/PDF artifacts, output paths, and canonical paper markers in `dist/`.
- Do not commit `tmp/technical-paper-render/`: DOCX/PDF render intermediates and page PNGs are QA-only.

### Task 1: Canonical Content Model and Contract

**Files:**
- Create: `paper/root_technical_paper.py`
- Create: `tests/test_technical_paper.py`

**Interfaces:**
- Produces: `DOCUMENT: dict`, `SECTIONS: tuple[dict, ...]`, `CLAIMS: tuple[dict, ...]`, `REFERENCES: tuple[dict, ...]`, `PROTOCOLS: tuple[dict, ...]`, and `FORBIDDEN_COPY: tuple[str, ...]`.
- Consumes: approved wording and evidence classifications from the specification and `whitepaper.html`.

- [ ] **Step 1: Write the failing content-model tests**

Create `tests/test_technical_paper.py` with:

```python
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "paper" / "root_technical_paper.py"

class ContentModelTests(unittest.TestCase):
    def load_module(self):
        spec = importlib.util.spec_from_file_location("root_technical_paper", MODULE_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_document_control_is_complete(self):
        paper = self.load_module()
        self.assertEqual(paper.DOCUMENT["document_id"], "ROOT-TCP-001")
        self.assertEqual(paper.DOCUMENT["revision"], "D0.1")
        self.assertEqual(paper.DOCUMENT["issue_date"], "25 August 2026")
        self.assertEqual(paper.DOCUMENT["evidence_cutoff"], "25 August 2026")
        self.assertEqual(paper.DOCUMENT["publication_status"], "Developer preview")
        self.assertEqual(paper.DOCUMENT["technical_reviewer"], "Not yet assigned")

    def test_required_sections_are_ordered(self):
        paper = self.load_module()
        self.assertEqual(
            [section["id"] for section in paper.SECTIONS],
            [
                "abstract", "room-level-problem", "architecture", "connectivity",
                "sensing", "placement", "evaluation", "limitations", "company",
                "references", "revision-history",
            ],
        )

    def test_claim_register_has_required_fields(self):
        paper = self.load_module()
        required = {"id", "status", "scope", "revision", "evidence_id", "evidence_date", "wording"}
        self.assertTrue({"CB-01", "HT-01", "HT-02", "PE-01", "PE-07"}.issubset(
            {claim["id"] for claim in paper.CLAIMS}
        ))
        for claim in paper.CLAIMS:
            self.assertTrue(required.issubset(claim))

    def test_copy_respects_disclosure_boundary(self):
        paper = self.load_module()
        corpus = "\n".join(
            [section["title"] + "\n" + "\n".join(section["paragraphs"]) for section in paper.SECTIONS]
        ).lower()
        for phrase in paper.FORBIDDEN_COPY:
            self.assertNotIn(phrase.lower(), corpus)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests/test_technical_paper.py -v
```

Expected: FAIL because `paper/root_technical_paper.py` does not exist.

- [ ] **Step 3: Implement the publication content module**

Create `paper/root_technical_paper.py` using immutable tuples and dictionaries. Include:

```python
DOCUMENT = {
    "title": "ROOT: A local architecture for room-level AC comfort",
    "subtitle": "Technical concept paper",
    "document_id": "ROOT-TCP-001",
    "revision": "D0.1",
    "publication_status": "Developer preview",
    "owner": "Haptique Electronics Pvt. Ltd.",
    "technical_reviewer": "Not yet assigned",
    "issue_date": "25 August 2026",
    "last_reviewed": "25 August 2026",
    "evidence_cutoff": "25 August 2026",
    "hardware_revision": "Not yet assigned",
    "firmware_revision": "Not yet assigned",
}

EVIDENCE_STATUSES = (
    "Cited background",
    "Implemented prototype behavior",
    "Hypothesis / design target",
    "Planned evaluation",
)

FORBIDDEN_COPY = (
    "acceleration award", "affiliated with panasonic", "patent pending",
    "breathing sense", "zero outages", "perfect coverage",
    "universal compatibility", "fully-tested", "100% local",
)
```

Port the approved abstract, technical prose, controlled disclosures, two references, seven planned protocols, and revision history from `whitepaper.html`. Preserve claim IDs and classify all unmeasured ROOT behavior as hypotheses/design targets or planned evaluations.

- [ ] **Step 4: Run the content-model tests**

Run the unittest command from Step 2.

Expected: all four tests PASS.

- [ ] **Step 5: Commit the content model**

```bash
git add paper/root_technical_paper.py tests/test_technical_paper.py
git commit -m "feat: define ROOT technical paper content model"
```

### Task 2: Deterministic A4 DOCX Builder

**Files:**
- Create: `scripts/build_technical_paper.py`
- Modify: `tests/test_technical_paper.py`
- Create: `output/docx/ROOT-Technical-Concept-Paper-D0.1.docx`

**Interfaces:**
- Consumes: all constants from `paper.root_technical_paper`.
- Produces: `build_docx(output_path: pathlib.Path, toc_page_map: dict[str, int] | None = None) -> pathlib.Path` and the final DOCX.
- Named internal helpers: `set_run_font`, `configure_styles`, `configure_section`, `set_cell_margins`, `set_fixed_table_geometry`, `add_cover`, `add_front_matter`, `add_technical_body`, `add_back_matter`, and `add_field`.

- [ ] **Step 1: Mark the DOCX artifact operation**

Run exactly once before the first DOCX authoring command:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/documents/skills/documents/container_tools/mark_artifact_operation_started.mjs --operation-kind create --expected-output-count 1 --output-format docx
```

Expected: successful operation marker.

- [ ] **Step 2: Add failing DOCX structure tests**

Extend `tests/test_technical_paper.py`:

```python
from docx import Document
from docx.enum.section import WD_SECTION
from docx.shared import Mm

DOCX_PATH = ROOT / "output" / "docx" / "ROOT-Technical-Concept-Paper-D0.1.docx"

class DocxArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = Document(DOCX_PATH)

    def test_a4_geometry(self):
        section = self.document.sections[0]
        self.assertAlmostEqual(section.page_width.mm, 210, delta=0.2)
        self.assertAlmostEqual(section.page_height.mm, 297, delta=0.2)
        for margin in (section.top_margin, section.right_margin, section.bottom_margin, section.left_margin):
            self.assertAlmostEqual(margin.mm, 20, delta=0.2)

    def test_heading_structure_and_metadata(self):
        text = "\n".join(p.text for p in self.document.paragraphs)
        for required in (
            "ROOT: A local architecture for room-level AC comfort",
            "ROOT-TCP-001", "D0.1", "Abstract", "1. The room-level problem",
            "2. System architecture", "7. Evaluation methodology",
            "8. Limitations, privacy, and safety boundary", "References", "Revision history",
        ):
            self.assertIn(required, text)
        self.assertEqual(sum(p.style.name == "Title" for p in self.document.paragraphs), 1)

    def test_tables_have_repeating_header_rows(self):
        self.assertGreaterEqual(len(self.document.tables), 4)
        for table in self.document.tables:
            first_row_xml = table.rows[0]._tr.xml
            self.assertIn("tblHeader", first_row_xml)
```

- [ ] **Step 3: Run the DOCX tests to verify they fail**

Run:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests/test_technical_paper.py -v
```

Expected: FAIL because the DOCX does not exist.

- [ ] **Step 4: Implement the builder and exact token map**

Create `scripts/build_technical_paper.py`. Configure A4 geometry and styles through python-docx, setting both `run.font.name` and OOXML `w:rFonts`. Encode this token map as a module constant:

```python
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
```

The builder must:

- create output directories without deleting unrelated files;
- set A4 portrait geometry and explicit margins;
- create a restrained cover using `editorial_cover` structure with left alignment and no full-bleed image;
- add document-control, revision, nomenclature, claim-register, protocol, and reference tables with fixed DXA widths and repeating header rows;
- add a static contents list in document order; when `toc_page_map` is provided, print the mapped page number for each numbered section and appendix;
- use real Heading 1/2/3 styles and real list numbering;
- add running headers with abbreviated title and revision;
- add footers with document ID, status, and PAGE/NUMPAGES fields;
- set `keep_with_next` on headings and captions;
- assign figure and table captions through a dedicated `Caption` style;
- insert page breaks only at front-matter and appendix boundaries;
- write the DOCX to a temporary path, then replace the stable output atomically.

- [ ] **Step 5: Build the DOCX**

Run:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_technical_paper.py --docx-only
```

Expected: creates `output/docx/ROOT-Technical-Concept-Paper-D0.1.docx`.

- [ ] **Step 6: Audit table geometry**

Run:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/documents/skills/documents/scripts/table_geometry.py output/docx/ROOT-Technical-Concept-Paper-D0.1.docx
```

Expected: fixed `tblW`, `tblGrid`, and `tcW` values agree for every table; no geometry mismatch.

- [ ] **Step 7: Run the DOCX tests**

Run the unittest command from Step 3.

Expected: content-model and DOCX tests PASS.

- [ ] **Step 8: Commit the DOCX builder**

```bash
git add scripts/build_technical_paper.py tests/test_technical_paper.py output/docx/ROOT-Technical-Concept-Paper-D0.1.docx
git commit -m "feat: build canonical ROOT technical paper DOCX"
```

### Task 3: Figures, Protocol Matrix, and Evidence Presentation

**Files:**
- Modify: `scripts/build_technical_paper.py`
- Modify: `tests/test_technical_paper.py`
- Rebuild: `output/docx/ROOT-Technical-Concept-Paper-D0.1.docx`
- Reuse: `assets/root-matte-technical-cutaway-v1.png`

**Interfaces:**
- Consumes: `CLAIMS`, `PROTOCOLS`, and `REFERENCES`.
- Produces: `add_control_loop_figure(document)`, `add_product_figure(document, image_path)`, `add_protocol_matrix(document)`, and `add_claim_register(document)`.

- [ ] **Step 1: Add failing evidence-presentation tests**

Add tests asserting:

```python
    def test_figures_and_protocols_are_complete(self):
        text = "\n".join(p.text for p in self.document.paragraphs)
        for marker in (
            "Figure 1. Conceptual four-stage control loop",
            "Figure 2. Illustrative ROOT product cutaway",
            "Conceptual architecture, not a measured result",
            "Illustrative image, not component or production evidence",
            "PE-01", "PE-02", "PE-03", "PE-04", "PE-05", "PE-06", "PE-07",
        ):
            self.assertIn(marker, text)

    def test_claim_register_includes_evidence_fields(self):
        table_text = "\n".join(
            cell.text for table in self.document.tables for row in table.rows for cell in row.cells
        )
        for heading in ("Claim ID", "Status", "Scope", "Revision", "Evidence ID", "Evidence date"):
            self.assertIn(heading, table_text)
```

- [ ] **Step 2: Run the new tests to verify they fail**

Run the unittest command.

Expected: FAIL because figures/protocols are incomplete.

- [ ] **Step 3: Implement the technical figures and matrices**

Implement Figure 1 as a four-column Word table with `Sense -> Interpret -> Decide -> Transmit`, numbered stages, short technical descriptions, and an adjacent text description. Treat it as a figure, remove exterior marketing-card styling, and caption it exactly:

`Figure 1. Conceptual four-stage control loop. Conceptual architecture, not a measured result. Status: Hypothesis / design target. Claim ID: HT-01.`

Insert `assets/root-matte-technical-cutaway-v1.png` at no more than 120 mm wide, preserve aspect ratio, add descriptive alternative text in the drawing properties, and caption it exactly:

`Figure 2. Illustrative ROOT product cutaway. Illustrative image, not component or production evidence. Status: Hypothesis / design target. Claim ID: HT-03.`

Create a seven-row planned-evaluation matrix with columns `ID`, `Evaluation`, `Conditions and comparator`, `Primary outputs`, and `Acceptance rule`. Keep acceptance rules described as `Pre-registered before testing` because no threshold has been approved.

Create a claim-register appendix with every claim and evidence field from the content module.

- [ ] **Step 4: Rebuild and rerun tests**

Run:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_technical_paper.py --docx-only
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests/test_technical_paper.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit the evidence presentation**

```bash
git add scripts/build_technical_paper.py tests/test_technical_paper.py output/docx/ROOT-Technical-Concept-Paper-D0.1.docx
git commit -m "feat: add evidence figures and protocol matrix"
```

### Task 4: Canonical PDF Export and Artifact Verification

**Files:**
- Modify: `scripts/build_technical_paper.py`
- Modify: `tests/test_technical_paper.py`
- Create: `output/pdf/ROOT-Technical-Concept-Paper-D0.1.pdf`
- Create during QA only: `tmp/technical-paper-render/page-*.png`

**Interfaces:**
- Produces: `render_canonical_pdf(docx_path, render_dir, pdf_path) -> pathlib.Path`, `extract_heading_pages(pdf_path) -> dict[str, int]`, and CLI modes `--docx-only`, `--pdf-only`, or both by default.
- Uses: bundled `render_docx.py --emit_pdf`, `pypdf.PdfReader`, and `pdfplumber`.

- [ ] **Step 1: Mark the PDF artifact operation**

Run exactly once before the first PDF authoring command:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/pdf/skills/pdf/container_tools/mark_artifact_operation_started.mjs --operation-kind create --expected-output-count 1 --output-format pdf
```

Expected: successful operation marker.

- [ ] **Step 2: Add failing PDF validation tests**

Extend `tests/test_technical_paper.py`:

```python
from pypdf import PdfReader
import pdfplumber

PDF_PATH = ROOT / "output" / "pdf" / "ROOT-Technical-Concept-Paper-D0.1.pdf"

class PdfArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = PdfReader(PDF_PATH)
        with pdfplumber.open(PDF_PATH) as pdf:
            cls.text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    def test_page_geometry_and_count(self):
        self.assertGreaterEqual(len(self.reader.pages), 12)
        self.assertLessEqual(len(self.reader.pages), 16)
        for page in self.reader.pages:
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            self.assertAlmostEqual(width, 595.28, delta=1.0)
            self.assertAlmostEqual(height, 841.89, delta=1.0)

    def test_required_pdf_content(self):
        for marker in (
            "ROOT-TCP-001", "D0.1", "Developer preview", "Abstract",
            "System architecture", "Evaluation methodology",
            "Limitations, privacy, and safety boundary", "References",
            "Revision history", "CB-01", "HT-01", "PE-07",
        ):
            self.assertIn(marker, self.text)

    def test_table_of_contents_has_page_numbers(self):
        self.assertRegex(
            self.text,
            r"Table of contents[\s\S]{0,5000}1\. The room-level problem[ .]+[0-9]+",
        )

    def test_pdf_has_no_forbidden_copy(self):
        lowered = self.text.lower()
        for phrase in ("acceleration award", "affiliated with panasonic", "patent pending",
                       "breathing sense", "zero outages", "perfect coverage"):
            self.assertNotIn(phrase, lowered)
```

- [ ] **Step 3: Run the PDF tests to verify they fail**

Run the unittest command.

Expected: FAIL because the PDF does not exist.

- [ ] **Step 4: Implement bundled rendering and stable PDF copy**

Have the default build use a deterministic two-pass publication flow:

1. build a provisional DOCX without page numbers in the static contents list;
2. render the provisional DOCX to a provisional PDF;
3. have `extract_heading_pages` use pdfplumber to locate each numbered heading and return its one-based page number;
4. require a page number for every numbered section and appendix;
5. rebuild the stable DOCX with the complete `toc_page_map`;
6. render that stable DOCX into the canonical PDF.

Have `render_canonical_pdf`:

1. clean only the supplied render directory below `tmp/technical-paper-render/`;
2. run bundled `render_docx.py` with `TMPDIR=/private/tmp`, the supplied output directory, and `--emit_pdf`;
3. require non-empty `page-*.png` files and emitted PDF;
4. atomically copy the emitted PDF to `output/pdf/ROOT-Technical-Concept-Paper-D0.1.pdf` for the final pass;
5. reopen the copied PDF with pypdf and reject non-A4 pages or an empty document.

The `--pdf-only` mode must call `render_canonical_pdf` using the existing stable DOCX without rebuilding or modifying it. The default mode builds the DOCX and then exports the PDF.

- [ ] **Step 5: Build both canonical artifacts**

Run:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_technical_paper.py
```

Expected: DOCX, PDF, and page PNGs are generated at their defined paths.

- [ ] **Step 6: Run structural tests**

Run the unittest command.

Expected: all content, DOCX, and PDF tests PASS.

- [ ] **Step 7: Commit the canonical PDF workflow**

```bash
git add scripts/build_technical_paper.py tests/test_technical_paper.py output/pdf/ROOT-Technical-Concept-Paper-D0.1.pdf output/docx/ROOT-Technical-Concept-Paper-D0.1.docx
git commit -m "feat: export verified ROOT technical paper PDF"
```

### Task 5: Companion Label and Production Boundary

**Files:**
- Modify: `whitepaper.html`
- Modify: `tests/whitepaper.test.mjs`
- Modify: `tests/production-boundary.test.mjs`

**Interfaces:**
- Produces: explicit HTML companion status and negative production assertions for all canonical artifacts.

- [ ] **Step 1: Add failing companion and boundary assertions**

In `tests/whitepaper.test.mjs`, require:

```javascript
assert.match(page, /Companion web edition/i);
assert.match(page, /ROOT-TCP-001/i);
assert.match(page, /D0\.1/i);
assert.match(page, /25 August 2026/i);
```

In `tests/production-boundary.test.mjs`, add:

```javascript
assert.doesNotMatch(outputText, /ROOT-Technical-Concept-Paper-D0\.1\.(?:pdf|docx)/i);
assert.doesNotMatch(outputText, /ROOT-TCP-001/i);
assert.doesNotMatch(outputText, /Companion web edition/i);
assert.equal(await pathExists(join(outputRoot, "output")), false);
```

- [ ] **Step 2: Run tests to verify the companion assertion fails**

Run:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --test tests/whitepaper.test.mjs tests/production-boundary.test.mjs
```

Expected: whitepaper contract FAILS because the companion label is absent; production boundary remains green.

- [ ] **Step 3: Add the companion label**

Change the HTML publication-status copy from a generic developer preview to:

`Companion web edition / D0.1`

Add a nearby sentence:

`The canonical review artifact is the versioned technical-paper PDF. Downloads remain disabled during local developer review.`

Do not add a PDF or DOCX link while the production release gate remains closed.

- [ ] **Step 4: Run Node contracts**

Run the Node command from Step 2.

Expected: both tests PASS and `dist/` contains no canonical artifact or marker.

- [ ] **Step 5: Commit the companion boundary**

```bash
git add whitepaper.html tests/whitepaper.test.mjs tests/production-boundary.test.mjs
git commit -m "test: enforce technical paper publication boundary"
```

### Task 6: Metadata, Accessibility, and Visual QA

**Files:**
- Modify as required: `scripts/build_technical_paper.py`
- Rebuild: `output/docx/ROOT-Technical-Concept-Paper-D0.1.docx`
- Rebuild: `output/pdf/ROOT-Technical-Concept-Paper-D0.1.pdf`
- QA only: `tmp/technical-paper-render/page-*.png`

**Interfaces:**
- Consumes: final DOCX/PDF.
- Produces: metadata-scrubbed artifacts, accessibility report, complete visual-review evidence, and final green verification.

- [ ] **Step 1: Scrub unapproved metadata**

Run:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/documents/skills/documents/scripts/privacy_scrub.py output/docx/ROOT-Technical-Concept-Paper-D0.1.docx --out /private/tmp/ROOT-Technical-Concept-Paper-D0.1-scrubbed.docx
```

Replace the final DOCX with the scrubbed file only after reopening it successfully. Re-render the scrubbed DOCX so the final PDF is derived from the final DOCX, not the pre-scrub version.

- [ ] **Step 2: Run the DOCX accessibility audit**

Run:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/documents/skills/documents/scripts/a11y_audit.py output/docx/ROOT-Technical-Concept-Paper-D0.1.docx --out_json tmp/technical-paper-a11y.json
```

Expected: no missing image alt text, no unmarked header rows, and no skipped heading levels. If header rows are unmarked, run `a11y_audit.py` with `--fix_table_headers first_row --out /private/tmp/ROOT-Technical-Concept-Paper-D0.1-a11y.docx`, reopen the result, and replace the final DOCX. Fix missing image alt text or skipped heading levels in `scripts/build_technical_paper.py`; do not use filename-derived alt text for the product figure.

- [ ] **Step 3: Render the final DOCX and PDF page sets**

Export the PDF from the final scrubbed DOCX without rebuilding it, then independently render the canonical PDF:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_technical_paper.py --pdf-only
rm -rf /private/tmp/root-technical-paper-pdf-pages
mkdir -p /private/tmp/root-technical-paper-pdf-pages
PATH="/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override:/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback:$PATH" pdftoppm -png output/pdf/ROOT-Technical-Concept-Paper-D0.1.pdf /private/tmp/root-technical-paper-pdf-pages/page
```

Expected: one DOCX-render PNG and one independent PDF-render PNG for every PDF page.

- [ ] **Step 4: Inspect every rendered page**

Create contact sheets from the complete PNG sets and inspect both the contact sheets and every full-resolution page. Reject and repair:

- clipped or overlapping text;
- orphaned headings or captions;
- split metadata rows;
- table headers missing after a page break;
- columns that are too narrow for their content;
- excessive blank space caused by forced page breaks;
- inconsistent header/footer placement;
- unreadable figure captions;
- false color-only evidence distinctions;
- font substitution;
- non-A4 pages or mixed orientation.

Repeat build, render, and inspection after every repair.

- [ ] **Step 5: Run final automated verification**

Run:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests/test_technical_paper.py -v
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --test tests/*.test.mjs
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check script.js
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check scripts/build-production.mjs
git diff --check
```

Expected: all Python and Node tests PASS, syntax checks exit 0, and `git diff --check` reports no errors.

- [ ] **Step 6: Verify production exclusion from a fresh build**

Run:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node scripts/build-production.mjs
test ! -e dist/whitepaper.html
test ! -e dist/output
! rg -n "ROOT-TCP-001|ROOT-Technical-Concept-Paper|Companion web edition|ac-whitepaper-" dist
```

Expected: all checks exit 0.

- [ ] **Step 7: Commit final publication artifacts**

```bash
git add scripts/build_technical_paper.py tests/test_technical_paper.py output/docx/ROOT-Technical-Concept-Paper-D0.1.docx output/pdf/ROOT-Technical-Concept-Paper-D0.1.pdf
git commit -m "docs: finalize ROOT technical concept paper"
```

- [ ] **Step 8: Request final review**

Use the requesting-code-review skill to audit the implementation against the specification, then run verification-before-completion before reporting the DOCX and PDF as final.
