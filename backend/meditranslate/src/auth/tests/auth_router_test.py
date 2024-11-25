import time
from unittest.mock import AsyncMock,ANY

import pytest
import requests
from fastapi.responses import Response,JSONResponse
from typing import Any
from faker import Faker
from uuid import uuid4
from meditranslate.app.loggers import logger

import json
fake = Faker()

# from server.src.users import user_router

from meditranslate.src.auth.tests.auth_test import AuthTest
from meditranslate.src.auth.auth_schemas import LoginSchema

timeout = 2  # 2 seconds


@pytest.mark.asyncio(loop_scope="session")
class TestAuthRouter(AuthTest):

    async def test_login(self):
        try:

            mock_login = self.mocker.patch(
                "wetranslateai.src.auth.auth_controller.login",
                new_callable=AsyncMock
            )
            username=fake.user_name()
            password=fake.password()
            creds = {
                "password":password,
                "username":username,
            }
            token = "test_token"
            mock_login.return_value = token
            response = await self.client.post("/auth/login", timeout=timeout,json=creds)
            assert response is not None
            assert response.status_code != 404, "Expected status code not to be 404"
            assert response.status_code != 405, "Expected status code not to be 405"
            assert response.status_code == 200, "Expected status code to be 201"
            mock_login.assert_called()
            mock_login.assert_awaited_once()
            mock_login.assert_awaited_once_with(LoginSchema(**creds))

        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")
