from app import api
from create_tables import create_tables
from falcon.testing import TestCase
from models.user_model import UserModel


class UserResourceTest(TestCase):

    def setUp(self):
        self.api = api

    @classmethod
    def setUpClass(cls):
        create_tables()

    def test_create_user_should_return_token(self):
        resp = self.simulate_post('/user')
        self.assertIn('token', resp.json)
        token = resp.json.get('token')
        hash = UserModel.generate_token_hash(token)
        user = UserModel.get(UserModel.token_hash == hash)
        self.assertEqual(user.token_hash, hash)

    def test_create_user_with_cookies_should_set_cookies(self):
        resp = self.simulate_post('/user', query_string='cookies=1')
        cookies = resp.headers.get('set-cookie', '')
        token = resp.json.get('token')
        self.assertIn("token=%s" % token, cookies)

    def test_auth_should_return_token_required(self):
        resp = self.simulate_post('/user/auth')
        self.assertEqual(resp.json.get('title'), 'Auth token required')

    def test_auth_should_return_invalid_token(self):
        resp = self.simulate_post('/user/auth', query_string='token=foobar')
        self.assertEqual(resp.json.get('title'), 'Invalid token')
        resp = self.simulate_post('/user/auth', headers={'Cookie': 'token=foobar'})
        self.assertEqual(resp.json.get('title'), 'Invalid token')

    def test_auth_should_authorize_user(self):
        user_resp = self.simulate_post('/user')
        token = user_resp.json.get('token')
        resp = self.simulate_post('/user/auth', query_string="token=%s" % token)
        cookies = resp.headers.get('set-cookie', '')
        self.assertIn("token=%s" % token, cookies)
