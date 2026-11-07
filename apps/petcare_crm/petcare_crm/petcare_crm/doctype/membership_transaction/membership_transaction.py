import frappe
from frappe.model.document import Document


class MembershipTransaction(Document):
    def validate(self):
        if self.amount and float(self.amount) <= 0:
            frappe.throw("Số tiền giao dịch phải lớn hơn 0.")
