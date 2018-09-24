# Usage

The `openschemas`  python module serves several command line utils along with 
python functions for interacting with the set of openschemas tools.

## map2model

For complete map2model usage, see the [map2model](https://www.github.com/openschemas/map2model) repository.

## Validator

The validator can be called from the command line, as shown below:

```
$ openschemas validate --criteria openschemas/main/validate/criteria/dummy.yml --infile ../specifications/_specifications/Container.html
Found ../specifications/_specifications/Container.html, valid name
Found openschemas/main/validate/criteria/dummy.yml, valid name
[criteria:dummy.yml]
Found /home/vanessa/Documents/Dropbox/Code/openschemas/specifications/_specifications/Container.html, valid name
[group:pass] ----- <start
Roses are red, violets are blue, here is a, it is True
[check:Dummy criteria that always returns warning]
 test:function openschemas.main.validate.criteria.base.dummy
 test:result pass
 test:level LOG
LOG openschemas.main.validate.criteria.base.dummy
[group:pass] ----- end>
[group:fail] ----- <start
If I were a rich man, well then I wouldn't be a dinosaur.
[check:Dummy criteria that always returns log]
 test:function openschemas.main.validate.criteria.base.dummy
 test:result fail
 test:level ERROR
ERROR openschemas.main.validate.criteria.base.dummy
```

or from interactive Python:

```
from openschemas.main import Client
validator = Client.SpecValidator(infile="Container.yml")
validator.validate_criteria(criteria="dummy.yml")
```

Take a look at the [dummy.yml](openschemas/main/validate/criteria/dummy.yml)
if you want to test, and a specification from the [specifications](https://www.github.com/openschemas/specifications/)
repository.

## Development

### Validation
The default specification.yml provided here does very basic checks for a specification,
and it's more likely the case that you want to write your own set of validation
criteria for a specification that you are working on. In fact, you can use
this library as a way to write general tests for any data structure against
a set of criteria (more on this later). Let's start out with a basic case
of wanting to write a new set of tests. The first thing you should do is create
some `criteria.yml` (or similarly named) file, and create chunks that look 
like this:

```yaml
version: 1
checks:
    mycheck:
      - name: This check will always print a message and pass
      - level: log
      - function: openschemas.main.validate.criteria.base.dummy
```

The function itself can be anywhere, as long as you provide the full path
to the python module (a `module.py` file, not an __init__.py file)
as shown above. In the example above, the function "dummy" would be
defined in the file `base.py`.

Once you write this file, you can use it with a `<Specification>.html` as is
shown above, or if you prefer, you can load a custom data file (not necessarily
a specification) as follows:

```python
from openschemas.main import Client
validator = Client.BasicValidator(infile="Container.yml")
validator.validate_criteria(criteria="dummy.yml")
```

How to write a test?

 - Your tests should take, as first argument, some spec variable. It's positional so naming isn't so important.
 - You can either handle exiting in the function, or return False if a test fails.
 - You are free to use whatever logging or printing you desire! Generally, it's a good idea to provide a user with enough information to see what is being tested, and any requirements to debug if a test is not passing.

