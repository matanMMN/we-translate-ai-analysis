""" Constant App Config Logic """
from pydantic import Field
from meditranslate.app.configurations.config import Config
from meditranslate.utils.files.file_format_type import FileFormatType
from meditranslate.utils.language import Language
from meditranslate.utils.security.json_web_tokens import JWTAlgorithm
from typing import Annotated,ClassVar, List,Set,Tuple
from pydantic import StringConstraints, PositiveInt, PositiveFloat
import os
from datetime import date,datetime
from languages import Hebrew,English

class AppConfig(Config):
    APP_NAME:Annotated[str,StringConstraints(
        strip_whitespace=True
    )] = Field(os.environ.get("APP_NAME","wetranslateai"))

    BUCKET_NAME:Annotated[str,StringConstraints(
        strip_whitespace=True
    )] = Field(os.environ.get("BUCKET_NAME","APP_BUCKET"))


    JWT_EXPIRE_MINUTES: int = Field(os.environ.get("JWT_EXPIRE_MINUTES", 60 * 24 * 30),title="jwt expire",description="",gt=5)
    JWT_ALGORITHM: JWTAlgorithm = Field(JWTAlgorithm.HS256,title="jwt algo",description="",validate_default=True,repr=False)

    APP_DESCRIPTION:Annotated[str,StringConstraints(
        strip_whitespace=True
    )] = Field(os.environ.get("APP_DESCRIPTION","No Description"))


    RELEASE_VERSION:Annotated[str,StringConstraints(
        strip_whitespace=True
    )] = Field(os.environ.get("RELEASE_VERSION","1.0.0"))

    RELEASE_DATE:datetime = Field(os.environ.get("RELEASE_DATE",datetime.today()))

    ALLOWED_UPLOAD_FILE_EXTENSIONS: Set[FileFormatType]= Field({
        FileFormatType.TXT,
        FileFormatType.PDF,
        FileFormatType.DOC,
        FileFormatType.DOCX,
        FileFormatType.TXT,
        FileFormatType.HTML,
        FileFormatType.MD
    },title="ALLOWED_UPLOAD_FILE_EXTENSIONS",description="")

    ALLOWED_TARGET_FILE_EXTENSIONS: Set[FileFormatType]= Field({
        FileFormatType.TXT,
        FileFormatType.PDF,
        FileFormatType.DOC,
        FileFormatType.DOCX,
        FileFormatType.TXT,
        FileFormatType.HTML,
        FileFormatType.MD
    },title="ALLOWED_TARGET_FILE_EXTENSIONS",description="")

    ALLOWED_REFERENCE_FILE_EXTENSIONS: Set[FileFormatType]= Field({
        FileFormatType.TXT,
        FileFormatType.PDF,
        FileFormatType.DOC,
        FileFormatType.DOCX,
        FileFormatType.TXT,
        FileFormatType.HTML,
        FileFormatType.MD
    },title="ALLOWED_REFERENCE_FILE_EXTENSIONS",description="")

    ALLOWED_SOURCE_FILE_EXTENSIONS: Set[FileFormatType]= Field({
        FileFormatType.TXT,
        FileFormatType.PDF,
        FileFormatType.DOC,
        FileFormatType.DOCX,
        FileFormatType.TXT,
        FileFormatType.HTML,
        FileFormatType.MD
    },title="ALLOWED_SOURCE_FILE_EXTENSIONS",description="")


    ALLOWED_SOURCE_LANGUAGES: Set[Language] = Field({Hebrew,English},title="", description="")

    ALLOWED_TARGET_LANGUAGES: Set[Language] = Field({Hebrew,English},title="", description="")

    UPLOAD_FILE_MAX_SIZE_IN_KB: float = Field(os.environ.get("UPLOAD_FILE_MAX_SIZE_IN_KB",100000), title="", description="", gt=0)


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

    ANTHROPIC_API_KEY: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("ANTHROPIC_API_KEY"),title="ANTHROPIC_API_KEY",description="")

    ANTHROPIC_MODEL_NAME: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("ANTHROPIC_MODEL_NAME"),title="ANTHROPIC_MODEL_NAME",description="")

    CLAUDE_MAX_TOKENS: PositiveInt = Field(
        os.environ.get("CLAUDE_MAX_TOKENS"),
        le=4096,
        title="CLAUDE_MAX_TOKENS",description="Maximum amount of tokens to generate per response from Claude.")

    CLAUDE_TEMPERATURE: PositiveFloat = Field(
        os.environ.get("CLAUDE_TEMPERATURE"),
        lt=1,
        title="CLAUDE_TEMPERATURE",description="Temperature to be used on generation by Claude.")

    CLAUDE_MAX_REPS: PositiveInt = Field(
        os.environ.get("CLAUDE_MAX_REPS"),
        lt=10,
        title="CLAUDE_MAX_REPS",description="Max repetitions to request a response from the Claude.")

    AWS_ENDPOINT_URL:Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("AWS_ENDPOINT_URL","http://0.0.0.0:4566"),title="AWS_ENDPOINT_URL",description="")

    AWS_ACCESS_KEY_ID:Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("AWS_ACCESS_KEY_ID"),title="AWS_ACCESS_KEY_ID",description="")

    AWS_SECRET_ACCESS_KEY:Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("AWS_SECRET_ACCESS_KEY"),title="AWS_SECRET_ACCESS_KEY",description="")


    AWS_REGION_NAME:Annotated[
        str,
        StringConstraints(
            strip_whitespace=True
        )
    ] = Field(os.environ.get("AWS_REGION_NAME"),title="AWS_REGION_NAME",description="")


    # endpoint_url = "http://localhost:4566"

