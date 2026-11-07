"""
Care Recommendation Engine & Retention Service (CRM 2.0).
Coordinates Care Pattern Intelligence and Customer Loyalty/Membership.
Supports:
- Rule-based recommendation generation for Due Soon and At Risk
- Membership benefit context enrichment (without hard dependency on membership)
- Deduplication and in-place updating of active recommendations (no duplicate records)
- Full lifecycle status transitions (NEW -> CONTACTED -> CONVERTED / DISMISSED)
"""

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from petcare_crm.utils.care_pattern_service import (
    CarePatternAnalyzer,
    RiskDetectionService,
    VisitPredictionService,
    _extract_date,
    _get_field,
)
from petcare_crm.utils.config import (
    RECOMMENDATION_ASSIGNED,
    RECOMMENDATION_CONTACTED,
    RECOMMENDATION_CONVERTED,
    RECOMMENDATION_DEDUP_WINDOW_DAYS,
    RECOMMENDATION_DISMISSED,
    RECOMMENDATION_NEW,
    RECOMMENDATION_TYPE_AT_RISK,
    RECOMMENDATION_TYPE_DUE_SOON,
)
from petcare_crm.utils.membership_service import MembershipService
from petcare_crm.utils.models import CareRecommendationDTO


def _get_val(obj: Any, key: str, default: Any = None) -> Any:
    return _get_field(obj, key, default)


def _set_val(obj: Any, key: str, value: Any) -> None:
    if isinstance(obj, dict):
        obj[key] = value
    elif hasattr(obj, key):
        setattr(obj, key, value)


class CareRecommendationCoordinator:
    """
    Coordinates evaluation, generation, deduplication, and updating of care recommendations.
    """

    ACTIVE_STATUSES = {
        RECOMMENDATION_NEW,
        RECOMMENDATION_ASSIGNED,
        RECOMMENDATION_CONTACTED,
    }

    TERMINAL_STATUSES = {
        RECOMMENDATION_CONVERTED,
        RECOMMENDATION_DISMISSED,
        "COMPLETED",
        "CANCELLED",
    }

    @classmethod
    def find_active_recommendation(
        cls,
        pet_identifier: str,
        service_type: str,
        existing_recs: List[Any],
        customer_identifier: Optional[str] = None,
    ) -> Optional[Any]:
        """
        Locates an existing active recommendation for (Pet, Service Type).
        """
        pet_str = str(pet_identifier).strip().lower()
        service_str = str(service_type).strip().lower()
        cust_str = str(customer_identifier).strip().lower() if customer_identifier else None

        for rec in existing_recs:
            r_pet = str(_get_val(rec, "pet") or "").strip().lower()
            r_service = str(_get_val(rec, "service_type") or "").strip().lower()
            r_status = str(_get_val(rec, "status") or "").strip().upper()
            r_cust = str(_get_val(rec, "customer") or "").strip().lower()

            if r_pet == pet_str and r_service == service_str and r_status in cls.ACTIVE_STATUSES:
                if cust_str and r_cust and r_cust != cust_str:
                    continue
                return rec
        return None

    @classmethod
    def build_recommendation_context(
        cls,
        pet: Any,
        customer: Any,
        service_type: str,
        visits: List[Any],
        current_date: Optional[date] = None,
        memberships: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """
        Synthesizes Pattern Analytics, Risk Evaluation, and Membership status into a single diagnostic context.
        """
        if current_date is None:
            current_date = date.today()
        else:
            current_date = _extract_date(current_date) or date.today()

        if memberships is None:
            memberships = []

        pet_id = str(_get_val(pet, "name") or _get_val(pet, "pet_name") or pet)
        pet_name = str(_get_val(pet, "pet_name") or _get_val(pet, "name") or pet)
        cust_id = str(_get_val(customer, "name") or customer)
        cust_name = str(_get_val(customer, "customer_name") or _get_val(customer, "name") or customer)

        # Risk evaluations
        due_soon_info = RiskDetectionService.detect_due_soon(
            pet=pet_id,
            service_type=service_type,
            visits=visits,
            current_date=current_date,
        )
        at_risk_info = RiskDetectionService.detect_at_risk(
            pet=pet_id,
            service_type=service_type,
            visits=visits,
            current_date=current_date,
        )

        # Membership context (if any)
        active_membership = MembershipService.get_active_membership(
            customer=cust_id,
            pet=pet_id,
            check_date=current_date,
            memberships_store=memberships,
        )

        remaining_benefit = None
        if active_membership:
            remaining_benefit = MembershipService.get_remaining_benefit(
                membership=active_membership,
                service_type=service_type,
            )

        return {
            "pet_id": pet_id,
            "pet_name": pet_name,
            "customer_id": cust_id,
            "customer_name": cust_name,
            "service_type": service_type,
            "current_date": current_date,
            "due_soon": due_soon_info,
            "at_risk": at_risk_info,
            "active_membership": active_membership,
            "remaining_benefit": remaining_benefit,
        }

    @classmethod
    def evaluate_and_upsert_recommendation(
        cls,
        pet: Any,
        customer: Any,
        service_type: str,
        visits: List[Any],
        current_date: Optional[date] = None,
        memberships: Optional[List[Any]] = None,
        existing_recs: Optional[List[Any]] = None,
        store: Optional[List[Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Main recommendation engine method:
        - Evaluates Due Soon and At Risk
        - Generates human-readable Vietnamese explanation
        - Enriches with Membership benefits if available (without forcing membership)
        - Updates existing active recommendation in-place or creates a new one
        - Avoids duplicate records
        Returns dict or None.
        """
        if current_date is None:
            current_date = date.today()
        else:
            current_date = _extract_date(current_date) or date.today()

        if existing_recs is None:
            existing_recs = []

        context = cls.build_recommendation_context(
            pet=pet,
            customer=customer,
            service_type=service_type,
            visits=visits,
            current_date=current_date,
            memberships=memberships,
        )

        due_soon = context["due_soon"]
        at_risk = context["at_risk"]
        membership = context["active_membership"]
        benefit = context["remaining_benefit"]
        pet_name = context["pet_name"]
        pet_id = context["pet_id"]
        cust_name = context["customer_name"]
        cust_id = context["customer_id"]

        # Determine Recommendation Type & Priority
        rec_type = None
        priority = "Medium"
        reason = ""
        suggested_action = ""

        # Membership context additions
        ms_name = _get_val(membership, "name") if membership else None
        ms_plan = (_get_val(membership, "membership_plan") or "") if membership else ""
        is_vip = bool(membership and any(k in ms_plan.upper() for k in ("VIP", "PLUS", "DIAMOND", "GOLD")))
        vip_tag = "[⭐ KHÁCH HÀNG VIP] " if is_vip else ""

        benefit_qty = _get_val(benefit, "remaining_quantity", 0) if benefit else 0
        benefit_text = ""
        if benefit and benefit_qty > 0:
            benefit_text = f" Khách hàng còn {benefit_qty} lượt {service_type} miễn phí/ưu đãi chưa dùng."
            priority = "High"

        # Check conditions
        if due_soon.is_due_soon:
            rec_type = RECOMMENDATION_TYPE_DUE_SOON
            days_left = due_soon.days_until_due
            pred_date_str = str(due_soon.predicted_date)
            reason = (
                f"{vip_tag}Pet '{pet_name}' sắp đến chu kỳ {service_type} "
                f"(còn {days_left} ngày tới ngày dự kiến {pred_date_str}).{benefit_text}"
            )
            suggested_action = f"Liên hệ khách hàng '{cust_name}' đặt lịch chăm sóc {service_type} trong {days_left} ngày tới."
        elif at_risk.is_at_risk:
            rec_type = RECOMMENDATION_TYPE_AT_RISK
            priority = "High"
            ratio = at_risk.absence_ratio
            days_absent = at_risk.days_since_last_visit
            reason = (
                f"{vip_tag}Pet '{pet_name}' đã quá chu kỳ chăm sóc {service_type} "
                f"({days_absent} ngày chưa quay lại, tỷ lệ vắng mặt {ratio:.2f}x).{benefit_text}"
            )
            suggested_action = f"Gửi tin nhắn/gọi điện chăm sóc win-back khách hàng '{cust_name}' cho dịch vụ {service_type}."
        else:
            return None

        # Check for existing active recommendation
        active_rec = cls.find_active_recommendation(
            pet_identifier=pet_id,
            service_type=service_type,
            existing_recs=existing_recs,
            customer_identifier=cust_id,
        )

        if active_rec is not None:
            # UPDATE in-place instead of creating duplicate
            _set_val(active_rec, "recommendation_date", current_date)
            _set_val(active_rec, "recommendation_type", rec_type)
            _set_val(active_rec, "priority", priority)
            _set_val(active_rec, "reason", reason)
            _set_val(active_rec, "suggested_action", suggested_action)
            if ms_name:
                _set_val(active_rec, "membership", ms_name)
            _set_val(active_rec, "action_taken", "UPDATED")

            if isinstance(active_rec, dict):
                return active_rec
            return {
                "name": _get_val(active_rec, "name"),
                "customer": cust_id,
                "pet": pet_id,
                "service_type": service_type,
                "recommendation_type": rec_type,
                "recommendation_date": current_date,
                "priority": priority,
                "reason": reason,
                "suggested_action": suggested_action,
                "status": _get_val(active_rec, "status"),
                "membership": ms_name,
                "action_taken": "UPDATED",
            }

        # CREATE NEW
        new_rec = {
            "customer": cust_id,
            "pet": pet_id,
            "service_type": service_type,
            "recommendation_type": rec_type,
            "recommendation_date": current_date,
            "priority": priority,
            "reason": reason,
            "suggested_action": suggested_action,
            "status": RECOMMENDATION_NEW,
            "membership": ms_name,
            "action_taken": "CREATED",
        }

        if store is not None:
            store.append(new_rec)
        if existing_recs is not None and new_rec not in existing_recs:
            existing_recs.append(new_rec)

        return new_rec

    @classmethod
    def mark_status(
        cls,
        recommendation: Any,
        status: str,
        notes: Optional[str] = None,
    ) -> Any:
        """Transitions status of a recommendation."""
        _set_val(recommendation, "status", status)
        if notes:
            _set_val(recommendation, "suggested_action", notes)
        return recommendation


class RecommendationService(CareRecommendationCoordinator):
    """
    Unified facade class for backward compatibility.
    """

    @classmethod
    def generate_care_recommendation(
        cls,
        pet: Any,
        customer: Any,
        service_type: str,
        visits: List[Any],
        current_date: Optional[date] = None,
        memberships: Optional[List[Any]] = None,
        existing_recs: Optional[List[Any]] = None,
        store: Optional[List[Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        return cls.evaluate_and_upsert_recommendation(
            pet=pet,
            customer=customer,
            service_type=service_type,
            visits=visits,
            current_date=current_date,
            memberships=memberships,
            existing_recs=existing_recs,
            store=store,
        )
