from io import BytesIO
from typing import Any, List,Tuple

from fastapi import UploadFile
from meditranslate.app.shared.base_controller import BaseController
from meditranslate.src.files.file_service import FileService
from meditranslate.src.translation_jobs.translation_job_service import TranslationJobService
from meditranslate.src.translations.translation_service import TranslationService
from meditranslate.src.translations.translation_schemas import (
    TranslationCreateSchema,
    GetManySchema,
    TranslationFileSchema,
    TranslationTextSchema
)
from meditranslate.app.db.models import Translation
from meditranslate.app.db.transaction import Transactional,Propagation
from meditranslate.src.users.user import User
from meditranslate.app.loggers import logger


class TranslationController(BaseController[Translation]):
    def __init__(
            self,
            translation_service: TranslationService,
            file_service: FileService,
            translation_job_service: TranslationJobService) -> None:
        super().__init__(Translation,translation_service)
        self.translation_service: TranslationService = translation_service
        self.file_service: FileService = file_service
        self.translation_job_service: TranslationJobService = translation_job_service

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def create_translation(self,current_user:User,translation_create_schema:TranslationCreateSchema) -> Translation:
        return await self.translation_service.create_translation(current_user,translation_create_schema)

    async def get_translation(self,translation_id: str) -> Translation:
        return await self.translation_service.get_translation(translation_id)

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def delete_translation(self,current_user:User,translation_id: str):
        return await self.translation_service.delete_translation(current_user,translation_id)

    async def get_many_translations(self,get_many_schema:GetManySchema) -> Tuple[List[Translation],int]:
        return await self.translation_service.get_many_translations(get_many_schema)

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def translate_file(self,current_user:User,file_id:str,translation_file_schema:TranslationFileSchema):
        src_file = await self.file_service.fetch_file_entity(file_id=file_id)
        src_file_stream, _ ,_ = await self.file_service.download_file_sync(file_id=file_id)

        translation_job = await self.translation_job_service.get_translation_job(
            translation_file_schema.translation_job_id, to_public=False)
        ref_file = await self.file_service.fetch_file_entity(translation_job.reference_file_id)
        ref_file_stream, _, _ = await self.file_service.download_file_sync(file_id=ref_file.id)

        translated_file_stream, new_file_name, content_type = await self.translation_service.translate_file(
            current_user,
            src_file,
            src_file_stream,
            ref_file,
            ref_file_stream,
            translation_file_schema
        )

        upload_file = UploadFile(
            filename=new_file_name,
            file=translated_file_stream,
            headers={
                'Content-Type': content_type

            }
        )
        return await self.file_service.upload_file(current_user,upload_file)

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def translate_text(self,current_user:User,translation_text_schema:TranslationTextSchema):
        return await self.translation_service.translate_text(current_user,translation_text_schema)

