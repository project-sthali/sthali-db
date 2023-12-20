from unittest import IsolatedAsyncioTestCase

from src.sthali_db.engines.postgres import PostgresEngine
from tests import ID, PAYLOAD_WITHOUT_ID


class TestBaseEngine(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        path = ""
        table = "test_table"
        self.engine = PostgresEngine(path, table)

    async def test_db_insert_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.engine.db_insert_one(ID, PAYLOAD_WITHOUT_ID)

    async def test_db_select_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.engine.db_select_one(ID)

    async def test_db_update_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.engine.db_update_one(ID, PAYLOAD_WITHOUT_ID)

    async def test_db_delete_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.engine.db_delete_one(ID)

    async def test_db_select_all(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.engine.db_select_all()
