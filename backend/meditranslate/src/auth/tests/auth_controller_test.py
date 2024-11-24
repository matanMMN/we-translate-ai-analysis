import pytest
from fastapi import Request
from meditranslate.src.auth.tests.auth_test import AuthTest
from unittest.mock import AsyncMock, patch,ANY
import json
from meditranslate.app.db.models import User
from uuid import uuid4

from faker import Faker
fake = Faker()

@pytest.mark.asyncio
class TestAuthController(AuthTest):

    async def test_login(self):
        try:
            mock_login = self.mocker.patch(
                "wetranslateai.src.auth.auth_service.login",
                new_callable=AsyncMock
            )
            creds = {
                "username":fake.user_name(),
                "password":fake.password(),
            }
            token = "test_token"
            mock_login.return_value = token
            response = await self.client.post("/auth/login",json=creds)
            assert response.status_code == 200
            mock_login.assert_awaited()
            mock_login.assert_awaited_once()
            mock_login.assert_called_once()
            mock_login.assert_called_once_with(creds)

        except Exception as e:
            pytest.fail(f"unknown error has occured: {str(e)}")
