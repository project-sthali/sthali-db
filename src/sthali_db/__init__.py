"""{...}."""

from .engine import DBSession, Engine
from .models import BaseModel, ModelType
from .schemas import BaseSchema, SchemaType

__all__ = [
    "BaseModel",
    "BaseSchema",
    "DBSession",
    "Engine",
    "ModelType",
    "SchemaType",
    "definitions_type",
]


definitions_type = list[
    tuple[
        type[ModelType],
        tuple[
            type[SchemaType],
            type[SchemaType],
            type[SchemaType],
        ],
    ]
]
