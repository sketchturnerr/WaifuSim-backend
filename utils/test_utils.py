import json


def with_token_query_string(func):

    def wrapper(self):
        resp = self.simulate_post('/user')
        token = resp.json.get('token')
        return func(self, "token=%s" % token)

    return wrapper


def create_waifu(tast_case, token_qs):
    body = json.dumps({'name': 'foo', 'description': 'bar', 'pic': 'baz'})
    resp = tast_case.simulate_post('/waifu', query_string=token_qs, body=body)
    return resp.json.get('id'), body
