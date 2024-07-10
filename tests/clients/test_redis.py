# from unittest import IsolatedAsyncioTestCase

# from src.sthali_db.engines.redis import RedisEngine
# from tests import ID, PAYLOAD_WITHOUT_ID


# class TestBaseEngine(IsolatedAsyncioTestCase):
#     def setUp(self) -> None:
#         path = ""
#         table = "test_table"
#         self.engine = RedisEngine(path, table)

#     async def test_insert_one(self) -> None:
#         with self.assertRaises(NotImplementedError):
#             await self.engine.insert_one(ID, PAYLOAD_WITHOUT_ID)

#     async def test_select_one(self) -> None:
#         with self.assertRaises(NotImplementedError):
#             await self.engine.select_one(ID)

#     async def test_update_one(self) -> None:
#         with self.assertRaises(NotImplementedError):
#             await self.engine.update_one(ID, PAYLOAD_WITHOUT_ID)

#     async def test_delete_one(self) -> None:
#         with self.assertRaises(NotImplementedError):
#             await self.engine.delete_one(ID)

#     async def test_select_many(self) -> None:
#         with self.assertRaises(NotImplementedError):
#             await self.engine.select_many()
