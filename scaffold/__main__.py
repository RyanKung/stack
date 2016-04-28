import sys
from scaffold.template import render

do = list

params = dict(project=sys.argv[-1])
do(render(*sys.argv[-3:-1], params))
