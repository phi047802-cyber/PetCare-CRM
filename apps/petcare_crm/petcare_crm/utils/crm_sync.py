# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate, getdate


def get_customer_info(customer_name_or_id):
    """
    Trích xuất thông tin khách hàng (tên, số điện thoại, email) từ Contact hoặc Customer.
    """
    if not customer_name_or_id:
        return {"name": "Khách Vãng Lai", "mobile": None, "email": None}

    name = str(customer_name_or_id)
    mobile = None
    email = None

    if frappe.db.exists("Contact", customer_name_or_id):
        c = frappe.get_cached_doc("Contact", customer_name_or_id)
        name = c.first_name or customer_name_or_id
        if c.last_name:
            name = f"{c.first_name} {c.last_name}"
        mobile = c.mobile_no or c.phone
        email = c.email_id
    elif frappe.db.exists("Customer", customer_name_or_id):
        cust = frappe.get_cached_doc("Customer", customer_name_or_id)
        name = cust.customer_name or customer_name_or_id
        mobile = cust.mobile_no
        email = cust.email_id
    else:
        # Tìm trong Contact theo first_name
        matched_contact = frappe.db.get_value("Contact", {"first_name": customer_name_or_id}, ["name", "first_name", "last_name", "phone", "email_id"], as_dict=True)
        if matched_contact:
            name = matched_contact.first_name
            if matched_contact.last_name:
                name = f"{matched_contact.first_name} {matched_contact.last_name}"
            mobile = matched_contact.phone
            email = matched_contact.email_id

    return {
        "name": name,
        "mobile": mobile,
        "email": email,
    }


def ensure_crm_lead(customer_name_or_id, notes=None):
    """
    Đảm bảo có một CRM Lead đại diện cho khách hàng này để cập nhật phễu bán hàng (Funnel/Leads).
    """
    if not frappe.db.exists("DocType", "CRM Lead"):
        return None

    cust_info = get_customer_info(customer_name_or_id)
    lead_name = cust_info["name"]

    # Kiểm tra xem Lead đã tồn tại chưa (theo email, mobile, hoặc lead_name)
    existing_lead = None
    if cust_info.get("email"):
        existing_lead = frappe.db.get_value("CRM Lead", {"email": cust_info["email"]}, "name")
    if not existing_lead and cust_info.get("mobile"):
        existing_lead = frappe.db.get_value("CRM Lead", {"mobile_no": cust_info["mobile"]}, "name")
    if not existing_lead:
        existing_lead = frappe.db.get_value("CRM Lead", {"lead_name": lead_name}, "name")

    if existing_lead:
        return existing_lead

    try:
        lead = frappe.get_doc({
            "doctype": "CRM Lead",
            "lead_name": lead_name,
            "first_name": lead_name,
            "email": cust_info.get("email"),
            "mobile_no": cust_info.get("mobile"),
            "status": "Qualified",
            "lead_owner": "Administrator",
            "details": notes or "Khách hàng dịch vụ thú cưng PetCare",
        }).insert(ignore_permissions=True)
        return lead.name
    except Exception as e:
        frappe.logger("petcare_crm").warning(f"Could not create CRM Lead for {lead_name}: {e}")
        return None


def sync_transaction_to_crm_deal(
    customer,
    deal_value,
    title,
    notes=None,
    transaction_date=None,
    deal_type="Won",
    lead_name=None,
):
    """
    Tự động ghi nhận/đồng bộ một giao dịch doanh thu PetCare sang CRM Deal trong Frappe CRM.
    Giúp màn hình /crm/dashboard cập nhật số liệu thời gian thực (Won Deals, Avg Deal Value, Sales Trend, Pipeline).
    """
    try:
        val = float(deal_value or 0)
    except (ValueError, TypeError):
        val = 0.0

    if val <= 0:
        return None

    if not frappe.db.exists("DocType", "CRM Deal"):
        return None

    try:
        t_date = str(transaction_date or nowdate())[:10]
        cust_info = get_customer_info(customer)
        c_name = lead_name or cust_info["name"]

        # Lấy hoặc tạo CRM Lead liên kết
        lead_id = ensure_crm_lead(customer, notes=title)

        deal = frappe.get_doc({
            "doctype": "CRM Deal",
            "status": "Won",
            "deal_value": val,
            "expected_deal_value": val,
            "currency": "VND",
            "exchange_rate": 1.0,
            "closed_date": t_date,
            "deal_owner": "Administrator",
            "lead_name": c_name,
            "first_name": c_name,
            "organization_name": title,
            "next_step": notes or title,
            "lead": lead_id,
        })

        if cust_info.get("mobile"):
            deal.mobile_no = cust_info["mobile"]
        if cust_info.get("email"):
            deal.email = cust_info["email"]

        if frappe.db.exists("Contact", customer):
            deal.contact = customer

        # Thêm nhật ký chuyển trạng thái sang Won để biểu đồ Funnel Conversion ghi nhận
        deal.append("status_change_log", {
            "from": "Qualification",
            "from_type": "Open",
            "to": "Won",
            "to_type": "Won",
            "from_date": f"{t_date} 08:00:00",
            "to_date": f"{t_date} 09:00:00",
            "duration": 3600,
            "log_owner": "Administrator",
        })

        deal.insert(ignore_permissions=True)
        frappe.db.commit()
        return deal.name
    except Exception as e:
        frappe.logger("petcare_crm").warning(f"Failed to sync CRM Deal: {e}")
        return None
