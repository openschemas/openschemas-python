# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python


from openschemas.logger import bot
from subprocess import (
    Popen,
    PIPE,
    STDOUT
)
import errno
import json
import os
import re
import shutil
import sys
import yaml

################################################################################
## FOLDER OPERATIONS ###########################################################
################################################################################


def mkdir_p(path):
    '''mkdir_p attempts to get the same functionality as mkdir -p
    :param path: the path to create.
    '''
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            bot.error("Error creating path %s, exiting." % path)
            sys.exit(1)


def get_installdir():
    return os.path.dirname(os.path.abspath(__file__))

def find_subdirectories(basepath):
    '''
    Return directories (and sub) starting from a base
    '''
    directories = []
    for root, dirnames, filenames in os.walk(basepath):
        new_directories = [d for d in dirnames if d not in directories]
        directories = directories + new_directories
    return directories

    
def find_directories(root,fullpath=True):
    '''
    Return directories at one level specified by user
    (not recursive)
    '''
    directories = []
    for item in os.listdir(root):
        # Don't include hidden directories
        if not re.match("^[.]",item):
            if os.path.isdir(os.path.join(root, item)):
                if fullpath:
                    directories.append(os.path.abspath(os.path.join(root, item)))
                else:
                    directories.append(item)
    return directories

 
def copy_directory(src, dest, force=False):
    ''' Copy an entire directory recursively
    '''
    if os.path.exists(dest) and force is True:
        shutil.rmtree(dest)

    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            bot.error('Directory not copied. Error: %s' % e)
            sys.exit(1)




################################################################################
## FILE OPERATIONS #############################################################
################################################################################


def write_file(filename, content, mode="w"):
    '''write_file will open a file, "filename" and write content, "content"
    and properly close the file
    '''
    with open(filename, mode) as filey:
        filey.writelines(content)
    return filename


def write_json(json_obj, filename, mode="w", print_pretty=True):
    '''write_json will (optionally,pretty print) a json object to file

    Parameters
    ==========
    json_obj: the dict to print to json
    filename: the output file to write to
    pretty_print: if True, will use nicer formatting
    '''
    with open(filename, mode) as filey:
        if print_pretty:
            filey.writelines(
                json.dumps(
                    json_obj,
                    indent=4,
                    separators=(
                        ',',
                        ': ')))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


def read_file(filename, mode="r", readlines=True):
    '''write_file will open a file, "filename" and write content, "content"
    and properly close the file
    '''
    with open(filename, mode) as filey:
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


def read_json(filename, mode='r'):
    '''read_json reads in a json file and returns
    the data structure as dict.
    '''
    with open(filename, mode) as filey:
        data = json.load(filey)
    return data


################################################################################
## YAML ########################################################################
################################################################################


def read_yaml(filename, mode='r', quiet=False):
    '''read a yaml file, only including sections between dashes
    '''
    metadata = {}
    with open(filename, mode) as stream:
        stream = stream.read()

    # Read yaml section
    section = stream.split('---')[1]
    docs = yaml.load_all(section)
    for doc in docs:
        if isinstance(doc, dict):
            for k,v in doc.items():
                if not quiet:
                    print('%s: %s' %(k,v))
                metadata[k] = v
    return metadata




################################################################################
# environment / options
################################################################################

def load_module(module_str):
    '''load a module based on a string name.

       Parameters
       ==========
       module_str: complete python path to module (and function). Note that this
       MUST be a python module (module.py) and not a function in an __init__.py
    '''
    module_str, function = module_str.rsplit('.', 1)
    module = __import__(module_str, fromlist=[''])
    return getattr(module, function)
    

def convert2boolean(arg):
    '''convert2boolean is used for environmental variables
       that must be returned as boolean

       Parameters
       ==========
       arg: the argument (string) to parse and check for indicators of boolean
    '''
    if not isinstance(arg, bool):
        return arg.lower() in ("yes", "true", "t", "1", "y")
    return arg


def getenv(variable_key, default=None, required=False, silent=True):
    '''getenv will attempt to get an environment variable. If the variable
       is not found, None is returned.

        Parameters
        ==========
        variable_key: the variable name
        required: exit with error if not found
        silent: Do not print debugging information for variable
    '''
    variable = os.environ.get(variable_key, default)
    if variable is None and required:
        bot.error("Cannot find environment variable %s, exiting." %variable_key)
        sys.exit(1)

    if not silent:
        if variable is not None:
            bot.verbose2("%s found as %s" %(variable_key,variable))
        else:
            bot.verbose2("%s not defined (None)" %variable_key)

    return variable
