from typing import List
from meditranslate.app.db.transaction import Propagation, Transactional
from fastapi import HTTPException
from meditranslate.src.requests.requests_service import RequestsService
from meditranslate.src.requests.requests import RequestType, RequestStatus
from meditranslate.src.requests.requests_schemas import (
    DeletionRequestCreate,
    TermRequestCreate,
    GlossaryRequestCreate,
    RequestUpdate,
    RequestResponse,
    RequestResponseSchema,
    RequestsResponseSchema
)
from meditranslate.app.db.models import User
from meditranslate.app.errors import AppError
from meditranslate.app.loggers import logger

class RequestsController:
    def __init__(self, service: RequestsService):
        self._service = service
        
    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def create_request(
        self,
        current_user: User,
        data: DeletionRequestCreate | TermRequestCreate | GlossaryRequestCreate,

    ) -> RequestResponseSchema:
        request = await self._service.create_request(current_user, data)
        return RequestResponseSchema(
            data=request.as_dict(),
            status_code=201
        )

    async def get_request(self, request_id: str) -> RequestResponseSchema:
        request = await self._service.get_request(request_id)
        return RequestResponseSchema(
            data=request.as_dict(),
            status_code=200
        )
    
    async def get_all_requests(
        self,
        current_user: User,
        request_type: RequestType | None = None,
        status: RequestStatus | None = None,
    ) -> RequestResponseSchema:
        requests = await self._service.get_all_requests(current_user, request_type, status)
        
        data = [request.as_dict() for request in requests]
        logger.info(data)
        return RequestsResponseSchema(
            data=data,
            status_code=200
        )

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def update_request(
        self,
        request_id: str,
        resolver: User,
        data: RequestUpdate
    ) -> RequestResponseSchema:
        request = await self._service.update_request(request_id, resolver, data)
        return RequestResponseSchema(
            data=request.as_dict(),
            status_code=200
        )
    

    async def get_requests_by_requester(
        self,
        current_user: User,
        requester_id: str,
        request_type: RequestType | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> RequestResponseSchema:
        requests = await self._service.get_requests_by_requester(current_user, requester_id, request_type, skip, limit)
        return RequestsResponseSchema(
            data=[request.as_dict() for request in requests],
            status_code=200
        )


    async def get_pending_requests(
        self,
        request_type: RequestType | None = None,
    ) -> RequestResponseSchema:
        requests = await self._service.get_pending_requests(request_type)
        return RequestsResponseSchema(
            data=[request.as_dict() for request in requests],
            status_code=200
        )
