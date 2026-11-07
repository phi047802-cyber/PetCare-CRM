// Copyright (c) 2026, PetCare CRM Team and contributors
// For license information, please see license.txt

frappe.query_reports["PetCare KPI Overview"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("Từ Ngày"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            reqd: 0
        },
        {
            fieldname: "to_date",
            label: __("Đến Ngày"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 0
        }
    ]
};
