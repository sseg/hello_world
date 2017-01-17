from http_agent.settings import (
    expand_nested_vars,

)
import os


def test_expand_nested_vars():
    os.environ['AAA'] = 'VAR_A'
    os.environ['BBB'] = 'VAR_B'
    os.environ['CCC'] = 'VAR_C'
    os.environ['DDD'] = 'VAR_D'
    os.environ['EEE'] = 'VAR_E'

    menu = {
        'spam': 'planted_${AAA}_in_string',
        'ham': '$BBB with spaces',
        'eggs': {
            'eggs and spam': 'nested ${CCC}',
            'eggs, ham, and spam': ['static', '$DDD', '$EEE']
        },
        'num': 3.24,
        'implicit_bool': 'False'
    }

    expanded_menu = expand_nested_vars(menu)

    assert expanded_menu['spam'] == 'planted_VAR_A_in_string'
    assert expanded_menu['ham'] == 'VAR_B with spaces'
    assert expanded_menu['eggs']['eggs and spam'] == 'nested VAR_C'
    assert expanded_menu['implicit_bool'] is False

    nested_array = expanded_menu['eggs']['eggs, ham, and spam']
    assert nested_array[0] == 'static'
    assert nested_array[1] == 'VAR_D'
    assert nested_array[2] == 'VAR_E'

    assert expanded_menu['num'] == 3.24
