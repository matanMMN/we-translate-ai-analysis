""" Constant App Config Logic """
from pydantic import Field
from meditranslate.app.configurations.config import Config
from meditranslate.utils.language import Language
from meditranslate.utils.security.json_web_tokens import JWTAlgorithm
from typing import Annotated,ClassVar,Set
from pydantic import StringConstraints
import os
from datetime import date,datetime
from languages import Hebrew,English

class AppConfig(Config):
    APP_NAME:Annotated[str,StringConstraints(
        strip_whitespace=True
    )] = Field(os.environ.get("APP_NAME","wetranslateai"))


    APP_DESCRIPTION:Annotated[str,StringConstraints(
        strip_whitespace=True
    )] = Field(os.environ.get("APP_DESCRIPTION","No Description"))


    RELEASE_VERSION:Annotated[str,StringConstraints(
        strip_whitespace=True
    )] = Field(os.environ.get("RELEASE_VERSION","1.0.0"))

    RELEASE_DATE:datetime = Field(os.environ.get("RELEASE_DATE",datetime.today()))


    ALLOWED_FILE_EXTENSIONS: Annotated[Set,ClassVar]= {
        "txt",
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "gif"
    }
    ALLOWED_SOURCE_LANGUAGES: Annotated[Set,Language] = {
        Hebrew,
        English
    }
    ALLOWED_TARGET_LANGUAGES: Annotated[Set,Language] = {
        Hebrew,
        English
    }

    JWT_ALGORITHM: JWTAlgorithm = Field(JWTAlgorithm.HS256,title="",description="",validate_default=True,repr=False)
    JWT_EXPIRE_MINUTES: int = Field(60 * 24,title="exp",description="",gt=100)

    TIMEZONE:Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("TIMEZONE","Asia/Jerusalem"),title="Timezone",description="")

    OPENAI_API_KEY:Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("OPENAI_API_KEY"),title="OPENAI_API_KEY",description="")

    ANTHROPIC_API_KEY:Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("ANTHROPIC_API_KEY"),title="ANTHROPIC_API_KEY",description="")


