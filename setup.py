# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from setuptools import setup, find_packages
import codecs
import os

################################################################################
# HELPER FUNCTIONS #############################################################
################################################################################

def get_lookup():
    '''get version and other setup.py information.
    '''
    lookup = dict()
    version_file = os.path.join('openschemas', 'version.py')
    with open(version_file) as filey:
        exec(filey.read(), lookup)
    return lookup

# Read in requirements
def get_requirements(lookup=None, key="INSTALL_REQUIRES"):
    '''get_requirements reads in requirements and versions from
    the lookup obtained with get_lookup'''

    if lookup == None:
        lookup = get_lookup()

    install_requires = []
    for module in lookup[key]:
        module_name = module[0]
        module_meta = module[1]
        if "exact_version" in module_meta:
            dependency = "%s==%s" %(module_name,module_meta['exact_version'])
        elif "min_version" in module_meta:
            if module_meta['min_version'] == None:
                dependency = module_name
            else:
                dependency = "%s>=%s" %(module_name,module_meta['min_version'])
        install_requires.append(dependency)
    return install_requires



# Make sure everything is relative to setup.py
install_path = os.path.dirname(os.path.abspath(__file__)) 
os.chdir(install_path)

# Get version information from the lookup
lookup = get_lookup()
VERSION = lookup['__version__']
NAME = lookup['NAME']
AUTHOR = lookup['AUTHOR']
AUTHOR_EMAIL = lookup['AUTHOR_EMAIL']
PACKAGE_URL = lookup['PACKAGE_URL']
KEYWORDS = lookup['KEYWORDS']
DESCRIPTION = lookup['DESCRIPTION']
LICENSE = lookup['LICENSE']
with open('README.md') as filey:
    LONG_DESCRIPTION = filey.read()

################################################################################
# MAIN #########################################################################
################################################################################


if __name__ == "__main__":

    INSTALL_REQUIRES = get_requirements(lookup)
    ALL_REQUIRES = get_requirements(lookup, 'ALL_REQUIRES')
    MAP2MODEL_REQUIRES = get_requirements(lookup, 'MAP2MODEL_REQUIRES')
    TEST_REQUIRES = get_requirements(lookup, 'TEST_REQUIRES')

    setup(name=NAME,
          version=VERSION,
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          maintainer=AUTHOR,
          maintainer_email=AUTHOR_EMAIL,
          packages=find_packages(), 
          include_package_data=True,
          zip_safe=False,
          url=PACKAGE_URL,
          license=LICENSE,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          keywords=KEYWORDS,
          setup_requires=["pytest-runner"],
          install_requires = ALL_REQUIRES,
          tests_require = TEST_REQUIRES,
          extras_require={
              'map2model': [MAP2MODEL_REQUIRES],
              'base': [INSTALL_REQUIRES],
              'all': [ALL_REQUIRES]
          },
          classifiers=[
              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',
              'Programming Language :: Python',
              'Topic :: Software Development',
              'Topic :: Scientific/Engineering',
              'Operating System :: Unix',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
          ],

          entry_points = {'console_scripts': [ 'map2model=openschemas.cli.map2model:main',
                                               'openschemas=openschemas.cli:main'] })
