import pytest
from fastapi import Request
from .user_test import UserTest
from unittest.mock import AsyncMock, patch,ANY
import json
from meditranslate.app.db.models import User
from uuid import uuid4
from tests.factory.users import create_fake_user

from faker import Faker
fake = Faker()

@pytest.mark.asyncio
@pytest.mark.run(after='TestUserRouter')
class TestUserController(UserTest):

    async def test_create_user(self):
        try:
            mock_create_user = self.mocker.patch(target="wetranslateai.src.users.user_service.UserService.create_user",new_callable=AsyncMock)
            mock_create_user.return_value = create_fake_user()
            response = await self.client.post("/users",json=create_fake_user(with_id=False))
            assert response.status_code == 201
            mock_create_user.assert_awaited()
            mock_create_user.assert_awaited_once()
            mock_create_user.assert_called_once()

        except Exception as e:
            pytest.fail(f"unknown error has occured: {str(e)}")

    async def test_get_user(self):
        try:
            mock_get_user = self.mocker.patch(
                "wetranslateai.src.users.user_service.UserService.get_user",
                new_callable=AsyncMock)
            user_id = str(uuid4())
            user = {
                "username":fake.user_name(),
                "first_name":fake.name(),
                "email":fake.email(),
                "id":user_id
            }
            mock_get_user.return_value = user
            response = await self.client.get(f"/users/{user_id}")
            assert response.status_code == 200
            mock_get_user.assert_awaited()
            mock_get_user.assert_awaited_once()
            mock_get_user.assert_called_once()
            mock_get_user.assert_called_once_with(user_id)

        except Exception as e:
            pytest.fail(f"unknown error has occured: {str(e)}")

    async def test_update_user(self):
        try:
            mock_update_user = self.mocker.patch(
                "wetranslateai.src.users.user_service.UserService.update_user",
                new_callable=AsyncMock
            )
            user_id = str(uuid4())
            user = {
                "username":fake.user_name(),
                "first_name":fake.name(),
                "email":fake.email(),
                "id":user_id
            }
            mock_update_user.return_value = user
            response = await self.client.put(f"/users/{user_id}",json=user)
            assert response.status_code == 200
            mock_update_user.assert_awaited()
            mock_update_user.assert_awaited_once()
            mock_update_user.assert_called_once()
            mock_update_user.assert_called_once_with(user_id,ANY)


        except Exception as e:
            pytest.fail(f"unknown error has occured: {str(e)}")

    async def test_delete_user(self):
        try:
            mock_delete_user = self.mocker.patch(
                "wetranslateai.src.users.user_service.UserService.delete_user",new_callable=AsyncMock)
            user_id = str(uuid4())
            mock_delete_user.return_value =None
            response = await self.client.delete(f"/users/{user_id}")
            assert response.status_code == 200
            mock_delete_user.assert_awaited()
            mock_delete_user.assert_awaited_once()
            mock_delete_user.assert_called_once()
            mock_delete_user.assert_called_once_with(user_id)

        except Exception as e:
            pytest.fail(f"unknown error has occured: {str(e)}")

    async def test_get_many_users(self):
        try:
            mock_get_user = self.mocker.patch(
                "wetranslateai.src.users.user_service.UserService.get_many_users",new_callable=AsyncMock)
            users = []
            total = len(users)
            mock_get_user.return_value = users,total
            response = await self.client.get(f"/users")
            assert response.status_code == 200
            mock_get_user.assert_awaited()
            mock_get_user.assert_awaited_once()
            mock_get_user.assert_called_once()
        except Exception as e:
            pytest.fail(f"unknown error has occured: {str(e)}")
