from idlelib.pyparse import trans
from io import BytesIO
from typing import Any,Dict,List,Optional,Tuple

from sqlalchemy.sql.functions import current_user

from meditranslate.src.translations.translation_repository import TranslationRepository
from meditranslate.app.db.models import Translation
from meditranslate.app.shared.base_service import BaseService
from meditranslate.app.errors import AppError,ErrorSeverity,ErrorType,HTTPStatus
from meditranslate.app.db.models import Translation
from meditranslate.src.translations.translation_schemas import (
    TranslationCreateSchema,
    GetManySchema,
    TranslationSchema,
    TranslationTextSchema,
    TranslationFileSchema
)
from meditranslate.app.db import User,File
from meditranslate.translation import TranslationEngine
from meditranslate.translation.translation_input import TranslationInput
from meditranslate.translation.translation_output import TranslationOutput
from meditranslate.utils.files.file_format_type import FileFormatType
from meditranslate.app.loggers import logger
from meditranslate.utils.files.formats.file_format_handler import FileFormatHandler

class TranslationService(BaseService[Translation]):
    def __init__(self, translation_repository: TranslationRepository,translation_engine:TranslationEngine):
        super().__init__(model=Translation, repository=translation_repository)
        self.translation_repository = translation_repository
        self.translation_engine = translation_engine

    def _to_public_translation(self,translation:Translation) -> dict:
        public_translation = translation.as_dict()
        # if translation.created_by_user is not None:
        #     public_translation["created_by_user"] = translation.created_by_user.full_name
        # if translation.translation_job is not None:
        #     public_translation["translation_job"] = translation.translation_job.title
        return public_translation

    async def create_translation(self,current_user:User,translation_create_schema:TranslationCreateSchema) -> Translation:
        new_translation_data = translation_create_schema.model_dump()
        new_translation_data["created_by"] = current_user.id
        new_translation = await self.translation_repository.create(new_translation_data)
        return new_translation

    async def get_translation(self,translation_id: str,raise_exception:bool=True,to_public:bool=True) -> Translation:
        translation = await self.translation_repository.get_by(field="id",value=translation_id,joins=None,unique=True)
        if not translation:
            if raise_exception:
                raise AppError(
                    title="get translation endpoint",
                    http_status=HTTPStatus.NOT_FOUND
                )
        else:
            if to_public:
                return self._to_public_translation(translation)
            else:
                return translation

    async def delete_translation(self,current_user:User,translation_id: str) -> None:
        translation = await self.translation_repository.get_by("id",translation_id,unique=True)
        if not translation:
            raise AppError(
                title="delete translation endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        return await self.translation_repository.delete(translation)


    async def get_many_translations(self,get_many_schema: GetManySchema) -> Tuple[List[Translation],int]:
        translations,total = await self.translation_repository.get_many(**get_many_schema.model_dump())
        public_translations = [self._to_public_translation(translation) for translation in translations]
        return public_translations,total


    @staticmethod
    def _get_supported_formats() -> List[FileFormatType]:
        return [
            FileFormatType.DOCX
        ]


    @staticmethod
    def _is_supported_format(format_type_string: str) -> bool:
        try:
            file_format_type = FileFormatType(format_type_string)
        except ValueError as e:
            logger.error(f"error in file extention '{format_type_string}' in translate file {str(e)}")
            raise e

        if file_format_type not in TranslationService._get_supported_formats():
            return False

        return True

    @staticmethod
    def _validate_formats(*to_vals: Tuple[str, str, str]):
        """
        Used to validate file formats before access to translation engine.

        :param to_vals: Tuples of format, file name and short description to be inserted into error message.
        """
        for val in to_vals:
            format_, name, desc = val
            if not TranslationService._is_supported_format(format_):
                message = f"Can not handle file format {format_} for file {name} ({desc})"

                raise AppError(
                    title="Developer Error: Unsupported file format",
                    description=message,
                    http_status=HTTPStatus.INTERNAL_SERVER_ERROR
                )

    async def translate_file(
            self,
            current_user: User,
            src_file_pointer: File,
            src_file_stream: BytesIO,
            ref_file_pointer: File,
            ref_file_stream: BytesIO,
            translation_file_schema: TranslationFileSchema):
        src_file_extension = src_file_pointer.file_format_type
        src_file_name = src_file_pointer.file_name
        dst_file_extension = translation_file_schema.target_file_format

        if src_file_name is None:
            raise AppError("no file name")

        src_file_name = src_file_name.rsplit(".", 1)[0]

        try:
            src_file_format_type = FileFormatType(src_file_extension)
        except ValueError as e:
            logger.error(f"error in file extention '{src_file_extension}' in translate file {str(e)}")
            raise e

        try:
            dst_file_format_type = FileFormatType(dst_file_extension)
        except ValueError as e:
            logger.error(f"error in file extention '{dst_file_extension}' in translate file {str(e)}")
            raise e

        translation_input = TranslationInput(input_bytes=src_file_stream, reference_bytes=ref_file_stream)
        translation_output = await self.translation_engine.translate_file(translation_input)

        created_translation = await self.create_translation(
            current_user=current_user,
            translation_create_schema=TranslationCreateSchema(
                source_language=translation_file_schema.source_language,
                target_language=translation_file_schema.target_language,
                input_text=FileFormatHandler().extract_text(
                    file_format=src_file_format_type, file_stream=src_file_stream),
                output_text=FileFormatHandler().extract_text(
                    file_format=dst_file_format_type, file_stream=translation_output.output_bytes),
                translation_job_id=translation_file_schema.translation_job_id,
                translation_metadata=translation_output.translation_metadata
            )
        )

        if created_translation is None:
            raise AppError(
                title="failed to create translation",
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

        new_file_stream = translation_output.output_bytes
        new_file_stream.seek(0)
        content_type = FileFormatHandler().get_content_type(src_file_format_type)
        new_file_name = (f"{src_file_name}"
                         + f"_{translation_file_schema.source_language}"
                         + f"_{translation_file_schema.target_language}"
                         + f".{src_file_format_type.value}")

        return new_file_stream, new_file_name, content_type


    async def translate_text(self,current_user:User,translation_text_schema:TranslationTextSchema):
        translation_input = TranslationInput(input_text=translation_text_schema.input_text,config=None)
        translation_output = await self.translation_engine.translate_file(translation_input)
        created_translation = await self.create_translation(
            current_user=current_user,
            translation_create_schema=TranslationCreateSchema(
                    source_language=translation_text_schema.source_language,
                    target_language=translation_text_schema.target_language,
                    input_text=translation_text_schema.input_text,
                    translation_job_id=translation_text_schema.translation_job_id,
                    translation_metadata=translation_output.translation_metadata,
                    output_text=translation_output.output_text
                )
        )
        return self._to_public_translation(created_translation)


