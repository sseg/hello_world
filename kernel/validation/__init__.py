from kernel.errors import ValidationError
from jsonschema.exceptions import ValidationError as _JSONValidationError
from jsonschema import validate as _validate


def validate_input(input, schema):
    try:
        _validate(input, schema)
    except _JSONValidationError as err:
        raise ValidationError(description=str(err.__cause__)) from err
