"""
Ported from Flask project. Adapted for Frappe Framework.
Business logic unchanged. DB layer replaced by Frappe ORM via frappe_adapters.py.
"""


class PetCareException(Exception):
    """Base exception for PetCare CRM domain."""
    pass


class MembershipException(PetCareException):
    """Base exception for Membership errors."""
    pass


class MembershipExpiredException(MembershipException):
    """Raised when trying to use an expired membership."""
    pass


class MembershipNotActiveException(MembershipException):
    """Raised when trying to use a non-active membership."""
    pass


class BenefitException(PetCareException):
    """Base exception for Membership Benefit errors."""
    pass


class BenefitNotFoundException(BenefitException):
    """Raised when a requested benefit type does not exist on a membership."""
    pass


class BenefitExhaustedException(BenefitException):
    """Raised when benefit remaining_quantity is 0."""
    pass


class InvalidDateRangeException(PetCareException):
    """Raised when end_date < start_date or date range is invalid."""
    pass


class InvalidPriceException(PetCareException):
    """Raised when price, discount, or final price is invalid."""
    pass


class ValidationError(PetCareException):
    """Raised when input parameters fail domain validation rules."""
    pass


class EntityNotFoundException(PetCareException):
    """Raised when an entity is not found in database."""
    pass


class InsufficientBalanceException(PetCareException):
    """Raised when wallet balance is insufficient for transaction."""
    pass


class InvalidStateTransitionException(PetCareException):
    """Raised when document lifecycle transition is prohibited."""
    pass



class TransactionRollbackException(PetCareException):
    """Raised when a transaction fails and must be rolled back."""
    pass
