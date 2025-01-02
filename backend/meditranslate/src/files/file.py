from __future__ import annotations
from datetime import datetime
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
    file_name_id: Mapped[Optional[str]] = mapped_column(String)
    file_name: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    file_path: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    file_url: Mapped[Optional[str]] = mapped_column(String, nullable=False) 
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
    current_version: Mapped[int] = mapped_column(default=1)
    versions: Mapped[List["FileVersion"]] = relationship("FileVersion", back_populates="file", cascade="all, delete-orphan")
    processing_task_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"<File(id={self.id}, file_name={self.file_name}, file_type={self.file_format_type})>"
    

class FileVersion(Base):
    __tablename__ = "file_versions"
    
    file_id: Mapped[str] = mapped_column(ForeignKey("files.id"))
    version_number: Mapped[int]
    file_path: Mapped[str]
    file_size: Mapped[int]
    file_language: Mapped[str] = mapped_column(String(10), nullable=True)
    file_format_type: Mapped[str]
    status: Mapped[FileStatus] = mapped_column(Enum(FileStatus))
    created_by: Mapped[str] = mapped_column(ForeignKey("users.id"))
    
    file: Mapped["File"] = relationship("File", back_populates="versions")
    created_by_user: Mapped["User"] = relationship("User")

    def __repr__(self):
        return f"<File(id={self.id}, file_name={self.file_name}, file_type={self.file_format_type})>"