from models.base_model import db
from models.user_model import UserModel
from models.user_to_waifu_model import UserToWaifuModel
from models.waifu_model import WaifuModel
from models.waifu_message_model import WaifuMessageModel


def create_tables():
    db.connect()
    db.create_tables((
        UserModel,
        WaifuModel,
        WaifuMessageModel,
        UserToWaifuModel,
    ), True)

if __name__ == '__main__':
    create_tables()
    db.manual_close()
