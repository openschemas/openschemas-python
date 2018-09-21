# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from openschemas.logger import bot

import json
import sys
import os
import re

from .command import ( init_command, run_command )
from .flags import parse_verbosity
from .logger import ( println,  init_level )
from .generate import RobotNamer

class Client:

    def __str__(self):
        return "[openschemas-python]"

    def __repr__(self):
        return self.__str__()

    def version(self):
        '''return the version
        '''
        from openschemas.version import __version__
        return __version__



# Commands
Client._init_command = init_command
Client._run_command = run_command

# Flags and Logger
Client._parse_verbosity = parse_verbosity
Client._println = println
Client._init_level = init_level
Client.RobotNamer = RobotNamer()
