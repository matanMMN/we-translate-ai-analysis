from typing import Any, List
from meditranslate.app.shared.base_controller import BaseController
from meditranslate.src.translation_jobs.translation_job_service import TranslationJobService
from meditranslate.src.translation_jobs.translation_job_schemas import (
    TranslationJobCreateSchema,
    GetManySchema,
    TranslationJobUpdateSchema
)
from meditranslate.app.db.models import TranslationJob,User
from meditranslate.app.db.transaction import Transactional,Propagation


class TranslationJobController(BaseController[TranslationJob]):
    def __init__(self, translation_job_service:TranslationJobService) -> None:
        super().__init__(TranslationJob,translation_job_service)
        self.translation_job_service:TranslationJobService = translation_job_service

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def create_translation_job(self,current_user:User,translation_job_create_schema:TranslationJobCreateSchema) -> TranslationJob:
        return await self.translation_job_service.create_translation_job(current_user,translation_job_create_schema)

    async def get_translation_job(self,translation_job_id: str) -> TranslationJob:
        return await self.translation_job_service.get_translation_job(translation_job_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_translation_job(self,current_user:User,translation_job_id: str, translation_job_update_schema:TranslationJobUpdateSchema) -> None:
        return await self.translation_job_service.update_translation_job(current_user,translation_job_id, translation_job_update_schema)

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def delete_translation_job(self,current_user:User,translation_job_id: str) -> None:
        return await self.translation_job_service.delete_translation_job(current_user,translation_job_id)

    async def get_many_translation_jobs(self,get_many_schema:GetManySchema) -> List[TranslationJob]:
        return await self.translation_job_service.get_many_translation_jobs(get_many_schema)
