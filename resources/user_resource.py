import json

import falcon
from models.base_model import db
from models.user_model import UserModel
from resources.middlewares.auth import set_auth_cookie, auth


class UserResource(object):

    def on_post(self, req, resp):
        with db.atomic():
            user = UserModel()
            token = user.update_token()
            user.save()
        if req.get_param('cookies') is not None:
            set_auth_cookie(resp, token)
        resp.body = json.dumps({'token': token})


class UserAuthResource(object):

    @falcon.before(auth())
    def on_post(self, req, resp):
        set_auth_cookie(resp, req.context['token'])
