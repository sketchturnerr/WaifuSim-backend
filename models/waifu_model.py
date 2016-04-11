from models.base_model import BaseModel
from datetime import datetime
from models.user_model import UserModel, USER_ROLE_USER, USER_ROLE_MODERATOR
from peewee import CharField, TextField, DateTimeField, IntegerField, ForeignKeyField

WAIFU_SHARING_STATUS_PRIVATE = 1
WAIFU_SHARING_STATUS_MODERATION = 2
WAIFU_SHARING_STATUS_PUBLIC = 3

SHARING_RESULT_NO_ACCESS = -1
SHARING_RESULT_NOT_MODIFIED = -2

SHARING_ACTIONS_MATRIX = {
    (WAIFU_SHARING_STATUS_PRIVATE, USER_ROLE_USER, 1): WAIFU_SHARING_STATUS_MODERATION,
    (WAIFU_SHARING_STATUS_PRIVATE, USER_ROLE_USER, 0): SHARING_RESULT_NO_ACCESS,
    (WAIFU_SHARING_STATUS_PRIVATE, USER_ROLE_MODERATOR, 1): WAIFU_SHARING_STATUS_PUBLIC,
    (WAIFU_SHARING_STATUS_PRIVATE, USER_ROLE_MODERATOR, 0): SHARING_RESULT_NO_ACCESS,

    (WAIFU_SHARING_STATUS_MODERATION, USER_ROLE_USER, 1): SHARING_RESULT_NOT_MODIFIED,
    (WAIFU_SHARING_STATUS_MODERATION, USER_ROLE_USER, 0): SHARING_RESULT_NO_ACCESS,
    (WAIFU_SHARING_STATUS_MODERATION, USER_ROLE_MODERATOR, 1): WAIFU_SHARING_STATUS_PUBLIC,
    (WAIFU_SHARING_STATUS_MODERATION, USER_ROLE_MODERATOR, 0): WAIFU_SHARING_STATUS_PUBLIC,

    (WAIFU_SHARING_STATUS_PUBLIC, USER_ROLE_USER, 1): SHARING_RESULT_NOT_MODIFIED,
    (WAIFU_SHARING_STATUS_PUBLIC, USER_ROLE_USER, 0): SHARING_RESULT_NOT_MODIFIED,
    (WAIFU_SHARING_STATUS_PUBLIC, USER_ROLE_MODERATOR, 1): SHARING_RESULT_NOT_MODIFIED,
    (WAIFU_SHARING_STATUS_PUBLIC, USER_ROLE_MODERATOR, 0): SHARING_RESULT_NOT_MODIFIED,
}


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

    @classmethod
    def get_by_id_and_user(cls, id, user):
        try:
            waifu = cls.get(
                (cls.id == id) &
                ((cls.owner == user) |
                 (cls.sharing_status == WAIFU_SHARING_STATUS_PUBLIC))
            )
        except ValueError:
            # id не int, что ж, у нас явно нет такого документа.
            return None
        return waifu

    def share(self, user):
        is_owner = 1 if self.owner == user else 0
        action = SHARING_ACTIONS_MATRIX[(self.sharing_status, user.role, is_owner)]
        if action in (WAIFU_SHARING_STATUS_MODERATION, WAIFU_SHARING_STATUS_PUBLIC, ):
            self.sharing_status = action
        return action
