# coding: utf8

import sys
from require.run import run_remote
import argparse

params = dict(project=sys.argv[-1], __project__=sys.argv[-1])
parser = argparse.ArgumentParser(description='Require')
subparsers = parser.add_subparsers(title='Available options:', help='Run `copymouse COMMAND -h` to get help')
new_project_parser = subparsers.add_parser('run', help='Initalize a new project based an template')
new_project_parser.add_argument('file', metavar='project', type=str, help='The remote file name.')


def main(args=parser.parse_args()):
    run_remote(args.file)
