import json
from datetime import datetime

import falcon
from models.base_model import db
from models.waifu_model import WaifuModel
from resources.middlewares.auth import auth
from resources.middlewares.body_checker import body_checker

DOCS_LINK = 'https://github.com/sketchturnerr/WaifuSim-backend#waifu'


class WaifuCollectionResource(object):

    @falcon.before(auth())
    @falcon.before(body_checker(('name', 'description', 'pic', ), DOCS_LINK))
    def on_post(self, req, resp):
        with db.atomic():
            waifu = WaifuModel(**req.context['parsed_body'])
            waifu.owner = req.context['user']
            waifu.save()
        resp.body = json.dumps(waifu.to_json())


class WaifuResource(object):

    @falcon.before(auth())
    def on_get(self, req, resp):
        pass

    @falcon.before(auth())
    @falcon.before(body_checker(('name', 'description', 'pic', ), DOCS_LINK))
    def on_put(self, req, resp, id):
        with db.atomic():
            try:
                waifu = WaifuModel.get(WaifuModel.id == id, WaifuModel.owner == req.context['user'])
            except ValueError:
                # id не int, что ж, у нас явно нет такого документа.
                raise falcon.HTTPNotFound()
            waifu.name = req.context['parsed_body']['name']
            waifu.description = req.context['parsed_body']['description']
            waifu.pic = req.context['parsed_body']['pic']
            waifu.updated_at = datetime.now()
            waifu.save()
        resp.body = json.dumps(waifu.to_json())

