import unittest

import sthali_db.clients

module = sthali_db.clients

class TestBase(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        base = module.Base("test_path", "test_table")
        self.base = base
        self.resource_id: module.ResourceId  = module.ResourceId.__metadata__[0].default_factory()  # type: ignore

    async def test_return_default(self) -> None:
        self.assertEqual(self.base.exception, module.Base.exception)
        self.assertEqual(self.base.status, module.Base.status)

    async def test_insert_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.insert_one(self.resource_id, {})

    async def test_select_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.select_one(self.resource_id)

    async def test_update_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.update_one(self.resource_id, {})

    async def test_delete_one_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base.delete_one(self.resource_id)

    async def test_select_many_not_implemented(self) -> None:
        paginate_parameters = sthali_db.dependencies.PaginateParameters()  # type: ignore

        with self.assertRaises(NotImplementedError):
            await self.base.select_many(paginate_parameters)
