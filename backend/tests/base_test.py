import pytest
from httpx import AsyncClient
import pytest_asyncio
from pytest import FixtureRequest
from pytest_mock import MockerFixture
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from meditranslate.app.loggers import logger
from fastapi import FastAPI

@pytest.mark.asyncio(loop_scope="session")
class BaseTest():
    """Base class for tests, integrating pytest fixtures."""

    @pytest_asyncio.fixture(autouse=True)
    async def setup_client(self, request:FixtureRequest, async_client:AsyncClient):

        """Set up the test environment for all derived tests."""
        self.client = async_client

    @pytest_asyncio.fixture(autouse=True)
    async def setup_app(self, request:FixtureRequest, app:FastAPI):

        """Set up the test environment for all derived tests."""
        self.app = app

    # @pytest_asyncio.fixture(autouse=True,scope="function")
    # async def setup_session(self, request:FixtureRequest, db_session: AsyncSession):
    #     """Set up the database for tests marked with 'database'."""
    #     self.session = db_session

    @pytest_asyncio.fixture(autouse=True)
    async def setup_mocker(self, request:FixtureRequest, mocker:MockerFixture):
        """Set up the database for tests marked with 'database'."""
        self.mocker = mocker
