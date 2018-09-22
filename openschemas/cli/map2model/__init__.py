#!/usr/bin/env python3

import openschemas.main.map2model.parser as md_parser
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

    parser = get_parser()
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    # Set the default specifications folder and configuration
    folder = args.specs
    if not folder:
        folder = 'specifications'

    # Inputs and outputs, defaults to docs/spec_files
    outfolder = args.outfolder or 'docs/spec_files'
    outfolder = os.path.abspath(outfolder)
    folder = os.path.abspath(folder)

    config = args.config or 'spec2model/configuration.yml'
        
    # Output folder we may need to make
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    print('Configuration file set to %s' % config)
    print('Output folder set to %s' % outfolder)
    print('Input folder set to %s\n' % folder)

    # Both must exist
    for path in [config, folder]:
        if not os.path.exists(path):
            print('Error, %s not found.' % path)
            sys.exit(1)

    spec_parser = md_parser.FrontMatterParser(input_folder=folder,
                                              output_folder=outfolder,
                                              config_file_path=config,
                                              template=args.template,
                                              repo=args.repo)
    spec_parser.parse_front_matter()
    

if __name__ == '__main__':
    main()
