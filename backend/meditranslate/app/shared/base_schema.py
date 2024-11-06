from pydantic import BaseModel as PydanticBaseModel, Field,ConfigDict, PrivateAttr,model_validator
from typing import Annotated, Any, ClassVar, Literal, Optional, Union,List,Dict,Type,Tuple
from meditranslate.app.loggers import logger
import datetime
from meditranslate.utils.datetime import datetime_to_str
from meditranslate.app.configurations import config

class BaseSchema(PydanticBaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: lambda _: datetime_to_str(config.TIMEZONE)},
        populate_by_name=True,
        extra='forbid', # for raising error
        json_schema_extra={

        }
    )
    __pydantic_extra__: Dict[str, int] = Field(init=False) # all extra , if extra is allowed

    def __init__(self, **data):
        super().__init__(**data)

    @model_validator(mode="after")
    def log_model_creation(self) -> 'BaseSchema':
        logger.debug(f"Created Pydantic model: {self.__class__.__name__} ")
        return self

    @classmethod
    def model_parametrized_name(cls, params: Tuple[Type[Any], ...]) -> str:
        return f'{params[0].__name__.title()}Schema'

