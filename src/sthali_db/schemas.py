"""Pydantic schemas for API request/response models.

This module provides base schemas with form field generation and HATEOAS support.
"""
from typing import TypeVar

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base schema with form field generation and HATEOAS link support."""

    class Config:
        """Pydantic model configuration."""

        from_attributes = True


SchemaType = TypeVar("SchemaType", bound=BaseSchema)
