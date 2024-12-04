### `DB`

```
Represents a database client adapter.

    Attributes:
        client (type[Base]): The underlying client used for specific database operations.

    Methods:
        insert_one(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            Inserts a single record into the database.

        select_one(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            Retrieves a single record from the database.

        update_one(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            Updates a single record in the database.

        delete_one(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            Deletes a single record from the database.

        select_many(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            Retrieves multiple records from the database.
    
```

