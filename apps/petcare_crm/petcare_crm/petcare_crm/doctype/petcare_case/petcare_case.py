# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from frappe import _


class PetCareCase(Document):
    def validate(self):
        self._validate_customer_pet()
        self._validate_lifecycle()
        self._set_defaults()

    def _validate_customer_pet(self):
        if not self.customer:
            frappe.throw(_("Khách hàng (customer) là bắt buộc."))
        if self.pet:
            pet_owner = frappe.db.get_value("Pet", self.pet, "customer")
            if pet_owner and pet_owner != self.customer:
                frappe.throw(_(f"Thú cưng '{self.pet}' không thuộc quyền sở hữu của khách hàng '{self.customer}'."))

    def _validate_lifecycle(self):
        if getattr(self, "status", None) in ["Resolved", "Closed"]:
            res = getattr(self, "resolution", None)
            if not res or not str(res).strip():
                frappe.throw(_("Vui lòng nhập phương án xử lý (resolution) trước khi hoàn tất Case."))
            if not getattr(self, "resolved_date", None):
                self.resolved_date = now_datetime()

    def _set_defaults(self):
        if not getattr(self, "assigned_to", None):
            self.assigned_to = frappe.session.user if frappe.session.user else "Administrator"
