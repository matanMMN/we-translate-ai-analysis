from io import BytesIO
import io

from meditranslate.src.files.file_version_schemas import FileVersionCreateSchema, FileVersionResponseSchema
from typing import Any,Dict,List,Tuple
from meditranslate.app.db.transaction import Propagation, Transactional
from meditranslate.utils.files.file_status import FileStatus
from meditranslate.app.storage.base_storage_service import BaseStorageService
from meditranslate.src.files.file_repository import FileRepository
from meditranslate.app.db.models import File
from meditranslate.app.shared.base_service import BaseService
from meditranslate.src.users.user import User
from meditranslate.utils.files.file_format_type import FileFormatType
from meditranslate.utils.files.formats.file_format_handler import FileFormatHandler
from meditranslate.utils.language.utils import get_language_from_text
from meditranslate.app.errors import AppError,HTTPStatus
from meditranslate.utils.files.formats.pdf_to_docx import pdf_to_docx_bytes
from sqlalchemy import event
from meditranslate.src.files.file_schemas import (
    FilePointerCreateSchema,
    FilePointerUpdateSchema,
    GetManySchema
)
from fastapi import UploadFile, BackgroundTasks
from meditranslate.app.loggers import logger
from uuid import uuid4
from meditranslate.app.configurations import config

class FileService(BaseService[File]):

    _listener_registered = False

    def __init__(self, file_repository: FileRepository,storage_service:BaseStorageService):
        super().__init__(model=File, repository=file_repository)
        self.file_repository = file_repository
        self.storage_service = storage_service
        if not FileService._listener_registered:
            event.listen(File, 'after_delete', self._delete_file_from_storage)
            FileService._listener_registered = True


    def _delete_file_from_storage(self, mapper, connection, target):
        """Event listener to delete file from storage when database record is deleted"""
        import asyncio
        
        async def delete_storage():
            try:
                file_name = target.file_path.split(f".v{target.current_version}", 1)
                base, ext = file_name
                print("file_name ",file_name)
                if target.file_path:
                    self.storage_service.delete_file(target.file_path)
                
                    if getattr(target, 'current_version', 0) > 1:
                        for version in range(1, target.current_version):
                            try:
                                versioned_path = f"{base}.v{version}{ext}"
                                self.storage_service.delete_file(versioned_path)
                            except Exception as e:
                                logger.warning(f"Failed to delete versioned file {versioned_path}: {str(e)}")
                            
            except Exception as e:
                logger.error(f"Error deleting file from storage: {str(e)}")

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(delete_storage())
        except Exception as e:
            logger.error(f"Error setting up async deletion: {str(e)}")

    def _to_public_file_pointer(self,file:File):
        public_file = file.as_dict()
    
        # if file.upload_by is not None:
        #     public_file["upload_by_user"] = file.upload_by_user.full_name
        if file.original_file_name is not None:
            public_file['file_name'] = file.original_file_name
            public_file['file_name_id'] = file.file_name
        return public_file
    

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_file(self,current_user:User,file_id:str, file:UploadFile):

        file_pointer = await self.file_repository.get_by("id",file_id,unique=True)
        if not file_pointer:
            raise AppError(
                title="get update job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
    

        new_version = file_pointer.current_version + 1
    
        try:
            # versioned_path = await self.storage_service.copy_to_version(
            #     file_pointer.file_path, 
            #     file_pointer.current_version
            # )
            # print("versioned_path ",versioned_path)

            new_file_name, original_file_name, storage_file_path, file_language, file_size, extension, status = await self.upload_file_to_storage(file=file, next_version=new_version)
            # version_data = FileVersionCreateSchema(
            #     file_id=file_id,
            #     version_number=file_pointer.current_version,
            #     file_path=file_pointer.file_path,
            #     # file_path=versioned_path,
            #     file_size=file_pointer.file_size,
            #     file_language=file_pointer.file_language,
            #     file_format_type=file_pointer.file_format_type,
            #     status=file_pointer.status,
            #     created_by=current_user.id
            # )
            # print("version_data ",version_data)
            # await self.file_repository.create_version(version_data)
            print("version_data created")        
            file_update_schema = FilePointerUpdateSchema(
                file_path=storage_file_path,
                file_url=self.storage_service.base_url,
                file_storage_provider=self.storage_service.storage_provider.value,
                file_metadata=None,
                original_file_name=original_file_name,
                file_name=new_file_name,
                file_format_type=extension.value,
                file_size=file_size,
                upload_by=current_user.id,
                file_language=file_language,
                status=status,
                current_version=new_version
            )
            
            await self.update_file_pointer(file_id, file_update_schema)
        # is_deleted = self.storage_service.delete_file(file_pointer.file_path)
        # new_file_name,original_file_name,storage_file_path,file_language,file_size,extension, status = await self.upload_file_to_storage(file=file)
        # file_update_schema = FilePointerUpdateSchema(
        #     file_path = storage_file_path,
        #     file_url = self.storage_service.base_url,
        #     file_storage_provider = self.storage_service.storage_provider.value,
        #     file_metadata = None,
        #     original_file_name = original_file_name,
        #     file_name = new_file_name,
        #     file_format_type = extension.value,
        #     file_size = file_size,
        #     upload_by = current_user.id,
        #     file_language=file_language,
        #     status=status,
        #     # updated_by=current_user.id
        # )
        except Exception as e:
            logger.error(f"Error updating file with versioning: {str(e)}")
            raise AppError(
                title="Error updating file",
                description=str(e),
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        
    async def download_file(self,file_id:str):
        file = await self.file_repository.get_by("id",file_id,unique=True)
        if not file:
            raise AppError(
                title="get download_file job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        file_stream = self.storage_service.download_file(file_path=file.file_path)
        # content_preview = file_stream.read(100)
        logger.debug(f"""\n
            File Name: {file.original_file_name}
            File preview Type": content_preview
        """)
        content_type = FileFormatHandler().get_content_type(FileFormatType(file.file_format_type))
        return file_stream, file.original_file_name,content_type

    async def download_file_sync(self,file_id:str, is_bytes=False) -> Tuple[BytesIO, str, str]:
        file = await self.file_repository.get_by("id",file_id,unique=True)
        if not file:
            raise AppError(
                title="get download_file job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        file_io = self.storage_service.download_file_sync(file_path=file.file_path)
        if is_bytes: file_io = self.storage_service.download_file_sync(file_path=file.file_path).read()
        content_type = FileFormatHandler().get_content_type(FileFormatType(file.file_format_type))
        return file_io, file.original_file_name,content_type


    def _is_valid_input_file(self,file_content:str):
        return True

    async def upload_file_to_storage(self, file:UploadFile, next_version=None):
        original_file_name = file.filename
        file_prefix, extension = original_file_name.rsplit('.', 1)
        if next_version is None:
            new_file_name = f"{file_prefix}-{str(uuid4())}.v1.{extension}"
        else:
            original_file_name = file_prefix.rsplit('.', 1)[0]
            new_file_name = f"{original_file_name}.v{next_version}.{extension}"
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
                user_message=f"{extension.value} files are not allowed",
                http_status=HTTPStatus.BAD_REQUEST
            )
        if extension == FileFormatType.PDF:
            # Store the original PDF file first
            file_data = await file.read()
            storage_file_path = self.storage_service.create_file_path(new_file_name)
            pdf_file = UploadFile(
                filename=original_file_name,
                file=io.BytesIO(file_data)
            )
            self.storage_service.upload_file(file=pdf_file, file_path=storage_file_path)            
            # For PDFs, we'll do basic language detection on the first page
            # try:
            #     from PyPDF2 import PdfReader
            #     from io import BytesIO
                
            #     pdf_stream = BytesIO(file_data)
            #     pdf_reader = PdfReader(pdf_stream)
            #     if len(pdf_reader.pages) > 0:
            #         first_page_text = pdf_reader.pages[0].extract_text()
            #         detected_language = get_language_from_text(first_page_text) or "en"
            #     else:
            #         detected_language = "en"  # Default to English if no text found
                
            #     # Return metadata with detected language
            #     return new_file_name, original_file_name, storage_file_path, detected_language, len(file_data), extension, FileStatus.PROCESSING.value
            # except Exception as e:
            #     logger.warning(f"Failed to detect PDF language: {str(e)}")
            #     # Fallback to English if language detection fails
            #     return new_file_name, original_file_name, storage_file_path, "en", len(file_data), extension, FileStatus.PROCESSING.value
            return new_file_name, original_file_name, storage_file_path, "language", len(file_data), extension, FileStatus.PROCESSING.value


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
            return new_file_name,original_file_name,storage_file_path,file_language,len(file_data),extension, FileStatus.READY.value
        except Exception as e:
            raise AppError(
                error=e,
                title="upload file exception",
                error_class=AppError,
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR
            ) from e
        

    async def restore_version(self, file_id: str, version_number: int, current_user: User):
        """Restore a specific version as the current version"""
        # Get the version to restore
        version = await self.file_repository.get_version(file_id, version_number)
        if not version:
            raise AppError(
                title="Version not found",
                http_status=HTTPStatus.NOT_FOUND
            )

        file_pointer = await self.file_repository.get_by("id", file_id, unique=True)
        if not file_pointer:
            raise AppError(
                title="File not found",
                http_status=HTTPStatus.NOT_FOUND
            )

        # Create a new version of the current state
        current_version_data = FileVersionCreateSchema(
            file_id=file_id,
            version_number=file_pointer.current_version,
            file_path=file_pointer.file_path,
            file_size=file_pointer.file_size,
            file_language=file_pointer.file_language,
            file_format_type=file_pointer.file_format_type,
            status=file_pointer.status,
            created_by=current_user.id
        )
        await self.file_repository.create_version(current_version_data)

        # Update the current file with the restored version's data
        new_version = file_pointer.current_version + 1
        file_update_schema = FilePointerUpdateSchema(
            file_path=version.file_path,
            file_url=self.storage_service.base_url,
            file_storage_provider=self.storage_service.storage_provider.value,
            file_size=version.file_size,
            file_language=version.file_language,
            file_format_type=version.file_format_type,
            status=version.status,
            current_version=new_version
        )
        await self.update_file_pointer(file_id, file_update_schema)
    async def get_file_versions(self, file_id: str) -> List[FileVersionResponseSchema]:
        """Get all versions of a file"""
        versions = await self.file_repository.get_versions(file_id)
        return [
            FileVersionResponseSchema(
                id=v.id,
                version_number=v.version_number,
                created_at=v.created_at,
                created_by=v.created_by,
                file_size=v.file_size,
                file_path=v.file_path,
                file_language=v.file_language,
                file_format_type=v.file_format_type,
                status=v.status.value
            ) for v in versions
        ]

    async def get_specific_version(self, file_id: str, version_number: int):
        """Download a specific version of a file"""
        version = await self.file_repository.get_version(file_id, version_number)
        if not version:
            raise AppError(
                title="Version not found",
                http_status=HTTPStatus.NOT_FOUND
            )
        
        file_stream = self.storage_service.download_file(file_path=version.file_path)
        content_type = FileFormatHandler().get_content_type(FileFormatType(version.file_format_type))
        return file_stream, version.file.original_file_name, content_type
    
    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def process_pdf_file(self, file_id: str, current_user:User):
        """
        Initiate asynchronous PDF processing using Celery.
        The actual processing is handled by the Celery worker.
        """
        from meditranslate.src.files.tasks import process_pdf_file_task

        try:
            
            file_pointer = await self.file_repository.get_by("id",file_id,unique=True)
            if not file_pointer: raise AppError(title="get update job endpoint",http_status=HTTPStatus.NOT_FOUND)
            task = process_pdf_file_task.delay(file_id, str(current_user.id))
            
            await self.update_file_pointer(
                file_id,
                FilePointerUpdateSchema(
                    processing_task_id=task.id,
                    status=FileStatus.PROCESSING.value),
            )
        
        except Exception as e:
            logger.error(f"Failed to initiate PDF processing: {str(e)}")
            await self.update_file_pointer(
                file_id,
                FilePointerUpdateSchema(
                    status=FileStatus.FAILED.value,
                    file_metadata={"error": str(e)}
                )
            )
        #     pdf_bytes, original_filename, _ = await self.download_file_sync(file_id, is_bytes=True)
            
            # docx_bytes = await pdf_to_docx_bytes(pdf_bytes, config.OPENAI_API_KEY)


        #     new_filename = original_filename.rsplit('.', 1)[0]
        #     new_file_name = f"{new_filename}-{str(uuid4())}.v1.docx"

            

        #     self.storage_service.delete_file(file_pointer.file_path)

        #     # Create new UploadFile for DOCX
        #     docx_file = UploadFile(
        #         filename=new_filename,
        #         file=io.BytesIO(docx_bytes)
        #     )
        #     # Store the DOCX file
            

        #     storage_file_path = self.storage_service.create_file_path(new_file_name)
        #     self.storage_service.upload_file(file=docx_file, file_path=storage_file_path)
            

        #     docx_io = io.BytesIO(docx_bytes)
        #     file_content = FileFormatHandler().extract_text(FileFormatType.DOCX, docx_io)
        #     file_language = get_language_from_text(file_content)

        #     if file_language is None or not self._is_valid_input_file(file_content):
        #         raise AppError(
        #         title="invalid file",
        #         user_message="invalid user input file content",
        #         http_status=HTTPStatus.NOT_ACCEPTABLE
        #         )
            
        #     update_schema = FilePointerUpdateSchema(
        #         original_file_name=new_filename,
        #         file_path=storage_file_path,
        #         file_format_type=FileFormatType.DOCX.value,
        #         status=FileStatus.READY.value,
        #         file_name=new_file_name,
        #         file_size=len(docx_bytes),
        #         file_language=file_language,
        #         file_url=self.storage_service.base_url,
        #         file_storage_provider=self.storage_service.storage_provider.value,
        #         upload_by=current_user.id,
        #         current_version=1,
        #         file_metadata=None  # Add if needed
        #     )
            
        #     await self.update_file_pointer(file_id, update_schema)

          

        # except Exception as e:
        #     logger.error(f"PDF processing failed: {str(e)}")
        #     await self.update_file_pointer(
        #         file_id,
        #         FilePointerUpdateSchema(status=FileStatus.FAILED.value,)
        #     )


    async def upload_file(self,current_user:User,file:UploadFile, background_tasks: BackgroundTasks) -> Dict[Any, dict | str | None]:
        new_file_name,original_file_name,storage_file_path,file_language,file_size,extension, status = await self.upload_file_to_storage(file=file)
        
        file_create_schema = FilePointerCreateSchema(
            file_path=storage_file_path,
            file_url=self.storage_service.base_url,
            file_storage_provider=self.storage_service.storage_provider.value,
            file_metadata=None,
            original_file_name=original_file_name,
            file_name=new_file_name,
            file_format_type=extension.value,
            file_size=file_size,
            upload_by=current_user.id,
            file_language=file_language,
            status=status
        )
        file_pointer = await self.create_file_pointer(file_create_schema)

        # if extension == FileFormatType.PDF:
            # await self.process_pdf_file(file_pointer.id, current_user)        
        if extension == FileFormatType.PDF:
            background_tasks.add_task(self.process_pdf_file, file_pointer.id, current_user)
    
        return self._to_public_file_pointer(file=file_pointer)


    async def create_file_pointer(self,file_create_schema: FilePointerCreateSchema) -> File:
        new_file_data = file_create_schema.model_dump()
        if 'status' in new_file_data:
            new_file_data['status'] = FileStatus(new_file_data['status'])
        new_file = await self.file_repository.create(new_file_data)
        return new_file

    async def update_file_pointer(self, file_id: str, file_update_schema: FilePointerUpdateSchema) -> File:
        file = await self.file_repository.get_by("id", file_id, unique=True)
        
        if not file:
            raise AppError(
                title="get translation job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        
        update_data = {
            k: v for k, v in file_update_schema.model_dump().items() if v is not None
        }
        
        # Convert string status to enum for database
        if 'status' in update_data:
            update_data['status'] = FileStatus(update_data['status'])
        await self.file_repository.update(file, update_data)
        return file

    async def fetch_file_entity(self, file_id: str):

        file = await self.file_repository.get_by("id",file_id,unique=True)

        if not file:
            raise AppError(
                title="get translation job endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )

        return file

    async def get_file(self, file_id: str) -> Dict[str, Any]:
        file = await self.fetch_file_entity(file_id)

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
