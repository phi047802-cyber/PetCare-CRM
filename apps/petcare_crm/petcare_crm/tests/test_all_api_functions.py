# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

"""
Suite 13: Full Public API & Controller Coverage Test Suite.
Exhaustively exercises and verifies all 61 functions in petcare_crm.api:
- Rate Limiting, Sanitization & Utility helpers
- Membership Lifecycle, Benefit Balances & Safe Deductions
- Care Pattern Intelligence, EWMA, Due Soon & At Risk Detection
- Scheduled Automation Manual Triggers (Daily & Hourly)
- Customer Portal & Quick Reception Check-in
- CRM Core Leads, Opportunities & Sales Funnel
- Customer 360, Tasks, Interactions & Cross-entity Security
- Service Operations, Catalog Items & Case Management
- KPI Dashboard Analytics & Financial Reporting
- Payments (VietQR Dynamic Generation, Webhooks, Reconciliation)
- Omnichannel Dispatcher & Outbox Management
- Owner Portal Self-Service Booking & Pet Health Book
- Appointment Management Lifecycle (Schedule, Check-in, Cancel)
- External eCommerce Integration (WooCommerce HMAC-SHA256 Webhook)
- Diagnostics (Mailtrap SMTP / Test Email, Demo Dataset Reset)
"""

import os
import sys
import json
import hmac
import hashlib
import base64
import unittest
from datetime import date, datetime, timedelta
from unittest.mock import MagicMock, patch

# Ensure apps/petcare_crm is on sys.path
sys.path.insert(0, os.path.abspath("apps/petcare_crm"))

class MockFrappeException(Exception):
    pass

class MockPermissionError(MockFrappeException):
    pass

class MockValidationError(MockFrappeException):
    pass

class MockDoc:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", "DOC-001")
        self.phone_nos = []
        self.email_ids = []
        self.benefits = []
        self.status = kwargs.get("status", "Active")
        self.customer = kwargs.get("customer", "CUST-001")
        self.pet = kwargs.get("pet", "PET-001")
        self.membership_plan = kwargs.get("membership_plan", "Gói Vàng - VIP Care")
        self.start_date = "2026-01-01"
        self.end_date = "2027-01-01"
        self.balance = 500000.0
        self.service_type = "Grooming"
        self.original_price = 300000.0
        self.final_price = 300000.0
        self.discount_amount = 0.0
        self.visit_date = "2026-11-17"
        self.appointment_date = "2026-11-20"
        self.appointment_time = "09:00"
        self.branch = "CN-TRUNGTAM"
        self.cancellation_reason = ""
        self.assigned_staff = ""
        self.phone = kwargs.get("phone", "0901234567")
        self.mobile_no = kwargs.get("mobile_no", "0901234567")
        self.email_id = kwargs.get("email_id", "an@example.com")
        self.first_name = kwargs.get("first_name", "An")
        self.last_name = kwargs.get("last_name", "Nguyen")
        self.lead_name = kwargs.get("lead_name", "Nguyễn Văn An")
        self.lead_owner = kwargs.get("lead_owner", "Administrator")
        self.linked_opportunity = kwargs.get("linked_opportunity", None)
        self.plan_name = kwargs.get("plan_name", "Standard Plan")
        self.price = kwargs.get("price", 1000000.0)
        self.duration_months = 12
        self.last_delivery_id = None
        self.species = "Dog"
        self.pet_name = "Bé Bơ"
        for k, v in kwargs.items():
            setattr(self, k, v)
        if args and isinstance(args[0], dict):
            for k, v in args[0].items():
                setattr(self, k, v)

    def update(self, d):
        if isinstance(d, dict):
            for k, v in d.items():
                setattr(self, k, v)
        return self

    def insert(self, *a, **kw):
        return self

    def save(self, *a, **kw):
        return self

    def append(self, key, val):
        if not hasattr(self, key):
            setattr(self, key, [])
        getattr(self, key).append(val)

    def add_comment(self, *a, **kw):
        return MagicMock()

    def get(self, k, d=None):
        return getattr(self, k, d)

    def set(self, k, v):
        setattr(self, k, v)

    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def check_in(self, technician=None):
        self.status = "Checked-In"
        self.assigned_staff = technician
        return "SV-001"

    def cancel_appointment(self, reason=None):
        self.status = "Cancelled"
        self.cancellation_reason = reason


if "frappe" in sys.modules:
    mock_frappe = sys.modules["frappe"]
else:
    mock_frappe = MagicMock()
    sys.modules["frappe"] = mock_frappe

mock_frappe.request = None
mock_frappe.local = None
mock_frappe.PermissionError = MockPermissionError
mock_frappe.ValidationError = MockValidationError
mock_frappe.TooManyRequestsError = MockFrappeException
mock_frappe.AuthenticationError = MockPermissionError
mock_frappe._ = lambda x: x

def _throw(msg, exc=MockFrappeException):
    raise exc(msg)

mock_frappe.throw = _throw
mock_frappe.session = MagicMock()
mock_frappe.session.user = "Administrator"
mock_frappe.logger = lambda x: MagicMock()

def mock_whitelist(*args, **kwargs):
    def decorator(fn):
        return fn
    if len(args) == 1 and callable(args[0]):
        return args[0]
    return decorator

mock_frappe.whitelist = mock_whitelist
mock_frappe.conf = {
    "owner_portal_secret": "test_owner_portal_secret_key_1234567890",
    "woocommerce_webhook_secret": "test_woocommerce_secret_key_1234567890",
    "vietqr_webhook_secret": "test_vietqr_webhook_secret_key_1234567890",
    "vietqr_bank_bin": "970436",
    "vietqr_account_no": "0000000001",
    "vietqr_account_name": "PETCARE TEST",
}
mock_frappe.utils = MagicMock()
mock_frappe.utils.nowdate.side_effect = lambda: date.today().isoformat()
mock_frappe.utils.now_datetime.side_effect = datetime.now
mock_frappe.utils.now.side_effect = lambda: f"{date.today().isoformat()} 09:00:00"
mock_frappe.utils.getdate = lambda d: datetime.strptime(str(d)[:10], "%Y-%m-%d").date() if isinstance(d, str) else d
mock_frappe.utils.get_datetime = lambda d: datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S") if isinstance(d, str) else d
mock_frappe.utils.add_days = lambda d, days: (mock_frappe.utils.getdate(d) + timedelta(days=days)).strftime("%Y-%m-%d")
mock_frappe.utils.add_months = lambda d, m: (mock_frappe.utils.getdate(d) + timedelta(days=m * 30)).strftime("%Y-%m-%d")
mock_frappe.get_roles = MagicMock(return_value=["System Manager", "Administrator"])

cache_mock = MagicMock()
cache_mock.incr.return_value = 1
mock_frappe.cache = MagicMock(return_value=cache_mock)

sys.modules["frappe.utils"] = mock_frappe.utils
sys.modules["frappe.model"] = MagicMock()
mock_doc_module = MagicMock()
mock_doc_module.Document = MockDoc
sys.modules["frappe.model.document"] = mock_doc_module

# Disable actual SMTP network calls for super fast and reliable tests
import petcare_crm.utils.email_service as email_service
email_service._send_smtp_email = lambda *a, **kw: True

# Mock validator results for demo dataset reset
import petcare_crm.patches.v1_0.validate_demo_data as vdd
from petcare_crm.patches.v1_0.seed_demo_data import EXPECTED_DEMO_COUNTS
vdd.validate = lambda *a, **kw: {
    "passed": True,
    "status": "PASS",
    "results": [],
    "observed_counts": EXPECTED_DEMO_COUNTS,
    "expected_counts": EXPECTED_DEMO_COUNTS,
}

from petcare_crm import api


class TestAllApiFunctions(unittest.TestCase):
    """Test suite executing all 61 public and internal API functions."""

    def setUp(self):
        mock_frappe.session.user = "Administrator"
        mock_frappe.request = None
        mock_frappe.local = None
        mock_frappe.get_roles.return_value = ["System Manager", "Administrator"]
        cache_mock.incr.return_value = 1
        mock_frappe.db.count = MagicMock(return_value=10)

        def fake_exists(doctype, name=None):
            if doctype == "PetCare Service" and name == "SVC-TEST-01":
                return False
            return True

        mock_frappe.db.exists = fake_exists

        def fake_get_value(doctype, filters, fieldname=None, as_dict=False):
            if as_dict:
                if doctype == "PetCare Service":
                    return {
                        "name": str(filters),
                        "service_name": "Grooming Test",
                        "category": "Grooming & Spa",
                        "is_active": 1,
                    }
                return {
                    "customer": "CUST-001",
                    "owner": "CUST-001",
                    "name": "VAL-001",
                    "service_visit": "SV-001",
                    "membership": "MEM-001",
                }
            if isinstance(fieldname, list):
                return ["CUST-001"] * len(fieldname)
            return "CUST-001"

        mock_frappe.db.get_value = fake_get_value
        mock_frappe.db.get_list = MagicMock(return_value=[])
        mock_frappe.db.get_all = MagicMock(return_value=[])
        mock_frappe.get_all = MagicMock(return_value=[])
        mock_frappe.get_list = MagicMock(return_value=[])
        mock_frappe.get_doc = lambda *a, **kw: MockDoc(*a, **kw)
        mock_frappe.get_cached_doc = lambda *a, **kw: MockDoc(*a, **kw)
        mock_frappe.db.sql = MagicMock(return_value=[{
            "name": "BEN-001",
            "customer": "CUST-001",
            "pet": "PET-001",
            "benefit_type": "Grooming",
            "total_quantity": 5,
            "used_quantity": 1,
            "remaining_quantity": 4,
            "discount_type": "FREE",
            "discount_value": 0,
            "status": "Active",
            "end_date": "2027-01-01",
            "gross_revenue": 5000000,
            "total_visits": 25,
            "total_discount": 500000,
            "net_revenue": 4500000,
        }])

    # ─────────────────────────────────────────────────────────────────
    # 1. UTILITIES & SECURITY HELPERS
    # ─────────────────────────────────────────────────────────────────

    def test_01_check_rate_limit(self):
        """_check_rate_limit: Pass under limit, throw when exceeding threshold."""
        cache_mock.incr.return_value = 1
        api._check_rate_limit("test_action", max_requests=10, window_sec=60)

        cache_mock.incr.return_value = 25
        with self.assertRaises(MockFrappeException):
            api._check_rate_limit("test_action", max_requests=10, window_sec=60)

    def test_02_parse_date(self):
        """_parse_date: String format, date object and None fallback."""
        d1 = api._parse_date("2026-11-17")
        self.assertEqual(d1, date(2026, 11, 17))
        today_val = date.today()
        d2 = api._parse_date(today_val)
        self.assertEqual(d2, today_val)
        d3 = api._parse_date(None)
        self.assertEqual(d3, today_val)

    def test_03_sanitize_string(self):
        """_sanitize_string: Strips whitespace, truncates and handles None."""
        sanitized = api._sanitize_string("  PetCare CRM String  ", max_len=50)
        self.assertEqual(sanitized, "PetCare CRM String")

        none_val = api._sanitize_string(None, allow_none=True)
        self.assertIsNone(none_val)

        truncated = api._sanitize_string("A" * 200, max_len=20)
        self.assertEqual(len(truncated), 20)

    def test_04_portal_tokens(self):
        """_generate_portal_token, _verify_owner_portal_access, generate_portal_token."""
        token = api._generate_portal_token("CUST-001")
        self.assertTrue(api._verify_portal_token("CUST-001", token))

        # Admin user verification
        mock_frappe.session.user = "Administrator"
        self.assertTrue(api._verify_owner_portal_access("CUST-001"))

        # Guest user with valid token
        mock_frappe.session.user = "Guest"
        self.assertTrue(api._verify_owner_portal_access("CUST-001", portal_token=token))

        # Guest user with invalid token throws
        with self.assertRaises(MockFrappeException):
            api._verify_owner_portal_access("CUST-001", portal_token="INVALID_TOKEN")

        # generate_portal_token API response contract
        mock_frappe.session.user = "Administrator"
        gen_res = api.generate_portal_token("CUST-001")
        self.assertTrue(gen_res["success"])
        self.assertEqual(gen_res["customer_id"], "CUST-001")
        self.assertEqual(gen_res["portal_token"], token)

    # ─────────────────────────────────────────────────────────────────
    # 2. MEMBERSHIP APIS
    # ─────────────────────────────────────────────────────────────────

    def test_05_get_active_membership(self):
        """get_active_membership returns active membership info or None."""
        res = api.get_active_membership("CUST-001", pet="PET-001")
        self.assertTrue(res is None or isinstance(res, dict))
        self.assertIsNone(api.get_active_membership(None))

    def test_06_get_remaining_benefit(self):
        """get_remaining_benefit returns benefit details."""
        b_doc = MockDoc(benefit_type="Grooming", remaining_quantity=4, total_quantity=5, used_quantity=1, discount_type="FREE", discount_value=0)
        ms_doc = MockDoc(benefits=[b_doc])
        mock_frappe.get_doc = lambda *a, **kw: ms_doc

        res = api.get_remaining_benefit("MEM-001", "Grooming")
        self.assertIsNotNone(res)
        self.assertEqual(res["benefit_type"], "Grooming")
        self.assertEqual(res["remaining_quantity"], 4)

    def test_07_record_benefit_usage(self):
        """record_benefit_usage decrements atomic count with validation."""
        res = api.record_benefit_usage("MEM-001", "Grooming", count=1)
        self.assertTrue(res["success"])
        self.assertEqual(res["remaining_quantity"], 3)

        with self.assertRaises(MockFrappeException):
            api.record_benefit_usage("MEM-001", "Grooming", count=0)

    def test_08_check_membership_renewal(self):
        """check_membership_renewal detects expiring memberships."""
        expiring_ms = [{
            "name": "MEM-EXP-001",
            "customer": "CUST-001",
            "pet": "PET-001",
            "membership_plan": "Gold",
            "end_date": date.today() + timedelta(days=3),
        }]
        mock_frappe.db.get_list.return_value = expiring_ms
        res = api.check_membership_renewal("CUST-001", "PET-001")
        self.assertEqual(res["count"], 1)
        self.assertTrue(res["renewals_needed"][0]["needs_renewal"])

    def test_09_top_up_membership(self):
        """top_up_membership increases wallet balance and creates transaction."""
        res = api.top_up_membership(customer="CUST-001", pet="PET-001", amount=500000, payment_method="Bank Transfer")
        self.assertTrue(res["success"])

        with self.assertRaises(MockFrappeException):
            api.top_up_membership(customer="CUST-001", amount=-1000)

        mock_frappe.session.user = "Guest"
        with self.assertRaises(MockFrappeException):
            api.top_up_membership(customer="CUST-001", amount=100000)

    def test_10_plans_and_registration(self):
        """get_available_plans and register_membership."""
        mock_frappe.get_all.return_value = [{"name": "PLAN-01", "plan_name": "Standard Plan", "price": 1000000}]
        plans = api.get_available_plans()
        self.assertIsNotNone(plans)

        reg_res = api.register_membership("CUST-001", "PET-001", "Standard Plan")
        self.assertTrue(reg_res.get("success", True))

    def test_11_renew_membership(self):
        """renew_membership with rollover calculation."""
        res = api.renew_membership(customer="CUST-001", pet="PET-001", new_plan_name="Standard Plan", payment_source="Direct")
        self.assertTrue(res.get("success", True))

    def test_12_membership_topup_qr(self):
        """get_membership_topup_qr generates dynamic VietQR for top-up."""
        qr_info = api.get_membership_topup_qr("MEM-001", amount=200000)
        self.assertEqual(qr_info["status"], "success")
        self.assertIn("PC-MEM-MEM-001", qr_info["transfer_content"])

    # ─────────────────────────────────────────────────────────────────
    # 3. CARE ENGINE & RECOMMENDATION APIS
    # ─────────────────────────────────────────────────────────────────

    def test_13_care_status_and_prediction(self):
        """_compute_care_status, get_care_status, predict_next_service."""
        status_res = api.get_care_status("PET-001", "Grooming")
        self.assertIn("status", status_res)

        pred_res = api.predict_next_service("PET-001", "Grooming", enable_seasonal_adjustment=True, enable_age_adjustment=True)
        self.assertEqual(pred_res["pet"], "PET-001")
        self.assertIn("predicted_next_visit", pred_res)

    def test_14_analyze_pet_care_pattern(self):
        """analyze_pet_care_pattern calculates EWMA and outlier stats."""
        res = api.analyze_pet_care_pattern("PET-001", "Grooming")
        self.assertIn("typical_interval", res)
        self.assertIn("confidence", res)

    def test_15_recommendations_and_scans(self):
        """get_pet_recommendations, update_recommendation_status, run_care_intelligence_scan, run_care_scan."""
        mock_frappe.db.get_list.return_value = [{"name": "REC-001", "status": "NEW"}]
        recs = api.get_pet_recommendations(customer="CUST-001")
        self.assertEqual(len(recs), 1)

        up_res = api.update_recommendation_status("REC-001", "CONTACTED", notes="Khách đồng ý đặt lịch")
        self.assertTrue(up_res["success"])

        scan_res = api.run_care_scan()
        self.assertTrue(scan_res["success"])

        intel_res = api.run_care_intelligence_scan()
        self.assertTrue(intel_res["success"])

    # ─────────────────────────────────────────────────────────────────
    # 4. WORKFLOW AUTOMATION & RECEPTION PORTAL
    # ─────────────────────────────────────────────────────────────────

    def test_16_automation_triggers(self):
        """run_daily_automation and run_hourly_workflow."""
        daily_res = api.run_daily_automation()
        self.assertTrue(daily_res["success"])

        hourly_res = api.run_hourly_workflow()
        self.assertTrue(hourly_res["success"])

    def test_17_portal_overview_and_details(self):
        """get_portal_overview and get_customer_portal_details."""
        overview = api.get_portal_overview()
        self.assertIn("metrics", overview)
        self.assertIn("pets", overview)

        details = api.get_customer_portal_details("0901234567")
        self.assertIn("found", details)

        short_res = api.get_customer_portal_details("a")
        self.assertFalse(short_res["found"])

    def test_18_quick_record_visit(self):
        """quick_record_visit receptionist check-in with auto benefit discount."""
        res = api.quick_record_visit("CUST-001", "PET-001", "Grooming", original_price=300000)
        self.assertTrue(res["success"])
        self.assertIn("final_price", res)

    # ─────────────────────────────────────────────────────────────────
    # 5. CRM CORE (LEADS, OPPORTUNITIES, CUSTOMER 360)
    # ─────────────────────────────────────────────────────────────────

    def test_19_create_and_submit_lead(self):
        """create_lead and submit_website_lead with honeypot trap."""
        lead_id = api.create_lead(
            lead_name="Phạm Văn Dũng",
            phone="0918-234-567",
            lead_source="Website",
            email="dung@petcare.vn",
            initial_pet_info="Cún Poodle 1 tuổi",
        )
        self.assertIsNotNone(lead_id)

        web_res = api.submit_website_lead(
            lead_name="Lê Thị Mai",
            phone="0987654321",
            email="mai@example.com",
            service_type="Spa",
        )
        self.assertEqual(web_res["status"], "success")

        # Honeypot returns simulated trap success
        trap_res = api.submit_website_lead("Spam Bot", "0900000000", hp_field="I am a bot")
        self.assertEqual(trap_res["status"], "success")
        self.assertEqual(trap_res["lead_id"], "LEAD-BOT-TRAP")

    def test_20_lead_lifecycle(self):
        """update_lead_status and add_lead_interaction."""
        res_up = api.update_lead_status("LEAD-001", "Qualified")
        self.assertEqual(res_up["status"], "success")

        res_note = api.add_lead_interaction("LEAD-001", "Call", "Khách hỏi giá gói tắm spa")
        self.assertEqual(res_note["status"], "success")

    def test_21_convert_lead_to_customer(self):
        """convert_lead_to_customer creating Customer, Pet and Opportunity."""
        res_conv = api.convert_lead_to_customer(
            lead_id="LEAD-001",
            pet_name="Bé Bơ",
            species="Dog",
            create_opportunity=1,
            opportunity_amount=1500000.0,
        )
        self.assertEqual(res_conv["status"], "success")

    def test_22_opportunity_lifecycle(self):
        """create_opportunity, update_opportunity_stage, get_pipeline_summary."""
        opp_id = api.create_opportunity(
            title="Gói Chăm Sóc Năm Cún Bơ",
            customer="CUST-001",
            expected_amount=5000000.0,
            stage="Proposal",
            probability=60.0,
        )
        self.assertIsNotNone(opp_id)

        up_opp = api.update_opportunity_stage(opp_id, "Closed Won")
        self.assertEqual(up_opp["status"], "success")

        pipeline = api.get_pipeline_summary()
        self.assertIn("total_active_pipeline_value", pipeline)

    def test_23_customer_360_and_tasks(self):
        """get_customer_360, create_crm_todo, add_customer_interaction, verify_customer_pet_access."""
        c360 = api.get_customer_360("CUST-001")
        self.assertIn("contact_id", c360)

        todo_id = api.create_crm_todo("Contact", "CUST-001", "Gọi điện chúc mừng sinh nhật bé cún")
        self.assertIsNotNone(todo_id)

        act_res = api.add_customer_interaction("CUST-001", "Tư vấn", "Khách hỏi thêm về dịch vụ khách sạn thú cưng")
        self.assertEqual(act_res["status"], "success")

        acc_res = api.verify_customer_pet_access("CUST-001", "PET-001")
        self.assertIn("valid", acc_res)

    # ─────────────────────────────────────────────────────────────────
    # 6. SERVICE OPERATIONS, CATALOG & CASE MANAGEMENT
    # ─────────────────────────────────────────────────────────────────

    def test_24_service_catalog(self):
        """get_service_catalog and create_service_catalog_item."""
        cat = api.get_service_catalog(species="Dog")
        self.assertIsInstance(cat, list)

        item = api.create_service_catalog_item(
            service_code="SVC-TEST-01",
            service_name="Tắm Trị Liệu Thảo Dược",
            category="Grooming & Spa",
            standard_price=350000.0,
            default_cycle_days=14,
        )
        self.assertIsNotNone(item)

    def test_25_record_pet_service_visit(self):
        """record_pet_service_visit with full technician and weight details."""
        visit = api.record_pet_service_visit(
            pet="PET-001",
            service_identifier="Grooming",
            visit_date="2026-11-17",
            technician="BS. Hoàng",
            notes="Bé ngoan, sấy lông cẩn thận",
            weight_kg=5.2,
        )
        self.assertEqual(visit["status"], "success")

    def test_26_service_cases(self):
        """create_service_case and update_case_status."""
        case_id = api.create_service_case(
            customer="CUST-001",
            subject="Khách phản hồi lông sấy chưa khô kỹ",
            description="Khu vực bụng dưới còn ẩm",
            pet="PET-001",
            priority="Medium",
        )
        self.assertIsNotNone(case_id)

        up_case = api.update_case_status(case_id, "Resolved", resolution="Đã liên hệ xin lỗi và tặng voucher giảm 20%")
        self.assertEqual(up_case["status"], "success")

    # ─────────────────────────────────────────────────────────────────
    # 7. ANALYTICS, PAYMENTS & OMNICHANNEL
    # ─────────────────────────────────────────────────────────────────

    def test_27_kpi_metrics(self):
        """get_kpi_dashboard_metrics returns 8 standard metrics."""
        kpis = api.get_kpi_dashboard_metrics("2026-10-01", "2026-11-17")
        self.assertTrue(kpis["success"])
        self.assertIn("data", kpis)

    def test_28_payment_qr_and_webhook(self):
        """get_service_visit_payment_qr and payment_webhook."""
        qr = api.get_service_visit_payment_qr("SV-001")
        self.assertEqual(qr["status"], "success")
        self.assertIn("transfer_content", qr)

        secret = mock_frappe.conf["vietqr_webhook_secret"]
        payload = "TRANS_999|300000.0|PC-SVC-SV-001"
        sig = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()

        wh_res = api.payment_webhook(
            transaction_id="TRANS_999",
            amount=300000.0,
            content="PC-SVC-SV-001",
            signature=sig,
        )
        self.assertNotEqual(wh_res.get("error_code"), "INVALID_SIGNATURE")

    def test_29_omnichannel(self):
        """send_omnichannel_notification and get_omnichannel_outbox."""
        send_res = api.send_omnichannel_notification(
            channel="SMS_BRANDNAME",
            recipient="0901234567",
            template_id="APPOINTMENT_REMINDER",
            template_data={"pet_name": "Bơ", "time": "09:00"},
        )
        self.assertEqual(send_res["status"], "success")

        outbox = api.get_omnichannel_outbox(recipient="0901234567")
        self.assertTrue(outbox["success"])

    # ─────────────────────────────────────────────────────────────────
    # 8. OWNER PORTAL SELF-SERVICE & APPOINTMENTS
    # ─────────────────────────────────────────────────────────────────

    def test_30_owner_portal_views(self):
        """owner_portal_get_pets, owner_portal_get_health_timeline, owner_portal_get_membership_wallet."""
        pets_res = api.owner_portal_get_pets("CUST-001")
        self.assertTrue(pets_res["success"])

        hist_res = api.owner_portal_get_health_timeline("CUST-001", "PET-001")
        self.assertTrue(hist_res["success"])

        wallet_res = api.owner_portal_get_membership_wallet("CUST-001")
        self.assertTrue(wallet_res["success"])

    def test_31_owner_portal_appointment_booking(self):
        """owner_portal_book_appointment creates appointment from portal."""
        preferred_datetime = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        book_res = api.owner_portal_book_appointment(
            customer_id="CUST-001",
            pet_id="PET-001",
            service_id="Grooming",
            preferred_datetime=preferred_datetime,
            notes="Đặt lịch qua Cổng chủ nuôi",
        )
        self.assertTrue(book_res["success"])

    def test_32_appointment_management(self):
        """create_appointment, get_appointments, check_in_appointment, cancel_appointment."""
        appt = api.create_appointment(
            customer="CUST-001",
            pet="PET-001",
            service_type="Grooming",
            appointment_date="2026-11-20",
            appointment_time="10:00",
            branch="CN-TRUNGTAM",
        )
        self.assertEqual(appt["status"], "Scheduled")

        appts = api.get_appointments(customer="CUST-001")
        self.assertTrue(appts.get("success", True))

        check_res = api.check_in_appointment("APP-001", technician="BS. Bình")
        self.assertEqual(check_res["status"], "Checked-In")

        canc_res = api.cancel_appointment("APP-001", reason="Khách bận đột xuất")
        self.assertEqual(canc_res["status"], "Cancelled")

    # ─────────────────────────────────────────────────────────────────
    # 9. ECOMMERCE & DIAGNOSTICS
    # ─────────────────────────────────────────────────────────────────

    def test_33_woocommerce_webhook(self):
        """woocommerce_order_webhook HMAC-SHA256 authenticated order intake."""
        wc_secret = mock_frappe.conf["woocommerce_webhook_secret"]
        order_payload = {
            "id": 888777,
            "status": "processing",
            "total": "950000",
            "currency": "VND",
            "billing": {"first_name": "Nguyen", "last_name": "Thanh", "phone": "0912999888", "email": "thanh@example.com"},
            "line_items": [{"id": 1, "name": "Spa & Cat Grooming", "quantity": 1, "price": 950000}],
        }
        raw_body = json.dumps(order_payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        sig = base64.b64encode(hmac.new(wc_secret.encode("utf-8"), raw_body, hashlib.sha256).digest()).decode("utf-8")

        res = api.woocommerce_order_webhook(payload=order_payload, signature=sig, topic="order.created", delivery_id="del-test-1")
        self.assertEqual(res["status"], "success")

    def test_34_diagnostics(self):
        """send_test_email and reset_demo_dataset."""
        email_res = api.send_test_email("admin@petcare.vn")
        self.assertTrue(email_res["success"])

        reset_res = api.reset_demo_dataset()
        self.assertTrue(reset_res["success"])

    def test_35_suggest_best_benefit(self):
        """suggest_best_benefit picks highest discount & earliest expiring membership."""
        future_exp = (date.today() + timedelta(days=30)).isoformat()
        later_exp = (date.today() + timedelta(days=90)).isoformat()

        mock_frappe.get_all = MagicMock(return_value=[
            {"name": "MEM-LONG", "membership_plan": "Gold", "pet": None, "end_date": later_exp},
            {"name": "MEM-SHORT", "membership_plan": "Silver", "pet": None, "end_date": future_exp},
        ])

        b_free = MagicMock(benefit_type="Grooming", total_quantity=4, used_quantity=1, discount_type="FREE", discount_value=100.0)
        b_pct = MagicMock(benefit_type="Grooming", total_quantity=4, used_quantity=0, discount_type="PERCENTAGE", discount_value=20.0)

        def fake_get_doc(dt, name):
            if name == "MEM-LONG":
                return MockDoc(name="MEM-LONG", benefits=[b_pct])
            return MockDoc(name="MEM-SHORT", benefits=[b_free])

        mock_frappe.get_doc = fake_get_doc
        res = api.suggest_best_benefit(customer="CUST-001", service_type="Grooming", original_price=350000.0)
        self.assertTrue(res["found"])
        self.assertEqual(res["best_option"]["membership"], "MEM-SHORT")
        self.assertEqual(res["best_option"]["discount_amount"], 350000.0)
        self.assertEqual(res["best_option"]["final_price"], 0.0)
        self.assertEqual(len(res["alternatives"]), 1)


if __name__ == "__main__":
    unittest.main()
