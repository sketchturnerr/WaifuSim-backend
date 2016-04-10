def with_token_query_string(func):

    def wrapper(self):
        resp = self.simulate_post('/user')
        token = resp.json.get('token')
        return func(self, "token=%s" % token)

    return wrapper