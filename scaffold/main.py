import sys
from scaffold.template import render
import argparse

params = dict(project=sys.argv[-1], __project__=sys.argv[-1])
parser = argparse.ArgumentParser(description='Scaffold')
subparsers = parser.add_subparsers(title='Available options:', help='Run `copymouse COMMAND -h` to get help')
new_project_parser = subparsers.add_parser('new', help='Initalize a new project based an template')
new_project_parser.add_argument('project', metavar='PROJECT', type=str, help='Your project name.')
new_project_parser.add_argument('template', metavar='PATH', type=str, help='External template path')
new_project_parser.add_argument('--remote', metavar='PATH', type=str, help='External template path')


def main():
    args = parser.parse_args()
    template_params = dict(project=args.project, __project__=args.project)
    list(render(args.template, args.project, template_params))
    return
