import unittest
import unittest.mock

import sthali_db.clients.default

module = sthali_db.clients.default

class TestDefaultClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = module.DefaultClient("", "test_table")
        self.resource_id: module.ResourceId  = module.ResourceId.__metadata__[0].default_factory()  # type: ignore

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_insert_one(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        result = await self.client.insert_one(self.resource_id, {"field_1": "value_1", "field_2": "value_2"})

        self.assertEqual(result, {"id": self.resource_id, "field_1": "value_1", "field_2": "value_2"})

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_insert_one_raise_exception(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.return_value = {"field_1": "value_1", "field_2": "value_2"}

        with self.assertRaises(self.client.exception) as context:
            await self.client.insert_one(self.resource_id, {"field_1": "value_1", "field_2": "value_2"})

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_409_CONFLICT)

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_select_one(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.return_value = {"field_1": "value_1", "field_2": "value_2"}

        result = await self.client.select_one(self.resource_id)
        self.assertEqual(result, {"id": self.resource_id, "field_1": "value_1", "field_2": "value_2"})

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_select_one_raise_exception(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.select_one(self.resource_id)

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_update_one(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.return_value = {"field_1": "value_1", "field_2": "value_2"}

        result = await self.client.update_one(self.resource_id, {"field_1": "new_value_1"})

        self.assertEqual(result, {"id": self.resource_id, "field_1": "new_value_1"})

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_update_one_partial(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.return_value = {"field_1": "value_1", "field_2": "value_2"}
        partial = True

        result = await self.client.update_one(self.resource_id, {"field_1": "new_value_1"}, partial)

        self.assertEqual(result, {"id": self.resource_id, "field_1": "new_value_1", "field_2": "value_2"})

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_update_one_raise_exception(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.update_one(self.resource_id, {"field_1": "new_value_1", "field_2": "value_2"})

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_delete_one(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.return_value = {"field_1": "value_1", "field_2": "value_2"}

        result = await self.client.delete_one(self.resource_id)
        self.assertIsNone(result)

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient._get")
    async def test_delete_one_not_found(self, mocked_get: unittest.mock.MagicMock) -> None:
        mocked_get.side_effect = self.client.exception(self.client.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.client.exception) as context:
            await self.client.delete_one(self.resource_id)

        self.assertEqual(context.exception.status_code, self.client.status.HTTP_404_NOT_FOUND)

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient._db")
    async def test_select_many(self, mocked_db: unittest.mock.MagicMock) -> None:
        mocked_db.items.return_value = {self.resource_id: {"field_1": "value_1", "field_2": "value_2"}}.items()
        paginate_parameters = module.dependencies.PaginateParameters()  # type: ignore

        result = await self.client.select_many(paginate_parameters)

        self.assertEqual(result, [{"id": self.resource_id, "field_1": "value_1", "field_2": "value_2"}])

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient._db")
    async def test_select_many_paginated(self, mocked_db: unittest.mock.MagicMock) -> None:
        mocked_db.items.return_value = {
            1: {"field_1": "value_1"},
            2: {"field_1": "value_2"},
            3: {"field_1": "value_3"},
        }.items()
        paginate_parameters = module.dependencies.PaginateParameters(skip=1, limit=1)

        result = await self.client.select_many(paginate_parameters)

        self.assertEqual(result, [{"id": 2, "field_1": "value_2"}])
