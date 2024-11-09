from typing import Any,Dict,List,Optional,Tuple
from meditranslate.app.storage.base_storage_service import BaseStorageService
from meditranslate.src.files.file_repository import FileRepository
from meditranslate.app.db.models import File
from meditranslate.app.shared.base_service import BaseService
from meditranslate.src.users.user import User
from meditranslate.utils.files.file_format_type import FileFormatType
from meditranslate.utils.files.file_size_unit import FileSizeUnit
from meditranslate.utils.security.password import hash_password
from meditranslate.app.errors import AppError,ErrorSeverity,ErrorType,HTTPStatus
from meditranslate.src.files.file_schemas import (
    FileCreateSchema,
    GetManySchema
)
from tempfile import SpooledTemporaryFile
from fastapi import UploadFile
from meditranslate.app.loggers import logger
from uuid import uuid4
from meditranslate.app.configurations import config

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
        file_stream = self.storage_service.download_file(file_path=file.file_path)
        content_preview = file_stream.read(100)
        logger.debug(f"""\n
            File Name: {file.original_file_name}
            File preview Type": {content_preview}
        """)
        return file_stream, file.original_file_name

    async def upload_file(self,file:UploadFile,user:User) -> File:
        file_data= await file.read()
        original_file_name = file.filename
        content_type = file.content_type
        extension = FileFormatType.TXT
        split = original_file_name.rsplit('.', 1)  # Split on the last dot only
        file_path = f"{original_file_name}{str(uuid4())}"

        logger.debug(f"""\n
            File Name: {original_file_name}
            File Content Type": {content_type}
            File Content:\n {file_data}
""")

        if len(split) == 2:
            extension_string = split[1].strip().lower()
            try:
                extension = FileFormatType(extension_string)
            except ValueError as e:
                raise AppError(
                    error=e,
                    title="wrong file format type",
                    error_class=AppError,
                    user_message=f"server does not accept files with {extension_string} extension",
                    http_status=HTTPStatus.BAD_REQUEST
                ) from e

        if extension not in config.ALLOWED_UPLOAD_FILE_EXTENSIONS:
            raise AppError(
                error=e,
                title="invalid file upload type",
                error_class=AppError,
                user_message=f"{extension.value} files  are not allowed",
                http_status=HTTPStatus.BAD_REQUEST
            ) from e

        try:
            self.storage_service.upload_file(file=file,file_path=file_path)
            storage_file_path = self.storage_service.create_file_path(file_path)
            self.storage_service.get_file(file_path=file_path)
            self.storage_service.get_file(file_path=storage_file_path)
        except Exception as e:
            raise AppError(
                error=e,
                title="upload file exception",
                error_class=AppError,
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR
            ) from e

        file_create_schema = FileCreateSchema(
            file_path = file_path,
            file_url = self.storage_service.base_url,
            file_storage_provider = self.storage_service.storage_provider.value,
            file_metadata = None,
            original_file_name = original_file_name,
            file_name = file.filename,
            file_format_type = extension,
            file_size = len(file_data),
            uploaded_by = user.id,
            file_size_unit="bytes"
        )
        file_pointer = await self.create_file(file_create_schema)
        public_file_pointer = self._to_public_file_pointer(file=file_pointer)
        return public_file_pointer

    async def create_file(self,file_create_schema: FileCreateSchema) -> File:
        new_file_data = file_create_schema.model_dump()
        new_file = await self.file_repository.create(new_file_data)
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
        is_deleted = self.storage_service.delete_file(file.file_path)
        if is_deleted:
            is_pointer_deleted = await self.file_repository.delete(file)
        return is_pointer_deleted

    async def get_many_files(self,files_get_many_schema: GetManySchema) -> Tuple[List[File],int]:
        files,total = await self.file_repository.get_many(**files_get_many_schema.model_dump())
        public_files = [self._to_public_file_pointer(file) for file in files]
        return public_files,total
