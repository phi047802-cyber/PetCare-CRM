# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class WooCommerceOrderSync(Document):
    def validate(self):
        if not self.external_order_key:
            frappe.throw(_("External Order Key là bắt buộc."))
        if not self.woocommerce_order_id:
            frappe.throw(_("WooCommerce Order ID là bắt buộc."))
        if float(self.order_total or 0) < 0:
            frappe.throw(_("Tổng tiền đơn hàng không được âm."))

