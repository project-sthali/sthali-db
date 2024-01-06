from unittest import IsolatedAsyncioTestCase

from src.sthali_db.dependencies import filter_parameters


class TestfilterParameters(IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        result = await filter_parameters()

        self.assertEqual(result, {"skip": 0, "limit": 100})

    async def test_return_custom(self) -> None:
        result = await filter_parameters(10, 10)

        self.assertEqual(result, {"skip": 10, "limit": 10})
