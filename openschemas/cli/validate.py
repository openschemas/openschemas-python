# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

import sys

def main(args):

    from openschemas.main import Client
    validator = Client.validator(infile=args.infile)
    validator.validate_criteria(criteria=args.criteria)
