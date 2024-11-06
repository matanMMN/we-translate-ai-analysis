from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, HttpUrl,constr,field_validator,Field,EmailStr,StringConstraints,ConfigDict
import re
from typing_extensions import Annotated



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


class FileCreateSchema(BaseFileSchema):
    pass


class FileResponseSchema(BaseResponseSchema):
    data: BaseFileSchema

class FilesResponseSchema(BaseResponseSchema):
    data: List[BaseFileSchema]







