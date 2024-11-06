from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, HttpUrl,constr,field_validator,Field,EmailStr,StringConstraints,ConfigDict
import re
from typing_extensions import Annotated





class BaseTranslationJobSchema(BaseSchema):
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

    title : Annotated[
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

    description : Annotated[
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

    source_language : Annotated[
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

    target_language : Annotated[
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

    priority : Annotated[
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

    due_date : Annotated[
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

    status : Annotated[
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
                ] = Field(None, title="", description="Unique identifier for the user")
    # current_step_index
    # reference_file_id
    # source_file_id
    # current_user_id
    # created_by
    # updated_by
    # approved_at
    # approved_by
    # archived_at
    # archived_by
    # deleted_at
    # deleted_by
    # data

class TranslationJobCreateSchema(BaseTranslationJobSchema):
    pass

class TranslationJobUpdateSchema(BaseTranslationJobSchema):
    pass


class TranslationJobResponseSchema(BaseResponseSchema):
    data: BaseTranslationJobSchema

class TranslationJobsResponseSchema(BaseResponseSchema):
    data: List[BaseTranslationJobSchema]







