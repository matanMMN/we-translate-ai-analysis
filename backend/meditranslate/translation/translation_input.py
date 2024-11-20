# from pydantic import BaseModel,StringConstraints
# from meditranslate.app.shared.base_schema import BaseSchema
# from pydantic import Field
from typing import Dict, Optional
from io import BytesIO
from dataclasses import dataclass


# class TranslationInput(BaseSchema):
#     config: Optional[Dict[str,str]] = Field(None,title="",description="")
#     input_bytes: BytesIO
#     reference_bytes: BytesIO


@dataclass
class FileTranslationInput:
    input_bytes: BytesIO
    reference_bytes: BytesIO
    config: Optional[Dict[str, str]] = None


@dataclass
class TextTranslationInput:
    input_text: str
    reference_bytes: BytesIO
    config: Optional[Dict[str, str]] = None
