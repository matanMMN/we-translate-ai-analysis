from typing import Any, List,Tuple
from meditranslate.app.shared.base_controller import BaseController
from meditranslate.src.files.file_service import FileService
from meditranslate.src.translations.translation_service import TranslationService
from meditranslate.src.translations.translation_schemas import (
    TranslationCreateSchema,
    GetManySchema,
)
from meditranslate.app.db.models import Translation
from meditranslate.app.db.transaction import Transactional,Propagation


class TranslationController(BaseController[Translation]):
    def __init__(self, translation_service:TranslationService,file_service:FileService) -> None:
        super().__init__(Translation,translation_service)
        self.translation_service:TranslationService = translation_service
        self.file_service:FileService = file_service

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def create_translation(self,translation_create_schema:TranslationCreateSchema) -> Translation:
        return await self.translation_service.create_translation(translation_create_schema)

    async def get_translation(self,translation_id: str) -> Translation:
        return await self.translation_service.get_translation(translation_id)

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def delete_translation(self,translation_id: str):
        return await self.translation_service.delete_translation(translation_id)

    async def get_many_translations(self,get_many_schema:GetManySchema) -> Tuple[List[Translation],int]:
        return await self.translation_service.get_many_translations(get_many_schema)

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def translate_file(self,file_id:str):
        file = await self.file_service.get_file(file_id=file_id)
        if not file:
            pass
            # raise AppError()
        else:
            return await self.translation_service.translate_file()

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def translate_text(self,translation_create_schema:TranslationCreateSchema):
        return await self.translation_service.translate_text(translation_create_schema)

