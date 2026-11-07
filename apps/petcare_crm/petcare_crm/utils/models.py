"""
Re-export and define dataclasses for use across utils and adapters.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from petcare_crm.utils.config import (
    DISCOUNT_TYPE_FREE,
    STATUS_ACTIVE,
    STATUS_EXPIRED,
)


@dataclass
class ServiceVisit:
    pet: str
    customer: str
    service_type: str
    visit_date: date
    original_price: float = 0.0
    final_price: float = 0.0
    membership: Optional[str] = None
    benefit_used: Optional[str] = None
    notes: Optional[str] = None
    name: Optional[str] = None


@dataclass
class MembershipBenefit:
    benefit_type: str
    total_quantity: int
    used_quantity: int = 0
    remaining_quantity: int = 0
    discount_type: str = DISCOUNT_TYPE_FREE
    discount_value: float = 100.0
    name: Optional[str] = None

    def __post_init__(self):
        if self.remaining_quantity == 0 and self.used_quantity == 0:
            self.remaining_quantity = self.total_quantity
        elif self.remaining_quantity == 0 and self.used_quantity > 0:
            self.remaining_quantity = max(0, self.total_quantity - self.used_quantity)

    def redeem(self, count: int = 1) -> None:
        if self.remaining_quantity < count:
            raise ValueError(f"Cannot redeem {count}. Remaining is {self.remaining_quantity}")
        self.used_quantity += count
        self.remaining_quantity -= count


@dataclass
class Membership:
    name: str
    customer: str
    membership_plan: str
    start_date: date
    end_date: date
    pet: Optional[str] = None
    status: str = STATUS_ACTIVE
    benefits: List[MembershipBenefit] = field(default_factory=list)

    def is_active(self, check_date: Optional[date] = None) -> bool:
        if check_date is None:
            check_date = date.today()
        if str(self.status).upper() != "ACTIVE":
            return False
        if self.start_date and check_date < self.start_date:
            return False
        if self.end_date and check_date > self.end_date:
            return False
        return True


@dataclass
class Pet:
    pet_name: str
    customer: str
    species: Optional[str] = None
    breed: Optional[str] = None
    birth_date: Optional[date] = None
    weight_kg: Optional[float] = None
    notes: Optional[str] = None
    name: Optional[str] = None

    def __post_init__(self):
        if not self.name:
            self.name = self.pet_name


@dataclass
class Customer:
    name: str
    customer_name: Optional[str] = None


@dataclass
class PatternResult:
    pet: str
    service_type: str
    number_of_visits: int
    last_visit_date: Optional[date] = None
    raw_deltas: List[int] = field(default_factory=list)
    filtered_deltas: List[int] = field(default_factory=list)
    outliers_detected: List[int] = field(default_factory=list)
    typical_interval: Optional[float] = None
    arithmetic_mean: Optional[float] = None
    median_interval: Optional[float] = None
    data_sufficiency: str = "INSUFFICIENT"
    confidence: str = "NONE"
    insufficient_data: bool = True
    reason: str = ""


@dataclass
class PredictionResult:
    pet: str
    service_type: str
    predicted_next_visit: Optional[date] = None
    average_interval: Optional[float] = None
    last_visit_date: Optional[date] = None
    number_of_visits: int = 0
    confidence: str = "NONE"
    insufficient_data: bool = True
    is_rule_based_estimate: bool = True
    disclaimer: str = "Dự đoán mang tính chất tham khảo dựa trên tần suất lịch sử, không phải lịch hẹn đã xác nhận."
    reason: str = ""
    seasonal_factor: float = 1.0
    age_factor: float = 1.0
    adjusted_interval: Optional[float] = None


@dataclass
class DueSoonResult:
    pet: str
    service_type: str
    status: str = "UNKNOWN"
    is_due_soon: bool = False
    predicted_date: Optional[date] = None
    days_until_due: Optional[int] = None
    days_since_last_visit: Optional[int] = None
    threshold_days: int = 5
    effective_threshold: int = 5
    reason: str = ""


@dataclass
class AtRiskResult:
    pet: str
    service_type: str
    status: str = "UNKNOWN"
    is_at_risk: bool = False
    average_interval: Optional[float] = None
    days_since_last_visit: Optional[int] = None
    absence_ratio: Optional[float] = None
    last_visit_date: Optional[date] = None
    threshold_ratio: float = 1.5
    reason: str = ""


@dataclass
class RiskEvaluationResult:
    pet: str
    service_type: str
    overall_status: str = "INSUFFICIENT_DATA"
    due_soon: Optional[DueSoonResult] = None
    at_risk: Optional[AtRiskResult] = None
    pattern: Optional[PatternResult] = None
    prediction: Optional[PredictionResult] = None


@dataclass
class CareRecommendationDTO:
    customer: str
    pet: str
    service_type: str
    recommendation_type: str
    recommendation_date: date
    priority: str = "Medium"
    reason: str = ""
    suggested_action: str = ""
    status: str = "NEW"
    membership: Optional[str] = None
    name: Optional[str] = None
    action_taken: str = "CREATED"
