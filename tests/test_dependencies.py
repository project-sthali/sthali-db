import unittest

import sthali_db.dependencies


class TestFilterParameters(unittest.IsolatedAsyncioTestCase):
    async def test_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            await sthali_db.dependencies.filter_parameters()


class TestPaginateParameters(unittest.IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        result = sthali_db.dependencies.PaginateParameters()  # type: ignore

        self.assertEqual(result.skip, 0)
        self.assertEqual(result.limit, 100)

    async def test_return_custom(self) -> None:
        result = sthali_db.dependencies.PaginateParameters(skip=10, limit=10)

        self.assertEqual(result.skip, 10)
        self.assertEqual(result.limit, 10)
