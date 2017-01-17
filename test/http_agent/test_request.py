from http_agent.request import Request, EntityType
from falcon.testing.helpers import create_environ
from falcon import HTTPBadRequest, HTTPUnauthorized
from unittest import mock


def test_request_body_prop():
    body = """
        A	B	C	D	E	F	G	H
        8	♖	♘	♗	♕	♔	♗	♘	♖
        ​...
    """
    env = create_environ(body=body)
    req = Request(env)
    assert req.body == body.encode()


def test_request_json_body_prop():
    body = '''{
        "key": null
    }'''
    env = create_environ(body=body)
    req = Request(env)
    assert req.json_body == {"key": None}


def test_request_json_body_prop_invalid_raises_400():
    body = ""
    env = create_environ(body=body)
    req = Request(env)

    try:
        req.json_body
    except HTTPBadRequest:
        pass
    else:
        assert False, "Expected an error to be raised"


def test_request_entity_prop():
    headers = {}
    sentinel = object()
    env = create_environ(headers=headers)
    req = Request(env)
    with mock.patch('http_agent.request.authenticate_entity') as mock_entity_factory:
        mock_entity_factory.return_value = sentinel
        assert req.entity is sentinel
        mock_entity_factory.assert_called_once_with()


def test_request_entity_prop_from_header():
    headers = {'Authorization': 'admin:1234'}
    sentinel = object()
    env = create_environ(headers=headers)
    req = Request(env)
    with mock.patch('http_agent.request.authenticate_entity') as mock_entity_factory:
        mock_entity_factory.return_value = sentinel
        assert req.entity is sentinel
        mock_entity_factory.assert_called_once_with(
            entity_type=EntityType['admin'],
            entity_id='1234'
        )


def test_request_entity_prop_invalid_entity_type_raises_401():
    headers = {'Authorization': 'invalid_user_type:1234'}
    env = create_environ(headers=headers)
    req = Request(env)
    try:
        req.entity
    except HTTPUnauthorized:
        pass
    else:
        assert False, "Expected an error to be raised"


def test_request_entity_prop_malformed_header_raises_401():
    headers = {'Authorization': '11532145'}
    env = create_environ(headers=headers)
    req = Request(env)
    try:
        req.entity
    except HTTPUnauthorized:
        pass
    else:
        assert False, "Expected an error to be raised"
