from typing import Any, List,Tuple
from meditranslate.app.shared.base_controller import BaseController
from meditranslate.src.files.file_service import FileService
from meditranslate.src.files.file_schemas import (
    FileCreateSchema,
    GetManySchema
)
from meditranslate.app.db.models import File
from meditranslate.app.db.transaction import Transactional,Propagation


class FileController(BaseController[File]):
    def __init__(self, file_service:FileService) -> None:
        super().__init__(File,file_service)
        self.file_service:FileService = file_service

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def create_file(self,file_create_schema:FileCreateSchema) -> File:
        return await self.file_service.create_file(file_create_schema)

    async def get_file(self,file_id: str) -> File:
        return await self.file_service.get_file(file_id)

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def delete_file(self,file_id: str):
        return await self.file_service.delete_file(file_id)

    async def get_many_files(self,files_get_many_schema:GetManySchema) -> Tuple[List[File],int]:
        return await self.file_service.get_many_files(files_get_many_schema)
