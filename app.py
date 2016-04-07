import falcon
import json

class WaifuMessage(object):
    def on_get(self, req, resp):
        resp.body = json.dumps({'items': [
            {'message': 'Привет, анон.', 'image': './pics/test_pic1.png'},
            {'message': 'Я тестовая 2d-тян, версия 0.1.', 'image': './pics/test_pic2.png'},
            {'message': 'Я могу говорить только эти три фразы, сорьки.', 'image': './pics/test_pic3.png'},
        ]})

api = falcon.API()
api.add_route('/waifu/messages', WaifuMessage())
