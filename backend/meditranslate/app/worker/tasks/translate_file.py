from meditranslate.app.db.decorator import standalone_session
from meditranslate.app.worker.worker import celery
from meditranslate.src.translations.translation_controller import TranslationController
from meditranslate.src.translations.translation_schemas import TranslationFileSchema
from meditranslate.app.db import User
from meditranslate.utils.files.formats.file_format_handler import FileFormatHandler
import asyncio

@celery.task(name="translate_file")
def translation_file_task(
    current_user: User,
    file_id:str,
    translation_file_schema: TranslationFileSchema,
    translation_controller: TranslationController
):
    """
    Create a new translation.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        translation_controller.translate_file(current_user,file_id,translation_file_schema)
    )
