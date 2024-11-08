from typing import Any,Dict,List,Optional,Tuple
from meditranslate.src.translation_jobs.translation_job_repository import TranslationJobRepository
from meditranslate.app.db.models import TranslationJob,User
from meditranslate.app.shared.base_service import BaseService
from meditranslate.utils.security.password import hash_password
from meditranslate.app.errors import AppError,ErrorSeverity,ErrorType,HTTPStatus
from meditranslate.src.translation_jobs.translation_job_schemas import (
    TranslationJobCreateSchema,
    TranslationJobUpdateSchema,
    GetManySchema
)
from datetime import datetime

class TranslationJobService(BaseService[TranslationJob]):
    def __init__(self, translation_job_repository: TranslationJobRepository):
        super().__init__(model=TranslationJob, repository=translation_job_repository)
        self.translation_job_repository = translation_job_repository


    async def create_translation_job(self,current_user:User,translation_job_create_schema:TranslationJobCreateSchema) -> TranslationJob:
        translation_job_create_schema.created_by = current_user.id
        new_translation_job_data = translation_job_create_schema.model_dump()
        new_translation_job = await self.translation_job_repository.create(new_translation_job_data)
        return new_translation_job

    async def get_translation_job(self,translation_job_id: str) -> TranslationJob:
        translation_job = await self.translation_job_repository.get_by(field="id",value=translation_job_id,joins=None,unique=True)
        if not translation_job:
            raise AppError(
                title="get translation job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        return translation_job

    async def update_translation_job(self,current_user:User,translation_job_id: str, update_translation_job_data: TranslationJobUpdateSchema) -> None:
        update_translation_job_data.updated_by = current_user.id
        update_translation_job_data = update_translation_job_data.model_dump()
        update_translation_job_data.pop("id",None)
        translation_job = await self.translation_job_repository.get_by("id",translation_job_id,unique=True)
        if not translation_job:
            raise AppError(
                title="update translation job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        return await self.translation_job_repository.update(translation_job,update_translation_job_data)


    async def delete_translation_job(self,current_user:User,translation_job_id: str) -> None:
        translation_job = await self.translation_job_repository.get_by("id",translation_job_id,unique=True)
        if not translation_job:
            raise AppError(
                title="delete translation job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )

        # if translation_job.deleted_at is None:
        #     return await self.translation_job_repository.update(translation_job, {"deleted_at":datetime.now(), "deleted_by":current_user.id})
        # else:
        #     return await self.translation_job_repository.delete(translation_job)

        return await self.translation_job_repository.delete(translation_job)



    async def get_many_translation_jobs(self,get_many_schema: GetManySchema) -> Tuple[List[TranslationJob],int]:
        translation_jobs,total = await self.translation_job_repository.get_many(**get_many_schema.model_dump())
        return translation_jobs,total
