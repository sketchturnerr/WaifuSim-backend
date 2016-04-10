import json
from time import sleep

from app import api
from create_tables import create_tables
from falcon.testing import TestCase


def with_token_query_string(func):

    def wrapper(self):
        resp = self.simulate_post('/user')
        token = resp.json.get('token')
        return func(self, "token=%s" % token)

    return wrapper


class WaifuResourceTest(TestCase):

    def setUp(self):
        self.api = api

    @classmethod
    def setUpClass(cls):
        create_tables()

    def _create_waifu(self, token_qs):
        body = json.dumps({'name': 'foo', 'description': 'bar', 'pic': 'baz'})
        resp = self.simulate_post('/waifu', query_string=token_qs, body=body)
        return resp.json.get('id'), body

    @with_token_query_string
    def test_create_waifu_should_return_bad_request(self, token_qs):
        resp = self.simulate_post('/waifu', query_string=token_qs)
        self.assertEqual(resp.status_code, 400)
        resp = self.simulate_post('/waifu', query_string=token_qs, body='{"fooo": ')
        self.assertEqual(resp.status_code, 400)
        body = json.dumps({'name': 'foo'})
        resp = self.simulate_post('/waifu', query_string=token_qs, body=body)
        self.assertEqual(resp.status_code, 400)

    @with_token_query_string
    def test_create_waifu_should_return_waifu_object(self, token_qs):
        body = json.dumps({'name': 'foo', 'description': 'bar', 'pic': 'baz'})
        resp = self.simulate_post('/waifu', query_string=token_qs, body=body)
        self.assertEqual(resp.json.get('name'), 'foo')
        self.assertEqual(resp.json.get('description'), 'bar')
        self.assertEqual(resp.json.get('pic'), 'baz')

    @with_token_query_string
    def test_update_waifu_should_return_not_found_for_not_existing_waifu(self, token_qs):
        body = json.dumps({'name': 'foo', 'description': 'bar', 'pic': 'baz'})
        resp = self.simulate_put('/waifu/99999999', query_string=token_qs, body=body)
        self.assertEqual(resp.status_code, 404)
        resp = self.simulate_put('/waifu/fff', query_string=token_qs, body=body)
        self.assertEqual(resp.status_code, 404)

    @with_token_query_string
    def test_update_waifu_should_return_not_found_for_waifu_owned_by_another_user(self, token_qs):
        id, body = self._create_waifu(token_qs)
        resp = self.simulate_post('/user')
        token = resp.json.get('token')
        resp = self.simulate_put("/waifu/%s" % id, query_string="token=%s" % token, body=body)
        self.assertEqual(resp.status_code, 404)

    @with_token_query_string
    def test_update_waifu_should_update_and_return_waifu(self, token_qs):
        id, _ = self._create_waifu(token_qs)
        body = json.dumps({'name': 'foo1', 'description': 'bar1', 'pic': 'baz1'})
        sleep(2)
        resp = self.simulate_put("/waifu/%s" % id, query_string=token_qs, body=body)
        self.assertEqual(resp.json.get('name'), 'foo1')
        self.assertEqual(resp.json.get('description'), 'bar1')
        self.assertEqual(resp.json.get('pic'), 'baz1')
        self.assertGreater(resp.json.get('updated_at')-resp.json.get('created_at'), 1)