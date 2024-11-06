from typing import Optional, TYPE_CHECKING,List
from uuid import uuid4
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, JSON, UUID,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from meditranslate.app.db import Base
from datetime import datetime


class TranslationJob(Base):
    __tablename__ = 'translation_jobs'
    __table_args__ = (
        UniqueConstraint('title', 'source_language','target_language', name='_title_langs_uc'),
    )

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False, default="")
    source_language: Mapped[str] = mapped_column(String, nullable=False)
    target_language: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False,default=0)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True)


    status: Mapped[str] = mapped_column(String, nullable=False)
    current_step_index: Mapped[Integer] = mapped_column(Integer, default=0)

    reference_file_id: Mapped[str] = mapped_column(
        ForeignKey('files.id', onupdate="CASCADE"),nullable=True,default=None)

    source_file_id: Mapped[str] = mapped_column(
        ForeignKey('files.id', onupdate="CASCADE"),nullable=True,default=None)

    current_user_id: Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"))

    created_by: Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"))
    updated_by: Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"))

    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True, default=None) # when status is completed
    approved_by: Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"))

    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True, default=None)
    archived_by: Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"))

    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True, default=None)
    deleted_by: Mapped[str] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"))

    data: Mapped[dict]  = mapped_column(JSON,nullable=True,default=None)

    current_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[current_user_id])

    reference_file: Mapped[Optional["File"]] = relationship('File',foreign_keys=[reference_file_id])
    source_file: Mapped[Optional["File"]] = relationship('File',foreign_keys=[source_file_id])

    translations: Mapped[List["Translation"]] = relationship('Translation')

    created_by_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[created_by])
    updated_by_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[updated_by])
    approved_by_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[approved_by])
    archived_by_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[archived_by])
    deleted_by_user: Mapped[Optional["User"]] = relationship('User',  foreign_keys=[deleted_by])
