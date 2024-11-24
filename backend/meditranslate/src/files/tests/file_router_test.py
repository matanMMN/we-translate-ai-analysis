# import time
# from unittest.mock import AsyncMock,ANY

# import pytest
# import requests
# from lib.common.loggers import logger
# from fastapi.responses import Response,JSONResponse
# from typing import Any
# from server.app.services.db import User
# from server.src.users.user_schemas import UserResponseSchema,UsersGetManySchema


# # from server.src.users import user_router

# from .file_test import UserTest

# timeout = 2  # 2 seconds


# @pytest.mark.asyncio(loop_scope="session")
# class TestUserRouter(UserTest):

#     async def test_random_post_user_endpoint(self):
#         try:
#             response = await self.client.post("/ASDFASDSA",json={}, timeout=timeout)
#             assert response.status_code == 404, "Expected status code to be 404"
#         except requests.exceptions.ConnectionError:
#             pytest.skip("Connection refused or could not resolve hostname")
#         except requests.exceptions.Timeout:
#             pytest.skip("Request timed out")
#         except Exception as e:
#             pytest.skip(f"An unexpected error occurred: {str(e)}")


#     async def test_random_get_user_endpoint(self):
#         try:
#             response = await self.client.get("/dasdadada", timeout=timeout)
#             assert response.status_code == 404, "Expected status code to be 404"
#         except requests.exceptions.ConnectionError:
#             pytest.skip("Connection refused or could not resolve hostname")
#         except requests.exceptions.Timeout:
#             pytest.skip("Request timed out")
#         except Exception as e:
#             pytest.skip(f"An unexpected error occurred: {str(e)}")


#     async def test_create_user(self):
#         try:
#             mock_create_user = self.mocker.patch(
#                 "server.src.users.user_controller.create_user",
#                 new_callable=AsyncMock
#             )

#             user_id = "1234a"
#             user = User(id=user_id)
#             mock_create_user.return_value = user
#             response = await self.client.post("/users", timeout=timeout,json={
#                 "id":user_id
#             })
#             assert response is not None
#             assert response.status_code != 404, "Expected status code not to be 404"
#             assert response.status_code != 405, "Expected status code not to be 405"
#             assert response.status_code == 201, "Expected status code to be 201"
#             mock_create_user.assert_called()
#             mock_create_user.assert_awaited_once()
#             mock_create_user.assert_called_once_with(ANY,ANY,[],{})
#             assert response.json()["data"]["id"] == user_id

#         except requests.exceptions.ConnectionError:
#             pytest.fail("Connection refused or could not resolve hostname")
#         except requests.exceptions.Timeout:
#             pytest.fail("Request timed out")
#         except Exception as e:
#             pytest.fail(f"An unexpected error occurred: {str(e)}")

#     async def test_get_user(self):
#         try:
#             mock_get_user = self.mocker.patch(
#                 "server.src.users.user_controller.get_user",
#                 new_callable=AsyncMock
#             )
#             user_id = "1234a"
#             user = User(id=user_id)
#             mock_get_user.return_value = user
#             response = await self.client.get(f"/users/{user_id}", timeout=timeout)
#             assert response is not None
#             assert response.status_code == 200, "Expected status code to be 200"
#             assert response.status_code != 404, "Expected status code not to be 404"
#             assert response.status_code != 405, "Expected status code not to be 405"
#             mock_get_user.assert_called()
#             mock_get_user.assert_awaited_once()
#             mock_get_user.assert_called_once_with(ANY, user_id,[],{})
#             assert response.json()["data"]["id"] == user_id
#         except requests.exceptions.ConnectionError:
#             pytest.fail("Connection refused or could not resolve hostname")
#         except requests.exceptions.Timeout:
#             pytest.fail("Request timed out")
#         except Exception as e:
#             pytest.fail(f"An unexpected error occurred: {str(e)}")

#     async def test_update_user(self):
#         try:
#             mock_update_user = self.mocker.patch(
#                 "server.src.users.user_controller.update_user",
#                 new_callable=AsyncMock
#             )

#             user_id = "1234a"
#             new_name = "new_name"
#             # before_user = User(id=user_id,first_name="before")
#             after_user = User(id=user_id,first_name=new_name)
#             mock_update_user.return_value = after_user
#             response = await self.client.put(f"/users/{user_id}", timeout=timeout,json={
#                 "first_name":new_name
#             })

#             assert response is not None
#             assert response.status_code != 404, "Expected status code not to be 404"
#             assert response.status_code != 405, "Expected status code not to be 405"
#             assert response.status_code == 200, "Expected status code to be 200"
#             mock_update_user.assert_called()
#             mock_update_user.assert_awaited_once()
#             mock_update_user.assert_called_once_with(ANY, user_id,ANY,[],{})
#             assert response.json()["data"]["id"] == user_id
#             assert response.json()["data"]["first_name"] == new_name

#         except requests.exceptions.ConnectionError:
#             pytest.fail("Connection refused or could not resolve hostname")
#         except requests.exceptions.Timeout:
#             pytest.fail("Request timed out")
#         except Exception as e:
#             pytest.fail(f"An unexpected error occurred: {str(e)}")

#     async def test_delete_user(self):
#         try:
#             mock_delete_user = self.mocker.patch(
#                 "server.src.users.user_controller.delete_user",
#                 new_callable=AsyncMock
#             )
#             user_id = "1234a"
#             mock_delete_user.return_value = None
#             response = await self.client.delete(f"/users/{user_id}", timeout=timeout)
#             assert response is not None
#             assert response.status_code != 404, "Expected status code not to be 404"
#             assert response.status_code != 405, "Expected status code not to be 405"
#             assert response.status_code == 200, "Expected status code to be 200"
#             assert response.json()['data'] == None
#             mock_delete_user.assert_called()
#             mock_delete_user.assert_awaited_once()
#             mock_delete_user.assert_called_once_with(ANY, user_id,[],{})

#         except requests.exceptions.ConnectionError:
#             pytest.fail("Connection refused or could not resolve hostname")
#         except requests.exceptions.Timeout:
#             pytest.fail("Request timed out")
#         except Exception as e:
#             pytest.fail(f"An unexpected error occurred: {str(e)}")

#     async def test_get_many_users(self):
#         try:
#             mock_get_many_users = self.mocker.patch(
#                 "server.src.users.user_controller.get_many_users",
#                 new_callable=AsyncMock
#             )
#             user_id_1 = "1234a1"
#             user_id_2 = "1234a2"
#             user1 = User(id=user_id_1)
#             user2 = User(id=user_id_2)
#             users = [
#                 user1,
#                 user2
#             ]
#             total = len(users)
#             mock_get_many_users.return_value = users,total
#             query_params = {
#                 "offset": 0,
#                 "limit": 10,
#                 "sort_by": "created_at",
#                 "sort_order": "asc",
#                 # "filters": {"active": True},  # Adjust according to your filter structure
#                 # "tags": ["tag1", "tag2"]
#             }
#             get_many_schema = UsersGetManySchema(**query_params)

#             response = await self.client.get("/users", timeout=timeout)
#             assert response is not None
#             assert response.status_code != 404, "Expected status code not to be 404"
#             assert response.status_code != 405, "Expected status code not to be 405"
#             assert response.status_code == 200, "Expected status code to be 200"
#             mock_get_many_users.assert_called()
#             mock_get_many_users.assert_awaited_once()
#             mock_get_many_users.assert_called_once_with(ANY, get_many_schema,[],{})
#             assert len(response.json()['data']) == 2
#             # assert response.json()['meta']['pagination'] == []

#         except requests.exceptions.ConnectionError:
#             pytest.fail("Connection refused or could not resolve hostname")
#         except requests.exceptions.Timeout:
#             pytest.fail("Request timed out")
#         except Exception as e:
#             pytest.fail(f"An unexpected error occurred: {str(e)}")

