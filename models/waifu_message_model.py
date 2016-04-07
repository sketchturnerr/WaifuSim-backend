from models.base_model import BaseModel
from peewee import ForeignKeyField
from playhouse.postgres_ext import BinaryJSONField
from models.waifu_model import WaifuModel

class WaifuMessageModel(BaseModel):
    class Meta:
        db_table = 'waifu_messages'

    content = BinaryJSONField(null=False)
    waifu = ForeignKeyField(WaifuModel, related_name='messages')
