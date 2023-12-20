from unittest.mock import Mock
from uuid import uuid4

from src.sthali_db import types
from src.sthali_db.engines.tinydb import TinyDB
# from src.sthali_db.types import DBSpecification

# from src.sthali_crud.db_engines import (
#     base,
#     DBEngine,
#     tinydb,
# )


# from tests import CREATE, DELETE, READ, READ_ALL, UPDATE


# class MockDBEngine(DBEngine):
#     db_insert_one = CREATE
#     db_select_one = READ
#     db_update_one = UPDATE
#     db_delete_one = DELETE
#     db_select_all = READ_ALL


# class MockEngine(base.BaseEngine):
#     db_insert_one = CREATE
#     db_select_one = READ
#     db_update_one = UPDATE
#     db_delete_one = DELETE
#     db_select_all = READ_ALL


class MockTinyDB(TinyDB):
    table = Mock()


DB_SPEC = types.DBSpecification(
    engine="Default",
    path="",
)


ID = uuid4()
PAYLOAD_WITHOUT_ID = {"field_1": "value_1"}
PAYLOAD_WITH_ID = {"id": ID, **PAYLOAD_WITHOUT_ID}
# PAYLOAD_WITH_ID_STR = {"id": str(ID), **PAYLOAD_WITHOUT_ID}
