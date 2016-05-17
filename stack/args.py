# coding:utf8
import argparse
import os

current_path = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description='Stack - The Python Tool Stack')
parser.usage = 'python -m stack [-h]'
subparsers = parser.add_subparsers(title='Available options:', help='Run `copymouse COMMAND -h` to get help')

# # stack new project template --remote
# new_project_parser = subparsers.add_parser('new', help='Initalize a new project based an template')
# new_project_parser.add_argument('project', metavar='PROJECT', type=str, help='Your project name.')
# new_project_parser.add_argument('-t', '--template', metavar='template', type=str, help='External template path', default='%s/template/default' % current_path)
# new_project_parser.add_argument('--remote', metavar='PATH', type=str, help='External template path')

# # stack init
init_project_parser = subparsers.add_parser('init', help='Initalize a new project envirement')
init_project_parser.add_argument('--python', metavar='PATH', type=str, help='Version of Python')


# stack install
install_parser = subparsers.add_parser('install', help='Install libs from pypi or git repos')
install_parser.add_argument('lib', metavar='LIB', type=str, help='Repo path or name of lib')
install_parser.add_argument('--repo', metavar='repo', type=str, help='Install via a git repo')
install_parser.add_argument('--git', metavar='git', type=str, help='Declare is a git repo', default=False)

# stack uninstall
install_parser = subparsers.add_parser('uninstall', help='Uninstall libs')
install_parser.add_argument('lib', metavar='LIB', type=str, help='Lib name')

# stack list
install_parser = subparsers.add_parser('list', help='List installed libs')

# stack_serve
serve_parser = subparsers.add_parser('serve', help='Serve current dir as git server')
serve_parser.add_argument('--ip', help='IP addr')
serve_parser.add_argument('--port', help='Port')


# stack python
subparsers.add_parser('clear', help='Clear and delete virtual envirement')
subparsers.add_parser('python', help='Run Python')
subparsers.add_parser('setup', help='Install libs from requirements')
subparsers.add_parser('repl', help='Run a iPython repl')
subparsers.add_parser('pip', help='Run Pip')
subparsers.add_parser('coverage', help='Run unittest with coverage testing')
subparsers.add_parser('test', help='Run unittest')
subparsers.add_parser('doc', help='Gen document')
