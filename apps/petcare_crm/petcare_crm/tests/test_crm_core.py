# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import unittest
import frappe
from frappe.utils import nowdate, now_datetime

from petcare_crm.utils.lead_service import LeadManagementService, LeadConversionCoordinator
from petcare_crm.utils.sales_pipeline_service import SalesPipelineService
from petcare_crm.utils.customer_service import CustomerService
from petcare_crm.utils.exceptions import (
    ValidationError,
    EntityNotFoundException,
    InvalidStateTransitionException,
)


class TestCRMCore(unittest.TestCase):
    """
    Unit & Integration Tests for CRM Core:
    - Lead intake & lifecycle
    - Follow-up activities & interaction logging
    - Lead conversion with strict customer deduplication
    - Sales Pipeline & Opportunity stages
    - Customer 360 & multi-pet associations
    """

    def setUp(self):
        # Thiết lập dữ liệu định danh duy nhất cho từng test run
        self.timestamp = now_datetime().strftime("%Y%m%d%H%M%S%f")
        self.phone_test = f"0912{self.timestamp[-6:]}"
        self.email_test = f"lead_{self.timestamp}@petcare-test.vn"

    def tearDown(self):
        frappe.db.rollback()

    def test_01_create_lead_success_and_validation(self):
        """Kiểm tra tạo Lead hợp lệ và các ràng buộc validation backend."""
        # 1. Tạo Lead thành công
        lead_id = LeadManagementService.create_lead(
            lead_name="Nguyễn Văn An",
            phone=self.phone_test,
            lead_source="Hotline",
            email=self.email_test,
            initial_pet_info="Cún Corgi 2 tuổi cần tắm spa",
            priority="High",
        )
        self.assertTrue(lead_id.startswith("LEAD-"))

        lead_doc = frappe.get_doc("PetCare Lead", lead_id)
        self.assertEqual(lead_doc.status, "New")
        self.assertEqual(lead_doc.phone, self.phone_test)
        self.assertEqual(lead_doc.priority, "High")

        # 2. Validation: Thiếu tên -> Báo lỗi
        with self.assertRaises(ValidationError):
            LeadManagementService.create_lead(
                lead_name="",
                phone=self.phone_test,
                lead_source="Hotline"
            )

        # 3. Validation: Số điện thoại không hợp lệ -> Báo lỗi
        with self.assertRaises(ValidationError):
            LeadManagementService.create_lead(
                lead_name="Trần Thị B",
                phone="12345",  # quá ngắn, không đúng chuẩn VN
                lead_source="Facebook Ads"
            )

    def test_02_lead_status_transitions_and_owner_assignment(self):
        """Kiểm tra quy tắc chuyển dịch trạng thái và phân công phụ trách."""
        lead_id = LeadManagementService.create_lead(
            lead_name="Lê Thị Cẩm",
            phone=self.phone_test,
            lead_source="Zalo"
        )

        # Chuyển sang Contacted
        LeadManagementService.update_status(lead_id, "Contacted")
        self.assertEqual(frappe.db.get_value("PetCare Lead", lead_id, "status"), "Contacted")

        # Chuyển sang Qualified
        LeadManagementService.update_status(lead_id, "Qualified")
        self.assertEqual(frappe.db.get_value("PetCare Lead", lead_id, "status"), "Qualified")

        # Chuyển sang Unqualified mà thiếu lý do -> Báo lỗi
        with self.assertRaises(ValidationError):
            LeadManagementService.update_status(lead_id, "Unqualified", unqualified_reason="")

        # Chuyển sang Unqualified có lý do -> Thành công
        LeadManagementService.update_status(lead_id, "Unqualified", unqualified_reason="Khách ở quá xa chi nhánh")
        lead_doc = frappe.get_doc("PetCare Lead", lead_id)
        self.assertEqual(lead_doc.status, "Unqualified")
        self.assertEqual(lead_doc.unqualified_reason, "Khách ở quá xa chi nhánh")

        # Phân công người phụ trách
        LeadManagementService.assign_owner(lead_id, "Administrator")
        self.assertEqual(frappe.db.get_value("PetCare Lead", lead_id, "lead_owner"), "Administrator")

    def test_03_lead_interactions_and_communication_history(self):
        """Kiểm tra ghi nhận lịch sử trao đổi / cuộc gọi với Lead."""
        lead_id = LeadManagementService.create_lead(
            lead_name="Phạm Hoàng Dũng",
            phone=self.phone_test,
            lead_source="Website"
        )

        # Ghi nhận cuộc gọi đầu tiên và tự động đánh dấu Contacted
        comm_id = LeadManagementService.add_interaction(
            lead_id=lead_id,
            interaction_type="Phone Call",
            notes="Đã gọi điện tư vấn gói spa tắm sấy định kỳ cho bé cún Poodle.",
            set_contacted=True
        )
        self.assertTrue(bool(comm_id))
        self.assertEqual(frappe.db.get_value("PetCare Lead", lead_id, "status"), "Contacted")

        # Kiểm tra Communication record đã được tạo chính xác
        comm_doc = frappe.get_doc("Communication", comm_id)
        self.assertEqual(comm_doc.reference_doctype, "PetCare Lead")
        self.assertEqual(comm_doc.reference_name, lead_id)
        self.assertIn("Phone Call", comm_doc.subject)

    def test_04_lead_conversion_new_customer_and_preservation_of_history(self):
        """Kiểm tra chuyển đổi Lead thành Contact & Pet mới, bảo toàn lịch sử tương tác."""
        lead_id = LeadManagementService.create_lead(
            lead_name="Hoàng Thị Mai",
            phone=self.phone_test,
            lead_source="Facebook Ads",
            email=self.email_test,
            initial_pet_info="Bé Miu Miu mèo Anh lông ngắn"
        )

        # Ghi nhận trước 1 tương tác trên Lead
        LeadManagementService.add_interaction(
            lead_id=lead_id,
            interaction_type="Zalo Message",
            notes="Khách hỏi giá gói tiêm phòng và spa cho mèo con."
        )

        # Chuyển đổi Lead kèm tạo Cơ hội bán hàng
        result = LeadConversionCoordinator.convert_lead(
            lead_id=lead_id,
            pet_name="Miu Miu",
            species="Cat",
            breed="British Shorthair",
            create_opportunity=True,
            opportunity_amount=1500000.0
        )

        self.assertEqual(result["status"], "success")
        self.assertFalse(result["is_existing_customer"])
        contact_id = result["contact_id"]
        pet_id = result["pet_id"]
        opp_id = result["opportunity_id"]

        # Kiểm tra Contact đã tạo
        contact_doc = frappe.get_doc("Contact", contact_id)
        self.assertEqual(contact_doc.first_name, "Hoàng")
        self.assertEqual(contact_doc.last_name, "Thị Mai")
        self.assertEqual(contact_doc.phone, self.phone_test)

        # Kiểm tra Pet đã tạo liên kết đúng Contact
        pet_doc = frappe.get_doc("Pet", pet_id)
        self.assertEqual(pet_doc.customer, contact_id)
        self.assertEqual(pet_doc.species, "Cat")

        # Kiểm tra Opportunity đã tạo
        opp_doc = frappe.get_doc("PetCare Opportunity", opp_id)
        self.assertEqual(opp_doc.customer, contact_id)
        self.assertEqual(opp_doc.pet, pet_id)
        self.assertEqual(opp_doc.expected_amount, 1500000.0)

        # Kiểm tra Lead đã chuyển trạng thái Converted và khóa không sửa đổi
        lead_doc = frappe.get_doc("PetCare Lead", lead_id)
        self.assertEqual(lead_doc.status, "Converted")
        self.assertEqual(lead_doc.converted_contact, contact_id)

        # Kiểm tra bảo toàn lịch sử tương tác: Communication đã được sao chép sang Contact
        contact_comms = frappe.get_all(
            "Communication",
            filters={"reference_doctype": "Contact", "reference_name": contact_id}
        )
        self.assertGreaterEqual(len(contact_comms), 1)

        # Không cho phép chuyển đổi lại Lead đã Converted
        with self.assertRaises(InvalidStateTransitionException):
            LeadConversionCoordinator.convert_lead(lead_id=lead_id)

    def test_05_lead_conversion_linking_existing_customer_deduplication(self):
        """
        Kiểm tra chuyển đổi Lead khi khách hàng ĐÃ TỒN TẠI trong hệ thống (dựa theo Số điện thoại):
        - Không được tạo mới Contact trùng lặp!
        - Phải liên kết vào đúng Contact hiện hữu.
        """
        # Tạo trước một Contact với số điện thoại thử nghiệm
        existing_contact = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "Trần",
            "last_name": "Văn Khách Cũ",
            "phone": self.phone_test,
            "mobile_no": self.phone_test,
            "email_id": self.email_test,
        }).insert(ignore_permissions=True)

        # Tạo một Lead mới nhưng cùng số điện thoại (khách cũ quan tâm thêm dịch vụ mới)
        new_lead_id = LeadManagementService.create_lead(
            lead_name="Anh Trần Khách Quen",
            phone=self.phone_test,
            lead_source="Hotline",
            initial_pet_info="Bé Cún Mới Nhận Nuôi"
        )

        # Thực hiện chuyển đổi Lead
        result = LeadConversionCoordinator.convert_lead(
            lead_id=new_lead_id,
            pet_name=f"Bé Đậu Phộng_{self.timestamp[-4:]}",
            species="Dog",
            breed="Poodle"
        )

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["is_existing_customer"])
        # Phải trả về chính xác ID của Contact cũ, KHÔNG TẠO MỚI!
        self.assertEqual(result["contact_id"], existing_contact.name)

        # Kiểm tra Pet mới đã được gán quyền sở hữu cho Contact cũ
        pet_doc = frappe.get_doc("Pet", result["pet_id"])
        self.assertEqual(pet_doc.customer, existing_contact.name)

    def test_06_sales_pipeline_opportunity_lifecycle_and_rules(self):
        """Kiểm tra vòng đời cơ hội bán hàng, tính toán weighted_amount và quy tắc Closed Won / Closed Lost."""
        # Tạo Contact mẫu
        cust = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "Vũ",
            "last_name": "Đức Minh",
            "phone": self.phone_test,
        }).insert(ignore_permissions=True)

        # 1. Tạo Opportunity
        opp_id = SalesPipelineService.create_opportunity(
            title="Tư vấn Thẻ Hội Viên Vàng 1 Năm",
            customer=cust.name,
            expected_amount=5000000.0,
            stage="Prospecting",
            probability=20.0
        )
        opp_doc = frappe.get_doc("PetCare Opportunity", opp_id)
        self.assertEqual(opp_doc.weighted_amount, 1000000.0)  # 5,000,000 * 20%

        # 2. Cập nhật sang Proposal -> Xác suất tăng
        opp_doc.stage = "Proposal"
        opp_doc.probability = 60.0
        opp_doc.save(ignore_permissions=True)
        self.assertEqual(opp_doc.weighted_amount, 3000000.0)  # 5,000,000 * 60%

        # 3. Chuyển sang Closed Lost mà không có lý do -> Báo lỗi
        with self.assertRaises(ValidationError):
            SalesPipelineService.update_stage(opp_id, "Closed Lost", lost_reason="")

        # 4. Chuyển sang Closed Lost có lý do -> Xác suất tự động về 0, weighted_amount về 0
        SalesPipelineService.update_stage(opp_id, "Closed Lost", lost_reason="Price Too High", lost_notes="Khách chê giá cao")
        opp_lost = frappe.get_doc("PetCare Opportunity", opp_id)
        self.assertEqual(opp_lost.stage, "Closed Lost")
        self.assertEqual(opp_lost.probability, 0.0)
        self.assertEqual(opp_lost.weighted_amount, 0.0)

        # 5. Chuyển sang Closed Won -> Xác suất tự động lên 100%
        SalesPipelineService.update_stage(opp_id, "Closed Won")
        opp_won = frappe.get_doc("PetCare Opportunity", opp_id)
        self.assertEqual(opp_won.stage, "Closed Won")
        self.assertEqual(opp_won.probability, 100.0)
        self.assertEqual(opp_won.weighted_amount, 5000000.0)

    def test_07_customer_360_profile_and_followup_todo(self):
        """Kiểm tra tổng hợp hồ sơ khách hàng 360 độ và tạo việc cần làm (ToDo)."""
        cust = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "Đặng",
            "last_name": "Thị Tuyết",
            "phone": self.phone_test,
            "email_id": self.email_test,
        }).insert(ignore_permissions=True)

        # Thêm 2 thú cưng cho khách hàng này (Quan hệ 1-Nhiều)
        pet1 = frappe.get_doc({
            "doctype": "Pet",
            "pet_name": f"Bé Xù_{self.timestamp[-4:]}",
            "customer": cust.name,
            "species": "Dog"
        }).insert(ignore_permissions=True)

        pet2 = frappe.get_doc({
            "doctype": "Pet",
            "pet_name": f"Bé Mít_{self.timestamp[-4:]}",
            "customer": cust.name,
            "species": "Cat"
        }).insert(ignore_permissions=True)

        # Tạo việc cần làm (ToDo) follow-up
        todo_id = CustomerService.create_followup_task(
            reference_doctype="Contact",
            reference_name=cust.name,
            description="Gọi điện hỏi thăm sức khỏe bé Xù sau buổi spa",
            priority="High"
        )
        self.assertTrue(bool(todo_id))
        todo_doc = frappe.get_doc("ToDo", todo_id)
        self.assertEqual(todo_doc.reference_name, cust.name)

        # Lấy hồ sơ 360 độ
        c360 = CustomerService.get_customer_360(cust.name)
        self.assertEqual(c360["contact_id"], cust.name)
        self.assertEqual(c360["pets_count"], 2)
        pet_names = [p["name"] for p in c360["pets"]]
        self.assertIn(pet1.name, pet_names)
        self.assertIn(pet2.name, pet_names)


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCRMCore)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)
