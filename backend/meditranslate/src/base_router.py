from fastapi import APIRouter
from meditranslate.src.common.common_router import common_router
from meditranslate.src.users.user_router import user_router
from meditranslate.src.auth.auth_router import auth_router
from meditranslate.src.translation_jobs.translation_job_router import translation_job_router
from meditranslate.src.translations.translation_router import translation_router
from meditranslate.src.files.file_router import file_router
from meditranslate.src.webhooks.webhook_router import webhook_router


base_router = APIRouter()


base_router.include_router(
    router=webhook_router,
    prefix="/webhooks",
    tags=["webhooks"]
)
base_router.include_router(
    router=common_router,
    prefix="",
)

base_router.include_router(
    router=user_router,
    prefix="/users"
)
base_router.include_router(
    router=auth_router,
    prefix="/auth"
)

base_router.include_router(
    router=translation_job_router,
    prefix="/jobs"
)

base_router.include_router(
    router=translation_router,
    prefix="/translations"
)

base_router.include_router(
    router=file_router,
    prefix="/files"
)



