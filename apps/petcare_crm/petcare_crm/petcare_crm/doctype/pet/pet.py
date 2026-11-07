# Copyright (c) 2026, PetCare Team and contributors
# For license information, please see license.txt

from typing import Any, Dict, List
import frappe
from frappe.model.document import Document
from frappe import _


class Pet(Document):
    def validate(self):
        if not self.pet_name or not self.pet_name.strip():
            frappe.throw(_("Tên thú cưng (pet_name) là bắt buộc."))
        self.pet_name = self.pet_name.strip()

        if not self.customer:
            frappe.throw(_("Chủ sở hữu (customer) là bắt buộc."))
        if not frappe.db.exists("Contact", self.customer):
            frappe.throw(_(f"Khách hàng '{self.customer}' không tồn tại trong hệ thống."))

        if self.weight_kg is not None and float(self.weight_kg) <= 0:
            frappe.throw(_("Cân nặng (weight_kg) phải lớn hơn 0."))

    def get_service_visits(self) -> List[Dict[str, Any]]:
        """
        Truy xuất danh sách các lần làm dịch vụ của RIÊNG thú cưng này.
        ĐẢM BẢO TUYỆT ĐỐI KHÔNG LẪN DỮ LIỆU CỦA PET KHÁC.
        """
        return frappe.get_all(
            "Service Visit",
            filters={"pet": self.name},
            fields=["name", "visit_date", "service_type", "original_price", "final_price", "membership", "benefit_used", "status"],
            order_by="visit_date asc"
        )
