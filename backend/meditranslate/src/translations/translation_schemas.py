from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema,TranslationLanguagesSchema,ObjectIdSchema,IdentifierStr,ModificationTimestampSchema,UserFullNamesModificationSchema,UserIdentifiersModificationSchema,FileFormatTypeStr,LanguageStr
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, HttpUrl,constr,field_validator,Field,StringConstraints,ConfigDict
import re
from typing_extensions import Annotated

InputTextStr = Annotated[
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
                ]

OutputTextStr = Annotated[
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
                ]


class PublicTranslationSchema(ObjectIdSchema,TranslationLanguagesSchema,UserFullNamesModificationSchema,UserIdentifiersModificationSchema,ModificationTimestampSchema):
    translation_job_id : Optional[IdentifierStr] = Field(None, title="translation_job_id", description="Unique identifier for the user")
    input_text: InputTextStr = Field(None, title="translation meta data", description="Unique identifier for the user")
    output_text: OutputTextStr = Field(None, title="translation meta data", description="Unique identifier for the user")

class TranslationSchema(ObjectIdSchema,TranslationLanguagesSchema,UserFullNamesModificationSchema,ModificationTimestampSchema):
    translation_job_id : Optional[IdentifierStr] = Field(None, title="translation_job_id", description="Unique identifier for the user")
    input_text: InputTextStr = Field(None, title="translation meta data", description="Unique identifier for the user")
    output_text: OutputTextStr = Field(None, title="translation meta data", description="Unique identifier for the user")
    translation_metadata : Optional[Dict[str,str]] = Field(None, title="translation meta data", description="Unique identifier for the user")

class TranslationCreateSchema(TranslationLanguagesSchema):
    translation_job_id : Optional[IdentifierStr] = Field(None, title="translation_job_id", description="Unique identifier for the user")
    input_text: Optional[InputTextStr] = Field(None, title="translation meta data", description="Unique identifier for the user")
    output_text: Optional[OutputTextStr] = Field(None, title="translation meta data", description="Unique identifier for the user")
    translation_metadata : Optional[Dict[str,str]] = Field(None, title="translation meta data", description="Unique identifier for the user")

class TranslationFileSchema(BaseSchema):
    translation_job_id : Optional[IdentifierStr] = Field(None, title="translation_job_id", description="")
    source_language : Optional[LanguageStr]= Field(..., title="source_language", description="")
    target_language : Optional[LanguageStr] = Field(..., title="target_language", description="")
    target_file_format : Optional[FileFormatTypeStr] = Field(None, title="target_file_format", description="")

class TranslationTextSchema(TranslationLanguagesSchema):
    translation_job_id : Optional[IdentifierStr] = Field(None, title="translation_job_id", description="")
    input_text : InputTextStr= Field(..., title="input text", description="")

class TranslationOutputResponseSchema(BaseResponseSchema):
    data: OutputTextStr

class TranslationResponseSchema(BaseResponseSchema):
    data: TranslationSchema

class TranslationsResponseSchema(BaseResponseSchema):
    data: List[TranslationSchema]

class PublicTranslationResponseSchema(BaseResponseSchema):
    data: PublicTranslationSchema

class PublicTranslationsResponseSchema(BaseResponseSchema):
    data: List[PublicTranslationSchema]


