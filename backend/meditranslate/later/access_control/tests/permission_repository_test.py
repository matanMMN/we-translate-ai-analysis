# # import sys
# # sys.dont_write_bytecode = True

# import pytest
# from wetranslateai.app.shared.constants import SortOrder
# from wetranslateai.app.errors import AppError
# from wetranslateai.src.access_control.permission_repository import PermissionRepository
# from wetranslateai.src.access_control.tests.access_control_test import AccessControlTest

# @pytest.mark.run(after=[''])
# @pytest.mark.asyncio(loop_scope="session")
# class TestPermissionRepository(AccessControlTest):

#     @pytest.mark.run(order=1)
#     async def test_create_permission(self):
#         permission_data = {
#             "id": "permission123",
#             "name":"name",
#         }
#         repo = PermissionRepository()
#         permission = await repo.create_permission(permission_data=permission_data)
#         assert permission is not None
#         assert permission.id == permission_data["id"]
#         assert permission.name == permission_data["name"]

#     @pytest.mark.run(order=2)
#     async def test_get_permission(self):
#         permission_id = "permission123"
#         repo = PermissionRepository()
#         new_permission = await repo.create_permission({"id": permission_id, "name": "read"})
#         permission = await repo.get_permission(permission_id=new_permission.id)
#         assert permission is not None
#         assert permission.id == permission_id

#     @pytest.mark.run(order=3)
#     async def test_update_permission(self):
#         permission_id = "permission123"
#         repo = PermissionRepository()
#         new_permission = await repo.create_permission({"id": permission_id, "name": "read"})
#         updated_data = {
#             "name": "new_per_name"
#         }
#         updated_permission = await repo.update_permission(permission_id=new_permission.id, permission_update_data=updated_data)
#         assert updated_permission is not None
#         assert updated_permission.name == updated_data["name"]

#     @pytest.mark.run(order=4)
#     async def test_delete_permission(self):
#         permission_id = "permission_to_delete"
#         repo = PermissionRepository()

#         with pytest.raises(AppError):
#             await repo.get_permission(permission_id=permission_id)



#         new_permission = await repo.create_permission({"id": permission_id, "name": "namename"})
#         permission = await repo.get_permission(permission_id=new_permission.id)
#         assert permission is not None

#         result = await repo.delete_permission(permission_id=permission_id)
#         assert result is True

#         with pytest.raises(AppError):
#             await repo.get_permission(permission_id=permission_id)


#     @pytest.mark.run(order=5)
#     async def test_delete_non_existent_permission(self):
#         permission_id = "non_existent_permission"
#         repo = PermissionRepository()
#         with pytest.raises(AppError):
#             await repo.get_permission(permission_id=permission_id)
#         with pytest.raises(AppError):
#             await repo.delete_permission(permission_id=permission_id)

#     @pytest.mark.run(order=6)
#     async def test_create_duplicate_permission(self):
#         permission_data = {
#             "id": "duplicate_permission",
#             "name": "read",
#         }
#         repo = PermissionRepository()

#         await repo.create_permission(permission_data=permission_data)

#         with pytest.raises(AppError):
#             await repo.create_permission(permission_data=permission_data)

#     @pytest.mark.run(order=7)
#     async def test_get_many_permissions(self):
#         limit = 2
#         offset = 0
#         sort_order = SortOrder.asc
#         repo = PermissionRepository()

#         # Create some permissions
#         permission_data_list = [
#             {"id": "permission1", "name": "read"},
#             {"id": "permission2", "name": "write"},
#             {"id": "permission3", "name": "delete"}
#         ]
#         for permission_data in permission_data_list:
#             await repo.create_permission(permission_data)

#         schema = {
#             "offset": offset,
#             "limit": limit,
#             "sort_by": "id",
#             "sort_order": sort_order,
#             "filters":{
#                 # "name":"regex:^rea+$"
#             }
#         }

#         permissions,total = await repo.get_many_permissions(schema=schema)
#         assert permissions is not None
#         assert len(permissions) == limit
#         assert len(permission_data_list) == total

#         permission_ids = [permission.id for permission in permissions]
#         expected_ids = sorted(
#             [permission_data["id"] for permission_data in permission_data_list],
#             reverse=(sort_order == SortOrder.desc)
#         )[offset:offset + limit]
#         assert permission_ids == expected_ids
