from tests.base_test import BaseTest
import pytest
from meditranslate.app.db import session
from sqlalchemy.sql import text
import pytest_asyncio

class AccessControlTest(BaseTest):
    @pytest_asyncio.fixture(autouse=True,scope="function")
    async def cleanup_db(self,request):
        """Ensure the database is clean before each test."""
        if request.cls and request.cls.__name__  == "TestUserRepository":
            await self.delete_all_users()
        yield

    async def delete_all_users(self):
        """Delete all users directly from the database."""
        async with session():
            # Corrected SQL query without '*'
            await session.execute(text("DELETE FROM users"))  # Use text to wrap the SQL
            await session.commit()

