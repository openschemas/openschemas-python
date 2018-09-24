#!/usr/bin/env python3

# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

import argparse
import sys
import os

def get_parser():
    parser = argparse.ArgumentParser(description="openschemas")

    parser.add_argument("--version", dest='version', 
                         help='print the version and exit', 
                         default=False, action="store_true")

    subparsers = parser.add_subparsers(help='description',
                                       title='actions',
                                       description='actions for openschemas',
                                       dest="command", metavar='general usage')

          
    validate = subparsers.add_parser("validate",
                                      help="validate a specification")

    validate.add_argument("--basic", dest='basic', 
                         help='use the basic validator, without extra checks and loading', 
                         default=False, action="store_true")

    validate.add_argument('--criteria', nargs='?',
                           help="define custom entry criteria (critera.yml)", 
                           default=None, type=str)

    validate.add_argument('--infile', nargs='?',
                           help="input file to validate", 
                           default=None, type=str)

    return parser


def get_subparsers(parser):
    '''get_subparser will get a dictionary of subparsers, to help with printing help
    '''

    actions = [action for action in parser._actions 
               if isinstance(action, argparse._SubParsersAction)]

    subparsers = dict()
    for action in actions:
        # get all subparsers and print help
        for choice, subparser in action.choices.items():
            subparsers[choice] = subparser

    return subparsers


def main():
    '''entrypoint for openschemas executable
    '''
    from openschemas.main import Client

    parser = get_parser()
    subparsers = get_subparsers(parser)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    if args.version is True:
        print(Client.version())
        sys.exit(0)        

    if args.command == "validate":
        from .validate import main
        main(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
