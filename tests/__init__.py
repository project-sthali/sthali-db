from unittest.mock import Mock
from uuid import uuid4

from src.sthali_db import types
from src.sthali_db.engines.tinydb import TinyDB


class MockTinyDB(TinyDB):
    table = Mock()


DB_SPEC = types.DBSpecification(
    engine="Default",
    path="",
)


ID = uuid4()
PAYLOAD_WITHOUT_ID = {"field_1": "value_1"}
PAYLOAD_WITH_ID = {"id": ID, **PAYLOAD_WITHOUT_ID}
