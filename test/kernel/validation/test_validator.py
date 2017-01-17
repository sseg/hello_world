from kernel.validation import validate_input, ValidationError


def test_valid_input():
    payload = {
        'foo': 'bar'
    }
    schema = {
        'properties': {
            'foo': {
                'type': 'string'
            }
        }
    }
    try:
        validate_input(payload, schema)
    except ValidationError:
        assert False, "Did not expect validation error"
    else:
        assert True


def test_invalid_input_raises_error():
    payload = {
        'foo': True
    }
    schema = {
        'properties': {
            'foo': {
                'type': 'string'
            }
        }
    }
    try:
        validate_input(payload, schema)
    except ValidationError:
        return  # OK
    else:
        assert False, "Expected an error"
