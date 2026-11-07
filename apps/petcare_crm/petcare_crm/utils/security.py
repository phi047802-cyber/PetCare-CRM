"""
Security, Authorization & Role-Based Access Control (RBAC) Module.
Enforces backend authorization and cross-entity access verification:
- Role hierarchy: System Manager > PetCare Manager > PetCare Sales > PetCare Technician > PetCare Analyst
- Cross-entity ownership validation (Customer -> Pet -> Membership -> Service Visit)
- Input sanitization and sensitive field protection
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import frappe
    from frappe import _
except ImportError:
    frappe = None
    _ = lambda x: x

from petcare_crm.utils.exceptions import ValidationError

# System Role Definitions
ROLE_SYSTEM_MANAGER = "System Manager"
ROLE_CRM_MANAGER = "PetCare Manager"
ROLE_SALES = "PetCare Sales"
ROLE_TECHNICIAN = "PetCare Technician"
ROLE_ANALYST = "PetCare Analyst"

ALL_PETCARE_ROLES = {
    ROLE_SYSTEM_MANAGER,
    ROLE_CRM_MANAGER,
    ROLE_SALES,
    ROLE_TECHNICIAN,
    ROLE_ANALYST,
}

# Role Hierarchy / Capability Matrix
ROLE_PERMISSIONS: Dict[str, Dict[str, Set[str]]] = {
    ROLE_SYSTEM_MANAGER: {
        "PetCare Lead": {"read", "create", "write", "delete", "report", "export"},
        "PetCare Opportunity": {"read", "create", "write", "delete", "report", "export"},
        "Pet": {"read", "create", "write", "delete", "report", "export"},
        "PetCare Service": {"read", "create", "write", "delete", "report", "export"},
        "Service Visit": {"read", "create", "write", "delete", "cancel", "report", "export"},
        "PetCare Case": {"read", "create", "write", "delete", "report", "export"},
        "Membership Plan": {"read", "create", "write", "delete", "report", "export"},
        "Customer Membership": {"read", "create", "write", "delete", "cancel", "report", "export"},
        "Benefit Redemption Ledger": {"read", "create", "write", "delete", "cancel", "report", "export"},
        "Membership Transaction": {"read", "create", "write", "delete", "report", "export"},
        "Care Recommendation": {"read", "create", "write", "delete", "report", "export"},
        "ToDo": {"read", "create", "write", "delete", "report", "export"},
    },
    ROLE_CRM_MANAGER: {
        "PetCare Lead": {"read", "create", "write", "delete", "report", "export"},
        "PetCare Opportunity": {"read", "create", "write", "delete", "report", "export"},
        "Pet": {"read", "create", "write", "report", "export"},
        "PetCare Service": {"read", "create", "write", "report", "export"},
        "Service Visit": {"read", "create", "write", "cancel", "report", "export"},
        "PetCare Case": {"read", "create", "write", "report", "export"},
        "Membership Plan": {"read", "create", "write", "report", "export"},
        "Customer Membership": {"read", "create", "write", "cancel", "report", "export"},
        "Benefit Redemption Ledger": {"read", "report", "export"},
        "Membership Transaction": {"read", "create", "report", "export"},
        "Care Recommendation": {"read", "create", "write", "delete", "report", "export"},
        "ToDo": {"read", "create", "write", "delete", "report", "export"},
    },
    ROLE_SALES: {
        "PetCare Lead": {"read", "create", "write", "report"},
        "PetCare Opportunity": {"read", "create", "write", "report"},
        "Pet": {"read", "create", "write", "report"},
        "PetCare Service": {"read"},
        "Service Visit": {"read", "create", "report"},
        "PetCare Case": {"read", "create", "write"},
        "Membership Plan": {"read"},
        "Customer Membership": {"read", "create", "report"},
        "Benefit Redemption Ledger": {"read"},
        "Membership Transaction": {"read"},
        "Care Recommendation": {"read", "write"},
        "ToDo": {"read", "create", "write"},
    },
    ROLE_TECHNICIAN: {
        "PetCare Lead": set(),
        "PetCare Opportunity": set(),
        "Pet": {"read", "write"},
        "PetCare Service": {"read"},
        "Service Visit": {"read", "create", "write"},
        "PetCare Case": {"read", "write"},
        "Membership Plan": {"read"},
        "Customer Membership": {"read"},
        "Benefit Redemption Ledger": {"read"},
        "Membership Transaction": set(),
        "Care Recommendation": {"read"},
        "ToDo": {"read", "write"},
    },
    ROLE_ANALYST: {
        "PetCare Lead": {"read", "report", "export"},
        "PetCare Opportunity": {"read", "report", "export"},
        "Pet": {"read", "report", "export"},
        "PetCare Service": {"read", "report", "export"},
        "Service Visit": {"read", "report", "export"},
        "PetCare Case": {"read", "report", "export"},
        "Membership Plan": {"read", "report", "export"},
        "Customer Membership": {"read", "report", "export"},
        "Benefit Redemption Ledger": {"read", "report", "export"},
        "Membership Transaction": {"read", "report", "export"},
        "Care Recommendation": {"read", "report", "export"},
        "ToDo": {"read", "report"},
    },
}

# Regex for Vietnamese phone number validation
VIETNAM_PHONE_REGEX = re.compile(r"^(03|05|07|08|09)\d{8}$")


def get_current_user() -> str:
    """Returns current active session user or 'Administrator' in local mode."""
    if frappe and hasattr(frappe, "session") and hasattr(frappe.session, "user"):
        return frappe.session.user or "Administrator"
    return "Administrator"


def get_current_user_roles(user: Optional[str] = None) -> List[str]:
    """Retrieves list of roles assigned to user."""
    target_user = user or get_current_user()
    if target_user == "Administrator":
        return [ROLE_SYSTEM_MANAGER]
    if frappe and hasattr(frappe, "get_roles"):
        return frappe.get_roles(target_user)
    return [ROLE_SYSTEM_MANAGER]


def check_role_permission(
    doctype: str,
    permission_type: str,
    user: Optional[str] = None,
    raise_exception: bool = False,
) -> bool:
    """
    Evaluates role permissions strictly at the backend layer.
    permission_type: 'read', 'create', 'write', 'delete', 'cancel', 'report', 'export'
    """
    user_roles = get_current_user_roles(user)
    if ROLE_SYSTEM_MANAGER in user_roles or "Administrator" == (user or get_current_user()):
        return True

    perm_type_lower = permission_type.lower()
    for role in user_roles:
        doctype_perms = ROLE_PERMISSIONS.get(role, {}).get(doctype, set())
        if perm_type_lower in doctype_perms:
            return True

    if raise_exception:
        msg = _(f"Bạn không có quyền '{permission_type}' trên dữ liệu '{doctype}'.")
        if frappe and hasattr(frappe, "throw"):
            frappe.throw(msg, getattr(frappe, "PermissionError", ValidationError))
        else:
            raise ValidationError(msg)

    return False


def validate_cross_entity_relationship(
    customer_id: str,
    pet_id: Optional[str] = None,
    membership_id: Optional[str] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Validates cross-entity ownership:
    - Pet MUST belong to the specified Customer.
    - Membership MUST belong to the specified Customer (and cover the Pet if not a Family plan).
    Prevents unauthorized cross-customer data leakage or linking.
    """
    if not frappe or not hasattr(frappe, "db"):
        return True, None

    # 1. Validate Pet ownership
    if pet_id:
        pet_owner = frappe.db.get_value("Pet", pet_id, ["customer", "owner"], as_dict=True)
        if not pet_owner:
            return False, f"Không tìm thấy thú cưng '{pet_id}' trong hệ thống."
        actual_cust = pet_owner.get("customer") or pet_owner.get("owner")
        if actual_cust and actual_cust != customer_id:
            return False, f"Thú cưng '{pet_id}' không thuộc sở hữu của khách hàng '{customer_id}'."

    # 2. Validate Membership ownership
    if membership_id:
        ms = frappe.db.get_value("Customer Membership", membership_id, ["customer", "pet", "status"], as_dict=True)
        if not ms:
            return False, f"Không tìm thấy thẻ hội viên '{membership_id}'."
        if ms.get("customer") != customer_id:
            return False, f"Thẻ hội viên '{membership_id}' không thuộc về khách hàng '{customer_id}'."
        # If membership is pet-specific, verify it matches
        ms_pet = ms.get("pet")
        if ms_pet and pet_id and ms_pet != pet_id:
            return False, f"Thẻ hội viên '{membership_id}' được chỉ định riêng cho thú cưng '{ms_pet}', không áp dụng cho '{pet_id}'."

    return True, None


def sanitize_phone(phone: Optional[str]) -> str:
    """Normalizes and validates Vietnamese phone numbers."""
    if not phone:
        return ""
    cleaned = re.sub(r"[\s\-\.\(\)]", "", str(phone).strip())
    if cleaned.startswith("+84"):
        cleaned = "0" + cleaned[3:]
    elif cleaned.startswith("84") and len(cleaned) == 11:
        cleaned = "0" + cleaned[2:]
    return cleaned


def is_valid_vietnam_phone(phone: str) -> bool:
    """Checks whether phone matches Vietnam standard 10-digit mobile prefix."""
    cleaned = sanitize_phone(phone)
    return bool(VIETNAM_PHONE_REGEX.match(cleaned))


def sanitize_input_string(val: Any, max_length: int = 140, allow_none: bool = False) -> Optional[str]:
    """Sanitizes user input, strips control characters and truncates safely."""
    if val is None:
        return None if allow_none else ""
    s = str(val).strip()
    # Strip potential HTML/script injection tags
    s = re.sub(r"<[^>]*>", "", s)
    return s[:max_length]


def sanitize_number(val: Any, min_val: float = 0.0, max_val: Optional[float] = None) -> float:
    """Validates and bounds numeric inputs."""
    try:
        n = float(val)
        if n < min_val:
            raise ValidationError(f"Giá trị không được nhỏ hơn {min_val}.")
        if max_val is not None and n > max_val:
            raise ValidationError(f"Giá trị không được vượt quá {max_val}.")
        return n
    except (ValueError, TypeError):
        raise ValidationError(f"Giá trị '{val}' không phải số hợp lệ.")
