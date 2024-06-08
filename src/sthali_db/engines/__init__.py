"""This module provides a high-level interface for interacting with different database engines."""

import importlib
import typing

import pydantic

from .base import BaseEngine, ResourceObj


class DBSpecification(pydantic.BaseModel):
    """Represents the specification for a database connection.

    Attributes:
        path (str): Path to the database.
            This field specifies the path to the database file or server.
        engine (str): One of available database engine drivers.
            This field specifies the database engine to be used for the connection.
            The available options are "Default", "Postgres", "Redis", "SQLite", and "TinyDB".
            Defaults to "Default".
    """

    path: typing.Annotated[str, pydantic.Field(description="Path to the database")]
    engine: typing.Annotated[
        typing.Literal["Default", "Postgres", "Redis", "SQLite", "TinyDB"],
        pydantic.Field(default="Default", description="One of available database engine drivers"),
    ]


class DBEngine:
    """Represents a database engine.

    Attributes:
        engine (BaseEngine): The underlying engine used for database operations.

    Methods:
        __init__(self, db_spec: DBSpecification, table: str) -> None:
            Initializes a new instance of the DBEngine class.

        insert_one(self, *args: typing.Any, **kwargs: typing.Any) -> Any:
            Inserts a single record into the database.

        select_one(self, *args: typing.Any, **kwargs: typing.Any) -> Any:
            Retrieves a single record from the database.

        update_one(self, *args: typing.Any, **kwargs: typing.Any) -> Any:
            Updates a single record in the database.

        delete_one(self, *args: typing.Any, **kwargs: typing.Any) -> Any:
            Deletes a single record from the database.

        select_many(self, *args: typing.Any, **kwargs: typing.Any) -> Any:
            Retrieves multiple records from the database.

    """

    engine: BaseEngine

    def __init__(self, db_spec: DBSpecification, table: str) -> None:
        """Initialize the DBEngine instance.

        Args:
            db_spec (DBSpecification): The specification for the database connection.
            table (str): The name of the table to interact with.
        """
        engine_module = importlib.import_module(f".{db_spec.engine.lower()}", package=__package__)
        engine_class: type[BaseEngine] = getattr(engine_module, f"{db_spec.engine}Engine")
        self.engine = engine_class(db_spec.path, table)

    async def insert_one(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> ResourceObj:
        """Insert a single record into the database.

        Args:
            *args: Positional arguments to be passed to the engine's insert_one method.
            **kwargs: Keyword arguments to be passed to the engine's insert_one method.

        Returns:
            Coroutine: A coroutine representing the asynchronous insertion operation.
        """
        return await self.engine.insert_one(*args, **kwargs)

    async def select_one(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> ResourceObj:
        """Select a single record from the database.

        Args:
            *args: Positional arguments to be passed to the engine's select_one method.
            **kwargs: Keyword arguments to be passed to the engine's select_one method.

        Returns:
            Coroutine: A coroutine representing the asynchronous selection operation.
        """
        return await self.engine.select_one(*args, **kwargs)

    async def update_one(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> ResourceObj:
        """Update a single record in the database.

        Args:
            *args: Positional arguments to be passed to the engine's update_one method.
            **kwargs: Keyword arguments to be passed to the engine's update_one method.

        Returns:
            Coroutine: A coroutine representing the asynchronous update operation.
        """
        return await self.engine.update_one(*args, **kwargs)

    async def delete_one(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None:
        """Delete a single record from the database.

        Args:
            *args: Positional arguments to be passed to the engine's delete_one method.
            **kwargs: Keyword arguments to be passed to the engine's delete_one method.

        Returns:
            Coroutine: A coroutine representing the asynchronous deletion operation.
        """
        return await self.engine.delete_one(*args, **kwargs)

    async def select_many(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> list[ResourceObj]:
        """Select multiple records from the database.

        Args:
            *args: Positional arguments to be passed to the engine's select_many method.
            **kwargs: Keyword arguments to be passed to the engine's select_many method.

        Returns:
            Coroutine: A coroutine representing the asynchronous selection operation.
        """
        return await self.engine.select_many(*args, **kwargs)
