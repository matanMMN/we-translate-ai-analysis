from datetime import datetime
from typing import Optional, List
from meditranslate.app.shared.schemas import BaseResponseSchema,BaseSchema, UserIdentifiersModificationSchema,ModificationTimestampSchema,ObjectIdSchema,UserFullNamesModificationSchema
from meditranslate.src.requests.requests import RequestType, RequestStatus
from meditranslate.src.users.user_schemas import UserSchema
from meditranslate.src.translation_jobs.translation_job_schemas import TranslationJobSchema

# Base Request Schema
class RequestBase(BaseSchema):
    request_type: RequestType
    # status: RequestStatus = RequestStatus.PENDING

# Create Schemas
class DeletionRequestCreate(RequestBase):
    project_id: str
    reason: str
    request_type: RequestType = RequestType.DELETION

class TermRequestCreate(RequestBase):
    source_term: str
    target_term: str
    context: Optional[str] = None
    request_type: RequestType = RequestType.TERM

class GlossaryRequestCreate(RequestBase):
    source_term: str
    target_term: str
    context: Optional[str] = None
    request_type: RequestType = RequestType.GLOSSARY

# Update Schema
class RequestUpdate(BaseSchema):
    status: RequestStatus
    resolution_note: Optional[str]

# Response Schema
class RequestResponse(ObjectIdSchema,RequestBase, RequestUpdate, BaseSchema):

    # Common fields
    requester_id: str
    resolver_id: str | None = None
    
    # Deletion request fields
    project_id: str | None = None
    project: Optional[TranslationJobSchema] = None
    reason: str | None = None
    
    created_at: datetime
    updated_at: datetime

    # Term and Glossary request fields
    source_term: Optional[str] = None
    target_term: Optional[str] = None
    context: Optional[str] = None

    class Config:
        from_attributes = True

class RequestResponseSchema(BaseResponseSchema):
    data: RequestResponse

class RequestsResponseSchema(BaseResponseSchema):
    data: List[RequestResponse]
