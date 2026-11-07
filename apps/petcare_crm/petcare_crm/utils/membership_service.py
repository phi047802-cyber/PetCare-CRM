"""
Ported from Flask project. Adapted for Frappe Framework.
Business logic unchanged. DB layer replaced by Frappe ORM via frappe_adapters.py.
"""

from datetime import date
from typing import Any, Dict, List, Optional
from petcare_crm.utils.config import (
    DISCOUNT_TYPE_FIXED,
    DISCOUNT_TYPE_FREE,
    DISCOUNT_TYPE_PERCENTAGE,
    STATUS_ACTIVE,
    STATUS_EXPIRED,
)
from petcare_crm.utils.exceptions import (
    BenefitExhaustedException,
    BenefitNotFoundException,
    InvalidPriceException,
    MembershipExpiredException,
    MembershipNotActiveException,
)


def _get_val(obj: Any, key: str, default: Any = None) -> Any:
    """Helper to access attribute from object or dict."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _is_membership_active(membership: Any, check_date: date) -> bool:
    """Helper to check if membership is active on check_date."""
    if membership is None:
        return False
    if hasattr(membership, "is_active") and callable(membership.is_active):
        return membership.is_active(check_date)
    
    status = _get_val(membership, "status")
    start_date = _get_val(membership, "start_date")
    end_date = _get_val(membership, "end_date")

    if not status or str(status).strip().lower() != STATUS_ACTIVE.lower():
        return False
    if start_date and check_date < start_date:
        return False
    if end_date and check_date > end_date:
        return False
    return True


class MembershipService:
    """Service layer for PetCare Membership & Benefit Management."""

    @staticmethod
    def get_active_membership(
        customer: str,
        pet: Optional[str] = None,
        check_date: Optional[date] = None,
        memberships_store: Optional[List[Any]] = None,
    ) -> Optional[Any]:
        """
        Find active membership for customer (and optionally pet) valid on check_date.
        """
        if check_date is None:
            check_date = date.today()

        if memberships_store is None:
            memberships_store = []

        active_memberships = []
        for ms in memberships_store:
            ms_customer = _get_val(ms, "customer")
            ms_pet = _get_val(ms, "pet")

            if ms_customer != customer:
                continue
            if pet and ms_pet and ms_pet != pet:
                continue
            if _is_membership_active(ms, check_date):
                active_memberships.append(ms)

        if not active_memberships:
            return None

        # Return the latest active membership if multiple exist
        def get_end_date(m):
            ed = _get_val(m, "end_date")
            return ed if ed is not None else date.min

        active_memberships.sort(key=get_end_date, reverse=True)
        return active_memberships[0]

    @staticmethod
    def get_remaining_benefit(
        membership: Any,
        service_type: str,
    ) -> Optional[Any]:
        """
        Find benefit matching service_type in membership.
        """
        if not membership:
            return None

        benefits = _get_val(membership, "benefits") or []
        for benefit in benefits:
            benefit_type = _get_val(benefit, "benefit_type", "")
            if benefit_type.lower() == service_type.lower():
                return benefit

        return None

    @classmethod
    def apply_membership_benefit(
        cls,
        membership: Optional[Any],
        service_type: str,
        original_price: float,
        check_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Calculate discount and final price given membership, service_type, and original_price.
        Returns detailed breakdown dict.
        """
        if original_price < 0:
            raise InvalidPriceException(f"Original price ({original_price}) cannot be negative.")

        if check_date is None:
            check_date = date.today()

        ms_name = _get_val(membership, "name") if membership else None
        ms_status = _get_val(membership, "status") if membership else None

        result = {
            "applied": False,
            "membership": ms_name,
            "benefit_used": None,
            "discount_type": None,
            "original_price": float(original_price),
            "membership_discount": 0.0,
            "final_price": float(original_price),
            "reason": "No active membership provided or benefit available.",
        }

        if not membership:
            return result

        if not _is_membership_active(membership, check_date):
            if str(ms_status).upper() != "ACTIVE":
                result["reason"] = f"Membership status is {ms_status}."
            else:
                result["reason"] = f"Membership not active on date {check_date}."
            return result

        benefit = cls.get_remaining_benefit(membership, service_type)
        if not benefit:
            result["reason"] = f"No benefit found for service type '{service_type}'."
            return result

        rem_qty = _get_val(benefit, "remaining_quantity", 0)
        if rem_qty <= 0:
            result["reason"] = f"Benefit '{service_type}' has 0 remaining quantity."
            return result

        # Apply benefit pricing rules
        discount = 0.0
        disc_type = _get_val(benefit, "discount_type")
        disc_val = float(_get_val(benefit, "discount_value", 0.0))

        if disc_type == DISCOUNT_TYPE_FREE:
            discount = original_price
        elif disc_type == DISCOUNT_TYPE_PERCENTAGE:
            discount = original_price * (disc_val / 100.0)
        elif disc_type == DISCOUNT_TYPE_FIXED:
            discount = min(original_price, disc_val)

        discount = round(discount, 2)
        final_price = cls.calculate_final_price(original_price, discount)

        benefit_name = _get_val(benefit, "name") or _get_val(benefit, "benefit_type")

        result.update(
            {
                "applied": True,
                "benefit_used": benefit_name,
                "benefit": benefit,
                "discount_type": disc_type,
                "membership_discount": discount,
                "final_price": final_price,
                "reason": f"Applied {disc_type} benefit for '{service_type}'.",
            }
        )
        return result

    @staticmethod
    def calculate_final_price(original_price: float, discount: float) -> float:
        """Calculate final_price = max(0.0, original_price - discount)."""
        if original_price < 0:
            raise InvalidPriceException(f"Original price ({original_price}) cannot be negative.")
        if discount < 0:
            raise InvalidPriceException(f"Discount ({discount}) cannot be negative.")
        if discount > original_price:
            raise InvalidPriceException(f"Discount ({discount}) cannot exceed original price ({original_price}).")
        return round(max(0.0, original_price - discount), 2)

    @classmethod
    def redeem_benefit(
        cls,
        membership: Any,
        service_type: str,
        count: int = 1,
        check_date: Optional[date] = None,
    ) -> Any:
        """
        Redeem count of benefit from membership.
        Updates used_quantity and remaining_quantity atomically.
        """
        if check_date is None:
            check_date = date.today()

        ms_status = _get_val(membership, "status")
        ms_end = _get_val(membership, "end_date")
        ms_plan = _get_val(membership, "membership_plan", "")

        if not _is_membership_active(membership, check_date):
            ms_status_str = str(ms_status).strip().lower() if ms_status else ""
            if ms_status_str == STATUS_EXPIRED.lower() or (ms_end and check_date > ms_end):
                raise MembershipExpiredException(
                    f"Cannot redeem benefit. Membership expired (status={ms_status}, end_date={ms_end})."
                )
            if ms_status_str != STATUS_ACTIVE.lower():
                raise MembershipNotActiveException(
                    f"Cannot redeem benefit. Membership status is {ms_status}."
                )
            raise MembershipExpiredException(
                f"Cannot redeem benefit. Membership not yet active on check_date {check_date}."
            )

        benefit = cls.get_remaining_benefit(membership, service_type)
        if not benefit:
            raise BenefitNotFoundException(
                f"Benefit for service type '{service_type}' not found on membership '{ms_plan}'."
            )

        rem_qty = _get_val(benefit, "remaining_quantity", 0)
        if rem_qty < count:
            raise BenefitExhaustedException(
                f"Cannot redeem {count} of '{service_type}'. Remaining quantity is {rem_qty}."
            )

        if hasattr(benefit, "redeem") and callable(benefit.redeem):
            benefit.redeem(count)
        else:
            used = _get_val(benefit, "used_quantity", 0) + count
            rem = rem_qty - count
            if isinstance(benefit, dict):
                benefit["used_quantity"] = used
                benefit["remaining_quantity"] = rem
            else:
                setattr(benefit, "used_quantity", used)
                setattr(benefit, "remaining_quantity", rem)

        return benefit
