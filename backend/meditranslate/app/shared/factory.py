from fastapi import Depends
from meditranslate.src.users.user_repository import  UserRepository
from meditranslate.src.users.user_service import  UserService
from meditranslate.src.auth.auth_service import AuthService
from meditranslate.src.auth.auth_controller import AuthController
from meditranslate.src.files.file_controller import FileController
from meditranslate.src.files.file_service import FileService
from meditranslate.src.files.file_repository import FileRepository
from meditranslate.src.translations.translation_controller import TranslationController
from meditranslate.src.translations.translation_service import TranslationService
from meditranslate.src.translations.translation_repository import TranslationRepository
from meditranslate.src.webhooks.webhook_repository import WebhookRepository
from meditranslate.src.webhooks.webhook_service import WebhookService
from meditranslate.src.webhooks.webhook_controller import WebhookController
from meditranslate.src.translation_jobs.translation_job_controller import TranslationJobController
from meditranslate.src.requests.requests_controller import RequestsController
from meditranslate.src.translation_jobs.translation_job_service import TranslationJobService
from meditranslate.src.requests.requests_service import RequestsService
from meditranslate.src.translation_jobs.translation_job_repository import TranslationJobRepository
from meditranslate.src.requests.requests_repository import RequestRepository
from meditranslate.app.storage import file_storage_service
from meditranslate.translation import translation_engine
from meditranslate.src.users.user_controller import UserController
from meditranslate.app.db import get_session

class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """


    @staticmethod
    def get_webhook_controller(db_session=Depends(get_session)) -> WebhookController:
        return WebhookController(
            WebhookService(WebhookRepository(db_session), TranslationJobRepository(db_session)))
    
    @staticmethod
    def get_user_controller(db_session=Depends(get_session)) -> UserController:
        return UserController(UserService(UserRepository(db_session)))

    @staticmethod
    def get_auth_controller(db_session=Depends(get_session)) -> AuthController:
        return AuthController(AuthService(UserRepository(db_session)))

    @staticmethod
    def get_file_controller(db_session=Depends(get_session)) -> FileController:
        return FileController(FileService(FileRepository(db_session),file_storage_service))

    @staticmethod
    def get_translation_job_controller(db_session=Depends(get_session)) -> TranslationJobController:
        return TranslationJobController(TranslationJobService(TranslationJobRepository(db_session)))
    
    @staticmethod
    def get_requests_controller(db_session=Depends(get_session)) -> RequestsController:
        return RequestsController(RequestsService(RequestRepository(db_session),TranslationJobRepository(db_session)))

    @staticmethod
    def get_translation_controller(db_session=Depends(get_session)) -> TranslationController:
        return TranslationController(
            TranslationService(TranslationRepository(db_session=db_session),translation_engine),
            FileService(FileRepository(db_session=db_session),storage_service=file_storage_service),
            TranslationJobService(TranslationJobRepository(db_session=db_session)),
            WebhookService(WebhookRepository(db_session), TranslationJobRepository(db_session))
        )









