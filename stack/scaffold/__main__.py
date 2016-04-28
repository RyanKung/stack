import sys
from scaffold.template import render
from typing import Generator, Any
from types import GeneratorType
from functools import reduce
from operator import concat

params = dict(project=sys.argv[-1], __project__=sys.argv[-1])


def do(xs: Generator):
    def expand(xs: Any):
        if isinstance(xs, GeneratorType) or hasattr(xs, '__iter__'):
            return [expand(i) for i in xs]
        else:
            return xs
    return reduce(lambda x, y: concat(x, expand(y)), xs, [])

res = do(render(*sys.argv[-2:], params))
