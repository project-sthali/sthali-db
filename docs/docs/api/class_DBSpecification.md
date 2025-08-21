### `DBSpecification`

```
Represents the specification for a database connection.

    Attributes:
        path (str): Path to the database.
            This field specifies the path to the database file or server.
        client (str): One of available database clients.
            This field specifies the database client to be used for the connection.
            The available options are &#34;Default&#34;, &#34;Postgres&#34;, &#34;Redis&#34;, &#34;SQLite&#34;, and &#34;TinyDB&#34;.
            Defaults to &#34;Default&#34;.
    
```

