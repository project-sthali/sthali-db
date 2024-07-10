"""This module provides the necessary components for interacting with the database.

It includes the following:

- `DBClient`: A class for connecting to the database and executing queries.
- `DBSpecification`: A class for defining the database specifications.
- `Models`: A module that contains the database models.
- `filter_parameters`: A function for filtering query parameters.
- `PaginateParameters`: A class for defining pagination parameters.
"""
from . import clients, dependencies, models
from .clients import DBClient, DBSpecification
from .dependencies import PaginateParameters, filter_parameters
from .models import Base, BaseWithId, Field, Models

__all__ = [
    "Base",
    "BaseWithId",
    "DBClient",
    "DBSpecification",
    "Field",
    "Models",
    "PaginateParameters",
    "clients",
    "dependencies",
    "filter_parameters",
    "models",
]
