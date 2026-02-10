"""{...}."""

from typing import TypeVar

from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()
ModelType = TypeVar("ModelType", bound=BaseModel)
