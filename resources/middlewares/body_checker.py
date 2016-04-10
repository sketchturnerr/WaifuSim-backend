import json

import sys

import falcon


def body_checker(required_params=(), documentation_link=None):

    def hook(req, resp, resource, params):
        if req.content_length in (None, 0, ):
            raise falcon.HTTPBadRequest('Bad request',
                                        'В запросе деолжны быть параметры, дружок.',
                                        href=documentation_link)
        #todo: https://github.com/falconry/falcon/pull/748
        try:
            body = json.loads(req.stream.read(sys.maxsize).decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPBadRequest('Bad request',
                                        'Ты прислал плохой json, няша, попробуй прислать другой.',
                                        href=documentation_link)
        params = {}
        description = "Ты забыл параметр '%s', няша."
        for key in required_params:
            if key not in body:
                raise falcon.HTTPBadRequest('Bad request', description % key, href=documentation_link)
            params[key] = body[key]
        req.context['parsed_body'] = params

    return hook
