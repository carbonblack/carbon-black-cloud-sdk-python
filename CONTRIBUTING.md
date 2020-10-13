# Contributing

We rely on pull requests to keep this project maintained. By participating in this project, you
agree to abide by the VMware [code of conduct](CODE-OF-CONDUCT.md)

Fork, then clone the repo:

    git clone git@github.com:carbonblack/cbc-sdk-python.git

Set up your machine:

    python3 -m virtualenv ./venv
    source venv/bin/activate
    python3 setup.py develop

Make sure the tests pass:

    pytest

Make your change. Add tests for your change. Make the tests pass:

    pytest

Push to your fork and [submit a pull request](https://github.com/carbonblack/cbc-sdk-python/compare/).

We try to respond to pull requests as quickly as possible. We may suggest
some changes or improvements or alternatives.

Some things that will increase the chance that your pull request is accepted:

* Write tests.
* Follow [PEP-8](https://www.python.org/dev/peps/pep-0008/), [flake8](https://flake8.pycqa.org/en/latest/), and clean code principles.
* Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).
