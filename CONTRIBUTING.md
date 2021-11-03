# Contributing

We rely on pull requests to keep this project maintained. By participating in this project, you
agree to abide by the VMware [code of conduct](CODE-OF-CONDUCT.md).

## Setup 

Fork, then clone the repo:

    git clone git@github.com:carbonblack/carbon-black-cloud-sdk-python.git

It is recommended to use [virtualenv](https://virtualenv.pypa.io/en/latest/) to set up the project. Once you have that
you can use it to generate a virtual environment, activate it and install the package.

    $ python3 -m virtualenv ./venv
    $ source venv/bin/activate
    $ (venv) python setup.py develop

Make sure the tests pass:

    $ (venv) pytest

## Developing

Install the dev dependencies and after that it is highly recommended installing `pre-commit`. 

    $ (venv) pip install -r requirements.txt 
    $ (venv) pre-commit install
    ...

The `pre-commit` will make sure that you have the right code quality before committing your changes. 

Make sure you have written the appropriate tests and make sure that all the other tests are passing. Then push to your fork and 
[submit a pull request](https://github.com/carbonblack/carbon-black-cloud-sdk-python/compare/).

We try to respond to pull requests as quickly as possible. We may suggest
some changes or improvements or alternatives.

Some things that will increase the chance that your pull request is accepted:

* Write tests.
* Follow [PEP-8](https://www.python.org/dev/peps/pep-0008/), [flake8](https://flake8.pycqa.org/en/latest/), and clean code principles.
* Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).
* Usage of [pre-commit](https://pre-commit.com/)