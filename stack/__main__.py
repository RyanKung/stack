# -*- coding: utf-8 -*-
import re
import sys
# from fabric.main import main
from stack.args import parser

if __name__ == '__main__':
    parser.parse_args()
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    # sys.exit(main([os.path.abspath(__file__)]))
