# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

from datetime import date
from typing import Any, Dict, List, Optional
import frappe
from frappe.utils import nowdate, getdate
from frappe import _

from petcare_crm.utils.exceptions import (
    PetCareException,
    ValidationError,
    EntityNotFoundException,
    BenefitExhaustedException,
    MembershipExpiredException,
)
from petcare_crm.utils.membership_service import MembershipService


class ServiceCatalogService:
    """Service layer for PetCare Service Catalog management."""

    @staticmethod
    def get_active_services(species: Optional[str] = None) -> List[Dict[str, Any]]:
        """Truy xuất danh mục dịch vụ đang kinh doanh, có thể lọc theo loài."""
        filters = {"is_active": 1}
        services = frappe.get_all(
            "PetCare Service",
            filters=filters,
            fields=[
                "name", "service_code", "service_name", "category",
                "standard_price", "default_cycle_days", "target_species", "estimated_duration_minutes"
            ],
            order_by="service_code asc"
        )
        if species:
            services = [s for s in services if s.target_species in ["All", species]]
        return services

    @staticmethod
    def get_service(service_code_or_name: str) -> Optional[Dict[str, Any]]:
        """Tìm kiếm dịch vụ theo mã hoặc tên."""
        if not service_code_or_name:
            return None

        # 1. Tìm theo service_code (PK)
        if frappe.db.exists("PetCare Service", service_code_or_name):
            return frappe.get_cached_doc("PetCare Service", service_code_or_name).as_dict()

        # 2. Tìm theo service_name
        by_name = frappe.db.get_value(
            "PetCare Service",
            {"service_name": service_code_or_name},
            ["name", "service_code", "service_name", "category", "standard_price", "default_cycle_days"],
            as_dict=True
        )
        return by_name

    @staticmethod
    def create_service(
        service_code: str,
        service_name: str,
        category: str,
        standard_price: float,
        default_cycle_days: int = 30,
        target_species: str = "All",
        estimated_duration_minutes: int = 60,
        description: Optional[str] = None,
    ) -> str:
        """Đăng ký mới một dịch vụ trong danh mục chuẩn."""
        code = str(service_code).strip().upper()
        if frappe.db.exists("PetCare Service", code):
            raise ValidationError(f"Mã dịch vụ '{code}' đã tồn tại trong danh mục.")

        doc = frappe.get_doc({
            "doctype": "PetCare Service",
            "service_code": code,
            "service_name": service_name.strip(),
            "category": category,
            "standard_price": float(standard_price),
            "default_cycle_days": int(default_cycle_days or 30),
            "target_species": target_species or "All",
            "estimated_duration_minutes": int(estimated_duration_minutes or 60),
            "description": description,
            "is_active": 1,
        })
        doc.insert(ignore_permissions=True)
        return doc.name


class ServiceVisitService:
    """Service layer for Service Visit operations, pricing, and benefit redemptions."""

    @staticmethod
    def create_service_visit(
        pet: str,
        service_identifier: str,
        visit_date: Optional[str] = None,
        technician: Optional[str] = None,
        notes: Optional[str] = None,
        weight_kg: Optional[float] = None,
        membership_id: Optional[str] = None,
        override_discount: Optional[float] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Ghi nhận một lượt dịch vụ thực tế cho thú cưng với Transaction Safety & Idempotency:
        - Kiểm tra Idempotency key tránh double-redeem khi retry
        - Khóa Pessimistic (for_update) chống race condition đồng thời
        - Cấn trừ quyền lợi hội viên và ghi nhận Audit Ledger
        - Tự động hoàn tác nếu có bất kỳ lỗi nào xảy ra (Atomic Transaction)
        """
        if not pet:
            raise ValidationError("Thú cưng (pet) là bắt buộc.")
        if not frappe.db.exists("Pet", pet):
            raise EntityNotFoundException(f"Không tìm thấy thú cưng với tên '{pet}'.")

        # 1. Kiểm tra Idempotency Key chống gọi trùng lặp (Idempotency Protection)
        if idempotency_key and frappe.db.exists("DocType", "Benefit Redemption Ledger"):
            existing_ledger = frappe.db.get_value(
                "Benefit Redemption Ledger",
                {"idempotency_key": idempotency_key},
                ["service_visit", "membership", "benefit_type", "discount_applied"],
                as_dict=True
            )
            if existing_ledger and frappe.db.exists("Service Visit", existing_ledger.service_visit):
                v_doc = frappe.get_doc("Service Visit", existing_ledger.service_visit)
                return {
                    "status": "success",
                    "visit_id": v_doc.name,
                    "pet": v_doc.pet,
                    "customer": v_doc.customer,
                    "service_type": v_doc.service_type,
                    "original_price": v_doc.original_price,
                    "discount_amount": v_doc.discount_amount,
                    "final_price": v_doc.final_price,
                    "membership_used": v_doc.membership,
                    "benefit_used": v_doc.benefit_used,
                    "is_idempotent_replay": True,
                }

        customer = frappe.db.get_value("Pet", pet, "customer")
        if not customer:
            raise ValidationError(f"Thú cưng '{pet}' chưa được gán chủ sở hữu (customer).")

        # Tra cứu dịch vụ
        srv = ServiceCatalogService.get_service(service_identifier)
        if srv:
            service_ref = srv.get("service_code") or srv.get("name")
            service_type_name = srv.get("service_name")
            original_price = float(srv.get("standard_price") or 0.0)
        else:
            service_ref = None
            service_type_name = service_identifier
            original_price = 200000.0

        v_date = getdate(visit_date) if visit_date else getdate(nowdate())

        try:
            # 2. Tra cứu Thẻ hội viên với Pessimistic Lock (for_update) chống xung đột đồng thời
            membership_doc = None
            benefit_used = None
            discount_type_applied = None
            discount_amount = 0.0
            final_price = original_price

            target_mem_id = membership_id
            if not target_mem_id:
                # Tìm thẻ Active của khách hàng
                active_mem_id = frappe.db.get_value(
                    "Customer Membership",
                    {
                        "customer": customer,
                        "status": "Active",
                        "start_date": ["<=", str(v_date)],
                        "end_date": [">=", str(v_date)],
                    },
                    "name"
                )
                if active_mem_id:
                    target_mem_id = active_mem_id

            if target_mem_id and frappe.db.exists("Customer Membership", target_mem_id):
                # Khóa dòng trong MariaDB để ngăn 2 request đồng thời trừ cùng 1 lượt
                try:
                    membership_doc = frappe.get_doc("Customer Membership", target_mem_id, for_update=True)
                except Exception:
                    membership_doc = frappe.get_doc("Customer Membership", target_mem_id)

                if membership_doc.status != "Active":
                    if membership_id:  # Khách cố ý chỉ định thẻ đã hết hạn
                        raise MembershipExpiredException(f"Thẻ hội viên '{target_mem_id}' có trạng thái là '{membership_doc.status}', không thể sử dụng.")
                    membership_doc = None

            # 3. Phân tích quyền lợi và Thứ tự ưu tiên (FREE > PERCENTAGE > FIXED)
            if membership_doc and membership_doc.status == "Active":
                # Kiểm tra thẻ gia đình hay thẻ riêng của bé
                if not membership_doc.pet or membership_doc.pet == pet:
                    candidate_benefits = []
                    for b in membership_doc.benefits:
                        if b.benefit_type and (
                            b.benefit_type.lower() in service_type_name.lower() or
                            service_type_name.lower() in b.benefit_type.lower()
                        ):
                            candidate_benefits.append(b)

                    # Sắp xếp candidate benefits theo thứ tự ưu tiên: FREE (3) > PERCENTAGE (2) > FIXED (1)
                    priority_map = {"FREE": 3, "PERCENTAGE": 2, "FIXED": 1}
                    candidate_benefits.sort(key=lambda x: priority_map.get(getattr(x, "discount_type", "FREE"), 0), reverse=True)

                    if candidate_benefits:
                        matched_benefit = candidate_benefits[0]
                        rem_qty = (matched_benefit.total_quantity or 0) - (matched_benefit.used_quantity or 0)

                        if rem_qty <= 0:
                            if membership_id:
                                raise BenefitExhaustedException(f"Quyền lợi '{matched_benefit.benefit_type}' trong thẻ đã dùng hết (remaining = 0).")
                        else:
                            benefit_used = matched_benefit.benefit_type
                            disc_type = matched_benefit.discount_type or "FREE"
                            discount_type_applied = disc_type
                            disc_val = float(matched_benefit.discount_value or 0.0)

                            if disc_type == "FREE":
                                final_price = 0.0
                                discount_amount = original_price
                            elif disc_type == "PERCENTAGE":
                                discount_amount = original_price * (disc_val / 100.0)
                                final_price = max(0.0, original_price - discount_amount)
                            elif disc_type == "FIXED":
                                discount_amount = min(original_price, disc_val)
                                final_price = max(0.0, original_price - discount_amount)

                            # Trừ 1 lượt quyền lợi trong thẻ
                            matched_benefit.used_quantity = (matched_benefit.used_quantity or 0) + 1
                            matched_benefit.remaining_quantity = (matched_benefit.total_quantity or 0) - matched_benefit.used_quantity
                            membership_doc.save(ignore_permissions=True)

            # Override discount nếu có
            if override_discount is not None and override_discount > 0:
                discount_amount = min(original_price, float(override_discount))
                final_price = max(0.0, original_price - discount_amount)

            # Giới hạn an toàn: Final price không được âm
            final_price = max(0.0, float(final_price))
            discount_amount = max(0.0, original_price - final_price)

            # 4. Tạo bản ghi Service Visit
            visit_doc = frappe.get_doc({
                "doctype": "Service Visit",
                "pet": pet,
                "customer": customer,
                "service": service_ref,
                "service_type": service_type_name,
                "visit_date": str(v_date),
                "original_price": original_price,
                "discount_amount": discount_amount,
                "final_price": final_price,
                "membership": membership_doc.name if membership_doc else None,
                "benefit_used": benefit_used,
                "technician": technician,
                "weight_kg": float(weight_kg) if weight_kg else None,
                "notes": notes,
                "status": "Completed",
            })
            visit_doc.insert(ignore_permissions=True)

            # 5. Tạo bản ghi Audit trong Benefit Redemption Ledger nếu có cấn trừ
            if membership_doc and benefit_used and frappe.db.exists("DocType", "Benefit Redemption Ledger"):
                frappe.get_doc({
                    "doctype": "Benefit Redemption Ledger",
                    "membership": membership_doc.name,
                    "service_visit": visit_doc.name,
                    "benefit_type": benefit_used,
                    "discount_type": discount_type_applied or "FREE",
                    "quantity_redeemed": 1,
                    "discount_applied": discount_amount,
                    "status": "Applied",
                    "idempotency_key": idempotency_key,
                }).insert(ignore_permissions=True)

            # 6. Cập nhật cân nặng mới cho Pet
            if weight_kg and float(weight_kg) > 0:
                frappe.db.set_value("Pet", pet, "weight_kg", float(weight_kg))

            frappe.db.commit()

            return {
                "status": "success",
                "visit_id": visit_doc.name,
                "pet": pet,
                "customer": customer,
                "service_type": service_type_name,
                "original_price": original_price,
                "discount_amount": discount_amount,
                "final_price": final_price,
                "membership_used": membership_doc.name if membership_doc else None,
                "benefit_used": benefit_used,
            }

        except Exception as e:
            frappe.db.rollback()
            raise e


class CaseManagementService:
    """Service layer for Customer Service Requests and Post-visit Issues (PetCare Case)."""

    @staticmethod
    def create_case(
        customer: str,
        subject: str,
        description: str,
        pet: Optional[str] = None,
        service_visit: Optional[str] = None,
        case_type: str = "Feedback",
        priority: str = "Medium",
        assigned_to: Optional[str] = None,
    ) -> str:
        """Tạo yêu cầu hỗ trợ hoặc phản hồi sau dịch vụ."""
        if not customer:
            raise ValidationError("Khách hàng (customer) là bắt buộc.")
        if not subject or not subject.strip():
            raise ValidationError("Tiêu đề yêu cầu (subject) không được để trống.")
        if not description or not description.strip():
            raise ValidationError("Nội dung chi tiết (description) không được để trống.")

        case_doc = frappe.get_doc({
            "doctype": "PetCare Case",
            "customer": customer,
            "pet": pet,
            "service_visit": service_visit,
            "subject": subject.strip(),
            "description": description.strip(),
            "case_type": case_type or "Feedback",
            "priority": priority or "Medium",
            "status": "New",
            "assigned_to": assigned_to or (frappe.session.user if frappe.session.user else "Administrator"),
        })
        case_doc.insert(ignore_permissions=True)
        return case_doc.name

    @staticmethod
    def update_case_status(
        case_id: str,
        new_status: str,
        resolution: Optional[str] = None,
    ) -> bool:
        """Cập nhật trạng thái xử lý Case (New -> In Progress -> Resolved -> Closed)."""
        if not frappe.db.exists("PetCare Case", case_id):
            raise EntityNotFoundException(f"Không tìm thấy Case với mã '{case_id}'.")

        case_doc = frappe.get_doc("PetCare Case", case_id)

        if new_status in ["Resolved", "Closed"] and not (resolution and resolution.strip()):
            raise ValidationError("Vui lòng nhập phương án xử lý (resolution) trước khi hoàn tất Case.")

        case_doc.status = new_status
        if resolution:
            case_doc.resolution = resolution.strip()
        case_doc.save(ignore_permissions=True)
        return True

    @staticmethod
    def get_cases_for_customer(customer: str) -> List[Dict[str, Any]]:
        """Truy xuất danh sách phản hồi/khiếu nại của một khách hàng."""
        return frappe.get_all(
            "PetCare Case",
            filters={"customer": customer},
            fields=["name", "subject", "case_type", "priority", "status", "pet", "creation", "resolution"],
            order_by="creation desc"
        )


class MembershipLifecycleService:
    """Service layer for Membership Renewal with rollover allowance and audit safety."""

    @staticmethod
    def renew_membership(
        old_membership_id: str,
        new_plan_name: str,
        allow_rollover: bool = True,
    ) -> Dict[str, Any]:
        """
        Gia hạn thẻ hội viên an toàn:
        - Kế thừa số lượt chưa dùng từ thẻ cũ (Rollover Allowance) nếu allow_rollover=True
        - Chuyển giao số dư ví trả trước (Wallet Balance)
        - Đánh dấu thẻ cũ là Renewed
        - Đảm bảo lịch sử các lần redeem cũ không bị thay đổi (Immutable History)
        """
        if not frappe.db.exists("Customer Membership", old_membership_id):
            raise EntityNotFoundException(f"Không tìm thấy thẻ hội viên cũ '{old_membership_id}'.")

        old_ms = frappe.get_doc("Customer Membership", old_membership_id, for_update=True)
        if not frappe.db.exists("Membership Plan", new_plan_name):
            raise EntityNotFoundException(f"Gói hội viên mới '{new_plan_name}' không tồn tại.")

        new_plan = frappe.get_doc("Membership Plan", new_plan_name)

        # Tính toán quyền lợi chuyển giao (Rollover)
        remaining_old = {}
        if allow_rollover:
            for b in old_ms.benefits:
                rem = (b.total_quantity or 0) - (b.used_quantity or 0)
                if rem > 0 and b.benefit_type:
                    remaining_old[b.benefit_type.lower()] = rem

        # Tạo danh sách benefits cho thẻ mới
        from datetime import timedelta
        new_start_date = date.today()
        new_end_date = new_start_date + timedelta(days=int(new_plan.validity_days or 365))

        new_benefits = []
        rollover_summary = []
        for pb in new_plan.benefits:
            b_type = pb.benefit_type
            carried_over = remaining_old.get(b_type.lower(), 0) if allow_rollover else 0
            total_qty = int(pb.total_quantity or 0) + carried_over

            new_benefits.append({
                "benefit_type": b_type,
                "total_quantity": total_qty,
                "used_quantity": 0,
                "remaining_quantity": total_qty,
                "discount_type": pb.discount_type or "FREE",
                "discount_value": pb.discount_value or 0,
            })
            if carried_over > 0:
                rollover_summary.append(f"{b_type}: +{carried_over} lượt")

        transferred_balance = float(old_ms.balance or 0.0)

        # Tạo thẻ hội viên mới
        new_ms = frappe.get_doc({
            "doctype": "Customer Membership",
            "customer": old_ms.customer,
            "pet": old_ms.pet,
            "membership_plan": new_plan_name,
            "start_date": str(new_start_date),
            "end_date": str(new_end_date),
            "status": "Active",
            "balance": transferred_balance,
            "benefits": new_benefits,
        })
        new_ms.insert(ignore_permissions=True)

        # Cập nhật trạng thái thẻ cũ sang Renewed và xóa số dư đã chuyển
        old_ms.status = "Renewed"
        old_ms.balance = 0.0
        old_ms.save(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "old_membership": old_ms.name,
            "new_membership": new_ms.name,
            "rollover_summary": rollover_summary,
            "transferred_balance": transferred_balance,
            "new_end_date": str(new_end_date),
        }

