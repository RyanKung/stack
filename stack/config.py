# -*- coding: utf-8 -*-

import yaml
import time
import os

path = 'stack.yaml'


def exist() -> bool:
    return os.path.exists(path)


def load() -> dict:
    with open(path, 'r+') as f:
        return yaml.load(''.join(f.readlines()))


def write(data: dict) -> None:
    with open(path, 'w+') as f:
        origin = yaml.load(''.join(f.readlines()))
        if origin:
            yaml_data = dict(origin, **data)
        else:
            yaml_data = dict({'build': [str(time.time())]}, **data)
        f.write(yaml.dump(yaml_data))
