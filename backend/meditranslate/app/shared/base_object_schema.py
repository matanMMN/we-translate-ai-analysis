from pydantic import  Field,ConfigDict, PrivateAttr,model_validator
from typing import Annotated, Any, ClassVar, Literal, Optional, Union,List,Dict,Type,Tuple
from meditranslate.app.loggers import logger
import datetime
from meditranslate.utils.datetime import datetime_to_str
from meditranslate.app.configurations import config
from .base_schema import BaseSchema

class BaseSchema(BaseSchema):
    id :Optional[str] = Field(None,title="",description="")
    created_at:Optional[datetime.datetime] = Field(None,title="",description="")
    updated_at:Optional[datetime.datetime] = Field(None,title="",description="")
