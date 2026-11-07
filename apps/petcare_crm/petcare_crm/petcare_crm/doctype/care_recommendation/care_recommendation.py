# Copyright (c) 2026, PetCare Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CareRecommendation(Document):
    def validate(self):
        """Validate Care Recommendation fields and statuses."""
        allowed_statuses = ["NEW", "ASSIGNED", "CONTACTED", "CONVERTED", "DISMISSED"]
        if getattr(self, "status", None) and self.status not in allowed_statuses:
            frappe.throw(_("Trạng thái khuyến nghị không hợp lệ: {0}").format(self.status))

        allowed_types = ["DUE_SOON", "AT_RISK", "RENEWAL"]
        if getattr(self, "recommendation_type", None) and self.recommendation_type not in allowed_types:
            frappe.throw(_("Loại khuyến nghị không hợp lệ: {0}").format(self.recommendation_type))

    def mark_contacted(self, notes: str = None):
        """Mark as contacted by care staff."""
        self.status = "CONTACTED"
        if notes:
            self.suggested_action = notes
        self.save()

    def mark_converted(self, notes: str = None):
        """Mark as successfully converted into a booking/service visit."""
        self.status = "CONVERTED"
        if notes:
            self.suggested_action = notes
        self.save()

    def dismiss(self, reason: str = None):
        """Dismiss this care recommendation."""
        self.status = "DISMISSED"
        if reason:
            self.suggested_action = reason
        self.save()
