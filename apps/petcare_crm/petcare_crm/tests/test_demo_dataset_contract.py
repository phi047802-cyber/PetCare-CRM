# Copyright (c) 2026, PetCare CRM Team and contributors

"""Static contract tests for the reproducible Frappe demo dataset."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock


REPO_ROOT = Path(__file__).resolve().parents[4]
APP_ROOT = REPO_ROOT / "apps" / "petcare_crm"
sys.path.insert(0, str(APP_ROOT))

if "frappe" not in sys.modules:
    sys.modules["frappe"] = MagicMock()

from petcare_crm.patches.v1_0.seed_demo_data import (  # noqa: E402
    DEMO_CONTACTS,
    DEMO_LEADS,
    DEMO_OPPORTUNITIES,
    DEMO_PETS,
    DEMO_PLANS,
    DEMO_SERVICES,
    EXPECTED_DEMO_COUNTS,
)


DOCTYPE_ROOT = APP_ROOT / "petcare_crm" / "petcare_crm" / "doctype"
MANIFEST_PATH = REPO_ROOT / "deliverables" / "demo-data" / "demo_dataset_manifest.json"
SEED_PATH = APP_ROOT / "petcare_crm" / "patches" / "v1_0" / "seed_demo_data.py"
PATCHES_PATH = APP_ROOT / "petcare_crm" / "patches.txt"


def load_doctype(name):
    path = DOCTYPE_ROOT / name / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def select_options(doctype, fieldname):
    for field in load_doctype(doctype)["fields"]:
        if field.get("fieldname") == fieldname:
            return set((field.get("options") or "").splitlines())
    raise AssertionError(f"Missing field {doctype}.{fieldname}")


class TestDemoDatasetContract(unittest.TestCase):
    def test_01_manifest_matches_python_contract(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["expected_counts"], EXPECTED_DEMO_COUNTS)
        self.assertFalse(manifest["contains_real_personal_data"])
        self.assertFalse(manifest["woocommerce_policy"]["preseed_order_sync"])

    def test_02_master_data_counts_are_stable(self):
        self.assertEqual(len(DEMO_CONTACTS), EXPECTED_DEMO_COUNTS["Contact"])
        self.assertEqual(len(DEMO_CONTACTS), EXPECTED_DEMO_COUNTS["Address"])
        self.assertEqual(len(DEMO_PETS), EXPECTED_DEMO_COUNTS["Pet"])
        self.assertEqual(len(DEMO_SERVICES), EXPECTED_DEMO_COUNTS["PetCare Service"])
        self.assertEqual(len(DEMO_PLANS), EXPECTED_DEMO_COUNTS["Membership Plan"])
        self.assertEqual(len(DEMO_LEADS), EXPECTED_DEMO_COUNTS["PetCare Lead"])
        self.assertEqual(len(DEMO_OPPORTUNITIES), EXPECTED_DEMO_COUNTS["PetCare Opportunity"])

    def test_03_every_pet_references_a_known_customer_key(self):
        customer_keys = {row["key"] for row in DEMO_CONTACTS}
        self.assertEqual(len(customer_keys), len(DEMO_CONTACTS))
        for pet in DEMO_PETS:
            self.assertIn(pet["customer_key"], customer_keys)
        self.assertEqual(
            len([pet for pet in DEMO_PETS if pet["customer_key"] == "An"]),
            2,
        )

    def test_04_service_and_plan_values_match_doctype_selects(self):
        service_categories = select_options("petcare_service", "category")
        benefit_types = select_options("plan_benefit", "benefit_type")
        discount_types = select_options("plan_benefit", "discount_type")

        for service in DEMO_SERVICES:
            self.assertIn(service["category"], service_categories)
        for plan in DEMO_PLANS:
            self.assertGreater(plan["duration_months"], 0)
            for benefit in plan["benefits"]:
                self.assertIn(benefit["benefit_type"], benefit_types)
                self.assertIn(benefit["discount_type"], discount_types)

    def test_05_lead_and_opportunity_values_match_doctype_selects(self):
        lead_statuses = select_options("petcare_lead", "status")
        lead_sources = select_options("petcare_lead", "lead_source")
        stages = select_options("petcare_opportunity", "stage")
        lost_reasons = select_options("petcare_opportunity", "lost_reason")

        for lead in DEMO_LEADS:
            self.assertIn(lead["status"], lead_statuses)
            self.assertIn(lead["lead_source"], lead_sources)
        for opportunity in DEMO_OPPORTUNITIES:
            self.assertIn(opportunity["stage"], stages)
            if opportunity["stage"] == "Closed Lost":
                self.assertIn(opportunity["lost_reason"], lost_reasons)

    def test_06_seed_uses_current_schema_and_real_document_links(self):
        source = SEED_PATH.read_text(encoding="utf-8")
        for legacy_field in ('"validity_days"', '"opportunity_amount"', '"sales_stage"'):
            self.assertNotIn(legacy_field, source)
        for invalid_link in ('"pet": "Bơ"', '"pet": "Miu Miu"', '"pet": "Đậu Phộng"'):
            self.assertNotIn(invalid_link, source)
        self.assertIn('"pet": pet_map[', source)
        self.assertIn('"recommendation_date":', source)

    def test_07_demo_seed_is_not_an_automatic_migration_patch(self):
        active_lines = [
            line.strip()
            for line in PATCHES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertNotIn("petcare_crm.patches.v1_0.seed_demo_data", active_lines)


if __name__ == "__main__":
    unittest.main()
