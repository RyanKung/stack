# -*- coding: utf-8 -*-

import yaml
import time
import os
import stack.util as util

path = 'stack.yaml'


def exist() -> bool:
    return os.path.exists(path)


def load() -> dict:
    with open(path, 'r+') as f:
        return yaml.load(''.join(f.readlines()))


def write(data: dict) -> None:
    origin = load()
    with open(path, 'w+') as f:
        if origin:
            yaml_data = dict(origin, **data)
        else:
            yaml_data = dict({'build': [str(time.time())]}, **data)
        f.write(yaml.dump(yaml_data))


def has_venv():
    return exist() and os.path.exists('.env')


def get_prefix() -> str:
    '''
    Find out wich python should be call
    '''
    return '.env/bin/' if all((not util.is_venv(), has_venv())) else ''
