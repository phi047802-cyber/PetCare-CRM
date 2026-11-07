# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import re
import frappe
from frappe.model.document import Document
from frappe import _


class PetCareLead(Document):
    def validate(self):
        self._validate_phone()
        self._validate_state_transitions()
        self._set_defaults()

    def _validate_phone(self):
        if not self.phone:
            frappe.throw(_("Số điện thoại là bắt buộc."))
        
        # Chuẩn hóa số điện thoại: loại bỏ dấu cách, dấu gạch nối, dấu chấm
        cleaned_phone = re.sub(r"[\s\-\.]", "", str(self.phone).strip())
        if cleaned_phone.startswith("+84"):
            cleaned_phone = "0" + cleaned_phone[3:]
        
        # Kiểm tra chỉ chứa chữ số và có độ dài hợp lệ (9 - 11 số)
        if not re.match(r"^0\d{8,10}$", cleaned_phone):
            frappe.throw(_(f"Số điện thoại '{self.phone}' không hợp lệ. Vui lòng nhập số điện thoại Việt Nam hợp lệ (ví dụ: 0912345678)."))
        
        self.phone = cleaned_phone

    def _validate_state_transitions(self):
        # Nếu chuyển sang Unqualified, bắt buộc phải có unqualified_reason
        if self.status == "Unqualified" and not (self.unqualified_reason and self.unqualified_reason.strip()):
            frappe.throw(_("Vui lòng nhập lý do không tiềm năng (unqualified_reason) khi chuyển trạng thái sang Unqualified."))

        # Nếu Lead đã Converted trong CSDL, không cho phép sửa đổi hoặc chuyển ngược trạng thái
        if not self.is_new():
            old_status = frappe.db.get_value("PetCare Lead", self.name, "status")
            if old_status == "Converted" and self.status != "Converted":
                frappe.throw(_("Không thể thay đổi trạng thái của Lead đã được chuyển đổi (Converted)."))

    def _set_defaults(self):
        if not self.lead_owner:
            self.lead_owner = frappe.session.user if frappe.session.user else "Administrator"
        if not self.priority:
            self.priority = "Medium"
