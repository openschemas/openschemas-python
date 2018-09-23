# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from openschemas.utils.managers import YamlManager
from .mapping import load_tsv
import os
import sys

class SpecValidator:
    '''the spec validator can "sniff" a file based on extension, and validate
       the file based on the extension, or have one of the specific type 
       validators (html, yaml) called directly.
    '''

    def __str__(self):
        return '[spec-validator:%s]' % self.name

    def __repr__(self):
        return self.__str__()

    def __init__(self, infile):

        self.load(infile)

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
        if self.validate_infile(infile):
            self.name = os.bath.basename(self.infile)
            self.folder = os.path.dirname(self.infile)
            self.defaults = SpecDefaults(self.name, self.folder)
            self.spec = YamlManager(self.infile)
            print('%s loaded successfully, see "spec" attribute' % infile)
            return self.spec.load()


    def validate_infile(self, infile):
        '''determine filename of infile 
           based on Specification Name (and extension). If the extension
           doesn't end in yml/yaml or html, it's not valid (and note
           we will need to add support for reading json)

           Parameters
           ==========
           name: the name of the specification
        '''
        extensions = ['yaml', 'yml', 'html']
        for ext in extensions:
            if infile.endswith(ext) and os.path.exists(name):
                print('Found %s, valid name' % infile)
                self.infile = os.path.abspath(infile)
                return True

        # Tell the user doesn't have valid, show which are
        valids = ','.join(extensions)
        print('%s does not have a valid extension (%s)' % (infile, valids))
        return False

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


    def validate_headers(self):
        '''Ensure that headers for specific files only conform to those
           required and expected 
        '''
        paths = self.defaults.get_paths()
        for key, path in paths.items():

            # This is a list of lists, the first list is the header row
            content = load_tsv(path)
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

    def load_name(self, name):
        '''load a tsv based on its name, the key in the self.paths lookup
        
        Parameters
        ==========
        name: the file key to load.
        '''
        if name in self.paths:
            return load_tsv(self.paths[name])

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
