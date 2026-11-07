"""
Ported from Flask project. Adapted for Frappe Framework.
Business logic unchanged. DB layer replaced by Frappe ORM via frappe_adapters.py.
"""

from typing import Dict, TypedDict

# Care Pattern Engine Global Thresholds (Fallbacks)
DUE_SOON_THRESHOLD_DAYS: int = 5
AT_RISK_RATIO: float = 1.5
MIN_VISITS_FOR_INTERVAL: int = 3
MIN_VISITS_FOR_FIRST_INTERVAL: int = 2
RECOMMENDATION_DEDUP_WINDOW_DAYS: int = 14
DEDUP_WINDOW_DAYS: int = RECOMMENDATION_DEDUP_WINDOW_DAYS
EWMA_ALPHA: float = 0.6

# Automation & Workflow Configurations (Prompt 7)
LEAD_UNCONTACTED_THRESHOLD_HOURS: int = 24       # Cảnh báo lead chưa liên hệ sau 24h
MEMBERSHIP_EXPIRATION_WARNING_DAYS: int = 7     # Cảnh báo gói hội viên sắp hết hạn trước 7 ngày
CASE_SLA_WARNING_HOURS: int = 48                # Cảnh báo Case chưa giải quyết sau 48h
ENABLE_LIVE_COMMUNICATION: bool = False         # Safe Mode: Không gửi email/WhatsApp thật trong demo
AUTO_CREATE_TODO_FOR_RECOMMENDATIONS: bool = True # Tự động tạo ToDo task cho nhân viên chăm sóc

# Supported Service Types (CRM 2.0 Engine)
SERVICE_TYPES = ["Grooming", "Spa", "Nail Care", "Vaccination"]


class ServiceThreshold(TypedDict):
    due_soon_days: int
    at_risk_ratio: float


# Service-Specific Threshold Matrix (CRM 2.0 Engine)
SERVICE_THRESHOLDS: Dict[str, ServiceThreshold] = {
    "grooming": {"due_soon_days": 5, "at_risk_ratio": 1.3},
    "spa": {"due_soon_days": 7, "at_risk_ratio": 1.6},
    "nail care": {"due_soon_days": 3, "at_risk_ratio": 1.4},
    "vaccination": {"due_soon_days": 14, "at_risk_ratio": 1.1},
}


def get_service_thresholds(service_type: str) -> ServiceThreshold:
    """Returns thresholds for given service type, or global default fallback."""
    st_lower = str(service_type).lower()
    return SERVICE_THRESHOLDS.get(
        st_lower,
        {"due_soon_days": DUE_SOON_THRESHOLD_DAYS, "at_risk_ratio": AT_RISK_RATIO},
    )


# Status Constants (Matching Frappe DocType Select Field values)
STATUS_ACTIVE = "Active"
STATUS_EXPIRED = "Expired"
STATUS_CANCELLED = "Cancelled"
STATUS_DRAFT = "Draft"

# CRM Recommendation Lifecycle Workflow States
RECOMMENDATION_NEW = "NEW"
RECOMMENDATION_ASSIGNED = "ASSIGNED"
RECOMMENDATION_CONTACTED = "CONTACTED"
RECOMMENDATION_CONVERTED = "CONVERTED"
RECOMMENDATION_DISMISSED = "DISMISSED"
RECOMMENDATION_SENT = "SENT"
RECOMMENDATION_COMPLETED = "COMPLETED"

RECOMMENDATION_TYPE_DUE_SOON = "DUE_SOON"
RECOMMENDATION_TYPE_AT_RISK = "AT_RISK"
RECOMMENDATION_TYPE_RENEWAL = "RENEWAL"

DISCOUNT_TYPE_FREE = "FREE"
DISCOUNT_TYPE_PERCENTAGE = "PERCENTAGE"
DISCOUNT_TYPE_FIXED = "FIXED"

# Multi-Branch Clinic Network Configuration (Limitation 2.5 Extension)
DEFAULT_BRANCH: str = "CN-TRUNGTAM"
CLINIC_BRANCHES = ["CN-TRUNGTAM", "CN-QUAN1", "CN-THUDUC", "CN-BINHTHANH"]
BRANCH_DETAILS = {
    "CN-TRUNGTAM": {"name": "Chi nhánh Trung Tâm (Quận 3)", "address": "123 Nguyễn Thị Minh Khai, Q3, TP.HCM", "phone": "028.3888.9999"},
    "CN-QUAN1": {"name": "Chi nhánh Quận 1", "address": "45 Lê Lợi, P. Bến Nghé, Q1, TP.HCM", "phone": "028.3888.1111"},
    "CN-THUDUC": {"name": "Chi nhánh Thủ Đức", "address": "78 Võ Văn Ngân, TP. Thủ Đức", "phone": "028.3888.2222"},
    "CN-BINHTHANH": {"name": "Chi nhánh Bình Thạnh", "address": "90 Phan Đăng Lưu, Q. Bình Thạnh, TP.HCM", "phone": "028.3888.3333"},
}
