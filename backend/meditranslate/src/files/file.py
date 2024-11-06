from meditranslate.app.db import Base
from sqlalchemy import String, Boolean, DateTime,LargeBinary,JSON,Enum,Float
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional,List,Dict
from datetime import date,datetime
from meditranslate.src.files.file_constants import FileFormatType,FileSizeUnit,FileStorageProvider


class File(Base):
    __tablename__ = 'files'

    file_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    original_file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False) # filename after normalizing
    file_path: Mapped[str] = mapped_column(String, nullable=False) # idk if need that tho
    file_url: Mapped[str] = mapped_column(String, nullable=False) #
    file_storage_provider: Mapped[FileStorageProvider] = mapped_column(Enum(FileStorageProvider), nullable=False)
    file_size: Mapped[float] = mapped_column(Float, nullable=False)
    file_size_unit: Mapped[FileSizeUnit] = mapped_column(Enum(FileSizeUnit), nullable=False)
    file_format_type: Mapped[FileFormatType] = mapped_column(Enum(FileFormatType), nullable=False)
    file_metadata: Mapped[dict] = mapped_column(JSON, nullable=True,default=None)

    def __repr__(self):
        return f"<File(id={self.id}, file_name={self.file_name}, file_type={self.file_format_type})>"
