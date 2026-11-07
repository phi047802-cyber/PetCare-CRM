# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath("apps/petcare_crm"))

# Setup mock frappe
class MockFrappeException(Exception):
    pass

class MockDocument:
    def __init__(self, *args, **kwargs):
        self._is_new = True
        self.name = kwargs.get("name", "DOC-001")
        for k, v in kwargs.items():
            setattr(self, k, v)
    def is_new(self):
        return getattr(self, "_is_new", True)
    def insert(self, *args, **kwargs):
        self._is_new = False
        return self
    def save(self, *args, **kwargs):
        return self
    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
    def get(self, k, default=None):
        return getattr(self, k, default)

mock_frappe = MagicMock()
mock_frappe._ = lambda x: x
def _throw(msg, exc=MockFrappeException):
    raise exc(msg)
mock_frappe.throw = _throw
mock_frappe.session = MagicMock()
mock_frappe.session.user = "Administrator"

mock_frappe_utils = MagicMock()
mock_frappe_utils.now_datetime.return_value = "2026-10-26 14:00:00"
mock_frappe_utils.nowdate.return_value = "2026-10-26"
mock_frappe_utils.getdate = lambda d: d

mock_frappe.utils = mock_frappe_utils
mock_frappe_doc = MagicMock()
mock_frappe_doc.Document = MockDocument
mock_frappe.model = MagicMock()
mock_frappe.model.document = mock_frappe_doc

sys.modules["frappe"] = mock_frappe
sys.modules["frappe.utils"] = mock_frappe_utils
sys.modules["frappe.model"] = mock_frappe.model
sys.modules["frappe.model.document"] = mock_frappe_doc

from petcare_crm.petcare_crm.doctype.benefit_redemption_ledger.benefit_redemption_ledger import BenefitRedemptionLedger
from petcare_crm.utils.service_operations import (
    ServiceCatalogService,
    ServiceVisitService,
    MembershipLifecycleService,
)
from petcare_crm.utils.exceptions import (
    ValidationError,
    BenefitExhaustedException,
    MembershipExpiredException,
)


class TestMembershipLifecycleAndRedemptionMock(unittest.TestCase):
    """
    Kiểm thử 10 kịch bản của Prompt 5:
    1. Membership active.
    2. Membership expired/cancelled.
    3. Benefit available/exhausted.
    4. Free Grooming.
    5. Spa giảm 10%.
    6. Service không thuộc Plan.
    7. Concurrency / double-redeem protection (Idempotency).
    8. Hủy Service Visit & Revert benefit.
    9. Renewal & Rollover.
    10. Thay đổi Plan không làm sai lịch sử.
    """

    def setUp(self):
        mock_frappe.db.reset_mock()
        mock_frappe.db.exists.return_value = True
        mock_frappe.get_doc.side_effect = None
        mock_frappe.get_cached_doc.side_effect = None
        mock_frappe.db.get_value.side_effect = None
        mock_frappe.db.get_value.return_value = "CT-001"

    def tearDown(self):
        mock_frappe.get_doc.side_effect = None
        mock_frappe.get_cached_doc.side_effect = None
        mock_frappe.db.get_value.side_effect = None

    def test_01_and_04_free_grooming_active_membership(self):
        """Kịch bản 1 & 4: Membership active, Free Grooming -> final_price = 0."""
        mock_frappe.db.get_value.return_value = "CT-001"
        mock_srv = MockDocument(service_code="SRV-GROOM", service_name="Grooming", standard_price=300000.0)

        mock_benefit = MockDocument(
            benefit_type="Grooming",
            total_quantity=5,
            used_quantity=1,
            remaining_quantity=4,
            discount_type="FREE",
            discount_value=0
        )
        mock_ms = MockDocument(
            name="MEM-001",
            status="Active",
            pet=None,
            benefits=[mock_benefit]
        )

        mock_frappe.get_cached_doc.return_value = mock_srv
        mock_frappe.get_doc.side_effect = lambda *args, **kwargs: (
            mock_ms if args and args[0] == "Customer Membership" else MockDocument(*args, **kwargs)
        )

        receipt = ServiceVisitService.create_service_visit(
            pet="Bé Bơ",
            service_identifier="SRV-GROOM",
            membership_id="MEM-001"
        )

        self.assertEqual(receipt["final_price"], 0.0)
        self.assertEqual(receipt["discount_amount"], 300000.0)
        self.assertEqual(mock_benefit.used_quantity, 2)
        self.assertEqual(mock_benefit.remaining_quantity, 3)

    def test_02_membership_expired_or_cancelled_cannot_redeem(self):
        """Kịch bản 2: Thẻ hội viên Expired / Cancelled -> Không được phép cấn trừ quyền lợi."""
        mock_frappe.db.get_value.return_value = "CT-001"
        mock_srv = MockDocument(service_code="SRV-SPA", service_name="Spa", standard_price=200000.0)
        mock_frappe.get_cached_doc.return_value = mock_srv

        mock_ms = MockDocument(
            name="MEM-002",
            status="Expired",
            pet=None,
            benefits=[]
        )
        mock_frappe.get_doc.side_effect = lambda *args, **kwargs: (
            mock_ms if args and args[0] == "Customer Membership" else MockDocument(*args, **kwargs)
        )

        with self.assertRaises(MembershipExpiredException):
            ServiceVisitService.create_service_visit(
                pet="Bé Bơ",
                service_identifier="SRV-SPA",
                membership_id="MEM-002"
            )

    def test_03_benefit_exhausted_raises_exception(self):
        """Kịch bản 3: Quyền lợi trong thẻ đã dùng hết (remaining = 0) -> Báo lỗi."""
        mock_frappe.db.get_value.return_value = "CT-001"
        mock_srv = MockDocument(service_code="SRV-SPA", service_name="Spa", standard_price=200000.0)
        mock_frappe.get_cached_doc.return_value = mock_srv

        mock_benefit = MockDocument(
            benefit_type="Spa",
            total_quantity=2,
            used_quantity=2,
            remaining_quantity=0,
            discount_type="FREE"
        )
        mock_ms = MockDocument(
            name="MEM-003",
            status="Active",
            pet=None,
            benefits=[mock_benefit]
        )
        mock_frappe.get_doc.side_effect = lambda *args, **kwargs: (
            mock_ms if args and args[0] == "Customer Membership" else MockDocument(*args, **kwargs)
        )

        with self.assertRaises(BenefitExhaustedException):
            ServiceVisitService.create_service_visit(
                pet="Bé Bơ",
                service_identifier="SRV-SPA",
                membership_id="MEM-003"
            )

    def test_05_spa_percentage_discount_10_percent(self):
        """Kịch bản 5: Quyền lợi giảm giá 10% cho Spa -> final_price = 90% original."""
        mock_frappe.db.get_value.return_value = "CT-001"
        mock_srv = MockDocument(service_code="SRV-SPA", service_name="Spa Thư Giãn", standard_price=500000.0)
        mock_frappe.get_cached_doc.return_value = mock_srv

        mock_benefit = MockDocument(
            benefit_type="Spa Thư Giãn",
            total_quantity=10,
            used_quantity=0,
            remaining_quantity=10,
            discount_type="PERCENTAGE",
            discount_value=10.0
        )
        mock_ms = MockDocument(
            name="MEM-004",
            status="Active",
            pet=None,
            benefits=[mock_benefit]
        )
        mock_frappe.get_doc.side_effect = lambda *args, **kwargs: (
            mock_ms if args and args[0] == "Customer Membership" else MockDocument(*args, **kwargs)
        )

        receipt = ServiceVisitService.create_service_visit(
            pet="Bé Bơ",
            service_identifier="SRV-SPA",
            membership_id="MEM-004"
        )

        self.assertEqual(receipt["original_price"], 500000.0)
        self.assertEqual(receipt["discount_amount"], 50000.0)
        self.assertEqual(receipt["final_price"], 450000.0)

    def test_06_service_not_in_plan_charges_normal_price(self):
        """Kịch bản 6: Dịch vụ không nằm trong gói thẻ -> Thu đúng giá gốc niêm yết."""
        mock_frappe.db.get_value.return_value = "CT-001"
        mock_srv = MockDocument(service_code="SRV-HOTEL", service_name="Khách Sạn Lưu Chuồng", standard_price=150000.0)
        mock_frappe.get_cached_doc.return_value = mock_srv

        mock_benefit = MockDocument(
            benefit_type="Grooming",
            total_quantity=5,
            used_quantity=0,
            remaining_quantity=5,
            discount_type="FREE"
        )
        mock_ms = MockDocument(
            name="MEM-005",
            status="Active",
            pet=None,
            benefits=[mock_benefit]
        )
        mock_frappe.get_doc.side_effect = lambda *args, **kwargs: (
            mock_ms if args and args[0] == "Customer Membership" else MockDocument(*args, **kwargs)
        )

        receipt = ServiceVisitService.create_service_visit(
            pet="Bé Bơ",
            service_identifier="SRV-HOTEL",
            membership_id="MEM-005"
        )

        self.assertEqual(receipt["original_price"], 150000.0)
        self.assertEqual(receipt["discount_amount"], 0.0)
        self.assertEqual(receipt["final_price"], 150000.0)
        self.assertIsNone(receipt["benefit_used"])

    def test_07_idempotency_retry_does_not_double_redeem(self):
        """Kịch bản 7: Retry với cùng Idempotency Key -> Trả về kết quả cũ, không trừ lượt lần 2."""
        mock_ledger_entry = MockDocument(
            service_visit="SV-2026-00099",
            membership="MEM-001",
            benefit_type="Grooming",
            discount_applied=300000.0
        )
        mock_visit_entry = MockDocument(
            name="SV-2026-00099",
            pet="Bé Bơ",
            customer="CT-001",
            service_type="Grooming",
            original_price=300000.0,
            discount_amount=300000.0,
            final_price=0.0,
            membership="MEM-001",
            benefit_used="Grooming"
        )

        def fake_get_value(doctype, filters, fieldname=None, as_dict=False):
            if doctype == "Benefit Redemption Ledger" and isinstance(filters, dict) and "idempotency_key" in filters:
                return mock_ledger_entry
            return None

        mock_frappe.db.get_value.side_effect = fake_get_value
        mock_frappe.get_doc.side_effect = lambda *args, **kwargs: (
            mock_visit_entry if args and args[0] == "Service Visit" else MockDocument(*args, **kwargs)
        )

        receipt = ServiceVisitService.create_service_visit(
            pet="Bé Bơ",
            service_identifier="Grooming",
            idempotency_key="REQ-UNIQUE-12345"
        )

        self.assertTrue(receipt.get("is_idempotent_replay"))
        self.assertEqual(receipt["visit_id"], "SV-2026-00099")

    def test_08_cancel_service_visit_reverts_benefit(self):
        """Kịch bản 8: Hủy phiếu dịch vụ -> Hoàn trả lại quyền lợi thẻ hội viên an toàn."""
        mock_benefit = MockDocument(
            benefit_type="Grooming",
            total_quantity=5,
            used_quantity=3,
            remaining_quantity=2
        )
        mock_ms = MockDocument(
            name="MEM-001",
            benefits=[mock_benefit]
        )
        mock_frappe.get_doc.side_effect = lambda *args, **kwargs: (
            mock_ms if args and args[0] == "Customer Membership" else MockDocument(*args, **kwargs)
        )

        ledger = BenefitRedemptionLedger()
        ledger.membership = "MEM-001"
        ledger.benefit_type = "Grooming"
        ledger.quantity_redeemed = 1
        ledger.discount_applied = 300000.0
        ledger.status = "Applied"

        ledger.revert(reason="Khách hủy dịch vụ đột xuất")

        self.assertEqual(ledger.status, "Reverted")
        self.assertEqual(mock_benefit.used_quantity, 2)
        self.assertEqual(mock_benefit.remaining_quantity, 3)

    def test_09_and_10_renewal_rollover_and_immutable_history(self):
        """Kịch bản 9 & 10: Gia hạn thẻ -> Kế thừa lượt tồn, bảo toàn số dư và lịch sử cũ."""
        old_benefit = MockDocument(
            benefit_type="Grooming",
            total_quantity=5,
            used_quantity=3,
            remaining_quantity=2
        )
        old_ms = MockDocument(
            name="MEM-OLD-001",
            customer="CT-001",
            pet="Bé Bơ",
            balance=500000.0,
            benefits=[old_benefit]
        )

        new_plan_benefit = MockDocument(
            benefit_type="Grooming",
            total_quantity=5,
            discount_type="FREE",
            discount_value=0
        )
        new_plan = MockDocument(
            name="PLAN-NEW-10",
            plan_name="Gói 10 Buổi",
            validity_days=180,
            benefits=[new_plan_benefit]
        )

        def fake_get_doc(*args, **kwargs):
            if args:
                if args[0] == "Customer Membership":
                    return old_ms
                elif args[0] == "Membership Plan":
                    return new_plan
                elif isinstance(args[0], dict):
                    return MockDocument(**args[0])
            return MockDocument()

        mock_frappe.get_doc.side_effect = fake_get_doc

        result = MembershipLifecycleService.renew_membership(
            old_membership_id="MEM-OLD-001",
            new_plan_name="PLAN-NEW-10",
            allow_rollover=True
        )

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["transferred_balance"], 500000.0)
        self.assertEqual(old_ms.status, "Renewed")
        self.assertEqual(old_ms.balance, 0.0)
        self.assertIn("Grooming: +2 lượt", result["rollover_summary"][0])


if __name__ == "__main__":
    unittest.main()
