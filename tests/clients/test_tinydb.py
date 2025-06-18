import unittest
import unittest.mock

import sthali_db.clients.tinydb

module = sthali_db.clients.tinydb


class TestTinydbClient(unittest.IsolatedAsyncioTestCase):
    @unittest.mock.patch("sthali_db.clients.tinydb.tinydb.TinyDB")
    def setUp(self, mocked_tinydb: unittest.mock.MagicMock) -> None:
        mocked_tinydb.return_value = unittest.mock.MagicMock()
        self.resource_id: module.ResourceId  = module.ResourceId.__metadata__[0].default_factory()  # type: ignore
        client = module.TinydbClient(path="test_db.json", table_name="test_table")
        self.client = client

    @unittest.mock.patch("sthali_db.clients.tinydb.TinydbClient._get")
    async def test_insert_one(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        result = await self.client.insert_one(self.resource_id, {"field_1": "value_1", "field_2": "value_2"})

        self.assertEqual(result, {"id": self.resource_id, "field_1": "value_1", "field_2": "value_2"})

    @unittest.mock.patch("sthali_db.clients.tinydb.TinydbClient._get")
    async def test_insert_one_raise_exception(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.return_value = {"field_1": "value_1", "field_2": "value_2"}

        with self.assertRaises(self.client.exception) as context:
            await self.client.insert_one(self.resource_id, {"field_1": "value_1", "field_2": "value_2"})

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_409_CONFLICT)

    @unittest.mock.patch("sthali_db.clients.tinydb.TinydbClient._get")
    async def test_select_one(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.return_value = {"field_1": "value_1", "field_2": "value_2"}

        result = await self.client.select_one(self.resource_id)

        self.assertEqual(result, {"id": self.resource_id, "field_1": "value_1", "field_2": "value_2"})

    @unittest.mock.patch("sthali_db.clients.tinydb.TinydbClient._get")
    async def test_select_one_raise_exception(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.select_one(self.resource_id)

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    @unittest.mock.patch("sthali_db.clients.tinydb.TinydbClient._get")
    async def test_update_one(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.return_value = {"field_1": "value_1", "field_2": "value_2"}

        result = await self.client.update_one(self.resource_id, {"field_1": "new_value_1"})

        self.assertEqual(result, {"id": self.resource_id, "field_1": "new_value_1"})

    @unittest.mock.patch("sthali_db.clients.tinydb.TinydbClient._get")
    async def test_update_one_partial(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.return_value = {"field_1": "value_1", "field_2": "value_2"}
        partial = True

        result = await self.client.update_one(self.resource_id, {"field_1": "new_value_1"}, partial)

        self.assertEqual(result, {"id": self.resource_id, "field_1": "new_value_1", "field_2": "value_2"})

    @unittest.mock.patch("sthali_db.clients.tinydb.TinydbClient._get")
    async def test_update_one_raise_exception(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.update_one(self.resource_id, {"field_1": "new_value_1", "field_2": "value_2"})

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    @unittest.mock.patch("sthali_db.clients.tinydb.TinydbClient._get")
    async def test_delete_one(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.return_value = {"field_1": "value_1", "field_2": "value_2"}

        result = await self.client.delete_one(self.resource_id)
        self.assertIsNone(result)

    @unittest.mock.patch("sthali_db.clients.tinydb.TinydbClient._get")
    async def test_delete_one_not_found(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.delete_one(self.resource_id)

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    async def test_select_many(self) -> None:
        self.client.table.all = unittest.mock.MagicMock(
            return_value=[
                {"resource_id": self.resource_id, "resource_obj": {"field_1": "value_1", "field_2": "value_2"}}
            ]
        )
        paginate_parameters = module.dependencies.PaginateParameters()  # type: ignore

        result = await self.client.select_many(paginate_parameters)

        self.assertEqual(result, [{"id": self.resource_id, "field_1": "value_1", "field_2": "value_2"}])

    async def test_select_many_paginated(self) -> None:
        self.client.table.all = unittest.mock.MagicMock(
            return_value=[
                {"resource_id": self.resource_id, "resource_obj": {"field_1": "value_1", "field_2": "value_2"}}
            ]
        )
        paginate_parameters = module.dependencies.PaginateParameters(skip=1, limit=1)

        result = await self.client.select_many(paginate_parameters)

        self.assertEqual(result, [])
