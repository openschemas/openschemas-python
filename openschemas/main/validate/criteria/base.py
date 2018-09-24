# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

# These are validation functions referenced in the default (and other)
# criteria.yml files (e.g., specification.yml)

from openschemas.logger import bot
from random import choice

def missing_function():
    '''this function is fired if the user forgets to define a "function" field
       in the check, which is technically the only required one :) It will
       always return False.
    '''
    messages = ['Ruhroh, you forgot to define the function here!',
                'Resistance is futile, and so is a check without a function.',
                'Forgetting something? Like, the function for this check?',
                'The scarecrow (today) sings "If I only had a function..."']

    message = choice(messages)
    bot.warning(message)
    return False
