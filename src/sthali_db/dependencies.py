"""This module provides the dependencies for sthali-db usage."""
from typing import Annotated, NoReturn

from pydantic import BaseModel, Field, NonNegativeInt


async def filter_parameters() -> NoReturn:
    """Not implemented."""
    raise NotImplementedError


class PaginateParameters(BaseModel):
    """Represents the parameters for retrieving items.

    Attributes:
        skip (NonNegativeInt): The number of items to skip. Defaults to 0.
        limit (NonNegativeInt): The maximum number of items to return. Defaults to 100.
    """

    skip: Annotated[NonNegativeInt, Field(description="The number of items to skip")] = 0
    limit: Annotated[NonNegativeInt, Field(description="The maximum number of items to return")] = 100
