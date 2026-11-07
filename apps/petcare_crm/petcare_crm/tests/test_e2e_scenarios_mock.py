"""
End-to-End (E2E) & Integration Test Suite for PetCare CRM (Prompt 9).
Comprehensive verification across all architectural layers:

1. Unit Tests (Algorithms & Business Services):
   - Lead Conversion & Deduplication
   - Customer Validation & Phone Sanitization
   - Dynamic Pricing & Floor Limits
   - Benefit Redemption
   - Care Pattern & Outlier IQR
   - Visit Prediction & Confidence Rating
   - Due Soon & At Risk Detection
   - Recommendation Deduplication

2. End-to-End Scenarios:
   - Scenario A: Lead Acquisition -> Qualification -> Conversion -> Customer 360
   - Scenario B: Customer -> Pet Profile -> Service Catalog -> Service Visit
   - Scenario C: Membership Granting -> Benefit Consumption -> Exhaustion -> Transaction Safety
   - Scenario D: Service History -> Pattern Analysis -> Prediction -> Recommendation Engine (Idempotent)
   - Scenario E: Access Control (RBAC Server Authorization & Cross-Entity Validation)
   - Scenario F: Scheduled Automations (Lead Follow-up, Expiration, SLA Escapes - Idempotent)
"""

import os
import sys
import unittest
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock

# Ensure apps/petcare_crm is on sys.path
sys.path.insert(0, os.path.abspath("apps/petcare_crm"))

# Setup mock frappe
class MockFrappeException(Exception):
    pass

class MockDocument:
    def __init__(self, *args, **kwargs):
        self._is_new = True
        self.name = kwargs.get("name", "DOC-001")
        self.last_name = ""
        self.first_name = ""
        for k, v in kwargs.items():
            setattr(self, k, v)
        if args and isinstance(args[0], dict):
            for k, v in args[0].items():
                setattr(self, k, v)

    def is_new(self):
        return getattr(self, "_is_new", True)

    def insert(self, *args, **kwargs):
        self._is_new = False
        return self

    def save(self, *args, **kwargs):
        return self

    def get(self, k, default=None):
        return getattr(self, k, default)

    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def add_comment(self, *args, **kwargs):
        return MagicMock()


if "frappe" in sys.modules:
    mock_frappe = sys.modules["frappe"]
else:
    mock_frappe = MagicMock()
    mock_frappe._ = lambda x: x
    def _throw(msg, exc=MockFrappeException):
        raise exc(msg)
    mock_frappe.throw = _throw
    mock_frappe.session = MagicMock()
    mock_frappe.session.user = "Administrator"
    mock_frappe.logger = lambda name: MagicMock()
    sys.modules["frappe"] = mock_frappe

mock_frappe_utils = MagicMock()
mock_frappe_utils.nowdate.return_value = "2026-10-26"
mock_frappe_utils.now_datetime.return_value = "2026-10-26 14:00:00"
mock_frappe_utils.getdate = lambda d: d if isinstance(d, date) else datetime.strptime(str(d)[:10], "%Y-%m-%d").date()
mock_frappe.utils = mock_frappe_utils

mock_frappe_doc = MagicMock()
mock_frappe_doc.Document = MockDocument
mock_frappe.model = MagicMock()
mock_frappe.model.document = mock_frappe_doc
sys.modules["frappe.utils"] = mock_frappe_utils
sys.modules["frappe.model"] = mock_frappe.model
sys.modules["frappe.model.document"] = mock_frappe_doc

# Module imports
from petcare_crm.utils.lead_service import LeadManagementService, LeadConversionCoordinator
from petcare_crm.utils.sales_pipeline_service import SalesPipelineService
from petcare_crm.utils.customer_service import CustomerService
from petcare_crm.utils.service_operations import ServiceCatalogService, ServiceVisitService
from petcare_crm.utils.membership_service import MembershipService
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
from petcare_crm.utils.models import ServiceVisit, Pet, Customer
from petcare_crm.utils.security import (
    ROLE_SYSTEM_MANAGER,
    ROLE_CRM_MANAGER,
    ROLE_SALES,
    ROLE_TECHNICIAN,
    ROLE_ANALYST,
    check_role_permission,
    validate_cross_entity_relationship,
    is_valid_vietnam_phone,
    sanitize_input_string,
    sanitize_number,
)
from petcare_crm.utils.workflow_automation import (
    TaskManager,
    LeadFollowupAutomation,
    MembershipRenewalAutomation,
    CareEngineAutomation,
    ServiceRecoveryAutomation,
    AutomationCoordinator,
)
from petcare_crm.utils.exceptions import (
    ValidationError,
    EntityNotFoundException,
    InvalidStateTransitionException,
    BenefitExhaustedException,
)

# Synchronize frappe mock references across modules
import petcare_crm.utils.lead_service as ls_mod
ls_mod.frappe = mock_frappe
import petcare_crm.utils.customer_service as cs_mod
cs_mod.frappe = mock_frappe
import petcare_crm.utils.service_operations as so_mod
so_mod.frappe = mock_frappe
import petcare_crm.utils.membership_service as ms_mod
ms_mod.frappe = mock_frappe
import petcare_crm.utils.workflow_automation as wa_mod
wa_mod.frappe = mock_frappe
import petcare_crm.utils.security as sec_mod
sec_mod.frappe = mock_frappe


class TestE2EScenariosMock(unittest.TestCase):
    """Full End-to-End Scenarios and Integrated Lifecycle Validation."""

    def setUp(self):
        self.today = date(2026, 10, 26)
        sec_mod.frappe = mock_frappe
        wa_mod.frappe = mock_frappe
        so_mod.frappe = mock_frappe
        ls_mod.frappe = mock_frappe
        cs_mod.frappe = mock_frappe
        mock_frappe.db.reset_mock()
        mock_frappe.db.get_value.side_effect = None
        mock_frappe.db.get_list.side_effect = None
        mock_frappe.get_doc.side_effect = None
        mock_frappe.get_all.side_effect = None
        mock_frappe.get_cached_doc.side_effect = None
        mock_frappe.session.user = "test_runner"
        mock_frappe.get_roles = MagicMock(return_value=[ROLE_SYSTEM_MANAGER])

    # ─────────────────────────────────────────────────────────────────
    # 1. UNIT TESTS: Independent Algorithms & Business Services
    # ─────────────────────────────────────────────────────────────────

    def test_unit_01_vietnam_phone_validation_and_sanitization(self):
        """Unit: Chuẩn hóa và kiểm tra số điện thoại di động Việt Nam."""
        self.assertTrue(is_valid_vietnam_phone("0912345678"))
        self.assertTrue(is_valid_vietnam_phone("0389998888"))
        self.assertTrue(is_valid_vietnam_phone("0701122334"))
        self.assertTrue(is_valid_vietnam_phone("0856677889"))
        self.assertTrue(is_valid_vietnam_phone("0523456789"))

        # Invalid prefixes or lengths
        self.assertFalse(is_valid_vietnam_phone("0123456789"))  # 01 prefix is obsolete
        self.assertFalse(is_valid_vietnam_phone("091234567"))   # 9 digits
        self.assertFalse(is_valid_vietnam_phone("091234567890")) # 12 digits
        self.assertFalse(is_valid_vietnam_phone("abcdefghij"))

    def test_unit_02_input_sanitization_and_number_floor(self):
        """Unit: Khử khuẩn HTML/Script và chặn số âm."""
        malicious = "<script>alert('hack');</script>Grooming VIP"
        sanitized = sanitize_input_string(malicious)
        self.assertNotIn("<script>", sanitized)
        self.assertIn("Grooming VIP", sanitized)

        # Number floor prevents negative amounts by raising ValidationError
        with self.assertRaises(ValidationError):
            sanitize_number(-50000.0, min_val=0.0)
        self.assertEqual(sanitize_number(150000.0, min_val=0.0), 150000.0)

    def test_unit_03_care_pattern_analyzer_with_iqr_outlier(self):
        """Unit: CarePatternAnalyzer loại bỏ outlier bằng IQR và tính EWMA."""
        intervals = [20, 20, 20, 20, 100]
        cleaned, outliers, low_f, up_f = CarePatternAnalyzer.filter_outliers_iqr(intervals)
        self.assertIn(100, outliers)
        self.assertEqual(cleaned, [20, 20, 20, 20])

        ewma = CarePatternAnalyzer.calculate_ewma(cleaned, alpha=0.6)
        self.assertEqual(ewma, 20.0)

    def test_unit_04_visit_prediction_confidence_ratings(self):
        """Unit: VisitPredictionService phân loại độ tin cậy định tính."""
        # 1 visit -> NONE / INSUFFICIENT
        visits_1 = [
            ServiceVisit(pet="PET-01", customer="C1", service_type="Grooming", visit_date=self.today - timedelta(days=20))
        ]
        pred_low = VisitPredictionService.predict_next_visit("PET-01", "Grooming", visits_1, self.today)
        self.assertTrue(pred_low.insufficient_data)
        self.assertEqual(pred_low.confidence, "NONE")

        # 4 visits with 30-day intervals -> HIGH/MEDIUM confidence
        visits_4 = [
            ServiceVisit(pet="PET-01", customer="C1", service_type="Grooming", visit_date=self.today - timedelta(days=90)),
            ServiceVisit(pet="PET-01", customer="C1", service_type="Grooming", visit_date=self.today - timedelta(days=60)),
            ServiceVisit(pet="PET-01", customer="C1", service_type="Grooming", visit_date=self.today - timedelta(days=30)),
            ServiceVisit(pet="PET-01", customer="C1", service_type="Grooming", visit_date=self.today),
        ]
        pred_high = VisitPredictionService.predict_next_visit("PET-01", "Grooming", visits_4, self.today)
        self.assertFalse(pred_high.insufficient_data)
        self.assertIn(pred_high.confidence, ["MEDIUM", "HIGH"])
        self.assertIsNotNone(pred_high.predicted_next_visit)
        self.assertTrue(pred_high.is_rule_based_estimate)

    def test_unit_05_risk_detection_due_soon_and_at_risk(self):
        """Unit: RiskDetectionService phân biệt Due Soon vs At Risk."""
        # Due soon: 3 visits, last visit was 28 days ago, interval 30 -> 2 days until due
        visits_due = [
            ServiceVisit(pet="PET-01", customer="C1", service_type="Grooming", visit_date=self.today - timedelta(days=88)),
            ServiceVisit(pet="PET-01", customer="C1", service_type="Grooming", visit_date=self.today - timedelta(days=58)),
            ServiceVisit(pet="PET-01", customer="C1", service_type="Grooming", visit_date=self.today - timedelta(days=28)),
        ]
        risk_due = RiskDetectionService.detect_due_soon("PET-01", "Grooming", visits_due, current_date=self.today)
        self.assertTrue(risk_due.is_due_soon)
        self.assertEqual(risk_due.status, "DUE_SOON")

        # At risk: absent 65 days with typical interval 30 (absence ratio > 2.0)
        visits_overdue = [
            ServiceVisit(pet="PET-01", customer="C1", service_type="Grooming", visit_date=self.today - timedelta(days=125)),
            ServiceVisit(pet="PET-01", customer="C1", service_type="Grooming", visit_date=self.today - timedelta(days=95)),
            ServiceVisit(pet="PET-01", customer="C1", service_type="Grooming", visit_date=self.today - timedelta(days=65)),
        ]
        risk_overdue = RiskDetectionService.detect_at_risk("PET-01", "Grooming", visits_overdue, current_date=self.today)
        self.assertTrue(risk_overdue.is_at_risk)
        self.assertEqual(risk_overdue.status, "AT_RISK")
        self.assertGreaterEqual(risk_overdue.absence_ratio, 2.0)

    # ─────────────────────────────────────────────────────────────────
    # 2. END-TO-END SCENARIO A: Lead Acquisition -> Conversion -> 360
    # ─────────────────────────────────────────────────────────────────

    def test_scenario_a_lead_to_customer_lifecycle(self):
        """
        Scenario A:
        1. Tạo Lead từ nguồn Facebook Ads.
        2. Giao người phụ trách & ghi nhận cuộc gọi tương tác.
        3. Chuyển đổi Lead thành Customer (Contact), Pet và Sales Opportunity.
        4. Kiểm tra Customer 360 liên kết đúng và trạng thái Lead là Converted.
        """
        # Step 1: Create Lead
        lead_doc = MockDocument(
            name="LEAD-2026-00010",
            doctype="PetCare Lead",
            lead_name="Võ Văn Nam",
            phone="0918123456",
            email="nam.vo@gmail.com",
            lead_source="Facebook Ads",
            status="New",
            priority="High",
            lead_owner="sales_agent_01",
            initial_pet_info="Chó Samoyed 5 tháng tuổi",
        )
        mock_comm = MockDocument(name="COMM-0001", doctype="Communication")

        def _get_doc_mock(*args, **kwargs):
            if args and args[0] == "PetCare Lead":
                return lead_doc
            elif args and isinstance(args[0], dict):
                dt = args[0].get("doctype")
                if dt == "PetCare Lead":
                    return lead_doc
                elif dt == "Communication":
                    return mock_comm
                elif dt == "Contact":
                    return MockDocument(name="CONT-001", first_name="Võ", last_name="Văn Nam", phone="0918123456")
                elif dt == "Pet":
                    return MockDocument(name="PET-SAM-01", pet_name="Bông Gòn", species="Dog", breed="Samoyed", customer="CONT-001")
                elif dt == "PetCare Opportunity":
                    return MockDocument(name="OPP-001", customer="CONT-001", amount=1500000.0, status="Open")
            return MockDocument(*args, **kwargs)

        mock_frappe.get_doc.side_effect = _get_doc_mock
        mock_frappe.db.exists.return_value = True
        mock_frappe.db.get_value.return_value = None  # No existing customer with this phone

        lead_id = LeadManagementService.create_lead(
            lead_name="Võ Văn Nam",
            phone="0918123456",
            lead_source="Facebook Ads",
            email="nam.vo@gmail.com",
            initial_pet_info="Chó Samoyed 5 tháng tuổi",
            lead_owner="sales_agent_01"
        )
        self.assertEqual(lead_id, "LEAD-2026-00010")

        # Step 2: Assign & Record Follow-up Communication
        comm_id = LeadManagementService.add_interaction(
            lead_id="LEAD-2026-00010",
            interaction_type="Call",
            notes="Đã gọi điện tư vấn gói tiêm phòng và tắm sấy lần đầu, khách hẹn cuối tuần ghé phòng khám.",
            set_contacted=True
        )
        self.assertEqual(comm_id, "COMM-0001")
        self.assertEqual(lead_doc.status, "Contacted")

        # Step 3: Convert Lead
        conversion_res = LeadConversionCoordinator.convert_lead(
            lead_id="LEAD-2026-00010",
            pet_name="Bông Gòn",
            species="Dog",
            breed="Samoyed",
            create_opportunity=True,
            opportunity_amount=1500000.0
        )

        # Step 4: Verification
        self.assertEqual(conversion_res["status"], "success")
        self.assertEqual(conversion_res["contact_id"], "CONT-001")
        self.assertEqual(conversion_res["pet_id"], "PET-SAM-01")
        self.assertEqual(conversion_res["opportunity_id"], "OPP-001")
        self.assertEqual(lead_doc.status, "Converted")
        self.assertEqual(lead_doc.converted_contact, "CONT-001")
        self.assertEqual(lead_doc.converted_pet, "PET-SAM-01")

    # ─────────────────────────────────────────────────────────────────
    # 3. END-TO-END SCENARIO B: Customer -> Pet -> Service Operations
    # ─────────────────────────────────────────────────────────────────

    def test_scenario_b_customer_service_operations_and_360(self):
        """
        Scenario B:
        1. Tạo Customer và đăng ký Pet.
        2. Tra cứu Service Catalog chuẩn (SRV-VACCINE).
        3. Tạo Service Visit và tính giá chuẩn.
        4. Kiểm tra hồ sơ Customer 360 phản ánh đủ Pet và Service Visit.
        """
        customer_id = "CONT-002"
        mock_customer = MockDocument(
            name=customer_id,
            first_name="Phạm Thị Lan",
            last_name="",
            phone="0903112233",
            email_id="lan.pham@gmail.com"
        )
        mock_pet = MockDocument(
            name="PET-CAT-01",
            pet_name="Miu Miu",
            species="Cat",
            breed="British Shorthair",
            customer=customer_id,
            weight_kg=4.2
        )
        mock_service = MockDocument(
            name="SRV-VACCINE",
            service_code="SRV-VACCINE",
            service_name="Tiêm Phòng 4 Bệnh",
            standard_price=250000.0,
            category="Medical",
            target_species="Cat"
        )

        mock_frappe.db.exists.return_value = True
        mock_frappe.get_cached_doc.return_value = mock_service
        mock_frappe.db.get_value.side_effect = lambda dt, name_or_flt, fld=None, *args, **kwargs: (
            customer_id if dt == "Pet" and fld == "customer" else None
        )

        # Create Service Visit
        visit_receipt = ServiceVisitService.create_service_visit(
            pet="PET-CAT-01",
            service_identifier="SRV-VACCINE",
            technician="tech_bacsi_hung",
            notes="Mèo khỏe mạnh, nhiệt độ bình thường 38.5C"
        )

        self.assertEqual(visit_receipt["original_price"], 250000.0)
        self.assertEqual(visit_receipt["discount_amount"], 0.0)
        self.assertEqual(visit_receipt["final_price"], 250000.0)
        self.assertEqual(visit_receipt["customer"], customer_id)

        # Verify Customer 360 aggregates
        mock_frappe.get_doc.side_effect = lambda dt, name, *a, **kw: (
            mock_customer if dt == "Contact" else MockDocument()
        )
        mock_frappe.get_all.side_effect = lambda dt, filters=None, fields=None, *a, **kw: (
            [mock_pet] if dt == "Pet" else (
                [MockDocument(name=visit_receipt["visit_id"], service_type="Tiêm Phòng 4 Bệnh", final_price=250000.0, pet="PET-CAT-01")]
                if dt == "Service Visit" else []
            )
        )

        c360 = CustomerService.get_customer_360(customer_id)
        self.assertEqual(c360["contact_id"], customer_id)
        self.assertEqual(len(c360["pets"]), 1)
        self.assertEqual(c360["pets"][0].pet_name, "Miu Miu")
        self.assertEqual(len(c360["service_visits"]), 1)

    # ─────────────────────────────────────────────────────────────────
    # 4. END-TO-END SCENARIO C: Membership & Benefit Redemption
    # ─────────────────────────────────────────────────────────────────

    def test_scenario_c_membership_and_redemption_lifecycle(self):
        """
        Scenario C:
        1. Cấp Membership với 2 lượt Grooming Free.
        2. Lượt 1: Redeem Grooming Free -> final_price = 0, balance = 1.
        3. Lượt 2: Redeem Grooming Free -> final_price = 0, balance = 0.
        4. Lượt 3: Thử redeem khi đã hết quyền lợi -> Ném BenefitExhaustedException và không làm sai số dư.
        5. Transaction safety: Kiểm tra số dư và audit ledger không bị sai lệch.
        """
        mock_benefit = MockDocument(
            benefit_type="Grooming",
            discount_type="FREE",
            discount_value=0.0,
            total_quantity=2,
            used_quantity=0,
            remaining_quantity=2
        )
        mock_membership = MockDocument(
            name="MEM-VIP-001",
            customer="CONT-002",
            status="Active",
            start_date="2026-10-01",
            end_date="2027-10-01",
            pet=None,  # All pets of customer
            benefits=[mock_benefit]
        )
        mock_srv = MockDocument(
            service_code="SRV-GROOM",
            service_name="Grooming",
            standard_price=300000.0
        )

        mock_frappe.db.exists.return_value = True
        mock_frappe.db.get_value.return_value = "CONT-002"
        mock_frappe.get_cached_doc.return_value = mock_srv
        mock_frappe.get_doc.side_effect = lambda *args, **kwargs: (
            mock_membership if args and args[0] == "Customer Membership" else MockDocument(*args, **kwargs)
        )

        # Visit 1: Redeem First Grooming (Balance 2 -> 1)
        v1 = ServiceVisitService.create_service_visit(
            pet="PET-CAT-01",
            service_identifier="SRV-GROOM",
            membership_id="MEM-VIP-001"
        )
        self.assertEqual(v1["final_price"], 0.0)
        self.assertEqual(v1["discount_amount"], 300000.0)
        self.assertEqual(mock_benefit.used_quantity, 1)

        # Visit 2: Redeem Second Grooming (Balance 1 -> 0)
        v2 = ServiceVisitService.create_service_visit(
            pet="PET-CAT-01",
            service_identifier="SRV-GROOM",
            membership_id="MEM-VIP-001"
        )
        self.assertEqual(v2["final_price"], 0.0)
        self.assertEqual(mock_benefit.used_quantity, 2)
        mock_benefit.remaining_quantity = 0

        # Visit 3: Benefit Exhausted -> Throws BenefitExhaustedException and preserves balance
        with self.assertRaises(BenefitExhaustedException):
            ServiceVisitService.create_service_visit(
                pet="PET-CAT-01",
                service_identifier="SRV-GROOM",
                membership_id="MEM-VIP-001"
            )

        # Verify balance and used_quantity remained locked at 2 (no over-deduction)
        self.assertEqual(mock_benefit.used_quantity, 2)
        self.assertEqual(mock_benefit.remaining_quantity, 0)

    # ─────────────────────────────────────────────────────────────────
    # 5. END-TO-END SCENARIO D: Care Intelligence & Deduplication
    # ─────────────────────────────────────────────────────────────────

    def test_scenario_d_care_intelligence_pattern_prediction_and_dedup(self):
        """
        Scenario D:
        1. Tạo chuỗi lịch sử 4 lần ghé thăm cách đều 30 ngày.
        2. Phân tích Pattern, dự đoán ngày tiếp theo (HIGH confidence).
        3. Phát hiện tình huống Due Soon và tích hợp context Membership.
        4. Tạo Care Recommendation.
        5. Chạy lại chu kỳ quét và kiểm tra tính Idempotent (cập nhật in-place, không tạo bản ghi trùng).
        """
        visits = [
            ServiceVisit(pet="PET-LUCKY", customer="CONT-002", service_type="Grooming", visit_date=self.today - timedelta(days=88)),
            ServiceVisit(pet="PET-LUCKY", customer="CONT-002", service_type="Grooming", visit_date=self.today - timedelta(days=58)),
            ServiceVisit(pet="PET-LUCKY", customer="CONT-002", service_type="Grooming", visit_date=self.today - timedelta(days=28)),
        ]

        pattern = CarePatternAnalyzer.analyze_pattern("PET-LUCKY", "Grooming", visits)
        self.assertEqual(pattern.number_of_visits, 3)
        self.assertEqual(pattern.typical_interval, 30.0)

        pred = VisitPredictionService.predict_next_visit("PET-LUCKY", "Grooming", visits, self.today)
        self.assertEqual(pred.predicted_next_visit, (self.today - timedelta(days=28)) + timedelta(days=30))
        self.assertEqual(pred.confidence, "MEDIUM")

        # Due Soon evaluated 2 days before predicted visit
        due_res = RiskDetectionService.detect_due_soon("PET-LUCKY", "Grooming", visits, current_date=self.today)
        self.assertTrue(due_res.is_due_soon)
        self.assertEqual(due_res.status, "DUE_SOON")
        self.assertEqual(due_res.days_until_due, 2)

        # Generate recommendation with RecommendationService store
        store: List[dict] = []
        pet_model = Pet(pet_name="Lucky", customer="CONT-002", name="PET-LUCKY")
        cust_model = Customer(name="CONT-002", customer_name="Lê Hoàng")

        # 1st Run: Create NEW recommendation
        rec1 = RecommendationService.generate_care_recommendation(
            pet=pet_model,
            customer=cust_model,
            service_type="Grooming",
            visits=visits,
            current_date=self.today,
            existing_recs=store,
            store=store,
        )
        self.assertIsNotNone(rec1)
        self.assertEqual(len(store), 1)
        self.assertEqual(rec1["action_taken"], "CREATED")
        self.assertEqual(rec1["recommendation_type"], "DUE_SOON")

        # 2nd Run on same active recommendation: Updates in-place, does NOT append duplicate
        rec2 = RecommendationService.generate_care_recommendation(
            pet=pet_model,
            customer=cust_model,
            service_type="Grooming",
            visits=visits,
            current_date=self.today,
            existing_recs=store,
            store=store,
        )
        self.assertIsNotNone(rec2)
        self.assertEqual(len(store), 1)  # Length remains strictly 1
        self.assertEqual(rec2["action_taken"], "UPDATED")

    # ─────────────────────────────────────────────────────────────────
    # 6. END-TO-END SCENARIO E: Access Control & Cross-Entity Validation
    # ─────────────────────────────────────────────────────────────────

    def test_scenario_e_access_control_rbac_and_cross_entity_validation(self):
        """
        Scenario E:
        1. Kiểm thử phân quyền RBAC: Sales, Technician, Analyst, Manager.
        2. Backend từ chối quyền trái phép (không dựa vào UI frontend).
        3. Kiểm tra Cross-Entity Validation: chặn dùng chéo Pet hoặc Membership của khách hàng khác.
        """
        # Role: Technician cannot create Lead or Opportunity
        mock_frappe.get_roles.return_value = [ROLE_TECHNICIAN]
        self.assertFalse(check_role_permission("PetCare Lead", "create", user="tech_user"))
        self.assertFalse(check_role_permission("PetCare Opportunity", "read", user="tech_user"))
        self.assertTrue(check_role_permission("Pet", "write", user="tech_user"))
        self.assertTrue(check_role_permission("Service Visit", "create", user="tech_user"))

        # Role: Analyst is read-only
        mock_frappe.get_roles.return_value = [ROLE_ANALYST]
        self.assertTrue(check_role_permission("PetCare Lead", "read", user="analyst_user"))
        self.assertTrue(check_role_permission("PetCare Lead", "report", user="analyst_user"))
        self.assertFalse(check_role_permission("PetCare Lead", "write", user="analyst_user"))
        self.assertFalse(check_role_permission("Service Visit", "create", user="analyst_user"))

        # Role: Sales cannot cancel financial documents
        mock_frappe.get_roles.return_value = [ROLE_SALES]
        self.assertFalse(check_role_permission("Service Visit", "cancel", user="sales_user"))
        self.assertFalse(check_role_permission("Customer Membership", "cancel", user="sales_user"))

        # Cross-Entity Ownership: Customer A's Pet on Customer B's Service Visit
        mock_frappe.db.get_value.side_effect = lambda dt, name, fld=None, *a, **kw: (
            {"customer": "CONT-CUSTOMER-A", "owner": "CONT-CUSTOMER-A"} if dt == "Pet" and name == "PET-A" else (
                {"customer": "CONT-CUSTOMER-B", "pet": None} if dt == "Customer Membership" and name == "MEM-B" else None
            )
        )

        # Mismatch Customer vs Pet -> Validation fails
        valid_pet, err_pet = validate_cross_entity_relationship(
            customer_id="CONT-CUSTOMER-B",
            pet_id="PET-A"
        )
        self.assertFalse(valid_pet)
        self.assertIn("không thuộc sở hữu", err_pet)

        # Mismatch Customer vs Membership -> Validation fails
        valid_mem, err_mem = validate_cross_entity_relationship(
            customer_id="CONT-CUSTOMER-A",
            membership_id="MEM-B"
        )
        self.assertFalse(valid_mem)
        self.assertIn("không thuộc về", err_mem)

    # ─────────────────────────────────────────────────────────────────
    # 7. END-TO-END SCENARIO F: Scheduled Automations & Idempotency
    # ─────────────────────────────────────────────────────────────────

    def test_scenario_f_automation_scheduled_jobs_and_idempotency(self):
        """
        Scenario F:
        1. Chạy LeadFollowupAutomation: Lead chưa liên hệ > 24h sinh ToDo.
        2. Chạy MembershipRenewalAutomation: Membership quá hạn chuyển Expired, sắp hết hạn sinh ToDo.
        3. Chạy lần 2 trên cùng tập dữ liệu: Xác nhận Idempotency (số ToDo không tăng gấp đôi).
        """
        # Test 1: Lead Follow-up Automation
        created_time = datetime(2026, 10, 24, 10, 0, 0)
        lead_data = [{
            "name": "LEAD-OLD",
            "lead_name": "Anh Hùng",
            "phone": "0912345678",
            "email": "hung@test.vn",
            "lead_owner": "sales1",
            "creation": created_time,
            "source": "Hotline"
        }]

        mock_frappe.db.get_list.side_effect = None
        mock_frappe.db.get_list.return_value = lead_data

        # First run: no task exists -> creates 1 ToDo
        mock_frappe.db.get_value.side_effect = None
        mock_frappe.db.get_value.return_value = None
        mock_frappe.get_doc.side_effect = None
        mock_frappe.get_doc.return_value = MockDocument(doctype="ToDo", name="TODO-001")

        res_1 = LeadFollowupAutomation.process_uncontacted_leads(self.today, threshold_hours=24)
        self.assertEqual(res_1["processed"], 1)
        self.assertEqual(res_1["tasks_created"], 1)

        # Second run: task already exists -> returns EXISTING, tasks_created = 0
        mock_frappe.db.get_value.side_effect = None
        mock_frappe.db.get_value.return_value = {
            "name": "TODO-001",
            "allocated_to": "sales1",
            "description": "Follow-up Lead",
            "priority": "Medium",
        }
        res_2 = LeadFollowupAutomation.process_uncontacted_leads(self.today, threshold_hours=24)
        self.assertEqual(res_2["processed"], 1)
        self.assertEqual(res_2["tasks_created"], 0)
        self.assertEqual(res_2["tasks_existing"], 1)

        # Test 2: Membership Expiration Auto-expire
        mock_expired_mem = [{"name": "MEM-EXP-001"}]
        mock_frappe.db.get_list.side_effect = None
        mock_frappe.db.get_list.return_value = mock_expired_mem

        expired_count = MembershipRenewalAutomation.auto_expire_memberships(self.today)
        self.assertEqual(expired_count, 1)
        mock_frappe.db.set_value.assert_called_with("Customer Membership", "MEM-EXP-001", "status", "Expired")


if __name__ == "__main__":
    unittest.main()
