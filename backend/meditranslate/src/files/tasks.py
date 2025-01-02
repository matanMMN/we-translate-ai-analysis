"""
Celery tasks for file processing operations.
"""
import asyncio
from fastapi import UploadFile
from celery import shared_task
from meditranslate.app.db.session import get_task_session
from meditranslate.app.celery_app import celery
from meditranslate.app.configurations import config
from meditranslate.utils.files.file_status import FileStatus
from meditranslate.src.files.file_service import FileService
from meditranslate.src.files.file_schemas import FilePointerUpdateSchema
from meditranslate.utils.files.formats.pdf_to_docx import pdf_to_docx_bytes
from meditranslate.utils.files.file_format_type import FileFormatType
from meditranslate.utils.files.formats.file_format_handler import FileFormatHandler
from meditranslate.utils.language.utils import get_language_from_text
from meditranslate.app.errors import AppError, HTTPStatus
from meditranslate.app.loggers import logger
from meditranslate.app.storage import file_storage_service
import io
from uuid import uuid4
from meditranslate.src.files.file_service import FileService
from meditranslate.src.files.file_repository import FileRepository
from contextlib import asynccontextmanager


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
        raise

async def process_file_async(file_id: str, user_id: str):
    """Async context manager for database session"""
    async for session in get_task_session():
        try:
            yield session
        finally:
            await session.close()

async def process_file_async(file_id: str, user_id: str):
    async for session in get_task_session():
        try:
            file_repository = FileRepository(session)
            file_service = FileService(file_repository, file_storage_service)

            print(f"Getting file pointer for file {file_id}")
            file_pointer = await file_service.file_repository.get_by("id", file_id, unique=True)
            if not file_pointer:
                raise AppError(title="get update job endpoint", http_status=HTTPStatus.NOT_FOUND)

            print(f"Downloading PDF file {file_id}") 
            download_result = await file_service.download_file_sync(file_id, is_bytes=True)
            pdf_bytes, original_filename, _ = download_result
            
            print(f"Converting PDF file {file_id} to DOCX")
            docx_bytes = await pdf_to_docx_bytes(pdf_bytes, config.OPENAI_API_KEY)
            print(f"Uploading DOCX file {file_id}")
            new_filename = original_filename.rsplit('.', 1)[0]
            new_file_name = f"{new_filename}-{str(uuid4())}.v1.docx"
            print(f"Deleting original PDF file {file_id}")
            file_service.storage_service.delete_file(file_pointer.file_path)
            
            # Create new UploadFile for DOCX
            print(f"Creating new UploadFile for DOCX")
            docx_file = UploadFile(
                filename=new_filename,
                file=io.BytesIO(docx_bytes)
            )
            print(f"Creating new storage file path for DOCX")
            storage_file_path = file_service.storage_service.create_file_path(new_file_name)
            print(f"Uploading DOCX file {file_id}")
            # Upload the DOCX file
            file_service.storage_service.upload_file(
                file=docx_file,
                file_path=storage_file_path
            )
            print(f"Extracting text and detecting language")
            # Extract text and detect language
            docx_io = io.BytesIO(docx_bytes)
            file_content = FileFormatHandler().extract_text(FileFormatType.DOCX, docx_io)
            file_language = get_language_from_text(file_content)
            print(f"Checking if file is valid")
            if file_language is None or not file_service._is_valid_input_file(file_content):
                raise AppError(
                    title="invalid file",
                    user_message="Could not detect language in converted file",
                    http_status=HTTPStatus.NOT_ACCEPTABLE
                )
            print(f"Updating file pointer with new information")
            # Update file pointer with new information
            update_schema = FilePointerUpdateSchema(
                original_file_name=new_filename,
                file_path=storage_file_path,
                file_format_type=FileFormatType.DOCX.value,
                status=FileStatus.READY.value,
                file_name=new_file_name,
                file_size=len(docx_bytes),
                file_language=file_language,
                file_url=file_service.storage_service.base_url,
                file_storage_provider=file_service.storage_service.storage_provider.value,
                upload_by=user_id,
                current_version=1,
                file_metadata=None
            )
            
            await file_service.update_file_pointer(file_id, update_schema)
            await session.commit()

            logger.info(f"Successfully processed PDF file {file_id} to DOCX")
        
        
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
                
@shared_task(
    name='process_pdf_file_task',
    bind=True,
    max_retries=1,
    default_retry_delay=8,
    queue='pdf_processing'
)
def process_pdf_file_task(self, file_id: str, user_id: str):
    """
    Process a PDF file asynchronously, converting it to DOCX format.
    """
    try:
        print(f"Processing PDF file {file_id} to DOCX")
        loop = get_or_create_eventloop()
        loop.run_until_complete(process_file_async(file_id, user_id))
        
    except Exception as e:
        logger.error(f"PDF processing failed for file {file_id}: {str(e)}")
        raise self.retry(exc=e)