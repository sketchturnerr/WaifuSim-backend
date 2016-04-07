import random
import string
import hashlib
from peewee import CharField, DateTimeField, IntegerField, ForeignKeyField
from models.base_model import BaseModel
from datetime import datetime
from models.waifu_model import WaifuModel

USER_ROLE_ORDINAR = 1

class UserModel(BaseModel):
    class Meta:
        db_table = 'users'

    token_hash = CharField(max_length=128, null=False, index=True)
    registred_at = DateTimeField(null=False, default=datetime.now)
    role = IntegerField(null=False, default=USER_ROLE_ORDINAR)
    waifu = ForeignKeyField(WaifuModel, related_name='users')

    def generate_token(self):
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(16))
        self.token_hash = hashlib.sha512(token)
        return token
