from http_agent.utils.middlewares.request_id import RequestIDMiddleware
from http_agent.utils.middlewares.accept import AcceptMiddleware


def make_middlewares(settings):
    return [
        RequestIDMiddleware(settings),
        AcceptMiddleware(settings)
    ]
