# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import unittest
import frappe
from frappe.utils import nowdate, now_datetime

from petcare_crm.utils.service_operations import (
    ServiceCatalogService,
    ServiceVisitService,
    CaseManagementService,
)
from petcare_crm.utils.customer_service import CustomerService
from petcare_crm.utils.exceptions import (
    ValidationError,
    EntityNotFoundException,
)


class TestServiceOperations(unittest.TestCase):
    """
    Unit & Integration Tests for PetCare Domain & Service Operations:
    - 1 Customer with multiple Pets
    - Service Catalog items and pricing
    - Service Visit with/without Membership benefits
    - Discount calculations
    - Customer 360 strict data isolation between Pets
    - Post-service Cases/Feedback lifecycle
    """

    def setUp(self):
        self.ts = now_datetime().strftime("%Y%m%d%H%M%S%f")
        self.phone = f"0933{self.ts[-6:]}"

    def tearDown(self):
        frappe.db.rollback()

    def test_01_multi_pet_ownership_under_one_customer(self):
        """Kiểm tra một Customer có nhiều Pet và không bị lẫn lộn."""
        cust = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "Nguyễn",
            "last_name": "Thanh Hải",
            "phone": self.phone,
        }).insert(ignore_permissions=True)

        pet1 = frappe.get_doc({
            "doctype": "Pet",
            "pet_name": f"Bé Corgi_{self.ts[-4:]}",
            "customer": cust.name,
            "species": "Dog",
            "weight_kg": 10.5
        }).insert(ignore_permissions=True)

        pet2 = frappe.get_doc({
            "doctype": "Pet",
            "pet_name": f"Bé Mèo Nga_{self.ts[-4:]}",
            "customer": cust.name,
            "species": "Cat",
            "weight_kg": 4.2
        }).insert(ignore_permissions=True)

        # Kiểm tra qua Customer 360
        c360 = CustomerService.get_customer_360(cust.name)
        self.assertEqual(c360["pets_count"], 2)
        pet_ids = [p["name"] for p in c360["pets"]]
        self.assertIn(pet1.name, pet_ids)
        self.assertIn(pet2.name, pet_ids)

    def test_02_service_catalog_registration_and_lookup(self):
        """Kiểm tra đăng ký và tra cứu danh mục dịch vụ chuẩn."""
        code = f"SRV-SPA-{self.ts[-4:]}"
        ServiceCatalogService.create_service(
            service_code=code,
            service_name="Tắm Spa Thảo Dược Toàn Diện",
            category="Grooming & Spa",
            standard_price=350000.0,
            default_cycle_days=21,
            target_species="Dog",
            estimated_duration_minutes=90
        )

        srv = ServiceCatalogService.get_service(code)
        self.assertIsNotNone(srv)
        self.assertEqual(srv["service_name"], "Tắm Spa Thảo Dược Toàn Diện")
        self.assertEqual(float(srv["standard_price"]), 350000.0)
        self.assertEqual(int(srv["default_cycle_days"]), 21)

    def test_03_service_visit_without_membership_full_price(self):
        """Kiểm tra lượt dịch vụ không có Thẻ hội viên -> Thu đúng giá gốc 100%."""
        cust = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "Lê",
            "last_name": "Văn Nam",
            "phone": self.phone,
        }).insert(ignore_permissions=True)

        pet = frappe.get_doc({
            "doctype": "Pet",
            "pet_name": f"Bé Husky_{self.ts[-4:]}",
            "customer": cust.name,
            "species": "Dog",
        }).insert(ignore_permissions=True)

        code = f"SRV-CUT-{self.ts[-4:]}"
        ServiceCatalogService.create_service(
            service_code=code,
            service_name="Cắt Tỉa Lông Nghệ Thuật",
            category="Grooming & Spa",
            standard_price=300000.0
        )

        # Mở phiếu dịch vụ
        receipt = ServiceVisitService.create_service_visit(
            pet=pet.name,
            service_identifier=code,
            weight_kg=18.5
        )

        self.assertEqual(receipt["status"], "success")
        self.assertEqual(receipt["original_price"], 300000.0)
        self.assertEqual(receipt["discount_amount"], 0.0)
        self.assertEqual(receipt["final_price"], 300000.0)
        self.assertIsNone(receipt["membership_used"])

        # Kiểm tra cân nặng Pet đã được cập nhật
        updated_pet = frappe.get_doc("Pet", pet.name)
        self.assertEqual(updated_pet.weight_kg, 18.5)

    def test_04_service_visit_with_membership_benefit_redemption(self):
        """Kiểm tra lượt dịch vụ có Thẻ hội viên (FREE 100%) -> Tự động cấn trừ 1 lượt."""
        cust = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "Phan",
            "last_name": "Thị Loan",
            "phone": self.phone,
        }).insert(ignore_permissions=True)

        pet = frappe.get_doc({
            "doctype": "Pet",
            "pet_name": f"Bé Poodle_{self.ts[-4:]}",
            "customer": cust.name,
            "species": "Dog",
        }).insert(ignore_permissions=True)

        # Tạo gói Plan và Thẻ hội viên với 5 lượt Tắm Spa Miễn Phí
        plan = frappe.get_doc({
            "doctype": "Membership Plan",
            "plan_name": f"Gói Spa Thân Thiết_{self.ts[-4:]}",
            "price": 1000000.0,
            "validity_days": 90,
            "benefits": [
                {
                    "benefit_type": "Tắm Spa",
                    "total_quantity": 5,
                    "discount_type": "FREE",
                    "discount_value": 0
                }
            ]
        }).insert(ignore_permissions=True)

        ms = frappe.get_doc({
            "doctype": "Customer Membership",
            "customer": cust.name,
            "pet": pet.name,
            "membership_plan": plan.name,
            "start_date": "2026-01-01",
            "end_date": "2026-12-31",
            "status": "Active",
            "benefits": [
                {
                    "benefit_type": "Tắm Spa",
                    "total_quantity": 5,
                    "used_quantity": 0,
                    "remaining_quantity": 5,
                    "discount_type": "FREE",
                    "discount_value": 0
                }
            ]
        }).insert(ignore_permissions=True)

        # Tạo dịch vụ Tắm Spa giá 250,000 VNĐ
        code = f"SRV-BATH-{self.ts[-4:]}"
        ServiceCatalogService.create_service(
            service_code=code,
            service_name="Tắm Spa Thư Giãn",
            category="Grooming & Spa",
            standard_price=250000.0
        )

        # Mở phiếu dịch vụ
        receipt = ServiceVisitService.create_service_visit(
            pet=pet.name,
            service_identifier=code,
            membership_id=ms.name
        )

        self.assertEqual(receipt["status"], "success")
        self.assertEqual(receipt["original_price"], 250000.0)
        self.assertEqual(receipt["discount_amount"], 250000.0)
        self.assertEqual(receipt["final_price"], 0.0)
        self.assertEqual(receipt["membership_used"], ms.name)
        self.assertEqual(receipt["benefit_used"], "Tắm Spa")

        # Kiểm tra thẻ đã bị trừ 1 lượt (remaining còn 4)
        ms_reloaded = frappe.get_doc("Customer Membership", ms.name)
        b = ms_reloaded.benefits[0]
        self.assertEqual(b.used_quantity, 1)
        self.assertEqual(b.remaining_quantity, 4)

    def test_05_strict_data_isolation_between_pets_in_customer_360(self):
        """
        Kiểm tra tính cô lập dữ liệu (Strict Data Isolation):
        Không được lấy Service Visit của Pet A gán cho Pet B dù cùng chung một chủ.
        """
        cust = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "Đỗ",
            "last_name": "Thị Hương",
            "phone": self.phone,
        }).insert(ignore_permissions=True)

        pet_a = frappe.get_doc({
            "doctype": "Pet",
            "pet_name": f"Bé Lu_{self.ts[-4:]}",
            "customer": cust.name,
            "species": "Dog",
        }).insert(ignore_permissions=True)

        pet_b = frappe.get_doc({
            "doctype": "Pet",
            "pet_name": f"Bé Mi_{self.ts[-4:]}",
            "customer": cust.name,
            "species": "Cat",
        }).insert(ignore_permissions=True)

        # Tạo 2 lượt dịch vụ cho Bé Lu
        ServiceVisitService.create_service_visit(pet=pet_a.name, service_identifier="Grooming", visit_date="2026-10-01")
        ServiceVisitService.create_service_visit(pet=pet_a.name, service_identifier="Spa", visit_date="2026-10-15")

        # Tạo 1 lượt dịch vụ cho Bé Mi
        ServiceVisitService.create_service_visit(pet=pet_b.name, service_identifier="Nail Care", visit_date="2026-10-20")

        # Kiểm tra hàm get_service_visits trên từng Pet Document
        visits_a = pet_a.get_service_visits()
        visits_b = pet_b.get_service_visits()

        self.assertEqual(len(visits_a), 2)
        self.assertEqual(len(visits_b), 1)

        # Đảm bảo không bị lẫn lộn giữa 2 bé
        self.assertEqual(visits_b[0]["service_type"], "Nail Care")

        # Kiểm tra qua Customer 360: visits_by_pet phân định rạch ròi
        c360 = CustomerService.get_customer_360(cust.name)
        self.assertEqual(len(c360["visits_by_pet"][pet_a.name]), 2)
        self.assertEqual(len(c360["visits_by_pet"][pet_b.name]), 1)

    def test_06_post_service_case_and_feedback_lifecycle(self):
        """Kiểm tra tạo phản hồi sau dịch vụ (PetCare Case) và quy trình giải quyết."""
        cust = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "Bùi",
            "last_name": "Văn Tiến",
            "phone": self.phone,
        }).insert(ignore_permissions=True)

        # 1. Tạo Case phản hồi
        case_id = CaseManagementService.create_case(
            customer=cust.name,
            subject="Bé bị ngứa nhẹ sau khi tắm spa",
            description="Khách phản hồi sau buổi spa hôm qua cún hay gãi tai, nhờ kiểm tra sữa tắm.",
            case_type="Health Issue",
            priority="High"
        )
        self.assertTrue(case_id.startswith("CASE-"))

        case_doc = frappe.get_doc("PetCare Case", case_id)
        self.assertEqual(case_doc.status, "New")

        # 2. Chuyển sang In Progress
        CaseManagementService.update_case_status(case_id, "In Progress")
        self.assertEqual(frappe.db.get_value("PetCare Case", case_id, "status"), "In Progress")

        # 3. Hoàn tất xử lý (Resolved) thiếu resolution -> Báo lỗi
        with self.assertRaises(ValidationError):
            CaseManagementService.update_case_status(case_id, "Resolved", resolution="")

        # 4. Hoàn tất xử lý có resolution -> Thành công
        CaseManagementService.update_case_status(
            case_id,
            "Resolved",
            resolution="Đã gọi điện hỏi thăm, đổi sang dòng sữa tắm dịu nhẹ không hương liệu cho lần tới."
        )
        resolved_case = frappe.get_doc("PetCare Case", case_id)
        self.assertEqual(resolved_case.status, "Resolved")
        self.assertIn("sữa tắm", resolved_case.resolution)
        self.assertIsNotNone(resolved_case.resolved_date)


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestServiceOperations)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)
