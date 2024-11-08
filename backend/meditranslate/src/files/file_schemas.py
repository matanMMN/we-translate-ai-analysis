from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, HttpUrl,constr,field_validator,Field,EmailStr,StringConstraints,ConfigDict
import re
from typing_extensions import Annotated

from meditranslate.utils.files.file_format_type import FileFormatType
from fastapi import Form


class BaseFileSchema(BaseSchema):
    model_config:ConfigDict=ConfigDict(
        extra="ignore",
        strict=False
    )
    id : Annotated[
                    Optional[str],
                    StringConstraints(
                        strip_whitespace=True,
                        to_upper=None,
                        to_lower=None,
                        strict=None,
                        max_length=None,
                        min_length=None,
                        pattern=None,
                    ),
                ] = Field(None, title="User ID", description="Unique identifier for the user")

    file_size: Optional[int] = Field(None,title="file_size", description="")


    file_format_type: Annotated[
        Optional[FileFormatType],
        StringConstraints(
            strip_whitespace=True,
            to_upper=None,
            to_lower=None,
            strict=None,
            max_length=None,
            min_length=None,
            pattern=None
        )
    ] = Field(None,title="file_format_type", description="")

    file_metadata: Optional[dict] = Field({},title="file_metadata", description="")





class FileCreateSchema(BaseFileSchema):
    pass


class FilePointerResponseSchema(BaseResponseSchema):
    data: BaseFileSchema

class FilePointersResponseSchema(BaseResponseSchema):
    data: List[BaseFileSchema]


