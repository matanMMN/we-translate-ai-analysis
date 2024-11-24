# import sys
# sys.dont_write_bytecode = True


from meditranslate.src.access_control.tests.access_control_test import AccessControlTest
import pytest
from meditranslate.src.access_control.role_permission_repository import RolePermissionRepository
from meditranslate.src.access_control.role_repository import RoleRepository
from meditranslate.src.access_control.permission_repository import PermissionRepository
from meditranslate.app.errors import AppError

@pytest.mark.run(after=['TestPermissionRepository','TestRoleRepository'])
@pytest.mark.asyncio(loop_scope="session")
class TestRolePermissionRepository(AccessControlTest):

    @pytest.mark.run(order=1)
    async def test_create_role_permission(self):

        role_id = "12345"
        permission_id = "123"
        role_permission_data = {
            "role_id": role_id,
            "permission_id": permission_id
        }
        role_repo = RoleRepository()
        permission_repo = PermissionRepository()

        role = await role_repo.create_role({"id": role_id, "name": "Admin"})
        permission = await permission_repo.create_permission({"id": permission_id,"name":"permi", "action": "read", "resource": "user"})

        role_permission_repo = RolePermissionRepository()

        role_permission = await role_permission_repo.create_role_permission(role_permission_data=role_permission_data)
        assert role_permission is not None
        assert role_permission.role_id == role_permission_data["role_id"]
        assert role_permission.permission_id == role_permission_data["permission_id"]

    @pytest.mark.run(order=2)
    async def test_get_role_permission(self):
        role_repo = RoleRepository()
        permission_repo = PermissionRepository()
        role = await role_repo.create_role({"id": "role_id_soemthing", "name": "Admin"})
        permission = await permission_repo.create_permission({"id": "permission_id_soemthign","name":"permi"})
        role_permission_repo = RolePermissionRepository()
        await role_permission_repo.create_role_permission(role_permission_data={
            "role_id":role.id,
            "permission_id":permission.id
        })
        role_permission = await role_permission_repo.get_role_permission(role_id=role.id, permission_id=permission.id)
        assert role_permission is not None
        assert role_permission.role_id == role.id
        assert role_permission.permission_id == permission.id

    @pytest.mark.run(order=3)
    async def test_get_role_permissions(self):
        role_repo = RoleRepository()
        permission_repo = PermissionRepository()
        role_id = "role123"
        permission_id = "permission123"
        permission_id_2 = "pereper12"
        role = await role_repo.create_role({"id": role_id, "name": "Admin"})
        permission = await permission_repo.create_permission({"id": permission_id,"name":"permi"})
        permission_2 = await permission_repo.create_permission({"id": permission_id_2,"name":"perami"})

        role_permission_repo = RolePermissionRepository()
        await role_permission_repo.create_role_permission(role_permission_data={
            "role_id":role.id,
            "permission_id":permission.id
        })
        await role_permission_repo.create_role_permission(role_permission_data={
            "role_id":role.id,
            "permission_id":permission_2.id
        })

        permissions = await role_permission_repo.get_role_permissions(role_id=role_id)

        assert permissions is not None
        assert len(permissions) == 2
        permission_ids = [permission.id for permission in permissions]
        assert permission.id in permission_ids
        assert permission_2.id in permission_ids



    @pytest.mark.run(order=4)
    async def test_delete_role_permission(self):
        role_repo = RoleRepository()
        permission_repo = PermissionRepository()
        role_id = "role123"
        permission_id = "permission123"
        role = await role_repo.create_role({"id": role_id, "name": "Admin"})
        permission = await permission_repo.create_permission({"id": permission_id,"name":"permi", "action": "read", "resource": "user"})
        role_permission_repo = RolePermissionRepository()

        with pytest.raises(AppError):
            await role_permission_repo.get_role_permission(role_id=role.id, permission_id=permission.id)

        await role_permission_repo.create_role_permission(role_permission_data={
            "role_id":role.id,
            "permission_id":permission.id
        })

        role_permission = await role_permission_repo.get_role_permission(role_id=role.id, permission_id=permission.id)
        assert role_permission is not None

        result = await role_permission_repo.delete_role_permission(role_id=role_id, permission_id=permission_id)
        assert result is True

        with pytest.raises(AppError):
            await role_permission_repo.get_role_permission(role_id=role.id, permission_id=permission.id)


    @pytest.mark.run(order=5)
    async def test_delete_non_existent_role_permission(self):
        role_permission_repo = RolePermissionRepository()
        role_id = "non_existent_role"
        permission_id = "non_existent_permission"
        with pytest.raises(AppError):
            await role_permission_repo.delete_role_permission(role_id=role_id, permission_id=permission_id)


    @pytest.mark.run(order=6)
    async def test_create_duplicate_role_permission(self):
        role_repo = RoleRepository()
        permission_repo = PermissionRepository()
        role_permission_repo = RolePermissionRepository()

        role = await role_repo.create_role({"id": "role_id_some", "name": "Manager"})
        permission = await permission_repo.create_permission({"id": "permission_id_some", "name":"test"})
        role_permission_data = {
            "role_id":role.id,
            "permission_id":permission.id
        }
        await role_permission_repo.create_role_permission(role_permission_data=role_permission_data)

        with pytest.raises(AppError):
            await role_permission_repo.create_role_permission(role_permission_data=role_permission_data)
