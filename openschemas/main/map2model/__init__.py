# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from openschemas.main.map2model.parser import FrontMatterParser
import sys
import os

def main(config_yml=None,
         folder=None,
         output=None,
         template=None,
         repo=None):
    '''entrypoint function for map2model, when used by the openschemas client.

       Parameters
       ==========
       config: The configuration.yml. If not defined, defaults to that in PWD.
       folder: the input folder where specification subfolders are expected. 
       If not defined, defaults to "specifications"
       output: the output folder for specification files. If not defined, 
       defaults to "spec files"
       template: the template to use for the specification. Defaults to
       "template.html" provided by the module
       repo: the repository where the specification will be published.
       defaults to openschemas/specifications
    '''

    # Set the default specifications folder and configuration
    if not folder:
        folder = 'specifications'

    # Inputs and outputs, defaults to docs/spec_files
    outfolder = output or 'spec_files'
    outfolder = os.path.abspath(outfolder)
    folder = os.path.abspath(folder)

    config = config_yml or 'configuration.yml'
        
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

    spec_parser = FrontMatterParser(input_folder=folder,
                                    output_folder=outfolder,
                                    config_file_path=config,
                                    template=template,
                                    repo=repo)
    spec_parser.parse_front_matter()
    return spec_parser
