import json
from datetime import datetime

import falcon
from models.base_model import db
from models.user_to_waifu_model import UserToWaifuModel
from models.waifu_model import WaifuModel
from resources.middlewares.auth import auth
from resources.middlewares.body_checker import body_checker

DOCS_LINK = 'https://github.com/sketchturnerr/WaifuSim-backend#user-waifu'


class UserWaifuResource(object):

    @falcon.before(auth())
    def on_get(self, req, resp):
        user = req.context['user']
        waifus = user.waifus
        if len(waifus) == 0:
            raise falcon.HTTPNotFound()
        else:
            # todo: rename related field
            resp.body = json.dumps(waifus[0].waifu.to_json())

    @falcon.before(auth())
    @falcon.before(body_checker(('id', ), DOCS_LINK))
    def on_post(self, req, resp):
        id = req.context['parsed_body']['id']
        user = req.context['user']
        waifu = WaifuModel.get_by_id_and_user(id, user)
        waifus = user.waifus
        with db.atomic():
            if len(waifus) > 0:
                waifus[0].update(created_at=datetime.now(), waifu=waifu).execute()
            else:
                UserToWaifuModel.create(user=user, waifu=waifu)
        resp.body = json.dumps(waifu.to_json())
