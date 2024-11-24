from pydantic import ConfigDict,Field,PrivateAttr, UrlConstraints,StringConstraints
from pydantic_core import Url
from pydantic_settings import BaseSettings
from typing import Annotated
import os

class CeleryConfig:
    CELERY_BACKEND_URL: Annotated[
        str,
        StringConstraints(),
        # UrlConstraints(
        #     # allowed_schemes=['redis', 'rediss'],
        #     # default_host='localhost',
        #     # default_port=6379,
        #     # default_path='/0'
        # ),
    ] = Field(os.environ.get("CELERY_BACKEND_URL","redis://redis:6379/0"),title="",description="")

    CELERY_BROKER_URL: Annotated[
        Url,
        UrlConstraints(
            # allowed_schemes=['amqp', 'rediss'] ,
            # default_host='localhost',
            # default_port=5672,
            # default_path='/'
        )
    ] = Field(os.environ.get("CELERY_BROKER_URL","amqp://user:password@rabbitmq:5672//"),title="",description="")
