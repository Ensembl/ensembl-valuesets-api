# Ensembl Python Template

[![Documentation Status](https://readthedocs.org/projects/template-python/badge/?version=latest)](http://template-python.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.com/Ensembl/template-python.svg?branch=main)](https://travis-ci.com/Ensembl/template-python)

Ensembl ValueSet API Project.

This repo contains code for the ValueSets API app.
The ValueSets API expose gRPC end points for providing information
about Ensembl Value Sets.

An Ensembl `ValueSet` is a collection of key/value pairs that are related to a given topic.
For example, biotypes, APPRIS annotation terms, or transcript support level (TSL) definitions.

A ValueSet item should have the following fields:
- `accession_id` (str): value set unique identifier - e.g. "mane.select"
- `label` (str): short human friendly name - e.g. "MANE Select"
- `value` (str): short machine friendly name - e.g. "select"
- `definition` (str): short description - e.g. "A Transcript which is matched between Ensembl/GENCODE and RefSeq as part of the MANE project"
- `description` (str|None): optional and verbose definition - e.g. "The Matched Annotation from NCBI and EMBL-EBI is a collaboration between Ensembl/GENCODE and RefSeq. The MANE Select is a default transcript per human gene that is representative of biology, well-supported, expressed and highly-conserved. This transcript set matches GRCh38 and is 100% identical between RefSeq and Ensembl/GENCODE for 5' UTR, CDS, splicing and 3'UTR."

## Requirements

- pyenv (with pyenv-virtualenv plugin)
- Python 3.10+
- grpcio 
- grpcio-tools 1.30+
- openpyxl 3.\*+ (optional)

- Python packages
  - Test
    - pytest
    - pylint
    - mypy
  - Docs
    - Sphinx
    - mock
    - sphinx-rtd-theme
  - Dev
    - ipython
    - black


## Getting Started

Clone this repo:
```
git clone --depth 1 -b main https://github.com/Ensembl/ensembl-valuesets-api.git
```
Install the python part (of the pipelines) and test it:
```
pip install ./ensembl-valuesets-api

# test
# do something!
```
Run the server, listening on default port 50051:
```
python scripts/run_server.py
```

Test the server with the provided basic client:
```
python scripts/client.py
```

### Optional installation
If you need to install "editable" python package use '-e' option
```
pip install -e ./ensembl-valuesets-api
```






The following files (or folder names) will need to be modified:
- `docs/conf.py`: Change accordigly to project's name
- `docs/install.rst`: Change installation instructions accordingly
- `README.md`: Write a meaningful README for your project

Once done with the basic customisation, create the initial commit:
```
cd <NEW_PROJECT_NAME>
git add .
git commit -m 'Initial commit'
```

#### Installing the development environment (with Pyenv)

```
pyenv virtualenv 3.8 <VIRTUAL-ENVIRONMENT-NAME>
cd <NEW_PROJECT_NAME>
pyenv local <VIRTUAL-ENVIRONMENT-NAME>
pip install -r requirements-dev.txt
pip install -e .
```

#### Testing

Run test suite:
```
cd <NEW_PROJECT_NAME>
pytest
```

To run tests, calculate and display testing coverage stats:
```
cd <NEW_PROJECT_NAME>
coverage run -m pytest
coverage report -m
```


#### Generate documentation
```
cd <NEW_PROJECT_NAME>
./scripts/build_docs.sh
```
Open automatically generated documentation page at `docs/_build/html/index.html`


#### Automatic Formatting
```
cd <NEW_PROJECT_NAME>
black --check src tests
```
Use `--diff` to print a diff of what Black would change, without actually changing the files.

To actually reformat all files contained in `src` and `test`:
```
cd <NEW_PROJECT_NAME>
black src tests
```

#### Linting and type checking
```
cd <NEW_PROJECT_NAME>
pylint src tests
mypy src tests
```
Pylint will check the code for syntax, name errors and formatting style.
Mypy will use type hints to statically type check the code.

It should be relatively easy (and definitely useful) to integrate both `pylint` and `mypy`
in your IDE/Text editor.


## Resources

#### Python Documentation
- [Official Python Docs](https://docs.python.org/3/)

#### Python distributions and virtual environments management
- [Pyenv docs](https://github.com/pyenv/pyenv#readme)
- [Pyenv virtualenv docs](https://github.com/pyenv/pyenv-virtualenv#readme)

#### Auto-generating documentation
- [Spinx Docs](https://www.sphinx-doc.org/en/master/index.html)

#### Linting, type checking and formatting
- [Pylint](https://www.pylint.org/)
- [Mypy](https://mypy.readthedocs.io/en/stable/)
- [Black](https://black.readthedocs.io/en/stable/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

#### Testing
- [pytest](https://docs.pytest.org/en/6.2.x/)
- [Coverage](https://coverage.readthedocs.io/)

#### Development tools
- [IPython](https://ipython.org/)

#### Distributing
- [Packaging Python](https://packaging.python.org/tutorials/packaging-projects/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0#apply)
- [Semantic Versioning](https://semver.org/)

