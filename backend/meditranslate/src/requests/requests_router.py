from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Body, Query
from meditranslate.app.shared.factory import Factory
from meditranslate.app.dependancies.auth import AuthenticationRequired
from meditranslate.app.dependancies.user import CurrentUserDep
from meditranslate.src.requests.requests_controller import RequestsController
from meditranslate.src.requests.requests import RequestType, RequestStatus
from meditranslate.src.requests.requests_schemas import (
    DeletionRequestCreate,
    TermRequestCreate,
    GlossaryRequestCreate,
    RequestUpdate,
    RequestsResponseSchema,
    RequestResponseSchema
)

requests_router = APIRouter(
    tags=["requests"],
    dependencies=[Depends(AuthenticationRequired)]
)

@requests_router.post(
    path="/deletion",
    response_model=RequestResponseSchema,
    status_code=201
)
async def create_deletion_request(
    data: Annotated[DeletionRequestCreate, Body()],
    current_user: CurrentUserDep,
    controller: RequestsController = Depends(Factory.get_requests_controller)
) -> RequestResponseSchema:
    return await controller.create_request(current_user, data)

@requests_router.post(
    path="/term",
    response_model=RequestResponseSchema,
    status_code=201
)
async def create_term_request(
    data: Annotated[TermRequestCreate, Body()],
    current_user: CurrentUserDep,
    controller: RequestsController = Depends(Factory.get_requests_controller)
) -> RequestResponseSchema:
    return await controller.create_request(current_user, data)

@requests_router.post(
    path="/glossary",
    response_model=RequestResponseSchema,
    status_code=201
)
async def create_glossary_request(
    data: Annotated[GlossaryRequestCreate, Body()],
    current_user: CurrentUserDep,
    controller: RequestsController = Depends(Factory.get_requests_controller)
) -> RequestResponseSchema:
    return await controller.create_request(current_user, data)

@requests_router.get(
    path="/{request_id}",
    response_model=RequestResponseSchema
)
async def get_request(
    request_id: str,
    controller: RequestsController = Depends(Factory.get_requests_controller)
) -> RequestResponseSchema:
    return await controller.get_request(request_id)

@requests_router.get(
    path="/",
    response_model=RequestsResponseSchema
)
async def get_all_requests(
    current_user: CurrentUserDep,
    request_type: Optional[RequestType] = Query(None),
    status: Optional[RequestStatus] = Query(None),
    controller: RequestsController = Depends(Factory.get_requests_controller)
) -> RequestsResponseSchema:
    return await controller.get_all_requests(current_user, request_type, status)

@requests_router.put(
    path="/{request_id}",
    response_model=RequestResponseSchema
)
async def update_request(
    request_id: str,
    data: Annotated[RequestUpdate, Body()],
    current_user: CurrentUserDep,
    controller: RequestsController = Depends(Factory.get_requests_controller)
) -> RequestResponseSchema:
    return await controller.update_request(request_id, current_user, data)

@requests_router.get(
    path="/user/{user_id}",
    response_model=RequestsResponseSchema
)
async def get_user_requests(
    current_user: CurrentUserDep,
    request_type: Optional[RequestType] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    controller: RequestsController = Depends(Factory.get_requests_controller)
) -> RequestsResponseSchema:
    return await controller.get_requests_by_requester(current_user, request_type, skip, limit)

@requests_router.get(
    path="/pending/all",
    response_model=RequestsResponseSchema
)
async def get_pending_requests(
    request_type: Optional[RequestType] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    controller: RequestsController = Depends(Factory.get_requests_controller)
) -> RequestsResponseSchema:
    return await controller.get_pending_requests(request_type, skip, limit) 