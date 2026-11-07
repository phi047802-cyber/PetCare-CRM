# Copyright (c) 2026, PetCare Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class ServiceVisit(Document):
    def validate(self):
        # 1. Tự động đồng bộ customer từ Pet nếu chưa chọn hoặc customer không khớp Link Contact
        if self.pet:
            pet_customer = frappe.db.get_value("Pet", self.pet, "customer")
            if not self.customer or not frappe.db.exists("Contact", self.customer):
                self.customer = pet_customer
            elif pet_customer and pet_customer != self.customer:
                frappe.throw(_(f"Thú cưng '{self.pet}' thuộc sở hữu của '{pet_customer}', không khớp với '{self.customer}'."))

        # 2. Đồng bộ từ PetCare Service nếu có chọn
        if self.service and frappe.db.exists("PetCare Service", self.service):
            srv = frappe.get_cached_doc("PetCare Service", self.service)
            if not self.service_type:
                self.service_type = srv.service_name
            if self.original_price is None:
                self.original_price = srv.standard_price

        # 3. Tính toán Discount và Final Price
        orig = float(self.original_price or 0.0)
        if orig < 0:
            frappe.throw(_("Giá gốc (original_price) không được âm."))

        if self.final_price is None:
            disc = float(self.discount_amount or 0.0)
            self.final_price = max(0.0, orig - disc)
        else:
            self.final_price = float(self.final_price)
            if self.final_price < 0:
                frappe.throw(_("Giá thực thu (final_price) không được âm."))

        # Cập nhật discount_amount tự động
        self.discount_amount = max(0.0, orig - float(self.final_price))

        # 4. Cập nhật cân nặng mới của Pet nếu có nhập
        if getattr(self, "weight_kg", None) and float(self.weight_kg) > 0 and getattr(self, "pet", None):
            frappe.db.set_value("Pet", self.pet, "weight_kg", float(self.weight_kg))

        # 5. Tự động gán chi nhánh mặc định nếu chưa chọn
        if not getattr(self, "branch", None):
            self.branch = "CN-TRUNGTAM"

    def on_submit(self):
        """Khi nộp phiếu dịch vụ (docstatus=1): cập nhật trạng thái thành Completed."""
        if self.status != "Cancelled":
            self.status = "Completed"

    def on_cancel(self):
        """Khi phiếu dịch vụ bị hủy (docstatus=2): cập nhật trạng thái và tự động hoàn trả quyền lợi hội viên."""
        self.status = "Cancelled"
        self.revert_benefit_redemptions(reason=f"Phiếu dịch vụ {self.name} bị hủy bỏ (on_cancel)")

    def revert_benefit_redemptions(self, reason: str = "Hủy phiếu dịch vụ"):
        """Hoàn tác toàn bộ quyền lợi đã cấn trừ trong Service Visit này."""
        if not frappe.db.exists("DocType", "Benefit Redemption Ledger"):
            return

        ledgers = frappe.get_all(
            "Benefit Redemption Ledger",
            filters={"service_visit": self.name, "status": "Applied"},
            fields=["name"]
        )
        for row in ledgers:
            ledger_doc = frappe.get_doc("Benefit Redemption Ledger", row.name)
            ledger_doc.revert(reason=reason)

