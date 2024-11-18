# from pydantic import BaseModel,StringConstraints
# from meditranslate.app.shared.base_schema import BaseSchema
# from pydantic import Field
from typing import Dict, Optional
from io import BytesIO

# class TranslationInput(BaseSchema):
#     config: Optional[Dict[str,str]] = Field(None,title="",description="")
#     input_bytes: BytesIO
#     reference_bytes: BytesIO

class TranslationInput:
    def __init__(self, input_bytes: BytesIO, reference_bytes: BytesIO, config: Optional[Dict[str, str]]):
        self.input_bytes = input_bytes
        self.reference_bytes = reference_bytes
        self.config = config
