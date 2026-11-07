# Copyright (c) 2026, PetCare Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class PetCareAppointment(Document):
    def validate(self):
        # 1. Kiem tra khach hang
        if not self.customer:
            frappe.throw(_("Khách hàng (customer) là bắt buộc."))
        if hasattr(frappe, "db") and frappe.db and hasattr(frappe.db, "exists"):
            if not frappe.db.exists("Contact", self.customer):
                frappe.throw(_(f"Khách hàng '{self.customer}' không tồn tại."))

        # 2. Kiem tra thu cung va quyen so huu
        if not self.pet:
            frappe.throw(_("Thú cưng (pet) là bắt buộc."))
        if hasattr(frappe, "db") and frappe.db and hasattr(frappe.db, "get_value"):
            pet_cust = frappe.db.get_value("Pet", self.pet, "customer")
            if pet_cust and pet_cust != self.customer:
                frappe.throw(_(f"Thú cưng '{self.pet}' thuộc sở hữu của '{pet_cust}', không khớp với '{self.customer}'."))

        # 3. Kiem tra ngay gio
        if not self.appointment_date:
            frappe.throw(_("Ngày hẹn (appointment_date) là bắt buộc."))

        # 4. Chi nhanh mac dinh
        if not self.branch:
            self.branch = "CN-TRUNGTAM"

        # 5. Trang thai mac dinh
        if not self.status:
            self.status = "Scheduled"

    def check_in(self, technician: str = None) -> str:
        """
        Nghiep vu Check-in tai quay Le Tan:
        - Chuyen trang thai sang Checked-In.
        - Tu dong khoi tao phieu Service Visit de bac si/ky thuat vien thuc hien.
        """
        if self.status in ["Completed", "Cancelled"]:
            frappe.throw(_(f"Không thể check-in lịch hẹn đã ở trạng thái {self.status}."))

        self.status = "Checked-In"
        if technician:
            self.assigned_staff = technician

        # Tu dong tao phieu Service Visit neu chua co
        visit_name = getattr(self, "linked_service_visit", None)
        if not visit_name and hasattr(frappe, "get_doc"):
            try:
                visit_doc = frappe.get_doc({
                    "doctype": "Service Visit",
                    "customer": self.customer,
                    "pet": self.pet,
                    "service_type": self.service_type or "General",
                    "service": self.service,
                    "visit_date": self.appointment_date,
                    "branch": self.branch or "CN-TRUNGTAM",
                    "technician": self.assigned_staff or technician,
                    "status": "In Progress",
                    "notes": f"Khởi tạo từ lịch hẹn {self.name}. {self.notes or ''}",
                })
                visit_doc.insert(ignore_permissions=True)
                self.linked_service_visit = visit_doc.name
                visit_name = visit_doc.name
            except Exception:
                pass

        self.save(ignore_permissions=True)
        return visit_name

    def cancel_appointment(self, reason: str = None):
        """Huy lich hen co luu ly do."""
        if self.status == "Completed":
            frappe.throw(_("Không thể hủy lịch hẹn đã hoàn thành dịch vụ."))
        self.status = "Cancelled"
        if reason:
            self.cancellation_reason = reason
        self.save(ignore_permissions=True)
