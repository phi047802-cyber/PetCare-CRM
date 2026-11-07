"""
PetCare CRM Utils Package.
Contains domain services, business logic, and coordinators.
"""

from petcare_crm.utils.config import (
    DUE_SOON_THRESHOLD_DAYS,
    AT_RISK_RATIO,
    MIN_VISITS_FOR_INTERVAL,
    SERVICE_THRESHOLDS,
    get_service_thresholds,
)
from petcare_crm.utils.exceptions import (
    PetCareException,
    ValidationError,
    EntityNotFoundException,
    MembershipExpiredException,
    BenefitExhaustedException,
    InvalidStateTransitionException,
)
from petcare_crm.utils.care_pattern_service import (
    CarePatternService,
    CarePatternAnalyzer,
    VisitPredictionService,
    RiskDetectionService,
)
from petcare_crm.utils.recommendation_service import (
    RecommendationService,
    CareRecommendationCoordinator,
)
from petcare_crm.utils.membership_service import MembershipService
from petcare_crm.utils.workflow_automation import (
    SafeCommunicationGateway,
    TaskManager,
    LeadFollowupAutomation,
    MembershipRenewalAutomation,
    CareEngineAutomation,
    ServiceRecoveryAutomation,
    AutomationCoordinator,
)

try:
    from petcare_crm.utils.lead_service import LeadManagementService, LeadConversionCoordinator
    from petcare_crm.utils.sales_pipeline_service import SalesPipelineService
    from petcare_crm.utils.customer_service import CustomerService
    from petcare_crm.utils.service_operations import (
        ServiceCatalogService,
        ServiceVisitService,
        CaseManagementService,
    )
except ImportError:
    pass
