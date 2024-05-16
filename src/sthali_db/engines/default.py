"""This module contains the DefaultEngine class which is responsible for managing resources in the database."""
import uuid

from ..types import PaginateParameters
from .base import BaseEngine


class DefaultEngine(BaseEngine):
    """
    This module provides the DefaultEngine class which is responsible for handling database operations.

    Attributes:
        db (dict): A dictionary representing the database.

    Args:
        _: A placeholder argument.
        table (str): The name of the table.

    Raises:
        self.exception: If the resource is not found in the database.
    """

    db = {}

    def __init__(self, _: str, table: str) -> None:
        self.table = table

    def _get(self, resource_id: uuid.UUID) -> dict:
        """
        Retrieves a resource from the database based on the given resource ID.

        Args:
            resource_id (uuid.UUID): The ID of the resource to retrieve.

        Returns:
            dict: The retrieved resource.

        Raises:
            self.exception: If the resource is not found in the database.
        """
        try:
            return self.db[resource_id]
        except KeyError as exception:
            raise self.exception(self.status.HTTP_404_NOT_FOUND, "not found") from exception

    async def insert_one(self, resource_id: uuid.UUID, resource_obj: dict) -> dict:
        """
        Inserts a resource object into the database.

        Args:
            resource_id (uuid.UUID): The ID of the resource.
            resource_obj (dict): The resource object to be inserted.

        Returns:
            dict: A dictionary containing the ID of the inserted resource and the resource object.
        """
        self.db[resource_id] = resource_obj
        return {"id": resource_id, **resource_obj}

    async def select_one(self, resource_id: uuid.UUID) -> dict:
        """
        Retrieves a resource from the database based on the given resource ID.

        Args:
            resource_id (uuid.UUID): The ID of the resource to retrieve.

        Returns:
            dict: The retrieved resource.

        Raises:
            self.exception: If the resource is not found in the database.
        """
        resource_obj = self._get(resource_id)
        return {"id": resource_id, **resource_obj}

    async def update_one(self, resource_id: uuid.UUID, resource_obj: dict, partial: bool = False) -> dict:
        """
        Updates a resource in the database based on the given resource ID.

        Args:
            resource_id (uuid.UUID): The ID of the resource to update.
            resource_obj (dict): The updated resource object.
            partial (bool, optional): Whether to perform a partial update or replace the entire resource object. Defaults to False.

        Returns:
            dict: A dictionary containing the ID of the updated resource and the updated resource object.
        """
        _resource_obj = self._get(resource_id)
        if partial:
            _resource_obj.update(resource_obj)
        else:
            _resource_obj = resource_obj
        self.db[resource_id] = _resource_obj
        return {"id": resource_id, **_resource_obj}

    async def delete_one(self, resource_id: uuid.UUID) -> None:
        """
        Deletes a resource from the database based on the given resource ID.

        Args:
            resource_id (uuid.UUID): The ID of the resource to delete.

        Raises:
            self.exception: If the resource is not found in the database.
        """
        self._get(resource_id)
        self.db.pop(resource_id, None)
        return None

    async def select_many(self, paginate_parameters: PaginateParameters) -> list:
        """
        Retrieves multiple resources from the database based on the given pagination parameters.

        Args:
            paginate_parameters (PaginateParameters): The pagination parameters.

        Returns:
            list: A list of dictionaries representing the retrieved resources.
        """
        return [{"id": k, **v} for k, v in self.db.items()][paginate_parameters.skip : paginate_parameters.limit]
