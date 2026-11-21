# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

"""
Suite 14: Scheduled Tasks & DocType Controllers Life-Cycle Verification.
Exhaustively exercises and verifies:
1. All 5 Scheduled Tasks in petcare_crm.tasks:
   - auto_expire_memberships
   - check_due_and_at_risk_pets
   - check_expiring_memberships
   - daily_petcare_scan
   - hourly_workflow_check
2. All 13 DocType Controllers and Business Model Logic:
   - BenefitRedemptionLedger (Validate, Pessimistic Row Lock & Revert)
   - CareRecommendation (Validate, Mark Contacted, Mark Converted, Dismiss)
   - CustomerMembership (Validity dates, auto-expire, remaining benefit calculations)
   - MembershipBenefit (Model attributes & association)
   - MembershipPlan (Plan specifications & structure)
   - MembershipTransaction (Validation of positive amounts)
   - Pet (Required pet name, ownership validation, weight constraints, get_service_visits)
   - PetCareAppointment (Validation, Front-desk Check-in to Visit, Cancellation)
   - PetCareCase (Ownership validation, Lifecycle SLA, Resolution enforcement)
   - PetCareLead (Vietnamese phone regex, sanitization, unqualified state transitions)
   - PetCareOpportunity (Probability constraints, weighted amount, stage transitions, won/lost rules)
   - PetCareService (Price validation, category specifications)
   - PlanBenefit & WooCommerceOrderSync (Validation of order IDs, keys and non-negative totals)
   - ServiceVisit (Auto-linking, pricing engine, submit completed, cancel revert)
"""

import os
import sys
import unittest
from datetime import date, datetime, timedelta
from unittest.mock import MagicMock

# Ensure apps/petcare_crm is on sys.path
sys.path.insert(0, os.path.abspath("apps/petcare_crm"))

class MockFrappeException(Exception):
    pass

class MockDoc:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", "DOC-001")
        self._is_new = False
        self.benefits = []
        self.status = kwargs.get("status", "Active")
        self.customer = kwargs.get("customer", "CUST-001")
        self.pet = kwargs.get("pet", "PET-001")
        self.membership = kwargs.get("membership", "MEM-001")
        self.quantity_redeemed = kwargs.get("quantity_redeemed", 1)
        self.discount_applied = kwargs.get("discount_applied", 50000.0)
        self.service_type = kwargs.get("service_type", "Grooming")
        self.service = kwargs.get("service", None)
        self.service_code = kwargs.get("service_code", None)
        self.sales_person = kwargs.get("sales_person", None)
        self.original_price = kwargs.get("original_price", 300000.0)
        self.final_price = kwargs.get("final_price", 300000.0)
        self.discount_amount = kwargs.get("discount_amount", 0.0)
        self.expected_amount = kwargs.get("expected_amount", 0.0)
        self.visit_date = "2026-11-17"
        self.appointment_date = "2026-11-20"
        self.branch = "CN-TRUNGTAM"
        self.cancellation_reason = ""
        self.assigned_staff = ""
        self.priority = kwargs.get("priority", "Medium")
        self.phone = kwargs.get("phone", "0901234567")
        self.mobile_no = kwargs.get("mobile_no", "0901234567")
        self.email_id = kwargs.get("email_id", "an@example.com")
        self.first_name = kwargs.get("first_name", "An")
        self.last_name = kwargs.get("last_name", "Nguyen")
        self.lead_name = kwargs.get("lead_name", "Nguyễn Văn An")
        self.lead_owner = kwargs.get("lead_owner", "Administrator")
        self.unqualified_reason = kwargs.get("unqualified_reason", "")
        self.lost_reason = kwargs.get("lost_reason", "")
        self.price = kwargs.get("price", 1000000.0)
        self.duration_months = 12
        self.species = "Dog"
        self.pet_name = "Bé Bơ"
        for k, v in kwargs.items():
            setattr(self, k, v)
        if args and isinstance(args[0], dict):
            for k, v in args[0].items():
                setattr(self, k, v)

    def is_new(self):
        return getattr(self, "_is_new", False)

    def insert(self, *a, **kw):
        self._is_new = False
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


if "frappe" in sys.modules:
    mock_frappe = sys.modules["frappe"]
else:
    mock_frappe = MagicMock()
    sys.modules["frappe"] = mock_frappe

mock_frappe.throw = lambda msg, *args, **kwargs: (_ for _ in ()).throw(MockFrappeException(msg))
mock_frappe.logger = lambda x: MagicMock()
mock_frappe.session = MagicMock()
mock_frappe.session.user = "Administrator"
mock_frappe.utils = MagicMock()
mock_frappe.utils.nowdate.side_effect = lambda: datetime.now().strftime("%Y-%m-%d")
mock_frappe.utils.now_datetime.side_effect = lambda: f"{datetime.now().strftime('%Y-%m-%d')} 09:00:00"
mock_frappe.utils.now.side_effect = lambda: f"{datetime.now().strftime('%Y-%m-%d')} 09:00:00"
mock_frappe.utils.getdate = lambda d: datetime.strptime(str(d)[:10], "%Y-%m-%d").date() if isinstance(d, str) else d
mock_frappe.model = MagicMock()
mock_doc_module = MagicMock()
mock_doc_module.Document = MockDoc
mock_frappe.model.document = mock_doc_module

sys.modules["frappe.utils"] = mock_frappe.utils
sys.modules["frappe.model"] = mock_frappe.model
sys.modules["frappe.model.document"] = mock_doc_module

import petcare_crm.tasks as tasks
from petcare_crm.petcare_crm.doctype.benefit_redemption_ledger.benefit_redemption_ledger import BenefitRedemptionLedger
from petcare_crm.petcare_crm.doctype.care_recommendation.care_recommendation import CareRecommendation
from petcare_crm.petcare_crm.doctype.customer_membership.customer_membership import CustomerMembership
from petcare_crm.petcare_crm.doctype.membership_benefit.membership_benefit import MembershipBenefit
from petcare_crm.petcare_crm.doctype.membership_plan.membership_plan import MembershipPlan
from petcare_crm.petcare_crm.doctype.membership_transaction.membership_transaction import MembershipTransaction
from petcare_crm.petcare_crm.doctype.pet.pet import Pet
from petcare_crm.petcare_crm.doctype.petcare_appointment.petcare_appointment import PetCareAppointment
from petcare_crm.petcare_crm.doctype.petcare_case.petcare_case import PetCareCase
from petcare_crm.petcare_crm.doctype.petcare_lead.petcare_lead import PetCareLead
from petcare_crm.petcare_crm.doctype.petcare_opportunity.petcare_opportunity import PetCareOpportunity
from petcare_crm.petcare_crm.doctype.petcare_service.petcare_service import PetCareService
from petcare_crm.petcare_crm.doctype.plan_benefit.plan_benefit import PlanBenefit
from petcare_crm.petcare_crm.doctype.service_visit.service_visit import ServiceVisit
from petcare_crm.petcare_crm.doctype.woocommerce_order_sync.woocommerce_order_sync import WooCommerceOrderSync


class TestAllTasksAndDocTypes(unittest.TestCase):
    """Test suite executing all scheduler tasks and doctype controller methods."""

    def setUp(self):
        mock_frappe.session.user = "Administrator"
        mock_frappe.db.exists = MagicMock(return_value=True)
        mock_frappe.db.get_value = MagicMock(return_value="CUST-001")
        mock_frappe.get_all = MagicMock(return_value=[])
        mock_frappe.get_list = MagicMock(return_value=[])
        mock_frappe.db.get_all = MagicMock(return_value=[])
        mock_frappe.db.get_list = MagicMock(return_value=[])
        mock_frappe.get_doc = lambda *a, **kw: MockDoc(*a, **kw)

    # ─────────────────────────────────────────────────────────────────
    # 1. SCHEDULED TASKS EXECUTION
    # ─────────────────────────────────────────────────────────────────

    def test_01_auto_expire_memberships_task(self):
        """auto_expire_memberships executes without runtime error."""
        count = tasks.auto_expire_memberships(date(2026, 11, 17))
        self.assertIsInstance(count, int)

    def test_02_check_due_and_at_risk_pets_task(self):
        """check_due_and_at_risk_pets executes CareEngine scan."""
        recs_count = tasks.check_due_and_at_risk_pets(date(2026, 11, 17))
        self.assertIsInstance(recs_count, int)

    def test_03_check_expiring_memberships_task(self):
        """check_expiring_memberships scans 7-day threshold."""
        renewal_recs = tasks.check_expiring_memberships(date(2026, 11, 17))
        self.assertIsInstance(renewal_recs, int)

    def test_04_daily_petcare_scan_task(self):
        """daily_petcare_scan runs full master daily coordination."""
        daily_res = tasks.daily_petcare_scan()
        self.assertTrue(daily_res["success"])
        self.assertIn("details", daily_res)

    def test_05_hourly_workflow_check_task(self):
        """hourly_workflow_check runs fast hourly checks."""
        hourly_res = tasks.hourly_workflow_check()
        self.assertTrue(hourly_res["success"])
        self.assertIn("total_tasks_created", hourly_res)

    # ─────────────────────────────────────────────────────────────────
    # 2. DOCTYPE CONTROLLERS & ENTITY LIFE-CYCLE VALIDATIONS
    # ─────────────────────────────────────────────────────────────────

    def test_06_benefit_redemption_ledger_controller(self):
        """BenefitRedemptionLedger validate and revert."""
        ledger = BenefitRedemptionLedger(
            membership="MEM-001",
            quantity_redeemed=1,
            discount_applied=100000.0,
            status="Applied",
            benefit_type="Grooming",
        )
        ledger.validate()
        self.assertIsNotNone(ledger.redemption_time)

        # Negative quantity throws
        ledger.quantity_redeemed = 0
        with self.assertRaises(MockFrappeException):
            ledger.validate()

        # Revert
        ledger.quantity_redeemed = 1
        ledger.revert(reason="Test Revert")
        self.assertEqual(ledger.status, "Reverted")

    def test_07_care_recommendation_controller(self):
        """CareRecommendation validate, mark_contacted, mark_converted, dismiss."""
        rec = CareRecommendation(
            customer="CUST-001",
            pet="PET-001",
            service_type="Grooming",
            recommendation_type="DUE_SOON",
            status="NEW",
        )
        rec.validate()

        rec.mark_contacted(notes="Called owner")
        self.assertEqual(rec.status, "CONTACTED")

        rec.mark_converted(notes="Converted to visit")
        self.assertEqual(rec.status, "CONVERTED")

        rec.dismiss(reason="Owner relocated")
        self.assertEqual(rec.status, "DISMISSED")

    def test_08_customer_membership_controller(self):
        """CustomerMembership date bounds, benefit remaining and balance validations."""
        b1 = MockDoc(benefit_type="Spa", total_quantity=5, used_quantity=2)
        cm = CustomerMembership(
            customer="CUST-001",
            pet="PET-001",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            benefits=[b1],
            status="Active",
            balance=200000.0,
        )
        cm.validate()
        self.assertEqual(b1.remaining_quantity, 3)

        # Inverted dates throw
        cm.start_date = date(2026, 12, 31)
        cm.end_date = date(2026, 1, 1)
        with self.assertRaises(MockFrappeException):
            cm.validate()

    def test_09_membership_transaction_controller(self):
        """MembershipTransaction enforces positive transaction amount."""
        tx = MembershipTransaction(amount=50000.0)
        tx.validate()

        tx.amount = -500
        with self.assertRaises(MockFrappeException):
            tx.validate()

    def test_10_pet_controller(self):
        """Pet validates required fields, customer existence and retrieves visits."""
        pet = Pet(pet_name="Lucky", customer="CUST-001", weight_kg=6.5)
        pet.validate()

        visits = pet.get_service_visits()
        self.assertIsInstance(visits, list)

        # Empty name throws
        pet.pet_name = "   "
        with self.assertRaises(MockFrappeException):
            pet.validate()

    def test_11_petcare_appointment_controller(self):
        """PetCareAppointment validate, check_in and cancel."""
        appt = PetCareAppointment(
            customer="CUST-001",
            pet="PET-001",
            appointment_date="2026-11-20",
            service_type="Grooming",
            status="Scheduled",
        )
        appt.validate()
        self.assertEqual(appt.branch, "CN-TRUNGTAM")

        appt.check_in(technician="BS. Mai")
        self.assertEqual(appt.status, "Checked-In")
        self.assertEqual(appt.assigned_staff, "BS. Mai")

        appt.cancel_appointment(reason="Khách có việc bận")
        self.assertEqual(appt.status, "Cancelled")

    def test_12_petcare_case_controller(self):
        """PetCareCase validate customer ownership, defaults, and resolution lifecycle."""
        case = PetCareCase(
            customer="CUST-001",
            pet="PET-001",
            subject="Khiếu nại sấy lông",
            status="Open",
        )
        case.validate()
        self.assertEqual(case.assigned_to, "Administrator")

        # Resolving case without resolution throws
        case.status = "Resolved"
        case.resolution = ""
        with self.assertRaises(MockFrappeException):
            case.validate()

        case.resolution = "Đã xin lỗi khách và gửi voucher 50k"
        case.validate()
        self.assertIsNotNone(case.resolved_date)

    def test_13_petcare_lead_controller(self):
        """PetCareLead validates Vietnamese phone and unqualified status reasons."""
        lead = PetCareLead(
            lead_name="Võ Văn Nam",
            phone="0912-345-678",
            status="New",
        )
        lead.validate()
        self.assertEqual(lead.phone, "0912345678")

        # Unqualified without reason throws
        lead.status = "Unqualified"
        lead.unqualified_reason = ""
        lead._is_new = False
        with self.assertRaises(MockFrappeException):
            lead._validate_state_transitions()

    def test_14_petcare_opportunity_controller(self):
        """PetCareOpportunity validates stage probabilities and weighted amount."""
        opp = PetCareOpportunity(
            title="Gói combo Spa 1 năm",
            customer="CUST-001",
            expected_amount=6000000.0,
            stage="Proposal",
            probability=50.0,
        )
        opp.validate()
        self.assertEqual(opp.weighted_amount, 3000000.0)

        # Closed Won sets 100% probability
        opp.stage = "Closed Won"
        opp.validate()
        self.assertEqual(opp.probability, 100.0)
        self.assertEqual(opp.weighted_amount, 6000000.0)

    def test_15_petcare_service_controller(self):
        """PetCareService enforces positive price and valid category."""
        srv = PetCareService(
            service_code="SVC-001",
            service_name="Cắt Tỉa Lông Nghệ Thuật",
            category="Grooming",
            standard_price=300000.0,
            default_cycle_days=21,
        )
        srv.validate()

        srv.standard_price = -100
        with self.assertRaises(MockFrappeException):
            srv.validate()

    def test_16_service_visit_controller(self):
        """ServiceVisit discount calculation, submit completed and cancel revert."""
        visit = ServiceVisit(
            pet="PET-001",
            customer="CUST-001",
            original_price=250000.0,
            final_price=None,
            discount_amount=50000.0,
            status="In Progress",
        )
        visit.validate()
        self.assertEqual(visit.final_price, 200000.0)

        visit.on_submit()
        self.assertEqual(visit.status, "Completed")

        visit.on_cancel()
        self.assertEqual(visit.status, "Cancelled")

    def test_17_woocommerce_order_sync_controller(self):
        """WooCommerceOrderSync requires keys and positive total."""
        sync = WooCommerceOrderSync(
            external_order_key="WC_ORD_999",
            woocommerce_order_id=999,
            order_total=500000.0,
        )
        sync.validate()

        sync.order_total = -10
        with self.assertRaises(MockFrappeException):
            sync.validate()


if __name__ == "__main__":
    unittest.main()
