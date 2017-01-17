import falcon
from falcon.request import Request as FalconRequest
from kernel.identity import Entity, EntityType, authenticate_entity
from typing import Optional
import ujson


class Request(FalconRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._body_loaded = False
        self._body = None
        self._json_body_loaded = False
        self._json_body = None

    @property
    def body(self) -> bytes:
        """Read the request body to a bytes-object and cache the result.
        """
        if not self._body_loaded:
            self._body = self._read_stream()
            self._body_loaded = True
        return self._body

    def _read_stream(self) -> str:
        return self.stream.read(self.content_length or 0)

    @property
    def json_body(self) -> dict:
        """Try to load a json request body to a python object and cache the result.
        """
        if not self._json_body_loaded:
            try:
                self._json_body = ujson.loads(self.body)
                self._json_body_loaded = True
            except ValueError as err:
                raise falcon.HTTPBadRequest(
                    description=(
                        'The supplied request body did not contain valid JSON: `{body}`'.format(
                            body=self.body.decode()
                        )
                    )
                ) from err
        return self._json_body

    @property
    def entity(self) -> Entity:
        """A representation of the authenticated requesting user.
        """
        creds = self._get_auth_declarations(self.auth)
        return authenticate_entity(**creds)

    def _get_auth_declarations(self, auth_header: Optional[str]) -> dict:
        """Get declared ID from auth header if any provided
        """
        if auth_header is None:
            return {}
        try:
            e_type, e_id = auth_header.split(':')
            return {
                'entity_type': EntityType[e_type],  # type: ignore # this is not a type dec
                'entity_id': e_id
            }
        except (ValueError, KeyError):
            raise falcon.HTTPUnauthorized(
                description="Invalid `auth` header provided. Try your request again "
                "with a header in the form 'user:<user_id>'."
            )
