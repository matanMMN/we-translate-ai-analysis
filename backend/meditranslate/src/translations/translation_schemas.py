from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, HttpUrl,constr,field_validator,Field,StringConstraints,ConfigDict
import re
from typing_extensions import Annotated

class BaseTranslationSchema(BaseSchema):
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
                ] = Field(None, title="translation ID", description="Unique identifier for the translation")

    translation_job_id : Annotated[
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
    ] = Field(None, title="translation_job_id", description="Unique identifier for the user")

    input_text : Annotated[
                    str,
                    StringConstraints(
                        strip_whitespace=True,
                        to_upper=None,
                        to_lower=None,
                        strict=None,
                        max_length=None,
                        min_length=None,
                        pattern=None,
                    ),
                ] = Field(None, title="translation meta data", description="Unique identifier for the user")
    output_text : Annotated[
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
                ] = Field(None, title="translation meta data", description="Unique identifier for the user")

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
                ] = Field(None, title="translation meta data", description="Unique identifier for the user")

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
                ] = Field(None, title="translation meta data", description="Unique identifier for the user")

    created_by : Annotated[
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
                ] = Field(None, title="translation meta data", description="Unique identifier for the user")

    updated_by : Annotated[
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
                ] = Field(None, title="translation meta data", description="Unique identifier for the user")

    meta : Optional[Dict[str,str]] = Field(None, title="translation meta data", description="Unique identifier for the user")
    # created_by_user
    # updated_by_user


class TranslationCreateSchema(BaseTranslationSchema):
    pass

class TranslationResponseSchema(BaseResponseSchema):
    data: BaseTranslationSchema

class TranslationsResponseSchema(BaseResponseSchema):
    data: List[BaseTranslationSchema]



class TranslationFileSchema(BaseModel):
    pass

class TranslationTextSchema(BaseModel):
    pass




