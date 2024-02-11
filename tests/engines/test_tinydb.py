from unittest import IsolatedAsyncioTestCase, mock

from src.sthali_db.engines.tinydb import TinyDB, TinyDBEngine
from tests import ID, PAYLOAD_WITH_ID, PAYLOAD_WITHOUT_ID


class MockTinyDB(TinyDB):
    table = mock.Mock()


class TestTinyDBEngine(IsolatedAsyncioTestCase):
    def setUp(self):
        db_path = "test_db.json"
        db_table = "test_table"

        with mock.patch("src.sthali_db.engines.tinydb.TinyDB") as mock_tiny_db:
            mock_tiny_db.return_value = MockTinyDB
            engine = TinyDBEngine(db_path, db_table)
            engine.db.table = mock.Mock()
            self.engine = engine

    def test_get(self):
        self.engine.db.table.return_value.search.return_value = [PAYLOAD_WITHOUT_ID]

        result = self.engine._get(ID)
        self.assertEqual(result, PAYLOAD_WITHOUT_ID)

    def test_get_not_found(self):
        self.engine.db.table.return_value.search.return_value = []

        with self.assertRaises(self.engine.exception) as context:
            self.engine._get(ID)

        self.assertEqual(context.exception.status_code, self.engine.status.HTTP_404_NOT_FOUND)

    def test_get_not_found_without_raise(self):
        self.engine.db.table.return_value.search.return_value = [{}]

        result = self.engine._get(ID, False)
        self.assertEqual(result, {})

    async def test_insert_one(self):
        result = await self.engine.insert_one(ID, PAYLOAD_WITHOUT_ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    @mock.patch("src.sthali_db.engines.tinydb.TinyDBEngine._get")
    async def test_select_one(self, mock_get):
        mock_get.return_value = {"resource_obj": PAYLOAD_WITHOUT_ID}

        result = await self.engine.select_one(ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    async def test_select_one_not_found(self):
        self.engine.db.table.return_value.search.return_value = []

        with self.assertRaises(self.engine.exception) as context:
            await self.engine.select_one(ID)

        self.assertEqual(context.exception.status_code, self.engine.status.HTTP_404_NOT_FOUND)

    @mock.patch("src.sthali_db.engines.tinydb.TinyDBEngine._get")
    async def test_update_one(self, mock_get):
        mock_get.return_value = {"resource_obj": PAYLOAD_WITHOUT_ID}

        result = await self.engine.update_one(ID, PAYLOAD_WITHOUT_ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    async def test_update_one_not_found(self):
        self.engine.db.table.return_value.search.return_value = []

        with self.assertRaises(self.engine.exception) as context:
            await self.engine.update_one(ID, PAYLOAD_WITHOUT_ID)

        self.assertEqual(context.exception.status_code, self.engine.status.HTTP_404_NOT_FOUND)

    @mock.patch("src.sthali_db.engines.tinydb.TinyDBEngine._get")
    async def test_delete_one(self, mock_get):
        mock_get.return_value = {"resource_obj": PAYLOAD_WITHOUT_ID}

        result = await self.engine.delete_one(ID)
        self.assertIsNone(result)

    async def test_delete_one_not_found(self):
        self.engine.db.table.return_value.search.return_value = None

        with self.assertRaises(self.engine.exception) as context:
            await self.engine.delete_one(ID)

        self.assertEqual(context.exception.status_code, self.engine.status.HTTP_404_NOT_FOUND)

    async def test_select_many(self):
        records = [{"resource_id": ID, "resource_obj": PAYLOAD_WITHOUT_ID}]
        self.engine.db.table.return_value.all.return_value = records

        result = await self.engine.select_many()
        self.assertEqual(result, [PAYLOAD_WITH_ID])
