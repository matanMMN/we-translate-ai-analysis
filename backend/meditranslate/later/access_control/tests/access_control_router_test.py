import time
from unittest.mock import AsyncMock
import traceback
import pytest
import requests
from meditranslate.src.access_control.tests.access_control_test import AccessControlTest
from unittest.mock import AsyncMock, patch
from fastapi.responses import Response,JSONResponse
from meditranslate.app.db.models import Role,Permission,RolePermission,UserRole

timeout = 2  # 2 seconds

prefix = "ac"

@pytest.mark.asyncio(loop_scope="session")
class TestAccessControlRouter(AccessControlTest):
    async def test_random_post_role_endpoint(self):
        try:
            response = await self.client.post(f"/{prefix}/nonexistent-endpoint", timeout=timeout)
            assert response is not None
            assert response.status_code == 404, "Expected status code to be 404 for non-existent endpoint"

        except requests.exceptions.ConnectionError:
            pytest.skip("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.skip("Request timed out")
        except Exception as e:
            pytest.skip(f"An unexpected error occurred: {str(e)}")


    async def test_create_role(self):
        try:
            mock_create_role = self.mocker.patch(
                "server.src.access_control.access_control_controller.create_role",
                new_callable=AsyncMock
            )
            role_id = "torl_of"
            role_title = "admin"
            role = Role(id=role_id,name=role_title)
            mock_create_role.return_value = role
            response = await self.client.post(f"/{prefix}/roles", json={
                    # "id":role_id,
                    "name": role_title
                }, timeout=timeout
            )
            assert response.status_code == 201, "Expected status code 201"
            mock_create_role.assert_called_once()
            mock_create_role.assert_awaited_once()

        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_get_role(self):
        try:
            mock_get_role = self.mocker.patch(
                "server.src.access_control.access_control_controller.get_role",
                new_callable=AsyncMock
            )
            role_id = "235"
            role_title = "asdasd"
            role = Role(id=role_id,name=role_title)
            mock_get_role.return_value = role
            response = await self.client.get(f"/{prefix}/roles/{role_id}", timeout=timeout)
            assert response.status_code == 200, "Expected status code 200"
            mock_get_role.assert_called_once()
            mock_get_role.assert_awaited_once()
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_update_role(self):
        try:
            mock_update_role = self.mocker.patch(
                "server.src.access_control.access_control_controller.update_role",
                new_callable=AsyncMock
            )
            role_id = "235"
            new_title = "yes"
            role = Role(id=role_id,name=new_title)
            mock_update_role.return_value = role
            response = await self.client.put(f"/{prefix}/roles/{role_id}", json={"name": new_title}, timeout=timeout)
            assert response.status_code == 200, "Expected status code 200"
            mock_update_role.assert_called_once()
            mock_update_role.assert_awaited_once()
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_delete_role(self):
        try:
            mock_create_role = self.mocker.patch(
                "server.src.access_control.access_control_controller.delete_role",
                new_callable=AsyncMock
            )
            role_id = "235"
            mock_create_role.return_value = True
            response = await self.client.delete(f"/{prefix}/roles/{role_id}", timeout=timeout)
            assert response.status_code == 200, "Expected status code 200"
            mock_create_role.assert_called_once()
            mock_create_role.assert_awaited_once()
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_get_many_roles(self):
        try:
            mock_get_many_roles = self.mocker.patch(
                "server.src.access_control.access_control_controller.get_many_roles",
                new_callable=AsyncMock
            )
            roles = [
                Role(id="123",name="paaaa"),
                Role(id="1234",name="masss")
            ]
            mock_get_many_roles.return_value = roles,len(roles)
            response = await self.client.get(f"/{prefix}/roles", timeout=timeout)
            assert response.status_code == 200, "Expected status code 200"
            mock_get_many_roles.assert_called_once()
            mock_get_many_roles.assert_awaited_once()
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_create_permission(self):
        try:
            mock_create_permission = self.mocker.patch(
                "server.src.access_control.access_control_controller.create_permission",
                new_callable=AsyncMock
            )
            mock_create_permission.return_value = Permission()
            response = await self.client.post(f"/{prefix}/permissions", json={"action": "read", "resource": "document"}, timeout=timeout)
            assert response.status_code == 201, "Expected status code 201"
            mock_create_permission.assert_called_once()
            mock_create_permission.assert_awaited_once()
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_get_permission(self):
        try:
            mock_get_permission = self.mocker.patch(
                "server.src.access_control.access_control_controller.get_permission",
                new_callable=AsyncMock
            )
            permission_id = "123"
            permission = Permission(id=permission_id,action="action",resource="resource")
            mock_get_permission.return_value = permission
            response = await self.client.get(f"/{prefix}/permissions/{permission_id}", timeout=timeout)
            assert response.status_code == 200, "Expected status code 200"
            mock_get_permission.assert_called_once()
            mock_get_permission.assert_awaited_once()
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_update_permission(self):
        try:
            mock_update_permission = self.mocker.patch(
                "server.src.access_control.access_control_controller.update_permission",
                new_callable=AsyncMock
            )
            permission_id = "123"
            permission = Permission(id=permission_id)
            mock_update_permission.return_value = permission
            response = await self.client.put(f"/{prefix}/permissions/{permission_id}", json={"action": "write", "resource": "document"}, timeout=timeout)
            assert response.status_code == 200, "Expected status code 200"
            mock_update_permission.assert_called_once()
            mock_update_permission.assert_awaited_once()
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_delete_permission(self):
        try:
            mock_delete_permission = self.mocker.patch(
                "server.src.access_control.access_control_controller.delete_permission",
                new_callable=AsyncMock
            )
            permission_id = "13233"
            mock_delete_permission.return_value = True
            response = await self.client.delete(f"/{prefix}/permissions/{permission_id}", timeout=timeout)
            assert response.status_code == 200, "Expected status code 200"
            mock_delete_permission.assert_called_once()
            mock_delete_permission.assert_awaited_once()
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_get_role_parent_roles(self):
        try:
            mock_get_role_parent_roles = self.mocker.patch(
                "server.src.access_control.access_control_controller.get_role_parent_roles",
                new_callable=AsyncMock
            )
            role_id = "123"
            roles = [
                Role(name="rol1"),
                Role(name="rol2"),
            ]
            mock_get_role_parent_roles.return_value = roles
            response = await self.client.get(f"/{prefix}/roles/{role_id}/parents", timeout=timeout)
            assert response.status_code == 200, "Expected status code 200"
            mock_get_role_parent_roles.assert_called_once()
            mock_get_role_parent_roles.assert_awaited_once()

        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_delete_role_hierarchy(self):
        try:
            mock_delete_role_hierarchy = self.mocker.patch(
                "server.src.access_control.access_control_controller.delete_role_hierarchy",
                new_callable=AsyncMock
            )
            parent_role_id = "12"
            child_role_id = "34"
            mock_delete_role_hierarchy.return_value = True
            response = await self.client.delete(f"/{prefix}/role-hierarchy/{parent_role_id}/{child_role_id}", timeout=timeout)
            assert response.status_code == 200, "Expected status code 200"
            mock_delete_role_hierarchy.assert_called_once()
            mock_delete_role_hierarchy.assert_awaited_once()
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_create_user_role(self):
        try:
            mock_create_user_role = self.mocker.patch(
                "server.src.access_control.access_control_controller.create_user_role",
                new_callable=AsyncMock
            )
            user_role = UserRole(user_id="123",role_id="12")
            mock_create_user_role.return_value = user_role
            response = await self.client.post(f"/{prefix}/user-roles", json={"user_id": "1", "role_id": "2"}, timeout=timeout)
            assert response.status_code == 201, "Expected status code 201"
            mock_create_user_role.assert_called_once()
            mock_create_user_role.assert_awaited_once()

        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_get_user_roles(self):
        try:
            mock_get_user_roles = self.mocker.patch(
                "server.src.access_control.access_control_controller.get_user_roles",
                new_callable=AsyncMock
            )
            user_id = "123"
            roles = [
                Role(id="123"),
                Role(id="1243")
            ]
            mock_get_user_roles.return_value = roles
            response = await self.client.get(f"/{prefix}/user-roles/{user_id}", timeout=timeout)
            assert response.status_code == 200, "Expected status code 200"
            mock_get_user_roles.assert_called_once()
            mock_get_user_roles.assert_awaited_once()
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")

    async def test_delete_user_role(self):
        try:
            mock_delete_user_role = self.mocker.patch(
                "server.src.access_control.access_control_controller.delete_user_role",
                new_callable=AsyncMock
            )
            user_id = "123"
            role_id = "1234"
            mock_delete_user_role.return_value = True
            response = await self.client.delete(f"/{prefix}/user-roles/{user_id}/{role_id}", timeout=timeout)
            assert response.status_code == 200, "Expected status code 204"
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused or could not resolve hostname")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred: {str(e)}")
