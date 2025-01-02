from meditranslate.utils.files.file_status import FileStatus
from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema,ObjectIdSchema,UserFullNamesModificationSchema,UserIdentifiersModificationSchema,ModificationTimestampSchema,LanguageStr,IdentifierStr,NameStr,FullNameStr,FileFormatTypeStr
from typing import List,Optional,Dict,Any,Literal,Union
from pydantic import Field,StringConstraints
from typing_extensions import Annotated

OriginalFileNameStr = Annotated[
                    str,
                    StringConstraints(
                        strip_whitespace=True,
                        to_upper=None,
                        to_lower=None,
                        strict=None,
                        max_length=None,
                        min_length=None,
                        pattern=None,
                    )
                ]
FileNameStr = Annotated[
                    str,
                    StringConstraints(
                        strip_whitespace=True,
                        to_upper=None,
                        to_lower=None,
                        strict=None,
                        max_length=None,
                        min_length=None,
                        pattern=None,
                    )
                ]

FileStorageProviderStr  = Annotated[
                    str,
                    StringConstraints(
                        strip_whitespace=True,
                        to_upper=None,
                        to_lower=None,
                        strict=None,
                        max_length=None,
                        min_length=None,
                        pattern=None,
                    )
                ]

FilePathStr  = Annotated[
                    str,
                    StringConstraints(
                        strip_whitespace=True,
                        to_upper=None,
                        to_lower=None,
                        strict=None,
                        max_length=None,
                        min_length=None,
                        pattern=None,
                    )
                ]

FileUrlStr  = Annotated[
                    str,
                    StringConstraints(
                        strip_whitespace=True,
                        to_upper=None,
                        to_lower=None,
                        strict=None,
                        max_length=None,
                        min_length=None,
                        pattern=None,
                    )
                ]



class PublicFilePointerSchema(ObjectIdSchema,UserFullNamesModificationSchema,ModificationTimestampSchema):
    file_name : FileNameStr = Field(..., title="file_name ID", description="Unique identifier for the user")
    file_size : Union[float,int] = Field(...,title="file_size", description="")
    file_format_type: FileFormatTypeStr = Field(...,title="file_format_type", description="")
    file_language: LanguageStr  = Field(...,title="file_format_type", description="")
    upload_by_user: Optional[Union[NameStr,FullNameStr]] = Field(None, title="uploader full name",description="full name of user")

class FilePointerSchema(ObjectIdSchema,UserIdentifiersModificationSchema,UserFullNamesModificationSchema,ModificationTimestampSchema):
    file_name_id: FileNameStr = Field(..., title="file_name with ID", description="Unique identifier for the user and the front-end")
    file_name : FileNameStr = Field(..., title="file_name", description="Unique identifier for the user")
    file_size : Union[float,int] = Field(...,title="file_size", description="")
    file_format_type: FileFormatTypeStr = Field(...,title="file_format_type", description="")
    file_language: LanguageStr  = Field(...,title="file_format_type", description="")
    upload_by: IdentifierStr = Field(..., title="uploadeer user id",description=" user upload.")
    upload_by_user: Optional[Union[NameStr,FullNameStr]] = Field(None, title="uploader full name",description="full name of user")
    status: str = Field(
        default=FileStatus.PENDING.value,
        description="Status of the file processing"
    )
    processing_task_id: Optional[str] = Field(..., title="processing_task_id",description=" processing task id")
    processing_error: Optional[str] = None


class FilePointerCreateSchema(BaseSchema):
    original_file_name : OriginalFileNameStr  = Field(..., title="original_file_name ", description="")
    file_name : FileNameStr = Field(..., title="file_name ID", description="Unique identifier for the user")
    file_size : Union[float,int] = Field(...,title="file_size", description="")
    file_path : FilePathStr = Field(..., title="file_path", description="file_id")
    file_url : FileUrlStr = Field(..., title="file_url", description="file_id")
    file_storage_provider: FileStorageProviderStr = Field(..., title="file_url", description="file_id")
    file_format_type: FileFormatTypeStr = Field(...,title="file_format_type", description="")
    file_metadata: Optional[dict] = Field(None,title="file_metadata", description="")
    file_language: Optional[LanguageStr]  = Field(...,title="file_format_type", description="")
    upload_by: IdentifierStr = Field(..., title="uploadeer user id",description=" user upload.")
    status: str = Field(
        default=FileStatus.PENDING.value,
        description="Status of the file processing"
    )
    processing_error: Optional[str] = None


class FilePointerUpdateSchema(BaseSchema):
    original_file_name: Optional[OriginalFileNameStr] = Field(default=None, title="original_file_name", description="")
    file_name: Optional[FileNameStr] = Field(default=None, title="file_name ID", description="Unique identifier for the user")
    file_size: Optional[Union[float,int]] = Field(default=None, title="file_size", description="")
    file_path: Optional[FilePathStr] = Field(default=None, title="file_path", description="file_id")
    file_url: Optional[FileUrlStr] = Field(default=None, title="file_url", description="file_id")
    file_storage_provider: Optional[FileStorageProviderStr] = Field(default=None, title="file_url", description="file_id")
    file_format_type: Optional[FileFormatTypeStr] = Field(default=None, title="file_format_type", description="")
    file_metadata: Optional[dict] = Field(None, title="file_metadata", description="")
    status: Optional[str] = Field(
        default=FileStatus.PENDING.value,
        description="Status of the file processing"
    )
    processing_error: Optional[str] = None
    file_language: Optional[LanguageStr] = Field(default=None, title="file_format_type", description="")
    upload_by: Optional[IdentifierStr] = Field(default=None, title="uploadeer user id", description=" user upload.")
    current_version: Optional[int] = Field(default=None, title="current_version", description=" current version of the file")
    processing_task_id: Optional[str] = Field(default=None, title="processing_task_id", description=" processing task id")


class FilePointerResponseSchema(BaseResponseSchema):
    data: FilePointerSchema

class FilePointersResponseSchema(BaseResponseSchema):
    data: List[FilePointerSchema]

class PublicFilePointerResponseSchema(BaseResponseSchema):
    data: PublicFilePointerSchema

class PublicFilePointersResponseSchema(BaseResponseSchema):
    data: List[PublicFilePointerSchema]

