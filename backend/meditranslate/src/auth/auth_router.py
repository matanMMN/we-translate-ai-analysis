from fastapi import APIRouter, Depends,Request,Query

from typing import Any,List,Annotated,Optional

from fastapi.security import OAuth2PasswordRequestForm

from meditranslate.app.shared.factory import Factory
from meditranslate.src.auth.auth_controller import AuthController
from .auth_schemas import (
    LoginSchema,
    TokenSchema,
    TokenResponseSchema
)


auth_router = APIRouter(
    tags=["auth"]
)

@auth_router.post(
    "/login",
    response_model=TokenResponseSchema,
    status_code=200
)
async def login(
    form_schema:Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_controller:AuthController = Depends(Factory.get_auth_controller)
) -> TokenResponseSchema:
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
    return TokenResponseSchema(
        data=TokenSchema(access_token=access_token,token_type="bearer").model_dump()
    )
