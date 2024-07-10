"""This module provides the dependencies for sthali-db usage."""
import typing

import pydantic


async def filter_parameters() -> typing.NoReturn:
    """Not implemented."""
    raise NotImplementedError


class PaginateParameters(pydantic.BaseModel):
    """Represents the parameters for retrieving items.

    Attributes:
        skip (pydantic.NonNegativeInt): The number of items to skip.
            Defaults to 0.
        limit (pydantic.NonNegativeInt): The maximum number of items to return.
            Defaults to 100.
    """

    skip: typing.Annotated[
        pydantic.NonNegativeInt,
        pydantic.Field(description="The number of items to skip"),
    ] = 0
    limit: typing.Annotated[
        pydantic.NonNegativeInt,
        pydantic.Field(description="The maximum number of items to return"),
    ] = 100
