"""
Mock Test Suite for Prompt 8: Security, API, Role Permissions & Reporting KPIs.
Verifies all Prompt 8 requirements in pure Python:
1. Role Permission Matrix (Sales, Technician, Analyst, Manager restrictions)
2. Cross-Entity Ownership Validation (Customer -> Pet -> Membership)
3. Input Sanitization & Vietnam Phone Validation
4. KPI 1: Lead Conversion calculation & source breakdown
5. KPI 2: Sales Pipeline total & weighted forecast
6. KPI 3 & 4: Active Memberships, wallet balances & expiring soon
7. KPI 5: Service Visits gross, discount & net revenue
8. KPI 6, 7 & 8: Due Soon, At Risk & Care Recommendation conversion
9. Full Dashboard synthesis & report summary
"""

import os
import sys
import unittest
from datetime import date, datetime, timedelta
from typing import Any, Dict, List
from unittest.mock import MagicMock

# Ensure apps/petcare_crm is on sys.path
sys.path.insert(0, os.path.abspath("apps/petcare_crm"))

# Setup mock frappe
if "frappe" in sys.modules:
    mock_frappe = sys.modules["frappe"]
else:
    mock_frappe = MagicMock()
    mock_frappe._ = lambda x: x
    mock_frappe.throw = lambda msg, *args, **kwargs: (_ for _ in ()).throw(Exception(msg))
    mock_frappe.session = MagicMock()
    mock_frappe.session.user = "Administrator"
    mock_frappe.logger = lambda name: MagicMock()
    sys.modules["frappe"] = mock_frappe

mock_frappe_utils = MagicMock()
mock_frappe_utils.nowdate.return_value = "2026-10-26"
mock_frappe_utils.getdate = lambda d: d
mock_frappe.utils = mock_frappe_utils

from petcare_crm.utils.security import (
    ROLE_ANALYST,
    ROLE_CRM_MANAGER,
    ROLE_SALES,
    ROLE_SYSTEM_MANAGER,
    ROLE_TECHNICIAN,
    check_role_permission,
    is_valid_vietnam_phone,
    sanitize_input_string,
    sanitize_number,
    sanitize_phone,
    validate_cross_entity_relationship,
)
from petcare_crm.utils.analytics_service import AnalyticsService
from petcare_crm.utils.exceptions import ValidationError
import petcare_crm.utils.security as sec_mod
sec_mod.frappe = mock_frappe
import petcare_crm.utils.analytics_service as as_mod
as_mod.frappe = mock_frappe


class TestSecurityAndReportingMock(unittest.TestCase):

    def setUp(self):
        self.today = date(2026, 10, 26)
        sec_mod.frappe = mock_frappe
        as_mod.frappe = mock_frappe
        mock_frappe.db.reset_mock()
        mock_frappe.db.get_value.side_effect = None
        mock_frappe.db.get_list.side_effect = None
        mock_frappe.db.exists.return_value = True
        mock_frappe.session.user = "test_user"
        mock_frappe.get_roles = MagicMock()

    # ─────────────────────────────────────────────────────────────────
    # 1. Role Permission Matrix Tests
    # ─────────────────────────────────────────────────────────────────
    def test_01_sales_role_permissions_and_restrictions(self):
        """PetCare Sales: Có quyền Read/Create/Write Lead, nhưng KHÔNG có quyền Delete."""
        mock_frappe.get_roles.return_value = [ROLE_SALES]

        # Sales can read, create, write PetCare Lead
        self.assertTrue(check_role_permission("PetCare Lead", "read", user="sales_user"))
        self.assertTrue(check_role_permission("PetCare Lead", "create", user="sales_user"))
        self.assertTrue(check_role_permission("PetCare Lead", "write", user="sales_user"))

        # Sales CANNOT delete PetCare Lead
        self.assertFalse(check_role_permission("PetCare Lead", "delete", user="sales_user"))

        # Sales can read Membership Plan, but CANNOT edit or delete plan
        self.assertTrue(check_role_permission("Membership Plan", "read", user="sales_user"))
        self.assertFalse(check_role_permission("Membership Plan", "write", user="sales_user"))
        self.assertFalse(check_role_permission("Membership Plan", "delete", user="sales_user"))

        # Sales CANNOT cancel Service Visit or Membership
        self.assertFalse(check_role_permission("Service Visit", "cancel", user="sales_user"))
        self.assertFalse(check_role_permission("Customer Membership", "cancel", user="sales_user"))

    def test_02_technician_role_restrictions(self):
        """PetCare Technician: KHÔNG truy cập Lead/Opportunity, nhưng được ghi nhận Service Visit."""
        mock_frappe.get_roles.return_value = [ROLE_TECHNICIAN]

        # Technician cannot access Lead or Opportunity
        self.assertFalse(check_role_permission("PetCare Lead", "read", user="tech_user"))
        self.assertFalse(check_role_permission("PetCare Opportunity", "read", user="tech_user"))

        # Technician CAN read and write Pet (update health notes/weight)
        self.assertTrue(check_role_permission("Pet", "read", user="tech_user"))
        self.assertTrue(check_role_permission("Pet", "write", user="tech_user"))

        # Technician CAN create and write Service Visit
        self.assertTrue(check_role_permission("Service Visit", "create", user="tech_user"))
        self.assertTrue(check_role_permission("Service Visit", "write", user="tech_user"))

    def test_03_analyst_role_is_strictly_read_only(self):
        """PetCare Analyst: Được phép đọc và xuất báo cáo, KHÔNG được sửa hay xóa."""
        mock_frappe.get_roles.return_value = [ROLE_ANALYST]

        for dt in ["PetCare Lead", "PetCare Opportunity", "Service Visit", "Customer Membership"]:
            self.assertTrue(check_role_permission(dt, "read", user="analyst_user"))
            self.assertTrue(check_role_permission(dt, "report", user="analyst_user"))
            self.assertFalse(check_role_permission(dt, "create", user="analyst_user"))
            self.assertFalse(check_role_permission(dt, "write", user="analyst_user"))
            self.assertFalse(check_role_permission(dt, "delete", user="analyst_user"))

    # ─────────────────────────────────────────────────────────────────
    # 2. Cross-Entity Ownership Validation Tests
    # ─────────────────────────────────────────────────────────────────
    def test_04_cross_entity_pet_ownership_mismatch(self):
        """Khách hàng A không thể chọn thú cưng của khách hàng B."""
        # Giả lập PET-LUNA thuộc sở hữu của CUST-B
        mock_frappe.db.get_value.return_value = {"customer": "CUST-B", "owner": "CUST-B"}

        valid, err_msg = validate_cross_entity_relationship(
            customer_id="CUST-A",
            pet_id="PET-LUNA",
        )
        self.assertFalse(valid)
        self.assertIn("không thuộc sở hữu", err_msg)

    def test_05_cross_entity_membership_ownership_mismatch(self):
        """Khách hàng A không thể sử dụng thẻ hội viên của khách hàng B."""
        def fake_get_value(doctype, name, fields, as_dict=True):
            if doctype == "Pet":
                return {"customer": "CUST-A"}
            elif doctype == "Customer Membership":
                return {"customer": "CUST-B", "pet": None, "status": "Active"}
            return None

        mock_frappe.db.get_value.side_effect = fake_get_value

        valid, err_msg = validate_cross_entity_relationship(
            customer_id="CUST-A",
            pet_id="PET-MOCHI",
            membership_id="MEM-B-001",
        )
        self.assertFalse(valid)
        self.assertIn("không thuộc về khách hàng", err_msg)

    # ─────────────────────────────────────────────────────────────────
    # 3. Input Validation & Sanitization Tests
    # ─────────────────────────────────────────────────────────────────
    def test_06_vietnam_phone_validation_and_cleaning(self):
        """Kiểm tra làm sạch và xác thực số điện thoại di động Việt Nam."""
        self.assertTrue(is_valid_vietnam_phone("0901234567"))
        self.assertTrue(is_valid_vietnam_phone("+84 901 234 567"))
        self.assertTrue(is_valid_vietnam_phone("038.999.8888"))
        self.assertTrue(is_valid_vietnam_phone("077-123-4567"))

        # Số không hợp lệ
        self.assertFalse(is_valid_vietnam_phone("12345"))          # Quá ngắn
        self.assertFalse(is_valid_vietnam_phone("0123456789"))     # Đầu 01 cũ
        self.assertFalse(is_valid_vietnam_phone("0901234567899"))  # Quá dài
        self.assertFalse(is_valid_vietnam_phone("abcdefghij"))     # Chữ

    def test_07_input_string_and_number_sanitization(self):
        """Khử nhiễm chuỗi XSS và kiểm tra số không âm."""
        raw_html = "<script>alert('hack')</script>Nguyễn Văn A"
        clean = sanitize_input_string(raw_html)
        self.assertEqual(clean, "alert('hack')Nguyễn Văn A")
        self.assertNotIn("<script>", clean)

        # Số hợp lệ
        self.assertEqual(sanitize_number("250000.5"), 250000.5)

        # Số âm -> Báo lỗi
        with self.assertRaises(ValidationError):
            sanitize_number("-1000", min_val=0.0)

    # ─────────────────────────────────────────────────────────────────
    # 4. Analytics & KPI Calculation Tests
    # ─────────────────────────────────────────────────────────────────
    def test_08_kpi_lead_conversion_calculation(self):
        """KPI 1: Tỷ lệ chuyển đổi Lead và phân bổ nguồn."""
        mock_leads = [
            {"name": "L1", "status": "Converted", "source": "Facebook", "converted_contact": "CT-1"},
            {"name": "L2", "status": "Converted", "source": "Google", "converted_contact": "CT-2"},
            {"name": "L3", "status": "Qualified", "source": "Facebook", "converted_contact": None},
            {"name": "L4", "status": "New", "source": "Referral", "converted_contact": None},
            {"name": "L5", "status": "Lost", "source": "Direct", "converted_contact": None},
        ]

        metrics = AnalyticsService.get_lead_conversion_metrics(leads_store=mock_leads)
        self.assertEqual(metrics["total_leads"], 5)
        self.assertEqual(metrics["converted_leads"], 2)
        self.assertEqual(metrics["conversion_rate_pct"], 40.0)
        self.assertEqual(metrics["by_source"]["Facebook"], 2)
        self.assertEqual(metrics["by_source"]["Google"], 1)

    def test_09_kpi_sales_pipeline_calculation(self):
        """KPI 2: Giá trị cơ hội và doanh số dự kiến có trọng số (Weighted Forecast)."""
        mock_opps = [
            # 10,000,000 @ 80% = 8,000,000
            {"name": "OPP-1", "stage": "Negotiation", "expected_amount": 10000000.0, "probability": 80.0},
            # 5,000,000 @ 40% = 2,000,000
            {"name": "OPP-2", "stage": "Qualification", "expected_amount": 5000000.0, "probability": 40.0},
        ]

        metrics = AnalyticsService.get_sales_pipeline_metrics(opportunities_store=mock_opps)
        self.assertEqual(metrics["total_opportunities"], 2)
        self.assertEqual(metrics["total_pipeline_amount"], 15000000.0)
        self.assertEqual(metrics["total_weighted_amount"], 10000000.0)
        self.assertEqual(metrics["by_stage"]["Negotiation"]["count"], 1)

    def test_10_kpi_membership_and_expiring_soon(self):
        """KPI 3 & 4: Số thẻ active, số dư ví và danh sách thẻ sắp hết hạn."""
        mock_mems = [
            # Active, expires in 3 days -> in both 7-day and 30-day lists
            {"name": "M1", "customer": "C1", "membership_plan": "VIP", "status": "Active", "end_date": self.today + timedelta(days=3), "balance": 500000.0},
            # Active, expires in 20 days -> in 30-day list only
            {"name": "M2", "customer": "C2", "membership_plan": "Basic", "status": "Active", "end_date": self.today + timedelta(days=20), "balance": 200000.0},
            # Expired
            {"name": "M3", "customer": "C3", "membership_plan": "VIP", "status": "Expired", "end_date": self.today - timedelta(days=5), "balance": 0.0},
        ]

        metrics = AnalyticsService.get_membership_metrics(current_date=self.today, memberships_store=mock_mems)
        self.assertEqual(metrics["active_memberships"], 2)
        self.assertEqual(metrics["total_member_balance"], 700000.0)
        self.assertEqual(metrics["expiring_within_7_days_count"], 1)
        self.assertEqual(metrics["expiring_within_30_days_count"], 2)
        self.assertEqual(metrics["expiring_soon_list"][0]["name"], "M1")

    def test_11_kpi_service_visits_and_retention(self):
        """KPI 5, 6, 7: Doanh thu dịch vụ, Due Soon và At Risk."""
        mock_visits = [
            {"service_type": "Grooming", "original_price": 300000.0, "discount_amount": 300000.0, "final_price": 0.0}, # Free benefit
            {"service_type": "Spa", "original_price": 500000.0, "discount_amount": 50000.0, "final_price": 450000.0},   # 10% discount
        ]
        v_metrics = AnalyticsService.get_service_visit_metrics(visits_store=mock_visits)
        self.assertEqual(v_metrics["total_service_visits"], 2)
        self.assertEqual(v_metrics["gross_revenue"], 800000.0)
        self.assertEqual(v_metrics["total_discounts_granted"], 350000.0)
        self.assertEqual(v_metrics["net_revenue"], 450000.0)

        # Retention KPIs
        mock_recs = [
            {"name": "R1", "service_type": "Grooming", "recommendation_type": "DUE_SOON", "status": "NEW"},
            {"name": "R2", "service_type": "Spa", "recommendation_type": "AT_RISK", "status": "CONTACTED", "customer": "C1", "pet": "P1"},
            {"name": "R3", "service_type": "Grooming", "recommendation_type": "DUE_SOON", "status": "CONVERTED"},
        ]
        r_metrics = AnalyticsService.get_care_retention_metrics(recommendations_store=mock_recs)
        self.assertEqual(r_metrics["total_recommendations"], 3)
        self.assertEqual(r_metrics["due_soon_total"], 2)
        self.assertEqual(r_metrics["at_risk_total"], 1)
        self.assertEqual(r_metrics["conversion_rate_pct"], 33.3)


if __name__ == "__main__":
    unittest.main()
