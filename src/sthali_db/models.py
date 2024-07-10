"""This module provides {...}."""
import typing
import uuid

import pydantic


@pydantic.dataclasses.dataclass
class Default:
    """Represents a default value for an attribute.

    Attributes:
        factory (typing.Callable[[], typing.Any] | None): The function used to create the default value for the
            attribute. Defaults to None.
        value (typing.Any | None): The default value for the attribute. Defaults to None.
    """

    factory: typing.Annotated[
        typing.Callable[[], typing.Any] | None,
        pydantic.Field(default=None, description="The function used to create the default value for the attribute"),
    ]
    value: typing.Annotated[
        typing.Any | None, pydantic.Field(default=None, description="The default value for the attribute")
    ]


@pydantic.dataclasses.dataclass
class Field:
    """Represents a field with its metadata.

    Attributes:
        name (str): Name of the field.
        type (typing.Any): Type annotation of the field.
        default (Default | None): Default value/factory of the field. Defaults to None.
        description (str | None): Description of the field. Defaults to None.
        optional (bool | None): Indicates if the field accepts None. Defaults to None.
        title (str | None): Title of the field. Defaults to None.
    """

    name: typing.Annotated[str, pydantic.Field(description="Name of the field")]
    type: typing.Annotated[typing.Any, pydantic.Field(description="Type annotation of the field")]
    default: typing.Annotated[Default | None, pydantic.Field(description="Default value/factory of the field")] = None
    description: typing.Annotated[str | None, pydantic.Field(description="Description of the field")] = None
    optional: typing.Annotated[bool | None, pydantic.Field(description="Indicates if the field accepts None")] = None
    title: typing.Annotated[str | None, pydantic.Field(description="Title of the field")] = None

    @property
    def metadata(self) -> dict[str, typing.Any]:
        """Get the metadata for the field.

        Returns:
            dict[str, typing.Any]: A dictionary containing the metadata for the field.
        """
        result: dict[str, typing.Any] = {
            "description": self.description or f"Field {self.name}",
            "title": self.title or self.name,
        }
        if self.default:
            if self.default.factory:
                result["default_factory"] = self.default.factory
            else:
                result["default"] = self.default.value
        return result

    @property
    def type_annotated(self) -> typing.Annotated[typing.Any, pydantic.Field]:
        """Returns the type annotation of the field.

        Returns:
            typing.Annotated[typing.Any, pydantic.Field]: The type annotation of the field.
        """
        field_type = (self.type, self.type | None)[bool(self.optional)]
        return typing.Annotated[field_type, pydantic.Field(**self.metadata)]


class Base(pydantic.BaseModel):
    """Base class for models."""


class BaseWithId(Base):
    """Represents a base class for models with a resource identifier."""

    id: typing.Annotated[uuid.UUID, pydantic.Field(description="Resource identifier")]


class Models:
    """Represents a collection of models.

    This class is responsible for creating and managing models dynamically based on the provided fields.
    It provides methods to create different types of models such as create, response, and update models.

    Attributes:
        name (str): The name of the collection of models.
        create_model (type[Base]): The dynamically created model for creating new instances.
        response_model (type[BaseWithId]): The dynamically created model for response payloads.
        update_model (type[Base]): The dynamically created model for updating existing instances.

    Methods:
        create(base: type[Base], name: str, fields: list[Field]) -> type[Base]:
            Creates a new model dynamically based on the provided base, name, and fields.

    """

    def __init__(self, name: str, fields: list[Field]) -> None:
        """Initialize the Models class.

        Args:
            name (str): The name of the collection of models.
            fields (list[Field]): The list of fields for the models.
        """
        self.name = name
        self.create_model = self.create(Base, f"Create{name.title()}", fields)
        self.response_model = self.create(BaseWithId, f"Response{name.title()}", fields)
        self.update_model = self.create(Base, f"Update{name.title()}", fields)

    @staticmethod
    def create(base: type[Base] | type[BaseWithId], name: str, fields: list[Field]) -> type[Base] | type[BaseWithId]:
        """Create a new model dynamically based on the provided base, name, and fields.

        Args:
            base (type[Base] | type[BaseWithId]): The base model to inherit from.
            name (str): The name of the new model.
            fields (list[Field]): The list of fields for the new model.

        Returns:
            type[Base] | type[BaseWithId]: The dynamically created model.
        """
        fields_constructor = {field.name: field.type_annotated for field in fields}
        return pydantic.create_model(__model_name=name, __base__=base, **fields_constructor)  # type: ignore
