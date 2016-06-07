# coding: utf8

import argparse
from .client import main as client
from .server import main as server

parser = argparse.ArgumentParser(description='wsh')
subparsers = parser.add_subparsers(title='Available options:', help='Run `wsh COMMAND -h` to get help')
subparsers.add_parser('--server', metavar='server', help='run as server')
subparsers.add_parser('--client', metavar='client', help='run as client')
subparsers.add_parser('--host', metavar='host')
subparsers.add_parser('--port', metavar='port')


def main(args=parser.parse_args()):
    if args.server:
        return server(host=args.host, port=args.port)
    if args.client:
        return client(host=args.host, port=args.port)
