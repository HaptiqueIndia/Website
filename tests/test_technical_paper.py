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
