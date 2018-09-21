# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

import os
import re

import json
from openschemas.logger import bot
import subprocess
import sys

################################################################################
## REPO OPERATIONS #############################################################
################################################################################


def clone(url, tmpdir=None, branch='master'):
    '''clone a repository from Github'''
    if tmpdir is None:
        tmpdir = tempfile.mkdtemp()
    name = os.path.basename(url).replace('.git', '')
    dest = '%s/%s-%s' %(tmpdir, name, branch)
    return_code = os.system('git clone -b %s %s %s' %(branch, url, dest))
    if return_code == 0:
        return dest
    bot.error('Error cloning repo.')
    sys.exit(return_code)


def get_post_fields(request):
    '''parse through a request, and return fields from post in a dictionary
    '''
    fields = dict()
    for field,value in request.form.items():
        fields[field] = value
    return fields
