from  datetime import datetime
from conf import Conf
from playhouse.postgres_ext import Model
from playhouse.db_url import connect

db = connect(Conf.get('db_connection_string'), register_hstore=False)


class BaseModel(Model):
    class Meta:
        database = db

    def to_json(self):
        json = {}
        for key in self._data.keys():
            value = getattr(self, key)
            if isinstance(value, datetime):
                value = value.timestamp()
            if isinstance(value, BaseModel): continue
            json[key] = value
        return json
