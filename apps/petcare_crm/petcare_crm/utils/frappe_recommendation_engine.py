"""
Frappe Recommendation Engine.
Integrates Care Intelligence with Frappe ORM and Customer Membership.
Generates, deduplicates, and updates Care Recommendation DocType records.
"""
from datetime import date, timedelta
from typing import Optional, Tuple, Union
import frappe
from petcare_crm.utils.care_pattern_service import (
    CarePatternService,
    RiskDetectionService,
)
from petcare_crm.utils.config import (
    RECOMMENDATION_DEDUP_WINDOW_DAYS,
    SERVICE_TYPES,
)
from petcare_crm.utils.frappe_adapters import (
    get_active_membership_object,
    get_service_visits_for_pet,
)

DEDUP_WINDOW = RECOMMENDATION_DEDUP_WINDOW_DAYS  # 14 ngày


def _find_active_recommendation(pet_name: str, service_type: str) -> Optional[dict]:
    """Tìm recommendation đang active (chưa đóng) của cặp (pet, service_type)."""
    existing = frappe.db.get_value(
        "Care Recommendation",
        {
            "pet": pet_name,
            "service_type": service_type,
            "status": ["in", ["NEW", "ASSIGNED", "CONTACTED"]],
        },
        ["name", "status", "recommendation_type", "recommendation_date"],
        as_dict=True,
    )
    return existing


def generate_and_save_recommendation(
    pet_name: str,
    customer_name: str,
    service_type: str,
    current_date: Optional[date] = None,
    auto_commit: bool = True,
    return_meta: bool = False,
) -> Union[Optional[str], Tuple[Optional[str], str, Optional[str]]]:
    """
    Sinh hoặc cập nhật Care Recommendation nếu điều kiện thỏa mãn.
    Tích hợp thông tin Membership để cá nhân hóa nội dung.
    Nếu đã tồn tại khuyến nghị active, cập nhật nội dung thay vì sinh bản ghi rác.
    Returns:
        - Nếu return_meta=False: tên document (str) hoặc None.
        - Nếu return_meta=True: (tên document, "CREATED" | "UPDATED" | "NONE", rec_type).
    """
    if current_date is None:
        current_date = date.today()

    def _ret(name, action, rtype):
        if return_meta:
            return name, action, rtype
        return name

    visits = get_service_visits_for_pet(pet_name, service_type)

    # Kiểm tra INSUFFICIENT_DATA trước
    interval_data = CarePatternService.calculate_average_interval(
        pet=pet_name, service_type=service_type, visits=visits
    )
    if interval_data.get("insufficient_data"):
        return _ret(None, "NONE", None)

    # Lấy trạng thái chăm sóc
    due_info = CarePatternService.detect_due_soon(
        pet=pet_name, service_type=service_type,
        visits=visits, current_date=current_date
    )
    at_risk_info = CarePatternService.detect_at_risk(
        pet=pet_name, service_type=service_type,
        visits=visits, current_date=current_date
    )

    rec_type = None
    priority = "Medium"

    if due_info.get("is_due_soon"):
        rec_type = "DUE_SOON"
    elif at_risk_info.get("is_at_risk"):
        rec_type = "AT_RISK"
        priority = "High"
    else:
        return _ret(None, "NONE", None)

    # Lấy thông tin Membership để cá nhân hóa
    membership = get_active_membership_object(customer_name, pet_name, current_date)
    membership_name = None
    benefit_info = ""

    if membership:
        membership_name = membership.name
        benefit = next(
            (b for b in membership.benefits
             if str(b.benefit_type).lower() == str(service_type).lower()
             and (b.remaining_quantity or 0) > 0),
            None
        )
        if benefit:
            priority = "High"
            benefit_info = (
                f" Khách hàng còn {benefit.remaining_quantity} lượt "
                f"'{benefit.benefit_type}' ưu đãi chưa dùng."
            )

    # Xây dựng reason và suggested_action
    if rec_type == "DUE_SOON":
        days = due_info.get("days_until_due", 0)
        pred_date = due_info.get("predicted_date")
        reason = (
            f"Pet '{pet_name}' sắp đến chu kỳ {service_type} "
            f"(còn {days} ngày tới ngày dự đoán {pred_date}).{benefit_info}"
        )
        suggested_action = f"Liên hệ khách hàng đặt lịch {service_type} trong {days} ngày tới."
    else:  # AT_RISK
        ratio = at_risk_info.get("absence_ratio", 0)
        days_absent = at_risk_info.get("days_since_last_visit", 0)
        reason = (
            f"Pet '{pet_name}' đã quá chu kỳ {service_type} "
            f"({days_absent} ngày vắng, tỷ lệ: {ratio:.2f} >= {at_risk_info.get('threshold_ratio', 1.5)}).{benefit_info}"
        )
        suggested_action = f"Gửi tin nhắn win-back, nhắc khách hàng quay lại sử dụng {service_type}."

    # Kiểm tra xem đã có recommendation active chưa -> Cập nhật in-place (deduplication & update)
    existing_rec = _find_active_recommendation(pet_name, service_type)
    if existing_rec:
        doc = frappe.get_doc("Care Recommendation", existing_rec["name"])
        doc.recommendation_date = str(current_date)
        doc.recommendation_type = rec_type
        doc.priority = priority
        doc.reason = reason
        doc.suggested_action = suggested_action
        if membership_name:
            doc.membership = membership_name
        doc.save(ignore_permissions=True)
        if auto_commit:
            frappe.db.commit()
        return _ret(doc.name, "UPDATED", rec_type)

    # Tạo mới nếu chưa có
    doc = frappe.get_doc({
        "doctype": "Care Recommendation",
        "customer": customer_name,
        "pet": pet_name,
        "service_type": service_type,
        "recommendation_type": rec_type,
        "recommendation_date": str(current_date),
        "reason": reason,
        "priority": priority,
        "suggested_action": suggested_action,
        "status": "NEW",
        "membership": membership_name,
    })
    doc.insert(ignore_permissions=True)
    if auto_commit:
        frappe.db.commit()
    return _ret(doc.name, "CREATED", rec_type)


def generate_all_recommendations(current_date: Optional[date] = None) -> dict:
    """
    Quét tất cả Pets và sinh/cập nhật Care Recommendation cho từng service type.
    """
    if current_date is None:
        current_date = date.today()

    all_pets = frappe.db.get_list("Pet", fields=["name", "customer"], ignore_permissions=True)
    created = []
    skipped = []

    for pet in all_pets:
        cust = pet.get("customer")
        if not cust:
            cust = pet.get("owner")
        for st in SERVICE_TYPES:
            rec_name = generate_and_save_recommendation(
                pet_name=pet["name"],
                customer_name=cust,
                service_type=st,
                current_date=current_date,
                auto_commit=False,
            )
            if rec_name:
                created.append(rec_name)
            else:
                skipped.append(f"{pet['name']}/{st}")

    if created:
        frappe.db.commit()

    return {
        "created": len(created),
        "skipped": len(skipped),
        "recommendation_names": created,
    }
