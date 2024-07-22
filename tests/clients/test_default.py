from unittest import IsolatedAsyncioTestCase, mock
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from sthali_db.clients import default


class TestDefaultClient(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = default.DefaultClient(_="", table="table")
        self.resource_id: default.ResourceId = uuid4()

    @mock.patch("sthali_db.clients.default.DefaultClient._db")
    @mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_insert_one(self, mocked_get: MagicMock, mocked_db: MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)
        mocked_db.return_value = {}

        result = await self.client.insert_one(self.resource_id, {"field1": "value1", "field2": "value2"})

        self.assertEqual(result, {"id": self.resource_id, **{"field1": "value1", "field2": "value2"}})

    @mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_insert_one_raise_exception(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}

        with self.assertRaises(self.client.exception) as context:
            await self.client.insert_one(self.resource_id, {"field1": "value1", "field2": "value2"})

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_409_CONFLICT)

    @mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_select_one(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}

        result = await self.client.select_one(self.resource_id)
        self.assertEqual(result, {"id": self.resource_id, **{"field1": "value1", "field2": "value2"}})

    @mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_select_one_raise_exception(self, mocked_get: MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.select_one(self.resource_id)

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    @mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_update_one(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}

        result = await self.client.update_one(self.resource_id, {"field1": "new_value1"})

        self.assertEqual(result, {"id": self.resource_id, **{"field1": "new_value1"}})

    @mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_update_one_partial(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = {"field1": "value1", "field2": "value2"}
        partial = True

        result = await self.client.update_one(self.resource_id, {"field1": "new_value1"}, partial)

        self.assertEqual(result, {"id": self.resource_id, **{"field1": "new_value1", "field2": "value2"}})

    @mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_update_one_raise_exception(self, mocked_get: MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.update_one(self.resource_id, {"field1": "new_value1", "field2": "new_value2"})

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    # # # @mock.patch("src.sthali_db.clients.default.Defaultengine._get")
    # # # async def test_delete_one(self, mock_get):
    # # #     mock_get.return_value = PAYLOAD_WITHOUT_ID

    # # #     result = await self.engine.delete_one(ID)
    # # #     self.assertIsNone(result)

    # # # async def test_delete_one_not_found(self):
    # # #     with self.assertRaises(self.engine.exception) as context:
    # # #         await self.engine.delete_one(ID)

    # # #     self.assertEqual(context.exception.status_code, self.engine.status.HTTP_404_NOT_FOUND)

    # # # @mock.patch("src.sthali_db.clients.default.Defaultengine.db")
    # # # async def test_select_many(self, mock_db):
    # # #     mock_db.items.return_value = [(ID, PAYLOAD_WITHOUT_ID)]

    # # #     result = await self.engine.select_many()
    # # #     self.assertEqual(result, [PAYLOAD_WITH_ID])
