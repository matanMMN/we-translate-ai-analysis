from meditranslate.app.db import Base
from sqlalchemy import String, Boolean, DateTime,LargeBinary,JSON,Enum,Float,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from typing import Optional,List,Dict

class File(Base):
    __tablename__ = 'files'
    original_file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False) # filename after normalizing
    file_path: Mapped[str] = mapped_column(String, nullable=False) # idk if need that tho
    file_url: Mapped[str] = mapped_column(String, nullable=False) #
    file_storage_provider: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[float] = mapped_column(Float, nullable=False)
    file_format_type: Mapped[str] = mapped_column(String, nullable=False)
    file_metadata: Mapped[Dict[str,str]] = mapped_column(JSON, nullable=True,default=None)
    file_language: Mapped[str] = mapped_column(JSON, nullable=True,default=None)
    upload_by: Mapped[Optional[str]] = mapped_column(ForeignKey('users.id', onupdate="CASCADE"),nullable=True,default=None)
    # Relationships
    upload_by_user: Mapped[Optional["User"]] = relationship('User', foreign_keys=[upload_by], lazy='select', remote_side='User.id')

    def __repr__(self):
        return f"<File(id={self.id}, file_name={self.file_name}, file_type={self.file_format_type})>"
