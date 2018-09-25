# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from openschemas.logger import bot

import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

      
################################################################################
# Supporting (shared) functions ################################################
################################################################################


def validate_loads(infile):
    '''determine if a file can load without error. If yes, return manager.
       If not, return None.
           
       Parameters
       ==========
       infile: the input file to attempt loading with the YamlManager,
       can be yaml or front end matter in html.
    '''
    from openschemas.utils.managers import YamlManager

    manager = YamlManager(infile)
    try:
        manager.load()
        return manager
    except:
        bot.warning('Load of %s not successfully, using default' % infile)


def load_criteria(self, criteria=None):
    '''load a criteria.yml file. If not specified, load (or reload)
       default provided by package.

       Parameters
       ==========
       criteria: a yml specification for criteria. If not provided, use
        default at criteria/specification.yml. If you need help creating
       a new criteria (that might be added to defaults) please open an issue
    '''
    # First pass - criteria file defined, and exists
    if criteria is not None:
        if os.path.exists(criteria):
            criteria = self.validate_exists(criteria)
            
    # Second pass, use default provided by library
    if criteria is None:
         criteria = self.default_criteria

    # Attempt to load (and validate) the criteria (returns YamlManager)
    self.criteria = validate_loads(criteria)

    # Again fall back to default if error loading user-provided
    if self.criteria is None:
        self.criteria = validate_loads(default_criteria)

    basename = os.path.basename(self.criteria.yml_path)

    bot.info('[criteria:%s]' % basename)
    return self.criteria.load()


def validate_criteria(self, criteria, infile=None):
    '''validate an infile (or already loaded one) against criteria.

       Parameters
       ==========
       infile: an input specification file
       criteria: a loaded (json/dict) or criteria, or html/yml file
    '''   
    from openschemas.utils import load_module
        
    # Read in the criteria - any errors will fall back to default
    if not isinstance(criteria, dict):
        criteria = self.load_criteria(criteria)

    # Also need an input file, load
    if infile is None:
        if not self.infile:
            bot.error('Please provide an infile to function, or load()')
        infile = self.infile

    # Same for infile, user can provide already loaded
    if not isinstance(infile, dict):
        infile = self.load(infile)

    if "checks" not in criteria:
        bot.error('criteria is missing "checks" section, exiting.')

    # Default missing function
    missing_function = 'openschemas.main.validate.criteria.base.missing'

    # Turn status into meaningful message for user
    lookup = {True: 'pass', False: 'fail', None: 'null'}         

    # Loop through checks, run against specification file
    for group, checks in criteria['checks'].items():

        print('[group|start:%s]' % group)
        values = dict()
        [values.update(dict(check)) for check in checks]
            
        # Obtain values, the only required is the function
        name = values.get('name', self.robot.generate())  
        level = values.get('level', 'warning').upper()
        function = values.get('function', missing_function)
        kwargs = values.get('kwargs')

        # If we have a function provided in the configuration yaml
        function_name = function
        function = load_module(function)

        if kwargs is None:
            valid = function(infile)
        else:
            values = dict()
            [values.update(dict(kwarg)) for kwarg in kwargs]
            valid = function(infile, **values)

        print('[check:%s]' % name)
        print(' test:function %s' % function_name)
        print(' test:result %s' % lookup[valid])

        if valid:
            bot.test("PASSED %s" % function_name)
        else:
            print(' test:level %s' % level)
            bot.named(level, function_name)
            if not valid:
                sys.exit(1)

        print('[group|end:%s]' % group)

    print('ALL TESTS PASSING')
