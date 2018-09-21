# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

def parse_verbosity(self, args):
    '''parse_verbosity will take an argument object, and return the args
       passed (from a dictionary) to a list

       Parameters
       ==========
       args: the argparse argument objects

    '''

    flags = []

    if args.silent is True:
       flags.append('--silent')
    elif args.quiet is True:
        flags.append('--quiet')
    elif args.debug is True:
       flags.append('--debug')
    elif args.verbose is True:
       flags.append('-' + 'v' * args.verbose)

    return flags
