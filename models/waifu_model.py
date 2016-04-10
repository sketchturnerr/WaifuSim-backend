from models.base_model import BaseModel
from datetime import datetime
from models.user_model import UserModel
from peewee import CharField, TextField, DateTimeField, IntegerField, ForeignKeyField

WAIFU_SHARING_STATUS_PRIVATE = 1
WAIFU_SHARING_STATUS_PUBLIC_MODERATION = 2
WAIFU_SHARING_STATUS_PUBLIC = 3


class WaifuModel(BaseModel):
    class Meta:
        db_table = 'waifus'

    name = CharField(max_length=128, null=False)
    description = TextField(null=False)
    pic = CharField(max_length=128, null=False)
    created_at = DateTimeField(null=False, default=datetime.now)
    updated_at = DateTimeField(null=False, default=datetime.now)
    rating = IntegerField(null=False, default=0)
    sharing_status = IntegerField(null=False, default=WAIFU_SHARING_STATUS_PRIVATE)
    owner = ForeignKeyField(UserModel, related_name='waifus_created_by_me')

    def to_json(self):
        json = super(WaifuModel, self).to_json()
        json['users_count'] = self.users.count()
        return json
