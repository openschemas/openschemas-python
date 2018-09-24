# OpenSchemas Python

[![CircleCI](https://circleci.com/gh/openschemas/openschemas-python.svg?style=svg)](https://circleci.com/gh/openschemas/openschemas-python)
[![PyPI version](https://badge.fury.io/py/openschemas.svg)](https://badge.fury.io/py/openschemas)

![https://github.com/openschemas/spec-template/raw/master/img/hexagon_square_small.png](https://github.com/openschemas/spec-template/raw/master/img/hexagon_square_small.png)

-------------------------------------------------------------------------------

This is a small module with helper functions and scripts for interacting with schema.org
specifications, provided as an [openschemas](https://www.github.com/openschemas) tool.  
Please contribute at [openschemas/openschemas-python](https://www.github.com/openschemas/openschemas-python) on
Github. Documentation will be provided as the library is developed.

# Quick Start

To install

```
git clone https://www.github.com/openschemas/openschemas-python
cd openschemas-python
python setup.py install
```

or the package is hosted on [pypi](https://pypi.org/project/openschemas/) and
can be installed with pip:

```
$ pip install openschemas

# See the version
$ openschemas --version

# Run map2model
$ map2model --config configuration.yml --folder specifications

# Run specification validator
$ openschemas validate --criteria openschemas/main/validate/criteria/dummy.yml --infile Container.html
```

For usage, please see our [documentation](https://openschemas.github.io/openschemas-python/html/usage.html) **under development**
