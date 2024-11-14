from io import BytesIO
from typing import Any,Dict,List,Optional,Tuple
from meditranslate.app.storage.base_storage_service import BaseStorageService
from meditranslate.src.files.file_repository import FileRepository
from meditranslate.app.db.models import File
from meditranslate.app.shared.base_service import BaseService
from meditranslate.src.users.user import User
from meditranslate.utils.files.file_format_type import FileFormatType
from meditranslate.utils.files.file_size_unit import FileSizeUnit
from meditranslate.utils.files.formats.file_format_handler import FileFormatHandler
from meditranslate.utils.language.utils import get_language_from_text
from meditranslate.utils.security.password import hash_password
from meditranslate.app.errors import AppError,ErrorSeverity,ErrorType,HTTPStatus
from meditranslate.src.files.file_schemas import (
    FilePointerCreateSchema,
    FilePointerUpdateSchema,
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
        # if file.upload_by is not None:
        #     public_file["upload_by_user"] = file.upload_by_user.full_name
        if file.original_file_name is not None:
            public_file['file_name'] = file.original_file_name
        return public_file

    async def update_file(self,current_user:User,file_id:str, file:UploadFile):
        file_pointer = await self.file_repository.get_by("id",file_id,unique=True)
        if not file_pointer:
            raise AppError(
                title="get update job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        is_deleted = self.storage_service.delete_file(file_pointer.file_path)
        new_file_name,original_file_name,storage_file_path,file_language,file_size,extension = await self.upload_file_to_storage(file=file)
        file_update_schema = FilePointerUpdateSchema(
            file_path = storage_file_path,
            file_url = self.storage_service.base_url,
            file_storage_provider = self.storage_service.storage_provider.value,
            file_metadata = None,
            original_file_name = original_file_name,
            file_name = new_file_name,
            file_format_type = extension.value,
            file_size = file_size,
            upload_by = current_user.id,
            file_language=file_language,
            # updated_by=current_user.id
        )
        await self.update_file_pointer(file_id,file_update_schema)

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

    async def download_file_sync(self,file_id:str) -> BytesIO:
        file = await self.file_repository.get_by("id",file_id,unique=True)
        if not file:
            raise AppError(
                title="get download_file job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        file_io = self.storage_service.download_file_sync(file_path=file.file_path)
        return file_io, file.original_file_name


    def _is_valid_input_file(self,file_content:str):
        return True

    async def upload_file_to_storage(self, file:UploadFile):
        original_file_name = file.filename
        new_file_name = f"{original_file_name}{str(uuid4())}"
        try:
            extension = FileFormatType.TXT
            file_extension_str = original_file_name.rsplit('.', 1)
            if len(file_extension_str) == 2:
                extension_string = file_extension_str[1].strip().lower()
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
                title="invalid file upload type",
                error_class=AppError,
                user_message=f"{extension.value} files  are not allowed",
                http_status=HTTPStatus.BAD_REQUEST
            )

        # content_type = FileFormatHandler().get_content_type(extension)
        # if file.content_type != content_type:
        #     raise AppError(
        #         title="invalid content type",
        #         error_class=AppError,
        #         user_message=f"invalid content type recv:{file.content_type} expected: {content_type} for file type {extension.value}",
        #         http_status=HTTPStatus.BAD_REQUEST
        #     )

        file_data = await file.read()
        file_stream = BytesIO(file_data)
        file_stream.seek(0)
        file_content = FileFormatHandler().extract_text(extension,file_stream)
        file_language = get_language_from_text(file_content)
        if file_language is None or not self._is_valid_input_file(file_content):
            raise AppError(
                title="invalid file",
                user_message="invalid user input file content",
                http_status=HTTPStatus.NOT_ACCEPTABLE
            )

        try:
            storage_file_path = self.storage_service.create_file_path(new_file_name)
            self.storage_service.upload_file(file=file,file_path=storage_file_path)
            logger.debug(self.storage_service.get_file(file_path=storage_file_path))
            return new_file_name,original_file_name,storage_file_path,file_language,len(file_data),extension
        except Exception as e:
            raise AppError(
                error=e,
                title="upload file exception",
                error_class=AppError,
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR
            ) from e

    async def upload_file(self,current_user:User,file:UploadFile) -> File:
        new_file_name,original_file_name,storage_file_path,file_language,file_size,extension = await self.upload_file_to_storage(file=file)
        file_create_schema = FilePointerCreateSchema(
            file_path = storage_file_path,
            file_url = self.storage_service.base_url,
            file_storage_provider = self.storage_service.storage_provider.value,
            file_metadata = None,
            original_file_name = original_file_name,
            file_name = new_file_name,
            file_format_type = extension.value,
            file_size = file_size,
            upload_by = current_user.id,
            file_language=file_language
        )
        file_pointer = await self.create_file_pointer(file_create_schema)
        public_file_pointer = self._to_public_file_pointer(file=file_pointer)
        return public_file_pointer


    async def create_file_pointer(self,file_create_schema: FilePointerCreateSchema) -> File:
        new_file_data = file_create_schema.model_dump()
        new_file = await self.file_repository.create(new_file_data)
        return new_file

    async def update_file_pointer(self,file_id:str, file_update_schema: FilePointerUpdateSchema) -> File:
        file = await self.file_repository.get_by("id",file_id,unique=True)
        if not file:
            raise AppError(
                title="get translation job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )

        update_file_data = file_update_schema.model_dump()
        await self.file_repository.update(file,update_file_data)

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
