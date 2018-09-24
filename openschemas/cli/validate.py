# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

import sys

def main(args):

    from openschemas.main import Client
    if args.basic is True:
        validator = Client.BasicValidator(infile=args.infile)
    else:
        validator = Client.SpecValidator(infile=args.infile)
    validator.validate_criteria(criteria=args.criteria)
