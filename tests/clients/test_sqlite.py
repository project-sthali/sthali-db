from unittest import IsolatedAsyncioTestCase
from uuid import uuid4

from sthali_db.clients.sqlite import ResourceId, ResourceObj, SQLiteClient


class TestsqliteClient(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = SQLiteClient("path", "table")
        self.resource_id: ResourceId = uuid4()
        self.resource_obj: ResourceObj = {}

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
        with self.assertRaises(NotImplementedError):
            await self.client.select_many({})
