import json

import falcon
from models.base_model import db
from models.waifu_model import WaifuModel, WAIFU_SHARING_STATUS_MODERATION, \
    WAIFU_SHARING_STATUS_PUBLIC, SHARING_RESULT_NO_ACCESS, SHARING_RESULT_NOT_MODIFIED
from resources.middlewares.auth import auth
from resources.middlewares.body_checker import body_checker

DOCS_LINK = 'https://github.com/sketchturnerr/WaifuSim-backend#waifu-share'

# todo: добавить тест
class WaifuShareResource(object):

    @falcon.before(auth())
    @falcon.before(body_checker(('id', ), DOCS_LINK))
    def on_post(self, req, resp):
        id = req.context['parsed_body']['id']
        user = req.context['user']
        with db.atomic():
            try:
                waifu = WaifuModel.get(WaifuModel.id == id)
            # todo: вынести в класс модели, ValueError отдается orm, так что там этому методу и место.
            # можно добавить метод с сигнатурой get в базовый класс, но менять ValueError, на peewee.DoesNotExist
            except ValueError:
                raise falcon.HTTPNotFound()
            action = waifu.share(user)
            if action in (WAIFU_SHARING_STATUS_MODERATION, WAIFU_SHARING_STATUS_PUBLIC, ):
                waifu.update(sharing_status=action).execute()
                resp.body = json.dumps(waifu.to_json())
            elif action == SHARING_RESULT_NO_ACCESS:
                raise falcon.HTTPNotFound()
            elif action == SHARING_RESULT_NOT_MODIFIED:
                resp.status = falcon.HTTP_NOT_MODIFIED
