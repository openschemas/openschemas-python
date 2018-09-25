# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

# These are validation functions referenced in the default (and other)
# For all of the below, "spec" refers to a loaded dictionary (or derivative)
# of a specification
# criteria.yml files (e.g., specification.yml)

from openschemas.logger import bot
import requests
import re

def optional(spec):
    '''optional_structure looks for a schema having optional fields, and
       issues a warning if doesn't exist. To implement this in a criteria.yml:

        checks:
            global:
              - name: Check for optional global sections and metadata
              - level: warning
              - function: openschemas.main.validate.criteria.structure.optional
    ''' 

    optional_fields = [('gh_folder', str, True, True)]
    return _test_fields(spec, optional_fields)

def required(spec):
    '''required_structure looks for a schema's required fields, and issues
       an exit if doesn't exist. To implement this in a criteria.yml:

        checks:
            global:
              - name: Check for required global sections and metadata
              - level: error
              - function: openschemas.main.validate.criteria.structure.required
    ''' 
  
    # (key, type, url, required)
    required_fields = [('description', str, False, True),
                       ('edit_url', str, True, True),
                       ('gh_tasks', str, True, True),
                       ('hierarchy', list, False, True),
                       ('mapping', list, False, True),
                       ('name', str, False, True),
                       ('parent_type', str, False, True),
                       ('spec_info', dict, False, True),
                       ('spec_type', str, False, True),
                       ('status', str, False, True),
                       ('subtitle', str, False, True),
                       ('use_cases_url', str, True, True),
                       ('version', str, False, True)]

    return _test_fields(spec, required_fields)


def spec_info(spec):
    '''test that the spec_info has all the required subfields

        spec_info:
          - name: Check that spec_info has all required subfields
          - level: error
          - function: openschemas.main.validate.criteria.structure.spec_info

    '''
    if "spec_info" not in spec:
        bot.exit('"spec_info" key is missing from specification upper level!')

    required_fields = [('description', str, False, True),
                       ('full_example', str, True, True),
                       ('version', str, False, True),
                       ('version_date', str, False, True)]

    _test_fields(spec['spec_info'], required_fields)

    # Test format of version date
    if not re.search('[0-9]{8}T[0-9]{6}', spec['spec_info']['version_date']):
        bot.exit('spec_info > version_date is malformed: "YYYYMMDDTHHMMSS"')
    return True


def semvar(spec):
    '''check that the specification uses semantic versioning

       semvar:
         - name: Check that the version strings use semantic versioning (x.x.x)
         - level: error
         - function: openschemas.main.validate.criteria.structure.semvar

    '''

    if "version" not in spec:
        bot.exit('"version" key is missing from specification upper level!')

    # We don't check for "spec_info" because this test comes after required
    if "version" not in spec["spec_info"]:
        bot.exit('"version" key is missing from spec > spec_info!')

    versions = [spec['version'],
                spec['spec_info']['version']]

    # Ensure semantic versioning
    for version in versions:
        if not re.search('[0-9]+[.][0-9]+[.][0-9]+', version):
           bot.exit('''"version" %s needs to use semantic versioning (x.x.x), 
                         see semvar.org''' % version)
    return True


def mapping(spec):
    '''test the mapping subgroup in the specification

        mapping:
          - name: Check for valid structure of list of mappings
          - level: error
          - function: openschemas.main.validate.criteria.structure.mapping

    '''

    if "mapping" not in spec:
        bot.exit('"mapping" key is missing from specification upper level!')

    required_fields = [('bsc_description', str, False, False),
                       ('cardinality', str, False, True),
                       ('controlled_vocab', str, False, False),
                       ('description', str, False, True),
                       ('example', str, False, False),
                       ('expected_types', list, False, True),
                       ('marginality', str, False, True),
                       ('parent', str, False, True),
                       ('property', str, False, True),
                       ('type', str, False, False),
                       ('type_url', str, False, False)]

    keys = [x[0] for x in required_fields]

    for entry in spec['mapping']:

        # Test required fields
        _test_fields(entry, required_fields)

        # Warning about extra fields
        extra_fields = [x for x in list(entry.keys()) if x not in keys]
        if len(extra_fields) > 0:
            bot.warning('Extra fields %s found, are they intentional?' 
                         % ','.join(extra_fields))

    return True



################################################################################
# Helpers for structure tests ##################################################
################################################################################

def _test_url(url, passing_codes=None):
    '''ensure that a url, when using "GET" returns a passing code.
       
       Parameters
       ==========
       url: the string url to get
       passing_codes: a list of passing codes
    '''
    if passing_codes is None:
        passing_codes = [200, 201]

    if not isinstance(passing_codes, list):
        passing_codes = [passing_codes]

    bot.custom(prefix='Testing', message= 'URL %s' % url, color='CYAN')
    response = requests.get(url)
    if response.status_code not in passing_codes:
        bot.exit('Invalid response code %s' % response.status_code)

def _test_fields(spec, fields):
    '''the shared function to test for a particular set of fields!
       The input spec should be a list of tuples, with each entry as:
       (key, type, url, required)

       Parameters
       ==========
       spec: the dictionary (or derivative) of the loaded specification
       fields: a list of tuples, each with (key, type, url, required)
    '''

    for entry in fields:

        name = entry[0]
        entry_type = entry[1]
        is_url = entry[2]
        required = entry[3]

        print('[field:%s}' % name)

        # Check 1. Check existence, if not valid, return
        if name not in spec:
            if required:
                bot.custom(prefix='Missing', message=spec, color='CYAN')
                bot.exit('%s is missing, invalid' % name)
            else:
                bot.test('%s is missing.' % name)
       
        else:

            # Check 2: check for type
            if not isinstance(spec[name], entry_type):
                bot.custom(prefix='Testing', message=entry, color='CYAN')
                bot.exit('Invalid type %s for %s, invalid' %(type(spec[name]), 
                                                              name)) 
            # Check 3: if URL should return 200
            if is_url: _test_url(spec[name])

            # Check 4: if required, should be present and defined
            if required:

                # Case 1: string
                if entry_type == str:
                    if spec[name] in ['', None]:
                        bot.custom(prefix='Missing', message=spec, color='CYAN')
                        bot.exit('%s is required, but not defined.' % name)

    return True
