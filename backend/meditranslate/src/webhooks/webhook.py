from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from meditranslate.app.db import User, TranslationJob

from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from meditranslate.app.db import Base

class Webhook(Base):
    __tablename__ = 'webhooks'

    # callback_url: Mapped[str] = mapped_column(
    #     String, 
    #     nullable=False
    # )    
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id', onupdate="CASCADE"),
        nullable=False
    )
    translation_job_id: Mapped[str] = mapped_column(
        ForeignKey('translation_jobs.id', onupdate="CASCADE"),
        nullable=False
    )

    file_id: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )
    
    is_triggered: Mapped[bool] = mapped_column(Boolean, default=False)
    triggered_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now()
    )

    user: Mapped["User"] = relationship(
        'User',
        foreign_keys=[user_id],
        lazy='select',
        remote_side='User.id'
    )
    translation_job: Mapped["TranslationJob"] = relationship(
        'TranslationJob',
        foreign_keys=[translation_job_id],
        lazy='select',
        remote_side='TranslationJob.id'
    )