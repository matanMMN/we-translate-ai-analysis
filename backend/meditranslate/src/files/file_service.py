from typing import Any,Dict,List,Optional,Tuple
from meditranslate.app.storage.base_storage_service import BaseStorageService
from meditranslate.src.files.file_repository import FileRepository
from meditranslate.app.db.models import File
from meditranslate.app.shared.base_service import BaseService
from meditranslate.utils.security.password import hash_password
from meditranslate.app.errors import AppError,ErrorSeverity,ErrorType,HTTPStatus
from meditranslate.src.files.file_schemas import (
    FileCreateSchema,
    GetManySchema
)

class FileService(BaseService[File]):
    def __init__(self, file_repository: FileRepository,storage_service:BaseStorageService):
        super().__init__(model=File, repository=file_repository)
        self.file_repository = file_repository
        self.storage_service = storage_service

    async def download_file(self):
        pass

    async def upload_file(self):
        pass

    async def create_file(self,file_create_schema: FileCreateSchema) -> File:
        new_file_data = file_create_schema.model_dump()
        new_file = await self.file_repository.create(**new_file_data)
        return new_file

    async def get_file(self,file_id: str) -> Optional[File]:
        file = await self.file_repository.get_by("id",file_id,unique=True)
        if not file:
            raise AppError(
                title="get translation job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        return file

    async def delete_file(self,file_id: str):
        file = await self.file_repository.get_by("id",file_id,unique=True)
        if not file:
            raise AppError(
                title="delete user endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        is_deleted = await self.file_repository.delete(file)
        return is_deleted

    async def get_many_files(self,files_get_many_schema: GetManySchema) -> Tuple[List[File],int]:
        files,total = await self.file_repository.get_many(**files_get_many_schema.model_dump())
        return files,total
