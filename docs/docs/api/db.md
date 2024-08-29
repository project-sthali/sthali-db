Represents a database client adapter.

    Attributes:
        client (type[Base]): The underlying client used for specific database operations.

    Methods:
        insert_one(self, *args: Any, **kwargs: Any) -> Any:
            Inserts a single record into the database.

        select_one(self, *args: Any, **kwargs: Any) -> Any:
            Retrieves a single record from the database.

        update_one(self, *args: Any, **kwargs: Any) -> Any:
            Updates a single record in the database.

        delete_one(self, *args: Any, **kwargs: Any) -> Any:
            Deletes a single record from the database.

        select_many(self, *args: Any, **kwargs: Any) -> Any:
            Retrieves multiple records from the database.
    