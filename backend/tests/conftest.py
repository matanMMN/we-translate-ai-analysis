""" Module """
from typing import Any, Generator
import pytest
import pytest_asyncio


from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session,async_sessionmaker,create_async_engine

from fastapi import FastAPI
from httpx import AsyncClient,ASGITransport

from meditranslate.app.application import create_app
from meditranslate.app.configurations import config
from meditranslate.app.db import get_session
from meditranslate.app.db.base import Base
from meditranslate.app.loggers import logger


TEST_DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost:5432/mydatabase"
BASE_URL = "http://testserver"



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


@pytest_asyncio.fixture(loop_scope="session",scope="session")
async def app(anyio_backend):
    app = create_app()
    yield app



@pytest_asyncio.fixture(loop_scope="session",scope="function")
async def app(anyio_backend):
    async_engine = create_async_engine(str(config.DATABASE_URL))
    AsyncScopedSession = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncScopedSession() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        AsyncScopedSession = s
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    await async_engine.dispose()

    async def override_get_db():
        db = AsyncScopedSession
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_session] = override_get_db
    yield app
    # shutdown app.



@pytest_asyncio.fixture(scope="function")
async def db_session(app:FastAPI) -> AsyncSession:
    async_engine = create_async_engine(str(config.DATABASE_URL))
    AsyncScopedSession = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncScopedSession() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        AsyncScopedSession = s
        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        pass

    await async_engine.dispose()


    def override_get_db():
        db = AsyncScopedSession
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_session] = override_get_db




@pytest_asyncio.fixture(loop_scope="session",scope="function")
async def async_client(app: FastAPI):
    transport:ASGITransport = ASGITransport(
        app=app,
        raise_app_exceptions=True,
        # client=("1.2.3.4",123),
        # root_path="/submount"
    )

    async with AsyncClient(
        transport=transport,
        base_url=BASE_URL,
        headers={
            "Accept": "application/json",  # Indicating that the client expects JSON responses
            "Content-Type": "application/json",  # Indicating the content type of the request
        },
    ) as ac:
        yield ac



@pytest.fixture(scope="session")
def api_app() -> Generator[FastAPI, Any, None]:
    """
    Create a new FastAPI app
    """
    app = create_app()

    yield app

@pytest_asyncio.fixture(scope="function")
async def api_client(api_app: FastAPI, db_session) -> AsyncClient:
    """
    Create a new FastAPI AsyncClient
    """

    async def _get_session():
        return db_session

    api_app.dependency_overrides[get_session] = _get_session
    transport:ASGITransport = ASGITransport(
        app=api_app,
        raise_app_exceptions=True,
        # client=("1.2.3.4",123),
        # root_path="/submount"
    )
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        yield client

