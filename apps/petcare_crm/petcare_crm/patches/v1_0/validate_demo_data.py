"""Read-only validation for the reproducible PetCare CRM demo dataset.

Run with:
  bench --site petcare.localhost execute \
    petcare_crm.patches.v1_0.validate_demo_data.execute
"""

import json
from typing import Any, Dict, Iterable, List

import frappe

from petcare_crm.patches.v1_0.seed_demo_data import (
    DEMO_CONTACTS,
    DEMO_LEADS,
    DEMO_OPPORTUNITIES,
    DEMO_PETS,
    DEMO_PLANS,
    DEMO_SERVICES,
    EXPECTED_DEMO_COUNTS,
)


def _names(doctype: str, filters: Dict[str, Any]) -> List[str]:
    if not frappe.db.exists("DocType", doctype):
        return []
    rows = frappe.get_all(doctype, filters=filters, fields=["name"])
    return [row.name if hasattr(row, "name") else row["name"] for row in rows]


def _field_values(doctype: str, names: Iterable[str], fieldname: str) -> List[Any]:
    names = list(names)
    if not names:
        return []
    rows = frappe.get_all(
        doctype,
        filters={"name": ["in", names]},
        fields=[fieldname],
    )
    return [getattr(row, fieldname, None) if hasattr(row, fieldname) else row.get(fieldname) for row in rows]


def _contact_names() -> List[str]:
    names = []
    for contact in DEMO_CONTACTS:
        for field, value in (
            ("mobile_no", contact["phone"]),
            ("phone", contact["phone"]),
            ("email_id", contact["email_id"]),
        ):
            names.extend(_names("Contact", {field: value}))
    return sorted(set(names))


def _check(name: str, expected: Any, actual: Any) -> Dict[str, Any]:
    return {
        "name": name,
        "passed": actual == expected,
        "expected": expected,
        "actual": actual,
    }


def validate(raise_on_error: bool = False, print_report: bool = True) -> Dict[str, Any]:
    """Validate only the records owned by the demo dataset; never mutates data."""
    contact_names = _contact_names()
    address_names = _names(
        "Address",
        {"address_title": ["in", [f"DEMO - {contact['first_name']}" for contact in DEMO_CONTACTS]]},
    )
    pet_names = _names(
        "Pet",
        {
            "customer": ["in", contact_names],
            "pet_name": ["in", [pet["pet_name"] for pet in DEMO_PETS]],
        },
    ) if contact_names else []
    service_names = _names(
        "PetCare Service",
        {"service_code": ["in", [service["service_code"] for service in DEMO_SERVICES]]},
    )
    plan_names = _names(
        "Membership Plan",
        {"plan_name": ["in", [plan["plan_name"] for plan in DEMO_PLANS]]},
    )
    membership_names = _names(
        "Customer Membership",
        {
            "customer": ["in", contact_names],
            "membership_plan": ["in", [plan["plan_name"] for plan in DEMO_PLANS]],
        },
    ) if contact_names else []
    visit_names = _names(
        "Service Visit", {"customer": ["in", contact_names], "pet": ["in", pet_names]}
    ) if contact_names and pet_names else []
    appointment_names = _names(
        "PetCare Appointment", {"customer": ["in", contact_names], "pet": ["in", pet_names]}
    ) if contact_names and pet_names else []
    lead_names = _names(
        "PetCare Lead", {"phone": ["in", [lead["phone"] for lead in DEMO_LEADS]]}
    )
    opportunity_names = _names(
        "PetCare Opportunity",
        {"opportunity_title": ["in", [row["opportunity_title"] for row in DEMO_OPPORTUNITIES]]},
    )
    recommendation_names = _names(
        "Care Recommendation", {"customer": ["in", contact_names], "pet": ["in", pet_names]}
    ) if contact_names and pet_names else []
    case_names = _names(
        "PetCare Case", {"customer": ["in", contact_names], "pet": ["in", pet_names]}
    ) if contact_names and pet_names else []
    todo_names = _names(
        "ToDo",
        {
            "reference_type": "Care Recommendation",
            "reference_name": ["in", recommendation_names],
        },
    ) if recommendation_names else []

    observed_counts = {
        "Contact": len(contact_names),
        "Address": len(address_names),
        "Pet": len(pet_names),
        "PetCare Service": len(service_names),
        "Membership Plan": len(plan_names),
        "Customer Membership": len(membership_names),
        "Service Visit": len(visit_names),
        "PetCare Appointment": len(appointment_names),
        "PetCare Lead": len(lead_names),
        "PetCare Opportunity": len(opportunity_names),
        "Care Recommendation": len(recommendation_names),
        "PetCare Case": len(case_names),
        "ToDo": len(todo_names),
    }

    checks = [
        _check(f"count:{doctype}", expected, observed_counts[doctype])
        for doctype, expected in EXPECTED_DEMO_COUNTS.items()
    ]

    an_contact = frappe.db.get_value("Contact", {"mobile_no": "0901234567"}, "name")
    if not an_contact:
        an_contact = frappe.db.get_value("Contact", {"phone": "0901234567"}, "name")
    an_pets = _names(
        "Pet",
        {"customer": an_contact, "pet_name": ["in", ["Bơ", "Đậu Đậu"]]},
    ) if an_contact else []
    checks.extend([
        _check("scenario:multi_pet_owner", 2, len(an_pets)),
        _check(
            "scenario:lead_statuses",
            ["Contacted", "Converted", "New", "Unqualified"],
            sorted(_field_values("PetCare Lead", lead_names, "status")),
        ),
        _check(
            "scenario:opportunity_stages",
            ["Closed Lost", "Closed Won", "Proposal", "Prospecting"],
            sorted(_field_values("PetCare Opportunity", opportunity_names, "stage")),
        ),
        _check(
            "scenario:membership_statuses",
            ["Active", "Active", "Active", "Expired"],
            sorted(_field_values("Customer Membership", membership_names, "status")),
        ),
        _check(
            "scenario:recommendation_types",
            ["AT_RISK", "DUE_SOON", "DUE_SOON", "RENEWAL"],
            sorted(_field_values("Care Recommendation", recommendation_names, "recommendation_type")),
        ),
        _check(
            "scenario:recommendation_statuses",
            ["CONTACTED", "CONVERTED", "NEW", "NEW"],
            sorted(_field_values("Care Recommendation", recommendation_names, "status")),
        ),
    ])

    failed = [check for check in checks if not check["passed"]]
    woo_count = 0
    if frappe.db.exists("DocType", "WooCommerce Order Sync"):
        woo_count = frappe.db.count("WooCommerce Order Sync")

    result = {
        "status": "PASS" if not failed else "FAIL",
        "dataset_version": "2026.11",
        "observed_counts": observed_counts,
        "checks": checks,
        "failed_checks": failed,
        "informational": {
            "woocommerce_order_sync_count": woo_count,
            "woocommerce_required_for_seed_validation": False,
        },
    }

    if print_report:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    if failed and raise_on_error:
        frappe.throw(
            "Demo dataset validation failed: "
            + ", ".join(check["name"] for check in failed)
        )
    return result


def execute() -> Dict[str, Any]:
    """Bench entry point."""
    return validate(raise_on_error=True, print_report=True)
