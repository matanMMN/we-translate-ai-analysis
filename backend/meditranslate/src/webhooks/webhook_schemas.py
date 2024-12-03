from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema
from datetime import datetime
from typing import Optional
from pydantic import Field, HttpUrl

class WebhookCreateSchema(BaseSchema):
    translation_job_id: str = Field(..., description="ID of the translation job")
    callback_url: HttpUrl = Field(..., description="URL to send webhook data to")

class WebhookSchema(BaseSchema):
    id: str
    user_id: str
    translation_job_id: str
    callback_url: HttpUrl
    file_id: Optional[str] = None
    is_triggered: bool = False
    triggered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class WebhookResponseSchema(BaseResponseSchema):
    data: WebhookSchema