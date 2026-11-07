"""
Mock Test Suite for Prompt 6: Customer Loyalty, Care Intelligence & Retention.
Verifies all 10 Prompt 6 scenarios in pure Python without requiring Frappe / Docker daemon:
1. 0 visits (insufficient data)
2. 1 visit (insufficient data for interval, last visit recorded)
3. 2 visits (first interval, preliminary cycle, LOW confidence)
4. Multiple visits (stable cycle, EWMA applied, MEDIUM/HIGH confidence)
5. Outlier interval (IQR outlier detection and removal)
6. Multiple service types under same pet (strictly isolated)
7. Multiple pets under same customer (strictly isolated)
8. Due Soon qualification (approaching due date, NOT triggered on visit day)
9. At Risk qualification (absence_ratio >= 1.5, explainable reasoning)
10. With vs without Membership (both work, benefits context enriched when present)
11. Recommendation deduplication & in-place update (no duplicate records)
"""

import unittest
import sys
import os
from datetime import date, timedelta
from typing import List
from unittest.mock import MagicMock

# Ensure apps/petcare_crm is on sys.path
sys.path.insert(0, os.path.abspath("apps/petcare_crm"))

# Mock frappe if not installed on host
if "frappe" not in sys.modules:
    mock_frappe = MagicMock()
    mock_frappe._ = lambda x: x
    mock_frappe.throw = lambda msg, *args, **kwargs: (_ for _ in ()).throw(Exception(msg))
    mock_frappe.logger = lambda name: MagicMock()
    sys.modules["frappe"] = mock_frappe
    sys.modules["frappe.model"] = MagicMock()
    sys.modules["frappe.model.document"] = MagicMock()

from petcare_crm.utils.config import (
    RECOMMENDATION_NEW,
    RECOMMENDATION_CONTACTED,
    RECOMMENDATION_CONVERTED,
    RECOMMENDATION_DISMISSED,
    RECOMMENDATION_TYPE_DUE_SOON,
    RECOMMENDATION_TYPE_AT_RISK,
)
from petcare_crm.utils.models import (
    Customer,
    Pet,
    ServiceVisit,
    Membership,
    MembershipBenefit,
)
from petcare_crm.utils.care_pattern_service import (
    CarePatternAnalyzer,
    VisitPredictionService,
    RiskDetectionService,
    CarePatternService,
)
from petcare_crm.utils.recommendation_service import (
    CareRecommendationCoordinator,
    RecommendationService,
)


class TestCareIntelligenceMock(unittest.TestCase):

    def setUp(self):
        self.today = date(2026, 10, 26)
        self.customer = Customer(name="CUST-001", customer_name="Nguyen Van A")
        self.pet = Pet(name="PET-MOCHI", pet_name="Mochi", customer="CUST-001", species="Dog", breed="Corgi")

    # ─────────────────────────────────────────────────────────────────
    # Scenario 1: 0 Service Visits
    # ─────────────────────────────────────────────────────────────────
    def test_01_zero_visits(self):
        visits: List[ServiceVisit] = []
        pattern = CarePatternAnalyzer.analyze_pattern(
            pet="PET-MOCHI", service_type="Grooming", visits=visits
        )
        self.assertEqual(pattern.number_of_visits, 0)
        self.assertTrue(pattern.insufficient_data)
        self.assertEqual(pattern.data_sufficiency, "INSUFFICIENT")
        self.assertEqual(pattern.confidence, "NONE")
        self.assertIsNone(pattern.typical_interval)
        self.assertIsNone(pattern.last_visit_date)

        pred = VisitPredictionService.predict_next_visit(
            pet="PET-MOCHI", service_type="Grooming", visits=visits
        )
        self.assertTrue(pred.insufficient_data)
        self.assertIsNone(pred.predicted_next_visit)

    # ─────────────────────────────────────────────────────────────────
    # Scenario 2: 1 Service Visit
    # ─────────────────────────────────────────────────────────────────
    def test_02_single_visit(self):
        visits = [
            ServiceVisit(
                pet="PET-MOCHI",
                customer="CUST-001",
                service_type="Grooming",
                visit_date=self.today - timedelta(days=20),
            )
        ]
        pattern = CarePatternAnalyzer.analyze_pattern(
            pet="PET-MOCHI", service_type="Grooming", visits=visits
        )
        self.assertEqual(pattern.number_of_visits, 1)
        self.assertEqual(pattern.last_visit_date, self.today - timedelta(days=20))
        self.assertTrue(pattern.insufficient_data)
        self.assertEqual(pattern.confidence, "NONE")
        self.assertIsNone(pattern.typical_interval)
        self.assertIn("Cần ít nhất 2 lượt", pattern.reason)

        pred = VisitPredictionService.predict_next_visit(
            pet="PET-MOCHI", service_type="Grooming", visits=visits
        )
        self.assertTrue(pred.insufficient_data)
        self.assertIsNone(pred.predicted_next_visit)

    # ─────────────────────────────────────────────────────────────────
    # Scenario 3: 2 Service Visits (First Interval / Preliminary Cycle)
    # ─────────────────────────────────────────────────────────────────
    def test_03_two_visits_first_interval(self):
        visits = [
            ServiceVisit(
                pet="PET-MOCHI",
                customer="CUST-001",
                service_type="Grooming",
                visit_date=self.today - timedelta(days=60),
            ),
            ServiceVisit(
                pet="PET-MOCHI",
                customer="CUST-001",
                service_type="Grooming",
                visit_date=self.today - timedelta(days=30),
            ),
        ]
        pattern = CarePatternAnalyzer.analyze_pattern(
            pet="PET-MOCHI", service_type="Grooming", visits=visits
        )
        self.assertEqual(pattern.number_of_visits, 2)
        self.assertEqual(pattern.raw_deltas, [30])
        self.assertEqual(pattern.typical_interval, 30.0)
        self.assertEqual(pattern.confidence, "LOW")
        self.assertEqual(pattern.data_sufficiency, "MINIMAL")

        # Prediction uses preliminary interval
        pred = VisitPredictionService.predict_next_visit(
            pet="PET-MOCHI", service_type="Grooming", visits=visits
        )
        self.assertEqual(pred.confidence, "LOW")
        self.assertEqual(pred.predicted_next_visit, (self.today - timedelta(days=30)) + timedelta(days=30))

    # ─────────────────────────────────────────────────────────────────
    # Scenario 4: Multiple Visits (Stable Recurring Cycle)
    # ─────────────────────────────────────────────────────────────────
    def test_04_multiple_visits_stable_cycle(self):
        # 4 visits with 30-day intervals
        visits = [
            ServiceVisit(
                pet="PET-MOCHI",
                customer="CUST-001",
                service_type="Grooming",
                visit_date=self.today - timedelta(days=90),
            ),
            ServiceVisit(
                pet="PET-MOCHI",
                customer="CUST-001",
                service_type="Grooming",
                visit_date=self.today - timedelta(days=60),
            ),
            ServiceVisit(
                pet="PET-MOCHI",
                customer="CUST-001",
                service_type="Grooming",
                visit_date=self.today - timedelta(days=30),
            ),
            ServiceVisit(
                pet="PET-MOCHI",
                customer="CUST-001",
                service_type="Grooming",
                visit_date=self.today,
            ),
        ]
        pattern = CarePatternAnalyzer.analyze_pattern(
            pet="PET-MOCHI", service_type="Grooming", visits=visits
        )
        self.assertEqual(pattern.number_of_visits, 4)
        self.assertFalse(pattern.insufficient_data)
        self.assertEqual(pattern.confidence, "MEDIUM")
        self.assertEqual(pattern.typical_interval, 30.0)
        self.assertEqual(pattern.arithmetic_mean, 30.0)
        self.assertEqual(pattern.median_interval, 30.0)

    # ─────────────────────────────────────────────────────────────────
    # Scenario 5: Statistical Outlier Interval (IQR Filtering)
    # ─────────────────────────────────────────────────────────────────
    def test_05_iqr_outlier_filtering(self):
        # Regular intervals around 30 days, plus one extreme gap of 180 days
        dates = [
            self.today - timedelta(days=300),
            self.today - timedelta(days=270),  # delta = 30
            self.today - timedelta(days=240),  # delta = 30
            self.today - timedelta(days=210),  # delta = 30
            self.today - timedelta(days=30),   # delta = 180 (OUTLIER)
            self.today,                        # delta = 30
        ]
        visits = [
            ServiceVisit(
                pet="PET-MOCHI",
                customer="CUST-001",
                service_type="Grooming",
                visit_date=d,
            )
            for d in dates
        ]
        pattern = CarePatternAnalyzer.analyze_pattern(
            pet="PET-MOCHI", service_type="Grooming", visits=visits, filter_outliers=True
        )
        self.assertEqual(len(pattern.outliers_detected), 1)
        self.assertIn(180, pattern.outliers_detected)
        self.assertNotIn(180, pattern.filtered_deltas)
        # Without outlier, interval should be 30.0, not skewed above 50
        self.assertEqual(pattern.typical_interval, 30.0)
        self.assertEqual(pattern.confidence, "HIGH")

    # ─────────────────────────────────────────────────────────────────
    # Scenario 6: Multiple Service Types for Same Pet (Isolated)
    # ─────────────────────────────────────────────────────────────────
    def test_06_multiple_service_types_isolated(self):
        visits = [
            # Grooming every 30 days
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=60)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=30)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today),
            # Vaccination once a year
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Vaccination", visit_date=self.today - timedelta(days=365)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Vaccination", visit_date=self.today),
        ]

        pattern_grooming = CarePatternAnalyzer.analyze_pattern(
            pet="PET-MOCHI", service_type="Grooming", visits=visits
        )
        pattern_vax = CarePatternAnalyzer.analyze_pattern(
            pet="PET-MOCHI", service_type="Vaccination", visits=visits
        )

        self.assertEqual(pattern_grooming.number_of_visits, 3)
        self.assertEqual(pattern_grooming.typical_interval, 30.0)

        self.assertEqual(pattern_vax.number_of_visits, 2)
        self.assertEqual(pattern_vax.typical_interval, 365.0)

    # ─────────────────────────────────────────────────────────────────
    # Scenario 7: Multiple Pets for Same Customer (Isolated)
    # ─────────────────────────────────────────────────────────────────
    def test_07_multiple_pets_isolated(self):
        visits = [
            # Pet Mochi: groomed every 20 days
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=40)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=20)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today),
            # Pet Luna: groomed every 45 days
            ServiceVisit(pet="PET-LUNA", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=90)),
            ServiceVisit(pet="PET-LUNA", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=45)),
            ServiceVisit(pet="PET-LUNA", customer="CUST-001", service_type="Grooming", visit_date=self.today),
        ]

        pattern_mochi = CarePatternAnalyzer.analyze_pattern("PET-MOCHI", "Grooming", visits)
        pattern_luna = CarePatternAnalyzer.analyze_pattern("PET-LUNA", "Grooming", visits)

        self.assertEqual(pattern_mochi.typical_interval, 20.0)
        self.assertEqual(pattern_luna.typical_interval, 45.0)

    # ─────────────────────────────────────────────────────────────────
    # Scenario 8: Due Soon Qualification (and Not on Visit Day)
    # ─────────────────────────────────────────────────────────────────
    def test_08_due_soon_qualification(self):
        # 3 visits, interval 30 days, last visit was 28 days ago -> 2 days until due
        visits = [
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=88)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=58)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=28)),
        ]
        due_result = RiskDetectionService.detect_due_soon(
            pet="PET-MOCHI", service_type="Grooming", visits=visits, current_date=self.today
        )
        self.assertTrue(due_result.is_due_soon)
        self.assertEqual(due_result.status, "DUE_SOON")
        self.assertEqual(due_result.days_until_due, 2)
        self.assertLessEqual(due_result.days_until_due, due_result.effective_threshold)

        # Pet visited TODAY (days_since_last_visit == 0) -> NOT due soon
        visits_today = visits + [
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today)
        ]
        due_today = RiskDetectionService.detect_due_soon(
            pet="PET-MOCHI", service_type="Grooming", visits=visits_today, current_date=self.today
        )
        self.assertFalse(due_today.is_due_soon)
        self.assertNotEqual(due_today.status, "DUE_SOON")

    # ─────────────────────────────────────────────────────────────────
    # Scenario 9: At Risk Qualification (absence_ratio >= 1.5)
    # ─────────────────────────────────────────────────────────────────
    def test_09_at_risk_qualification(self):
        # Typical interval 30 days, but last visit was 50 days ago (50 / 30 = 1.67 >= 1.5)
        visits = [
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=110)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=80)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=50)),
        ]
        at_risk_result = RiskDetectionService.detect_at_risk(
            pet="PET-MOCHI", service_type="Grooming", visits=visits, current_date=self.today
        )
        self.assertTrue(at_risk_result.is_at_risk)
        self.assertEqual(at_risk_result.status, "AT_RISK")
        self.assertGreaterEqual(at_risk_result.absence_ratio, 1.5)
        self.assertIn("vượt ngưỡng cảnh báo", at_risk_result.reason)

    # ─────────────────────────────────────────────────────────────────
    # Scenario 10: With vs Without Membership
    # ─────────────────────────────────────────────────────────────────
    def test_10_with_and_without_membership(self):
        visits = [
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=88)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=58)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=28)),
        ]

        # Case A: Without Membership -> Generates normal recommendation
        rec_no_ms = RecommendationService.generate_care_recommendation(
            pet=self.pet,
            customer=self.customer,
            service_type="Grooming",
            visits=visits,
            current_date=self.today,
            memberships=[],
        )
        self.assertIsNotNone(rec_no_ms)
        self.assertEqual(rec_no_ms["recommendation_type"], RECOMMENDATION_TYPE_DUE_SOON)
        self.assertIsNone(rec_no_ms["membership"])
        self.assertIn("Mochi", rec_no_ms["reason"])

        # Case B: With VIP Membership & Remaining Benefits
        benefit = MembershipBenefit(benefit_type="Grooming", total_quantity=5, used_quantity=2)
        membership = Membership(
            name="MS-VIP-001",
            customer="CUST-001",
            membership_plan="VIP Club",
            start_date=self.today - timedelta(days=100),
            end_date=self.today + timedelta(days=265),
            benefits=[benefit],
        )

        rec_with_ms = RecommendationService.generate_care_recommendation(
            pet=self.pet,
            customer=self.customer,
            service_type="Grooming",
            visits=visits,
            current_date=self.today,
            memberships=[membership],
        )
        self.assertIsNotNone(rec_with_ms)
        self.assertEqual(rec_with_ms["membership"], "MS-VIP-001")
        self.assertEqual(rec_with_ms["priority"], "High")
        self.assertIn("3 lượt Grooming", rec_with_ms["reason"])
        self.assertIn("[⭐ KHÁCH HÀNG VIP]", rec_with_ms["reason"])

    # ─────────────────────────────────────────────────────────────────
    # Scenario 11: Deduplication and In-Place Update (No Garbage Records)
    # ─────────────────────────────────────────────────────────────────
    def test_11_deduplication_and_in_place_update(self):
        visits = [
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=88)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=58)),
            ServiceVisit(pet="PET-MOCHI", customer="CUST-001", service_type="Grooming", visit_date=self.today - timedelta(days=28)),
        ]
        store: List[dict] = []

        # 1st Run: Create NEW recommendation
        rec1 = RecommendationService.generate_care_recommendation(
            pet=self.pet,
            customer=self.customer,
            service_type="Grooming",
            visits=visits,
            current_date=self.today,
            existing_recs=store,
            store=store,
        )
        self.assertIsNotNone(rec1)
        self.assertEqual(len(store), 1)
        self.assertEqual(rec1["action_taken"], "CREATED")
        self.assertEqual(rec1["status"], RECOMMENDATION_NEW)

        # 2nd Run on same active recommendation: Updates in-place, does NOT append duplicate
        rec2 = RecommendationService.generate_care_recommendation(
            pet=self.pet,
            customer=self.customer,
            service_type="Grooming",
            visits=visits,
            current_date=self.today,
            existing_recs=store,
            store=store,
        )
        self.assertIsNotNone(rec2)
        self.assertEqual(len(store), 1)  # Length remains exactly 1!
        self.assertEqual(rec2["action_taken"], "UPDATED")

        # 3rd Run: User contacted customer -> status is CONTACTED
        store[0]["status"] = RECOMMENDATION_CONTACTED
        rec3 = RecommendationService.generate_care_recommendation(
            pet=self.pet,
            customer=self.customer,
            service_type="Grooming",
            visits=visits,
            current_date=self.today,
            existing_recs=store,
            store=store,
        )
        self.assertEqual(len(store), 1)
        self.assertEqual(rec3["action_taken"], "UPDATED")
        self.assertEqual(rec3["status"], RECOMMENDATION_CONTACTED)

        # 4th Run: User converted recommendation -> status is CONVERTED
        store[0]["status"] = RECOMMENDATION_CONVERTED
        # Next cycle when Due Soon triggers again: creates a fresh recommendation
        rec4 = RecommendationService.generate_care_recommendation(
            pet=self.pet,
            customer=self.customer,
            service_type="Grooming",
            visits=visits,
            current_date=self.today,
            existing_recs=store,
            store=store,
        )
        self.assertEqual(len(store), 2)  # New distinct record created
        self.assertEqual(rec4["action_taken"], "CREATED")
        self.assertEqual(rec4["status"], RECOMMENDATION_NEW)


if __name__ == "__main__":
    unittest.main()
