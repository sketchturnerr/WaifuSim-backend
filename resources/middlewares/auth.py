from conf import Conf
import falcon
from peewee import DoesNotExist
from models.user_model import UserModel, USER_ROLE_USER


def set_auth_cookie(resp, token):
    resp.set_cookie('token', token, max_age=Conf.get('max_auth_cookie_age', 86400*15))


def auth(required_role=USER_ROLE_USER):

    def hook(req, resp, resource, params):
        #todo: hooks.py:151: DeprecationWarning:
        token = req.get_param('token')
        token = token or req.cookies.get('token')
        if token is None:
            raise falcon.HTTPUnauthorized(
                'Auth token required',
                'Тут нужна кука или quary-параметр `token`, анончик.', False,
                href='https://github.com/sketchturnerr/WaifuSim-backend/new/master#auth')
        try:
            user = UserModel.get(UserModel.token_hash == UserModel.generate_token_hash(token))
        except DoesNotExist:
            raise falcon.HTTPUnauthorized(
                'Invalid token',
                'У тебя невалидный токен, няша :C', False,
                href='https://github.com/sketchturnerr/WaifuSim-backend/new/master#auth')
        if user.role < required_role:
            raise falcon.HTTPNotFound()
        req.context['user'] = user
        req.context['token'] = token
    return hook
