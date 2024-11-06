from fastapi import APIRouter, Depends,Request,Query

from meditranslate.app.shared.factory import Factory
from meditranslate.app.shared.schemas import MetaSchema, PaginationSchema
from meditranslate.src.files.file_controller import FileController
from fastapi import File
from typing import Any,List,Annotated,Optional
from meditranslate.src.files.file_schemas import (
    FileCreateSchema,
    GetManySchema,
    FileResponseSchema,
    FilesResponseSchema,

)
from fastapi.responses import JSONResponse
import json



file_router = APIRouter()

@file_router.post("", response_model=FileResponseSchema,status_code=201)
async def create_file(
    file_create_schema: FileCreateSchema,
    file_controller: FileController = Depends(Factory.get_file_controller)
)-> FileResponseSchema:
    """
    Create a new file.
    """
    file = await file_controller.create_file(file_create_schema)
    return FileResponseSchema(
        data=file.as_dict(),
        status_code=201,
    )

@file_router.get("/{file_id}", response_model=FileResponseSchema,status_code=200)
async def get_file(
    file_id: str,
    file_controller: FileController = Depends(Factory.get_file_controller)

)-> FileResponseSchema:
    """
    Retrieve a file by their ID.
    """
    file = await file_controller.get_file(file_id)
    return FileResponseSchema(
        data=file,
        status_code=200,
    )


@file_router.get("", response_model=FileResponseSchema,status_code=200)
async def upload_file(
    file: Annotated[bytes, File()],
    file_controller: FileController = Depends(Factory.get_file_controller),
)-> FileResponseSchema:
    """
    Upload File
    """
    file = await file_controller.get_file(file_id)
    return FileResponseSchema(
        data=file.as_dict(),
        status_code=200,
    )

# @file_router.get("/{file_id}", response_model=FileResponseSchema,status_code=200)
# async def download_file(
#     file_id: str,
#     file_controller: FileController = Depends(Factory.get_file_controller)
# )-> Any:
#     """
#     Retrieve a file by their ID.
#     """
#     file = await file_controller.(request, file_id,[],{})
#     return fileResponseSchema(
#         data=file.as_dict(),
#         status_code=200,
#     )



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



@file_router.get("", response_model=FilesResponseSchema,status_code=200)
async def get_many_files(
    get_many_schema:Annotated[GetManySchema, Query()],
    file_controller: FileController = Depends(Factory.get_file_controller)
)-> FilesResponseSchema:
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

    return FilesResponseSchema(
        data=files,
        status_code=200,
        meta=meta.model_dump(),
        message="Files retrieved successfully"
    )
