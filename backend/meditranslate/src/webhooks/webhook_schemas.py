from meditranslate.utils.files.file_format_type import FileFormatType
from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema
from datetime import datetime
from typing import Optional
from pydantic import Field, HttpUrl

class WebhookCreateSchema(BaseSchema):
    translation_job_id: str = Field(..., description="ID of the translation job")
    # callback_url: HttpUrl = Field(..., description="URL to send webhook data to")

class WebhookSchema(BaseSchema):
    id: str
    user_id: str
    translation_job_id: str
    # callback_url: HttpUrl
    file_id: Optional[str] = None
    is_triggered: bool = False
    triggered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class WebhookResponseSchema(BaseResponseSchema):
    data: WebhookSchema

class FileConversionWebhookCreateSchema(BaseSchema):
    file_id: str = Field(..., description="ID of the file being converted")
    # source_format: FileFormatType = Field(..., description="Original file format")
    # target_format: FileFormatType = Field(..., description="Target file format")

class FileConversionWebhookSchema(BaseSchema):
    id: str
    user_id: str
    # file_id: str
    # source_format: FileFormatType
    # target_format: FileFormatType
    status: str  # 'pending', 'processing', 'completed', 'failed'
    error_message: Optional[str] = None
    file_id: Optional[str] = None
    is_triggered: bool = False
    triggered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class FileConversionWebhookResponseSchema(BaseResponseSchema):
    data: FileConversionWebhookSchema
