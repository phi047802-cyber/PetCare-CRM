"""
PetCare CRM Daily & Hourly Scheduler Tasks (T39–T41 & Prompt 7).
Connects CRM Core, Service Operations, Membership, and Care Engine into automated workflows.

Entry points:
- daily_petcare_scan(): Runs full daily automation cycle (Leads, Memberships, Care Engine, Cases).
- hourly_workflow_check(): Runs fast hourly checks for uncontacted leads and urgent SLA breaches.

Manual trigger via Bench:
  bench --site petcare.localhost execute petcare_crm.tasks.daily_petcare_scan
  bench --site petcare.localhost execute petcare_crm.tasks.hourly_workflow_check
"""

import frappe
from datetime import date
from typing import Optional, Dict, Any

from petcare_crm.utils.workflow_automation import (
    AutomationCoordinator,
    CareEngineAutomation,
    LeadFollowupAutomation,
    MembershipRenewalAutomation,
    ServiceRecoveryAutomation,
)


def auto_expire_memberships(today: Optional[date] = None) -> int:
    """Tự động chuyển trạng thái các gói hội viên đã quá hạn (end_date < today) sang Expired."""
    if today is None:
        today = frappe.utils.getdate(frappe.utils.nowdate())
    return MembershipRenewalAutomation.auto_expire_memberships(today)


def check_due_and_at_risk_pets(today: Optional[date] = None) -> int:
    """
    Quét tất cả Pets, phân tích chu kỳ chăm sóc, phân loại DUE_SOON / AT_RISK.
    Cập nhật Care Recommendations và tạo task follow-up.
    """
    if today is None:
        today = frappe.utils.getdate(frappe.utils.nowdate())
    res = CareEngineAutomation.run_care_scan(today)
    return res.get("recs_created", 0)


def check_expiring_memberships(today: Optional[date] = None) -> int:
    """
    Quét Customer Membership sắp hết hạn trong 7 ngày.
    Tạo hoặc cập nhật Care Recommendation loại RENEWAL và task nhắc gia hạn.
    """
    if today is None:
        today = frappe.utils.getdate(frappe.utils.nowdate())
    res = MembershipRenewalAutomation.process_expiring_memberships(today)
    return res.get("recs_created", 0)


def daily_petcare_scan() -> Dict[str, Any]:
    """
    Main daily job — được gọi tự động hàng ngày bởi Frappe Scheduler.
    Chạy toàn bộ chu trình tự động hóa:
    1. Kiểm tra và giao việc cho Lead mới chưa liên hệ
    2. Auto-expire thẻ hết hạn & cảnh báo gia hạn hội viên
    3. Phân tích Care Engine (Due Soon & At Risk)
    4. Service Recovery kiểm tra các Case quá hạn SLA
    """
    frappe.logger("petcare_crm").info(
        f"[PetCare Daily Scan] Bắt đầu lúc {frappe.utils.now()}"
    )
    today = frappe.utils.getdate(frappe.utils.nowdate())

    results = AutomationCoordinator.run_all_automations(current_date=today)

    frappe.logger("petcare_crm").info(
        f"[PetCare Daily Scan] Hoàn tất lúc {frappe.utils.now()}. "
        f"Tasks mới: {results['total_tasks_created']} | Tasks đã tồn tại: {results['total_tasks_existing']} | Lỗi: {len(results['errors'])}"
    )

    due_created = results.get("care_engine", {}).get("recs_created", 0)
    renewal_created = results.get("membership_renewal", {}).get("recs_created", 0)

    return {
        "success": results["status"] != "failed",
        "due_count": due_created,
        "renewal_count": renewal_created,
        "total_created": results["total_tasks_created"],
        "details": results,
    }


def hourly_workflow_check() -> Dict[str, Any]:
    """
    Fast hourly job — kiểm tra các sự kiện cần phản hồi nhanh:
    - Lead mới chưa được liên hệ sau 24h
    - Case dịch vụ có độ ưu tiên cao / khẩn cấp quá hạn xử lý
    """
    frappe.logger("petcare_crm").info(
        f"[PetCare Hourly Workflow] Bắt đầu lúc {frappe.utils.now()}"
    )
    today = frappe.utils.getdate(frappe.utils.nowdate())

    lead_res = LeadFollowupAutomation.process_uncontacted_leads(today)
    case_res = ServiceRecoveryAutomation.process_open_cases(today)

    total_tasks = lead_res.get("tasks_created", 0) + case_res.get("tasks_created", 0)
    frappe.db.commit()

    return {
        "success": True,
        "lead_tasks_created": lead_res.get("tasks_created", 0),
        "case_tasks_created": case_res.get("tasks_created", 0),
        "total_tasks_created": total_tasks,
    }
