#!/usr/bin/env python3

import argparse
import sys
import os

def get_parser():
    parser = argparse.ArgumentParser(description="map2model")

    parser.add_argument("--config", dest='config', 
                         help='configuration.yml file, defaults to configuration.yml in folder', 
                         type=str, default=None)

    parser.add_argument("--folder", dest='specs', 
                         help='folder with input specification subfolders', 
                         type=str, default=None)

    parser.add_argument("--output", dest='outfolder', 
                         help='folder to write output specification subfolders', 
                         type=str, default=None)

    parser.add_argument("--template", dest='template', 
                         help='template for openschemas.github.io. Should not need change.', 
                         type=str, default=None)

    parser.add_argument("--repo", dest='repo', 
                         help='final repo intended for specifications.', 
                         type=str, default='openschemas/specifications')

    return parser


def main():
    '''entrypoint for run.py script.
    '''
    from openschemas.main.map2model import main
    
    parser = get_parser()
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    spec_parser = main(folder=args.specs,
                       output=args.outfolder,
                       config_yml=args.config,
                       template=args.template,
                       repo=args.repo)

if __name__ == '__main__':
    main()
