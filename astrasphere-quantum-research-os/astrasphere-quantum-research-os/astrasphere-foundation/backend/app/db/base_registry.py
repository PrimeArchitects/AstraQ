"""Central import point for all ORM models.

Alembic's autogenerate needs every model imported somewhere before it
inspects `Base.metadata`. As feature models are added under
`app/models/`, import them here.
"""

from app.models.auth_provider import AuthProvider  # noqa: F401
from app.models.session import Session  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.user_preferences import UserPreferences  # noqa: F401
