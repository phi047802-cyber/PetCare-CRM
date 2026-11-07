# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

from typing import Any, Dict, List, Optional
import frappe
from frappe import _

from petcare_crm.utils.exceptions import (
    PetCareException,
    ValidationError,
    EntityNotFoundException,
)


class SalesPipelineService:
    """Service layer for PetCare Sales Pipeline & Opportunity management."""

    @staticmethod
    def create_opportunity(
        title: str,
        customer: str,
        expected_amount: float,
        stage: str = "Prospecting",
        pet: Optional[str] = None,
        probability: float = 20.0,
        sales_person: Optional[str] = None,
        expected_closing: Optional[str] = None,
        source_lead: Optional[str] = None,
    ) -> str:
        """Tạo cơ hội bán hàng với validation chặt chẽ."""
        if not title or not title.strip():
            raise ValidationError("Tiêu đề cơ hội (title) không được để trống.")
        if not customer:
            raise ValidationError("Khách hàng (customer) là bắt buộc.")
        if not frappe.db.exists("Contact", customer):
            raise EntityNotFoundException(f"Khách hàng '{customer}' không tồn tại trong hệ thống.")

        if expected_amount is None or float(expected_amount) < 0:
            raise ValidationError("Giá trị cơ hội (expected_amount) không được âm.")

        if pet:
            pet_owner = frappe.db.get_value("Pet", pet, "customer")
            if pet_owner and pet_owner != customer:
                raise ValidationError(f"Thú cưng '{pet}' không thuộc quyền sở hữu của khách hàng '{customer}'.")

        opp = frappe.get_doc({
            "doctype": "PetCare Opportunity",
            "opportunity_title": title.strip(),
            "customer": customer,
            "pet": pet,
            "stage": stage or "Prospecting",
            "expected_amount": float(expected_amount),
            "probability": float(probability or 20.0),
            "sales_person": sales_person or (frappe.session.user if frappe.session.user else "Administrator"),
            "expected_closing": expected_closing,
            "source_lead": source_lead,
        })
        opp.insert(ignore_permissions=True)
        return opp.name

    @staticmethod
    def update_stage(
        opp_id: str,
        new_stage: str,
        lost_reason: Optional[str] = None,
        lost_notes: Optional[str] = None,
    ) -> bool:
        """Cập nhật giai đoạn cơ hội bán hàng (Prospecting -> Closed Won / Closed Lost)."""
        if not frappe.db.exists("PetCare Opportunity", opp_id):
            raise EntityNotFoundException(f"Không tìm thấy Cơ hội bán hàng với mã '{opp_id}'.")

        opp = frappe.get_doc("PetCare Opportunity", opp_id)

        if new_stage == "Closed Lost":
            if not lost_reason:
                raise ValidationError("Vui lòng chọn lý do thất bại (lost_reason) khi chuyển sang Closed Lost.")
            opp.lost_reason = lost_reason
            opp.lost_notes = lost_notes.strip() if lost_notes else None

        opp.stage = new_stage
        opp.save(ignore_permissions=True)
        return True

    @staticmethod
    def get_pipeline_summary() -> Dict[str, Any]:
        """Tổng hợp số liệu phễu bán hàng theo từng giai đoạn thời gian thực."""
        stages = ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
        summary = {s: {"count": 0, "total_value": 0.0, "weighted_value": 0.0} for s in stages}

        opportunities = frappe.get_all(
            "PetCare Opportunity",
            fields=["stage", "expected_amount", "weighted_amount"]
        )

        for opp in opportunities:
            st = opp.stage
            if st in summary:
                summary[st]["count"] += 1
                summary[st]["total_value"] += float(opp.expected_amount or 0.0)
                summary[st]["weighted_value"] += float(opp.weighted_amount or 0.0)

        total_active_pipeline = sum(
            summary[s]["total_value"] for s in ["Prospecting", "Qualification", "Proposal", "Negotiation"]
        )
        total_won = summary["Closed Won"]["total_value"]

        return {
            "by_stage": summary,
            "total_active_pipeline_value": total_active_pipeline,
            "total_won_value": total_won,
            "total_deals": len(opportunities),
        }
