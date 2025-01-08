from datetime import datetime
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from meditranslate.src.users.user import User
from meditranslate.src.translation_jobs.translation_job import TranslationJob
from meditranslate.app.db.base import Base
from meditranslate.utils.requests.request_status import RequestStatus
from meditranslate.utils.requests.request_type import RequestType

class Request(Base):
    __tablename__ = "requests"

    request_type: Mapped[RequestType] = mapped_column()
    status: Mapped[RequestStatus] = mapped_column(default=RequestStatus.PENDING)
    
    # Common fields for all request types
    requester_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    resolver_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    resolution_note: Mapped[str | None] = mapped_column(nullable=True)
    
    # Deletion request fields
    project_id: Mapped[str | None] = mapped_column(ForeignKey("translation_jobs.id", ondelete="CASCADE"), nullable=True)
    reason: Mapped[str | None] = mapped_column(nullable=True)
    
    # Term and Glossary request fields
    source_term: Mapped[str | None] = mapped_column(nullable=True)
    target_term: Mapped[str | None] = mapped_column(nullable=True)
    context: Mapped[str | None] = mapped_column(nullable=True)

    # Relationships
    requester: Mapped["User"] = relationship("User", foreign_keys=[requester_id])
    resolver: Mapped["User"] = relationship("User", foreign_keys=[resolver_id])
    project: Mapped["TranslationJob | None"] = relationship("TranslationJob")