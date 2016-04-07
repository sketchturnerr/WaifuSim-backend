from conf import Conf
from playhouse.postgres_ext import Field, Model
from playhouse.db_url import connect, PooledPostgresqlExtDatabase

db = connect(Conf.get('db_connection_string'), register_hstore=False)

class BaseModel(Model):
    class Meta:
        database = db
