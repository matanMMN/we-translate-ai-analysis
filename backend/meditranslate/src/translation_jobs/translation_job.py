from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from meditranslate.app.db import File,User,Translation

from typing import Optional, TYPE_CHECKING,List
from uuid import uuid4
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, JSON, UUID,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from meditranslate.app.db import Base
from meditranslate.src.webhooks.webhook import Webhook
from datetime import datetime


class TranslationJob(Base):
    __tablename__ = 'translation_jobs'
    __table_args__ = (
        UniqueConstraint('title', 'source_language','target_language', name='_title_langs_uc'),
    )
    webhooks: Mapped[List["Webhook"]] = relationship(
        'Webhook',
        back_populates="translation_job",
        cascade="all, delete-orphan"
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True, default="")
    source_language: Mapped[str] = mapped_column(String, nullable=False)
    target_language: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False,default=0)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True),nullable=True,default=None,server_default=None)

    status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    current_step_index: Mapped[int] = mapped_column(Integer, default=0)

    reference_file_id: Mapped[Optional[str]] = mapped_column(ForeignKey('files.id'),nullable=True)
    source_file_id: Mapped[Optional[str]] = mapped_column(ForeignKey('files.id'),nullable=True)
    target_file_id: Mapped[Optional[str]] = mapped_column(ForeignKey('files.id'),nullable=True)

    current_user_id: Mapped[Optional[str]] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"),nullable=True,default=None)

    created_by: Mapped[Optional[str]] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"),nullable=True,default=None)
    updated_by: Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"),nullable=True,default=None)

    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True),nullable=True, default=None) # when status is completed
    approved_by: Mapped[Optional[str]] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"))

    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True),nullable=True, default=None)
    archived_by: Mapped[Optional[str]] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"),nullable=True,default=None)

    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True),nullable=True, default=None)
    deleted_by: Mapped[Optional[str]] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"),nullable=True,default=None)

    data: Mapped[dict]  = mapped_column(JSON,nullable=False,default=dict)

    current_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[current_user_id], lazy='select', remote_side='User.id')

    reference_file: Mapped[Optional["File"]] = relationship('File',foreign_keys=[reference_file_id], lazy='select', remote_side='File.id')
    source_file: Mapped[Optional["File"]] = relationship('File',foreign_keys=[source_file_id] ,lazy='select', remote_side='File.id')

    translations: Mapped[List["Translation"]] = relationship('Translation', back_populates="translation_job", lazy='select')

    created_by_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[created_by], lazy='select', remote_side='User.id')
    updated_by_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[updated_by], lazy='select', remote_side='User.id')
    approved_by_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[approved_by], lazy='select', remote_side='User.id')
    archived_by_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[archived_by], lazy='select', remote_side='User.id')
    deleted_by_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[deleted_by], lazy='select', remote_side='User.id')