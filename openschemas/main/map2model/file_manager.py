# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from .config import YamlManager
from .validator import FolderValidator
import os

here = os.path.abspath(os.path.dirname(__file__))

class FolderDigger:

    yml_config = ''

    def __init__(self, config_file_path = None):
        self.specs_list = {}
        self.config_file_path = config_file_path or '%s/configuration.yml' %here
        self.yml_config = YamlManager()
       
    def get_specs(self, spec_config, input_folder):
        specs_list = {}
        for current_config in spec_config:

            # If name not defined, will skip because None
            spec_name = current_config.get('name')

            # The names of the folders and files are predictable
            spec_folder = os.path.join(input_folder, spec_name)

            # Validate specification
            validator = FolderValidator(spec_folder)
            if validator.validate():

                # Get lookup dictionary of all default files
                paths = validator.defaults.get_paths()
                current_config.update(paths)
                specs_list[spec_name] = current_config

        return specs_list

    def get_specification_list(self, input_folder):
        print("Reading Configuration file.")
        self.yml_config.set_yml_path(self.config_file_path)
        spec_config = self.yml_config.get_spec_yml_config()
        all_specs = self.get_specs(spec_config, input_folder)
        print("%s mapping files obtained." % len(all_specs))
        return all_specs
