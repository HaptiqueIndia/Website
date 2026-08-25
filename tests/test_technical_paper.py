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

    def test_claim_register_has_required_fields_and_uses_no_prototype_status(self):
        paper = self.load_module()
        required = {
            "id", "status", "scope", "revision", "evidence_id", "evidence_date",
            "wording", "owner", "review_date", "superseded_wording",
        }
        self.assertTrue({"CB-01", "HT-01", "HT-02", "PE-01", "PE-07"}.issubset(
            {claim["id"] for claim in paper.CLAIMS}
        ))
        for claim in paper.CLAIMS:
            self.assertTrue(required.issubset(claim))
        self.assertNotIn("Implemented prototype behavior", {claim["status"] for claim in paper.CLAIMS})

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
            "reporting_requirements",
        }
        for protocol in paper.PROTOCOLS:
            self.assertTrue(required.issubset(protocol))
            self.assertEqual(protocol["acceptance_criterion"], "Defined before testing")

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
        def strings(value):
            if isinstance(value, str):
                return [value]
            if isinstance(value, dict):
                return [item for nested in value.values() for item in strings(nested)]
            if isinstance(value, (tuple, list)):
                return [item for nested in value for item in strings(nested)]
            return []

        corpus = "\n".join(strings((
            paper.DOCUMENT, paper.SECTIONS, paper.CLAIMS, paper.REFERENCES,
            paper.PROTOCOLS, paper.CONTROLLED_DISCLOSURES, paper.REVISION_HISTORY,
        ))).lower()
        for phrase in paper.FORBIDDEN_COPY:
            self.assertNotIn(phrase.lower(), corpus)


if __name__ == "__main__":
    unittest.main()
