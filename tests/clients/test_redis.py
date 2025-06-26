import unittest

import sthali_db.clients.redis

module = sthali_db.clients.redis

class TestRedisClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = module.RedisClient("test_path", "test_table")
        self.resource_id: module.ResourceId = module.ResourceId.__metadata__[0].default_factory()  # type: ignore
        self.resource_obj: module.ResourceObj = {}

    async def test_insert_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.client.insert_one(self.resource_id, self.resource_obj)

    async def test_select_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.client.select_one(self.resource_id)

    async def test_update_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.client.update_one(self.resource_id, self.resource_obj)

    async def test_delete_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.client.delete_one(self.resource_id)

    async def test_select_many(self) -> None:
        paginate_parameters = module.dependencies.PaginateParameters()  # type: ignore

        with self.assertRaises(NotImplementedError):
            await self.client.select_many(paginate_parameters)
