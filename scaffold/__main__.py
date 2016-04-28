import sys
from scaffold.template import render

params = dict(project=sys.argv[-1])
render(*sys.argv[-3:-1], params)
