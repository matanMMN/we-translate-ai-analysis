import sys

from fastapi.responses import JSONResponse

from meditranslate.app.errors.error_handler import ErrorHandler,AppError
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from meditranslate.src.base_router import base_router
from meditranslate.app.db import init_db
from prometheus_fastapi_instrumentator import Instrumentator,metrics
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from meditranslate.app.middlewares.sqlalchemy_middleware import SQLAlchemyMiddleware
from meditranslate.app.middlewares.logging_middleware import LoggingMiddleware
from meditranslate.app.middlewares.error_middleware import ErrorMiddleware

from meditranslate.app.configurations import config,EnvironmentType
from fastapi import Depends
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from typing import List
from meditranslate.app.loggers import logger
from fastapi.exceptions import RequestValidationError
from fastapi import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from meditranslate.app.dependancies.limit import rate_limiter_dependency

from fastapi.exceptions import HTTPException
from globals import ROOT_DIR

from meditranslate.app.monitoring import setup_monitoring
from meditranslate.app.info import get_contact_info,get_license_info,get_terms_of_service,get_summary


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    redis_connection = redis.from_url(config.REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)
    await init_db()
    yield
    # shutdown ,cleanup
    await FastAPILimiter.close()

def create_app() -> FastAPI:
    app_ = FastAPI(
        title=config.APP_NAME,
        description=config.APP_DESCRIPTION,
        contact=get_contact_info(),
        license_info=get_license_info(),
        version=config.RELEASE_VERSION,
        terms_of_service=get_terms_of_service(),
        summary=get_summary(),
        docs_url=None if config.ENVIRONMENT == EnvironmentType.PRODUCTION  else config.DOCS_URL,
        redoc_url=None if config.ENVIRONMENT == EnvironmentType.PRODUCTION  else config.REDOC_URL,
        debug=config.DEBUG,
        lifespan=lifespan,
        dependencies=[
            rate_limiter_dependency(
                minutes=1,
                times=config.GLOBAL_RATE_LIMIT_PER_MINUTE
            )],
    )
    setup_monitoring(app=app_)


    @app_.exception_handler(Exception)
    async def exception_handler(request:Request, exc:Exception):
        logger.error("Exception exception_handler")
        return await ErrorHandler.handle_error(request,exc)

    @app_.exception_handler(AppError)
    async def exception_handler(request:Request, exc:AppError):
        logger.error("App Error  exception_handler")
        return await ErrorHandler.handle_error(request,exc)

    @app_.exception_handler(RequestValidationError)
    async def standard_validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error("RequestValidationError exception_handler")
        return await ErrorHandler.handle_error(request,exc)

    @app_.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request:Request, exc:StarletteHTTPException):
        logger.error("StarletteHTTPException exception_handler")
        return await ErrorHandler.handle_error(request,exc)

    app_.add_middleware(
        ErrorMiddleware
    )

    app_.add_middleware(
        LoggingMiddleware
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app_.add_middleware(
        TrustedHostMiddleware, allowed_hosts=["*"]
    )

    app_.add_middleware(
        SQLAlchemyMiddleware
    )

    app_.include_router(base_router)

    return app_

