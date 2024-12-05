"""This module provides a high-level interface for interacting with different database clients.

Classes:
    DB: Represents a database client adapter.

Dataclasses:
    DBSpecification: Represents the specification for a database connection.
"""

import importlib
import typing

import pydantic

if typing.TYPE_CHECKING:
    from .clients import Base


@pydantic.dataclasses.dataclass
class DBSpecification:
    """Represents the specification for a database connection.

    Attributes:
        path (str): Path to the database.
            This field specifies the path to the database file or server.
        client (str): One of available database clients.
            This field specifies the database client to be used for the connection.
            The available options are "Default", "Postgres", "Redis", "SQLite", and "TinyDB".
            Defaults to "Default".
    """

    path: typing.Annotated[str, pydantic.Field(description="Path to the database")]
    client: typing.Annotated[
        typing.Literal["Default", "Postgres", "Redis", "SQLite", "TinyDB"],
        pydantic.Field(default="Default", description="One of available database clients"),
    ]


class DB:
    """Represents a database client adapter.

    Args:
        db_spec (DBSpecification): The specification for the database connection.
        table (str): The name of the table to interact with.
    """

    def __init__(self, db_spec: DBSpecification, table: str) -> None:
        """Initialize the DB instance.

        Args:
            db_spec (DBSpecification): The specification for the database connection.
            table (str): The name of the table to interact with.
        """
        client_module = importlib.import_module(f".clients.{db_spec.client.lower()}", package=__package__)
        client_class: type[Base] = getattr(client_module, f"{db_spec.client}Client")
        client = client_class(db_spec.path, table)

        self.insert_one = client.insert_one
        self.select_one = client.select_one
        self.update_one = client.update_one
        self.delete_one = client.delete_one
        self.select_many = client.select_many
