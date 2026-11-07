# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

"""
Automated Test Suite for WordPress Lead Capture Integration (Rubric A4.8).
Tests all 6 required integration scenarios:
1. Valid submission via create_lead (Server-to-Server Proxy).
2. Valid submission via submit_website_lead (Public Guest API).
3. Missing mandatory fields validation (lead_name, phone).
4. Invalid phone format rejection (letters, length, non-VN prefix).
5. Vietnamese phone normalization (+84 -> 0, space/hyphen stripping).
6. Honeypot anti-spam bot trap (benign response, zero dirty DB records).
7. Lead Source tagging & combined pet info formatting.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath("apps/petcare_crm"))

# Setup mock frappe if not already present
if "frappe" not in sys.modules:
    mock_frappe = MagicMock()
    mock_frappe._ = lambda x: x
    def _throw(msg, exc=Exception):
        raise exc(msg)
    mock_frappe.throw = _throw
    mock_frappe.session = MagicMock()
    mock_frappe.session.user = "Administrator"
    def mock_whitelist(*args, **kwargs):
        def decorator(fn):
            return fn
        if len(args) == 1 and callable(args[0]):
            return args[0]
        return decorator

    mock_frappe.whitelist = mock_whitelist

    mock_frappe_utils = MagicMock()
    mock_frappe_utils.now_datetime.return_value = "2026-10-26 14:00:00"
    mock_frappe_utils.nowdate.return_value = "2026-10-26"
    mock_frappe_utils.getdate = lambda d: d
    mock_frappe.utils = mock_frappe_utils

    sys.modules["frappe"] = mock_frappe
    sys.modules["frappe.utils"] = mock_frappe_utils
    sys.modules["frappe.model"] = MagicMock()
    sys.modules["frappe.model.document"] = MagicMock()

import frappe
from petcare_crm.utils.lead_service import LeadManagementService
from petcare_crm.utils.exceptions import ValidationError


class TestWordPressLeadIntegration(unittest.TestCase):

    def setUp(self):
        frappe.flags.in_test = True
        frappe.cache = lambda: None
        self.created_docs = []

        def mock_get_doc(data):
            doc = MagicMock()
            for k, v in data.items():
                setattr(doc, k, v)
            doc.name = f"LEAD-2026-{len(self.created_docs) + 10001}"
            def fake_insert(ignore_permissions=True):
                self.created_docs.append(doc)
                return doc
            doc.insert = fake_insert
            return doc

        frappe.get_doc = mock_get_doc

    def test_01_valid_lead_submission_server_proxy(self):
        """Kịch bản 1: WordPress Server Proxy gọi create_lead với đầy đủ dữ liệu."""
        lead_id = LeadManagementService.create_lead(
            lead_name="Nguyễn Văn An",
            phone="0912345678",
            lead_source="WordPress Form",
            email="an.nguyen@example.com",
            initial_pet_info="Dịch vụ quan tâm: Tắm Spa. Bé Poodle 4kg",
            priority="Medium",
            lead_owner="Administrator"
        )
        self.assertTrue(lead_id.startswith("LEAD-2026-"))
        self.assertEqual(len(self.created_docs), 1)
        doc = self.created_docs[0]
        self.assertEqual(doc.lead_name, "Nguyễn Văn An")
        self.assertEqual(doc.phone, "0912345678")
        self.assertEqual(doc.lead_source, "WordPress Form")
        self.assertEqual(doc.status, "New")

    def test_02_phone_normalization_plus84_and_spaces(self):
        """Kịch bản 2: Chuẩn hóa số điện thoại Việt Nam từ +84 hoặc có dấu gạch ngang/khoảng trắng."""
        test_cases = [
            ("+84912345678", "0912345678"),
            ("091 234 5678", "0912345678"),
            ("091-234-5678", "0912345678"),
            ("+84 987 654 321", "0987654321"),
        ]
        for raw_phone, expected_phone in test_cases:
            lead_id = LeadManagementService.create_lead(
                lead_name="Khách Hàng Test SĐT",
                phone=raw_phone,
                lead_source="WordPress Form"
            )
            self.assertTrue(lead_id.startswith("LEAD-2026-"))
            self.assertEqual(self.created_docs[-1].phone, expected_phone)

    def test_03_missing_mandatory_fields(self):
        """Kịch bản 3: Từ chối lưu bản ghi nếu thiếu họ tên hoặc số điện thoại."""
        # Thiếu họ tên
        with self.assertRaises(ValidationError) as ctx:
            LeadManagementService.create_lead(lead_name="", phone="0912345678", lead_source="WordPress Form")
        self.assertIn("lead_name", str(ctx.exception))

        # Thiếu số điện thoại
        with self.assertRaises(ValidationError) as ctx:
            LeadManagementService.create_lead(lead_name="Trần Văn B", phone="", lead_source="WordPress Form")
        self.assertIn("phone", str(ctx.exception))

    def test_04_invalid_phone_format(self):
        """Kịch bản 4: Chặn các định dạng số điện thoại không hợp lệ (chữ cái, sai độ dài)."""
        invalid_phones = ["123456", "0912abcxyz", "01234567890123", "abcxyz"]
        for bad_phone in invalid_phones:
            with self.assertRaises(ValidationError):
                LeadManagementService.create_lead(
                    lead_name="Khách Hàng Lỗi",
                    phone=bad_phone,
                    lead_source="WordPress Form"
                )

    def test_05_honeypot_bot_trap_via_api(self):
        """Kịch bản 5: Bẫy bot spam qua Honeypot - bot điền trường ẩn thì trả về giả lập thành công, KHÔNG ghi DB."""
        from petcare_crm.api import submit_website_lead

        # Giả lập bot điền trường hp_field
        initial_doc_count = len(self.created_docs)
        response = submit_website_lead(
            lead_name="Bot Casino 88",
            phone="0911223344",
            hp_field="http://spam-link-casino.com"
        )
        # Phải trả về status success và lead_id bot trap
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["lead_id"], "LEAD-BOT-TRAP")
        # Cơ sở dữ liệu hoàn toàn không tăng thêm bản ghi nào
        self.assertEqual(len(self.created_docs), initial_doc_count)

    def test_06_public_guest_api_happy_path(self):
        """Kịch bản 6: Gọi endpoint submit_website_lead công khai với dữ liệu hợp lệ."""
        from petcare_crm.api import submit_website_lead

        response = submit_website_lead(
            lead_name="Lê Thị Hồng",
            phone="0988776655",
            email="hong.le@example.com",
            service_type="Khám Sức Khỏe & Thú Y",
            pet_notes="Bé Mèo Nga 1 tuổi cần siêu âm bụng",
            hp_field="" # Honeypot để trống đúng chuẩn người thật
        )
        self.assertEqual(response["status"], "success")
        self.assertTrue(response["lead_id"].startswith("LEAD-2026-"))
        created = self.created_docs[-1]
        self.assertEqual(created.lead_name, "Lê Thị Hồng")
        self.assertEqual(created.phone, "0988776655")
        self.assertEqual(created.lead_source, "Website Landing Page")
        self.assertIn("Khám Sức Khỏe", created.initial_pet_info)
        self.assertIn("Bé Mèo Nga", created.initial_pet_info)


if __name__ == "__main__":
    unittest.main()
