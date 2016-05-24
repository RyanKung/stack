# coding:utf8
import argparse
import os
from .util import get_execs

current_path = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description='Stack - The Python Tool Stack')
parser.usage = 'python -m stack [-h]'
subparsers = parser.add_subparsers(title='Available options:', help='Run `copymouse COMMAND -h` to get help')


# # stack python
# subparsers.add_parser('python', help='Run Python')
# subparsers.add_parser('setup', help='Install libs from requirements')
# subparsers.add_parser('repl', help='Run a iPython repl')
# subparsers.add_parser('pip', help='Run Pip')
# subparsers.add_parser('coverage', help='Run unittest with coverage testing')
# subparsers.add_parser('test', help='Run unittest')
# subparsers.add_parser('doc', help='Gen document')

list(map(lambda x: subparsers.add_parser(x, help='Run %s' % x), get_execs()))
