# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

# These are validation functions referenced in the default (and other)
# criteria.yml files (e.g., specification.yml)

def optional(infile):
    '''optional_structure looks for a schema having optional fields, and
       issues a warning if doesn't exist. To implement this in a criteria.yml:

        checks:
            global:
              - name: Check for optional global sections and metadata
              - level: warning
              - function: openschemas.main.validate.criteria.optional_structure
    ''' 
    print('hallo moto! write me dinosaur!')
    return True

def required(infile):
    '''required_structure looks for a schema's required fields, and issues
       an error if doesn't exist. To implement this in a criteria.yml:

        checks:
            global:
              - name: Check for required global sections and metadata
              - level: error
              - function: openschemas.main.validate.criteria.required_structure
    ''' 
    print('hallo moto! write me dinosaur!')
    return True
