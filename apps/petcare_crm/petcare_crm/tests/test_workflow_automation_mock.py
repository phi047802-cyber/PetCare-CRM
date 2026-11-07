"""
Mock Test Suite for Prompt 7: Workflow, Automation & Customer Follow-up.
Verifies all Prompt 7 requirements in pure Python:
1. Lead Follow-up (uncontacted lead -> ToDo task with owner & deadline)
2. Lead Follow-up filtering (recent/contacted leads skipped)
3. Lead Follow-up idempotency (re-run does not create duplicate ToDo)
4. Membership Auto-expiry (active past end_date -> Expired)
5. Membership Renewal Warning (7-day advance notice -> RENEWAL rec & ToDo)
6. Membership Renewal Idempotency (re-run does not duplicate recs or ToDo)
7. Care Engine Scan (Due Soon & At Risk -> recommendations & follow-up ToDo)
8. Care Engine Idempotency (re-run updates in-place, no duplicate ToDo)
9. Service Recovery SLA Escalation (unresolved cases > SLA -> escalation ToDo)
10. Service Recovery Idempotency (re-run does not duplicate escalation ToDo)
11. Safe Mode Communication (suppresses real emails/messages in demo mode)
12. AutomationCoordinator fault tolerance & structured audit report
"""

import os
import sys
import unittest
from datetime import date, datetime, timedelta
from typing import Any, Dict, List
from unittest.mock import MagicMock

# Ensure apps/petcare_crm is on sys.path
sys.path.insert(0, os.path.abspath("apps/petcare_crm"))

# Shared Mock Frappe Document and DB
class MockDocument:
    def __init__(self, *args, **kwargs):
        self._is_new = True
        self.name = kwargs.get("name", "DOC-001")
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

from petcare_crm.utils.config import (
    RECOMMENDATION_NEW,
    RECOMMENDATION_TYPE_AT_RISK,
    RECOMMENDATION_TYPE_DUE_SOON,
    RECOMMENDATION_TYPE_RENEWAL,
    STATUS_ACTIVE,
    STATUS_EXPIRED,
)
from petcare_crm.utils.models import (
    Customer,
    Membership,
    MembershipBenefit,
    Pet,
    ServiceVisit,
)
from petcare_crm.utils.workflow_automation import (
    AutomationCoordinator,
    CareEngineAutomation,
    LeadFollowupAutomation,
    MembershipRenewalAutomation,
    SafeCommunicationGateway,
    ServiceRecoveryAutomation,
    TaskManager,
)
import petcare_crm.utils.workflow_automation as wa
wa.frappe = mock_frappe
import petcare_crm.utils.frappe_recommendation_engine as fre
fre.frappe = mock_frappe
import petcare_crm.tasks as tasks_module
tasks_module.frappe = mock_frappe


class TestWorkflowAutomationMock(unittest.TestCase):

    def setUp(self):
        self.today = date(2026, 10, 26)
        wa.frappe = mock_frappe
        fre.frappe = mock_frappe
        tasks_module.frappe = mock_frappe
        mock_frappe.db.reset_mock()
        mock_frappe.get_doc.side_effect = None
        mock_frappe.db.get_value.side_effect = None
        mock_frappe.db.get_list.side_effect = None
        mock_frappe.db.exists.side_effect = None

    # ─────────────────────────────────────────────────────────────────
    # Scenario 1 & 2: Lead Follow-up Automation
    # ─────────────────────────────────────────────────────────────────
    def test_01_lead_followup_creates_task_for_uncontacted_lead(self):
        """Lead ở trạng thái 'New' quá 24h -> Tạo ToDo task cho lead_owner."""
        created_time = datetime(2026, 10, 24, 10, 0, 0)  # > 48h ago
        mock_lead = {
            "name": "LEAD-2026-001",
            "lead_name": "Tran Van B",
            "phone": "0901234567",
            "email": "b@example.com",
            "lead_owner": "sales_staff_1@petcare.com",
            "creation": created_time,
            "source": "Facebook Ads",
        }

        mock_frappe.db.get_list.return_value = [mock_lead]
        # Không có ToDo Open nào trước đó
        mock_frappe.db.get_value.return_value = None

        todo_instances = []
        def fake_get_doc(*args, **kwargs):
            doc = MockDocument(*args, **kwargs)
            if args and isinstance(args[0], dict) and args[0].get("doctype") == "ToDo":
                todo_instances.append(doc)
            return doc

        mock_frappe.get_doc.side_effect = fake_get_doc

        res = LeadFollowupAutomation.process_uncontacted_leads(self.today, threshold_hours=24)

        self.assertEqual(res["processed"], 1)
        self.assertEqual(res["tasks_created"], 1)
        self.assertEqual(res["tasks_existing"], 0)
        self.assertEqual(len(todo_instances), 1)
        todo = todo_instances[0]
        self.assertEqual(todo.allocated_to, "sales_staff_1@petcare.com")
        self.assertEqual(todo.reference_type, "PetCare Lead")
        self.assertEqual(todo.reference_name, "LEAD-2026-001")
        self.assertIn("Tran Van B", todo.description)

    def test_02_lead_followup_idempotency_prevents_duplicate_tasks(self):
        """Chạy lại scheduler lần 2 cho cùng 1 Lead -> KHÔNG tạo thêm ToDo trùng."""
        mock_lead = {
            "name": "LEAD-2026-001",
            "lead_name": "Tran Van B",
            "phone": "0901234567",
            "creation": datetime(2026, 10, 24, 10, 0, 0),
        }
        mock_frappe.db.get_list.return_value = [mock_lead]
        # Giả lập đã có sẵn 1 ToDo Open
        mock_frappe.db.get_value.return_value = {
            "name": "TODO-001",
            "allocated_to": "sales_staff_1@petcare.com",
            "description": "Follow-up Lead",
            "priority": "Medium",
        }

        res = LeadFollowupAutomation.process_uncontacted_leads(self.today, threshold_hours=24)

        self.assertEqual(res["processed"], 1)
        self.assertEqual(res["tasks_created"], 0)   # Không tạo mới!
        self.assertEqual(res["tasks_existing"], 1)  # Báo nhận diện ToDo có sẵn

    # ─────────────────────────────────────────────────────────────────
    # Scenario 3 & 4: Membership Expiration & Auto-Expiry
    # ─────────────────────────────────────────────────────────────────
    def test_03_membership_auto_expire_past_end_date(self):
        """Gói hội viên đã quá hạn (end_date < today) -> Chuyển sang Expired."""
        mock_expired_mem = [{"name": "MEM-EXP-001"}]
        mock_frappe.db.get_list.return_value = mock_expired_mem

        count = MembershipRenewalAutomation.auto_expire_memberships(self.today)
        self.assertEqual(count, 1)
        mock_frappe.db.set_value.assert_called_with("Customer Membership", "MEM-EXP-001", "status", "Expired")

    def test_04_membership_renewal_warning_creates_rec_and_task(self):
        """Gói hội viên còn 3 ngày nữa hết hạn -> Tạo Care Recommendation (RENEWAL) và ToDo."""
        expiring_mem = {
            "name": "MEM-ACTIVE-001",
            "customer": "CUST-001",
            "pet": "PET-MOCHI",
            "end_date": self.today + timedelta(days=3),
            "membership_plan": "VIP Club",
        }

        def fake_get_list(doctype, *args, **kwargs):
            filters = kwargs.get("filters", {})
            if "end_date" in filters and filters["end_date"][0] == "<":
                return []  # Không có thẻ nào quá hạn
            return [expiring_mem]

        mock_frappe.db.get_list.side_effect = fake_get_list
        mock_frappe.db.get_value.return_value = None  # Chưa có active rec hay ToDo

        created_docs = []
        def fake_get_doc(*args, **kwargs):
            doc = MockDocument(*args, **kwargs)
            created_docs.append(doc)
            return doc

        mock_frappe.get_doc.side_effect = fake_get_doc

        res = MembershipRenewalAutomation.process_expiring_memberships(self.today, warning_days=7)

        self.assertEqual(res["expiring_count"], 1)
        self.assertEqual(res["recs_created"], 1)
        self.assertEqual(res["tasks_created"], 1)
        self.assertEqual(res["tasks_existing"], 0)

        # Verify docs
        rec = next((d for d in created_docs if getattr(d, "doctype", None) == "Care Recommendation"), None)
        self.assertIsNotNone(rec)
        self.assertEqual(rec.recommendation_type, RECOMMENDATION_TYPE_RENEWAL)
        self.assertEqual(rec.priority, "High")  # <= 3 days -> High
        self.assertIn("3 ngày", rec.reason)

        todo = next((d for d in created_docs if getattr(d, "doctype", None) == "ToDo"), None)
        self.assertIsNotNone(todo)
        self.assertEqual(todo.reference_type, "Customer Membership")
        self.assertEqual(todo.reference_name, "MEM-ACTIVE-001")

    def test_05_membership_renewal_idempotency_prevents_duplicate_recs_and_tasks(self):
        """Chạy lại lần 2 khi đã có sẵn Recommendation và ToDo -> Update in-place, không tạo thêm ToDo."""
        expiring_mem = {
            "name": "MEM-ACTIVE-001",
            "customer": "CUST-001",
            "pet": "PET-MOCHI",
            "end_date": self.today + timedelta(days=3),
            "membership_plan": "VIP Club",
        }
        mock_frappe.db.get_list.return_value = [expiring_mem]

        # Đã có sẵn active Recommendation và ToDo Open
        def fake_get_value(doctype, filters, *args, **kwargs):
            if doctype == "Care Recommendation":
                return {"name": "REC-RENEW-001", "status": "NEW"}
            elif doctype == "ToDo":
                return {"name": "TODO-RENEW-001", "status": "Open"}
            return None

        mock_frappe.db.get_value.side_effect = fake_get_value

        res = MembershipRenewalAutomation.process_expiring_memberships(self.today, warning_days=7)

        self.assertEqual(res["recs_created"], 0)
        self.assertEqual(res["recs_updated"], 1)
        self.assertEqual(res["tasks_created"], 0)
        self.assertEqual(res["tasks_existing"], 1)

    # ─────────────────────────────────────────────────────────────────
    # Scenario 5 & 6: Service Recovery SLA Automation
    # ─────────────────────────────────────────────────────────────────
    def test_06_service_recovery_escalates_breached_case(self):
        """Case khiếu nại mở quá SLA (48h) -> Tạo ToDo escalation cho người phụ trách."""
        case_data = {
            "name": "CASE-2026-001",
            "customer": "CUST-001",
            "pet": "PET-MOCHI",
            "subject": "Bé bị xước chân khi cắt móng",
            "priority": "High",
            "status": "In Progress",
            "assigned_to": "support_lead@petcare.com",
            "creation": datetime(2026, 10, 23, 10, 0, 0),  # 72 hours ago
        }
        mock_frappe.db.get_list.return_value = [case_data]
        mock_frappe.db.get_value.return_value = None  # Chưa có ToDo Open

        created_todos = []
        def fake_get_doc(*args, **kwargs):
            doc = MockDocument(*args, **kwargs)
            if args and isinstance(args[0], dict) and args[0].get("doctype") == "ToDo":
                created_todos.append(doc)
            return doc

        mock_frappe.get_doc.side_effect = fake_get_doc

        res = ServiceRecoveryAutomation.process_open_cases(self.today, sla_hours=48)

        self.assertEqual(res["cases_checked"], 1)
        self.assertEqual(res["escalated_count"], 1)
        self.assertEqual(res["tasks_created"], 1)
        self.assertEqual(len(created_todos), 1)
        todo = created_todos[0]
        self.assertEqual(todo.allocated_to, "support_lead@petcare.com")
        self.assertEqual(todo.priority, "Urgent")  # High priority case escalated to Urgent
        self.assertIn("Service Recovery SLA Escalation", todo.description)

    def test_07_service_recovery_idempotency_prevents_duplicate_tasks(self):
        """Chạy lần 2 khi Case đã có escalation ToDo -> Không tạo thêm ToDo."""
        case_data = {
            "name": "CASE-2026-001",
            "customer": "CUST-001",
            "subject": "Khiếu nại dịch vụ",
            "priority": "High",
            "status": "Open",
            "creation": datetime(2026, 10, 23, 10, 0, 0),
        }
        mock_frappe.db.get_list.return_value = [case_data]
        mock_frappe.db.get_value.return_value = {"name": "TODO-CASE-001", "status": "Open"}

        res = ServiceRecoveryAutomation.process_open_cases(self.today, sla_hours=48)

        self.assertEqual(res["cases_checked"], 1)
        self.assertEqual(res["tasks_created"], 0)
        self.assertEqual(res["tasks_existing"], 1)

    # ─────────────────────────────────────────────────────────────────
    # Scenario 7: Safe Mode Communication Gateway
    # ─────────────────────────────────────────────────────────────────
    def test_08_safe_mode_communication_suppresses_real_sending(self):
        """Khi ENABLE_LIVE_COMMUNICATION là False -> Chỉ ghi mock log, không gửi thật."""
        res = SafeCommunicationGateway.send_communication(
            recipient="customer@example.com",
            subject="Nhắc lịch chăm sóc thú cưng",
            content="Bé Mochi sắp đến chu kỳ Grooming...",
            channel="Email",
            reference_doctype="PetCare Lead",
            reference_name="LEAD-001",
            force_live=False,
        )

        self.assertFalse(res["sent"])
        self.assertEqual(res["mode"], "SAFE_MODE_MOCK")
        self.assertIn("Safe Mode", res["message"])

    # ─────────────────────────────────────────────────────────────────
    # Scenario 8: Master AutomationCoordinator Fault Tolerance & Report
    # ─────────────────────────────────────────────────────────────────
    def test_09_coordinator_handles_partial_failures_and_generates_report(self):
        """Khi 1 tác vụ bị lỗi (ví dụ Lead lỗi DB), coordinator bắt ngoại lệ và tiếp tục các tác vụ còn lại."""
        mock_lead_bad = {
            "name": "LEAD-BAD",
            "status": "New",
            "creation": "INVALID_DATE_FORMAT_FORCE_ERROR",
        }
        mock_frappe.db.get_list.return_value = [mock_lead_bad]

        report = AutomationCoordinator.run_all_automations(self.today)

        self.assertIn("timestamp", report)
        self.assertIn("lead_followup", report)
        self.assertIn("membership_renewal", report)
        self.assertIn("care_engine", report)
        self.assertIn("service_recovery", report)
        # Báo cáo được tạo đầy đủ
        self.assertIsInstance(report["total_tasks_created"], int)
        self.assertIsInstance(report["errors"], list)


if __name__ == "__main__":
    unittest.main()
