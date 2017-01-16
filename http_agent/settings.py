from os.path import expandvars, join, dirname
from types import MappingProxyType
import sys
import warnings
import yaml


try:
    from dotenv import load_dotenv
    with_dotenv = True
except ImportError:
    warnings.warn("No dotenv package found: getting settings from environment.")
    with_dotenv = False


def expand_nested_vars(mapping):
    new = {}
    for k, v in mapping.items():
        if hasattr(v, 'items'):
            new[k] = expand_nested_vars(v)
        elif isinstance(v, str):
            new[k] = expandvars(v)
            normalized = new[k].strip().lower()
            if normalized == 'true':
                new[k] = True
            if normalized == 'false':
                new[k] = False
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


def build_settings() -> MappingProxyType:
    path = ''
    try:
        path = get_config_path()
        with open(path) as fp:
            base = yaml.safe_load(fp.read())
        if with_dotenv:
            dotenv_path = join(dirname(path), '.env')
            load_dotenv(dotenv_path)
        as_dict = expand_nested_vars(base)
        return MappingProxyType(as_dict)
    except Exception as err:
        raise RuntimeError("Invalid settings path provided: %s" % path) from err
