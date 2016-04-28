# coding:utf8

import os
import re
import string
import logging
from operator import contains
from functools import partial
from typing import Iterable
from scaffold.types import IO
from itertools import starmap, chain

__all__ = ['render']

VALID_FILENAMES = set(['.gitignore'])
VALID_PROJECT = re.compile('[a-zA-Z0-9.-]{2,}')


def filename_template(n: str, params: dict, placeholder='project') -> str:
    '''replace placeholder from filename'''
    return n.replace('__%s__' % placeholder, params[placeholder])


def is_invalid_folder(n: str) -> bool:
    '''A valid folder should not startwith .'''
    return n.startswith('.')


def is_invalid_path(n: str) -> bool:
    '''A valid folder should not startwith .'''
    return any(filter(partial(contains, n), ['.git', '.venv']))


def is_invalid_file(n: str) -> bool:
    '''A valid file should not end with pyc or pyo or py~(emacs temp file)'''
    return any([contains(VALID_FILENAMES, n),
                n.startswith('.'),
                n.endswith(('.pyc', '.pyo', '.py~'))])


def render(src: str, dist: str, params: dict) -> Iterable:
    '''recursionly parse and replace files as string.template with params
    from to dist'''

    if not os.path.exists(dist):
        os.mkdir(dist)

    def map_files(filename: str, current: str, target: str) -> IO:
        '''file and filename mapper'''
        if is_invalid_file(filename) or is_invalid_path(current):
            return None
        logging.info('mapping file %s from %s to %s' % (filename, current, target))
        filename = filename_template(filename, params)
        srcpath, distpath = os.path.join(current, filename), os.path.join(target, filename)
        with open(srcpath, 'r') as f:
            content = string.Template(f.read())
        with open(distpath, 'w') as f:
            f.write(content.safe_substitute(params))

    def map_folders(name: str, current: str, target: str) -> IO:
        '''folder napper'''
        if is_invalid_folder(name) or is_invalid_path(current):
            return None
        logging.info('maping folder %s from %s to %s' % (name, current, target))
        foldername = filename_template(name, params)
        os.mkdir(os.path.join(target, foldername))

    def render_all(current, folders, files):
        '''map and render all'''
        target = filename_template(current.replace(src, dist), params)
        return chain(map(partial(map_folders, current=current, target=target), folders),
                     map(partial(map_files, current=current, target=target), files))

    return starmap(render_all, os.walk(src))
