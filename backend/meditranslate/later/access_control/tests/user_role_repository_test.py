# import sys
# sys.dont_write_bytecode = True

import pytest
from meditranslate.app.errors import AppError
from meditranslate.src.access_control.tests.access_control_test import AccessControlTest
from meditranslate.src.access_control.user_role_repository import UserRoleRepository
from meditranslate.src.access_control.role_repository import RoleRepository
from meditranslate.src.users.user_repository import UserRepository

@pytest.mark.run(after=['TestUserRepository','TestRoleRepository'])
@pytest.mark.asyncio(loop_scope="session")
class TestUserRoleRepository(AccessControlTest):

    @pytest.mark.run(order=1)
    async def test_create_user_role(self):
        user_repo = UserRepository()
        role_repo = RoleRepository()
        user = await user_repo.create_user({})
        role = await role_repo.create_role({"name":"role_name"})
        user_id = user.id
        role_id = role.id

        user_role_data = {
            "user_id": user_id,
            "role_id": role_id
        }

        repo = UserRoleRepository()
        user_role = await repo.create_user_role(user_role_data=user_role_data)
        assert user_role is not None
        assert user_role.user_id == user_role_data["user_id"]
        assert user_role.role_id == user_role_data["role_id"]

    @pytest.mark.run(order=2)
    async def test_get_user_role(self):
        user_repo = UserRepository()
        role_repo = RoleRepository()
        user = await user_repo.create_user({})
        role = await role_repo.create_role({"name":"role_name"})
        user_id = user.id
        role_id = role.id

        repo = UserRoleRepository()

        user_role = await repo.create_user_role(user_role_data={"user_id": user_id, "role_id": role_id})
        fetched_user_role = await repo.get_user_role(user_id=user_id, role_id=role_id)

        assert fetched_user_role is not None
        assert fetched_user_role.user_id == user_id
        assert fetched_user_role.role_id == role_id

    @pytest.mark.run(order=3)
    async def test_get_user_roles(self):
        user_repo = UserRepository()
        role_repo = RoleRepository()
        user = await user_repo.create_user({})
        role = await role_repo.create_role({"name":"role_name"})
        user_id = user.id
        role_id = role.id

        role_2 = await role_repo.create_role({"name":"role_name_2"})
        role_2_id = role_2.id

        repo = UserRoleRepository()
        await repo.create_user_role(user_role_data={"user_id": user_id, "role_id": role_id})
        await repo.create_user_role(user_role_data={"user_id": user_id, "role_id": role_2_id})

        # Fetch user roles
        roles = await repo.get_user_roles(user_id=user_id)
        assert roles is not None
        assert len(roles) == 2
        role_ids = [role.id for role in roles]
        assert role_id in role_ids
        assert role_2_id in role_ids

    @pytest.mark.run(order=4)
    async def test_delete_user_role(self):
        user_repo = UserRepository()
        role_repo = RoleRepository()
        user = await user_repo.create_user({})
        role = await role_repo.create_role({"name":"role_name"})
        user_id = user.id
        role_id = role.id

        repo = UserRoleRepository()
        await repo.create_user_role(user_role_data={"user_id": user_id, "role_id": role_id})
        user_role = await repo.get_user_role(user_id=user_id, role_id=role_id)
        assert user_role is not None
        result = await repo.delete_user_role(user_id=user_id, role_id=role_id)
        assert result is True

        with pytest.raises(AppError):
            await repo.get_user_role(user_id=user_id, role_id=role_id)

    @pytest.mark.run(order=5)
    async def test_delete_non_existent_user_role(self):
        user_id = "non_existent_user"
        role_id = "non_existent_role"
        repo = UserRoleRepository()

        with pytest.raises(AppError):
            await repo.delete_user_role(user_id=user_id, role_id=role_id)



    @pytest.mark.run(order=6)
    async def test_get_role_users(self):
        user_repo = UserRepository()
        role_repo = RoleRepository()
        user = await user_repo.create_user({})
        user_2 = await user_repo.create_user({})
        role = await role_repo.create_role({"name":"role_name"})
        user_id = user.id
        user_2_id = user_2.id
        role_id = role.id


        repo = UserRoleRepository()

        # Create some users for the role
        await repo.create_user_role(user_role_data={"user_id": user_id, "role_id": role_id})
        await repo.create_user_role(user_role_data={"user_id": user_2_id, "role_id": role_id})

        # Fetch users associated with the role
        users = await repo.get_role_users(role_id=role_id)
        assert users is not None
        assert len(users) == 2
        user_ids = [user.id for user in users]
        assert user_2_id in user_ids
        assert user_id in user_ids

    @pytest.mark.run(order=7)
    async def test_create_duplicate_user_role(self):
        user_repo = UserRepository()
        role_repo = RoleRepository()
        user = await user_repo.create_user({})
        role = await role_repo.create_role({"name":"role_name"})
        user_id = user.id
        role_id = role.id

        user_role_data = {
            "user_id": user_id,
            "role_id": role_id
        }
        repo = UserRoleRepository()

        await repo.create_user_role(user_role_data=user_role_data)

        with pytest.raises(AppError):
            await repo.create_user_role(user_role_data=user_role_data)
