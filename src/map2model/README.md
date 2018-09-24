# OpenSchemas map2model

![https://github.com/openschemas/spec-template/raw/master/img/hexagon_square_small.png](https://github.com/openschemas/spec-template/raw/master/img/hexagon_square_small.png)

This version of **map2model** is a simplified version of Python module 
derived from the [Bioschemas Groups](http://bioschemas.org/groups/). It will help you
to create an OpenSchema intended for submission to [schemas.org](schemas.org), with
a focus on tech / hpc specifications that might not fall cleanly under strictly 
biological sciences, but support open science.

**map2model** retrieves properties and schema.org (Marginality, Cardinality and Controlled Vocabularies) 
using mapping files (in a specifications folder, see an [example here](https://www.github.com/openschemas/spec-container)) 
then classifies properties into two groups:
1. **Extended properties:** Properties that are part of the extended schema.org Type.
1. **New properties:** Properties that are new to the schema.org vocabulary or are completely new to schema.org.

After classifying the properties, **map2model** generates Markdown file(s) 
that can be interpreted by [openschemas.github.io](https://openschemas.github.io)

![map2model workflow](https://github.com/openschemas/map2model/raw/master/docs/img/map2model_workflow.png)
> If you want to modify the Flow Chart open the [xml file](docs/img/map2model_workflow.xml) and name it `map2model_workflow.png` in the *doc > img*.

## Contribute a Specification
Do you want to contribute a specification? Your workflow will look like this:

1. Create your specification easily using [Google Sheets](https://docs.google.com/spreadsheets/d/1Ty69GRzc3xuvfpEIRHjfl_9L25MNFfrKXCdwrpxYslo/edit?usp=sharing)
1. Fork the [template repository](https://www.github.com/openschemas/spec-template) and download them to it. You can also see a live example, [soec-container](https://www.github.com/openschemas/spec-container) that also has content in Github Pages. When you connect your forked repository to CircleCI it will use the [schema-builder](https://www.github.com/openschemas/schema-builder) to generate the files as artifacts or back to github pages. You can use the same `schema-builder` container to do this locally.
1. Issue a pull request to the [specifications](https://www.github.com/openschemas/specifications) repository with your contribution! This means:
   - forking the repository, cloning your fork
   - adding your `MySpecification.html` file to the `_specifications` folder
   - opening a pull request for review

We encourage this setup so that each of the specifications is maintained in a modular fashion. You can
maintain your specification (and issues / discussion around it) in its own Git repository,
to ensure modularity and version control of examples and associated documentation. We would be happy to 
create for you an `openschemas/spec-<NAME>` repository here if you want to join the Github organization
and get support from the maintainers within!

## Usage

This usage details native usage of map2model, which isn't reproducible and not the recommended approach! 
However if you are building software with it, you will need to know this. If not, we recommend first the 
[template](https://www.github.com/openschemas/spec-template) and the docker 
[openschemas/schema-builder](https://www.github.com/openschemas/schema-builder) that 
packages map2model and is used by the template.

### Requirements
These instructions are for local usage.

Before starting, please ensure you have the following installed:
1. Git [https://git-scm.com/downloads](https://git-scm.com/downloads)
1. Python 3  [https://www.python.org/downloads/](https://www.python.org/downloads/)
1. Pip [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)

### Executing map2model

Clone the **map2model** repository: ```git clone https://github.com/OpenSchemas/map2model.git```

```bash
git clone https://github.com/OpenSchemas/map2model.git
cd map2model
```

Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

If you want to add a specification, add an entry to [spec2model/configuration.yml]. This file tells map2model which specifications exist. To create a new specification, the section that you need to add includes:

```
- name: NameOfMySpec
  status: revision
  spec_type: Profile
  use_cases_url:
  version: 0.2.0
  parent_type: CreativeWork
```

For usage, ask the run.py script:

```
python3 run.py --help
usage: run.py [-h] [--config CONFIG] [--folder SPECS] [--output OUTFOLDER]
              [--template TEMPLATE] [--repo REPO]

map2model

optional arguments:
  -h, --help           show this help message and exit
  --config CONFIG      configuration.yml file, defaults to configuration.yml
                       in folder
  --folder SPECS       folder with input specification subfolders
  --output OUTFOLDER   folder to write output specification subfolders
  --template TEMPLATE  template for openschemas.github.io. Should not need
                       change.
  --repo REPO          final repo intended for specifications.
usage: run.py [-h] [--config CONFIG] [--folder SPECS] [--output OUTFOLDER]
              [--template TEMPLATE] [--repo REPO]

map2model

optional arguments:
  -h, --help           show this help message and exit
  --config CONFIG      configuration.yml file, defaults to configuration.yml
                       in folder
  --folder SPECS       folder with input specification subfolders
  --output OUTFOLDER   folder to write output specification subfolders
  --template TEMPLATE  template for openschemas.github.io. Should not need
                       change.
  --repo REPO          final repo intended for specifications.
```

See the [schema-builder](https://www.github.com/openschemas/schema-builder) for 
good examples of these various arguments.

We provide a [Google Drive sheets template](https://docs.google.com/spreadsheets/d/1Ty69GRzc3xuvfpEIRHjfl_9L25MNFfrKXCdwrpxYslo/edit?usp=sharing) that you can use to do this, and simply export each sheet as .tsv (tab separated values). This means that four files should go into your `_NameOfMySpec` folder. While your specification is a draft, the name of the folder will start with an underscore (`_NameOfMySpec`). When you are done, remove the underscore (`NameOfMySpec`).

When you are finished with your spec, run the script to generate files in *map2model > docs > spec_files*. Check that your folder is present! 

```
tree docs/spec_files
├── Container
│   ├── Container.html
│   ├── Container.yml
│   ├── examples
│   │   └── README.md
│   └── README.md
└── DataCatalog
    ├── DataCatalog.html
    ├── DataCatalog.yml
    ├── examples
    │   └── README.md
    └── README.md
```

If you are generating specifications for contribution, you will next want to 
open a pull request (PR) to update the [specifications](https://www.github.com/openschemas/specifications) repository.
Specifically, add the *.html files to the [_specifications folder](https://github.com/openschemas/specifications/tree/master/_specifications) in this repository.
