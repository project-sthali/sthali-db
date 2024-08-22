from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch
from uuid import uuid4

from sthali_db.clients.default import DefaultClient, PaginateParameters, ResourceId


class TestDefaultClient(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = DefaultClient(_="", table_name="test_table")
        self.resource_id: ResourceId = uuid4()

    @patch("sthali_db.clients.default.DefaultClient._get")
    async def test_insert_one(self, mocked_get: MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        result = await self.client.insert_one(self.resource_id, {"field1": "value1", "field2": "value2"})

        self.assertEqual(result, {"id": self.resource_id, "field1": "value1", "field2": "value2"})

    @patch("sthali_db.clients.default.DefaultClient._get")
    async def test_insert_one_raise_exception(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}

        with self.assertRaises(self.client.exception) as context:
            await self.client.insert_one(self.resource_id, {"field1": "value1", "field2": "value2"})

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_409_CONFLICT)

    @patch("sthali_db.clients.default.DefaultClient._get")
    async def test_select_one(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}

        result = await self.client.select_one(self.resource_id)
        self.assertEqual(result, {"id": self.resource_id, "field1": "value1", "field2": "value2"})

    @patch("sthali_db.clients.default.DefaultClient._get")
    async def test_select_one_raise_exception(self, mocked_get: MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.select_one(self.resource_id)

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    @patch("sthali_db.clients.default.DefaultClient._get")
    async def test_update_one(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}

        result = await self.client.update_one(self.resource_id, {"field1": "new_value1"})

        self.assertEqual(result, {"id": self.resource_id, "field1": "new_value1"})

    @patch("sthali_db.clients.default.DefaultClient._get")
    async def test_update_one_partial(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}
        partial = True

        result = await self.client.update_one(self.resource_id, {"field1": "new_value1"}, partial)

        self.assertEqual(result, {"id": self.resource_id, "field1": "new_value1", "field2": "value2"})

    @patch("sthali_db.clients.default.DefaultClient._get")
    async def test_update_one_raise_exception(self, mocked_get: MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.update_one(self.resource_id, {"field1": "new_value1", "field2": "value2"})

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    @patch("sthali_db.clients.default.DefaultClient._get")
    async def test_delete_one(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}

        result = await self.client.delete_one(self.resource_id)
        self.assertIsNone(result)

    @patch("sthali_db.clients.default.DefaultClient._get")
    async def test_delete_one_not_found(self, mocked_get: MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.delete_one(self.resource_id)

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    @patch("sthali_db.clients.default.DefaultClient._db")
    async def test_select_many(self, mocked_db: MagicMock) -> None:
        mocked_db.items.return_value = {self.resource_id: {"field1": "value1", "field2": "value2"}}.items()
        paginate_parameters = PaginateParameters()  # type: ignore

        result = await self.client.select_many(paginate_parameters)

        self.assertEqual(result, [{"id": self.resource_id, "field1": "value1", "field2": "value2"}])

    @patch("sthali_db.clients.default.DefaultClient._db")
    async def test_select_many_paginated(self, mocked_db: MagicMock) -> None:
        mocked_db.items.return_value = {1: {"field1": "1"}, 2: {"field1": "2"}, 3: {"field1": "3"}}.items()
        paginate_parameters = PaginateParameters(skip=1, limit=1)

        result = await self.client.select_many(paginate_parameters)

        self.assertEqual(result, [{"id": 2, "field1": "2"}])
