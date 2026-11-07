"""
Frappe Adapter Layer.
Converts Frappe document dicts to service layer dataclass objects.
This is the bridge between Frappe ORM and the ported business logic.
"""
import frappe
from datetime import date, datetime
from typing import List, Optional

from petcare_crm.utils.models import (
    ServiceVisit,
    Membership,
    MembershipBenefit,
)
from petcare_crm.utils.membership_service import MembershipService, _is_membership_active
from petcare_crm.utils.config import (
    DISCOUNT_TYPE_FREE,
    STATUS_ACTIVE,
)


def _parse_date(d) -> Optional[date]:
    """Convert string hoặc date object sang Python date."""
    if d is None:
        return None
    if isinstance(d, date):
        return d
    if isinstance(d, datetime):
        return d.date()
    try:
        return datetime.strptime(str(d)[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def get_service_visits_for_pet(pet_name: str, service_type: str = None) -> list:
    """
    Lấy danh sách Service Visit từ Frappe DB,
    convert sang ServiceVisit dataclass để service layer dùng.
    """
    filters = {"pet": pet_name}
    if service_type:
        filters["service_type"] = service_type

    rows = frappe.db.get_list(
        "Service Visit",
        filters=filters,
        fields=["name", "pet", "customer", "service_type",
                "visit_date", "original_price", "final_price", "membership"],
        order_by="visit_date asc",
        ignore_permissions=True,
    )

    result = []
    for r in rows:
        sv = ServiceVisit(
            pet=r.get("pet", ""),
            customer=r.get("customer", ""),
            service_type=r.get("service_type", ""),
            visit_date=_parse_date(r.get("visit_date")),
            original_price=float(r.get("original_price") or 0),
            final_price=float(r.get("final_price") or 0),
            membership=r.get("membership"),
            name=r.get("name"),
        )
        result.append(sv)
    return result


def get_membership_objects_for_customer(customer: str, pet: str = None) -> list:
    """
    Lấy tất cả Customer Membership từ Frappe DB,
    convert sang Membership dataclass để MembershipService dùng.
    """
    if not customer:
        return []
    customer = str(customer).strip()
    contact_ids = [customer]
    try:
        matched_contacts = frappe.db.sql(
            """
            SELECT name FROM `tabContact`
            WHERE name = %(c)s 
               OR first_name = %(c)s 
               OR last_name = %(c)s
               OR CONCAT_WS(' ', first_name, last_name) = %(c)s
               OR email_id = %(c)s
               OR phone = %(c)s
            LIMIT 10
            """,
            {"c": customer},
            pluck=True
        )
        for c in matched_contacts:
            if c not in contact_ids:
                contact_ids.append(c)
    except Exception:
        pass

    if len(contact_ids) == 1:
        filters = {"customer": contact_ids[0]}
    else:
        filters = {"customer": ["in", contact_ids]}

    if pet:
        filters["pet"] = pet

    rows = frappe.db.get_list(
        "Customer Membership",
        filters=filters,
        fields=["name", "customer", "pet", "membership_plan",
                "start_date", "end_date", "status"],
        order_by="end_date desc",
        ignore_permissions=True,
    )

    if not rows:
        return []

    # Batch load toàn bộ benefits trong 1 query
    ms_names = [r["name"] for r in rows]
    benefits_by_parent = {}
    benefits_raw = frappe.db.get_list(
        "Membership Benefit",
        filters={"parent": ["in", ms_names]},
        fields=["parent", "benefit_type", "total_quantity", "used_quantity",
                "remaining_quantity", "discount_type", "discount_value"],
        ignore_permissions=True,
    )
    for b in benefits_raw:
        benefits_by_parent.setdefault(b["parent"], []).append(b)

    memberships = []
    for r in rows:
        parent_benefits = benefits_by_parent.get(r["name"], [])
        benefits = [
            MembershipBenefit(
                benefit_type=b.get("benefit_type", ""),
                total_quantity=int(b.get("total_quantity") or 0),
                used_quantity=int(b.get("used_quantity") or 0),
                remaining_quantity=int(
                    b.get("remaining_quantity")
                    if b.get("remaining_quantity") is not None
                    else (int(b.get("total_quantity") or 0) - int(b.get("used_quantity") or 0))
                ),
                discount_type=b.get("discount_type") or DISCOUNT_TYPE_FREE,
                discount_value=float(b.get("discount_value") or 100.0),
            )
            for b in parent_benefits
        ]

        ms = Membership(
            name=r["name"],
            customer=r["customer"],
            pet=r.get("pet"),
            membership_plan=r["membership_plan"],
            start_date=_parse_date(r["start_date"]),
            end_date=_parse_date(r["end_date"]),
            status=r.get("status", STATUS_ACTIVE),
            benefits=benefits,
        )
        memberships.append(ms)
    return memberships


def get_active_membership_object(customer: str, pet: str = None, check_date: date = None):
    """
    H4: Trả về Membership object còn hạn hoặc None.
    Khắc phục logic gán sai target_customer từ memberships[0].
    """
    if not customer:
        return None
    if check_date is None:
        check_date = date.today()
    elif not isinstance(check_date, date):
        check_date = _parse_date(check_date) or date.today()

    memberships = get_membership_objects_for_customer(customer, pet)
    if not memberships:
        return None

    # Lọc các membership đang active và còn hiệu lực tại check_date
    active_memberships = [
        ms for ms in memberships
        if _is_membership_active(ms, check_date)
        and (not pet or not ms.pet or ms.pet == pet)
    ]

    if not active_memberships:
        return None

    # Ưu tiên membership có end_date xa nhất (còn hạn lâu nhất)
    def _sort_key(m):
        return m.end_date if m.end_date is not None else date.min

    active_memberships.sort(key=_sort_key, reverse=True)
    return active_memberships[0]
