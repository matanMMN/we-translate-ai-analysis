from pydantic import ConfigDict,Field,PrivateAttr, UrlConstraints,StringConstraints
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    model_config:ConfigDict = ConfigDict(extra="forbid")
    
