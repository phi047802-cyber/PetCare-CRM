"""
T42: Unit tests for Scheduler Daily Automation Tasks.
Tests: daily_petcare_scan, check_due_and_at_risk_pets, check_expiring_memberships.
Run: bench --site petcare.localhost run-tests --app petcare_crm --module petcare_crm.tests.test_tasks
"""
import frappe
import unittest
from datetime import date, timedelta
from petcare_crm.tasks import (
    daily_petcare_scan,
    check_due_and_at_risk_pets,
    check_expiring_memberships,
)


class TestSchedulerTasks(unittest.TestCase):

    def setUp(self):
        frappe.set_user("Administrator")
        self._cleanup()
        self._setup_data()

    def tearDown(self):
        frappe.db.rollback()

    def _cleanup(self):
        frappe.db.delete("Care Recommendation", {"customer": ["like", "TestSched%"]})
        frappe.db.delete("Service Visit", {"customer": ["like", "TestSched%"]})
        frappe.db.delete("Customer Membership", {"customer": ["like", "TestSched%"]})
        frappe.db.delete("Pet", {"pet_name": ["in", ["Sched-Mochi", "Sched-Luna", "Sched-Lucky"]]})
        frappe.db.delete("Membership Plan", {"plan_name": "Sched Plan"})
        frappe.db.delete("Contact", {"first_name": ["in", ["TestSched1", "TestSched2"]]})
        frappe.db.commit()

    def _setup_data(self):
        self.today = date.today()

        # 1. Contacts
        self.c1 = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "TestSched1",
            "is_primary_contact": 1,
        }).insert(ignore_permissions=True).name

        self.c2 = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "TestSched2",
            "is_primary_contact": 1,
        }).insert(ignore_permissions=True).name

        # 2. Plan
        self.plan = frappe.get_doc({
            "doctype": "Membership Plan",
            "plan_name": "Sched Plan",
            "price": 500000,
            "duration_months": 1,
            "benefits": [
                {
                    "benefit_type": "Grooming",
                    "total_quantity": 2,
                    "discount_type": "FREE",
                    "discount_value": 100.0,
                }
            ]
        }).insert(ignore_permissions=True).name

        # 3. Pets
        # Mochi: DUE_SOON
        frappe.get_doc({
            "doctype": "Pet",
            "pet_name": "Sched-Mochi",
            "customer": self.c1,
            "species": "Dog",
            "breed": "Corgi",
        }).insert(ignore_permissions=True)

        for d_off in [84, 56, 28]:
            frappe.get_doc({
                "doctype": "Service Visit",
                "pet": "Sched-Mochi",
                "customer": self.c1,
                "service_type": "Grooming",
                "visit_date": str(self.today - timedelta(days=d_off)),
                "original_price": 200000,
            }).insert(ignore_permissions=True)

        # Luna: AT_RISK
        frappe.get_doc({
            "doctype": "Pet",
            "pet_name": "Sched-Luna",
            "customer": self.c2,
            "species": "Cat",
            "breed": "Persian",
        }).insert(ignore_permissions=True)

        for d_off in [100, 75, 50]:
            frappe.get_doc({
                "doctype": "Service Visit",
                "pet": "Sched-Luna",
                "customer": self.c2,
                "service_type": "Grooming",
                "visit_date": str(self.today - timedelta(days=d_off)),
                "original_price": 200000,
            }).insert(ignore_permissions=True)

        # Expiring Membership (expires in 3 days -> triggers RENEWAL)
        frappe.get_doc({
            "doctype": "Customer Membership",
            "customer": self.c1,
            "pet": "Sched-Mochi",
            "membership_plan": "Sched Plan",
            "start_date": str(self.today - timedelta(days=27)),
            "end_date": str(self.today + timedelta(days=3)),
            "status": "Active",
            "benefits": [
                {
                    "benefit_type": "Grooming",
                    "total_quantity": 2,
                    "used_quantity": 1,
                    "remaining_quantity": 1,
                    "discount_type": "FREE",
                    "discount_value": 100.0,
                }
            ]
        }).insert(ignore_permissions=True)

        frappe.db.commit()

    def test_daily_petcare_scan_creates_expected_recommendations(self):
        """daily_petcare_scan tạo đầy đủ DUE_SOON, AT_RISK và RENEWAL."""
        result = daily_petcare_scan()
        self.assertTrue(result["success"])
        self.assertGreaterEqual(result["due_count"], 2)  # Mochi (DUE_SOON) + Luna (AT_RISK)
        self.assertGreaterEqual(result["renewal_count"], 1)  # c1 membership renewal

        # Verify DUE_SOON
        rec_due = frappe.db.get_value(
            "Care Recommendation",
            {"pet": "Sched-Mochi", "service_type": "Grooming", "recommendation_type": "DUE_SOON"},
            ["name", "priority"],
            as_dict=True
        )
        self.assertIsNotNone(rec_due)
        self.assertEqual(rec_due["priority"], "Medium")

        # Verify AT_RISK
        rec_risk = frappe.db.get_value(
            "Care Recommendation",
            {"pet": "Sched-Luna", "service_type": "Grooming", "recommendation_type": "AT_RISK"},
            ["name", "priority"],
            as_dict=True
        )
        self.assertIsNotNone(rec_risk)
        self.assertEqual(rec_risk["priority"], "High")

        # Verify RENEWAL
        rec_renew = frappe.db.get_value(
            "Care Recommendation",
            {"customer": self.c1, "recommendation_type": "RENEWAL"},
            ["name", "priority"],
            as_dict=True
        )
        self.assertIsNotNone(rec_renew)
        self.assertEqual(rec_renew["priority"], "High")  # <= 3 days -> High

    def test_daily_petcare_scan_dedup_skips_duplicates(self):
        """Chạy lần 2 không tạo thêm bản ghi trùng lặp."""
        res1 = daily_petcare_scan()
        res2 = daily_petcare_scan()
        self.assertEqual(res2["due_count"], 0)
        self.assertEqual(res2["renewal_count"], 0)
