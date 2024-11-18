# from pydantic import BaseModel,StringConstraints
# from meditranslate.app.shared.base_schema import BaseSchema
from typing import Dict
from io import BytesIO

# class TranslationOutput(BaseSchema):
#     translation_metadata: Dict[str,str]
#     output_bytes: BytesIO

class TranslationOutput:
    def __init__(self, output_bytes: BytesIO, translation_metadata: Dict[str, str]):
        self.output_bytes = output_bytes
        self.translation_metadata = translation_metadata
