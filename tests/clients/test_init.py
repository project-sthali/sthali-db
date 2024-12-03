import unittest
import unittest.mock
from uuid import uuid4

import sthali_db.clients


class TestBase(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        base = sthali_db.clients.Base("test_path", "test_table")
        self.base = base

    async def test_return_default(self) -> None:
        self.assertEqual(self.base.exception, sthali_db.clients.Base.exception)
        self.assertEqual(self.base.status, sthali_db.clients.Base.status)

    async def test_insert_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.insert_one(uuid4(), {})

    async def test_select_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.select_one(uuid4())

    async def test_update_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.update_one(uuid4(), {})

    async def test_delete_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.delete_one(uuid4())

    async def test_select_many_not_implemented(self) -> None:
        paginate_parameters = sthali_db.dependencies.PaginateParameters()  # type: ignore

        with self.assertRaises(NotImplementedError):
            await self.base.select_many(paginate_parameters)


class TestDBSpecification(unittest.IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        db_spec = sthali_db.clients.DBSpecification("test_path")  # type: ignore

        self.assertEqual(db_spec.path, "test_path")
        self.assertEqual(db_spec.client, "Default")

    async def test_return_custom(self) -> None:
        db_spec = sthali_db.clients.DBSpecification("test_path", "TinyDB")

        self.assertEqual(db_spec.path, "test_path")
        self.assertEqual(db_spec.client, "TinyDB")


class TestDB(unittest.IsolatedAsyncioTestCase):
    class MockDefaultClient:
        insert_one = unittest.mock.AsyncMock(return_value="insert_one")
        select_one = unittest.mock.AsyncMock(return_value="select_one")
        update_one = unittest.mock.AsyncMock(return_value="update_one")
        delete_one = unittest.mock.AsyncMock(return_value="delete_one")
        select_many = unittest.mock.AsyncMock(return_value="select_many")

    @unittest.mock.patch("sthali_db.clients.default.DefaultClient")
    def setUp(self, mocked_client: unittest.mock.MagicMock) -> None:
        mocked_client.return_value = self.MockDefaultClient()
        db_spec = sthali_db.clients.DBSpecification("test_path")  # type: ignore
        self.db = sthali_db.clients.DB(db_spec, "table")  # type: ignore

    async def test_return_default(self) -> None:
        self.assertTrue(isinstance(self.db.client, self.MockDefaultClient))

    async def test_insert_one(self) -> None:
        result = await self.db.insert_one()

        self.assertEqual(result, "insert_one")

    async def test_select_one(self) -> None:
        result = await self.db.select_one()

        self.assertEqual(result, "select_one")

    async def test_update_one(self) -> None:
        result = await self.db.update_one()

        self.assertEqual(result, "update_one")

    async def test_delete_one(self) -> None:
        result = await self.db.delete_one()

        self.assertEqual(result, "delete_one")

    async def test_select_many(self) -> None:
        result = await self.db.select_many()

        self.assertEqual(result, "select_many")
