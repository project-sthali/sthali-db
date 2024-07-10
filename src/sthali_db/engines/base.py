"""This module provides the base engine class for interacting with a database."""
import typing
import uuid

import fastapi
import pydantic

from ..dependencies import PaginateParameters

ResourceId = typing.Annotated[uuid.UUID, pydantic.Field(description="The unique identifier of the resource")]
ResourceObj = typing.Annotated[dict[str, typing.Any], pydantic.Field(description="The resource object")]
Partial = typing.Annotated[bool | None, pydantic.Field(description="Perform a partial update")]


class BaseClient:
    """Base client class for interacting with a database.

    Provides the basic interface for performing CRUD operations on a database.
    Derived classes should implement the specific methods for each operation.

    Attributes:
        exception (fastapi.HTTPException): The exception module to be used for raising HTTP exceptions.
        status (fastapi.status): The status module to be used for HTTP status codes.

    Args:
        path (str): The path to the database.
        table (str): The name of the table in the database.

    """

    exception = fastapi.HTTPException
    status = fastapi.status

    def __init__(self, path: str, table: str) -> None:
        """Initialize the BaseClient class.

        Args:
            path (str): The path to the database.
            table (str): The name of the table in the database.

        """

    async def insert_one(self, resource_id: ResourceId, resource_obj: ResourceObj) -> ResourceObj:
        """Inserts a resource object in the database.

        Args:
            resource_id (ResourceId): The ID of the resource to be inserted.
            resource_obj (ResourceObj): The resource object to be inserted.

        Returns:
            ResourceObj: The resource object containing the ID.

        Raises:
            self.exception: If the resource already exists in the database.
        """
        raise NotImplementedError

    async def select_one(self, resource_id: ResourceId) -> ResourceObj:
        """Retrieves a resource from the database based on the given ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be retrieved.

        Returns:
            ResourceObj: The retrieved resource object.

        Raises:
            self.exception: If the resource is not found in the database.
        """
        raise NotImplementedError

    async def update_one(
        self,
        resource_id: ResourceId,
        resource_obj: ResourceObj,
        partial: Partial = None,
    ) -> ResourceObj:
        """Updates a resource in the database based on the given ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be updated.
            resource_obj (ResourceObj): The resource object to be updated.
            partial (Partial): Whether to perform a partial update or replace the entire resource object.
                Defaults to None.

        Returns:
            ResourceObj: The resource object containing the ID.

        Raises:
            self.exception: If the resource is not found in the database.
        """
        raise NotImplementedError

    async def delete_one(self, resource_id: ResourceId) -> None:
        """Deletes a resource from the database based on the given resource ID.

        Args:
            resource_id (ResourceId): The ID of the resource to be deleted.

        Returns:
            None

        Raises:
            self.exception: If the resource is not found in the database.
        """
        raise NotImplementedError

    async def select_many(self, paginate_parameters: PaginateParameters) -> list[ResourceObj]:
        """Retrieves multiple resources from the database based on the given pagination parameters.

        Args:
            paginate_parameters (PaginateParameters): The pagination parameters.

        Returns:
            list[ResourceObj]: A list of objects representing the retrieved resources.
        """
        raise NotImplementedError
