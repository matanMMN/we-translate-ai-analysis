from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from meditranslate.app.db import User

from meditranslate.utils.files.file_status import FileStatus
from meditranslate.app.db import Base
from sqlalchemy import String, Boolean, DateTime,LargeBinary,JSON,Enum,Float,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from typing import Optional,List,Dict

class File(Base):
    __tablename__ = 'files'
    original_file_name: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    file_name: Mapped[Optional[str]] = mapped_column(String, nullable=False) # filename after normalizing
    file_path: Mapped[Optional[str]] = mapped_column(String, nullable=False) # idk if need that tho
    file_url: Mapped[Optional[str]] = mapped_column(String, nullable=False) #
    file_storage_provider: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    file_size: Mapped[Optional[float]] = mapped_column(Float, nullable=False)
    file_format_type: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    file_metadata: Mapped[Optional[Dict[str,str]]] = mapped_column(JSON, nullable=True,default=None)
    file_language: Mapped[Optional[str]] = mapped_column(JSON, nullable=True,default=None)
    upload_by: Mapped[Optional[str]] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"),nullable=True,default=None)
    # Relationships
    upload_by_user: Mapped[Optional["User"]] = relationship('User', foreign_keys=[upload_by], lazy='select', remote_side='User.id')
    status: Mapped[Optional[FileStatus]] = mapped_column(
        Enum(FileStatus, native_enum=False), 
        default=FileStatus.PENDING,
        nullable=False
    )
    
    processing_error: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    def __repr__(self):
        return f"<File(id={self.id}, file_name={self.file_name}, file_type={self.file_format_type})>"
