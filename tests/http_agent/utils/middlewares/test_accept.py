from http_agent.utils.middlewares.accept import parse_accept_header
from falcon import HTTPNotAcceptable


def test_compliant_accept_header():
    header = 'application/json; version=1'
    parsed = parse_accept_header(header)
    assert parsed[0] == 'application/json'
    assert parsed[1] == 1


def test_wildcard_accept_header():
    header = '*/*; version=1'
    parsed = parse_accept_header(header)
    assert parsed[0] == '*/*'
    assert parsed[1] == 1


def test_no_content_type_raises():
    header = 'version=1'
    try:
        parse_accept_header(header)
    except HTTPNotAcceptable:
        pass
    else:
        assert False, "Expected error"


def test_no_version_raises():
    header = 'application/json'
    try:
        parse_accept_header(header)
    except HTTPNotAcceptable:
        pass
    else:
        assert False, "Expected error"


def test_integer_version_raises():
    header = '*/*; version=1.0.dev'
    try:
        parse_accept_header(header)
    except HTTPNotAcceptable:
        pass
    else:
        assert False, "Expected error"
