import json


class WaifuMessageResource(object):

    def on_get(self, req, resp, id):
        resp.body = json.dumps({'items': [
            {'message': 'Привет, анон.', 'image': './pics/test_pic1.png'},
            {'message': 'Я тестовая 2d-тян, версия 0.1.', 'image': './pics/test_pic2.png'},
            {'message': 'Я могу говорить только эти три фразы, сорьки.', 'image': './pics/test_pic3.png'},
        ]})

    def on_post(self, req, resp, id):
        pass

    def on_put(self, req, resp, id):
        pass

    def on_delete(self, req, resp, id):
        pass
