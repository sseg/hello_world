import falcon
import ujson
from http_agent.utils import kernel_error_handler, make_entity_tag


class Greetings:
    def __init__(self, app, core):
        self.app = app
        self.core = core

    @kernel_error_handler
    def on_get(self, req, resp):
        with self.core.session(entity=req.entity) as session:
            greetings = session.do(self.core.greetings.get_all())
        resp.body = ujson.dumps(greetings)

    @kernel_error_handler
    def on_post(self, req, resp):
        with self.core.session(entity=req.entity) as session:
            greeting = session.do(self.core.greetings.add(req.json_body))
        resp.status = falcon.HTTP_201
        resp.location = '/greetings/%s' % greeting['id']
        resp.body = ujson.dumps(greeting)
        resp.set_header('ETag', make_entity_tag(resp.body))


class Greeting:
    def __init__(self, app, core):
        self.app = app
        self.core = core

    @kernel_error_handler
    def on_get(self, req, resp, greet_id):
        with self.core.session(entity=req.entity) as session:
            greeting = session.do(self.core.greetings.get(greet_id))
        body = ujson.dumps(greeting)
        etag = make_entity_tag(body)
        resp.set_header('ETag', etag)
        if req.if_none_match == etag:
            resp.status = falcon.HTTP_304
            return
        resp.body = body
        return

    @kernel_error_handler
    def on_patch(self, req, resp, greet_id):
        with self.core.session(entity=req.entity) as session:
            if req.if_none_match is not None:
                original = session.do(self.core.greetings.get(greet_id))
                if original is None:
                    raise falcon.HTTPNotFound
                original_entity_tag = make_entity_tag(ujson.dumps(original))
                if original_entity_tag != req.if_none_match:
                    raise falcon.HTTPPreconditionFailed
            patched = session.do(self.core.greetings.update(greet_id, req.json_body))
        resp.body = ujson.dumps(patched)
        resp.set_header('Etag', make_entity_tag(resp.body))

    @kernel_error_handler
    def on_delete(self, req, resp, greet_id):
        with self.core.session(entity=req.entity) as session:
            if req.if_none_match is not None:
                original = session.do(self.core.greetings.get(greet_id))
                if original is None:
                    raise falcon.HTTPNotFound
                original_entity_tag = make_entity_tag(ujson.dumps(original))
                if original_entity_tag != req.if_none_match:
                    raise falcon.HTTPPreconditionFailed
            deleted = session.do(self.core.greetings.delete(greet_id))
        resp.body = ujson.dumps(deleted)


class Do_Greet:
    def __init__(self, app, core):
        self.app = app
        self.core = core

    @kernel_error_handler
    def on_post(self, req, resp, greet_id):
        with self.core.session(entity=req.entity) as session:
            greeting = session.do(self.core.greetings.say_hello(greet_id, req.json_body))
        resp.body = ujson.dumps(greeting)


class Status:
    def __init__(self, app, core):
        self.app = app
        self.core = core

    def on_get(self, req, resp):
        resp.body = "OK"
