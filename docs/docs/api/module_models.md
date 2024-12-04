### `sthali_db.models`

```
This module provides classes for creating dynamic models based on field specifications.

Classes:
    Base: Represents a base class for models.
    BaseWithId: Represents a base class for models with a resource identifier.
    Models(name: str, fields: list[FieldSpecification]): Represents a collection of models.

Dataclasses:
    FieldSpecification: Represents a field with its metadata.

```

#### `FieldSpecification`

```
Represents a field with its metadata.

    Attributes:
        name (str): Name of the field.
        type (Types.TypeEnum): Type annotation of the field.
        default (Default | None): Default value/factory of the field. Defaults to None.
        description (str | None): Description of the field. Defaults to None.
        optional (bool | None): Indicates if the field accepts None. Defaults to None.
        title (str | None): Title of the field. Defaults to None.
    
```


#### `Models`

```
Represents a collection of models.

    This class is responsible for creating and managing models dynamically based on the provided fields.
    It provides methods to create different types of models such as create, response, and update models.

    Attributes:
        name (str): The name of the collection of models.
        create_model (type[Base]): The dynamically created model for creating new instances.
        response_model (type[BaseWithId]): The dynamically created model for response payloads.
        update_model (type[Base]): The dynamically created model for updating existing instances.
    
```


#### `Types`

```
Types class provides a mechanism to manage a custom enumeration of types.

    Attributes:
        types_enum (TypeEnum): An enumeration of various types and values.

    Methods:
        get(name: str) -> typing.Any:
            Retrieve an attribute from the `types_enum` based on the given name.
        set(name: str, value: typing.Any = None, operation: typing.Literal["add", "del"] = "add") -> None:
            Modifies the `types_enum` attribute by adding or deleting an enumeration member.
    
```

