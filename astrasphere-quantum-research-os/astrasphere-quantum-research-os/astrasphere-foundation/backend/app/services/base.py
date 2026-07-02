"""Marker base class for application services.

Services encapsulate business logic and orchestrate one or more
repositories. Routers depend on services, never on repositories directly —
this is the boundary that keeps HTTP concerns out of business logic.
"""


class BaseService:
    """Intentionally minimal. Concrete services compose repositories via __init__."""
