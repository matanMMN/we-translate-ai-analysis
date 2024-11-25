from fastapi import APIRouter,Request,Query,Body

from meditranslate.app.dependancies.auth import AuthenticationRequired
from meditranslate.app.dependancies.user import CurrentUserDep
from meditranslate.app.shared.factory import Factory
from meditranslate.app.shared.schemas import PaginationSchema,MetaSchema

# from wetranslateai.app.shared.schemas import MetaSchema, PaginationSchema

from . import user_controller
from typing import Any,List,Annotated,Optional
from .user_schemas import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
    UsersResponseSchema,
    GetManySchema,
)
from fastapi.responses import JSONResponse
import json
from meditranslate.app.loggers import logger

from fastapi import Depends
from meditranslate.src.users.user_controller import UserController

user_router = APIRouter(
    tags=["users"],
    dependencies=[Depends(AuthenticationRequired)]
)

@user_router.post(
    path="",
    response_model=UserResponseSchema,
    status_code=201,
)
async def create_user(
    current_user: CurrentUserDep,
    user_create_schema: Annotated[UserCreateSchema,Body()],
    user_controller: UserController = Depends(Factory.get_user_controller)
)-> UserResponseSchema:
    """
    Create a new user.
    """
    user = await user_controller.create_user(current_user,user_create_schema)
    return UserResponseSchema(
        data=user,
        status_code=201,
    )


@user_router.get(
    "/{user_id}",
    response_model=UserResponseSchema,
    status_code=200,
)
async def get_user(
    current_user: CurrentUserDep,
    user_id: str,
    user_controller: UserController = Depends(Factory.get_user_controller)
)-> UserResponseSchema:
    """
    Retrieve a user by their ID.
    """
    logger.info(current_user)
    user = await user_controller.get_user(user_id)
    return UserResponseSchema(
        data=user,
        status_code=200,
        message="Retrieved User Successfully"
    )



@user_router.get(
    "/me/",
    response_model=UserResponseSchema,
    status_code=200,
)
async def get_user_me(
    current_user: CurrentUserDep,
    user_controller: UserController = Depends(Factory.get_user_controller)
)-> UserResponseSchema:
    """
    Retrieve a user by their ID.
    """
    logger.info(current_user)
    user = await user_controller.get_user(user_id=current_user.id,raise_exception=True,is_public=True)
    return UserResponseSchema(
        data=user,
        status_code=200,
        message="Retrieved User Successfully"
    )


@user_router.put(
    "/{user_id}",
    response_model=UserResponseSchema,
    status_code=200,
)
async def update_user(
    current_user: CurrentUserDep,
    user_id: str,
    user_update_schema: Annotated[UserUpdateSchema,Body()],
    user_controller: UserController = Depends(Factory.get_user_controller)
)-> UserResponseSchema:
    """
    Update a user's information.
    """

    await user_controller.update_user(current_user,user_id, user_update_schema)
    update_user = await user_controller.get_user(user_id=user_id)
    return UserResponseSchema(
        data=update_user,
        status_code=200,
    )


@user_router.delete(
    "/{user_id}",
    status_code=200,
)
async def delete_user(
    current_user: CurrentUserDep,
    user_id: str,
    user_controller: UserController = Depends(Factory.get_user_controller)
)-> Any:
    """
    Delete a user by their ID.
    """
    await user_controller.delete_user(current_user,user_id)



@user_router.get(
    "",
    response_model=UsersResponseSchema,
    status_code=200,
)
async def get_many_users(
    get_many_schema:Annotated[GetManySchema, Query()],
    user_controller: UserController = Depends(Factory.get_user_controller)
)-> UsersResponseSchema:
    """
    Retrieve a list of users with pagination.
    """
    users,total = await user_controller.get_many_users(get_many_schema)
    pagination = PaginationSchema(
        total=total,
        page=0,
        page_size=len(users)
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
    logger.debug(f"Retrieved users: {users}, total: {total}")

    return UsersResponseSchema(
        data=users,
        status_code=200,
        meta=meta.model_dump(),
        message="Users retrieved successfully"
    )


