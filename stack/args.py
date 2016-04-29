# coding:utf8
import argparse


parser = argparse.ArgumentParser(description='stack - The Python Tool Stack')
parser.usage = 'python -m stack [-h]'

subparsers = parser.add_subparsers(title='Available options:', help='run `copymouse COMMAND -h` to get help')

subparsers.add_parser('init', help='initialize a project in current directory.')

start_parser = subparsers.add_parser('start', help='start to create a new project.')
start_parser.add_argument('project', metavar='PROJECT', type=str,
                          help='your project name.')

parser.add_argument('-p', '--prototype', metavar='PROTOTYPE', type=str,
                    required=True, help='[web|egg|etc..]')
parser.add_argument('-t', '--template', metavar='PATH', type=str,
                    help='external template path')
