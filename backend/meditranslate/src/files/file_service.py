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
from tempfile import SpooledTemporaryFile
from fastapi import UploadFile
class FileService(BaseService[File]):
    def __init__(self, file_repository: FileRepository,storage_service:BaseStorageService):
        super().__init__(model=File, repository=file_repository)
        self.file_repository = file_repository
        self.storage_service = storage_service

    def _to_public_file_pointer(self,file:File):
        public_file = file.as_dict()
        public_file.pop("file_path")
        public_file.pop("file_url")
        public_file.pop("file_storage_provider")
        public_file.pop("file_metadata")
        public_file['name'] = file.original_file_name
        return public_file

    async def download_file(self,file_id:str):
        file = await self.file_repository.get_by("id",file_id,unique=True)
        if not file:
            raise AppError(
                title="get download_file job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        res = await self.storage_service.download_file(file_id=file.file_id)

    async def upload_file(self,file:UploadFile,file_create_schema:FileCreateSchema) -> File:
        # https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile
        file.filename
        file.content_type
        f:SpooledTemporaryFile = file.file
        file_data= await file.read(
        self.storage_service.upload_file(file_data=file_data,filename=file.filename))
        await self.create_file()

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
        public_file = self._to_public_file_pointer(file)
        return public_file

    async def delete_file(self,file_id: str):
        file = await self.file_repository.get_by("id",file_id,unique=True)
        if not file:
            raise AppError(
                title="delete user endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        res = await self.storage_service.delete_file(file.file_id)
        # TODO
        is_deleted = await self.file_repository.delete(file)
        return is_deleted

    async def get_many_files(self,files_get_many_schema: GetManySchema) -> Tuple[List[File],int]:
        files,total = await self.file_repository.get_many(**files_get_many_schema.model_dump())
        public_files = [self._to_public_file_pointer(file) for file in files]
        return public_files,total
