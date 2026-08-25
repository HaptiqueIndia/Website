import importlib.util
import pathlib
import tempfile
import unittest
import zipfile

from docx import Document


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "paper" / "root_technical_paper.py"
BUILDER_PATH = ROOT / "scripts" / "build_technical_paper.py"
DOCX_PATH = ROOT / "output" / "docx" / "ROOT-Technical-Concept-Paper-D0.1.docx"
APPROVED_FORBIDDEN_COPY = (
    "acceleration award", "affiliated with panasonic", "patent pending",
    "breathing sense", "zero outages", "perfect coverage",
    "universal compatibility", "fully-tested", "100% local",
)


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

    def test_claim_register_has_required_fields_and_uses_no_prototype_status(self):
        paper = self.load_module()
        required = {
            "id", "status", "scope", "revision", "evidence_id", "evidence_date",
            "wording", "owner", "review_date", "superseded_wording",
            "hardware_revision", "firmware_revision",
        }
        self.assertTrue({"CB-01", "HT-01", "HT-02", "PE-01", "PE-07"}.issubset(
            {claim["id"] for claim in paper.CLAIMS}
        ))
        for claim in paper.CLAIMS:
            self.assertTrue(required.issubset(claim))
        self.assertNotIn("Implemented prototype behavior", {claim["status"] for claim in paper.CLAIMS})
        for claim in paper.CLAIMS:
            expected_revision = "Not applicable" if claim["id"] == "CB-01" else "Target revision not yet assigned"
            self.assertEqual(claim["hardware_revision"], expected_revision)
            self.assertEqual(claim["firmware_revision"], expected_revision)

    def test_controlled_disclosures_have_approval_provenance(self):
        paper = self.load_module()
        required = {
            "id", "disclosure_type", "exact_wording", "source_or_approval_record",
            "owner", "approval_date", "next_review_date",
        }
        disclosure_types = {disclosure["disclosure_type"] for disclosure in paper.CONTROLLED_DISCLOSURES}
        self.assertEqual(
            disclosure_types,
            {"Intended use and medical boundary", "Safety role", "Company identity", "Privacy and data boundary", "Recognition and patent omission"},
        )
        for disclosure in paper.CONTROLLED_DISCLOSURES:
            self.assertTrue(required.issubset(disclosure))

    def test_protocols_have_complete_planning_contract(self):
        paper = self.load_module()
        required = {
            "conditions", "comparator_ground_truth", "sample_interval", "repeated_trials",
            "primary_outcomes", "secondary_outcomes", "acceptance_criterion",
            "exclusions_missing_data", "uncertainty", "retained_evidence_artifact",
            "reporting_requirements", "hardware_revision", "firmware_revision",
        }
        for protocol in paper.PROTOCOLS:
            self.assertTrue(required.issubset(protocol))
            self.assertEqual(protocol["acceptance_criterion"], "Defined before testing")
            self.assertEqual(protocol["hardware_revision"], "Target revision not yet assigned")
            self.assertEqual(protocol["firmware_revision"], "Target revision not yet assigned")

    def test_references_include_required_authorship_or_organization(self):
        paper = self.load_module()
        references = {reference["id"]: reference for reference in paper.REFERENCES}
        self.assertEqual(
            references["REF-01"]["authors"],
            ("Haiyan Yan", "Yawei Li", "Thomas Parkinson", "Stefano Schiavon", "Hui Zhang", "Rui Sun", "Shengkai Zhao", "Wei Zhao", "Zhen Sun", "Fangning Shi"),
        )
        self.assertEqual(references["REF-02"]["organization"], "Bluetooth SIG")

    def test_copy_respects_disclosure_boundary(self):
        paper = self.load_module()
        self.assertEqual(paper.FORBIDDEN_COPY, APPROVED_FORBIDDEN_COPY)
        def strings(value):
            if isinstance(value, str):
                return [value]
            if isinstance(value, dict):
                return [item for nested in value.values() for item in strings(nested)]
            if isinstance(value, (tuple, list)):
                return [item for nested in value for item in strings(nested)]
            return []

        corpus = "\n".join(strings((
            paper.EVIDENCE_STATUSES, paper.DOCUMENT, paper.SECTIONS, paper.CLAIMS, paper.REFERENCES,
            paper.PROTOCOLS, paper.CONTROLLED_DISCLOSURES, paper.REVISION_HISTORY,
        ))).lower()
        for phrase in APPROVED_FORBIDDEN_COPY:
            self.assertNotIn(phrase.lower(), corpus)


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


class DocxBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("build_technical_paper", BUILDER_PATH)
        cls.builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.builder)

    def test_front_matter_accepts_explicit_toc_page_map(self):
        document = Document()
        self.builder.configure_styles(document)
        for section in document.sections:
            self.builder.configure_section(section)

        self.builder.add_front_matter(
            document,
            {"room-level-problem": 42, "appendix-a": 99},
        )

        contents = "\n".join(paragraph.text for paragraph in document.paragraphs)
        self.assertIn("1. The room-level problem\t42", contents)
        self.assertIn("Appendix A. Controlled disclosures\t99", contents)

    def test_build_docx_creates_valid_a4_artifact(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = pathlib.Path(temporary_directory) / "built.docx"
            result = self.builder.build_docx(
                output_path,
                {"room-level-problem": 4, "appendix-a": 11},
            )

            self.assertEqual(result, output_path)
            self.assertTrue(output_path.is_file())
            document = Document(output_path)
            section = document.sections[0]
            self.assertAlmostEqual(section.page_width.mm, 210, delta=0.2)
            self.assertAlmostEqual(section.page_height.mm, 297, delta=0.2)
            for margin in (
                section.top_margin,
                section.right_margin,
                section.bottom_margin,
                section.left_margin,
            ):
                self.assertAlmostEqual(margin.mm, 20, delta=0.2)

            text = "\n".join(paragraph.text for paragraph in document.paragraphs)
            for required in (
                "ROOT: A local architecture for room-level AC comfort",
                "ROOT-TCP-001",
                "1. The room-level problem\t4",
                "Appendix A. Controlled disclosures\t11",
                "Implemented prototype behavior",
                "Revision history",
            ):
                self.assertIn(required, text)
            self.assertGreaterEqual(len(document.tables), 7)
            for table in document.tables:
                self.assertIn("tblHeader", table.rows[0]._tr.xml)

            with zipfile.ZipFile(output_path) as archive:
                footer_xml = archive.read("word/footer1.xml").decode("utf-8")
                settings_xml = archive.read("word/settings.xml").decode("utf-8")
            self.assertIn("PAGE", footer_xml)
            self.assertIn("NUMPAGES", footer_xml)
            self.assertIn("updateFields", settings_xml)

    def test_build_docx_is_byte_deterministic(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = pathlib.Path(temporary_directory)
            first = self.builder.build_docx(directory / "first.docx")
            second = self.builder.build_docx(directory / "second.docx")

            self.assertEqual(first.read_bytes(), second.read_bytes())


if __name__ == "__main__":
    unittest.main()
