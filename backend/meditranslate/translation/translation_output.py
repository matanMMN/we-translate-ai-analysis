from pydantic import BaseModel,StringConstraints
from meditranslate.app.shared.base_schema import BaseSchema
from typing import Dict,Annotated

class TranslationOutput(BaseSchema):
    translation_metadata:Dict[str,str]
    output_text:Annotated[str,StringConstraints()]
