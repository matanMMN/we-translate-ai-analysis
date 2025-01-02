from fastapi import APIRouter, Depends,Query,UploadFile,File,BackgroundTasks
from meditranslate.app.shared.schemas import BaseResponseSchema
from meditranslate.src.files.file_version_schemas import ListFilePointerResponseSchema
from meditranslate.app.dependancies.user import CurrentUserDep
from meditranslate.app.shared.factory import Factory
from meditranslate.app.shared.schemas import MetaSchema, PaginationSchema
from meditranslate.src.files.file_controller import FileController
from meditranslate.app.dependancies.auth import AuthenticationRequired
from meditranslate.app.dependancies.user import CurrentUserDep
from typing import Any,Annotated
from meditranslate.src.files.file_schemas import (
    GetManySchema,
    FilePointerResponseSchema,
    FilePointersResponseSchema,

)

from fastapi.responses import StreamingResponse

file_router = APIRouter(tags=["files"],dependencies=[Depends(AuthenticationRequired)])

@file_router.get("/{file_id}", response_model=FilePointerResponseSchema,status_code=200)
async def get_file(
    file_id: str,
    file_controller: FileController = Depends(Factory.get_file_controller)

)-> FilePointerResponseSchema:
    """
    Retrieve a file by their ID.
    """
    file = await file_controller.get_file(file_id)
    return FilePointerResponseSchema(
        data=file,
        status_code=200,
    )

@file_router.put("/{file_id}", response_model=FilePointerResponseSchema,status_code=200)
async def update_file(
    current_user: CurrentUserDep,
    file_id: str,
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
    file_controller: FileController = Depends(Factory.get_file_controller)

)-> FilePointerResponseSchema:
    await file_controller.update_file(current_user,file_id,file)
    updated_file = await file_controller.get_file(file_id)
    return FilePointerResponseSchema(
        data=updated_file,
        status_code=200,
    )

@file_router.post("/upload/", response_model=FilePointerResponseSchema,status_code=201)
async def upload_file(
    current_user: CurrentUserDep,
    background_tasks: BackgroundTasks,
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
    file_controller: FileController = Depends(Factory.get_file_controller),
)-> FilePointerResponseSchema:
    """
    Upload File
    """
    file = await file_controller.upload_file(current_user, file, background_tasks)
    print(file)
    return FilePointerResponseSchema(
        data=file,
        status_code=201,
    )

@file_router.get("/download/{file_id}" ,status_code=200, response_class=StreamingResponse)
async def download_file(
    file_id: str,
    file_controller: FileController = Depends(Factory.get_file_controller)
)-> StreamingResponse:
    """
    Download File
    """

    file_stream,filename,mime_type = await file_controller.download_file(file_id)
    return StreamingResponse( # StreamingResponse more flexible and able to send any file size unlike FileResponse
        file_stream,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition":f"attachment; filename*=UTF-8''{filename}",
            "Content-Type": mime_type
        },
        status_code=200,
    )



@file_router.delete(
    "/{file_id}",
    status_code=200,
)
async def delete_file(
    file_id: str,
    file_controller: FileController = Depends(Factory.get_file_controller)
)-> Any:
    """
    Delete a file by their ID.
    """
    await file_controller.delete_file(file_id)



@file_router.get("", response_model=FilePointersResponseSchema,status_code=200)
async def get_many_files(
    get_many_schema:Annotated[GetManySchema, Query()],
    file_controller: FileController = Depends(Factory.get_file_controller)
)-> FilePointersResponseSchema:
    """
    Retrieve a list of files with pagination.
    """
    files,total = await file_controller.get_many_files(get_many_schema)
    pagination = PaginationSchema(
        total=total,
        page=0,
        page_size=len(files)
    )
    if get_many_schema:
        schema = get_many_schema.model_dump()
        if schema.get("limit",None) is not None and schema.get("offset",None) is not None:
            page_size = get_many_schema.limit
            page = (get_many_schema.offset // get_many_schema.limit) + 1
            pagination = PaginationSchema(
                total=total,
                page=page,
                page_size=page_size
            )

    meta = MetaSchema(
        pagination=pagination
    )

    return FilePointersResponseSchema(
        data=files,
        status_code=200,
        meta=meta.model_dump(),
        message="Files retrieved successfully"
    )
@file_router.get("/{file_id}/versions", response_model=ListFilePointerResponseSchema)
async def get_file_versions(
    file_id: str,
    file_controller: FileController = Depends(Factory.get_file_controller)
) -> ListFilePointerResponseSchema:
    """Get all versions of a specific file"""
    versions = await file_controller.get_file_versions(file_id)
    return ListFilePointerResponseSchema(data=versions,)

@file_router.get("/{file_id}/versions/{version_number}")
async def download_file_version(
    file_id: str,
    version_number: int,
    file_controller: FileController = Depends(Factory.get_file_controller)

):
    """Download a specific version of a file"""
    file_stream, filename, content_type = await file_controller.get_specific_version(
        file_id=file_id,
        version_number=version_number
    )
    return StreamingResponse(
        file_stream,
        media_type=content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )

@file_router.post("/{file_id}/restore/{version_number}")
async def restore_file_version(
    file_id: str,
    version_number: int,
    current_user: CurrentUserDep,
    file_controller: FileController = Depends(Factory.get_file_controller)
):
    """Restore a specific version as the current version"""
    await file_controller.restore_version(
        file_id=file_id,
        version_number=version_number,
        current_user=current_user
    )
    return BaseResponseSchema(
        message="File version restored successfully"
    )