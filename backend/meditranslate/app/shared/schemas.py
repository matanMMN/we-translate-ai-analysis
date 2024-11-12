from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, Field,ConfigDict, PrivateAttr, StringConstraints,model_validator
from meditranslate.app.shared.constants import SortOrder
from meditranslate.app.shared.base_schema import BaseSchema
from pydantic import BaseModel
from typing import Annotated, Optional,Dict,Any,List, Union
from pydantic.functional_validators import AfterValidator
import json


class PaginationSchema(BaseSchema):
    total: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None


class MetaSchema(BaseSchema):
    pagination: Optional[PaginationSchema] = None


class GetManySchema(BaseSchema):
    model_config:ConfigDict = ConfigDict(
        from_attributes=True
    )
    offset: Optional[int] = Field(default=0, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    sort_by: Optional[str] = None
    sort_order: Optional[str] = SortOrder.asc.value
    filters: Optional[Dict[str, Any] | str] = ""


class BaseResponseSchema(BaseSchema):
    data: Optional[Any] = None  # When returning actual data
    message: Optional[str] = None  # Success or info message
    error: Optional[str] = None  # Error message in case of failure
    status_code: Optional[int] = Field(default=200, description="HTTP status code")
    meta: Optional[MetaSchema] = None  # Metadata, often for pagination
    warnings: Optional[List[str]] = None  # Warnings or additional information

LETTERS_ONLY_REGEX_PATTERN = "^[A-Za-z]"

IdentifierStr = Annotated[str,
        StringConstraints(
            strip_whitespace=True,
            max_length=None,
            min_length=4,
            pattern=None,
        ),
]

NameStr  = Annotated[str,
        StringConstraints(
            strip_whitespace=True,
            max_length=None,
            min_length=1,
            pattern=LETTERS_ONLY_REGEX_PATTERN,
        ),
]

FullNameStr  = Annotated[str,
        StringConstraints(
            strip_whitespace=True,
            max_length=None,
            min_length=1,
            pattern="^[A-Za-z]+( [A-Za-z]+)+$",
        ),
]
LanguageStr = Annotated[str,
        StringConstraints(
            strip_whitespace=True,
            max_length=49,
            min_length=2,
            to_lower=True,
            pattern=LETTERS_ONLY_REGEX_PATTERN,
        ),
]

FileFormatTypeStr  = Annotated[
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

LETTERS_NUMBERS_ONLY_REGEX_PATTERN = r"^[A-Za-z0-9]*"



PassWordStr  = Annotated[str,
        StringConstraints(
            strip_whitespace=True,
            max_length=None,
            min_length=4,
            pattern=None,
        ),
]


UserNameStr = Annotated[str,
        StringConstraints(
            strip_whitespace=True,
            max_length=None,
            min_length=4,
            pattern="^[A-Za-z][A-Za-z0-9_]*", # {7,29} , "^[A-Za-z][A-Za-z0-9_]{7,29}$"

        ),
]

def valid_json(v:str):
    try:
        assert isinstance(v, str), "value must be string"
        value = json.loads(v)
        assert isinstance(value, dict) ,"value must be a valid json"
    except json.JSONDecodeError:
        raise ValueError("Value must be a valid JSON string or a dictionary")
    return v

JsonStr = Annotated[str, AfterValidator(valid_json)]


class ObjectIdSchema(BaseSchema):
    id: IdentifierStr = Field(...)

class ModificationTimestampSchema(BaseSchema):
    created_at: datetime = Field(..., title=" created at id", description="Timestamp when the object was created.")
    updated_at: datetime = Field(..., title=" updated at id", description="Timestamp when the object was last updated.")

class UserIdentifiersModificationSchema(BaseSchema):
    created_by: Optional[IdentifierStr] = Field(None, title="creator user id",description="user that created this")
    updated_by: Optional[IdentifierStr] = Field(None, title="updator user id",description="last user updated.")

class UserFullNamesModificationSchema(BaseSchema):
    created_by_user: Optional[Union[NameStr,FullNameStr]] = Field(None, title="creator full name",description="full name of user")
    updated_by_user: Optional[Union[NameStr,FullNameStr]] = Field(None, title="updator user full name",description="ful name of user")

class TranslationLanguagesSchema(BaseSchema):
    source_language : LanguageStr = Field(..., title="source lang", description="")
    target_language : LanguageStr = Field(..., title="target lang", description="")
