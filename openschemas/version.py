# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

__version__ = "0.0.13"
AUTHOR = 'Vanessa Sochat'
AUTHOR_EMAIL = 'vsochat@stanford.edu'
NAME = 'openschemas'
PACKAGE_URL = "https://www.github.com/openschemas/openschemas-python"
KEYWORDS = 'openschemas, markdown, schemaorg, rdf'
DESCRIPTION = "openschemas python helper functions for schemaorg schemas"
LICENSE = "LICENSE"

INSTALL_REQUIRES = (
    ('pyaml', {'min_version': '17.12.1'}),
    ('requests', {'min_version': '2.18.1'})
)

TEST_REQUIRES = (
    ('pytest', {'min_version': None}),
    ('requests', {'min_version': '2.18.1'})
)

MAP2MODEL_REQUIRES = (
    ('Pygments', {'exact_version': '2.2.0'}),
    ('python-frontmatter', {'exact_version': '0.4.2'}),
    ('rdflib', {'exact_version': '4.2.2'}),
    ('rdflib-jsonld', {'exact_version': '0.4.0'}),
    ('requests', {'min_version': '2.18.1'}),
    ('ruamel.std.argparse', {'exact_version': '0.8.1'}),
    ('ruamel.yaml', {'exact_version': '0.15.31'}),
    ('ruamel.yaml.cmd', {'exact_version': '0.4.2'}),
    ('ruamel.yaml.convert', {'exact_version': '0.3.0'})
)

ALL_REQUIRES = (INSTALL_REQUIRES +
                MAP2MODEL_REQUIRES)
