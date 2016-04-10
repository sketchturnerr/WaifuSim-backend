import random
import string
import hashlib

from peewee import CharField, DateTimeField, IntegerField
from models.base_model import BaseModel
from datetime import datetime

USER_ROLE_USER = 1
USER_ROLE_MODERATOR = 2

TOKEN_CHARS = string.ascii_uppercase+string.digits+string.ascii_lowercase


class UserModel(BaseModel):
    class Meta:
        db_table = 'users'

    token_hash = CharField(max_length=128, null=False, index=True)
    registred_at = DateTimeField(null=False, default=datetime.now)
    role = IntegerField(null=False, default=USER_ROLE_USER)

    @classmethod
    def generate_token_hash(cls, token):
        return hashlib.sha512(token.encode('utf-8')).hexdigest()

    def update_token(self):
        token = ''.join(random.choice(TOKEN_CHARS) for _ in range(16))
        self.token_hash = self.generate_token_hash(token)
        return token
