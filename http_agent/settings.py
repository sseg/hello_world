from os.path import expandvars, join, dirname
from types import MappingProxyType
from typing import Union, Callable
import sys
import warnings
import yaml


def bool_if_bool_string(string: str) -> Union[str, bool]:
    normalized = string.strip().lower()
    if normalized == 'true':
        return True
    if normalized == 'false':
        return False
    return string


def expand_nested_vars(mapping: dict) -> dict:
    new = {}  # change to `new: dict` after flake8>=3.3.0
    for k, v in mapping.items():
        if hasattr(v, 'items'):
            new[k] = expand_nested_vars(v)
        elif isinstance(v, str):
            # check types once new has type declaration
            new[k] = bool_if_bool_string(expandvars(v))  # type: ignore
        elif hasattr(v, '__iter__'):
            new[k] = type(v)(expandvars(i) if isinstance(i, str) else i for i in v)
        else:
            new[k] = v
    return new


def get_config_path() -> str:
    try:
        path = sys.argv[-1]
    except IndexError:
        warnings.warn("No application configuration file provided.")
        path = ''
    return path


def get_env_loader() -> Callable:
    try:
        from dotenv import load_dotenv
        return load_dotenv
    except ImportError:
        warnings.warn("No dotenv package found: getting settings from environment.")
    return lambda file: None


def build_settings() -> MappingProxyType:
    load_dotenv = get_env_loader()
    path = ''
    try:
        path = get_config_path()
        with open(path) as fp:
            base = yaml.safe_load(fp.read())
        dotenv_path = join(dirname(path), '.env')
        load_dotenv(dotenv_path)
        as_dict = expand_nested_vars(base)
        return MappingProxyType(as_dict)
    except Exception as err:
        raise RuntimeError("Invalid settings path provided: %s" % path) from err
