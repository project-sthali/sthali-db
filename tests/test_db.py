import unittest
import unittest.mock

import sthali_db.db


class TestDBSpecification(unittest.IsolatedAsyncioTestCase):
    # async def test_return_default(self) -> None:
    #     db_spec = sthali_db.db.DBSpecification("test_path")  # type: ignore

    #     self.assertEqual(db_spec.path, "test_path")
    #     self.assertEqual(db_spec.client, "Default")

    # async def test_return_custom(self) -> None:
    async def test_return(self) -> None:
        db_spec = sthali_db.db.DBSpecification(path="test_path", client="tinydb")

        self.assertEqual(db_spec.path, "test_path")
        self.assertEqual(db_spec.client, "Tinydb")


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
        db_spec = sthali_db.db.DBSpecification("test_path", "default")  # type: ignore
        self.db = sthali_db.db.DB(db_spec, "table")  # type: ignore

    # async def test_return_default(self) -> None:
    #     self.assertTrue(isinstance(self.db.client, self.MockDefaultClient))

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
