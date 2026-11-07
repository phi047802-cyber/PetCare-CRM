# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import date
from petcare_crm.utils.analytics_service import AnalyticsService


def execute(filters=None):
    filters = filters or {}
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    columns = [
        {"label": _("Chỉ Số (KPI)"), "fieldname": "kpi_name", "fieldtype": "Data", "width": 240},
        {"label": _("Giá Trị Thực Tế"), "fieldname": "metric_value", "fieldtype": "Data", "width": 180},
        {"label": _("Đơn Vị / Chi Tiết"), "fieldname": "details", "fieldtype": "Data", "width": 300},
        {"label": _("Phân Khúc / Trạng Thái"), "fieldname": "segment", "fieldtype": "Data", "width": 220},
    ]

    dash = AnalyticsService.get_full_crm_dashboard(from_date, to_date)
    lead_m = dash["lead_conversion"]
    pipe_m = dash["sales_pipeline"]
    mem_m = dash["membership_status"]
    srv_m = dash["service_visits"]
    care_m = dash["care_retention"]

    data = [
        # Lead Conversion
        {
            "kpi_name": "Tỷ Lệ Chuyển Đổi Lead",
            "metric_value": f"{lead_m['conversion_rate_pct']}%",
            "details": f"{lead_m['converted_leads']} / {lead_m['total_leads']} Lead thành công",
            "segment": "CRM Core",
        },
        # Sales Pipeline
        {
            "kpi_name": "Tổng Giá Trị Cơ Hội (Pipeline)",
            "metric_value": frappe.format_value(pipe_m["total_pipeline_amount"], {"fieldtype": "Currency"}),
            "details": f"{pipe_m['total_opportunities']} cơ hội đang theo dõi",
            "segment": "Bán Hàng & Nâng Gói",
        },
        {
            "kpi_name": "Doanh Thu Dự Kiến Có Trọng Số",
            "metric_value": frappe.format_value(pipe_m["total_weighted_amount"], {"fieldtype": "Currency"}),
            "details": "Dự báo dựa trên xác suất từng giai đoạn",
            "segment": "Bán Hàng & Nâng Gói",
        },
        # Memberships
        {
            "kpi_name": "Thẻ Hội Viên Đang Hoạt Động",
            "metric_value": f"{mem_m['active_memberships']} thẻ",
            "details": f"Tổng số dư ví: {frappe.format_value(mem_m['total_member_balance'], {'fieldtype': 'Currency'})}",
            "segment": "Membership & Loyalty",
        },
        {
            "kpi_name": "Hội Viên Sắp Hết Hạn (<= 7 ngày)",
            "metric_value": f"{mem_m['expiring_within_7_days_count']} thẻ",
            "details": f"Cần liên hệ gia hạn (30 ngày tới: {mem_m['expiring_within_30_days_count']} thẻ)",
            "segment": "Membership & Loyalty",
        },
        # Service Visits
        {
            "kpi_name": "Tổng Lượt Dịch Vụ Thực Hiện",
            "metric_value": f"{srv_m['total_service_visits']} lượt",
            "details": f"Doanh thu thuần: {frappe.format_value(srv_m['net_revenue'], {'fieldtype': 'Currency'})}",
            "segment": "Vận Hành Dịch Vụ",
        },
        {
            "kpi_name": "Tổng Ưu Đãi / Giảm Giá Đã Áp Dụng",
            "metric_value": frappe.format_value(srv_m["total_discounts_granted"], {"fieldtype": "Currency"}),
            "details": f"Doanh số niêm yết: {frappe.format_value(srv_m['gross_revenue'], {'fieldtype': 'Currency'})}",
            "segment": "Vận Hành Dịch Vụ",
        },
        # Care Retention
        {
            "kpi_name": "Thú Cưng Sắp Đến Chu Kỳ (Due Soon)",
            "metric_value": f"{care_m['due_soon_total']} bé",
            "details": "Cần kích hoạt thông báo nhắc lịch định kỳ",
            "segment": "Care Retention",
        },
        {
            "kpi_name": "Khách Hàng Có Nguy Cơ Rời Bỏ (At Risk)",
            "metric_value": f"{care_m['at_risk_total']} bé",
            "details": "Vắng mặt vượt >= 1.5 lần chu kỳ sinh học",
            "segment": "Care Retention",
        },
        {
            "kpi_name": "Tỷ Lệ Chốt Khuyến Nghị CSKH",
            "metric_value": f"{care_m['conversion_rate_pct']}%",
            "details": f"Tổng số khuyến nghị: {care_m['total_recommendations']}",
            "segment": "Care Retention",
        },
    ]

    report_summary = [
        {"value": f"{lead_m['conversion_rate_pct']}%", "indicator": "blue", "label": _("Lead Win Rate"), "datatype": "Percent"},
        {"value": frappe.format_value(srv_m["net_revenue"], {"fieldtype": "Currency"}), "indicator": "green", "label": _("Doanh Thu Thuần"), "datatype": "Currency"},
        {"value": mem_m["active_memberships"], "indicator": "purple", "label": _("Hội Viên Active"), "datatype": "Int"},
        {"value": care_m["at_risk_total"], "indicator": "red", "label": _("Bé At-Risk"), "datatype": "Int"},
    ]

    return columns, data, None, None, report_summary
