import json

from falcon.testing import TestCase
from app import api
from create_tables import create_tables
from utils.test_utils import with_token_query_string, create_waifu


class UserResourceTest(TestCase):

    def setUp(self):
        # todo: move this to base class
        self.api = api

    @classmethod
    def setUpClass(cls):
        # todo: move this to base class
        create_tables()

    @with_token_query_string
    def test_get_user_waifu_should_return_not_found(self, token_qs):
        resp = self.simulate_get('/user/waifu', query_string=token_qs)
        self.assertEqual(resp.status_code, 404)

    @with_token_query_string
    def test_post_user_waifu_should_return_not_found(self, token_qs):
        resp = self.simulate_post('/user/waifu', query_string=token_qs, body='{"id": -1}')
        self.assertEqual(resp.status_code, 404)

    @with_token_query_string
    def test_post_user_waifu_should_add_waifu(self, token_qs):
        id, _ = create_waifu(self, token_qs)
        body = json.dumps({'id': id})
        resp = self.simulate_post('/user/waifu', query_string=token_qs, body=body)
        self.assertEqual(resp.json.get('id'), id)
        resp = self.simulate_get('/user/waifu', query_string=token_qs)
        self.assertEqual(resp.json.get('id'), id)

    @with_token_query_string
    def test_post_user_waifu_should_replace_waifu(self, token_qs):
        id, _ = create_waifu(self, token_qs)
        body = json.dumps({'id': id})
        resp = self.simulate_post('/user/waifu', query_string=token_qs, body=body)
        self.assertEqual(resp.json.get('id'), id)

        id, _ = create_waifu(self, token_qs)
        body = json.dumps({'id': id})
        resp = self.simulate_post('/user/waifu', query_string=token_qs, body=body)
        self.assertEqual(resp.json.get('id'), id)

        resp = self.simulate_get('/user/waifu', query_string=token_qs)
        self.assertEqual(resp.json.get('id'), id)
