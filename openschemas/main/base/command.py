# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from openschemas.main.base.logger import println
from openschemas.utils import run_command as run_cmd
from openschemas.logger import bot

import subprocess
import json
import sys
import os
import re



def init_command(self, action, flags=None):
    '''return the initial Singularity command with any added flags.
        
       Parameters
       ==========
       action: the main action to perform (e.g., build)
       flags: one or more additional flags (e.g, volumes) 
       not implemented yet.
    '''
    cmd = ['singularity', action ]

    if self.quiet is True:
        cmd.insert(1, '--quiet')
    if self.debug is True:
        cmd.insert(1, '--debug')

    return cmd


def run_command(self, cmd, sudo=False, capture=True):
    '''run_command is a wrapper for the global run_command, checking first
       for sudo and exiting on error if needed. The message is returned as
       a list of lines for the calling function to parse, and stdout uses
       the parent process so it appears for the user.

       Parameters
       ==========
       cmd: the command to run
       sudo: does the command require sudo?
       On success, returns result. Otherwise, exists on error
    '''
    result = run_cmd(cmd, sudo=sudo, capture=capture, quiet=self.quiet)
    message = result['message']
    return_code = result['return_code']
        
    if result['return_code'] == 0:
        if len(message) == 1:
            message = message[0]
        return message

    if self.quiet is False:
        bot.error("Return Code %s: %s" %(return_code,
                                         message))
