# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import re
from typing import Any, Dict, Optional, Tuple
import frappe
from frappe.utils import now_datetime, getdate, nowdate
from frappe import _

from petcare_crm.utils.exceptions import (
    PetCareException,
    ValidationError,
    EntityNotFoundException,
    InvalidStateTransitionException,
)


class LeadManagementService:
    """Service layer for PetCare Lead lifecycle management and interactions."""

    @staticmethod
    def create_lead(
        lead_name: str,
        phone: str,
        lead_source: str,
        email: Optional[str] = None,
        initial_pet_info: Optional[str] = None,
        priority: str = "Medium",
        lead_owner: Optional[str] = None,
    ) -> str:
        """Tạo mới một khách hàng tiềm năng với validation đầy đủ."""
        if not lead_name or not lead_name.strip():
            raise ValidationError("Tên khách hàng tiềm năng (lead_name) là bắt buộc.")
        if not phone or not phone.strip():
            raise ValidationError("Số điện thoại (phone) là bắt buộc.")

        cleaned_phone = re.sub(r"[\s\-\.]", "", str(phone).strip())
        if cleaned_phone.startswith("+84"):
            cleaned_phone = "0" + cleaned_phone[3:]

        if not re.match(r"^0\d{8,10}$", cleaned_phone):
            raise ValidationError(
                f"Số điện thoại '{phone}' không hợp lệ. Vui lòng nhập số điện thoại Việt Nam hợp lệ (ví dụ: 0912345678)."
            )

        lead = frappe.get_doc({
            "doctype": "PetCare Lead",
            "lead_name": lead_name.strip(),
            "phone": cleaned_phone,
            "email": email.strip() if email else None,
            "lead_source": lead_source,
            "status": "New",
            "priority": priority or "Medium",
            "lead_owner": lead_owner or (frappe.session.user if frappe.session.user else "Administrator"),
            "initial_pet_info": initial_pet_info,
        })
        lead.insert(ignore_permissions=True)
        return lead.name

    @staticmethod
    def update_status(
        lead_id: str,
        new_status: str,
        unqualified_reason: Optional[str] = None,
    ) -> bool:
        """Cập nhật trạng thái Lead tuân thủ quy tắc chuyển dịch trạng thái."""
        if not frappe.db.exists("PetCare Lead", lead_id):
            raise EntityNotFoundException(f"Không tìm thấy Lead với mã '{lead_id}'.")

        lead = frappe.get_doc("PetCare Lead", lead_id)
        if lead.status == "Converted" and new_status != "Converted":
            raise InvalidStateTransitionException("Không thể chuyển đổi trạng thái của Lead đã hoàn tất chuyển đổi (Converted).")

        if new_status == "Unqualified" and not (unqualified_reason and unqualified_reason.strip()):
            raise ValidationError("Vui lòng nhập lý do không tiềm năng khi chuyển sang Unqualified.")

        lead.status = new_status
        if unqualified_reason:
            lead.unqualified_reason = unqualified_reason.strip()
        lead.save(ignore_permissions=True)
        return True

    @staticmethod
    def assign_owner(lead_id: str, new_owner: str) -> bool:
        """Phân công người phụ trách xử lý Lead."""
        if not frappe.db.exists("PetCare Lead", lead_id):
            raise EntityNotFoundException(f"Không tìm thấy Lead với mã '{lead_id}'.")
        if not frappe.db.exists("User", new_owner):
            raise EntityNotFoundException(f"Người dùng '{new_owner}' không tồn tại trong hệ thống.")

        frappe.db.set_value("PetCare Lead", lead_id, "lead_owner", new_owner)
        return True

    @staticmethod
    def add_interaction(
        lead_id: str,
        interaction_type: str,
        notes: str,
        set_contacted: bool = False,
    ) -> str:
        """Ghi nhận lịch sử tương tác cuộc gọi/tin nhắn với Lead."""
        if not frappe.db.exists("PetCare Lead", lead_id):
            raise EntityNotFoundException(f"Không tìm thấy Lead với mã '{lead_id}'.")
        if not notes or not notes.strip():
            raise ValidationError("Nội dung ghi chú tương tác không được để trống.")

        lead = frappe.get_doc("PetCare Lead", lead_id)

        # Thêm comment vào timeline của Lead
        comment = lead.add_comment(
            "Comment",
            text=f"<b>[{interaction_type}]</b>: {notes.strip()}"
        )

        # Tạo Communication record chính quy của Frappe để lưu vết
        comm = frappe.get_doc({
            "doctype": "Communication",
            "communication_type": "Communication",
            "communication_medium": "Phone" if "Phone" in interaction_type else "Other",
            "subject": f"Tương tác với Lead: {lead.lead_name} ({interaction_type})",
            "content": notes.strip(),
            "reference_doctype": "PetCare Lead",
            "reference_name": lead_id,
            "sender": frappe.session.user if frappe.session.user else "Administrator",
            "sent_or_received": "Sent",
            "status": "Linked",
        })
        comm.insert(ignore_permissions=True)

        if set_contacted and lead.status == "New":
            lead.status = "Contacted"
            lead.save(ignore_permissions=True)

        return comm.name


class LeadConversionCoordinator:
    """
    Use Case Coordinator: Chuyển đổi Lead thành Khách hàng (Contact), Thú cưng (Pet) và Deal (Opportunity).
    Tuân thủ kiểm tra trùng lặp thông minh theo số điện thoại / email, bảo toàn 100% lịch sử tương tác.
    """

    @staticmethod
    def convert_lead(
        lead_id: str,
        pet_name: Optional[str] = None,
        species: str = "Dog",
        breed: Optional[str] = None,
        create_opportunity: bool = False,
        opportunity_amount: float = 0.0,
    ) -> Dict[str, Any]:
        if not frappe.db.exists("PetCare Lead", lead_id):
            raise EntityNotFoundException(f"Không tìm thấy Lead với mã '{lead_id}'.")

        lead = frappe.get_doc("PetCare Lead", lead_id)
        if lead.status == "Converted":
            raise InvalidStateTransitionException(f"Lead '{lead_id}' đã được chuyển đổi trước đó.")

        # Khởi động Transaction an toàn
        try:
            # 1. Kiểm tra trùng lặp khách hàng (Contact) theo tiêu chí nghiêm ngặt (Số điện thoại / Email)
            # TUYỆT ĐỐI KHÔNG GỘP CHỈ VÌ TÊN GIỐNG NHAU
            existing_contact = None
            if lead.phone:
                existing_contact = frappe.db.get_value(
                    "Contact",
                    {"phone": lead.phone},
                    "name"
                ) or frappe.db.get_value(
                    "Contact",
                    {"mobile_no": lead.phone},
                    "name"
                )

            if not existing_contact and lead.email:
                existing_contact = frappe.db.get_value(
                    "Contact",
                    {"email_id": lead.email},
                    "name"
                )

            if existing_contact:
                contact_name = existing_contact
                is_existing_customer = True
            else:
                # Tạo Contact mới
                name_parts = lead.lead_name.strip().split(" ", 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ""

                contact_doc = frappe.get_doc({
                    "doctype": "Contact",
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": lead.phone,
                    "mobile_no": lead.phone,
                    "email_id": lead.email if lead.email else None,
                    "is_primary_contact": 1,
                })
                contact_doc.insert(ignore_permissions=True)
                contact_name = contact_doc.name
                is_existing_customer = False

            # 2. Xử lý Thú cưng (Pet) nếu có thông tin
            pet_doc_name = None
            p_name = pet_name.strip() if pet_name else None
            if not p_name and lead.initial_pet_info:
                p_name = lead.initial_pet_info.strip().split("\n")[0][:30]

            if p_name:
                # Kiểm tra xem khách này đã có thú cưng tên này chưa
                existing_pet = frappe.db.get_value("Pet", {"pet_name": p_name, "customer": contact_name}, "name")
                if existing_pet:
                    pet_doc_name = existing_pet
                else:
                    pet_doc = frappe.get_doc({
                        "doctype": "Pet",
                        "pet_name": p_name,
                        "customer": contact_name,
                        "species": species or "Dog",
                        "breed": breed.strip() if breed else None,
                        "notes": f"Khởi tạo từ chuyển đổi Lead {lead_id}",
                    })
                    pet_doc.insert(ignore_permissions=True)
                    pet_doc_name = pet_doc.name

            # 3. Tạo Cơ hội bán hàng (PetCare Opportunity) nếu được yêu cầu
            opp_name = None
            if create_opportunity:
                opp_doc = frappe.get_doc({
                    "doctype": "PetCare Opportunity",
                    "opportunity_title": f"Cơ hội từ Lead: {lead.lead_name}",
                    "customer": contact_name,
                    "pet": pet_doc_name,
                    "stage": "Prospecting",
                    "expected_amount": float(opportunity_amount or 0.0),
                    "probability": 20.0,
                    "sales_person": lead.lead_owner or frappe.session.user,
                    "source_lead": lead_id,
                })
                opp_doc.insert(ignore_permissions=True)
                opp_name = opp_doc.name

            # 4. Bảo toàn lịch sử hoạt động: Chuyển giao / sao chép Communication sang Contact
            lead_comms = frappe.get_all(
                "Communication",
                filters={"reference_doctype": "PetCare Lead", "reference_name": lead_id},
                fields=["name", "subject", "content", "communication_medium", "sender"]
            )
            for c in lead_comms:
                frappe.get_doc({
                    "doctype": "Communication",
                    "communication_type": "Communication",
                    "communication_medium": c.communication_medium or "Other",
                    "subject": f"[Từ Lead {lead_id}] {c.subject}",
                    "content": c.content,
                    "reference_doctype": "Contact",
                    "reference_name": contact_name,
                    "sender": c.sender,
                    "sent_or_received": "Sent",
                    "status": "Linked",
                }).insert(ignore_permissions=True)

            # 5. Cập nhật trạng thái của Lead sang Converted
            lead.status = "Converted"
            lead.converted_contact = contact_name
            lead.converted_pet = pet_doc_name
            lead.converted_opportunity = opp_name
            lead.converted_date = now_datetime()
            lead.save(ignore_permissions=True)

            frappe.db.commit()

            return {
                "status": "success",
                "lead_id": lead_id,
                "contact_id": contact_name,
                "is_existing_customer": is_existing_customer,
                "pet_id": pet_doc_name,
                "opportunity_id": opp_name,
                "message": "Chuyển đổi Lead thành công.",
            }

        except Exception as e:
            frappe.db.rollback()
            raise e
