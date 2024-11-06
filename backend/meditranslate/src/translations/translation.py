from typing import Optional, TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import Double, String, Text, DateTime, ForeignKey, UUID,JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from meditranslate.app.db import Base


class Translation(Base):
    __tablename__ = 'translations'

    translation_job_id: Mapped[str] = mapped_column(ForeignKey('translation_jobs.id', onupdate="CASCADE",),nullable=True)

    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    output_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    source_language: Mapped[String] = mapped_column(String(50), nullable=False)
    target_language: Mapped[String] = mapped_column(String(50), nullable=False)

    created_by: Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"))
    updated_by: Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"))

    meta: Mapped[dict] = mapped_column(JSON,nullable=False,default={})

    # Relationships
    # translation_job: Mapped["TranslationJob"] = relationship('TranslationJob', back_populates='translations')
    created_by_user: Mapped["User"] = relationship('User', foreign_keys=created_by)
    updated_by_user: Mapped["User"] = relationship('User', foreign_keys=updated_by)
