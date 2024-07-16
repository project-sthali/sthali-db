from unittest import TestCase, IsolatedAsyncioTestCase

from sthali_db import models


class TestDefault(IsolatedAsyncioTestCase):
    async def test_return_default(self) -> None:
        result = models.Default()

        self.assertEqual(result.factory, None)
        self.assertEqual(result.value, None)

    async def test_return_custom(self) -> None:
        func = lambda: None
        result = models.Default(factory=func, value=0)

        self.assertEqual(result.factory, func)
        self.assertEqual(result.value, 0)
