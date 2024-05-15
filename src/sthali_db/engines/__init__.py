import importlib
from typing import Any

from ..types import DBSpecification
from .base import BaseEngine


class DBEngine:
    """
    Represents a database engine that provides methods for interacting with the database.

    Attributes:
        engine (BaseEngine): The underlying engine used for database operations.

    Methods:
        __init__(self, db_spec: DBSpecification, table: str) -> None:
            Initializes a new instance of the DBEngine class.

        insert_one(self, *args, **kwargs) -> Any:
            Inserts a single record into the database.

        select_one(self, *args, **kwargs) -> Any:
            Retrieves a single record from the database.

        update_one(self, *args, **kwargs) -> Any:
            Updates a single record in the database.

        delete_one(self, *args, **kwargs) -> Any:
            Deletes a single record from the database.

        select_many(self, *args, **kwargs) -> Any:
            Retrieves multiple records from the database.

    """

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
