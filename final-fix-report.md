# ROOT technical paper final-fix report

Date: 25 August 2026
Scope: five HIGH blockers from `.omo/evidence/root-canonical-technical-paper-gate-review.md`

## Test-first evidence

- Scenario: enforce a 150–220-word abstract, cover reviewer/evidence controls, and all required protocol fields in DOCX/PDF. Invocation: `python3 -m unittest tests/test_technical_paper.py`. Binary observable before implementation: targeted assertions failed because the abstract had 80 words, the cover omitted required controls, and the rendered protocol register exposed only the reduced field set. Artifact: `.omo/evidence/root-technical-paper-final-fix/red-python.log`.
- Scenario: enforce separate HTML publication status and companion designation, committed builder/CSS, and an exact production allowlist. Invocation: `node --test tests/whitepaper.test.mjs tests/production-boundary.test.mjs`. Binary observable before implementation: the exact publication status was absent, the builder was absent from `HEAD`, and the builder copied unreferenced assets. Artifact: `.omo/evidence/root-technical-paper-final-fix/red-node.log`.

## Implemented fixes

- Expanded the canonical abstract to 164 words while retaining the thesis, engineering scope, and explicit no-measured-performance boundary.
- Added visible cover controls for owner, technical reviewer, issue date, and evidence cutoff.
- Replaced the reduced five-column protocol matrix with a readable three-column, repeated-header register. Every PE-01 through PE-07 record now publishes hardware revision, firmware revision, conditions, comparator/ground truth, sample interval, repeated trials, primary outcome, secondary outcomes, fixed acceptance criterion, exclusions/missing-data handling, uncertainty, retained artifact, and reporting requirements.
- Kept `Companion web edition / D0.1` as the web designation and separately added the exact shared status `Technical concept paper / Developer preview` to the HTML reader and document control.
- Added the page-scoped companion stylesheet and committed production-builder contract. The builder strips local-only paper CSS and emits only the explicitly allowlisted public files.

## Artifact verification

- Scenario: default two-pass build from the canonical source. Invocation: bundled Python `scripts/build_technical_paper.py`. Binary observable: exit 0 and both final files emitted. Artifact: `.omo/evidence/root-technical-paper-final-fix/default-two-pass-build.log`.
- Scenario: reopen the scrubbed DOCX. Invocation: bundled metadata scrubber followed by `python-docx`/OOXML inspection. Binary observable: creator and last modifier empty, no custom properties, and zero `rsid*` attributes. Artifacts: `.omo/evidence/root-technical-paper-final-fix/metadata-scrub.log` and `.omo/evidence/root-technical-paper-final-fix/metadata-reopen.log`.
- Scenario: independent deterministic DOCX rebuilds after scrub and archive normalization. Invocation: two fresh build → scrub → normalize cycles. Binary observable: both copies and the final DOCX have SHA-256 `cbcca4ca496973a1ef61e82f847ec49aba27705ac9abc9c27a467a81210ae924`. Artifact: `.omo/evidence/root-technical-paper-final-fix/deterministic-docx-green.log`.
- Scenario: regenerate only the PDF from the unchanged final DOCX. Invocation: bundled Python `scripts/build_technical_paper.py --pdf-only`. Binary observable: DOCX SHA-256 is unchanged and the canonical PDF is byte-identical to the renderer-retained PDF. Artifacts: `.omo/evidence/root-technical-paper-final-fix/pdf-only-final-regeneration.log`, `pdf-only-final-docx-hash-before.txt`, and `pdf-only-final-docx-hash-after.txt`.
- Scenario: document accessibility audit. Invocation: bundled DOCX accessibility checker. Binary observable: high=0, medium=0, low=0. Artifact: `.omo/evidence/root-technical-paper-final-fix/a11y-report.json`.
- Scenario: 100% visual inspection of both output formats. Invocation: DOCX renderer and independent Poppler PDF rasterization, followed by original-resolution inspection of every page. Binary observable: 13 A4 DOCX pages and 13 A4 PDF pages, with no missing glyph, overlap, clipping, broken table, missing repeated header, or header/footer defect. Artifacts: `.omo/evidence/root-technical-paper-final-fix/visual-inspection.md`, `pdf-pages/`, and `pdf-pages-final/`. The final PDF page images are byte-identical to the inspected set; evidence: `final-pdf-page-equivalence.log`.

## Pre-commit green checks

- Python syntax: exit 0; `.omo/evidence/root-technical-paper-final-fix/precommit-python-syntax.log`.
- Node syntax: exit 0; `.omo/evidence/root-technical-paper-final-fix/precommit-node-syntax.log`.
- Python artifact/contract suite: 27/27 pass; `.omo/evidence/root-technical-paper-final-fix/precommit-python-tests.log`.
- HTML reader contract: 1/1 pass; `.omo/evidence/root-technical-paper-final-fix/precommit-whitepaper-node.log`.
- Production exclusion and exact allowlist: 1/1 pass; `.omo/evidence/root-technical-paper-final-fix/precommit-production-boundary.log`.

## Residual concern

Non-blocking: LibreOffice embeds run-specific metadata in PDF bytes, so separate PDF export runs are not byte-stable. The delivered PDF is byte-identical to the renderer-emitted PDF retained from the final unchanged DOCX. The editable DOCX is byte-deterministic after the required build, privacy scrub, and normalization flow.

## Committed-head verification

- Scenario: verify the exact committed working-tree contract. Invocation: bundled Python unit tests, bundled Node test runner, Python/Node syntax checks, and `git diff --check HEAD^ HEAD`. Binary observable: Python 27/27 pass, Node 3/3 pass, both syntax checks exit 0, and the committed diff is whitespace-clean. Artifacts: `.omo/evidence/root-technical-paper-final-fix/postcommit-python-tests.log`, `postcommit-node-tests.log`, `postcommit-python-syntax.log`, `postcommit-node-syntax.log`, and `postcommit-diff-check.log`.
- Scenario: reproduce from an isolated committed snapshot. Invocation: `git archive HEAD` into `/private/tmp/root-final-fix-export.xAe2lF`, followed by the full Python/Node suites and syntax checks using bundled runtimes. Binary observable: Python 27/27 pass; Node 2 pass, 0 fail, 1 expected skip because a git archive intentionally has no `.git`; syntax checks exit 0; the allowlisted production artifact builds successfully inside the export. Artifact: `.omo/evidence/root-technical-paper-final-fix/clean-export-final.log`.
