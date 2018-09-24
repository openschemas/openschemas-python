# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from openschemas.utils.managers import YamlManager
from openschemas.main.base import RobotNamer
from openschemas.logger import bot
from openschemas.utils import load_module
import os
import sys

class SpecValidator:
    '''the spec validator can "sniff" a file based on extension, and validate
       the file based on the extension, or have one of the specific type 
       validators (html, yaml) called directly. There are two steps.

       Step 0. validates the file itself. Does it exist? Load without error?
       Step 1. validates the file against a criteria.yml, default is provided
    '''

    def __str__(self):
        return '[spec-validator:%s]' % self.name

    def __repr__(self):
        return self.__str__()

    def __init__(self, infile, critera=None):

        self.load(infile)
        self.load_criteria(criteria)
        self.robot = RobotNamer()

# Loading

    def load(self, infile):
        '''load an input file, meaning checking for the file's existence,
           that it has a default extension, and loading it into the "spec"
           via the YamlManager (that can handle frontmatter in a html or
           standard yml/yaml

           Parameters
           ==========
           infile: the input file to load
        '''
        # Step 0. of validation checks exist and load of file
        self.infile = self.validate_exists(infile)
        if self.infile is not None:

            # If the fie exists, we can store metadata about it
            self.name = os.bath.basename(self.infile)
            self.folder = os.path.dirname(self.infile)
            self.defaults = SpecDefaults(self.name, self.folder)

            # We only return a manager if the file loads cleanly.
            self.spec =  self.validate_loads(infile) # returns YamlManager
            if self.spec is not None:
                return self.spec.load()


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
        default_criteria = '%s/criteria/specification.yml' % here
        if criteria is None:
            criteria = default_criteria

        # Attempt to load (and validate) the criteria (returns YamlManager)
        self.criteria = self.validate_loads(criteria)

        # Again fall back to default if error loading user-provided
        if self.criteria is None:
            self.criteria = self.validate_loads(default_criteria)

        bot.info('[criteria:%s]' % self.criteria.yml_path)
        return self.criteria.load()

# Criteria

    def validate_criteria(self, infile=None, criteria=None):
        '''validate an infile (or already loaded one) against criteria.

           Parameters
           ==========
           infile: an input specification file
           criteria: a loaded (json/dict) or criteria, or html/yml file
        '''   
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
        missing_function = 'openschemas.main.validate.criteria.missing_function'

        # Turn status into meaningful message for user
        lookup = {True: 'pass', False: 'fail', None: 'null'}         

        # Loop through checks, run against specification file
        for group, checks in criteria['checks'].items():
            print('[group:%s] ---- <start>' % group)
            values = dict()
            [values.update(dict(check)) for check in checks]
            
            # Obtain values, the only required is the function
            name = values.get('name', robot.generate())  
            level = values.get('level', 'warning').upper()
            function = values.get('function', missing_function)
            kwargs = values.get('kwargs')

            # If we have a function provided in the configuration yaml
            function_name = function
            function = load_module(function)

            if not kwargs:
                result = function(infile)
            else:
                result = function(infile, **kwargs)

            # The logger will exit with -1 if error or below
            bot.named(level, function_name)

            print('[check:%s]' % name)
            print(' test:function %s -->' % function_name)
            print(' test:result ------->' % lookup[result])
            print(' test:level -------->' % level)
            print('[group:%s] ---- <end>' % group)
            bot.message()

# Validation

    def validate_exists(self, infile, extensions=None):
        '''determine filename of infile 
           based on Specification Name (and extension). If the extension
           doesn't end in yml/yaml or html, it's not valid (and note
           we will need to add support for reading json). If valid,
           return the filename. If not, return None.

           Parameters
           ==========
           name: the name of the specification / yaml file
           extensions: a list of valid extensions
        '''
        if extensions == None:
            extensions = ['yaml', 'yml', 'html']

        if not isinstance(extensions, (list,tuple)):
            extensions = [extensions]

        for ext in extensions:
            if infile.endswith(ext) and os.path.exists(name):
                print('Found %s, valid name' % infile)
                return os.path.abspath(infile)

        # Tell the user doesn't have valid, show which are
        valids = ','.join(extensions)
        print('%s does not have a valid extension (%s)' % (infile, valids))

    def validate_loads(self, infile):
        '''determine if a file can load without error. If yes, return manager.
           If not, return None.
           
           Parameters
           ==========
           infile: the input file to attempt loading with the YamlManager,
           can be yaml or front end matter in html.
        '''
        manager = YamlManager(infile)
        try:
            manager.load()
            return manager
        except:
            bot.warning('Load of %s not successfully, using default' % infile)
     
   
# Getting

    def _check_spec(self):
        '''any validation requires a loaded spec, which must be done with
           either initialization of the validator, or the load() function
        '''
        if hasattr(self, 'spec'):
            return True
        print('You must .load() a yaml or html with frontend matter first')
        return False

    def get(self, key=None):
        '''get the loaded content. if key is None, return the entire thing!
           Otherwise return a key index into the yaml

           Parameters
           ==========
           key: a key index to return, otherwise return entire thing
        '''
        if self._check_spec():
            spec = self.spec.load()
            if key is not None and key in spec:
                spec = spec[key]                
            return spec


# Validating

    def validate(self, infile=None, criteria=None):
        '''validate runs each set of tests, and returns a list of results.
           If any validators fail, we return a False (failed) validation,
           otherwise True
       
           Parameters
           ==========
           infile: if provided, load new infile (to share a validator instance)
           criteria: a criteria.yml file to validate from. If not provided,
           we use the template.

        '''
        if infile is not None:
            self.load(infile)

        # If we have/had a loaded spec, this is True
        if self._check_spec():

            # Step 1.
            results = [self.validate_keys(infile),
                       self.validate_paths()]

            # First validate existing and paths
            for result in results:
                if not result:
                    return False

            # Only then try to read files!
            if not self.validate_headers():
                return False

        return result


    def validate_headers(self, content):
        '''Ensure that headers for specific files only conform to those
           required and expected 
        '''
        paths = self.defaults.get_paths()
        for key, path in paths.items():

            # This is a list of lists, the first list is the header row
            found = content[0]

            # Default headers expected, including capitalization
            headers = self.defaults.get_headers(key)

            # Missing or extra currently not allowed
            missing_headers = [x for x in headers if x not in found]
            extra_headers = [x for x in found if x not in headers]
            if len(missing_headers) + len(extra_headers) > 0:
                print('Invalid: Extra or missing headers for %s' % path)
                return False

        return True

    def validate_extension(self, path, ext='tsv'):
        '''Ensure the worksheet is a tsv file (default ends in tsv)
 
           Parameters
           ==========
           path: a name (string) of the worksheet file
           ext: the extension to check using "endswith"
        '''
        if not path.endswith(ext):
            print('Invalid: Worksheet %s must have extension %s' % (path, ext))
        return path.endswith(ext)
        

class SpecDefaults:
    infile = None
    name = None
    ext = None

    def __init__(self, name, folder=None):
        self.sniff_filename(name)
        self.paths = self.set_paths(folder)
 
    def get_names(self):
        return self.lookup

    def get_paths(self):
        return self.paths


    def set_paths(self, folder=None):
        '''define expected set of file (fullpath) from names lookup with
           a folder name.

           Parameters
           ==========
           name: the name of the specification
        '''
        paths = {}
        if folder is not None:
            for key, filename in self.lookup.items():
                paths[key] = os.path.join(folder, filename)
        return paths


    def get_headers(self, key):
        '''get a headers list for a particular key in the names of
           defaults.
   
           Parameters
           ==========
           key: the key in the self.lookup to get default headers for
        '''
        headers = {'specification_file': ['Title',
                                          'Subtitle',
                                          'Description',
                                          'Version',
                                          'Official Type',
                                          'Full Example'],

                   'mapping_file': ['Property',
                                    'Expected Type',
                                    'Description',
                                    'Type',
                                    'Type URL',
                                    'BSC Description',
                                    'Marginality',
                                    'Cardinality',
                                    'Controlled Vocabulary',
                                    'Example'],

                   'authors_file': ['Firstnames', 
                                    'Surname', 
                                    'Role', 
                                    'Institution',
                                    'Contribution'],

                   'bioschemas_file': ["Property",
                                       "Expected Type",
                                       "Description",
                                       "Type",
                                       "Type URL",
                                       "BSC Description",
                                       "Marginality",
                                       "Cardinality",
                                       "Controlled Vocabulary",
                                       "Example"]}

        if key in self.lookup:
            if key in headers:
                return headers[key]
