from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch
from uuid import uuid4

from sthali_db.clients.tinydb import PaginateParameters, ResourceId, TinyDBClient


class TestTinyDBClient(IsolatedAsyncioTestCase):
    @patch("sthali_db.clients.tinydb.TinyDB")
    def setUp(self, mocked_tinydb: MagicMock) -> None:
        mocked_tinydb.return_value = MagicMock()

        self.resource_id: ResourceId = uuid4()
        client = TinyDBClient(path="test_db.json", table_name="test_table")
        self.client = client

    @patch("sthali_db.clients.tinydb.TinyDBClient._get")
    async def test_insert_one(self, mocked_get: MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        result = await self.client.insert_one(self.resource_id, {"field1": "value1", "field2": "value2"})

        self.assertEqual(result, {"id": self.resource_id, "field1": "value1", "field2": "value2"})

    @patch("sthali_db.clients.tinydb.TinyDBClient._get")
    async def test_insert_one_raise_exception(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}

        with self.assertRaises(self.client.exception) as context:
            await self.client.insert_one(self.resource_id, {"field1": "value1", "field2": "value2"})

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_409_CONFLICT)

    @patch("sthali_db.clients.tinydb.TinyDBClient._get")
    async def test_select_one(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}

        result = await self.client.select_one(self.resource_id)

        self.assertEqual(result, {"id": self.resource_id, "field1": "value1", "field2": "value2"})

    @patch("sthali_db.clients.tinydb.TinyDBClient._get")
    async def test_select_one_raise_exception(self, mocked_get: MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.select_one(self.resource_id)

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    @patch("sthali_db.clients.tinydb.TinyDBClient._get")
    async def test_update_one(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}

        result = await self.client.update_one(self.resource_id, {"field1": "new_value1"})

        self.assertEqual(result, {"id": self.resource_id, "field1": "new_value1"})

    @patch("sthali_db.clients.tinydb.TinyDBClient._get")
    async def test_update_one_partial(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}
        partial = True

        result = await self.client.update_one(self.resource_id, {"field1": "new_value1"}, partial)

        self.assertEqual(result, {"id": self.resource_id, "field1": "new_value1", "field2": "value2"})

    @patch("sthali_db.clients.tinydb.TinyDBClient._get")
    async def test_update_one_raise_exception(self, mocked_get: MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.update_one(self.resource_id, {"field1": "new_value1", "field2": "value2"})

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    @patch("sthali_db.clients.tinydb.TinyDBClient._get")
    async def test_delete_one(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}

        result = await self.client.delete_one(self.resource_id)
        self.assertIsNone(result)

    @patch("sthali_db.clients.tinydb.TinyDBClient._get")
    async def test_delete_one_not_found(self, mocked_get: MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.delete_one(self.resource_id)

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    async def test_select_many(self) -> None:
        self.client.table.all = MagicMock(
            return_value=[{"resource_id": self.resource_id, "resource_obj": {"field1": "value1", "field2": "value2"}}]
        )
        paginate_parameters = PaginateParameters()  # type: ignore

        result = await self.client.select_many(paginate_parameters)

        self.assertEqual(result, [{"id": self.resource_id, "field1": "value1", "field2": "value2"}])

    async def test_select_many_paginated(self) -> None:
        self.client.table.all = MagicMock(
            return_value=[{"resource_id": self.resource_id, "resource_obj": {"field1": "value1", "field2": "value2"}}]
        )
        paginate_parameters = PaginateParameters(skip=1, limit=1)

        result = await self.client.select_many(paginate_parameters)

        self.assertEqual(result, [])
