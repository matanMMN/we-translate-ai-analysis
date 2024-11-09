from typing import Any,Dict,List,Optional,Tuple
from meditranslate.src.translations.translation_repository import TranslationRepository
from meditranslate.app.db.models import Translation
from meditranslate.app.shared.base_service import BaseService
from meditranslate.app.errors import AppError,ErrorSeverity,ErrorType,HTTPStatus
from meditranslate.app.db.models import Translation
from meditranslate.src.translations.translation_schemas import (
    TranslationCreateSchema,
    GetManySchema,
    TranslationTextSchema
)
from meditranslate.translation import TranslationEngine
from meditranslate.translation.translation_input import TranslationInput
from meditranslate.translation.translation_output import TranslationOutput

class TranslationService(BaseService[Translation]):
    def __init__(self, translation_repository: TranslationRepository,translation_engine:TranslationEngine):
        super().__init__(model=Translation, repository=translation_repository)
        self.translation_repository = translation_repository
        self.translation_engine = translation_engine

    def _to_public_translation(self,translation:Translation) -> dict:
        public_translation = translation.as_dict()
        return public_translation

    async def create_translation(self,translation_create_schema:TranslationCreateSchema) -> Translation:
        new_translation_data = translation_create_schema.model_dump()
        new_translation = await self.translation_repository.create(new_translation_data)
        return self._to_public_translation(new_translation)



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

    async def delete_translation(self,translation_id: str) -> None:
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

    def export_translations(self):
        pass

    async def translate_file(self):
        pass

    async def translate_text(self,translation_create_schema:TranslationCreateSchema):
        input_text = translation_create_schema.input_text
        translation_input = TranslationInput()
        translation_output:TranslationOutput = await self.translation_engine.translate(translation_input)
        created_translation = await self.create_translation(TranslationCreateSchema(
        ))
        response = TranslationTextSchema(

        )
        return response.model_dump()
