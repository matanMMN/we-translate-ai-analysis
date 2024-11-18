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
class TranslationInput:
    input_bytes: BytesIO
    input_fname: str
    reference_bytes: BytesIO
    reference_fname: str
    user_id: str
    config: Optional[Dict[str, str]] = None
