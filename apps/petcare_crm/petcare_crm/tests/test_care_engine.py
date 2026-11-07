"""
T37: Automated unit tests for Module 2 — Care Pattern Engine.
Tests: calculate_average_interval, predict_next_service, get_care_status.
Run: bench --site petcare.localhost run-tests --app petcare_crm --module petcare_crm.tests.test_care_engine
"""
import frappe
import unittest
from datetime import date, timedelta


def _create_visits(pet_name, customer_name, service_type, visit_dates):
    """Helper: tạo bộ Service Visit."""
    for d in visit_dates:
        frappe.get_doc({
            "doctype": "Service Visit",
            "pet": pet_name,
            "customer": customer_name,
            "service_type": service_type,
            "visit_date": str(d),
            "original_price": 300000,
            "final_price": 300000,
        }).insert(ignore_permissions=True)
    frappe.db.commit()


class TestCareEngine(unittest.TestCase):

    def setUp(self):
        frappe.set_user("Administrator")
        self._cleanup()

        # Tạo Contact và Pet
        contact = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "TestCareCustomer",
            "is_primary_contact": 1,
        }).insert(ignore_permissions=True)
        self.customer_name = contact.name

        frappe.get_doc({
            "doctype": "Pet",
            "pet_name": "TEST-PET-UNIT",
            "customer": self.customer_name,
            "species": "Dog",
            "breed": "Poodle",
        }).insert(ignore_permissions=True)
        frappe.db.commit()

    def tearDown(self):
        """Xóa test data sau mỗi test."""
        frappe.db.rollback()

    def _cleanup(self):
        frappe.db.delete("Care Recommendation", {"pet": "TEST-PET-UNIT"})
        frappe.db.delete("Service Visit", {"pet": "TEST-PET-UNIT"})
        frappe.db.delete("Pet", {"pet_name": "TEST-PET-UNIT"})
        if hasattr(self, "customer_name") and self.customer_name:
            frappe.db.delete("Contact", {"name": self.customer_name})
        frappe.db.delete("Contact", {"first_name": "TestCareCustomer"})
        frappe.db.commit()

    # ─────────────────────────────────────────────────────────────────────
    # TEST: INSUFFICIENT_DATA
    # ─────────────────────────────────────────────────────────────────────

    def test_insufficient_data_when_less_than_3_visits(self):
        """FLOW 3b: Chỉ có 2 visits → INSUFFICIENT_DATA."""
        today = date.today()
        _create_visits(
            "TEST-PET-UNIT", self.customer_name, "Grooming",
            [today - timedelta(days=60), today - timedelta(days=30)]
        )
        result = frappe.call(
            "petcare_crm.api.get_care_status",
            pet_name="TEST-PET-UNIT", service_type="Grooming"
        )
        self.assertTrue(result["insufficient_data"])
        self.assertEqual(result["status"], "INSUFFICIENT_DATA")

    def test_no_recommendation_created_for_insufficient_data(self):
        """FLOW 3b: Không tạo Care Recommendation khi INSUFFICIENT_DATA."""
        today = date.today()
        _create_visits(
            "TEST-PET-UNIT", self.customer_name, "Grooming",
            [today - timedelta(days=60), today - timedelta(days=30)]
        )
        count_before = frappe.db.count("Care Recommendation",
            {"pet": "TEST-PET-UNIT", "service_type": "Grooming"})

        from petcare_crm.utils.frappe_recommendation_engine import generate_and_save_recommendation
        result = generate_and_save_recommendation(
            "TEST-PET-UNIT", self.customer_name, "Grooming", today
        )
        self.assertIsNone(result)
        count_after = frappe.db.count("Care Recommendation",
            {"pet": "TEST-PET-UNIT", "service_type": "Grooming"})
        self.assertEqual(count_before, count_after)

    # ─────────────────────────────────────────────────────────────────────
    # TEST: DUE SOON — FLOW 2
    # ─────────────────────────────────────────────────────────────────────

    def test_due_soon_detection_within_5_days(self):
        """FLOW 2: Pets với interval 30 ngày, last visit 27 ngày trước → DUE SOON."""
        today = date.today()
        # 3 visits cách nhau 30 ngày, last visit = today - 27 ngày
        _create_visits(
            "TEST-PET-UNIT", self.customer_name, "Grooming", [
                today - timedelta(days=87),
                today - timedelta(days=57),
                today - timedelta(days=27),
            ]
        )
        result = frappe.call(
            "petcare_crm.api.get_care_status",
            pet_name="TEST-PET-UNIT", service_type="Grooming",
            check_date=str(today)
        )
        self.assertFalse(result["insufficient_data"])
        self.assertTrue(result["due_soon"]["is_due_soon"])
        self.assertEqual(result["due_soon"]["status"], "DUE_SOON")
        # Số ngày còn lại phải <= 5
        self.assertLessEqual(result["due_soon"]["days_until_due"], 5)

    # ─────────────────────────────────────────────────────────────────────
    # TEST: AT RISK — FLOW 3a
    # ─────────────────────────────────────────────────────────────────────

    def test_at_risk_detection_when_ratio_exceeds_1_5(self):
        """FLOW 3a: Pet vắng > 1.5x chu kỳ → AT_RISK."""
        today = date.today()
        # Interval ~30 ngày, nhưng last visit = 50 ngày trước (ratio = 1.67)
        _create_visits(
            "TEST-PET-UNIT", self.customer_name, "Grooming", [
                today - timedelta(days=110),
                today - timedelta(days=80),
                today - timedelta(days=50),
            ]
        )
        result = frappe.call(
            "petcare_crm.api.get_care_status",
            pet_name="TEST-PET-UNIT", service_type="Grooming",
            check_date=str(today)
        )
        self.assertFalse(result["insufficient_data"])
        self.assertTrue(result["at_risk"]["is_at_risk"])
        self.assertGreaterEqual(result["at_risk"]["absence_ratio"], 1.5)

    # ─────────────────────────────────────────────────────────────────────
    # TEST: PREDICT NEXT SERVICE — T11
    # ─────────────────────────────────────────────────────────────────────

    def test_predict_next_service_returns_future_date(self):
        """predict_next_service trả về ngày tương lai hợp lý."""
        today = date.today()
        _create_visits(
            "TEST-PET-UNIT", self.customer_name, "Grooming", [
                today - timedelta(days=62),
                today - timedelta(days=31),
                today - timedelta(days=1),
            ]
        )
        result = frappe.call(
            "petcare_crm.api.predict_next_service",
            pet_name="TEST-PET-UNIT", service_type="Grooming"
        )
        self.assertFalse(result["insufficient_data"])
        self.assertIsNotNone(result["predicted_next_visit"])
        # Ngày dự đoán phải trong tương lai
        from datetime import datetime
        predicted = datetime.strptime(
            result["predicted_next_visit"][:10], "%Y-%m-%d"
        ).date()
        self.assertGreater(predicted, today - timedelta(days=5))

    # ─────────────────────────────────────────────────────────────────────
    # TEST: OVERDUE STATUS — H5 & M1
    # ─────────────────────────────────────────────────────────────────────

    def test_overdue_status_when_past_predicted_date_but_not_at_risk(self):
        """H5: Pet quá hạn lịch dự kiến (35 ngày / 30 ngày chu kỳ) nhưng ratio < 1.5 → OVERDUE."""
        today = date.today()
        _create_visits(
            "TEST-PET-UNIT", self.customer_name, "Grooming", [
                today - timedelta(days=95),
                today - timedelta(days=65),
                today - timedelta(days=35),
            ]
        )
        result = frappe.call(
            "petcare_crm.api.get_care_status",
            pet_name="TEST-PET-UNIT", service_type="Grooming",
            check_date=str(today)
        )
        self.assertFalse(result["insufficient_data"])
        self.assertEqual(result["status"], "OVERDUE")
        self.assertEqual(result["due_soon"]["status"], "OVERDUE")
        self.assertFalse(result["at_risk"]["is_at_risk"])

    # ─────────────────────────────────────────────────────────────────────
    # TEST: STATISTICAL IQR OUTLIER REMOVAL — L5 & M1
    # ─────────────────────────────────────────────────────────────────────

    def test_iqr_outlier_filtering_removes_extreme_gap(self):
        """L5: IQR Outlier Filter loại bỏ khoảng cách đột biến (180 ngày)."""
        from petcare_crm.utils.care_pattern_service import CarePatternService
        from petcare_crm.utils.models import ServiceVisit

        today = date.today()
        # Visits: 30, 30, 30 ngày, và 1 lần đột biến 180 ngày
        dates = [
            today - timedelta(days=270),
            today - timedelta(days=240),
            today - timedelta(days=210),
            today - timedelta(days=30),  # gap = 180
            today,                       # gap = 30
        ]
        visits = [
            ServiceVisit(
                pet="TEST-PET-UNIT",
                customer=self.customer_name,
                service_type="Grooming",
                visit_date=d
            )
            for d in dates
        ]
        res_filtered = CarePatternService.calculate_average_interval(
            "TEST-PET-UNIT", "Grooming", visits, filter_outliers=True, use_ewma=False
        )
        self.assertEqual(res_filtered["outliers_removed"], 1)
        # Chu kỳ sau khi lọc outlier phải ~ 30 ngày, không bị kéo lên > 60 ngày
        self.assertLess(res_filtered["average_interval"], 45)
