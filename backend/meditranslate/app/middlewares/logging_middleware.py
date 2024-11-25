from typing import Optional,Dict,Any
from pydantic import BaseModel, Field,ConfigDict
from starlette.datastructures import Headers
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Message, Receive, Scope, Send
import time
from fastapi import Request,Response
from meditranslate.app.loggers import logger
import json



class RequestLog(BaseModel):
    method: str
    url: str
    headers: Dict[str, str]
    query_params: Dict[str, str]
    cookies: Dict[str, str]
    client: Optional[str]
    body: Optional[Any]

class ResponseLog(BaseModel):
    status_code: int
    headers: Dict[str, str]
    # body: Optional[Any]

class LogEntry(BaseModel):
    model_config:ConfigDict=ConfigDict(
        arbitrary_types_allowed=True
    )
    request: dict
    response: dict
    duration: float


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_time = time.time()
        response = await call_next(request)
        duration = time.time() - request_time
        log_entry = LogEntry(
            request=self.parse_request(request),
            response=self.parse_response(response),
            duration=duration,
        )
        logger.debug(log_entry)
        return response

    def parse_request(self,request:Request) -> dict:
        return {}

    def parse_response(self,response:Response) -> dict:
        return {}
