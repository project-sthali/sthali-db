# import unittest

# from tests import clients
# from sthali_db.engines import base


# class MockBase(base.BaseEngine):
#     pass
#     # table = mock.Mock()
#     # path = ""

#     # __init__ = mock.Mock(return_value=None)

# class TestBaseEngine(unittest.IsolatedAsyncioTestCase):
#     def setUp(self) -> None:
#         path = ""
#         table = ""
#         self.engine = MockBase(path, table)

#     async def test_insert_one(self) -> None:
#         with self.assertRaises(NotImplementedError):
#             await self.engine.insert_one(clients.RESOURCE_ID, clients.RESOURCE_OBJ_WITHOUT_ID)

#     async def test_select_one(self) -> None:
#         with self.assertRaises(NotImplementedError):
#             await self.engine.select_one(clients.RESOURCE_ID)

#     async def test_update_one(self) -> None:
#         with self.assertRaises(NotImplementedError):
#             await self.engine.update_one(clients.RESOURCE_ID, clients.RESOURCE_OBJ_WITHOUT_ID)

#     async def test_delete_one(self) -> None:
#         with self.assertRaises(NotImplementedError):
#             await self.engine.delete_one(clients.RESOURCE_ID)

#     async def test_select_many(self) -> None:
#         with self.assertRaises(NotImplementedError):
#             await self.engine.select_many(base.PaginateParameters())
