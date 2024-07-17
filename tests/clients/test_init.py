from unittest import IsolatedAsyncioTestCase, mock
from unittest.mock import AsyncMock
from uuid import uuid4

from sthali_db import clients


class TestBaseClient(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        result = clients.BaseClient(path="path", table="table")
        self.result = result

    async def test_return_default(self) -> None:
        self.assertEqual(self.result.exception, clients.HTTPException)
        self.assertEqual(self.result.status, clients.status)

    async def test_insert_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.result.insert_one(resource_id=uuid4(), resource_obj={})

    async def test_select_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.result.insert_one(resource_id=uuid4(), resource_obj={})

    async def test_update_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.result.insert_one(resource_id=uuid4(), resource_obj={})

    async def test_delete_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.result.insert_one(resource_id=uuid4(), resource_obj={})

    async def test_select_many_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.result.insert_one(resource_id=uuid4(), resource_obj={})


class TestDBSpecification(IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        result = clients.DBSpecification(path="path")  # type: ignore

        self.assertEqual(result.path, "path")
        self.assertEqual(result.client, "Default")

    async def test_return_custom(self) -> None:
        result = clients.DBSpecification(path="path", client="TinyDB")

        self.assertEqual(result.path, "path")
        self.assertEqual(result.client, "TinyDB")


class TestDBClient(IsolatedAsyncioTestCase):
    class MockClient:
        insert_one = AsyncMock(return_value="insert_one")
        select_one = AsyncMock(return_value="select_one")
        update_one = AsyncMock(return_value="update_one")
        delete_one = AsyncMock(return_value="delete_one")
        select_many = AsyncMock(return_value="select_many")

    @mock.patch("sthali_db.clients.default.DefaultClient")
    def setUp(self, mocked_client) -> None:
        mocked_client.return_value = self.MockClient()
        db_spec = clients.DBSpecification(path="path")  # type: ignore
        self.client = clients.DBClient(db_spec=db_spec, table="table")  # type: ignore

    async def test_return_default(self) -> None:
        self.assertTrue(isinstance(self.client.client, self.MockClient))

    async def test_select_one(self) -> None:
        result = await self.client.select_one()

        self.assertEqual(result, "select_one")

    async def test_update_one(self) -> None:
        result = await self.client.update_one()

        self.assertEqual(result, "update_one")

    async def test_delete_one(self) -> None:
        result = await self.client.delete_one()

        self.assertEqual(result, "delete_one")

    async def test_select_many(self) -> None:
        result = await self.client.select_many()

        self.assertEqual(result, "select_many")
