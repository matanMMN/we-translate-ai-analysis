from fastapi import APIRouter,Request,Query,Body
from meditranslate.app.dependancies.auth import AuthenticationRequired
from meditranslate.app.dependancies.user import CurrentUserDep
from meditranslate.app.shared.factory import Factory
from typing import Any,List,Annotated,Optional
from meditranslate.src.translations.translation_schemas import (
    TranslationCreateSchema,
    TranslationResponseSchema,
    TranslationFileSchema,
    TranslationTextSchema
)
from fastapi.responses import JSONResponse
import json
from meditranslate.app.loggers import logger

from fastapi import Depends
from meditranslate.src.translations.translation_controller import TranslationController
from meditranslate.src.users.user import User
from meditranslate.app.worker.tasks.translate_file import translation_file_task

translation_router = APIRouter(
    tags=["translations"],
    dependencies=[Depends(AuthenticationRequired)]
)

# @translation_router.post(
#     path="",
#     response_model=TranslationResponseSchema,
#     status_code=201
# )
# async def create_translation(
#     current_user: CurrentUserDep,
#     translation_create_schema: Annotated[TranslationCreateSchema,Body(example={
#             "input_text": "input text example",
#             "source_language":"hebrew",
#             "target_language": "english"
#         })],
#     translation_controller: TranslationController = Depends(Factory.get_translation_controller)
# )-> TranslationResponseSchema:
#     """
#     Create a new translation.
#     """
#     translation = await translation_controller.create_translation(current_user,translation_create_schema)
#     return TranslationResponseSchema(
#         data=translation,
#         status_code=201,
#     )

@translation_router.post(
    path="/text",
    response_model=TranslationResponseSchema,
    status_code=200
)
async def translation_text(
    current_user: CurrentUserDep,
    translation_text_schema: Annotated[TranslationTextSchema,Body()],
    translation_controller: TranslationController = Depends(Factory.get_translation_controller)
)-> TranslationResponseSchema:
    """
    Create a new translation.
    """
    translation = await translation_controller.translate_text(current_user,translation_text_schema)
    return TranslationResponseSchema(
        data=translation,
        status_code=201,
    )


@translation_router.post(
    path="/file/{file_id}",
    status_code=200
)
async def translation_file(
    current_user: CurrentUserDep,
    file_id:str,
    translation_file_schema: Annotated[TranslationFileSchema,Body()],
    translation_controller: TranslationController = Depends(Factory.get_translation_controller)
):
    """
    Create a new translation.
    """
    await translation_controller.translate_file(current_user,file_id,translation_file_schema)


@translation_router.post(
    path="/file/{file_id}/",
    status_code=200
)
async def translation_file_with_worker(
    current_user: CurrentUserDep,
    file_id:str,
    translation_file_schema: Annotated[TranslationFileSchema,Body()],
    translation_controller: TranslationController = Depends(Factory.get_translation_controller)
):
    """
    Create a new translation.
    """
    translation_file_task(current_user,file_id,translation_file_schema,translation_controller)
