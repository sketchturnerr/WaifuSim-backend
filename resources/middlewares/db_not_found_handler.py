import falcon


def handler(ex, req, resp, params):
    raise falcon.HTTPNotFound()
