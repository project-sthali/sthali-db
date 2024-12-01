### `sthali_db.models`

```
This module provides classes for creating dynamic models based on field specifications.
```

#### `FieldSpecification`

```
Represents a field with its metadata.

    Attributes:
        name (str): Name of the field.
        type (typing.Any): Type annotation of the field.
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

