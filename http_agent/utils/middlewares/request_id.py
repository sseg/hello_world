from uuid import uuid4


class RequestIDMiddleware:
    def __init__(self, settings):
        self.rid_header_name = settings['headers']['request_attribution_id']

    def process_request(self, req, _resp):
        rid = req.get_header(self.rid_header_name) or str(uuid4())
        req.id = rid

    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header(self.rid_header_name, req.id)
