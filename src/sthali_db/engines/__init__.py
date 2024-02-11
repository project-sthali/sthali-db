import importlib
from typing import Any

from ..types import DBSpecification
from .base import BaseEngine


class DBEngine:
    engine: BaseEngine

    def __init__(self, db_spec: DBSpecification, table: str) -> None:
        engine_module = importlib.import_module(f".{db_spec.engine.lower()}", package=__package__)
        engine_class: type[BaseEngine] = getattr(engine_module, f"{db_spec.engine}Engine")
        self.engine = engine_class(db_spec.path, table)

    async def insert_one(self, *args, **kwargs) -> Any:
        return await self.engine.insert_one(*args, **kwargs)

    async def select_one(self, *args, **kwargs) -> Any:
        return await self.engine.select_one(*args, **kwargs)

    async def update_one(self, *args, **kwargs) -> Any:
        return await self.engine.update_one(*args, **kwargs)

    async def delete_one(self, *args, **kwargs) -> Any:
        return await self.engine.delete_one(*args, **kwargs)

    async def select_many(self, *args, **kwargs) -> Any:
        return await self.engine.select_many(*args, **kwargs)
