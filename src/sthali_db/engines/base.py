import typing
import uuid

import fastapi

from ..types import PaginateParameters


class BaseEngine:
    """
    Base engine class for interacting with a database.

    This class provides the basic interface for performing CRUD operations on a database.
    Derived classes should implement the specific methods for each operation.

    Attributes:
        exception: The exception class to be used for raising HTTP exceptions.
        status: The status module to be used for HTTP status codes.

    Args:
        path (str): The path to the database.
        table (str): The name of the table in the database.
    """

    exception = fastapi.HTTPException
    status = fastapi.status

    def __init__(self, path: str, table: str) -> None:
        pass

    async def insert_one(self, resource_id: uuid.UUID, resource_obj: dict) -> typing.NoReturn:
        """
        Inserts a single resource object into the database.

        Args:
            resource_id (uuid.UUID): The unique identifier for the resource.
            resource_obj (dict): The resource object to be inserted.

        Raises:
            NotImplementedError: This method should be implemented by the derived class.
        """
        raise NotImplementedError

    async def select_one(self, resource_id: uuid.UUID) -> typing.NoReturn:
        """
        Retrieves a single resource from the database based on the given resource ID.

        Args:
            resource_id (uuid.UUID): The ID of the resource to retrieve.

        Raises:
            NotImplementedError: This method should be implemented by the derived class.
        """
        raise NotImplementedError

    async def update_one(self, resource_id: uuid.UUID, resource_obj: dict, partial: bool = False) -> typing.NoReturn:
        """
        Update a resource with the given ID.

        Args:
            resource_id (uuid.UUID): The ID of the resource to update.
            resource_obj (dict): The updated resource object.
            partial (bool, optional): If True, perform a partial update. Defaults to False.

        Raises:
            NotImplementedError: This method should be implemented by the derived class.
        """
        raise NotImplementedError

    async def delete_one(self, resource_id: uuid.UUID) -> typing.NoReturn:
        """
        Deletes a resource with the given ID.

        Args:
            resource_id (uuid.UUID): The ID of the resource to delete.

        Raises:
            NotImplementedError: This method should be implemented by the derived class.
        """
        raise NotImplementedError

    async def select_many(self, paginate_parameter: PaginateParameters) -> typing.NoReturn:
        """
        Retrieves multiple records from the database.

        Args:
            paginate_parameter (PaginateParameters): An object containing parameters for pagination.

        Raises:
            NotImplementedError: This method should be implemented by the derived class.
        """
        raise NotImplementedError
