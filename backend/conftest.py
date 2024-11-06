""" Module """
import logging
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio
from _pytest.logging import LogCaptureFixture
from meditranslate.app.application import create_app
from meditranslate.app.loggers import logger
from sqlalchemy.ext.asyncio import create_async_engine
from meditranslate.app.db import Base

pytestmark = pytest.mark.anyio

logging.getLogger('faker').setLevel(logging.ERROR)

TEST_DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost:5432/mydatabase"

BASE_URL = "http://testserver"

class PropagateHandler(logging.Handler):
    def emit(self,record):
        logger = logging.getLogger(record.name)
        if logger.isEnabledFor(record.levelno):
            logger.handle(record)


@pytest.fixture(autouse=True,scope="session")
def cleanup_loguru():
    logger.remove()


@pytest.fixture(autouse=True,scope="session")
def propegate_loguru(cleanup_loguru):
    handler_id = logger.add(PropagateHandler(),format="{message}")
    yield
    logger.remove(handler_id)

@pytest_asyncio.fixture(autouse=True) #ignore
async def caplog(caplog: LogCaptureFixture):
    """
        Make pytest work with loguru. See:https://loguru.readthedocs.io/en/stable/resources/migration.html#making-things-work-with-pytest-and-caplog
    """
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)


@pytest.fixture(params=[
    pytest.param(('asyncio', {'use_uvloop': True}), id='asyncio+uvloop'),
    # pytest.param(('asyncio', {'use_uvloop': False}), id='asyncio'),
    # pytest.param(('trio', {'restrict_keyboard_interrupt_to_checkpoints': True}), id='trio')
])
def anyio_backend(request):
    return request.param


@pytest_asyncio.fixture(autouse=True) # initialize database for session
async def initial_database(anyio_backend) -> None:
    async_engine = create_async_engine(str(TEST_DATABASE_URL))
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await async_engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def initial_app(initial_database):
    app = create_app()
    yield app

@pytest_asyncio.fixture(autouse=True)
async def async_client(initial_app: FastAPI):
    transport:ASGITransport = ASGITransport(
        app=initial_app,
        raise_app_exceptions=True,
        # client=("1.2.3.4",123),
        # root_path="/submount"
    )

    async with AsyncClient(
        transport=transport,
        base_url=BASE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    ) as ac:
        yield ac
