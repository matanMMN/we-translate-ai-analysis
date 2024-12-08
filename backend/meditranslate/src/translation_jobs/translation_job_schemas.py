from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema,NameStr,FullNameStr,IdentifierStr,TranslationLanguagesSchema,UserIdentifiersModificationSchema,ModificationTimestampSchema,ObjectIdSchema,UserFullNamesModificationSchema,JsonStr
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, HttpUrl,constr,field_validator,Field,EmailStr,StringConstraints,ConfigDict,Json
import re
from typing_extensions import Annotated
import enum

class TranslationJobStatus(enum.Enum):
    INITIAL = "initial"

TitleStr = Annotated[
            str,
            StringConstraints(
                strip_whitespace=True,
                max_length=50,
                min_length=1
                ),
            ]

DescriptionStr = Annotated[
                    str,
                    StringConstraints(
                        strip_whitespace=True,
                        max_length=450,
                    )
                ]

StatusStr = Annotated[
                    str,
                    StringConstraints(
                        strip_whitespace=True,
                        max_length=450,
                    )
                ]


class PublicTranslationJobSchema(ObjectIdSchema,UserFullNamesModificationSchema,TranslationLanguagesSchema,ModificationTimestampSchema):
    title : TitleStr = Field(..., title="", description="")
    description : DescriptionStr = Field(..., title="User ID", description="Unique identifier for the user")
    source_file_id : Optional[IdentifierStr] = Field(None, title="source file id", description="")
    reference_file_id: Optional[IdentifierStr] = Field(None, title="reference file id", description="")
    target_file_id :Optional[IdentifierStr] = Field(None, title="target file id", description="")
    priority : int = Field(..., title="priority", description="",ge=0)
    due_date : Optional[datetime] = Field(None, title="due date", description="")
    status : StatusStr = Field(..., title="status", description="Unique identifier for the user")
    data : dict = Field(..., title="data", description="Unique identifier for the user")
    current_step_index : int = Field(..., title="current_step_index", description="",ge=0)
    current_user_id : Optional[IdentifierStr] = Field(None, title="", description="")
    current_user :Optional[Union[NameStr,FullNameStr]] = Field(None, title="current_user_ name", description="")

    # @validator("data", pre=True, always=True)
    # def ensure_json(cls, v):
    #     # If `data` is provided as a dictionary, dump it to JSON string
    #     if isinstance(v, dict):
    #         return json.dumps(v)
    #     # If already a string, validate it is a JSON-encoded string
    #     try:
    #         json.loads(v)  # Validates it's a JSON string
    #         return v
    #     except json.JSONDecodeError:
    #         raise ValueError("data must be a valid JSON string or dict")

    # approved_at: Optional[datetime]= Field(None, title="", description="")
    # approved_by : Annotated[
    #                 Optional[str],
    #                 StringConstraints(
    #                     strip_whitespace=True,
    #                     to_upper=None,
    #                     to_lower=None,
    #                     strict=None,
    #                     max_length=None,
    #                     min_length=None,
    #                     pattern=None,
    #                 ),
    #             ] = Field(None, title="", description="")
    # archived_at: Optional[datetime]= Field(None, title="", description="")
    # archived_by : Annotated[
    #                 Optional[str],
    #                 StringConstraints(
    #                     strip_whitespace=True,
    #                     to_upper=None,
    #                     to_lower=None,
    #                     strict=None,
    #                     max_length=None,
    #                     min_length=None,
    #                     pattern=None,
    #                 ),
    #             ] = Field(None, title="", description="")
    # deleted_at: Optional[datetime]= Field(None, title="", description="")
    # deleted_by : Annotated[
    #                 Optional[str],
    #                 StringConstraints(
    #                     strip_whitespace=True,
    #                     to_upper=None,
    #                     to_lower=None,
    #                     strict=None,
    #                     max_length=None,
    #                     min_length=None,
    #                     pattern=None,
    #                 ),
    #             ] = Field(None, title="", description="")

class TranslationJobSchema(ObjectIdSchema,UserIdentifiersModificationSchema,UserFullNamesModificationSchema,TranslationLanguagesSchema,ModificationTimestampSchema):
    title : TitleStr = Field(..., title="", description="")
    description : DescriptionStr = Field(..., title="User ID", description="Unique identifier for the user")
    data : dict = Field(..., title="data", description="Unique identifier for the user")
    source_file_id : Optional[IdentifierStr] = Field(None, title="source file id", description="")
    reference_file_id: Optional[IdentifierStr] = Field(None, title="reference file id", description="")
    target_file_id :Optional[IdentifierStr] = Field(None, title="target file id", description="")
    priority : int = Field(..., title="priority", description="",ge=0)
    due_date : Optional[datetime] = Field(None, title="due date", description="")
    status : StatusStr = Field(..., title="status", description="Unique identifier for the user")
    current_step_index : int = Field(..., title="current_step_index", description="",ge=0)
    current_user_id : Optional[IdentifierStr] = Field(None, title="", description="")
    current_user :Optional[Union[NameStr,FullNameStr]] = Field(None, title="current_user_ name", description="")


class TranslationJobCreateSchema(TranslationLanguagesSchema):
    title :TitleStr = Field(..., title="User ID", description="Unique identifier for the user")
    description :Optional[DescriptionStr] = Field(None, title="User ID", description="Unique identifier for the user")
    source_file_id :Optional[IdentifierStr] = Field(None, title="source file id", description="")
    reference_file_id :Optional[IdentifierStr] = Field(None, title="source file id", description="")
    target_file_id :Optional[IdentifierStr] = Field(None, title="target file id", description="")
    priority : Optional[int]= Field(0, title="priority", description="",ge=0)
    due_date : Optional[datetime] = Field(None, title="due date", description="")
    status : Optional[StatusStr] = Field(TranslationJobStatus.INITIAL.value, title="status", description="")
    data : Optional[dict] = Field(None, title="data", description="")
    current_step_index : Optional[int] = Field(0, title="current_step_index", description="",ge=0)
    current_user_id :Optional[IdentifierStr] = Field(None, title="current_user_id", description="")


class TranslationJobUpdateSchema(BaseSchema):
    title : Optional[TitleStr] = Field(None, title="", description="")
    description : Optional[DescriptionStr] = Field(None, title="User ID", description="Unique identifier for the user")
    source_file_id :Optional[IdentifierStr] = Field(None, title="source file id", description="")
    reference_file_id :Optional[IdentifierStr] = Field(None, title="reference file id", description="")
    target_file_id :Optional[IdentifierStr] = Field(None, title="target file id", description="")
    priority : Optional[int]= Field(None, title="priority", description="",ge=0)
    due_date : Optional[datetime] = Field(None, title="due date", description="")
    status : Optional[StatusStr] = Field(None, title="status", description="")
    data : Optional[dict] = Field(None, title="data", description="Unique identifier for the user")
    current_step_index : Optional[int] = Field(None, title="current_step_index", description="",ge=0)
    current_user_id :Optional[IdentifierStr] = Field(None, title="current_user_id", description="")

# class TranslationJobUpdateSchema(BaseSchema):
#     # Basic fields
#     title: Optional[TitleStr] = Field(None, title="", description="")
#     description: Optional[DescriptionStr] = Field(None, title="", description="")
#     source_language: Optional[LanguageStr] = Field(None, title="Source language", description="")
#     target_language: Optional[LanguageStr] = Field(None, title="Target language", description="")
#     priority: Optional[int] = Field(None, title="priority", description="", ge=0)
#     due_date: Optional[datetime] = Field(None, title="due date", description="")
#     status: Optional[StatusStr] = Field(None, title="status", description="")
#     data: Optional[dict] = Field(None, title="data", description="")
#     current_step_index: Optional[int] = Field(None, title="current_step_index", description="", ge=0)

#     # File references
#     source_file_id: Optional[IdentifierStr] = Field(None, title="source file id", description="")
#     reference_file_id: Optional[IdentifierStr] = Field(None, title="reference file id", description="")
#     target_file_id: Optional[IdentifierStr] = Field(None, title="target file id", description="")

#     # User references and timestamps
#     current_user_id: Optional[IdentifierStr] = Field(None, title="", description="")
#     created_by: Optional[IdentifierStr] = Field(None, title="", description="")
#     updated_by: Optional[IdentifierStr] = Field(None, title="", description="")
#     created_at: Optional[datetime] = Field(None, title="", description="")
#     updated_at: Optional[datetime] = Field(None, title="", description="")

#     # Approval fields
#     approved_at: Optional[datetime] = Field(None, title="", description="")
#     approved_by: Optional[IdentifierStr] = Field(None, title="", description="")

#     # Archive fields
#     archived_at: Optional[datetime] = Field(None, title="", description="")
#     archived_by: Optional[IdentifierStr] = Field(None, title="", description="")

#     # Deletion fields
#     deleted_at: Optional[datetime] = Field(None, title="", description="")
#     deleted_by: Optional[IdentifierStr] = Field(None, title="", description="")

#     # User names (from UserFullNamesModificationSchema)
#     created_by_user: Optional[Union[NameStr, FullNameStr]] = Field(None, title="creator name", description="")
#     updated_by_user: Optional[Union[NameStr, FullNameStr]] = Field(None, title="updater name", description="")
#     current_user: Optional[Union[NameStr, FullNameStr]] = Field(None, title="current user name", description="")

class TranslationJobResponseSchema(BaseResponseSchema):
    data: TranslationJobSchema

class TranslationJobsResponseSchema(BaseResponseSchema):
    data: List[TranslationJobSchema]


class PublicTranslationJobResponseSchema(BaseResponseSchema):
    data: PublicTranslationJobSchema

class PublicTranslationJobsResponseSchema(BaseResponseSchema):
    data: List[PublicTranslationJobSchema]






