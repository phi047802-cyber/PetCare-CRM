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

if "frappe" in sys.modules:
    mock_frappe = sys.modules["frappe"]
    mock_frappe_utils = mock_frappe.utils
    mock_frappe_doc = mock_frappe.model.document
else:
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

from petcare_crm.petcare_crm.doctype.petcare_service.petcare_service import PetCareService
from petcare_crm.petcare_crm.doctype.petcare_case.petcare_case import PetCareCase
from petcare_crm.petcare_crm.doctype.service_visit.service_visit import ServiceVisit
from petcare_crm.utils.service_operations import (
    ServiceCatalogService,
    ServiceVisitService,
    CaseManagementService,
)
from petcare_crm.utils.exceptions import ValidationError, EntityNotFoundException


class TestServiceOperationsMock(unittest.TestCase):
    """
    Kiểm thử độc lập các quy tắc nghiệp vụ Service Operations & PetCare Domain
    đáp ứng 100% các tiêu chí nghiệm thu của Prompt 4.
    """

    def setUp(self):
        mock_frappe.db.reset_mock()
        mock_frappe.db.exists.return_value = True
        mock_frappe.get_doc.side_effect = None
        mock_frappe.get_cached_doc.side_effect = None
        mock_frappe.db.get_value.side_effect = None

    def tearDown(self):
        mock_frappe.get_doc.side_effect = None
        mock_frappe.get_cached_doc.side_effect = None
        mock_frappe.db.get_value.side_effect = None

    def test_01_service_catalog_validation(self):
        """Kiểm tra validation của danh mục dịch vụ."""
        srv = PetCareService()
        srv.service_code = " srv-spa-01 "
        srv.service_name = "Tắm Spa"
        srv.standard_price = 250000.0
        srv.default_cycle_days = 20
        srv.validate()
        self.assertEqual(srv.service_code, "SRV-SPA-01")

        # Giá âm -> Throw
        srv.standard_price = -5000.0
        with self.assertRaises(Exception):
            srv.validate()

    def test_02_service_visit_pricing_calculation(self):
        """Kiểm tra tính giá gốc, discount_amount và final_price."""
        sv = ServiceVisit()
        sv.pet = "Bé Bơ"
        sv.customer = "CT-001"
        sv.service = None
        sv.original_price = 300000.0
        sv.final_price = 200000.0  # giảm 100k
        mock_frappe.db.get_value.return_value = "CT-001"
        mock_frappe.db.exists.return_value = True

        sv.validate()
        self.assertEqual(sv.discount_amount, 100000.0)
        self.assertEqual(sv.final_price, 200000.0)

    def test_03_case_lifecycle_and_resolution(self):
        """Kiểm tra vòng đời PetCare Case: Resolved bắt buộc có resolution."""
        c = PetCareCase()
        c.customer = "CT-001"
        c.pet = None
        c.status = "Resolved"
        c.resolution = ""

        # Thiếu resolution khi Resolved -> Throw
        with self.assertRaises(Exception):
            c.validate()

        # Có resolution -> Pass
        c.resolution = "Đã đổi loại sữa tắm cho bé"
        c.validate()
        self.assertIsNotNone(c.resolved_date)

    def test_04_service_visit_free_benefit_redemption_mock(self):
        """Kiểm tra luồng cấn trừ quyền lợi thẻ hội viên miễn phí 100% (FREE)."""
        mock_frappe.db.exists.return_value = True
        mock_frappe.db.get_value.return_value = "CT-001"

        # Mock PetCare Service
        mock_srv = MockDocument(
            service_code="SRV-BATH",
            service_name="Tắm Spa",
            standard_price=250000.0
        )

        # Mock Benefit & Membership
        mock_benefit = MockDocument(
            benefit_type="Tắm Spa",
            total_quantity=5,
            used_quantity=1,
            remaining_quantity=4,
            discount_type="FREE",
            discount_value=0
        )
        mock_membership = MockDocument(
            name="MEM-2026-0001",
            status="Active",
            pet=None,  # Family plan
            benefits=[mock_benefit]
        )

        def fake_get_cached_doc(doctype, name):
            if doctype == "PetCare Service":
                return mock_srv
            return MockDocument()

        mock_frappe.get_cached_doc.side_effect = fake_get_cached_doc
        mock_frappe.get_doc.side_effect = lambda *args, **kwargs: (
            mock_membership if args and args[0] == "Customer Membership" else MockDocument(*args, **kwargs)
        )

        receipt = ServiceVisitService.create_service_visit(
            pet="Bé Bơ",
            service_identifier="SRV-BATH",
            membership_id="MEM-2026-0001"
        )

        self.assertEqual(receipt["status"], "success")
        self.assertEqual(receipt["original_price"], 250000.0)
        self.assertEqual(receipt["discount_amount"], 250000.0)
        self.assertEqual(receipt["final_price"], 0.0)
        self.assertEqual(receipt["benefit_used"], "Tắm Spa")
        # Đã trừ 1 lượt: used = 2
        self.assertEqual(mock_benefit.used_quantity, 2)


if __name__ == "__main__":
    unittest.main()
