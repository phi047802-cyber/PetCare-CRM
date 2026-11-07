# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class PetCareOpportunity(Document):
    def validate(self):
        self._validate_amounts()
        self._validate_stage_and_probability()
        self._validate_pet_ownership()
        self._set_defaults()

    def _validate_amounts(self):
        if self.expected_amount is None or float(self.expected_amount) < 0:
            frappe.throw(_("Giá trị cơ hội (expected_amount) không được âm."))

    def _validate_stage_and_probability(self):
        if self.stage == "Closed Won":
            self.probability = 100.0
        elif self.stage == "Closed Lost":
            self.probability = 0.0
            if not self.lost_reason:
                frappe.throw(_("Vui lòng chọn lý do thất bại (lost_reason) khi chuyển cơ hội sang Closed Lost."))
        else:
            # Giai đoạn đang thương lượng, xác suất từ 0 đến 100%
            prob = float(self.probability or 20)
            if prob < 0 or prob > 100:
                frappe.throw(_("Xác suất thành công phải nằm trong khoảng từ 0% đến 100%."))
            self.probability = prob

        # Tính toán giá trị kỳ vọng có trọng số
        self.weighted_amount = float(self.expected_amount or 0) * (float(self.probability) / 100.0)

    def _validate_pet_ownership(self):
        if self.pet:
            pet_owner = frappe.db.get_value("Pet", self.pet, "customer")
            if pet_owner and pet_owner != self.customer:
                frappe.throw(_(f"Thú cưng '{self.pet}' không thuộc về khách hàng '{self.customer}'."))

    def _set_defaults(self):
        if not self.sales_person:
            self.sales_person = frappe.session.user if frappe.session.user else "Administrator"
