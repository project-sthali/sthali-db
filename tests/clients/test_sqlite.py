import unittest
from uuid import uuid4

import sthali_db.clients.sqlite


class TestsqliteClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = sthali_db.clients.sqlite.SQLiteClient("test_path", "test_table")
        self.resource_id: sthali_db.clients.sqlite.ResourceId = uuid4()
        self.resource_obj: sthali_db.clients.sqlite.ResourceObj = {}

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
        paginate_parameters = sthali_db.clients.sqlite.dependencies.PaginateParameters()  # type: ignore

        with self.assertRaises(NotImplementedError):
            await self.client.select_many(paginate_parameters)
