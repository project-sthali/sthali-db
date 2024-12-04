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
