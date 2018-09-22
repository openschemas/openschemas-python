#!/usr/bin/env python3

import argparse
import sys
import os

def get_parser():
    parser = argparse.ArgumentParser(description="openschemas")

    parser.add_argument("--version", dest='version', 
                         help='print the version and exit', 
                         default=False, action="store_true")
    return parser


def main():
    '''entrypoint for openschemas executable
    '''
    from openschemas.main import Client

    parser = get_parser()
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    if args.version is True:
        print(Client.version())
        sys.exit(0)        

    parser.print_help()

if __name__ == '__main__':
    main()
