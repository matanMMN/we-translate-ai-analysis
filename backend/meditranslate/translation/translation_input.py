from pydantic import StringConstraints,Field
from meditranslate.app.shared.base_schema import BaseSchema
from typing import Dict,Annotated,Optional

class TranslationInput(BaseSchema):
    config:Optional[Dict[str,str]] = Field(None,title="",description="")
    input_text:Annotated[str,StringConstraints()]
