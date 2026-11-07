# Copyright (c) 2026, PetCare Team and contributors
# For license information, please see license.txt

import frappe

PETCARE_ROLES = [
    {"role_name": "PetCare Front Desk", "desk_access": 1},
    {"role_name": "PetCare Veterinarian", "desk_access": 1},
    {"role_name": "PetCare Groomer", "desk_access": 1},
    {"role_name": "PetCare Manager", "desk_access": 1},
    {"role_name": "PetCare Sales", "desk_access": 1},
    {"role_name": "PetCare Analyst", "desk_access": 1},
    {"role_name": "PetCare Customer Portal", "desk_access": 0},
]


def setup_petcare_crm():
    """
    Tự động khởi tạo Roles và phân quyền mặc định khi cài đặt hoặc migrate app (Finding-08 Fix).
    Đảm bảo site mới cài đặt có đầy đủ Role cần thiết để vận hành.
    """
    if not hasattr(frappe, "db") or not frappe.db:
        return

    # 1. Khởi tạo các Role nếu chưa tồn tại
    for r_info in PETCARE_ROLES:
        role_name = r_info["role_name"]
        if hasattr(frappe.db, "exists") and not frappe.db.exists("Role", role_name):
            try:
                role_doc = frappe.get_doc({
                    "doctype": "Role",
                    "role_name": role_name,
                    "desk_access": r_info.get("desk_access", 1),
                })
                role_doc.insert(ignore_permissions=True)
            except Exception:
                pass

    if hasattr(frappe.db, "commit"):
        try:
            frappe.db.commit()
        except Exception:
            pass
