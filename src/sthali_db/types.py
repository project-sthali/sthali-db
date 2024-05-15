import typing

import pydantic


@pydantic.dataclasses.dataclass
class DBSpecification:
    """DB specification.

    This class represents the specification for a database connection.

    Attributes:
        path (str): Path to the database.
            This field specifies the path to the database file or server.
        engine (str): One of available database engine drivers.
            This field specifies the database engine to be used for the connection.
            The available options are "Default", "Postgres", "Redis", "SQLite", and "TinyDB".
            The default value is "Default".
    """

    path: typing.Annotated[str, pydantic.Field(description="Path to the database")]
    engine: typing.Annotated[
        typing.Literal["Default", "Postgres", "Redis", "SQLite", "TinyDB"],
        pydantic.Field(description="One of available database engine drivers", default="Default"),
    ]


@pydantic.dataclasses.dataclass
class PaginateParameters:
    """Paginate parameters.

    This class represents the parameters for pagination.

    Attributes:
        skip (int): The number of items to skip.
            This field specifies the number of items to skip.
            The default value is 0.
        limit (int): The maximum number of items to return.
            This field specifies the maximum number of items to return.
            The default value is 100.
    """

    skip: typing.Annotated[
        pydantic.NonNegativeInt, pydantic.Field(description="The number of items to skip", default=0)
    ]
    limit: typing.Annotated[
        pydantic.NonNegativeInt, pydantic.Field(description="The maximum number of items to return", default=100)
    ]
