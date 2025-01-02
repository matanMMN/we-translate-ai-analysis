from datetime import datetime
from meditranslate.app.shared.base_schema import BaseSchema
from meditranslate.utils.files.file_status import FileStatus
from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,ObjectIdSchema,UserFullNamesModificationSchema,UserIdentifiersModificationSchema,ModificationTimestampSchema,LanguageStr,IdentifierStr,NameStr,FullNameStr,FileFormatTypeStr
from typing import List
class FileVersionCreateSchema(BaseSchema):
    file_id: str
    version_number: int
    file_path: str
    file_size: int
    file_language: str | None
    file_format_type: str
    status: FileStatus
    created_by: str

class FileVersionResponseSchema(ObjectIdSchema,UserIdentifiersModificationSchema,UserFullNamesModificationSchema,ModificationTimestampSchema):
    id: str
    version_number: int
    created_at: datetime
    created_by: str
    file_size: int
    file_path: str
    file_language: str | None
    file_format_type: str
    status: str 

class ListFilePointerResponseSchema(BaseResponseSchema):
    data: List[FileVersionResponseSchema]