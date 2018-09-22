# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

import .parser as md_parser
import sys
import os

def main(config=None,
         folder=None,
         outfolder=None,
         ):
    '''entrypoint function for map2model, when used by the openschemas client.

       Parameters
       ==========
       config: The configuration.yml. If not defined, defaults to that in PWD.
       folder: the input folder where specification subfolders are expected. 
       If not defined, defaults to "specifications"
       outfolder: the output folder for specification files. If not defined, 
       defaults to "spec files"
    '''

    # Set the default specifications folder and configuration
    if not folder:
        folder = 'specifications'

    # Inputs and outputs, defaults to docs/spec_files
    outfolder = outfolder or 'spec_files'
    outfolder = os.path.abspath(outfolder)
    folder = os.path.abspath(folder)

    config = config or 'configuration.yml'
        
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
    return spec_parser
