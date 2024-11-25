# from pydantic import BaseModel,StringConstraints
# from meditranslate.app.shared.base_schema import BaseSchema
from dataclasses import dataclass
from typing import Dict
from io import BytesIO

# class TranslationOutput(BaseSchema):
#     translation_metadata: Dict[str,str]
#     output_bytes: BytesIO

@dataclass
class FileTranslationOutput:
    output_bytes: BytesIO
    translation_metadata: Dict[str, str]


@dataclass
class TextTranslationOutput:
    output_text: str
    translation_metadata: Dict[str, str]
