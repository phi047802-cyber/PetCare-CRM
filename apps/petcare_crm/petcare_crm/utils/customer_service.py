# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import re
from typing import Any, Dict, List, Optional
import frappe
from frappe.utils import nowdate, getdate
from frappe import _

from petcare_crm.utils.exceptions import (
    PetCareException,
    ValidationError,
    EntityNotFoundException,
)


class CustomerService:
    """Service layer for Customer (Contact), Multi-pet tracking and 360-degree interaction history."""

    @staticmethod
    def find_existing_customer(
        phone: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Tìm kiếm khách hàng hiện hữu theo tiêu chí duy nhất (Số điện thoại hoặc Email).
        TUYỆT ĐỐI KHÔNG TÌM / GỘP CHỈ BẰNG TÊN GIỐNG NHAU.
        """
        if phone:
            cleaned_phone = re.sub(r"[\s\-\.]", "", str(phone).strip())
            if cleaned_phone.startswith("+84"):
                cleaned_phone = "0" + cleaned_phone[3:]

            matched = frappe.db.get_value(
                "Contact",
                {"phone": cleaned_phone},
                ["name", "first_name", "last_name", "phone", "email_id"],
                as_dict=True
            ) or frappe.db.get_value(
                "Contact",
                {"mobile_no": cleaned_phone},
                ["name", "first_name", "last_name", "phone", "email_id"],
                as_dict=True
            )
            if matched:
                return matched

        if email and email.strip():
            matched = frappe.db.get_value(
                "Contact",
                {"email_id": email.strip()},
                ["name", "first_name", "last_name", "phone", "email_id"],
                as_dict=True
            )
            if matched:
                return matched

        return None

    @staticmethod
    def get_customer_360(contact_id: str) -> Dict[str, Any]:
        """
        Truy xuất hồ sơ 360 độ hợp nhất của khách hàng:
        - Thông tin liên lạc
        - Danh sách các thú cưng trực thuộc
        - Các gói hội viên đang sở hữu & số dư ví
        - Lịch sử các phiếu sử dụng dịch vụ (Service Visits)
        - Các cơ hội kinh doanh đang theo dõi (Opportunities)
        - Lịch sử trao đổi / cuộc gọi (Communications)
        """
        if not frappe.db.exists("Contact", contact_id):
            raise EntityNotFoundException(f"Không tìm thấy khách hàng với mã '{contact_id}'.")

        contact = frappe.get_doc("Contact", contact_id)

        # 1. Danh sách thú cưng
        pets = frappe.get_all(
            "Pet",
            filters={"customer": contact_id},
            fields=["name", "pet_name", "species", "breed", "birth_date", "weight_kg"]
        )

        # 2. Danh sách thẻ hội viên
        memberships = frappe.get_all(
            "Customer Membership",
            filters={"customer": contact_id},
            fields=["name", "membership_plan", "start_date", "end_date", "status", "balance", "pet"]
        )

        # 3. Lịch sử dịch vụ (Service Visits)
        visits = frappe.get_all(
            "Service Visit",
            filters={"customer": contact_id},
            fields=["name", "pet", "service_type", "visit_date", "original_price", "final_price"],
            order_by="visit_date desc"
        )

        # 4. Cơ hội bán hàng (Opportunities)
        opportunities = frappe.get_all(
            "PetCare Opportunity",
            filters={"customer": contact_id},
            fields=["name", "opportunity_title", "stage", "expected_amount", "probability", "sales_person"]
        )

        # 5. Lịch sử tương tác / cuộc gọi
        communications = frappe.get_all(
            "Communication",
            filters={"reference_doctype": "Contact", "reference_name": contact_id},
            fields=["name", "subject", "content", "communication_medium", "creation", "sender"],
            order_by="creation desc",
            limit=20
        )

        # 6. Yêu cầu hỗ trợ & Phản hồi sau dịch vụ (PetCare Cases)
        cases = []
        if frappe.db.exists("DocType", "PetCare Case"):
            cases = frappe.get_all(
                "PetCare Case",
                filters={"customer": contact_id},
                fields=["name", "subject", "case_type", "priority", "status", "pet", "creation", "resolution"],
                order_by="creation desc"
            )

        # 7. Đề xuất chăm sóc (Care Recommendations) cho các bé của chủ này
        pet_names = [p.name for p in pets]
        recommendations = []
        if pet_names and frappe.db.exists("DocType", "Care Recommendation"):
            recommendations = frappe.get_all(
                "Care Recommendation",
                filters={"customer": contact_id},
                fields=["name", "pet", "service_type", "pattern_status", "average_interval_days", "status", "due_date"],
                order_by="creation desc"
            )

        # Phân tách lịch sử dịch vụ theo từng Pet riêng biệt (Strict Pet Isolation)
        visits_by_pet = {p.name: [] for p in pets}
        for v in visits:
            if v.pet in visits_by_pet:
                visits_by_pet[v.pet].append(v)

        total_spent = sum(float(v.final_price or 0.0) for v in visits)

        return {
            "contact_id": contact.name,
            "full_name": f"{contact.first_name or ''} {contact.last_name or ''}".strip(),
            "phone": contact.phone or contact.mobile_no,
            "email": contact.email_id,
            "pets": pets,
            "pets_count": len(pets),
            "memberships": memberships,
            "service_visits": visits,
            "visits_by_pet": visits_by_pet,
            "visits_count": len(visits),
            "opportunities": opportunities,
            "communications": communications,
            "cases": cases,
            "cases_count": len(cases),
            "recommendations": recommendations,
            "total_spent": total_spent,
        }

    @staticmethod
    def create_followup_task(
        reference_doctype: str,
        reference_name: str,
        description: str,
        assigned_to: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: str = "Medium",
    ) -> str:
        """Tạo công việc theo dõi (ToDo) gắn với bản ghi CRM."""
        if not description or not description.strip():
            raise ValidationError("Mô tả công việc (description) không được để trống.")

        todo = frappe.get_doc({
            "doctype": "ToDo",
            "description": description.strip(),
            "reference_type": reference_doctype,
            "reference_name": reference_name,
            "allocated_to": assigned_to or (frappe.session.user if frappe.session.user else "Administrator"),
            "date": due_date or nowdate(),
            "priority": priority or "Medium",
            "status": "Open",
        })
        todo.insert(ignore_permissions=True)
        return todo.name

    @staticmethod
    def add_communication_log(
        reference_doctype: str,
        reference_name: str,
        subject: str,
        content: str,
        communication_medium: str = "Phone",
    ) -> str:
        """Ghi nhận lịch sử giao tiếp xuyên suốt vòng đời khách hàng."""
        if not content or not content.strip():
            raise ValidationError("Nội dung giao tiếp (content) không được để trống.")

        comm = frappe.get_doc({
            "doctype": "Communication",
            "communication_type": "Communication",
            "communication_medium": communication_medium or "Phone",
            "subject": subject or f"Ghi chú tương tác ({reference_doctype})",
            "content": content.strip(),
            "reference_doctype": reference_doctype,
            "reference_name": reference_name,
            "sender": frappe.session.user if frappe.session.user else "Administrator",
            "sent_or_received": "Sent",
            "status": "Linked",
        })
        comm.insert(ignore_permissions=True)
        return comm.name
