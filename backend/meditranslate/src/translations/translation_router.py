from fastapi import APIRouter,Request,Query,Body
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

translation_router = APIRouter(
    tags=["translations"],
)

@translation_router.post(
    path="",
    response_model=TranslationResponseSchema,
    status_code=201,
    dependencies=[

    ],
)
async def create_translation(
    translation_create_schema: Annotated[TranslationCreateSchema,Body()],
    translation_controller: TranslationController = Depends(Factory.get_translation_controller)
)-> TranslationResponseSchema:
    """
    Create a new translation.
    """
    translation = await translation_controller.create_translation(translation_create_schema)
    return TranslationResponseSchema(
        data=translation,
        status_code=201,
    )

@translation_router.post(
    path="/text",
    response_model=TranslationResponseSchema,
    status_code=201,
    dependencies=[

    ],
)
async def translation_text(
    translation_create_schema: Annotated[TranslationTextSchema,Body()],
    translation_controller: TranslationController = Depends(Factory.get_translation_controller)
)-> TranslationResponseSchema:
    """
    Create a new translation.
    """
    translation = await translation_controller.translate_text(translation_create_schema)
    return TranslationResponseSchema(
        data=translation,
        status_code=201,
    )


@translation_router.post(
    path="/file/{file_id}",
    response_model=TranslationResponseSchema,
    status_code=201,
    dependencies=[

    ],
)
async def translation_file(
    file_id:str,
    translation_create_schema: Annotated[TranslationFileSchema,Body()],
    translation_controller: TranslationController = Depends(Factory.get_translation_controller)
)-> TranslationResponseSchema:
    """
    Create a new translation.
    """
    translation = await translation_controller.translate_file(translation_create_schema)
    return TranslationResponseSchema(
        data=translation,
        status_code=201,
    )



