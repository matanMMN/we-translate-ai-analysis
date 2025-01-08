from datetime import datetime
from http import HTTPStatus
from logging import Filter
from typing import List, Optional
from meditranslate.app.errors import AppError
from meditranslate.app.shared.base_service import BaseService
from meditranslate.src.requests.requests_repository import RequestRepository
from meditranslate.src.translation_jobs.translation_job_repository import TranslationJobRepository
from meditranslate.src.requests.requests import Request, RequestType, RequestStatus
from meditranslate.src.users.user import User
from meditranslate.src.requests.requests_schemas import (
    DeletionRequestCreate,
    TermRequestCreate,
    GlossaryRequestCreate,
    RequestUpdate
)
from meditranslate.app.loggers import logger

class RequestsService(BaseService[Request]):
    def __init__(self, requests_repository: RequestRepository,translation_job_repository: TranslationJobRepository):
        super().__init__(model=Request, repository=requests_repository)
        self.requests_repository = requests_repository
        self.translation_job_repository = translation_job_repository


    async def _check_duplicate_request(self, data: DeletionRequestCreate | TermRequestCreate | GlossaryRequestCreate) -> None:
        """Check for duplicate pending requests"""
        logger.debug(f"Checking for duplicate {data.request_type} requests")
        
        if data.request_type == RequestType.DELETION:
            logger.debug(f"Checking for existing deletion request for project {data.project_id}")
            existing_request = await self.requests_repository.get_by(
                field="project_id",
                value=data.project_id,
                joins=None,
                unique=True
            )
        else:  # TERM or GLOSSARY
            logger.debug(f"Checking for existing {data.request_type.lower()} request for terms: {data.source_term} -> {data.target_term}")
            # First check by source term
            existing_request = await self.requests_repository.get_by(
                field="source_term",
                value=data.source_term,
                joins=None,
                unique=True
            )
            # If found, verify it matches other criteria
            if existing_request and (
                existing_request.target_term == data.target_term and
                existing_request.request_type == data.request_type and
                existing_request.status == RequestStatus.PENDING
            ):
                pass
            else:
                existing_request = None

        if existing_request and existing_request.status == RequestStatus.PENDING:
            logger.warning(f"Found duplicate pending {data.request_type.lower()} request")
            error_message = (
                f"A pending deletion request already exists for project {data.project_id}"
                if data.request_type == RequestType.DELETION
                else f"A pending {data.request_type.lower()} request already exists for these terms"
            )
            raise AppError(
                title="Duplicate Request",
                context=error_message,
                http_status=HTTPStatus.CONFLICT
            )

    async def _validate_request_data(self, data: DeletionRequestCreate | TermRequestCreate | GlossaryRequestCreate) -> None:
        """Validate request data based on request type"""
        logger.debug(f"Starting validation for {data.request_type} request")
        await self._check_duplicate_request(data)
        if data.request_type == RequestType.DELETION:
            await self._validate_deletion_request(data)
        elif data.request_type in [RequestType.TERM, RequestType.GLOSSARY]:
            await self._validate_term_request(data)

    async def _validate_deletion_request(self, data: DeletionRequestCreate) -> None:
        """Validate deletion request specific fields"""
        logger.debug(f"Validating deletion request for project {data.project_id}")
        
        if not data.project_id:
            logger.warning("Deletion request missing project ID")
            raise AppError(
                title="Validation Error",
                context="Project ID is required for deletion requests",
                http_status=HTTPStatus.BAD_REQUEST
            )
        
        if not data.reason or len(data.reason.strip()) < 10:
            logger.warning("Deletion request reason too short or missing")
            raise AppError(
                title="Validation Error",
                context="Reason is not elaborated enough",
                http_status=HTTPStatus.BAD_REQUEST
            )
        
        logger.debug(f"Checking if project {data.project_id} exists")
        project = await self.translation_job_repository.get_by(field="id", value=data.project_id, joins=None, unique=True)
        if not project:
            logger.warning(f"Project {data.project_id} not found")
            raise AppError(
                title="Not Found",
                context=f"Project with ID {data.project_id} not found",
                http_status=HTTPStatus.NOT_FOUND
            )

        
    async def _validate_term_request(self, data: TermRequestCreate | GlossaryRequestCreate) -> None:
        """Validate term/glossary request specific fields"""
        logger.debug(f"Validating {data.request_type.lower()} request")
        
        if not data.source_term or not data.target_term:
            logger.warning(f"{data.request_type} request missing source or target term")
            raise AppError(
                title="Validation Error",
                context=f"Source and target terms are required for {data.request_type.lower()} requests",
                http_status=HTTPStatus.BAD_REQUEST
            )

        if data.context and len(data.context.strip()) < 10:
            logger.warning("Request context too short")
            raise AppError(
                title="Validation Error",
                context="Context, if provided, must be at least 10 characters long",
                http_status=HTTPStatus.BAD_REQUEST
            )


    async def create_request(
        self,
        current_user: User,
        data: DeletionRequestCreate | TermRequestCreate | GlossaryRequestCreate
    ) -> Request:
        logger.info(f"Creating new {data.request_type} request for user {current_user.id}")
        request_data = data.model_dump()
        request_data["requester_id"] = current_user.id
        
        logger.debug(f"Validating request data: {request_data}")
        await self._validate_request_data(data)
        
        
        logger.info("Creating request in database")
        logger.info(request_data)
        try:
            request = await self.requests_repository.create(request_data)
            logger.info(f"Successfully created request with ID: {request.id}")
            return request
        except Exception as e:
            logger.error(f"Failed to create request: {str(e)}")
            raise

    async def get_request(self, request_id: str) -> Request:
        """Get a single request by ID with all relationships loaded"""
        logger.info(f"Fetching request with ID: {request_id}")
        
        request = await self.requests_repository.get_by(
            field="id",
            value=request_id,
            unique=True
        )
        
        if not request:
            logger.warning(f"Request {request_id} not found")
            raise AppError(
                title="Not Found",
                detail=f"Request with ID {request_id} not found",
                http_status=HTTPStatus.NOT_FOUND
            )
            
        logger.info(f"Successfully fetched request {request_id}")
        return request

    async def get_all_requests(
        self,
        current_user: User,
        request_type: Optional[RequestType] = None,
        status: Optional[RequestStatus] = None,
    ) -> List[Request]:
        """Get all requests with optional type and status filters"""
        logger.info(f"Fetching all requests with type: {request_type}, status: {status}")
        
        filters = []
        if request_type is not None:
            logger.debug(f"Adding request_type filter: {request_type}")
            filter_request_type = Filter("request_type")
            filter_request_type.value = request_type
            filters.append(filter_request_type)
            
        if status is not None:
            logger.debug(f"Adding status filter: {status}")
            filter_status = Filter("status")
            filter_status.value = status
            filters.append(filter_status)
            
        # Get requests with applied filters (if any)
        requests, _ = await self.requests_repository.get_many(filters=filters)
            
        logger.info(f"Found {len(requests)} requests after filtering")
        return requests


    async def update_request(
        self,
        request_id: str,
        resolver: User,
        data: RequestUpdate
    ) -> Request:
        """Update a request's status and add resolution details"""
        logger.info(f"Updating request {request_id} by resolver {resolver.id}")    
        request = await self.get_request(request_id)
        updated_request = data.model_dump()
        updated_request['updated_at'] = datetime.now()

        # if request.status != RequestStatus.PENDING:
        #     logger.warning(f"Attempt to update non-pending request {request_id}")
        #     raise AppError(
        #         title="Invalid Operation",
        #         detail="Only pending requests can be updated",
        #         http_status=HTTPStatus.BAD_REQUEST
        #     )       

        try:
            await self.requests_repository.update(request, updated_request)
            logger.info(f"Successfully updated request {request_id}")
            return await self.get_request(request_id)
        except Exception as e:
            logger.error(f"Failed to update request {request_id}: {str(e)}")
            raise

    async def get_requests_by_requester(
        self,
        current_user: User,
        request_type: Optional[RequestType] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Request]:
        """Get all requests made by a specific user"""
        logger.info(f"Fetching requests for requester {current_user.id}")
        

        filters = [Filter("requester_id", current_user.id)]
        requests, _ = await self.requests_repository.get_many(filters=filters)
        # Apply type filter in memory if specified
        if request_type:
            requests = [r for r in requests if r.request_type == request_type]
            
        # Apply pagination in memory
        start = skip
        end = skip + limit
        requests = requests[start:end]
            
        logger.info(f"Found {len(requests)} requests for requester {current_user.id}")
        return requests

    async def get_pending_requests(
        self,
        request_type: Optional[RequestType] = None,
    ) -> List[Request]:
        """Get all pending requests"""
        logger.info(f"Fetching pending requests of type: {request_type}")
        
        requests, _ = await self.requests_repository.get_many(filters=[Filter("status", RequestStatus.PENDING)])
        if request_type:
            requests = [r for r in requests if r.request_type == request_type]
    
            
        logger.info(f"Found {len(requests)} pending requests")
        return requests