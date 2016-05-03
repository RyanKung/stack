# coding:utf8
import argparse


parser = argparse.ArgumentParser(description='Stack - The Python Tool Stack')
parser.usage = 'python -m stack [-h]'
subparsers = parser.add_subparsers(title='Available options:', help='Run `copymouse COMMAND -h` to get help')

# stack new project template --remote
new_project_parser = subparsers.add_parser('new', help='Initalize a new project based an template')
new_project_parser.add_argument('project', metavar='PROJECT', type=str, help='Your project name.')
new_project_parser.add_argument('-t', '--template', metavar='PATH', type=str, help='External template path')
new_project_parser.add_argument('--remote', metavar='PATH', type=str, help='External template path')

# stack init
init_project_parser = subparsers.add_parser('init', help='Initalize a new project envirement')
init_project_parser.add_argument('--python', metavar='PATH', type=str, help='Version of Python')


# stack install
install_parser = subparsers.add_parser('install', help='Install libs from pypi or git repos')
install_parser.add_argument('module', metavar='LIB', type=str, help='Repo path or name of lib')
install_parser.add_argument('--git', metavar='LIB', type=str, help='Declare a git repo')

# stack uninstall
install_parser = subparsers.add_parser('uninstall', help='Uninstall libs')
install_parser.add_argument('module', metavar='LIB', type=str, help='Lib name')

# stack list
install_parser = subparsers.add_parser('list', help='List installed libs')

# stack python
subparsers.add_parser('python', help='Run Python')
subparsers.add_parser('repl', help='Run a iPython repl')
subparsers.add_parser('pip', help='Run Pip')
