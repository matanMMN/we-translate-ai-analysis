from typing import Any, Generic, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel

from meditranslate.app.db import Base, Propagation, Transactional
from meditranslate.app.db.base_repository import BaseRepository
from meditranslate.app.errors import AppError, ErrorSeverity, HTTPStatus, ErrorType
from meditranslate.app.shared.base_service import BaseService

ModelType = TypeVar("ModelType", bound=Base)


class BaseController(Generic[ModelType]):
    """Base class for data controller."""

    def __init__(self, model: Type[ModelType], service: BaseService):
        self.model_class = model
        self.service = service

