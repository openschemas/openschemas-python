# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from .file_manager import FolderDigger
from .mapping import MappingParser
from .validator import FolderValidator
from datetime import datetime
import time
import frontmatter
import os
import sys
from io import BytesIO

here = os.path.abspath(os.path.dirname(__file__))

class FrontMatterParser:
    '''the FrontEndMatterParser takes an input folder of specification
       subfolders, and a configuration.yml file, and generates a set of
       specification folders, each with a <Specification>.html file that
       can be contributed as a specification to the openschemas.github.io
       repository.
    '''

    def __init__(self, input_folder='specifications', 
                       output_folder = None,
                       config_file_path= None,
                       template = None,
                       repo = None):

        '''defaults here are intended for running in spec2map repository. 
           Use via run.py to edit for your needs.

           Parameters
           ==========
           input_folder: a folder of specification subfolders, each with .tsv
           output_folder: base to write matching output subfolders
           config_file_path: path to configuration.yml
           template.html is the template for openschemas.github.io
           repo: github <org>/<repository> for specifications 

        '''
        if config_file_path is None:
            config_file_path = '%s/configuration.yml' % here

        if template is None:
            template = '%s/templates/template.html' % here

        self.input_folder = self._check_input_folder(input_folder)
        self.template = self._check_input_folder(template)
        self.md_files_path = output_folder or 'docs/spec_files/'

        self.file_manager = FolderDigger(config_file_path)
        self.parser = MappingParser()
        self._parse_repo(repo)


    def _parse_repo(self, repo = None):
        '''parse an <ORG>/<REPO> into the full Github name, along with the
           username and reponame, and github pages. This should be for where
           the specification is to be published.

           Parameters
           ==========
           repo: should correspond to the <ORG>/<REPONAME>
        '''
        if repo is None:
            repo = 'openschemas/specifications'

        username, reponame = repo.split('/')
        self.repo = "https://www.github.com/%s" %(repo)
        self.username = username
        self.reponame = reponame
        self.ghpages = "https://%s.github.io/%s" %(username, reponame)

    def _check_input_folder(self, folder):
        '''check for the existence of the input folder, ensure full path,
           and return if exists. Exit if doesn't!
           
           Parameters
           ==========
           input_folder: path (relative or full) to input folder with specification
           subdirectories.
        '''
        folder = os.path.abspath(folder)
        if not os.path.exists(folder):
            print('Cannot find %s' % folder)
            sys.exit(1)
        print('Found folder %s' % folder)
        return folder        

    def _get_specs_list(self):
        '''return listing of specs, meaning loaded workbooks. The workbooks should
           already be validated by the file manager, and so we don't do it here.
           Each entry in the specs_list is a dictionary that includes paths to:
           mapping_file, bioschemas_file, specification_file, and authors_file.
        '''
        all_specs = dict()

        for name, params in self.specs_list.items():
            self.parser.set_metadata(params)
            all_specs[name] = self.parser.get_mapping()

        return all_specs

    def _get_specification_post(self, 
                                spec_dict, 
                                skip_fields=None,
                                info_fields=None,
                                info_key='spec_info'):
        '''from a spec_dict, derive the post material, a dictionary that
           will be converted to yaml.
 
           Parameters
           ==========
           spec_dict: a dictionary with:
               name: the name of the folder (and Specification)
               workbook: the loaded workbook (or file to it)
               params: the original values in the configuration.yml for the folder
           skip_fields: don't include subset of fields (list)
           info_fields: fields to add to "spec_info" (info_key)
           info_key: key to use for info_fields into metadata
        '''
        metadata = {}
        post = frontmatter.Post('')
        name = spec_dict['name']
        version_date = datetime.now().strftime('%Y%m%dT%H%M%S')
        info = {'version_date': version_date}

        # Skip over set of pre-defined fields
        if not skip_fields:
            skip_fields = []

        if not info_fields:
            info_fields = ['description',
                           'full_example',
                           'offical_type'
                           'subtitle',
                           'title',
                           'version',
                           "version_date"]

        # Fields specifically for openschemas template
        info['full_example'] = "%s/tree/master/%s/examples/" % (self.repo, name)

        if not isinstance(skip_fields, list):
            skip_fields = [skip_fields]

        for spec_field in spec_dict:

            # Info gets added to the metadata at the end under info_key
            if spec_field in info_fields:
                info[spec_field] = spec_dict[spec_field]
            if spec_field not in skip_fields:
                metadata[spec_field] = spec_dict[spec_field]

        metadata[info_key] = info
        post.metadata = metadata
        return post

    def _create_spec_folder_struct(self, spec_name):
        '''create a spec folder and subdirectory for examples for a 'spec_name'
           only if it doesn't exist.

           Parameters
           ==========
           spec_name: the name of the specification
        '''
        # Individual specification folder under "docs/spec_files"
        spec_dir = os.path.join(self.md_files_path, spec_name)

        # Create if doesn't exist
        if not os.path.exists(spec_dir):
            os.makedirs(spec_dir)

        # Equivalent for "examples" subfolder
        spec_exp_dir = os.path.join(spec_dir, 'examples')
        if not os.path.exists(spec_exp_dir):
            os.makedirs(spec_exp_dir)

            with open(os.path.join(spec_exp_dir, "README.md"), "w") as example_file:
                example_file.write("## %s coding examples. \n" % spec_name)
                example_file.write("Folder that stores JSON-LD, RDFa or microdata examples.\n")
                print("%s file structure created." % spec_name)

        # Either way, return the specification directory
        return spec_dir

    def _write_README(self, md_folder, spec_dict):
        '''write a README for a particular spec_md_folder
 
           Parameters
           ==========
           md_folder: a folder where a specification README should be written
           spec_dict: a dictionary with:
               name: the name of the folder (and Specification)
               workbook: the loaded workbook (or file to it)
               params: the original values in the configuration.yml for the folder
        '''
        md_file_path = os.path.join(md_folder, 'README.md')
        with open(md_file_path, "w") as readme:
 
            # Look up some fields
            name = spec_dict['name']
            version = spec_dict['version']
            spec_type = spec_dict['spec_type']
            hierarchy = spec_dict['hierarchy']
            description = spec_dict['description'] 
            subtitle = spec_dict['subtitle'].strip()

            readme.write("## %s specification v. %s \n\n" % (name, version))
            readme.write("**%s** \n\n" % spec_type)

            for i_pos, step_hier in enumerate(reversed(hierarchy)):
                readme.write(step_hier)
                if i_pos < len(hierarchy)-1:
                    readme.write(" > ")
            if spec_type == "Type":
                readme_file.write(" > %s" % name)
            readme.write("\n\n**%s** \n" % subtitle)
            readme.write("\n# Description \n")
            readme.write("%s \n" % description)
            readme.write("# Links \n")
            readme.write("- [Specification](%s/%s/)\n" % (self.ghpages, name))
            readme.write("- [Specification source](%s.html)\n" % name)
            readme.write("- [Coding Examples](%s/tree/master/examples)\n" % spec_dict['gh_folder'])
            readme.write("- [GitHUb Issues](%s)\n" % spec_dict['gh_tasks'])
            readme.write("> These files were generated using [map2model](https://github.com/openschemas/map2model) Python Module.")
        

    def save_html_template(self, data, output_name, template_file=None):
        '''save an html template, meaning a jekyll template with 
           {{OPENSCHEMAS_FRONTEND_MATTER}} to replace with front matter.
           If a template isn't defined, the default provided by the package
           is used

           Parameters
           ==========
           template_file: the jekyll template to use, provided if not defined
           output_name: the name for the output file, should end in .html
        '''
        if template_file is None:
            template_file = '%s/templates/template.html' % here

        if not output_name.endswith('.html'):
            output_name = "%s.html" % output_name

        md_fm_bytes = BytesIO()
        frontmatter.dump(data, md_fm_bytes)
        content =  str(md_fm_bytes.getvalue(), 'utf-8')

        # Read in the template, do replace
        with open(template_file, 'r') as tfile:
            template = tfile.read()
        template = template.replace('{{OPENSCHEMAS_FRONTEND_MATTER}}', content)

        # Write to file
        with open(output_name, 'w') as outfile:
            outfile.write(template)
        return output_name
    

    def parse_front_matter(self):
        '''the primary function to parse the provided front matter, the tsv
           files, and generate yml specifications from the templates
        '''
        
        # Dictionary of the entries in configuration.yml with folder name as index
        self.specs_list = self.file_manager.get_specification_list(self.input_folder)
        all_specs = self._get_specs_list()

        for spec_name, spec_dict in all_specs.items():

            # Prepare frontmatter post object with basic metadata
            post = self._get_specification_post(spec_dict)
            post.metadata['version'] = str(post.metadata['version'])
            spec_name = post.metadata['name']

            # Create folder structure (examples) and README.md
            spec_dir = self._create_spec_folder_struct(spec_name)
            self._write_README(spec_dir, spec_dict)

            # Write as output a yml and html file
            output_name =  os.path.join(spec_dir, '%s' % spec_name)
            self.save_html_template(post, output_name)
            self.file_manager.yml_config.save_yml(output_name, post.metadata)

            print('%s MarkDown file generated.' % spec_name)

        print('Generation Process Complete. Output files are in %s' % self.md_files_path)
