import typing

import pydantic


async def filter_parameters() -> typing.NoReturn:
    raise NotImplementedError


async def paginate_parameters(
    skip: typing.Annotated[
        pydantic.NonNegativeInt, pydantic.Field(description="The number of items to skip", default=0)
    ],
    limit: typing.Annotated[
        pydantic.NonNegativeInt, pydantic.Field(description="The maximum number of items to return", default=100)
    ],
) -> dict:
    """
    Paginates the parameters for retrieving items.

    Args:
        skip (int): The number of items to skip. Defaults to 0.
        limit (int): The maximum number of items to return. Defaults to 100.

    Returns:
        dict: A dictionary containing the skip and limit parameters.
    """
    return {"skip": skip, "limit": limit}
