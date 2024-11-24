from pydantic import BaseModel as PydanticBaseModel, Field,ConfigDict, PrivateAttr,model_validator,StringConstraints
from typing import Annotated, Any, ClassVar, Literal, Optional, Union,List,Dict,Type,Tuple
from meditranslate.app.loggers import logger
import datetime
from meditranslate.utils.datetime import datetime_to_str
from meditranslate.app.configurations import config
import json

class BaseSchema(PydanticBaseModel):

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda _: datetime_to_str(config.TIMEZONE)
        },
        populate_by_name=True,
        extra='ignore', # for raising error
        strict=False,
        json_schema_extra={

        }
    )
    __pydantic_extra__: Dict[str, int] = Field(init=False) # all extra , if extra is allowed
    schema_name: ClassVar[str]  # Class-level variable to store schema name


    def __init__(self, **data):
        super().__init__(**data)

    # def __init_subclass__(cls, **kwargs):
    #     """Dynamically set schema_name to the subclass name."""
    #     super().__init_subclass__(**kwargs)
    #     cls.schema_name = cls.__name__.title().replace("Schema","")

    #     # Dynamically set schema_name from class name (without 'Schema' suffix)
    #     cls.schema_name = cls.__name__.title().replace("Schema", "")

    #     # Dynamically modify field titles based on schema name
    #     for field_name, field in cls.__fields__.items():
    #         # Modify title and description for fields that have a `Field` function
    #         if isinstance(field.default, Field):  # Check if it's a Pydantic Field
    #             field.default.title = f"{cls.schema_name} {field_name.title()} Schema"
    #             field.default.description = f"The {field_name} of {cls.schema_name}."


    @model_validator(mode="after")
    def log_model_creation(self) -> 'BaseSchema':
        logger.debug(f"Created Pydantic model: {self.__class__.__name__} ")
        return self

    @classmethod
    def model_parametrized_name(cls, params: Tuple[Type[Any], ...]) -> str:
        return f'{params[0].__name__.title()}Schema'
