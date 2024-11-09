from fastapi import APIRouter, Depends,Request,Query,UploadFile,File,Form

from meditranslate.app.shared.factory import Factory
from meditranslate.app.shared.schemas import MetaSchema, PaginationSchema
from meditranslate.src.files.file_controller import FileController
from meditranslate.app.dependancies.auth import AuthenticationRequired
from meditranslate.app.dependancies.user import CurrentUserDep
from typing import Any,List,Annotated,Optional
from meditranslate.src.files.file_schemas import (
    GetManySchema,
    FilePointerResponseSchema,
    FilePointersResponseSchema,

)

from fastapi.responses import FileResponse,StreamingResponse
import json

file_router = APIRouter(
    tags=["files"],
    dependencies=[Depends(AuthenticationRequired)]
)

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


@file_router.post("/upload/", response_model=FilePointerResponseSchema,status_code=201)
async def upload_file(
    current_user: CurrentUserDep,
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
    # file_create_form_schema: Annotated[FileCreateSchema,Form(...,media_type="multipart/form-data")], # TODO change this FORM is not working
    file_controller: FileController = Depends(Factory.get_file_controller),
)-> FilePointerResponseSchema:
    """
    Upload File
    """
    file = await file_controller.upload_file(file,current_user)
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

    file_stream,filename = await file_controller.download_file(file_id)
    return StreamingResponse( # StreamingResponse more flexible and able to send any file size unlike FileResponse
        file_stream,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition":f"attachment; filename={filename}",
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
