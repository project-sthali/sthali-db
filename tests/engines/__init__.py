from sthali_db import engines


RESOURCE_ID = engines.base.uuid.uuid4()
RESOURCE_OBJ_WITHOUT_ID = {"field_1": "value_1"}
RESOURCE_OBJ_WITH_ID = {"id": RESOURCE_ID, **RESOURCE_OBJ_WITHOUT_ID}



# # from unittest.mock import Mock

# # from tests import ENGINES


# # class MockBase(ENGINES.base.BaseEngine):
# #     table = Mock()
# #     path = ""


# # class MockDefault(ENGINES.default.DefaultEngine):
# #     table = Mock()
# #     path = ""


# # class MockPostgres(ENGINES.postgres.PostgresEngine):
# #     table = Mock()
# #     path = ""


# # class MockRedis(ENGINES.redis.RedisEngine):
# #     table = Mock()
# #     path = ""


# # class MockSQLite(ENGINES.sqlite.SQLiteEngine):
# #     table = Mock()
# #     path = ""


# # class MockTinyDB(ENGINES.tinydb.TinyDB):
# #     table = Mock()
# #     path = ""
