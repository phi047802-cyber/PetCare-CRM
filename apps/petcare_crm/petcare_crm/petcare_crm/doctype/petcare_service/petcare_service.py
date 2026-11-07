# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class PetCareService(Document):
    def validate(self):
        if self.service_code:
            self.service_code = str(self.service_code).strip().upper()
        if not self.service_name or not self.service_name.strip():
            frappe.throw(_("Tên dịch vụ (service_name) là bắt buộc."))
        if self.standard_price is None or float(self.standard_price) < 0:
            frappe.throw(_("Đơn giá tiêu chuẩn (standard_price) không được âm."))
        if self.default_cycle_days and int(self.default_cycle_days) <= 0:
            frappe.throw(_("Chu kỳ chăm sóc mặc định (default_cycle_days) phải lớn hơn 0."))
