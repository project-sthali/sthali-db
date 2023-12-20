from unittest import IsolatedAsyncioTestCase, mock

from src.sthali_db.engines.default import DefaultEngine
from tests import ID, PAYLOAD_WITH_ID, PAYLOAD_WITHOUT_ID


class TestDefaultEngine(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        path = ""
        table = "test_table"
        self.engine = DefaultEngine(path, table)

    @mock.patch("src.sthali_db.engines.default.DefaultEngine.db")
    def test_get(self, mock_db):
        mock_db.__getitem__.return_value = PAYLOAD_WITHOUT_ID

        result = self.engine._get(ID)
        self.assertEqual(result, PAYLOAD_WITHOUT_ID)

    @mock.patch("src.sthali_db.engines.default.DefaultEngine.db")
    def test_get_not_found(self, mock_db):
        mock_db.__getitem__.side_effect = KeyError

        with self.assertRaises(self.engine.exception) as context:
            self.engine._get(ID)

        self.assertEqual(context.exception.status_code, self.engine.status.HTTP_404_NOT_FOUND)

    async def test_db_insert_one(self):
        result = await self.engine.db_insert_one(ID, PAYLOAD_WITHOUT_ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    @mock.patch("src.sthali_db.engines.default.DefaultEngine._get")
    async def test_db_select_one(self, mock_get):
        mock_get.return_value = PAYLOAD_WITHOUT_ID

        result = await self.engine.db_select_one(ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    @mock.patch("src.sthali_db.engines.default.DefaultEngine._get")
    async def test_db_select_one_not_found(self, mock_get):
        mock_get.side_effect = self.engine.exception(self.engine.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.engine.exception) as context:
            await self.engine.db_select_one(ID)

        self.assertEqual(context.exception.status_code, self.engine.status.HTTP_404_NOT_FOUND)

    @mock.patch("src.sthali_db.engines.default.DefaultEngine._get")
    async def test_db_update_one(self, mock_get):
        mock_get.return_value = PAYLOAD_WITHOUT_ID

        result = await self.engine.db_update_one(ID, PAYLOAD_WITHOUT_ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    @mock.patch("src.sthali_db.engines.default.DefaultEngine._get")
    async def test_db_update_one_not_found(self, mock_get):
        mock_get.side_effect = self.engine.exception(self.engine.status.HTTP_404_NOT_FOUND)

        with self.assertRaises(self.engine.exception) as context:
            await self.engine.db_update_one(ID, PAYLOAD_WITHOUT_ID)

        self.assertEqual(context.exception.status_code, self.engine.status.HTTP_404_NOT_FOUND)

    @mock.patch("src.sthali_db.engines.default.DefaultEngine._get")
    async def test_db_delete_one(self, mock_get):
        mock_get.return_value = PAYLOAD_WITHOUT_ID

        result = await self.engine.db_delete_one(ID)
        self.assertIsNone(result)

    async def test_db_delete_one_not_found(self):
        with self.assertRaises(self.engine.exception) as context:
            await self.engine.db_delete_one(ID)

        self.assertEqual(context.exception.status_code, self.engine.status.HTTP_404_NOT_FOUND)

    @mock.patch("src.sthali_db.engines.default.DefaultEngine.db")
    async def test_db_select_all(self, mock_db):
        mock_db.items.return_value = [(ID, PAYLOAD_WITHOUT_ID)]

        result = await self.engine.db_select_all()
        self.assertEqual(result, [PAYLOAD_WITH_ID])
