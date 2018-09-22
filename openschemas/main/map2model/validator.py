# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from .mapping import load_tsv
import os
import sys

class FolderValidator:

    def __str__(self):
        return '[folder-validator:%s]' % self.name

    def __repr__(self):
        return self.__str__()

    def __init__(self, folder):

        self.folder = os.path.abspath(folder)
        self.name = os.path.basename(folder)
        self.defaults = WorksheetDefaults(self.name, folder)

    def validate(self, folder=None):
        '''validate runs each set of tests, and returns a list of results.
           If any validators fail, we return a False (failed) validation,
           otherwise True
        '''
        results = [self.validate_exists(folder),
                   self.validate_paths()]


        # First validate existing and paths
        for result in results:
            if not result:
                return False

        # Only then try to read files!
        if not self.validate_headers():
            return False

        return result

    def validate_exists(self, folder=None):
        '''Ensure the folder exists
 
           Parameters
           ==========
           folder: full (or relative) path to folder
        '''        
        if folder is None:
            folder = self.folder

        print('Looking for %s...' % folder)
        if not os.path.exists(folder):
            print('Invalid: Worksheet folder %s does not exist' % folder)
            return False
        return True

    def validate_paths(self, ext='tsv'):
        '''Ensure that default files (self.defaults) exist in the folder
           (self.folder) 
        '''
        paths = self.defaults.get_paths()
        for key, path in paths.items():

            # 1. The path must exist
            if not os.path.exists(path):
                print('Invalid: Cannot find %s' % path)
                return False

            # 2. If changed the defaults, we wouldn't be able to load
            if not self.validate_extension(path, ext=ext):
                return False
 
        return True

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
        

class WorksheetDefaults:
    
    def __init__(self, name, folder=None):
        self.name = name
        self.lookup = self.set_names(name)
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

    def set_names(self, name, ext='tsv'):
        '''define expected set of file names (basepath) 
           based on Specification Name

           Parameters
           ==========
           name: the name of the specification
        '''
        lookup = {'mapping_file': '%s - Mapping.%s' % (name, ext),
                  'specification_file': '%s - Specification.%s' % (name, ext),
                  'bioschemas_file': '%s - Bioschemas.%s' % (name, ext),
                  'authors_file': '%s - Authors.%s' % (name, ext)}
        return lookup


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
