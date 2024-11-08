from pydantic import ConfigDict,Field,PrivateAttr, UrlConstraints,StringConstraints
from typing import Annotated, Literal,Tuple
from pydantic_core import Url
import os
import sys
from datetime import datetime
from meditranslate.app.configurations.base_config import BaseConfig
from enum import Enum
from meditranslate.utils.security.json_web_tokens import JWTAlgorithm

LOG_LEVEL = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]



class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Config(BaseConfig):
    _defined_at: datetime = PrivateAttr(default_factory=datetime.now)

    GLOBAL_RATE_LIMIT_PER_MINUTE: int = Field(os.environ.get("GLOBAL_RATE_LIMIT_PER_MINUTE",100),title="GLOBAL_RATE_LIMIT_PER_MINUTE",description="")

    APP_HOST: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("APP_HOST"),title="host",description="")

    UPLOAD_DIR: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("UPLOAD_DIR","uploads"),title="host",description="")

    APP_PORT: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("APP_PORT"),title="port",description="")


    DOCS_URL: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("DOCS_URL","/docs"),title="",description="")

    REDOC_URL: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("REDOCS_URL","/redoc"),title="",description="")

    RETENTION_LOG_LEVEL:LOG_LEVEL = Field(
        os.environ.get(
            "RETENTION_LOG_LEVEL",
            "DEBUG",
        )
        ,title="base log level",description="")


    LAST_RUN_LOG_LEVEL:LOG_LEVEL = Field(
        os.environ.get(
            "LAST_RUN_LOG_LEVEL",
            "DEBUG",
        )
        ,title="base log level",description="")


    STD_LOG_LEVEL:LOG_LEVEL = Field(
        os.environ.get(
            "STD_LOG_LEVEL",
            "DEBUG",
        )
        ,title="base log level",description="")

    BASE_LOG_LEVEL: LOG_LEVEL = Field(
        os.environ.get(
            "BASE_LOG_LEVEL",
            "DEBUG",
        )
        ,title="base log level",description="")


    DEBUG: bool = Field(os.environ.get("DEBUG",False),title="debug",description="")
    DEBUG_ON_INIT: bool = Field(os.environ.get("DEBUG",True),title="debug",description="")
    PRINT_ENVIRONMENT: str = Field(os.environ.get("PRINT_ENVIRONMENT",""),title="print env",description="")
    PRINT_APP: str = Field(os.environ.get("PRINT_APP",""),title="print app",description="")


    ENVIRONMENT: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,

        )
    ] = Field(
        os.environ.get(
            "ENVIRONMENT",
            EnvironmentType.DEVELOPMENT.value
        )
        ,title="env",description="")




    SECRET_KEY: str = Field(os.environ.get("SHOW_SQL_ALCHEMY_QUERIES",False),title="SHOW_SQL_ALCHEMY_QUERIES",description="")
    SECRET_KEY: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=4
        )
    ] = Field(os.environ.get("SECRET_KEY","secret-key"),title="Secret Key",description="A secret key for encryption and security purposes",validate_default=True,repr=False)

    RUN_IN_DOCKER: bool = Field(os.environ.get("RUN_IN_DOCKER",False),title="is in docker",description="")

    DATABASE_DRIVER: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=4
        )
    ] = Field(os.environ.get("DATABASE_DRIVER", "postgresql+asyncpg"), title="database driver", description="")

    DATABASE_USERNAME: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=4
        )
    ] = Field(os.environ.get("DATABASE_USERNAME", "myuser"), title="database username", description="")

    DATABASE_PASSWORD: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=4
        )
    ] = Field(os.environ.get("DATABASE_PASSWORD", "mypassword"), title="database password", description="")

    DATABASE_PORT: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=4
        )
    ] = Field(os.environ.get("DATABASE_PORT", "5432"), title="database port", description="")

    DATABASE_HOST: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=4
        )
    ] = Field(os.environ.get("DATABASE_HOST", "db" if RUN_IN_DOCKER is True else "localhost"), title="database host", description="")

    DATABASE_NAME: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=4
        )
    ] = Field(os.environ.get("DATABASE_NAME", "testdb" if ENVIRONMENT == EnvironmentType.TESTING.value else "mydatabase"), title="database name", description="")

    # constructed_url = f"{DATABASE_DRIVER}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    DATABASE_URL: Annotated[
        Url,
        UrlConstraints(
            default_host="localhost",
            max_length=None
        ),
    ] = Field(os.environ.get("DATABASE_URL",f"postgresql+asyncpg://myuser:mypassword@postgresql:5432/mydatabase"),
        title="database url",
        description=""
    )

    FILE_STORAGE_URL: Annotated[
        Url,
        UrlConstraints()
    ] = Field(os.environ.get("FILE_STORAGE_URL","mongodb://user:password@mongo:27017/"), title="file storage url", description="")


    FILE_STORAGE_NAME: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=4
        )
    ] = Field(os.environ.get("FILE_STORAGE_NAME","filedb"),title="FILE_STORAGE_NAME",description="")


    CELERY_WORKER_NAME: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=4
        )
    ] = Field(os.environ.get("CELERY_WORKER_NAME","worker"),title="CELERY_WORKER_NAME",description="",validate_default=True,repr=False)

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


    SHOW_SQL_ALCHEMY_QUERIES: bool = Field(os.environ.get("SHOW_SQL_ALCHEMY_QUERIES",False),title="SHOW_SQL_ALCHEMY_QUERIES",description="")




