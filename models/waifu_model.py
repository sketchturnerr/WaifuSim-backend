from models.base_model import BaseModel
from datetime import datetime
from peewee import CharField, TextField, DateTimeField, IntegerField, BooleanField

class WaifuModel(BaseModel):
    class Meta:
        db_table = 'waifus'

    name = CharField(max_length=128, null=False)
    description = TextField(null=False)
    pic = CharField(max_length=128, null=False)
    created_at = DateTimeField(null=False, default=datetime.now)
    rating = IntegerField(null=False, default=0)
    is_contrib = BooleanField(null=False, default=False)
