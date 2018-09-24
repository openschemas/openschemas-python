# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from openschemas.logger import bot
from openschemas.utils import read_file
from ruamel.yaml import YAML
import frontmatter
import os
import sys
import re

class YamlManager:

    yml_path = None

    def __init__(self, yml_path = None):
        ''' on init, if a path is provided we want to tell the user quickly
            if it doesn't exist. If the path exists, we also load.
        '''
        self.yaml = YAML()
        self.loaded = {}

        # Did the user provide a path to load?
        if yml_path is not None:
            self.set_yml_path(yml_path)

    def set_yml_path(self, file_path):
        if self._validate_exists(file_path):
            self.yml_path = file_path
        else:
            bot.warning("%s does not exist." % yml_path)

    def _validate_exists(self, yml_path = None):
        '''first determine if the yml_path is defined, with preference
           to a potentially new file set by the user at runtime. If not set,
           use previously loaded file. In both cases, first check if the
           file exists. Return False if not defined or doesn't exist

           Parameters
           ==========
           yml_path: a yaml file path, if desired, to override previously set
        '''
        if not yml_path:
            yml_path = self.yml_path

        if yml_path not in ['', None]:
            if os.path.exists(yml_path):
                return True
            else:
                bot.warning("%s does not exist." % yml_path)
        else:
            bot.warning("Yaml file is not defined.")
        return False

    def load(self, file_path = None):
        '''load the yaml file depending on its extension

           Parameters
           ==========
           file_path: a yaml/html file path, if desired, to override previous
        '''

        if not file_path:
            file_path = self.yml_path

        # Read in raw content
        if self._validate_exists(file_path):

            # Read in yaml as frontend matter from html
            if file_path.endswith('html'):
                self._load_html(file_path)

            # Read in standard yaml
            else:
                self._load_yaml(file_path)
            return self.loaded

# Loading

    def _load_yaml(self, file_path, allow_duplicate_keys = True):
        '''load the yaml file

           Parameters
           ==========
           file_path: the yaml file path to read
        '''
        self.yaml.allow_duplicate_keys = allow_duplicate_keys
        stream = read_file(file_path, readlines=False)
        self.loaded = self.yaml.load(stream)
        
    def _load_html(self, file_path):
        '''load the yaml as frontend matter from an html file

           Parameters
           ==========
           file_path: an html file path to read
        '''
        stream = read_file(file_path, readlines=False)
        self.loaded = frontmatter.loads(stream).metadata

# Saving

    def save_yml(self, output_file, content=None, mode = 'w', ext='yml'):
        '''save a yml file, either provided by the client (content)
           or if not provided, the loaded content.
         
           Parameters
           ==========
           output_file: the output file to save to. Should end in yml or yaml
           content: the content to parse to yaml, can be str or dict
           mode: the mode to use (default is w, write)

        '''
        # If content isn't provided, use client loaded content (must be dict)
        if not content:
            content = self.loaded
        
        # Remove any derivation (won'account for compressed e.g., .tar.gz)
        output_file, _ = os.path.splitext(output_file)

        # Ensure ends with a yml derivative extension
        if not re.search('(%s$)' % ext, output_file):
            output_file = "%s.%s" % (output_file, ext)

        with open(output_file, mode) as outfile:
            self.yaml.dump(content, outfile)

    def save_yaml(self, output_file, content=None, mode = 'w'):
        return self.save_yml(output_file, content, mode, ext='yaml')

# Reading

    def get_key(self, key='specifications'):
        '''return a portion of the yml file based on key

           Parameters
           ==========
           key: defaults to specifications
        '''
        # If not yet loaded, load it based on extension
        if not hasattr(self, 'loaded'):
            self.load(self.yml_path)
        return self.loaded[key]
