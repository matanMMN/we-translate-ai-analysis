import pytest
from fastapi import Request
from meditranslate.src.access_control.tests.access_control_test import AccessControlTest
from unittest.mock import AsyncMock, patch,ANY
import json
import pytest
from meditranslate.src.access_control.access_control_schemas import (
    RoleCreateSchema, RoleUpdateSchema, RolesGetManySchema, PermissionCreateSchema,
    PermissionUpdateSchema, PermissionsGetManySchema, RoleHierarchyCreateSchema
)
from typing import Any
from meditranslate.app.db.models import User,Role, Permission,UserRole,RolePermission

prefix = "ac"
def with_base(data:dict,**kwargs):
    d = {
        'APP_API_KEY': kwargs.get('APP_API_KEY',None),
        'TENANT_API_KEY': kwargs.get('TENANT_API_KEY',None),
    }
    data.update(d)
    return data

@pytest.mark.asyncio
@pytest.mark.run(after='TestAccessControlRouter')
class TestAccessControlController(AccessControlTest):

    async def test_create_role(self):
        mock_create_role = self.mocker.patch(
            "server.src.access_control.access_control_service.create_role",
            new_callable=AsyncMock
        )
        role_data = {"id":"2w","name": "admin"}
        mock_create_role.return_value = Role(**role_data)
        response = await self.client.post(f"/{prefix}/roles", json=role_data)

        assert response.status_code == 201
        mock_create_role.assert_awaited_once_with(ANY,[],{})
        mock_create_role.assert_awaited_once()
        mock_create_role.assert_called_once()

    async def test_get_role(self):
        mock_get_role = self.mocker.patch(
            "server.src.access_control.access_control_service.get_role",
            new_callable=AsyncMock
        )
        role_id = "1"
        role_data = {"id": role_id, "name": "admin"}
        mock_get_role.return_value = Role(**role_data)
        response = await self.client.get(f"/{prefix}/roles/{role_id}")

        assert response.status_code == 200
        mock_get_role.assert_awaited_once_with(role_id,[],{})
        mock_get_role.assert_awaited_once()
        mock_get_role.assert_called_once()


    async def test_update_role(self):
        mock_update_role = self.mocker.patch(
            "server.src.access_control.access_control_service.update_role",
            new_callable=AsyncMock
        )
        role_id = "1"
        updated_data = {"name": "new_admin"}
        mock_update_role.return_value = Role(id=role_id, **updated_data)
        response = await self.client.put(f"/{prefix}/roles/{role_id}", json=updated_data)

        assert response.status_code == 200
        mock_update_role.assert_awaited_once_with(role_id, ANY,[],{})
        mock_update_role.assert_awaited_once()
        mock_update_role.assert_called_once()


    async def test_delete_role(self):
        mock_delete_role = self.mocker.patch(
            "server.src.access_control.access_control_service.delete_role",
            new_callable=AsyncMock
        )
        role_id = "1"
        mock_delete_role.return_value = {}
        response = await self.client.delete(f"/{prefix}/roles/{role_id}")

        assert response.status_code == 200
        mock_delete_role.assert_awaited_once_with(role_id,[],{})
        mock_delete_role.assert_awaited_once()
        mock_delete_role.assert_called_once()


    async def test_get_many_roles(self):
        mock_get_many_roles = self.mocker.patch(
            "server.src.access_control.access_control_service.get_many_roles",
            new_callable=AsyncMock
        )
        roles = [
            Role(id="1", name="admin"),
            Role(id="2", name="user"),
            Role(id="3", name="guest")
        ]
        total = len(roles)
        mock_get_many_roles.return_value = (roles, total)
        response = await self.client.get(f"/{prefix}/roles")

        assert response.status_code == 200
        mock_get_many_roles.assert_awaited_once_with(ANY,[],{})
        mock_get_many_roles.assert_awaited_once()
        mock_get_many_roles.assert_called_once()


    async def test_create_permission(self):
        mock_create_permission = self.mocker.patch(
            "server.src.access_control.access_control_service.create_permission",
            new_callable=AsyncMock
        )
        permission_data = {"action": "read", "resource": "document"}
        mock_create_permission.return_value = Permission(**permission_data)
        response = await self.client.post(f"/{prefix}/permissions", json=permission_data)

        assert response.status_code == 201
        mock_create_permission.assert_awaited_once_with(ANY,[],{})
        mock_create_permission.assert_awaited_once()
        mock_create_permission.assert_called_once()

    async def test_update_permission(self):
        mock_update_permission = self.mocker.patch(
            "server.src.access_control.access_control_service.update_permission",
            new_callable=AsyncMock
        )
        permission_id = "1"
        updated_data = {"action": "write", "resource": "document"}
        mock_update_permission.return_value = Permission(id=permission_id, **updated_data)
        response = await self.client.put(f"/{prefix}/permissions/{permission_id}", json=updated_data)

        assert response.status_code == 200
        mock_update_permission.assert_awaited_once_with(permission_id, ANY,[],{})
        mock_update_permission.assert_awaited_once()
        mock_update_permission.assert_called_once()


    async def test_get_permission(self):
        mock_get_permission = self.mocker.patch(
            "server.src.access_control.access_control_service.get_permission",
            new_callable=AsyncMock
        )
        permission_id = "1"
        mock_get_permission.return_value = Permission(id=permission_id, name="yes")
        response = await self.client.get(f"/{prefix}/permissions/{permission_id}")

        assert response.status_code == 200
        mock_get_permission.assert_awaited_once_with(permission_id,[],{})
        mock_get_permission.assert_awaited_once()
        mock_get_permission.assert_called_once()

    async def test_delete_permission(self):
        mock_delete_permission = self.mocker.patch(
            "server.src.access_control.access_control_service.delete_permission",
            new_callable=AsyncMock
        )
        permission_id = "1dsa"
        mock_delete_permission.return_value = {}
        response = await self.client.delete(f"/{prefix}/permissions/{permission_id}")

        assert response.status_code == 200
        mock_delete_permission.assert_awaited_once_with(permission_id,[],{})
        mock_delete_permission.assert_awaited_once()
        mock_delete_permission.assert_called_once()

    async def test_get_many_permissions(self):
        mock_get_many_permissions = self.mocker.patch(
            "server.src.access_control.access_control_service.get_many_permissions",
            new_callable=AsyncMock
        )
        permissions = [
            Permission(id="1", name="dasda"),
            Permission(id="2", name="pepepe"),
            Permission(id="3", name="dasda")
        ]
        total = len(permissions)
        mock_get_many_permissions.return_value = (permissions, total)
        response = await self.client.get(f"/{prefix}/permissions")
        assert response.status_code == 200
        mock_get_many_permissions.assert_awaited_once_with(ANY,[],{})
        mock_get_many_permissions.assert_awaited_once()
        mock_get_many_permissions.assert_called_once()



    async def test_create_user_role(self):
        mock_create_user_role = self.mocker.patch(
            "server.src.access_control.access_control_service.create_user_role",
            new_callable=AsyncMock
        )
        user_id = "user_id"
        role_id = "role_id"
        mock_create_user_role.return_value = True
        user_role = {
            "user_id":user_id,
            "role_id":role_id
        }
        response = await self.client.post(f"/{prefix}/user-roles",json=user_role)
        assert response.status_code == 201
        mock_create_user_role.assert_awaited_once_with(with_base(user_role),[],{})
        mock_create_user_role.assert_awaited_once()
        mock_create_user_role.assert_called_once()

    async def test_get_user_roles(self):
        mock_get_user_roles = self.mocker.patch(
            "server.src.access_control.access_control_service.get_user_roles",
            new_callable=AsyncMock
        )
        roles = []
        user_id = "1234"
        mock_get_user_roles.return_value = roles
        response = await self.client.get(f"/{prefix}/user-roles/{user_id}")
        assert response.status_code == 200
        mock_get_user_roles.assert_awaited_once_with(ANY,[],{})
        mock_get_user_roles.assert_awaited_once()
        mock_get_user_roles.assert_called_once()

    async def test_delete_user_role(self):
        mock_delete_user_roles = self.mocker.patch(
            "server.src.access_control.access_control_service.delete_user_role",
            new_callable=AsyncMock
        )
        user_id = "123"
        role_id = "dsda"
        mock_delete_user_roles.return_value = True
        response = await self.client.delete(f"/{prefix}/user-roles/{user_id}/{role_id}")
        assert response.status_code == 200
        mock_delete_user_roles.assert_awaited_once_with(user_id,role_id,[],{})
        mock_delete_user_roles.assert_awaited_once()
        mock_delete_user_roles.assert_called_once()

    async def test_create_role_permission(self):
        mock_create_role_permission = self.mocker.patch(
            "server.src.access_control.access_control_service.create_role_permission",
            new_callable=AsyncMock
        )
        role_id = "1234"
        permission_id = "adsa"
        role_permission = {
            "permission_id":permission_id,
            "role_id":role_id
        }
        mock_create_role_permission.return_value = None

        response = await self.client.post(f"/{prefix}/role/{role_id}/permissions", json=role_permission)
        assert response.status_code == 201
        mock_create_role_permission.assert_awaited_once_with(with_base(role_permission),[],{})
        mock_create_role_permission.assert_awaited_once()
        mock_create_role_permission.assert_called_once()

    async def test_get_role_permissions(self):
        mock_get_role_permissions = self.mocker.patch(
            "server.src.access_control.access_control_service.get_role_permissions",
            new_callable=AsyncMock
        )
        role_id = "12312"
        mock_get_role_permissions.return_value = []
        response = await self.client.get(f"/{prefix}/role/{role_id}/permissions")
        assert response.status_code == 200
        # mock_get_role_permissions.assert_awaited_once_with(with_base({"role_id":role_id}),[],{}) # TODO
        mock_get_role_permissions.assert_awaited_once_with(ANY,[],{})
        mock_get_role_permissions.assert_awaited_once()
        mock_get_role_permissions.assert_called_once()


    async def test_delete_role_permission(self):
        mock_delete_role_permission = self.mocker.patch(
            "server.src.access_control.access_control_service.delete_role_permission",
            new_callable=AsyncMock
        )
        mock_delete_role_permission.return_value = True
        role_id = "ddfs"
        permission_id = "dasd"
        response = await self.client.delete(f"/{prefix}/role/{role_id}/permissions/{permission_id}")
        assert response.status_code == 200
        mock_delete_role_permission.assert_awaited_once_with(role_id,permission_id,[],{})
        mock_delete_role_permission.assert_awaited_once()
        mock_delete_role_permission.assert_called_once()

    async def test_create_role_hierarchy(self):
        mock_create_role_hierarchy = self.mocker.patch(
            "server.src.access_control.access_control_service.create_role_hierarchy",
            new_callable=AsyncMock
        )
        mock_create_role_hierarchy.return_value = None
        parent_role_id = "123"
        child_role_id = "123"
        response = await self.client.post(f"/{prefix}/role-hierarchy",json={
            "parent_role_id":parent_role_id,
            "child_role_id":child_role_id
        })
        assert response.status_code == 201
        mock_create_role_hierarchy.assert_awaited_once_with(ANY,[],{})
        mock_create_role_hierarchy.assert_awaited_once()
        mock_create_role_hierarchy.assert_called_once()


    async def test_delete_role_hierarchy(self):
        mock_delete_role_hierarchy = self.mocker.patch(
            "server.src.access_control.access_control_service.delete_role_hierarchy",
            new_callable=AsyncMock
        )
        parent_role_id = "123"
        child_role_id = "123"
        mock_delete_role_hierarchy.return_value = None
        response = await self.client.delete(f"/{prefix}/role-hierarchy/{parent_role_id}/{child_role_id}")
        assert response.status_code == 200
        mock_delete_role_hierarchy.assert_awaited_once_with(parent_role_id,child_role_id,[],{})
        mock_delete_role_hierarchy.assert_awaited_once()
        mock_delete_role_hierarchy.assert_called_once()

    async def test_get_role_parent_roles(self):

        mock_get_parent_roles = self.mocker.patch(
            "server.src.access_control.access_control_service.get_role_parent_roles",
            new_callable=AsyncMock
        )
        role_id = "1"
        roles = [Role(id="2", name="parent_role")]
        mock_get_parent_roles.return_value = roles
        response = await self.client.get(f"/{prefix}/roles/{role_id}/parents")
        assert response.status_code == 200
        mock_get_parent_roles.assert_awaited_once_with(ANY,[],{})
        mock_get_parent_roles.assert_awaited_once()
        mock_get_parent_roles.assert_called_once()


    async def test_get_role_child_roles(self):
        mock_get_role_child_roles = self.mocker.patch(
            "server.src.access_control.access_control_service.get_role_child_roles",
            new_callable=AsyncMock
        )
        mock_get_role_child_roles.return_value = []
        role_id = "asdsa"
        response = await self.client.get(f"/{prefix}/roles/{role_id}/children")
        assert response.status_code == 200
        mock_get_role_child_roles.assert_awaited_once_with(ANY,[],{})
        mock_get_role_child_roles.assert_awaited_once()
        mock_get_role_child_roles.assert_called_once()













    # async def test_get_all_parent_roles_recursive(self):
    #     mock_get_role_parents_roles_recursive = self.mocker.patch(
    #         "server.src.access_control.access_control_service.get_all_parent_roles_recursive",
    #         new_callable=AsyncMock
    #     )
    #     mock_get_role_parents_roles_recursive.return_value =
    #     response = await self.client.get(f"/{prefix}/permissions")
    #     assert response.status_code == 200
    #     mock_get_role_parents_roles_recursive.assert_awaited_once_with(ANY,[],{})
    #     mock_get_role_parents_roles_recursive.assert_awaited_once()
    #     mock_get_role_parents_roles_recursive.assert_called_once()

    # async def test_get_all_child_roles_recursive(self):
    #     mock_get_role_child_roles_recursive = self.mocker.patch(
    #         "server.src.access_control.access_control_service.get_all_child_roles_recursive",
    #         new_callable=AsyncMock
    #     )
    #     mock_get_role_child_roles_recursive.return_value =
    #     response = await self.client.get(f"/{prefix}/permissions")
    #     assert response.status_code == 200
    #     mock_get_role_child_roles_recursive.assert_awaited_once_with(ANY,[],{})
    #     mock_get_role_child_roles_recursive.assert_awaited_once()
    #     mock_get_role_child_roles_recursive.assert_called_once()

