# from server.lib.common.loggers import logger
# import pytest
# from server.lib.common.errors.app_error import AppError
# from .file_test import UserTest

# @pytest.mark.asyncio
# @pytest.mark.run(after='TestUserController')
# class TestUserService(UserTest):
#     async def test_create_user(self):
#         response = await self.client.post("/users",json={})
#         assert response.status_code == 201

#     async def test_get_user(self):
#         try:
#             response = await self.client.post("/users",json={})
#             assert response is not None
#             result = response.json()
#             user = result['data']
#             user_id = user['id']
#             response = await self.client.get(f"/users/{user_id}")
#             result = response.json()
#             assert response.status_code == 200
#         except Exception as e:
#             pytest.fail(f"unknown error has occured: {str(e)}")

#     async def test_update_user(self):
#         try:
#             expected = "new_name"
#             response = await self.client.post("/users",json={})
#             assert response is not None
#             result = response.json()
#             user = result.get('data',None)
#             user_id = user.get('id')
#             if not user_id:
#                 pytest.fail("failed to get user id")
#             response = await self.client.put(f"/users/{user_id}",json={
#                 "first_name":expected
#             })
#             result = response.json()
#             user = result.get('data',None)
#             actual = user.get("first_name") if user else None
#             assert response.status_code == 200
#             assert actual == expected

#         except Exception as e:
#             pytest.fail(f"unknown error has occured: {str(e)}")

#     async def test_delete_user(self):
#         user_id = "1234"
#         user = await self.client.post("/users",json={"id":user_id})
#         assert response is not None
#         result = response.json()
#         user = result['data']
#         user_id = user['id']
#         user = await self.client.get(f"/users/{user_id}")
#         assert user
#         response = await self.client.delete(f"/users/{user_id}")
#         assert response.status_code == 200
#         with pytest.raises(AppError):
#             await self.client.get(f"/users/{user_id}")


#     async def test_get_many_users(self):
#         response = await self.client.get("/users")
#         assert response.status_code == 200
#         # assert isinstance(response.json(),list) is True
