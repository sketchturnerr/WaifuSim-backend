import falcon
from resources.user_resource import UserResource, UserAuthResource
from resources.waifu_message_resource import WaifuMessageResource
from resources.waifu_resource import WaifuResource

api = falcon.API()

api.add_route('/user', UserResource())
api.add_route('/user/auth', UserAuthResource())
api.add_route('/waifu', WaifuResource())
api.add_route('/waifu/messages', WaifuMessageResource())
