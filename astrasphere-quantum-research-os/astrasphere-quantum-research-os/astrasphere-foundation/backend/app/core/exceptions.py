"""Domain-level exceptions, decoupled from HTTP concerns.

Services and repositories raise these; the exception-handling middleware
translates them into HTTP responses. This keeps the domain layer free of
any FastAPI/HTTP imports (Clean Architecture boundary).
"""


class AstraSphereError(Exception):
    """Base class for all application-defined errors."""


class NotFoundError(AstraSphereError):
    """Raised when a requested resource does not exist."""


class ConflictError(AstraSphereError):
    """Raised when an operation conflicts with existing state."""


class ValidationError(AstraSphereError):
    """Raised when domain-level validation fails outside of Pydantic schemas."""


class UnauthorizedError(AstraSphereError):
    """Raised when a caller lacks a valid identity (auth not yet implemented)."""


class ForbiddenError(AstraSphereError):
    """Raised when a caller is identified but lacks permission."""


class RateLimitError(AstraSphereError):
    """Raised when a caller exceeds an enforced rate limit."""
