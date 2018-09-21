# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

__version__ = "0.0.0"
AUTHOR = 'Vanessa Sochat'
AUTHOR_EMAIL = 'vsochat@stanford.edu'
NAME = 'openschemas'
PACKAGE_URL = "https://www.github.com/openschemas/openschemas-python"
KEYWORDS = 'openschemas, markdown, schemaorg, rdf'
DESCRIPTION = "openschemas python helper functions for schemaorg schemas"
LICENSE = "LICENSE"

INSTALL_REQUIRES = (
    ('pyaml', {'min_version': '17.12.1'}),
    ('requests', {'min_version': None})
)

TEST_REQUIRES = (
    ('pytest', {'min_version': None}),
    ('requests', {'min_version': None})
)

