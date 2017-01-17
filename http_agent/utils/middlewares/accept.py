from typing import Tuple
import falcon


def parse_accept_header(header: str) -> Tuple[str, int]:
    try:
        split = header.split(';')
        ctype, version_dec = split[0], split[1]
        version_split = version_dec.strip().split('=')
        assert version_split[0].strip() == 'version'
        version = int(version_split[1].strip())
        return ctype.strip(), version
    except Exception as err:
        raise falcon.HTTPNotAcceptable(
            description='The supplied Accept header was not valid: `{accept_header_value}`. '
                        'Your header should include an acceptable content-type and an API version. '
                        'For example: `*/*; version=1`'.format(
                            accept_header_value=header
                        )
        ) from err


class AcceptMiddleware:
    def __init__(self, settings):
        self.ignored_paths = frozenset([
            '/status'
        ])

    def process_request(self, req, resp):
        if req.path in self.ignored_paths:
            return

        content_type, version = parse_accept_header(req.accept)

        # TODO: use version for API versioning
        # requires https://github.com/falconry/falcon/issues/967
        assert version == 1

        # TODO: dispatch to handler based on accepted content-type
        assert content_type in ('application/json', '*/*')

        req.env['HTTP_ACCEPT'] = content_type
