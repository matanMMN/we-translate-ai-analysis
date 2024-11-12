from typing import Dict, Optional, TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import Double, String, Text, DateTime, ForeignKey, UUID,JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from meditranslate.app.db import Base

# Import models only for type checking to avoid circular imports
# if TYPE_CHECKING:
#     from .user import User
#     from .translation_job import TranslationJob


class Translation(Base):
    __tablename__ = 'translations'


    translation_job_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey('translation_jobs.id', ondelete="SET NULL"), nullable=True
    )
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    output_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    source_language: Mapped[str] = mapped_column(String(50), nullable=False)
    target_language: Mapped[str] = mapped_column(String(50), nullable=False)

    created_by: Mapped[Optional[str]] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"),nullable=True,default=None)

    translation_metadata: Mapped[Optional[Dict[str,str]]] = mapped_column(JSON,nullable=True)

    # Relationships
    translation_job: Mapped[Optional["TranslationJob"]] = relationship(
        'TranslationJob', back_populates="translations", lazy='select',
        remote_side='TranslationJob.id'
    )

    created_by_user: Mapped[Optional["User"]] = relationship('User', foreign_keys=[created_by], lazy='select', remote_side='User.id')
