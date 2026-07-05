"""Central import point for all ORM models.

Alembic's autogenerate needs every model imported somewhere before it
inspects `Base.metadata`. As feature models are added under
`app/models/`, import them here.
"""

from app.models.activity_log import ActivityLog  # noqa: F401
from app.models.ai_job import AIJob  # noqa: F401
from app.models.auth_provider import AuthProvider  # noqa: F401
from app.models.bookmark import Bookmark  # noqa: F401
from app.models.chat_message import ChatMessage  # noqa: F401
from app.models.chat_session import ChatSession  # noqa: F401
from app.models.folder import Folder  # noqa: F401
from app.models.notification import Notification  # noqa: F401
from app.models.paper_metadata import PaperMetadata  # noqa: F401
from app.models.research_paper import ResearchPaper  # noqa: F401
from app.models.session import Session  # noqa: F401
from app.models.tag import Tag, paper_tags  # noqa: F401
from app.models.team_member import TeamMember  # noqa: F401
from app.models.team_workspace import TeamWorkspace  # noqa: F401
from app.models.uploaded_file import UploadedFile  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.user_preferences import UserPreferences  # noqa: F401
