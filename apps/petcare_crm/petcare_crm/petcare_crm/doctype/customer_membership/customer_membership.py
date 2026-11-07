import frappe
from frappe.model.document import Document
from datetime import date, datetime


class CustomerMembership(Document):
    def validate(self):
        # Validate ngày hiệu lực
        if self.start_date and self.end_date:
            s_date = self.start_date if isinstance(self.start_date, date) else datetime.strptime(str(self.start_date)[:10], "%Y-%m-%d").date()
            e_date = self.end_date if isinstance(self.end_date, date) else datetime.strptime(str(self.end_date)[:10], "%Y-%m-%d").date()
            if e_date < s_date:
                frappe.throw("Ngày kết thúc (End Date) không được nhỏ hơn ngày bắt đầu (Start Date).")

        # Tính lại remaining_quantity cho tất cả benefits
        for b in self.benefits:
            b.remaining_quantity = (b.total_quantity or 0) - (b.used_quantity or 0)
            if b.remaining_quantity < 0:
                frappe.throw(
                    f"Benefit '{b.benefit_type}': used ({b.used_quantity}) "
                    f"vượt total ({b.total_quantity}). Vui lòng kiểm tra lại."
                )

        # Auto-expire nếu quá end_date
        if self.status == "Active" and self.end_date:
            if isinstance(self.end_date, str):
                end = datetime.strptime(str(self.end_date)[:10], "%Y-%m-%d").date()
            else:
                end = self.end_date
            if end < date.today():
                self.status = "Expired"
        # Validate balance không âm
        if hasattr(self, 'balance') and self.balance and float(self.balance) < 0:
            frappe.throw('Số dư tài khoản không được âm.')

