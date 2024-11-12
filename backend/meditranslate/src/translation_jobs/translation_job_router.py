from fastapi import APIRouter
from fastapi import APIRouter,Request,Query,Body

from meditranslate.app.dependancies.auth import AuthenticationRequired
from meditranslate.app.dependancies.user import CurrentUserDep
from meditranslate.app.shared.factory import Factory
from meditranslate.app.shared.schemas import PaginationSchema,MetaSchema

from typing import Any,List,Annotated,Optional
from meditranslate.src.translation_jobs.translation_job_schemas import (
    TranslationJobCreateSchema,
    TranslationJobUpdateSchema,
    TranslationJobResponseSchema,
    TranslationJobsResponseSchema,
    GetManySchema,
)
from fastapi.responses import JSONResponse
import json
from meditranslate.app.loggers import logger

from fastapi import Depends
from meditranslate.src.translation_jobs.translation_job_controller import TranslationJobController


translation_job_router = APIRouter(
    tags=["translation jobs"],
    dependencies=[Depends(AuthenticationRequired)]
)



@translation_job_router.post(
    path="",
    response_model=TranslationJobResponseSchema,
    status_code=201,
)
async def create_translation_job(
    current_user: CurrentUserDep,
    translation_job_create_schema: Annotated[TranslationJobCreateSchema,Body(example={
            "title": "exampletitle",
            "description": "example description",
            "source_language":"hebrew",
            "target_language": "english"
        })],
    translation_job_controller: TranslationJobController = Depends(Factory.get_translation_job_controller)
)-> TranslationJobResponseSchema:
    """
    Create a new translation_job.
    """
    translation_job = await translation_job_controller.create_translation_job(current_user,translation_job_create_schema)
    logger.debug(translation_job)
    return TranslationJobResponseSchema(
        data=translation_job,
        status_code=201,
    )


@translation_job_router.get(
    "/{translation_job_id}",
    response_model=TranslationJobResponseSchema,
    status_code=200
)
async def get_translation_job(
    translation_job_id: str,
    translation_job_controller: TranslationJobController = Depends(Factory.get_translation_job_controller)
)-> Any:
    """
    Retrieve a translation_job by their ID.
    """
    translation_job = await translation_job_controller.get_translation_job(translation_job_id)
    return TranslationJobResponseSchema(
        data=translation_job,
        status_code=200,
    )


@translation_job_router.put(
    "/{translation_job_id}",
    response_model=TranslationJobResponseSchema,
    status_code=200
)
async def update_translation_job(
    current_user: CurrentUserDep,
    translation_job_id: str,
    translation_job_update_schema: Annotated[TranslationJobUpdateSchema,Body()],
    translation_job_controller: TranslationJobController = Depends(Factory.get_translation_job_controller)
)-> Any:
    """
    Update a translation_job's information.
    """
    await translation_job_controller.update_translation_job(current_user,translation_job_id, translation_job_update_schema)
    updated_translation_job = await translation_job_controller.get_translation_job(translation_job_id)
    logger.error(updated_translation_job)
    return TranslationJobResponseSchema(
        data=updated_translation_job,
        status_code=200,
    )


@translation_job_router.delete(
    "/{translation_job_id}",
    status_code=200,
)
async def delete_translation_job(
    current_user: CurrentUserDep,
    translation_job_id: str,
    translation_job_controller: TranslationJobController = Depends(Factory.get_translation_job_controller)
)-> Any:
    """
    Delete a translation_job by their ID.
    """
    await translation_job_controller.delete_translation_job(current_user,translation_job_id)



@translation_job_router.get(
    "",
    response_model=TranslationJobsResponseSchema,
    status_code=200,
)
async def get_many_translation_jobs(
    get_many_schema:Annotated[GetManySchema, Query()],
    translation_job_controller: TranslationJobController = Depends(Factory.get_translation_job_controller)
)-> Any:
    """
    Retrieve a list of translation_jobs with pagination.
    """
    translation_jobs,total = await translation_job_controller.get_many_translation_jobs(get_many_schema)
    pagination = PaginationSchema(
        total=total,
        page=0,
        page_size=len(translation_jobs)
    )
    if get_many_schema:
        schema = get_many_schema.model_dump()
        if schema.get("limit",None) is not None and schema.get("offset",None) is not None:
            page_size = get_many_schema.limit
            page = (get_many_schema.offset // get_many_schema.limit) + 1
            pagination = PaginationSchema(
                total=total,
                page=page,
                page_size=page_size
            )

    meta = MetaSchema(
        pagination=pagination
    )
    logger.debug(f"Retrieved translation_jobs: {translation_jobs}, total: {total}")

    return TranslationJobsResponseSchema(
        data=translation_jobs,
        status_code=200,
        meta=meta.model_dump(),
        message="translation_jobs retrieved successfully"
    )


