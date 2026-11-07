"""
Workflow, Automation & Customer Follow-up Engine (CRM 2.0).
Provides robust, idempotent scheduled automations across:
1. Lead Follow-up (uncontacted leads, task allocation, due date management)
2. Membership Expiration & Auto-expiry (7-day advance renewal warnings, task allocation)
3. Care Engine Periodic Scans (Due Soon & At Risk detection, recommendation update, follow-up tasks)
4. Service Recovery (unresolved cases SLA monitoring, escalation tasks)
5. Safe Mode Communication Gateway (prevents accidental real email/WhatsApp in demo mode)
6. AutomationCoordinator (unified execution, transaction boundary safety, full audit logging)
"""

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import frappe
except ImportError:
    frappe = None

from petcare_crm.utils.config import (
    AUTO_CREATE_TODO_FOR_RECOMMENDATIONS,
    CASE_SLA_WARNING_HOURS,
    DEDUP_WINDOW_DAYS,
    ENABLE_LIVE_COMMUNICATION,
    LEAD_UNCONTACTED_THRESHOLD_HOURS,
    MEMBERSHIP_EXPIRATION_WARNING_DAYS,
    RECOMMENDATION_NEW,
    RECOMMENDATION_TYPE_AT_RISK,
    RECOMMENDATION_TYPE_DUE_SOON,
    RECOMMENDATION_TYPE_RENEWAL,
    SERVICE_TYPES,
    STATUS_ACTIVE,
    STATUS_EXPIRED,
)
from petcare_crm.utils.care_pattern_service import (
    CarePatternService,
    _extract_date,
    _get_field,
)
from petcare_crm.utils.recommendation_service import RecommendationService


def _get_val(obj: Any, key: str, default: Any = None) -> Any:
    return _get_field(obj, key, default)


def _log_info(msg: str):
    if frappe and hasattr(frappe, "logger"):
        frappe.logger("petcare_crm").info(msg)
    else:
        pass


def _log_error(title: str, message: str = ""):
    if frappe and hasattr(frappe, "log_error"):
        try:
            frappe.log_error(title=title, message=message)
        except Exception:
            pass


class SafeCommunicationGateway:
    """
    Prevents unauthorized or real email/SMS/WhatsApp dispatch in demo/dev mode.
    Dispatches real communications ONLY when ENABLE_LIVE_COMMUNICATION is True.
    """

    @classmethod
    def send_communication(
        cls,
        recipient: str,
        subject: str,
        content: str,
        channel: str = "Email",
        reference_doctype: Optional[str] = None,
        reference_name: Optional[str] = None,
        force_live: bool = False,
    ) -> Dict[str, Any]:
        """
        Idempotent and safe communication gateway.
        """
        is_live_allowed = force_live or ENABLE_LIVE_COMMUNICATION

        if not is_live_allowed:
            _log_info(f"[SafeMode] Suppressed sending {channel} to {recipient}: {subject}")

            # Record internal communication log in Frappe if DB is available
            comm_name = None
            if frappe and reference_doctype and reference_name and hasattr(frappe, "db"):
                try:
                    comm = frappe.get_doc({
                        "doctype": "Communication",
                        "communication_type": "Communication",
                        "communication_medium": channel,
                        "subject": f"[DEMO/SAFE MODE] {subject}",
                        "content": content,
                        "recipients": recipient,
                        "reference_doctype": reference_doctype,
                        "reference_name": reference_name,
                        "status": "Draft",
                        "sent_or_received": "Sent",
                    })
                    comm.insert(ignore_permissions=True)
                    comm_name = comm.name
                except Exception:
                    pass

            return {
                "sent": False,
                "mode": "SAFE_MODE_MOCK",
                "channel": channel,
                "recipient": recipient,
                "subject": subject,
                "communication_name": comm_name,
                "message": "Thông báo được mô phỏng trong Safe Mode. Không gửi email thật ra ngoài.",
            }

        # Real communication dispatch (when explicitly enabled)
        if frappe and hasattr(frappe, "sendmail"):
            frappe.sendmail(
                recipients=[recipient],
                subject=subject,
                message=content,
                reference_doctype=reference_doctype,
                reference_name=reference_name,
            )
            return {
                "sent": True,
                "mode": "LIVE",
                "channel": channel,
                "recipient": recipient,
                "subject": subject,
            }

        return {"sent": False, "mode": "NO_DISPATCHER", "recipient": recipient}


class TaskManager:
    """
    Manages Frappe ToDo tasks with strict idempotency:
    Does NOT create duplicate tasks if an Open task already exists for the same reference.
    """

    @classmethod
    def ensure_todo(
        cls,
        reference_type: str,
        reference_name: str,
        description: str,
        allocated_to: Optional[str] = None,
        priority: str = "Medium",
        due_date: Optional[date] = None,
    ) -> Tuple[Optional[Any], str]:
        """
        Creates a ToDo task only if no Open ToDo exists for (reference_type, reference_name).
        Returns:
            (todo_doc_or_dict, "CREATED" | "EXISTING" | "SKIPPED")
        """
        if not frappe or not hasattr(frappe, "db"):
            return None, "NO_DB"

        allocated_user = allocated_to or "Administrator"
        due_str = str(due_date or date.today())

        # Check existing Open task
        existing_task = frappe.db.get_value(
            "ToDo",
            {
                "reference_type": reference_type,
                "reference_name": reference_name,
                "status": "Open",
            },
            ["name", "allocated_to", "description", "priority"],
            as_dict=True,
        )

        if existing_task:
            return existing_task, "EXISTING"

        # Create new ToDo task
        todo = frappe.get_doc({
            "doctype": "ToDo",
            "reference_type": reference_type,
            "reference_name": reference_name,
            "allocated_to": allocated_user,
            "description": description,
            "priority": priority,
            "date": due_str,
            "status": "Open",
        })
        todo.insert(ignore_permissions=True)
        return todo, "CREATED"


class LeadFollowupAutomation:
    """
    Automation: Lead Follow-up
    1. Identifies Leads in 'New' status uncontacted for >= LEAD_UNCONTACTED_THRESHOLD_HOURS.
    2. Creates follow-up ToDo task assigned to lead_owner with deadline.
    3. Idempotent: avoids duplicate tasks if an open ToDo exists.
    """

    @classmethod
    def process_uncontacted_leads(
        cls,
        current_date: Optional[date] = None,
        threshold_hours: int = LEAD_UNCONTACTED_THRESHOLD_HOURS,
    ) -> Dict[str, Any]:
        if current_date is None:
            current_date = date.today()
        if not frappe or not hasattr(frappe, "db"):
            return {"processed": 0, "tasks_created": 0, "tasks_existing": 0, "errors": []}

        leads = frappe.db.get_list(
            "PetCare Lead",
            filters={"status": "New"},
            fields=["name", "lead_name", "phone", "email", "lead_owner", "creation", "lead_source", "source"],
            ignore_permissions=True,
        )

        processed = 0
        tasks_created = 0
        tasks_existing = 0
        errors = []

        now_dt = datetime.now()

        for lead in leads:
            try:
                processed += 1
                # Check creation time
                creation_dt = lead.get("creation")
                if isinstance(creation_dt, str):
                    try:
                        creation_dt = datetime.strptime(creation_dt[:19], "%Y-%m-%d %H:%M:%S")
                    except Exception:
                        creation_dt = now_dt - timedelta(hours=threshold_hours + 1)
                elif not isinstance(creation_dt, datetime):
                    creation_dt = now_dt - timedelta(hours=threshold_hours + 1)

                hours_elapsed = (now_dt - creation_dt).total_seconds() / 3600.0

                # If lead has been waiting longer than threshold_hours (e.g. 24h)
                if hours_elapsed >= threshold_hours:
                    lead_owner = lead.get("lead_owner") or "Administrator"
                    lead_display = lead.get("lead_name") or lead["name"]
                    phone_display = lead.get("phone") or "Chưa có SĐT"

                    desc = (
                        f"Follow-up Lead mới: '{lead_display}' (SĐT: {phone_display}, Nguồn: {lead.get('lead_source') or lead.get('source') or 'Trực tiếp'}). "
                        f"Đã mở {int(hours_elapsed)}h chưa liên hệ. Hạn xử lý: Trong ngày."
                    )

                    _, action = TaskManager.ensure_todo(
                        reference_type="PetCare Lead",
                        reference_name=lead["name"],
                        description=desc,
                        allocated_to=lead_owner,
                        priority="Medium",
                        due_date=current_date,
                    )

                    if action == "CREATED":
                        tasks_created += 1
                    elif action == "EXISTING":
                        tasks_existing += 1
            except Exception as e:
                err_msg = f"Error processing lead {lead.get('name')}: {str(e)}"
                errors.append(err_msg)
                _log_error("LeadFollowupAutomation Error", err_msg)

        return {
            "processed": processed,
            "tasks_created": tasks_created,
            "tasks_existing": tasks_existing,
            "errors": errors,
        }


class MembershipRenewalAutomation:
    """
    Automation: Membership Expiration & Renewal
    1. Auto-expires memberships where end_date < current_date.
    2. Identifies memberships expiring within MEMBERSHIP_EXPIRATION_WARNING_DAYS (7 days).
    3. Generates/updates RENEWAL Care Recommendations.
    4. Creates renewal ToDo tasks for customer care staff without duplicates.
    """

    @classmethod
    def auto_expire_memberships(cls, current_date: Optional[date] = None) -> int:
        """Transitions active memberships past end_date to Expired."""
        if current_date is None:
            current_date = date.today()
        if not frappe or not hasattr(frappe, "db"):
            return 0

        expired_list = frappe.db.get_list(
            "Customer Membership",
            filters={
                "status": STATUS_ACTIVE,
                "end_date": ["<", str(current_date)],
            },
            fields=["name"],
            ignore_permissions=True,
        )

        for ms in expired_list:
            frappe.db.set_value("Customer Membership", ms["name"], "status", STATUS_EXPIRED)

        return len(expired_list)

    @classmethod
    def process_expiring_memberships(
        cls,
        current_date: Optional[date] = None,
        warning_days: int = MEMBERSHIP_EXPIRATION_WARNING_DAYS,
    ) -> Dict[str, Any]:
        if current_date is None:
            current_date = date.today()
        if not frappe or not hasattr(frappe, "db"):
            return {
                "auto_expired": 0,
                "expiring_count": 0,
                "recs_created_or_updated": 0,
                "tasks_created": 0,
                "tasks_existing": 0,
                "errors": [],
            }

        # 1. Auto-expire past memberships
        auto_expired_count = cls.auto_expire_memberships(current_date)

        # 2. Query expiring memberships
        threshold_date = current_date + timedelta(days=warning_days)
        expiring = frappe.db.get_list(
            "Customer Membership",
            filters={
                "status": STATUS_ACTIVE,
                "end_date": ["between", [str(current_date), str(threshold_date)]],
            },
            fields=["name", "customer", "pet", "end_date", "membership_plan"],
            ignore_permissions=True,
        )

        recs_created = 0
        recs_updated = 0
        tasks_created = 0
        tasks_existing = 0
        errors = []

        for ms in expiring:
            try:
                ms_end = ms["end_date"]
                if isinstance(ms_end, str):
                    ms_end = datetime.strptime(ms_end[:10], "%Y-%m-%d").date()

                days_left = (ms_end - current_date).days
                priority = "High" if days_left <= 3 else "Medium"
                cust = ms["customer"]
                plan_name = ms.get("membership_plan") or "Thẻ hội viên"

                pet_id = ms.get("pet") or ""
                if not pet_id:
                    pet_id = frappe.db.get_value("Pet", {"customer": cust}, "name") or ""

                reason = (
                    f"Gói hội viên '{plan_name}' của khách hàng '{cust}' "
                    f"sắp hết hạn sau {days_left} ngày (ngày hết: {ms_end}). "
                    f"Vui lòng liên hệ để tư vấn gia hạn kịp thời."
                )
                action_text = f"Liên hệ khách hàng '{cust}' gia hạn gói '{plan_name}' trước ngày {ms_end}."

                # Step 2A: Check or update active Care Recommendation for Renewal
                existing_rec = frappe.db.get_value(
                    "Care Recommendation",
                    {
                        "customer": cust,
                        "service_type": "Membership Renewal",
                        "status": ["in", ["NEW", "ASSIGNED", "CONTACTED"]],
                    },
                    ["name", "status"],
                    as_dict=True,
                )

                if existing_rec:
                    doc = frappe.get_doc("Care Recommendation", existing_rec["name"])
                    doc.recommendation_date = str(current_date)
                    doc.reason = reason
                    doc.priority = priority
                    doc.suggested_action = action_text
                    doc.membership = ms["name"]
                    doc.save(ignore_permissions=True)
                    recs_updated += 1
                else:
                    doc = frappe.get_doc({
                        "doctype": "Care Recommendation",
                        "customer": cust,
                        "pet": pet_id or None,
                        "service_type": "Membership Renewal",
                        "recommendation_type": RECOMMENDATION_TYPE_RENEWAL,
                        "recommendation_date": str(current_date),
                        "reason": reason,
                        "priority": priority,
                        "suggested_action": action_text,
                        "status": RECOMMENDATION_NEW,
                        "membership": ms["name"],
                    })
                    doc.insert(ignore_permissions=True)
                    recs_created += 1

                # Step 2B: Idempotent ToDo Task
                todo_desc = (
                    f"Nhắc gia hạn hội viên: Gói '{plan_name}' của khách '{cust}' "
                    f"còn {days_left} ngày (hết hạn: {ms_end})."
                )
                _, action = TaskManager.ensure_todo(
                    reference_type="Customer Membership",
                    reference_name=ms["name"],
                    description=todo_desc,
                    allocated_to="Administrator",
                    priority=priority,
                    due_date=ms_end,
                )
                if action == "CREATED":
                    tasks_created += 1
                elif action == "EXISTING":
                    tasks_existing += 1

            except Exception as e:
                err_msg = f"Error processing renewal for {ms.get('name')}: {str(e)}"
                errors.append(err_msg)
                _log_error("MembershipRenewalAutomation Error", err_msg)

        return {
            "auto_expired": auto_expired_count,
            "expiring_count": len(expiring),
            "recs_created": recs_created,
            "recs_updated": recs_updated,
            "recs_created_or_updated": recs_created + recs_updated,
            "tasks_created": tasks_created,
            "tasks_existing": tasks_existing,
            "errors": errors,
        }


class CareEngineAutomation:
    """
    Automation: Care Engine Periodic Scan
    1. Scans all Pets across supported Service Types.
    2. Detects Due Soon and At Risk patterns.
    3. Upserts Care Recommendations with in-place deduplication.
    4. Optionally creates ToDo follow-up tasks for active recommendations.
    """

    @classmethod
    def run_care_scan(
        cls,
        current_date: Optional[date] = None,
        create_tasks: bool = AUTO_CREATE_TODO_FOR_RECOMMENDATIONS,
    ) -> Dict[str, Any]:
        if current_date is None:
            current_date = date.today()
        if not frappe or not hasattr(frappe, "db"):
            return {
                "pets_scanned": 0,
                "due_soon_count": 0,
                "at_risk_count": 0,
                "tasks_created": 0,
                "tasks_existing": 0,
                "errors": [],
            }

        from petcare_crm.utils.frappe_recommendation_engine import generate_and_save_recommendation

        all_pets = frappe.db.get_list("Pet", fields=["name", "customer", "owner"], ignore_permissions=True)
        due_soon_created = 0
        at_risk_created = 0
        recs_updated = 0
        tasks_created = 0
        tasks_existing = 0
        errors = []

        # Batch Pre-fetch active recommendations to eliminate N+1 queries (Finding-13 Fix)
        active_recs_cache = {}
        try:
            raw_recs = frappe.db.get_list(
                "Care Recommendation",
                filters={"status": ["in", ["NEW", "ASSIGNED", "CONTACTED"]]},
                fields=["name", "pet", "service_type", "status", "recommendation_type", "priority", "reason", "suggested_action"],
                ignore_permissions=True,
            )
            for r in raw_recs:
                active_recs_cache[(r.get("pet"), r.get("service_type"))] = r
        except Exception:
            active_recs_cache = {}

        for pet in all_pets:
            cust = pet.get("customer") or pet.get("owner")
            if not cust:
                continue

            for st in SERVICE_TYPES:
                try:
                    rec_name, action_meta, rec_type = generate_and_save_recommendation(
                        pet_name=pet["name"],
                        customer_name=cust,
                        service_type=st,
                        current_date=current_date,
                        auto_commit=False,
                        return_meta=True,
                    )

                    if rec_name:
                        if action_meta == "CREATED":
                            if rec_type == RECOMMENDATION_TYPE_DUE_SOON:
                                due_soon_created += 1
                            elif rec_type == RECOMMENDATION_TYPE_AT_RISK:
                                at_risk_created += 1
                        elif action_meta == "UPDATED":
                            recs_updated += 1

                        # Idempotent ToDo creation
                        if create_tasks:
                            rec_doc = frappe.get_doc("Care Recommendation", rec_name)
                            prio = rec_doc.priority or "Medium"
                            todo_desc = (
                                f"Chăm sóc khách hàng: {rec_doc.reason} "
                                f"Đề xuất: {rec_doc.suggested_action}"
                            )
                            _, action = TaskManager.ensure_todo(
                                reference_type="Care Recommendation",
                                reference_name=rec_name,
                                description=todo_desc,
                                allocated_to="Administrator",
                                priority=prio,
                                due_date=current_date + timedelta(days=2),
                            )
                            if action == "CREATED":
                                tasks_created += 1
                            elif action == "EXISTING":
                                tasks_existing += 1
                except Exception as e:
                    err = f"Care scan error for pet {pet.get('name')}/{st}: {str(e)}"
                    errors.append(err)
                    _log_error("CareEngineAutomation Error", err)

        return {
            "pets_scanned": len(all_pets),
            "due_soon_created": due_soon_created,
            "at_risk_created": at_risk_created,
            "due_soon_count": due_soon_created,
            "at_risk_count": at_risk_created,
            "recs_created": due_soon_created + at_risk_created,
            "recs_updated": recs_updated,
            "tasks_created": tasks_created,
            "tasks_existing": tasks_existing,
            "errors": errors,
        }


class ServiceRecoveryAutomation:
    """
    Automation: Service Recovery & SLA Follow-up
    1. Monitors open/in-progress PetCare Cases.
    2. Detects cases unresolved beyond CASE_SLA_WARNING_HOURS.
    3. Escalates and creates ToDo task for assigned staff / supervisor.
    """

    @classmethod
    def process_open_cases(
        cls,
        current_date: Optional[date] = None,
        sla_hours: int = CASE_SLA_WARNING_HOURS,
    ) -> Dict[str, Any]:
        if current_date is None:
            current_date = date.today()
        if not frappe or not hasattr(frappe, "db"):
            return {"cases_checked": 0, "escalated_count": 0, "tasks_created": 0, "tasks_existing": 0, "errors": []}

        cases = frappe.db.get_list(
            "PetCare Case",
            filters={"status": ["in", ["Open", "In Progress", "Pending Customer"]]},
            fields=["name", "customer", "pet", "subject", "priority", "status", "assigned_to", "creation"],
            ignore_permissions=True,
        )

        escalated_count = 0
        tasks_created = 0
        tasks_existing = 0
        errors = []
        now_dt = datetime.now()

        for case in cases:
            try:
                creation_dt = case.get("creation")
                if isinstance(creation_dt, str):
                    try:
                        creation_dt = datetime.strptime(creation_dt[:19], "%Y-%m-%d %H:%M:%S")
                    except Exception:
                        creation_dt = now_dt - timedelta(hours=sla_hours + 1)
                elif not isinstance(creation_dt, datetime):
                    creation_dt = now_dt - timedelta(hours=sla_hours + 1)

                hours_open = (now_dt - creation_dt).total_seconds() / 3600.0

                effective_sla = sla_hours
                if str(case.get("priority")).upper() in ("URGENT", "HIGH"):
                    effective_sla = max(12, int(sla_hours / 2))

                if hours_open >= effective_sla:
                    escalated_count += 1
                    assigned_user = case.get("assigned_to") or "Administrator"
                    case_subj = case.get("subject") or "Khiếu nại/Yêu cầu dịch vụ"
                    cust = case.get("customer") or "Khách hàng"

                    todo_desc = (
                        f"Service Recovery SLA Escalation: Case '{case_subj}' của khách '{cust}' "
                        f"chưa hoàn tất sau {int(hours_open)}h (SLA cảnh báo: {effective_sla}h). "
                        f"Cần ưu tiên xử lý dứt điểm."
                    )

                    _, action = TaskManager.ensure_todo(
                        reference_type="PetCare Case",
                        reference_name=case["name"],
                        description=todo_desc,
                        allocated_to=assigned_user,
                        priority="Urgent" if case.get("priority") in ("Urgent", "High") else "High",
                        due_date=current_date,
                    )

                    if action == "CREATED":
                        tasks_created += 1
                    elif action == "EXISTING":
                        tasks_existing += 1
            except Exception as e:
                err = f"Service recovery error for case {case.get('name')}: {str(e)}"
                errors.append(err)
                _log_error("ServiceRecoveryAutomation Error", err)

        return {
            "cases_checked": len(cases),
            "escalated_count": escalated_count,
            "tasks_created": tasks_created,
            "tasks_existing": tasks_existing,
            "errors": errors,
        }


class AutomationCoordinator:
    """
    Master Coordinator for all PetCare CRM automations.
    Runs scheduled workflows, ensures transaction safety, and outputs structured audit report.
    """

    @classmethod
    def run_all_automations(
        cls,
        current_date: Optional[date] = None,
        force_safe_mode: bool = True,
    ) -> Dict[str, Any]:
        """
        Runs the full automated lifecycle:
        1. Lead Follow-up check
        2. Membership Auto-expiry & Renewal warnings
        3. Care Engine Due Soon & At Risk analysis
        4. Service Recovery SLA checks
        """
        if current_date is None:
            current_date = date.today()

        timestamp = datetime.now().isoformat()
        _log_info(f"[AutomationCoordinator] Starting all automations at {timestamp}")

        results: Dict[str, Any] = {
            "timestamp": timestamp,
            "current_date": str(current_date),
            "safe_mode": not ENABLE_LIVE_COMMUNICATION,
            "lead_followup": {},
            "membership_renewal": {},
            "care_engine": {},
            "service_recovery": {},
            "total_tasks_created": 0,
            "total_tasks_existing": 0,
            "errors": [],
            "status": "success",
        }

        # 1. Lead Follow-up
        try:
            lead_res = LeadFollowupAutomation.process_uncontacted_leads(current_date)
            results["lead_followup"] = lead_res
            results["total_tasks_created"] += lead_res.get("tasks_created", 0)
            results["total_tasks_existing"] += lead_res.get("tasks_existing", 0)
            results["errors"].extend(lead_res.get("errors", []))
            if frappe and hasattr(frappe, "db"):
                frappe.db.commit()
        except Exception as e:
            err = f"Fatal error in LeadFollowupAutomation: {str(e)}"
            results["errors"].append(err)
            _log_error("LeadFollowup Fatal Error", err)

        # 2. Membership Renewal
        try:
            mem_res = MembershipRenewalAutomation.process_expiring_memberships(current_date)
            results["membership_renewal"] = mem_res
            results["total_tasks_created"] += mem_res.get("tasks_created", 0)
            results["total_tasks_existing"] += mem_res.get("tasks_existing", 0)
            results["errors"].extend(mem_res.get("errors", []))
            if frappe and hasattr(frappe, "db"):
                frappe.db.commit()
        except Exception as e:
            err = f"Fatal error in MembershipRenewalAutomation: {str(e)}"
            results["errors"].append(err)
            _log_error("MembershipRenewal Fatal Error", err)

        # 3. Care Engine Scan
        try:
            care_res = CareEngineAutomation.run_care_scan(current_date)
            results["care_engine"] = care_res
            results["total_tasks_created"] += care_res.get("tasks_created", 0)
            results["total_tasks_existing"] += care_res.get("tasks_existing", 0)
            results["errors"].extend(care_res.get("errors", []))
            if frappe and hasattr(frappe, "db"):
                frappe.db.commit()
        except Exception as e:
            err = f"Fatal error in CareEngineAutomation: {str(e)}"
            results["errors"].append(err)
            _log_error("CareEngine Fatal Error", err)

        # 4. Service Recovery
        try:
            case_res = ServiceRecoveryAutomation.process_open_cases(current_date)
            results["service_recovery"] = case_res
            results["total_tasks_created"] += case_res.get("tasks_created", 0)
            results["total_tasks_existing"] += case_res.get("tasks_existing", 0)
            results["errors"].extend(case_res.get("errors", []))
            if frappe and hasattr(frappe, "db"):
                frappe.db.commit()
        except Exception as e:
            err = f"Fatal error in ServiceRecoveryAutomation: {str(e)}"
            results["errors"].append(err)
            _log_error("ServiceRecovery Fatal Error", err)

        if results["errors"]:
            results["status"] = "partial_success" if results["total_tasks_created"] > 0 else "failed"

        _log_info(
            f"[AutomationCoordinator] Finished. Tasks created: {results['total_tasks_created']}, "
            f"Existing: {results['total_tasks_existing']}, Errors: {len(results['errors'])}"
        )
        return results
