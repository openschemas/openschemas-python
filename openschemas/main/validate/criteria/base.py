# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

# These are validation functions referenced in the default (and other)
# criteria.yml files (e.g., specification.yml)

from openschemas.logger import bot
from random import choice

def missing(spec):
    '''this function is fired if the user forgets to define a "function" field
       in the check, which is technically the only required one :) It will
       always return False.
    '''
    messages = ['Ruhroh, you forgot to define the function here!',
                'Resistance is futile, and so is a check without a function.',
                'Forgetting something? Like, the function for this check?',
                'The scarecrow (today) sings "If I only had a function..."']

    message = choice(messages)
    print(message)
    return False


def dummy(spec, passing=True):
    '''dummy can be used for testing, it returns the status given as an argument

       Parameters
       ==========
       spec: the input spec, in json format (dict)
       passing: boolean to return True or False (default is True)
    '''
    msg = "not True"
    if passing:
        msg = "True"

    messages = ['Roses are red, violets are blue, here is a test, it is %s' % msg,
                "If I were a rich man, well then I wouldn't be a dinosaur.",
                "Sweet dreams are made of cheese, who am I to diss a brie?"]

    message = choice(messages)
    print(message)
    return passing
