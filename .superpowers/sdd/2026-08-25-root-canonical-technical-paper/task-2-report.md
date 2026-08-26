# Task 2 Report: Deterministic A4 DOCX Builder

## Status

Complete. The canonical DOCX builder, structural tests, and generated DOCX are implemented. The DOCX was rendered with the bundled Documents renderer and all 11 generated page PNGs were visually inspected. No final PDF was created in the repository; Task 4 retains PDF and final static-TOC ownership.

## Implementation

- Added `scripts/build_technical_paper.py` with the required public interface:

  ```python
  build_docx(output_path: pathlib.Path, toc_page_map: dict[str, int] | None = None) -> pathlib.Path
  ```

- Consumes every canonical constant from `paper.root_technical_paper`: `DOCUMENT`, `EVIDENCE_STATUSES`, `FORBIDDEN_COPY`, `SECTIONS`, `CLAIMS`, `CONTROLLED_DISCLOSURES`, `REFERENCES`, `PROTOCOLS`, and `REVISION_HISTORY`.
- Encodes the brief's exact `TOKENS` map and applies the named A4 engineering-report overrides: A4 portrait, 20 mm margins, 10 mm header/footer distance, 9,638 DXA content width, Arial type system, restrained coral/ink hierarchy, and fixed paragraph rhythm.
- Implements the required helpers: `set_run_font`, `configure_styles`, `configure_section`, `set_cell_margins`, `set_fixed_table_geometry`, `add_cover`, `add_front_matter`, `add_technical_body`, `add_back_matter`, and `add_field`.
- Uses the `compact_reference_guide` preset as the base and adapts `editorial_cover` into a restrained, left-aligned technical cover with no image and no inherited Title border.
- Uses one real `Title` paragraph and real `Heading 1`/`Heading 2` styles. Headings and captions have `keep_with_next`; captions use the dedicated `Caption` style.
- Adds real OOXML numbering definitions for decimal and bullet lists, with 540-DXA text indent and 270-DXA hanging indent.
- Adds document-control, nomenclature/evidence status, claim-register, planned-protocol, reference, revision, and controlled-disclosure tables.
- Marks the first row of every body table with `w:tblHeader`, prevents body rows from splitting with `w:cantSplit`, uses expanding row heights, explicit cell margins, vertical centering, and synchronized fixed DXA geometry.
- Keeps all four evidence statuses visible while explicitly stating that no D0.1 claim is assigned `Implemented prototype behavior`; the builder fails closed if a canonical claim uses that status.
- Adds a static contents list in document order. A supplied `toc_page_map` renders mapped pages for each numbered section and Appendix A; an omitted map leaves the Task 4 page-number pass untouched.
- Adds running abbreviated-title/revision headers and centered footers with document ID, publication status, and real `PAGE`/`NUMPAGES` fields.
- Uses page breaks only within front-matter packaging and at the appendix boundary.
- Writes a raw DOCX in the output directory, normalizes ZIP timestamps, and atomically replaces the stable output with `os.replace`.
- Sets fixed core-property timestamps and verified byte-for-byte deterministic rebuilds.

## Required operation marker

The Documents create operation was marked exactly once, immediately before the first builder-authoring command:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/documents/skills/documents/container_tools/mark_artifact_operation_started.mjs --operation-kind create --expected-output-count 1 --output-format docx
```

Output: empty stdout, exit code 0.

## RED evidence

Command:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests/test_technical_paper.py -v
```

Output before implementation:

```text
test_claim_register_has_required_fields_and_uses_no_prototype_status (...) ... ok
test_controlled_disclosures_have_approval_provenance (...) ... ok
test_copy_respects_disclosure_boundary (...) ... ok
test_document_control_is_complete (...) ... ok
test_protocols_have_complete_planning_contract (...) ... ok
test_references_include_required_authorship_or_organization (...) ... ok
test_required_sections_are_ordered (...) ... ok
setUpClass (tests.test_technical_paper.DocxArtifactTests) ... ERROR

FileNotFoundError: [Errno 2] No such file or directory: '/Users/willisdesai/Documents/ACBOSS-recovered/output/docx/ROOT-Technical-Concept-Paper-D0.1.docx'

Ran 7 tests in 0.003s
FAILED (errors=1)
```

The failure was the intended missing-artifact failure; all pre-existing canonical content-model tests remained green.

## Build evidence

Command:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_technical_paper.py --docx-only
```

Output:

```text
/Users/willisdesai/Documents/ACBOSS-recovered/output/docx/ROOT-Technical-Concept-Paper-D0.1.docx
```

## Render evidence

Final render command:

```bash
env TMPDIR=/private/tmp /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/documents/skills/documents/render_docx.py output/docx/ROOT-Technical-Concept-Paper-D0.1.docx --output_dir /private/tmp/root-task2-render.0eIQih
```

Output:

```text
Pages rendered to /private/tmp/root-task2-render.0eIQih
```

Generated pages: `page-1.png` through `page-11.png`, each 1,414 x 2,000 pixels. The renderer's internal PDF was emitted only into the private temporary QA directory during diagnosis; no PDF was created or delivered in the repository.

## Every-page visual inspection

- Page 1: restrained left-aligned technical cover; title wraps cleanly; inherited Word Title border removed; metadata, running header, and footer are intact.
- Page 2: document-control table is fully visible with consistent header fill, column widths, cell padding, and an intentionally quiet lower half-page.
- Page 3: contents and the complete nomenclature/evidence-status table fit on one page; no orphaned rows; all four statuses are present and the implemented-prototype status is clearly unassigned.
- Page 4: Abstract through the start of connectivity; heading spacing is restored; the four-stage numbered list wraps under its text markers; no collision at the Heading 2 boundary.
- Page 5: connectivity continuation, sensing, placement, and the start of the claim register; caption remains with the table and the first claim rows fit cleanly.
- Page 6: claim-register continuation; repeating header is present; no row splits; revised evidence/revision columns avoid the earlier severe identifier wrapping.
- Page 7: final claim row, evaluation narrative, real bullet list, and start of the protocol table; hierarchy and transition spacing are clear.
- Page 8: protocol-table continuation; repeating header is present; long planning cells remain readable without clipping or fixed-height truncation.
- Page 9: final protocol row followed by limitations, company position, and reference introduction; no broken row or heading orphan.
- Page 10: complete reference table and revision-history table; URLs wrap within their cells and footer fields render `Page 10 of 11`.
- Page 11: controlled-disclosure appendix and complete table; wider review-control column removes pinned punctuation and all rows remain within the page.

All 11 pages were inspected at original resolution through the image viewer. Final result: no clipping, overlap, broken tables, missing glyphs, header/footer displacement, or uncontrolled page break. A batch preview initially displayed alternating-page thumbnail corruption; individual page inspection plus PDF text-coordinate inspection confirmed the page files and rendered PDF were correct.

## Table geometry audit

Command:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/documents/skills/documents/scripts/table_geometry.py output/docx/ROOT-Technical-Concept-Paper-D0.1.docx
```

Result:

```text
table 1: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[2372, 7266]
table 2: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[2966, 6672]
table 3: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[771, 1478, 1542, 1671, 1478, 2698]
table 4: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[1409, 1483, 2076, 1779, 2891]
table 5: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[964, 2447, 2743, 1483, 2001]
table 6: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[1038, 1409, 1928, 1483, 1483, 2297]
table 7: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[816, 1557, 3114, 1631, 1260, 1260]
OK: all tables have matching tblW, tblInd, tblGrid, and tcW
```

The full audit printed matching `tcW` arrays for every row in all seven tables and exited 0.

## GREEN evidence

Command:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests/test_technical_paper.py -v
```

Output:

```text
test_claim_register_has_required_fields_and_uses_no_prototype_status (...) ... ok
test_controlled_disclosures_have_approval_provenance (...) ... ok
test_copy_respects_disclosure_boundary (...) ... ok
test_document_control_is_complete (...) ... ok
test_protocols_have_complete_planning_contract (...) ... ok
test_references_include_required_authorship_or_organization (...) ... ok
test_required_sections_are_ordered (...) ... ok
test_a4_geometry (...) ... ok
test_heading_structure_and_metadata (...) ... ok
test_tables_have_repeating_header_rows (...) ... ok

Ran 10 tests in 0.023s
OK
```

## Additional structural verification

- Heading audit: 16 `Heading 1` paragraphs and 2 `Heading 2` paragraphs. Its generic “numbering without heading style” reminder identified only the intentionally real numbered and bullet list paragraphs, not fake headings.
- Section audit: one A4 portrait section, 8.27 x 11.69 in, with 0.79 in (20 mm) margins and unlinked header/footer parts.
- Field report: exactly one `PAGE` and one `NUMPAGES`, both in `word/footer1.xml`; rendered values increment correctly through `Page 11 of 11`.
- Deterministic rebuild command and output:

  ```text
  0dbaa6aa24332698928411994cf46f27442ca266bcbc747b081258141dc803ba  output/docx/ROOT-Technical-Concept-Paper-D0.1.docx
  /Users/willisdesai/Documents/ACBOSS-recovered/output/docx/ROOT-Technical-Concept-Paper-D0.1.docx
  0dbaa6aa24332698928411994cf46f27442ca266bcbc747b081258141dc803ba  output/docx/ROOT-Technical-Concept-Paper-D0.1.docx
  ```

## Files

- Created `scripts/build_technical_paper.py`.
- Modified `tests/test_technical_paper.py`.
- Created `output/docx/ROOT-Technical-Concept-Paper-D0.1.docx`.
- Created this report.

No other repository files were modified by this task.

## Self-review

- Verified the exact public function signature and all named helpers.
- Re-read the brief against the builder: A4 geometry, exact tokens, cover, front/body/back matter, tables, static TOC map input, lists, headings, captions, running furniture, fields, controlled page breaks, atomic output, and no final PDF are implemented.
- Confirmed all body tables have repeating first rows, exact 9,638-DXA widths, 120-DXA indents matching the start cell margin, and no fixed row heights.
- Confirmed the one `Title` paragraph and required heading/metadata strings through the structural tests.
- Confirmed all four evidence statuses remain available while the claim register uses none assigned to `Implemented prototype behavior`.
- Confirmed no user-owned or unrelated dirty-worktree files were staged or changed.

## Concerns and handoff notes

- No blocking layout concern remains. The document-control page is intentionally sparse, while the claim and protocol registers are deliberately dense but readable at 8.1 pt; Task 3 can enrich figure/protocol presentation without changing the canonical content boundary.
- Task 4 must supply the final `toc_page_map`, rebuild the DOCX, and own the canonical PDF/two-pass page mapping. Without a supplied map, Task 2 correctly leaves static contents page numbers absent.
- Task 6 accessibility follow-up: every table's first row is marked `w:tblHeader` as required. Confirm screen-reader header scope and continued-table narration, and review whether dense multi-column claim/protocol tables need additional accessible summaries. Repeating headers improve navigation but do not by themselves express full header associations.

## Round 1 review fixes — 25 August 2026

### Implementation

- Added builder-level regression coverage that calls `build_docx` into temporary directories. The tests reopen the generated file and prove A4 geometry, 20 mm margins, required content, supplied static TOC values, all seven tables, repeating header rows, `PAGE`/`NUMPAGES` fields, and `updateFields` configuration.
- Added a byte-level determinism regression that compares two independent temporary builds.
- Removed the private, untyped `document._root_toc_page_map` state. `build_docx` now passes `toc_page_map: dict[str, int] | None` explicitly to the typed `add_front_matter` interface, which passes it to `_toc_page`.
- Consolidated every preset-controlled literal used by the builder into the single `TOKENS` map: heading and paragraph spacing, table indent and cell margins, border sizing, list indent/hanging/spacing, header/footer typography and distances, contents tab position, and cover spacing/typography.
- Recorded the `compact_reference_guide` base and the named engineering-report deviations in `TOKENS`. Deliberate overrides include A4/20 mm page geometry; Arial; 10 pt body with 5 pt after and 1.18 leading; H1 spacing from 18/10 pt to 18/8 pt; H2 spacing from 14/7 pt to 14/6 pt; H3 size from 12 pt to 11.5 pt; the 9,638-DXA A4 table width and neutral header fill; compact list rounding/leading; and the restrained, left-aligned `editorial_cover` structure.
- Removed unused `WD_BREAK`, `WD_SECTION`, and `Mm` imports.
- Per controller ruling, the 1,032-line builder remains one module because Tasks 3–4 extend its approved named interfaces.

### Round 1 RED evidence

Command:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests.test_technical_paper.DocxBuilderTests -v
```

Output before the production change:

```text
test_build_docx_creates_valid_a4_artifact (...) ... ok
test_build_docx_is_byte_deterministic (...) ... ok
test_front_matter_accepts_explicit_toc_page_map (...) ... ERROR

TypeError: add_front_matter() takes 1 positional argument but 2 were given

Ran 3 tests in 0.573s
FAILED (errors=1)
```

This failure proved that front matter still depended on hidden document state and did not accept the required explicit map.

### Round 1 GREEN evidence

Builder-focused command:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests.test_technical_paper.DocxBuilderTests -v
```

Output:

```text
test_build_docx_creates_valid_a4_artifact (...) ... ok
test_build_docx_is_byte_deterministic (...) ... ok
test_front_matter_accepts_explicit_toc_page_map (...) ... ok

Ran 3 tests in 0.591s
OK
```

Full test command:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests/test_technical_paper.py -v
```

Output:

```text
test_claim_register_has_required_fields_and_uses_no_prototype_status (...) ... ok
test_controlled_disclosures_have_approval_provenance (...) ... ok
test_copy_respects_disclosure_boundary (...) ... ok
test_document_control_is_complete (...) ... ok
test_protocols_have_complete_planning_contract (...) ... ok
test_references_include_required_authorship_or_organization (...) ... ok
test_required_sections_are_ordered (...) ... ok
test_a4_geometry (...) ... ok
test_heading_structure_and_metadata (...) ... ok
test_tables_have_repeating_header_rows (...) ... ok
test_build_docx_creates_valid_a4_artifact (...) ... ok
test_build_docx_is_byte_deterministic (...) ... ok
test_front_matter_accepts_explicit_toc_page_map (...) ... ok

Ran 13 tests in 0.592s
OK
```

### Round 1 deterministic-build check

Command:

```bash
round1_dir=$(mktemp -d /private/tmp/root-task2-round1-determinism.XXXXXX)
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_technical_paper.py --docx-only --output "$round1_dir/first.docx"
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_technical_paper.py --docx-only --output "$round1_dir/second.docx"
shasum -a 256 "$round1_dir/first.docx" "$round1_dir/second.docx"
cmp -s "$round1_dir/first.docx" "$round1_dir/second.docx"
printf 'cmp_exit=%s\n' "$?"
```

Output:

```text
/private/tmp/root-task2-round1-determinism.YU5oYE/first.docx
/private/tmp/root-task2-round1-determinism.YU5oYE/second.docx
0dbaa6aa24332698928411994cf46f27442ca266bcbc747b081258141dc803ba  /private/tmp/root-task2-round1-determinism.YU5oYE/first.docx
0dbaa6aa24332698928411994cf46f27442ca266bcbc747b081258141dc803ba  /private/tmp/root-task2-round1-determinism.YU5oYE/second.docx
cmp_exit=0
```

The canonical output has the same SHA-256, so the token/interface refactor caused no artifact-byte or layout change.

### Round 1 table-geometry audit

Command:

```bash
/Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/documents/skills/documents/scripts/table_geometry.py output/docx/ROOT-Technical-Concept-Paper-D0.1.docx
```

Output summary, preserving the exact audited geometry:

```text
table 1: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[2372, 7266]
table 2: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[2966, 6672]
table 3: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[771, 1478, 1542, 1671, 1478, 2698]
table 4: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[1409, 1483, 2076, 1779, 2891]
table 5: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[964, 2447, 2743, 1483, 2001]
table 6: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[1038, 1409, 1928, 1483, 1483, 2297]
table 7: tblW=dxa:9638 tblInd=dxa:120 grid_sum=9638 grid=[816, 1557, 3114, 1631, 1260, 1260]
OK: all tables have matching tblW, tblInd, tblGrid, and tcW
```

The command also printed matching `tcW` arrays for every row and exited 0.

### Round 1 render and every-page inspection

Command:

```bash
round1_render_dir=$(mktemp -d /private/tmp/root-task2-round1-render.XXXXXX)
env TMPDIR=/private/tmp /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/willisdesai/.cache/codex-runtimes/codex-primary-runtime/plugins/openai-primary-runtime/plugins/documents/skills/documents/render_docx.py output/docx/ROOT-Technical-Concept-Paper-D0.1.docx --output_dir "$round1_render_dir"
```

Output:

```text
Pages rendered to /private/tmp/root-task2-round1-render.eXKc9Z
```

All 11 `page-*.png` files were opened and inspected individually at original render resolution:

- Page 1: restrained left-aligned cover; title wraps cleanly; metadata and footer remain inside the A4 content frame.
- Page 2: complete document-control table; no clipping or malformed cells.
- Page 3: contents and full nomenclature/status table; all four evidence statuses present and legible.
- Page 4: Abstract through section 3; real numbered list aligns consistently; page transition is natural.
- Page 5: sections 4–6 and first claim-register rows; caption/header alignment and wrapping remain clean.
- Page 6: claim-register continuation with repeating header; all row boundaries and footer are visible.
- Page 7: final claim row, evaluation copy, bullets, and first protocol row; no orphaned headings.
- Page 8: protocol continuation with repeating header; dense cells remain within page and table bounds.
- Page 9: final protocol row, limitations, company position, and references introduction; no overlap.
- Page 10: complete reference and revision-history tables; URLs wrap cleanly.
- Page 11: full controlled-disclosure appendix/table; all rows and footer remain visible.

Result: no clipping, overlap, missing glyphs, broken table geometry, header/footer displacement, or unexpected pagination. The render remains 11 pages. No final PDF was created in the repository.

### Round 1 files and self-review

- Modified `scripts/build_technical_paper.py`.
- Modified `tests/test_technical_paper.py`.
- Rebuilt `output/docx/ROOT-Technical-Concept-Paper-D0.1.docx`; bytes remained identical to the committed artifact.
- Appended this report.
- `git diff --check` passed for all modified Task 2 text files.
- Confirmed the four evidence statuses remain available and no claim uses `Implemented prototype behavior`.
- Confirmed the public `build_docx` signature is unchanged and Task 4 still owns the final TOC page map/PDF pass.
- Confirmed no unrelated dirty-worktree file was changed or staged.

### Round 1 concerns

- Non-blocking final-review concern: `scripts/build_technical_paper.py` is large (about 1,032 lines). It was intentionally not split because the approved Task 2 plan locates builder helpers and assembly there, and Tasks 3–4 extend those named interfaces. Revisit modularization only after those interfaces settle.
- Existing layout/accessibility handoffs remain: claim/protocol tables are deliberately dense; Task 3 may enrich their presentation, and Task 6 should verify accessible header scope and continued-table narration.
