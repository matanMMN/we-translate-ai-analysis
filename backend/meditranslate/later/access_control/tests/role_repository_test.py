# import sys
# sys.dont_write_bytecode = True

from meditranslate.app.shared.constants import SortOrder
import pytest
from meditranslate.src.access_control.role_repository import RoleRepository
from meditranslate.app.errors import AppError
from meditranslate.src.access_control.tests.access_control_test import AccessControlTest

# @pytest.mark.run(after='')
@pytest.mark.asyncio(loop_scope="session")
class TestRoleRepository(AccessControlTest):

    # @pytest.mark.profile
    @pytest.mark.run(order=1)
    async def test_create_role(self):
        role_data = {
            "id": "role123",
            "name": "Admin"
        }
        repo = RoleRepository()
        role = await repo.create_role(role_data=role_data)
        assert role is not None
        assert role.id == role_data["id"]
        assert role.name == role_data["name"]

    @pytest.mark.run(order=2)
    async def test_get_role(self):
        role_id = "role123"
        repo = RoleRepository()

        # Create role first
        await repo.create_role({"id": role_id, "name": "Admin"})

        # Retrieve the created role
        role = await repo.get_role(role_id=role_id)
        assert role is not None
        assert role.id == role_id
        assert role.name == "Admin"

    @pytest.mark.run(order=3)
    async def test_update_role(self):
        role_id = "role123"
        repo = RoleRepository()

        # Create role first
        await repo.create_role({"id": role_id, "name": "Admin"})

        # Update role name
        updated_data = {"name": "Super Admin"}
        updated_role = await repo.update_role(role_id=role_id, role_update_data=updated_data)
        assert updated_role is not None
        assert updated_role.name == updated_data["name"]

    @pytest.mark.run(order=4)
    async def test_delete_role(self):
        role_id = "role_to_delete"
        repo = RoleRepository()

        # Create role first
        await repo.create_role({"id": role_id, "name": "To Be Deleted"})

        # Ensure it exists
        role = await repo.get_role(role_id=role_id)
        assert role is not None

        # Delete role
        result = await repo.delete_role(role_id=role_id)
        assert result is True

        # Ensure it's deleted
        with pytest.raises(AppError):
            await repo.get_role(role_id=role_id)


    @pytest.mark.run(order=5)
    async def test_delete_non_existent_role(self):
        role_id = "non_existent_role"
        repo = RoleRepository()

        # Attempt to delete a role that doesn't exist
        with pytest.raises(AppError):
            await repo.delete_role(role_id=role_id)


    @pytest.mark.run(order=6)
    async def test_create_duplicate_role(self):
        role_data = {
            "id": "duplicate_role",
            "name": "Manager"
        }
        repo = RoleRepository()

        # Create the role for the first time
        await repo.create_role(role_data=role_data)

        # Try to create the same role again, expect an exception
        with pytest.raises(AppError):  # Assuming AppError is raised for duplicates
            await repo.create_role(role_data=role_data)

    @pytest.mark.run(order=7)
    async def test_get_many_roles(self):
        repo = RoleRepository()

        # Create some roles
        role_data_list = [
            {"id": "role1", "name": "Admin"},
            {"id": "role2", "name": "Manager"},
            {"id": "role3", "name": "User"}
        ]
        for role_data in role_data_list:
            await repo.create_role(role_data)

        schema = {
            "offset": 0,
            "limit": 10,
            "sort_by": "name",
            "sort_order": SortOrder.asc
        }

        # Fetch roles with schema
        roles = await repo.get_many_roles(schema=schema)
        assert roles is not None
        assert len(roles) == len(role_data_list)

        # Check if the roles match the expected data
        role_names = [role.name for role in roles]
        expected_names = sorted([role_data["name"] for role_data in role_data_list])
        assert role_names == expected_names
