import falcon
from resources.waifu_message_resource import WaifuMessageResource

api = falcon.API()
api.add_route('/waifu/messages', WaifuMessageResource())
