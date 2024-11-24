from unittest.mock import AsyncMock
from uuid import uuid4
from httpx import AsyncClient
import pytest
from meditranslate.app.errors.app_error import AppError
from meditranslate.src.auth.tests.auth_test import AuthTest
from meditranslate.app.db.models import User
from meditranslate.src.users.user_repository import UserRepository
from meditranslate.utils.security.password import hash_password
from meditranslate.app.db.session import get_session
from fastapi.testclient import TestClient

from faker import Faker
fake = Faker()


@pytest.mark.asyncio
@pytest.mark.run(after='TestUserController')
class TestAuthService(AuthTest):
    async def test_login(self,api_client:AsyncClient):
        # self.app.dependency_overrides[get_session] = get_session
        # self.app.dependency_overrides["db_session"] = lambda: self.session()

        # test_client = TestClient(self.app)


        email = fake.email()
        username =fake.user_name()
        password =fake.password()
        user_id = str(uuid4())
        user_args = {
            "username":username,
            "password":password,
            "email":email
        }

        create_response = await api_client.post(f"/users",json=user_args)
        login_response = await api_client.post(f"/auth/login",json={
            "username":username,
            "password":password
        })
        assert login_response == 200

