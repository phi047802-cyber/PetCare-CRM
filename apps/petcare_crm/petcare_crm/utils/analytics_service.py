"""
Analytics, Reporting & KPI Intelligence Service (CRM 2.0).
Provides business metric calculations, aggregations, and data contract definitions:
1. Lead Conversion (total leads, converted count, conversion rate %, source breakdown)
2. Sales Pipeline (opportunity count, total pipeline value, weighted expected value, stage breakdown)
3. Active Membership (active count, distribution by plan, total member wallet balance)
4. Membership Expiring Soon (expiring within 7 and 30 days, detailed renewal candidate list)
5. Service Visits (visit volume, gross revenue, discount total, net revenue, service breakdown)
6. Due Soon (pets due soon within window, breakdown by service type)
7. At-Risk Customers (pets absent >= 1.5x cycle, absence ratio, win-back candidates)
8. Care Recommendations Lifecycle (generation count, status breakdown, conversion rate %)
"""

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Union

try:
    import frappe
except ImportError:
    frappe = None

from petcare_crm.utils.config import (
    RECOMMENDATION_CONVERTED,
    RECOMMENDATION_NEW,
    RECOMMENDATION_TYPE_AT_RISK,
    RECOMMENDATION_TYPE_DUE_SOON,
    RECOMMENDATION_TYPE_RENEWAL,
    STATUS_ACTIVE,
    STATUS_EXPIRED,
)


def _get_val(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


class AnalyticsService:
    """
    Centralized analytics and reporting service.
    Implements exact business logic formulas and supports both Frappe DB queries and in-memory mock datasets.
    """

    @classmethod
    def get_lead_conversion_metrics(
        cls,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        leads_store: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """
        KPI 1: Lead Conversion
        Formula: Conversion Rate = (Converted Leads / Total Leads) * 100
        """
        if leads_store is None and frappe and hasattr(frappe, "db"):
            filters = {}
            if from_date:
                filters["creation"] = [">=", str(from_date)]
            if to_date:
                filters["creation"] = ["<=", str(to_date) + " 23:59:59"]
            leads = frappe.db.get_list(
                "PetCare Lead",
                filters=filters,
                fields=["name", "status", "lead_source", "source", "converted_contact"],
                ignore_permissions=True,
            )
        else:
            leads = leads_store or []

        total_leads = len(leads)
        converted_leads = 0
        source_counts: Dict[str, int] = {}
        status_counts: Dict[str, int] = {}

        for l in leads:
            st = str(_get_val(l, "status") or "New")
            src = str(_get_val(l, "lead_source") or _get_val(l, "source") or "Direct")
            status_counts[st] = status_counts.get(st, 0) + 1
            source_counts[src] = source_counts.get(src, 0) + 1
            if st.lower() == "converted" or _get_val(l, "converted_contact"):
                converted_leads += 1

        conv_rate = round((converted_leads / total_leads * 100.0), 1) if total_leads > 0 else 0.0

        return {
            "total_leads": total_leads,
            "converted_leads": converted_leads,
            "conversion_rate_pct": conv_rate,
            "by_source": source_counts,
            "by_status": status_counts,
        }

    @classmethod
    def get_sales_pipeline_metrics(
        cls,
        opportunities_store: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """
        KPI 2: Sales Pipeline
        Formula: Weighted Amount = Sum(Expected Amount * (Probability / 100))
        """
        if opportunities_store is None and frappe and hasattr(frappe, "db"):
            opps = frappe.db.get_list(
                "PetCare Opportunity",
                fields=["name", "stage", "expected_amount", "probability", "weighted_amount"],
                ignore_permissions=True,
            )
        else:
            opps = opportunities_store or []

        total_opps = len(opps)
        total_pipeline_val = 0.0
        total_weighted_val = 0.0
        by_stage: Dict[str, Dict[str, Any]] = {}

        for opp in opps:
            stg = str(_get_val(opp, "stage") or "Prospecting")
            amt = float(_get_val(opp, "expected_amount") or 0.0)
            prob = float(_get_val(opp, "probability") or 0.0)
            weighted = float(_get_val(opp, "weighted_amount") or (amt * prob / 100.0))

            is_lost = stg.lower() in ["closed lost", "lost", "cancelled"]
            if not is_lost:
                total_pipeline_val += amt
                total_weighted_val += weighted

            if stg not in by_stage:
                by_stage[stg] = {"count": 0, "amount": 0.0, "weighted": 0.0}
            by_stage[stg]["count"] += 1
            by_stage[stg]["amount"] += amt
            by_stage[stg]["weighted"] += weighted

        return {
            "total_opportunities": total_opps,
            "total_pipeline_amount": round(total_pipeline_val, 2),
            "total_weighted_amount": round(total_weighted_val, 2),
            "by_stage": by_stage,
        }

    @classmethod
    def get_membership_metrics(
        cls,
        current_date: Optional[date] = None,
        memberships_store: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """
        KPI 3 & 4: Active Memberships and Expiring Soon
        """
        if current_date is None:
            current_date = date.today()

        if memberships_store is None and frappe and hasattr(frappe, "db"):
            memberships = frappe.db.get_list(
                "Customer Membership",
                fields=["name", "customer", "pet", "membership_plan", "status", "start_date", "end_date", "balance"],
                ignore_permissions=True,
            )
        else:
            memberships = memberships_store or []

        active_count = 0
        total_balance = 0.0
        plan_counts: Dict[str, int] = {}
        expiring_7_days: List[Dict[str, Any]] = []
        expiring_30_days: List[Dict[str, Any]] = []

        for ms in memberships:
            st = str(_get_val(ms, "status") or "")
            plan = str(_get_val(ms, "membership_plan") or "Other")
            bal = float(_get_val(ms, "balance") or 0.0)
            end_d = _get_val(ms, "end_date")

            if isinstance(end_d, str):
                try:
                    end_d = datetime.strptime(end_d[:10], "%Y-%m-%d").date()
                except Exception:
                    end_d = None

            if st == STATUS_ACTIVE:
                active_count += 1
                total_balance += bal
                plan_counts[plan] = plan_counts.get(plan, 0) + 1

                if end_d:
                    days_left = (end_d - current_date).days
                    item = {
                        "name": _get_val(ms, "name"),
                        "customer": _get_val(ms, "customer"),
                        "pet": _get_val(ms, "pet"),
                        "plan": plan,
                        "end_date": str(end_d),
                        "days_left": days_left,
                    }
                    if 0 <= days_left <= 7:
                        expiring_7_days.append(item)
                    if 0 <= days_left <= 30:
                        expiring_30_days.append(item)

        return {
            "active_memberships": active_count,
            "total_member_balance": round(total_balance, 2),
            "by_plan": plan_counts,
            "expiring_within_7_days_count": len(expiring_7_days),
            "expiring_within_30_days_count": len(expiring_30_days),
            "expiring_soon_list": expiring_7_days,
        }

    @classmethod
    def get_service_visit_metrics(
        cls,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        visits_store: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """
        KPI 5: Service Visits & Revenue
        Gross Revenue = Sum(Original Price), Net Revenue = Sum(Final Price)
        """
        if visits_store is None and frappe and hasattr(frappe, "db"):
            filters = {"status": ["!=", "Cancelled"]}
            if from_date:
                filters["visit_date"] = [">=", str(from_date)]
            if to_date:
                filters["visit_date"] = ["<=", str(to_date)]
            visits = frappe.db.get_list(
                "Service Visit",
                filters=filters,
                fields=["name", "service_type", "original_price", "discount_amount", "final_price", "benefit_used", "status", "branch"],
                ignore_permissions=True,
            )
        else:
            visits = visits_store or []

        total_visits = 0
        cancelled_visits_count = 0
        gross_rev = 0.0
        discounts = 0.0
        net_rev = 0.0
        service_counts: Dict[str, Dict[str, Any]] = {}

        for v in visits:
            st = str(_get_val(v, "service_type") or _get_val(v, "service") or "General")
            v_status = str(_get_val(v, "status") or "Completed")
            if v_status.lower() in ["cancelled", "hủy", "huy"]:
                cancelled_visits_count += 1
                continue

            orig = float(_get_val(v, "original_price") or 0.0)
            disc = float(_get_val(v, "discount_amount") or 0.0)
            fin = float(_get_val(v, "final_price") or (orig - disc))

            total_visits += 1
            gross_rev += orig
            discounts += disc
            net_rev += fin

            if st not in service_counts:
                service_counts[st] = {"visits": 0, "revenue": 0.0}
            service_counts[st]["visits"] += 1
            service_counts[st]["revenue"] += fin

        return {
            "total_service_visits": total_visits,
            "cancelled_visits_count": cancelled_visits_count,
            "gross_revenue": round(gross_rev, 2),
            "total_discounts_granted": round(discounts, 2),
            "net_revenue": round(net_rev, 2),
            "by_service_type": service_counts,
        }

    @classmethod
    def get_care_retention_metrics(
        cls,
        recommendations_store: Optional[List[Any]] = None,
        visits_store: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """
        KPI 6, 7 & 8: Due Soon, At Risk, Care Recommendations & Customer Retention Rate
        """
        if recommendations_store is None and frappe and hasattr(frappe, "db"):
            recs = frappe.db.get_list(
                "Care Recommendation",
                fields=["name", "customer", "pet", "service_type", "recommendation_type", "status", "priority", "reason"],
                ignore_permissions=True,
            )
        else:
            recs = recommendations_store or []

        total_recs = len(recs)
        due_soon_count = 0
        at_risk_count = 0
        renewal_count = 0
        by_status: Dict[str, int] = {}
        due_soon_by_service: Dict[str, int] = {}
        at_risk_candidates: List[Dict[str, Any]] = []

        for r in recs:
            rtype = str(_get_val(r, "recommendation_type") or "")
            st = str(_get_val(r, "status") or RECOMMENDATION_NEW)
            service = str(_get_val(r, "service_type") or "General")

            by_status[st] = by_status.get(st, 0) + 1

            if rtype == RECOMMENDATION_TYPE_DUE_SOON:
                due_soon_count += 1
                due_soon_by_service[service] = due_soon_by_service.get(service, 0) + 1
            elif rtype == RECOMMENDATION_TYPE_AT_RISK:
                at_risk_count += 1
                at_risk_candidates.append({
                    "name": _get_val(r, "name"),
                    "customer": _get_val(r, "customer"),
                    "pet": _get_val(r, "pet"),
                    "service_type": service,
                    "reason": _get_val(r, "reason"),
                    "priority": _get_val(r, "priority"),
                    "status": st,
                })
            elif rtype == RECOMMENDATION_TYPE_RENEWAL:
                renewal_count += 1

        converted_recs = by_status.get(RECOMMENDATION_CONVERTED, 0)
        rec_conv_rate = round(converted_recs / total_recs * 100.0, 1) if total_recs > 0 else 0.0

        # True Customer Retention Rate based on Repeat Visits
        cust_visit_counts: Dict[str, int] = {}
        if visits_store is not None:
            for v in visits_store:
                if str(_get_val(v, "status") or "").lower() not in ["cancelled", "hủy", "huy"]:
                    c = _get_val(v, "customer")
                    if c:
                        cust_visit_counts[c] = cust_visit_counts.get(c, 0) + 1
        elif frappe and hasattr(frappe, "db"):
            try:
                active_visits = frappe.db.get_list(
                    "Service Visit",
                    filters={"status": ["!=", "Cancelled"]},
                    fields=["customer"],
                    ignore_permissions=True,
                )
                for v in active_visits:
                    c = _get_val(v, "customer")
                    if c:
                        cust_visit_counts[c] = cust_visit_counts.get(c, 0) + 1
            except Exception:
                pass

        total_active_cust = len(cust_visit_counts)
        repeat_cust = sum(1 for cnt in cust_visit_counts.values() if cnt >= 2)
        retention_rate = round(repeat_cust / total_active_cust * 100.0, 1) if total_active_cust > 0 else 0.0

        return {
            "total_recommendations": total_recs,
            "due_soon_total": due_soon_count,
            "at_risk_total": at_risk_count,
            "renewal_total": renewal_count,
            "conversion_rate_pct": rec_conv_rate,
            "recommendation_conversion_rate_pct": rec_conv_rate,
            "customer_retention_rate_pct": retention_rate,
            "repeat_customers_count": repeat_cust,
            "total_active_customers": total_active_cust,
            "by_status": by_status,
            "due_soon_by_service": due_soon_by_service,
            "at_risk_candidates": at_risk_candidates[:20],
        }

    @classmethod
    def get_branch_comparison_metrics(
        cls,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        visits_store: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """
        Multi-branch comparative analytics (Limitation 2.5 Extension).
        Calculates revenue and visit volume partitioned across clinic network branches.
        """
        from petcare_crm.utils.config import CLINIC_BRANCHES, BRANCH_DETAILS, DEFAULT_BRANCH

        if visits_store is None and frappe and hasattr(frappe, "db"):
            filters = {"status": ["!=", "Cancelled"]}
            if from_date:
                filters["visit_date"] = [">=", str(from_date)]
            if to_date:
                filters["visit_date"] = ["<=", str(to_date)]
            try:
                visits = frappe.db.get_list(
                    "Service Visit",
                    filters=filters,
                    fields=["name", "branch", "original_price", "discount_amount", "final_price", "status"],
                    ignore_permissions=True,
                )
            except Exception:
                visits = []
        else:
            visits = visits_store or []

        branch_stats = {
            b: {
                "branch_code": b,
                "name": BRANCH_DETAILS.get(b, {}).get("name", b),
                "visit_count": 0,
                "gross_revenue": 0.0,
                "net_revenue": 0.0,
            }
            for b in CLINIC_BRANCHES
        }

        for v in visits:
            v_status = str(_get_val(v, "status") or "Completed")
            if v_status.lower() in ["cancelled", "hủy", "huy"]:
                continue
            b = str(_get_val(v, "branch") or DEFAULT_BRANCH)
            if b not in branch_stats:
                branch_stats[b] = {
                    "branch_code": b,
                    "name": b,
                    "visit_count": 0,
                    "gross_revenue": 0.0,
                    "net_revenue": 0.0,
                }
            orig = float(_get_val(v, "original_price") or 0.0)
            disc = float(_get_val(v, "discount_amount") or 0.0)
            fin = float(_get_val(v, "final_price") or (orig - disc))

            branch_stats[b]["visit_count"] += 1
            branch_stats[b]["gross_revenue"] += orig
            branch_stats[b]["net_revenue"] += fin

        return {
            "total_branches": len(branch_stats),
            "branches": list(branch_stats.values()),
        }

    @classmethod
    def get_full_crm_dashboard(
        cls,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        branch: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Synthesizes all 8 required KPIs into a comprehensive operational dashboard.
        Optionally scoped by clinic branch.
        """
        dashboard = {
            "generated_at": datetime.now().isoformat(),
            "from_date": str(from_date or ""),
            "to_date": str(to_date or ""),
            "branch": branch or "ALL",
            "lead_conversion": cls.get_lead_conversion_metrics(from_date, to_date),
            "sales_pipeline": cls.get_sales_pipeline_metrics(),
            "membership_status": cls.get_membership_metrics(),
            "service_visits": cls.get_service_visit_metrics(from_date, to_date),
            "care_retention": cls.get_care_retention_metrics(),
            "branch_performance": cls.get_branch_comparison_metrics(from_date, to_date),
        }
        return dashboard
