import typing

import pydantic

from .types import PaginateParameters


async def filter_parameters() -> typing.NoReturn:
    """
    Placeholder function for filtering parameters.
    This function raises a NotImplementedError.
    """
    raise NotImplementedError


async def paginate_parameters(
    skip: typing.Annotated[
        pydantic.NonNegativeInt, pydantic.Field(description="The number of items to skip", default=0)
    ],
    limit: typing.Annotated[
        pydantic.NonNegativeInt, pydantic.Field(description="The maximum number of items to return", default=100)
    ],
) -> PaginateParameters:
    """
    Paginates the parameters for retrieving items.

    Args:
        skip (int): The number of items to skip. Defaults to 0.
        limit (int): The maximum number of items to return. Defaults to 100.

    Returns:
        PaginateParameters: An instance of the PaginateParameters class containing the skip and limit parameters.
    """
    return PaginateParameters(skip=skip, limit=limit)
