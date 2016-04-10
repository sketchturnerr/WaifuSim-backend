from datetime import datetime
from peewee import ForeignKeyField, CompositeKey, DateTimeField
from models.base_model import BaseModel
from models.user_model import UserModel
from models.waifu_model import WaifuModel


class UserToWaifuModel(BaseModel):
    class Meta:
        db_table = 'users_to_waifus'
        primary_key = CompositeKey('user', 'waifu')

    user = ForeignKeyField(UserModel)
    waifu = ForeignKeyField(WaifuModel)
    created_at = DateTimeField(null=False, default=datetime.now)
