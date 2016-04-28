# -*- coding: utf-8 -*-
import re
import sys
import os

from fabric.main import main
import pdb; pdb.set_trace()
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main(os.path.abspath(__file__)))
