import falcon
from peewee import DoesNotExist
from resources.middlewares import db_not_found_handler
from resources.user_resource import UserResource, UserAuthResource
from resources.user_waifu_resource import UserWaifuResource
from resources.waifu_message_resource import WaifuMessageResource
from resources.waifu_resource import WaifuResource, WaifuCollectionResource
from waifu_share_resource import WaifuShareResource

api = falcon.API()

api.add_route('/user', UserResource())
api.add_route('/user/auth', UserAuthResource())
api.add_route('/user/waifu', UserWaifuResource())
api.add_route('/waifu', WaifuCollectionResource())
api.add_route('/waifu/{id}', WaifuResource())
api.add_route('/waifu/{id}/messages', WaifuMessageResource())
api.add_route('/waifu/share', WaifuShareResource())
api.add_error_handler(DoesNotExist, db_not_found_handler.handler)