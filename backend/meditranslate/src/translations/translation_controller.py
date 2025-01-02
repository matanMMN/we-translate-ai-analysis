from typing import Any, List,Tuple

from meditranslate.utils.files.file_status import FileStatus
from fastapi import UploadFile, BackgroundTasks
from meditranslate.app.shared.base_controller import BaseController
from meditranslate.src.files.file_service import FileService
from meditranslate.src.translation_jobs.translation_job_schemas import TranslationJobUpdateSchema
from meditranslate.src.translation_jobs.translation_job_service import TranslationJobService
from meditranslate.src.translations.translation_service import TranslationService
from celery.result import AsyncResult
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
from meditranslate.src.webhooks.webhook_service import WebhookService


class TranslationController(BaseController[Translation]):
    def __init__(
            self,
            translation_service: TranslationService,
            file_service: FileService,
            translation_job_service: TranslationJobService,
            webhook_service: WebhookService) -> None:
        super().__init__(Translation,translation_service)
        self.translation_service: TranslationService = translation_service
        self.file_service: FileService = file_service
        self.translation_job_service: TranslationJobService = translation_job_service
        self.webhook_service: WebhookService = webhook_service

    async def _wait_for_reference_file(self, file_id: str, task_id: str):
        """
        Wait for reference file processing task to complete using Celery's result backend
        """
        task_result = AsyncResult(task_id)
        print("INITIAL TASK STATUS:", task_result.status)
        print("TASK ID", task_id)
        print("FILE ID", file_id)
        
        try:
            wait_result = task_result.wait(timeout=None)

            print("WAIT RESULT:", wait_result)
            print("TASK STATUS AFTER WAIT:", task_result.status)
            print("TASK READY:", task_result.ready())
            print("TASK SUCCESSFUL:", task_result.successful())
            
            if task_result.ready() and task_result.successful():
                file = await self.file_service.file_repository.get_by("id", file_id, unique=True)
                await self.file_service.file_repository.session.refresh(file)
                print("FILE", file)
                return await self.file_service.fetch_file_entity(file_id)
            else:
                logger.error(f"Reference file {file_id} processing failed: {task_result.result}")
                return None

                
        except Exception as e:
            print("ERROR WAITING FOR REFERENCE FILE", e)
            logger.error(f"Error waiting for reference file {file_id} task {task_id}: {str(e)}")
            return None
        finally:
            print("FORGETTING TASK RESULT")
            task_result.forget()


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
    async def translate_file(self,current_user:User,file_id:str,translation_file_schema:TranslationFileSchema, background_tasks: BackgroundTasks):
        src_file = await self.file_service.fetch_file_entity(file_id=file_id)
        src_file_stream, _ ,_ = await self.file_service.download_file_sync(file_id=file_id)

        translation_job = await self.translation_job_service.get_translation_job(
            translation_file_schema.translation_job_id, to_public=False)
        ref_file = await self.file_service.fetch_file_entity(translation_job.reference_file_id)
        print("REF FILE", ref_file)
        if FileStatus(ref_file.status) == FileStatus.PROCESSING:
            print("WAITING FOR REFERENCE FILE")
            ref_file = await self._wait_for_reference_file(file_id=translation_job.reference_file_id, task_id=ref_file.processing_task_id)
        
        ref_file_stream, _, _ = await self.file_service.download_file_sync(file_id=ref_file.id)

        translated_file_stream, new_file_name, content_type, complete = await self.translation_service.translate_file(
            current_user,
            src_file,
            src_file_stream,
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

        result_file = await self.file_service.upload_file(current_user,upload_file, background_tasks)

        await self.translation_job_service.update_translation_job(
            current_user=current_user,
            translation_job_id=translation_job.id,
            update_translation_job_data=TranslationJobUpdateSchema(
                target_file_id=result_file.get("id"),
                is_translating=False
            )
        )

        await self.webhook_service.notify_translation_complete(
            translation_job.id,
            {
                    "event_type": "file_translation_complete",
                    "file_id": result_file.get("id"),
                    "file_name": new_file_name,
                    "content_type": content_type
            }
        )

        return result_file, complete

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def translate_text(self,current_user: User, translation_text_schema: TranslationTextSchema):
        translation_job = await self.translation_job_service.get_translation_job(
            translation_text_schema.translation_job_id, to_public=False)
        ref_file = await self.file_service.fetch_file_entity(translation_job.reference_file_id)
        ref_file_stream, _, _ = await self.file_service.download_file_sync(file_id=ref_file.id)

        translation_result = await self.translation_service.translate_text(
            current_user,
            ref_file_stream,
            translation_text_schema
        )
        await self.webhook_service.notify_translation_complete(
            translation_job.id,
            {
                "event_type": "text_translation_complete",
                "translation_job_id": translation_job.id,
                "translation_result": translation_result,
                "is_complete": True   
            }
        )

        return translation_result
