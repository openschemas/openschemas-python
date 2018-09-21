# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

import os

def init_level(self, quiet=False):
    '''set the logging level based on the environment
        
       Parameters
       ==========
       quiet: boolean if True, set to quiet. Gets overriden by environment
              setting, and only exists to define default

    '''
        
    if os.environ.get('MESSAGELEVEL') == "QUIET":
        quiet = True

    self.quiet = quiet



def println(self, output, quiet=False):
    '''print will print the output, given that quiet is not True. This
       function also serves to convert output in bytes to utf-8

       Parameters
       ==========
       output: the string to print
       quiet: a runtime variable to over-ride the default.

    '''
    if isinstance(output,bytes):
        output = output.decode('utf-8')
    if self.quiet is False and quiet is False:
        print(output)
