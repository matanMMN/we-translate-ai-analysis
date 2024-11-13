from fastapi import APIRouter, Body, Depends,Request,Query

from typing import Any,List,Annotated,Optional

from fastapi.security import OAuth2PasswordRequestForm

from meditranslate.app.shared.factory import Factory
from meditranslate.src.auth.auth_controller import AuthController
from meditranslate.src.users.user_schemas import UserResponseSchema
from .auth_schemas import (
    LoginSchema,
    TokenSchema,
    TokenResponseSchema,
    RegisterUserSchema
)
from meditranslate.app.loggers import logger


auth_router = APIRouter(
    tags=["auth"]
)


@auth_router.post(
    path="/register",
    response_model=UserResponseSchema,
    status_code=201,

)
async def register_user(
    user_create_schema: Annotated[RegisterUserSchema,Body(example={
            "email" : "string@string.com",
            "username": "string",
            "password" : "string",
            "first_name":"example",
            "last_name":"example"
        })],
    auth_controller: AuthController = Depends(Factory.get_auth_controller)
)-> UserResponseSchema:
    """
    Create a new user.
    """
    new_user = await auth_controller.register_user(user_create_schema)
    logger.debug(new_user)
    return UserResponseSchema(
        data=new_user,
        status_code=201
    )


@auth_router.post(
    "/token",
    response_model=TokenSchema,
    status_code=200,
)
async def login(
    form_schema:Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_controller:AuthController = Depends(Factory.get_auth_controller)
) -> TokenSchema:
    data = {}
    data["scopes"] = []
    for scope in form_schema.scopes:
        data["scopes"].append(scope)
    if form_schema.client_id:
        data["client_id"] = form_schema.client_id
    if form_schema.client_secret:
        data["client_secret"] = form_schema.client_secret

    login_schema = LoginSchema(username=form_schema.username,password=form_schema.password)
    access_token = await auth_controller.login(login_schema)

    return TokenSchema(access_token=access_token,token_type="bearer")
