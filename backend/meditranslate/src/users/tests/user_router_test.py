import time
from unittest.mock import AsyncMock,ANY

import pytest
import requests
from fastapi.responses import Response,JSONResponse
from typing import Any
from meditranslate.app.db import User
from meditranslate.src.users.user_schemas import GetManySchema
from faker import Faker
from uuid import uuid4
from meditranslate.app.loggers import logger
import json
fake = Faker()

# from server.src.users import user_router

from .user_test import UserTest

timeout = 2  # 2 seconds


@pytest.mark.asyncio(loop_scope="session")
class TestUserRouter(UserTest):

    async def test_create_user(self):
        try:

            mock_create_user = self.mocker.patch(
                "wetranslateai.src.users.user_controller.create_user",
                new_callable=AsyncMock
            )
            email=fake.email()
            username=fake.user_name()
            password=fake.password()
            user = {
                "email":email,
                "username":username,
            }
            mock_create_user.return_value = user
            response = await self.client.post("/users", timeout=timeout,json={
                "email":email,
                "username":username,
                "password":password
            })
            assert response is not None
            assert response.status_code != 404, "Expected status code not to be 404"
            assert response.status_code != 405, "Expected status code not to be 405"
            assert response.status_code == 201, "Expected status code to be 201"
            mock_create_user.assert_called()
            mock_create_user.assert_awaited_once()

        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_get_user(self):
        try:
            mock_get_user = self.mocker.patch(
                "wetranslateai.src.users.user_controller.get_user",
                new_callable=AsyncMock
            )
            user_id = str(uuid4())
            email=fake.email()
            username=fake.user_name()
            password=fake.password()
            user = {
                "id": user_id,
                "email":email,
                "username":username,
            }
            mock_get_user.return_value = user
            response = await self.client.get(f"/users/{user_id}", timeout=timeout)
            assert response is not None
            assert response.status_code == 200, "Expected status code to be 200"
            assert response.status_code != 404, "Expected status code not to be 404"
            assert response.status_code != 405, "Expected status code not to be 405"
            mock_get_user.assert_called()
            mock_get_user.assert_awaited_once()

        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_update_user(self):
        try:
            mock_update_user = self.mocker.patch(
                "wetranslateai.src.users.user_controller.update_user",
                new_callable=AsyncMock
            )
            user_id = str(uuid4())
            email=fake.email()
            username=fake.user_name()
            password=fake.password()
            new_name = "new_name"
            updated_user = {
                "id": user_id,
                "email":email,
                "username":username,
                "first_name":new_name
            }
            mock_update_user.return_value = updated_user
            response = await self.client.put(f"/users/{user_id}", timeout=timeout,json={
                "first_name":new_name
            })
            print(response)

            assert response is not None
            assert response.status_code != 404, "Expected status code not to be 404"
            assert response.status_code != 405, "Expected status code not to be 405"
            assert response.status_code == 200, "Expected status code to be 200"
            mock_update_user.assert_called()
            mock_update_user.assert_awaited_once()


        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_delete_user(self):
        try:
            mock_delete_user = self.mocker.patch(
                "wetranslateai.src.users.user_controller.delete_user",
                new_callable=AsyncMock
            )
            user_id = "1234a"
            mock_delete_user.return_value = None
            response = await self.client.delete(f"/users/{user_id}", timeout=timeout)
            assert response is not None
            assert response.status_code != 404, "Expected status code not to be 404"
            assert response.status_code != 405, "Expected status code not to be 405"
            assert response.status_code == 200, "Expected status code to be 200"
            mock_delete_user.assert_called()
            mock_delete_user.assert_awaited_once()

        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_get_many_users(self):
        try:
            mock_get_many_users = self.mocker.patch(
                "wetranslateai.src.users.user_controller.get_many_users",
                new_callable=AsyncMock
            )
            user_id_1 = "1234a1"
            user_id_2 = "1234a2"
            user1 = {
                "id":user_id_1,
                "username":fake.user_name(),
                "email":fake.email()
            }
            user2 = {
                "id":user_id_2,
                "username":fake.user_name(),
                "email":fake.email()
            }
            users = [
                user1,
                user2
            ]
            total = len(users)
            mock_get_many_users.return_value = users,total
            query_params = {
                "offset": 0,
                "limit": 10,
                "sort_by": "created_at",
                "sort_order": "asc",
                # "filters": {"active": True},  # Adjust according to your filter structure
                # "tags": ["tag1", "tag2"]
            }
            get_many_schema = GetManySchema(**query_params)

            response = await self.client.get("/users", timeout=timeout,params=get_many_schema.model_dump())

            assert response is not None
            assert response.status_code != 404, "Expected status code not to be 404"
            assert response.status_code != 405, "Expected status code not to be 405"
            assert response.status_code == 200, "Expected status code to be 200"
            mock_get_many_users.assert_called()
            mock_get_many_users.assert_awaited_once()
            # Print status code

            # # Print JSON body
            # try:
            #     logger.info(f"Status Code: {response.status_code}" )
            #     logger.info(f"Status Code: {response.text}" )
            #     # json_response = response.content
            #     json_response = response.json()
            #     logger.info(f"Response JSON: {json_response}")
            # except Exception as e:
            #     logger.error("Failed to parse JSON:", str(e))
            #     logger.error(f"Response Text: {response.text}")

        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

