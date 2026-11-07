# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from frappe import _


class BenefitRedemptionLedger(Document):
    def validate(self):
        if not getattr(self, "redemption_time", None):
            self.redemption_time = now_datetime()

        if self.quantity_redeemed is None or int(self.quantity_redeemed) <= 0:
            frappe.throw(_("Số lượng cấn trừ (quantity_redeemed) phải lớn hơn 0."))

        if self.discount_applied is None or float(self.discount_applied) < 0:
            frappe.throw(_("Số tiền chiết khấu (discount_applied) không được âm."))

    def revert(self, reason: str = "Service Visit cancelled"):
        """Hoàn tác cấn trừ quyền lợi vào lại Thẻ hội viên (Audit trail an toàn)."""
        if self.status == "Reverted":
            frappe.throw(_("Bản ghi cấn trừ này đã được hoàn tác trước đó."))

        if self.membership and frappe.db.exists("Customer Membership", self.membership):
            # Khóa pessimistic row để tránh race condition
            ms_doc = frappe.get_doc("Customer Membership", self.membership, for_update=True)
            matched = False
            for b in ms_doc.benefits:
                if b.benefit_type and b.benefit_type.lower() == self.benefit_type.lower():
                    b.used_quantity = max(0, (b.used_quantity or 0) - int(self.quantity_redeemed or 1))
                    b.remaining_quantity = (b.total_quantity or 0) - b.used_quantity
                    matched = True
                    break

            if matched:
                ms_doc.save(ignore_permissions=True)

        self.status = "Reverted"
        self.reverted_time = now_datetime()
        self.reverted_reason = reason
        self.save(ignore_permissions=True)
