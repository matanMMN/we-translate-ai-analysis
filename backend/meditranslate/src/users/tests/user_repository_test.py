# import sys
# sys.dont_write_bytecode = True

from meditranslate.app.loggers import logger
from meditranslate.app.shared.schemas import SortOrder
import pytest
from meditranslate.src.users.user_repository import UserRepository
from meditranslate.app.errors import AppError
from meditranslate.src.users.tests.user_test import UserTest
from faker import Faker

fake = Faker()

# @pytest.mark.run(after='')
@pytest.mark.asyncio(loop_scope="session")
class TestUserRepository(UserTest):

    # @pytest.mark.profile
    @pytest.mark.run(order=0)
    async def test_create_user(self):
        user_data = {
            "email":fake.email(),
            "username":fake.user_name(),
            "hashed_password":fake.password(),
        }
        repo = UserRepository(self.session)
        user = await repo.create(user_data)
        logger.info("USER:")
        logger.info(user)
        assert user is not None
        return user


    @pytest.mark.run(order=1)
    async def test_get_user(self):
        repo = UserRepository(self.session)
        user_data = {
            "email":fake.email(),
            "username":fake.user_name(),
            "hashed_password":fake.password(),
        }
        user = await repo.create(user_data)
        new_user_id = user.id
        fetch_user = await repo.get_by("id",new_user_id,unique=True)
        assert fetch_user is not None
        assert fetch_user.id == new_user_id

    @pytest.mark.run(order=3)
    async def test_delete_user(self):
        repo = UserRepository(self.session)
        user_data = {
            "email":fake.email(),
            "username":fake.user_name(),
            "hashed_password":fake.password(),
        }
        user = await repo.create(user_data)
        new_user_id = user.id
        await repo.delete(user)
        old_user = await repo.get_by("id",new_user_id,unique=True)
        assert old_user is None


    @pytest.mark.run(order=3)
    async def test_update_user(self):
        repo = UserRepository(self.session)
        user_data = {
            "email":fake.email(),
            "username":fake.user_name(),
            "hashed_password":fake.password(),
        }
        user = await repo.create(user_data)
        new_user_id = user.id
        old_first_name = user.first_name
        new_name = fake.name()
        user_update_data = {
            "first_name":new_name,
        }
        updated_user = await repo.update(user,user_update_data)
        assert updated_user is not None
        assert updated_user.id == new_user_id
        assert old_first_name == None
        assert old_first_name !=  new_name
        assert updated_user.first_name == new_name



    # @pytest.mark.run(order=4)
    # async def test_get_many_users(self):
    #     new_users = []
    #     sort_by = "first_name"
    #     limit = 11
    #     offset = 5
    #     filters = None
    #     sort_order = SortOrder.desc

    #     # Create new users with and without first_name
    #     for i in range(10):
    #         new_user = {
    #             "id": f"1000000000000000000000000000000000{i}",
    #             "first_name": f"user_{i}" if i != 0 else None  # Ensure None for first user
    #         }
    #         new_users.append(new_user)

    #     # Create users in the database
    #     for new_user in new_users:
    #         await UserRepository().create_user(new_user)

    #     schema = {
    #         "offset": offset,
    #         "limit": limit,
    #         "sort_by": sort_by,
    #         "sort_order": sort_order,
    #         "filters": filters
    #     }

    #     # Get users from repository
    #     users,total = await UserRepository().get_many_users(schema=schema)

    #     # Prepare actual users list
    #     logger.info(users)
    #     actual_users = [{"first_name": user.first_name, "id": user.id} for user in users if user.first_name]

    #     # Prepare expected users list
    #     expected_users = [
    #         {"id": user['id'], "first_name": user.get('first_name', "")}  # Use .get() to avoid KeyError
    #         for user in new_users
    #     ]

    #     # Sort the expected users
    #     expected_users.sort(
    #         key=lambda u: (u['first_name'] is None, u['first_name']),  # Place None last
    #         reverse=(sort_order == SortOrder.desc)  # Handle sort order
    #     )


    #     expected_users = expected_users[offset:offset + limit]
    #     # for user in new_users:
    #     #     await UserRepository().delete_user(user_id=user['id'])
    #     assert actual_users == expected_users
    #     assert len(actual_users) <= limit



    # @pytest.mark.run(order=0)
    # async def test_delete_non_existent_user(self):
    #     user_id = "non_existent_user_id1234567891234567"
    #     with pytest.raises(AppError):
    #         await UserRepository().delete_user(user_id=user_id)



    # @pytest.mark.run(order=0)
    # async def test_update_non_existent_user(self):
    #     user_id = "non_existent_user_id1234567891234567"
    #     update_data = {
    #         "first_name": "Updated Name"
    #     }
    #     with pytest.raises(AppError) as excinfo:  # Adjust exception type as needed
    #         await UserRepository().update_user(user_id=user_id, update_data=update_data)
    #     #     raise ExceptionGroup(
    #     #         "Group message",
    #     #         [
    #     #             RuntimeError("Exception 123 raised"),
    #     #         ],
    #     #     )
    #     # assert excinfo.group_contains(RuntimeError, match=r".* 123 .*")
    #     # assert not excinfo.group_contains(TypeError)



    # @pytest.mark.run(order=1)
    # async def test_create_user_with_duplicate_id(self):
    #     user_data = {
    #         "id": "123456789123456789a23456782123560789",
    #         "username": "hello"
    #     }
    #     repo = UserRepository()
    #     await repo.create_user(user_data=user_data)  # Create user first time
    #     with pytest.raises(AppError):  # Assuming ValueError is raised for duplicate IDs
    #         await repo.create_user(user_data=user_data)
    #     # await repo.delete_user(user_data['id'])




    # @pytest.mark.run(order=6)
    # async def test_get_many_users_with_filters(self):
    #     new_users = []
    #     for i in range(10):
    #         new_user = {
    #             "id": f"1000000000000000000000000000000000{i}",
    #             "first_name": f"user_{i}" if i % 2 == 0 else None  # Only even indexed users have first_name
    #         }
    #         new_users.append(new_user)

    #     for new_user in new_users:
    #         await UserRepository().create_user(new_user)

    #     schema = {
    #         "offset": 0,
    #         "limit": 10,
    #         "sort_by": "first_name",
    #         "sort_order": SortOrder.asc,
    #         "filters": {"first_name": {"$not_null": True}}
    #     }
    #     with pytest.raises(AppError):
    #         users = await UserRepository().get_many_users(schema=schema)

    #         actual_users = [{"first_name": user.first_name, "id": user.id} for user in users if user.first_name]
    #         expected_users = sorted(
    #             [{"id": user['id'], "first_name": user['first_name']} for user in new_users if user.get('first_name') is not None],
    #             key=lambda u: u['first_name']
    #         )
    #         assert actual_users == expected_users




    # @pytest.mark.run(order=9)
    # async def test_get_many_users_with_limit_exceeding(self):
    #     new_users = []
    #     for i in range(10):
    #         new_user = {
    #             "id": f"1000000000000000000000000000000000{i}",
    #             "first_name": f"user_{i}"
    #         }
    #         new_users.append(new_user)

    #     for new_user in new_users:
    #         await UserRepository().create_user(new_user)

    #     schema = {
    #         "offset": 0,
    #         "limit": 20,  # Limit exceeds the number of created users
    #         "sort_by": "first_name",
    #         "sort_order": SortOrder.asc,
    #         "filters": None
    #     }

    #     users,total = await UserRepository().get_many_users(schema=schema)

    #     actual_users = [{"first_name": user.first_name, "id": user.id} for user in users]
    #     actual_users.sort(key=lambda u: u['id'])
    #     assert total == len(new_users)
    #     assert new_users == actual_users
