# VMware Carbon Black Cloud Python SDK

**Latest Version:** 1.0.1
<br>
**Release Date:** 17 December 2020

[![Coverage Status](https://coveralls.io/repos/github/carbonblack/carbon-black-cloud-sdk-python/badge.svg?t=Id6Baf)](https://coveralls.io/github/carbonblack/carbon-black-cloud-sdk-python)
[![Codeship Status for carbonblack/carbon-black-cloud-sdk-python](https://app.codeship.com/projects/9e55a370-a772-0138-aae4-129773225755/status?branch=develop)](https://app.codeship.com/projects/402767)



## Recent updates

View the latest release notes [here](https://github.com/carbonblack/carbon-black-cloud-sdk-python/releases).


## License

Use of the Carbon Black Cloud Python SDK is governed by the license found in [LICENSE](https://github.com/carbonblack/carbon-black-cloud-sdk-python/blob/develop/LICENSE).

## Support

1. View all API and integration offerings on the [Developer Network](https://developer.carbonblack.com) along with reference documentation, video tutorials, and how-to guides.
2. Use the [Developer Community Forum](https://community.carbonblack.com/) to discuss issues and get answers from other API developers in the Carbon Black Community.
3. Create a github issue for bugs and change requests or create a ticket with [Carbon Black Support](http://carbonblack.com/resources/support/).

## Documentation

Visit [ReadTheDocs](https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/) for this project's documentation.

## Requirements

The Carbon Black Cloud Python SDK is design to work on Python 3.6 and above.

All requirements are installed as part of `pip install carbon-black-cloud-sdk`. If you're planning on pushing changes to the Carbon Black Cloud Python SDK, the following can be used after cloning the repo `pip install -r requirements.txt`

### Carbon Black Cloud

At least one Carbon Black Cloud product is required to use this SDK:

* [Platform](https://developer.carbonblack.com/reference/carbon-black-cloud/platform-apis/)
* [Endpoint Standard](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-defense/)
* [Audit and Remediation](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/)
* [Enterprise EDR](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/)

_Note: Support for the latest products such as Workloads and Containers are planned for early 2021_

### Python Packages

- requests
- cachetools
- pyyaml
- pika
- prompt_toolkit
- pygments
- python-dateutil
- protobuf
- solrq
- validators

If developing the SDK, you also need:

- pytest==5.4.2
- pymox==0.7.8
- coverage==5.1
- coveralls==2.0.0
- flake8==3.8.1
- flake8-colors==0.1.6
- flake8-docstrings==1.5.0


## Getting Started

Visit the [Getting Started Guide](https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/getting-started) for an example of authenticating and making an API call using the SDK.

### Setting the User-Agent

The SDK supports custom User-Agent's when making API calls. This allows you to identify yourself when using the SDK. See [Setting the User-Agent](https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/getting-started#setting-the-user-agent) section of the documentation for more information.

## Developing Improvements for the Carbon Black Cloud Python SDK

Use the following steps if you want to provide additional examples, fix a bug, or add a feature to the SDK.

### Installing for SDK development

You will need to fork the repo in order to create pull requests when submitting code for review. For details on forking a repo, see [here](https://help.github.com/en/github/getting-started-with-github/fork-a-repo).

```
git clone https://github.com/{fork-name}/carbon-black-cloud-sdk-python
cd carbon-black-cloud-sdk-python
pip install -r requirements.txt
```

If you want to test/execute the eample scripts from the repo then install the SDK with the following command. This will install the SDK in editable mode so changes to the repo modify the installed package.

```
pip install -e .
```

**Note: The above command needs to be run from the base folder of the repo**


### Running the SDK tests

From the parent directory `carbon-black-cloud-sdk-python`, run the command `pytest`.

### Building the documentation

ReadTheDocs hosts [the documentation for the SDK](https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/). If you make changes to the SDK that require an update to the documentation, first install the documentation packages from pip:

```
pip install sphinxcontrib-apidoc
pip install sphinx_rtd_theme
```

Then, build the docs locally with the following commands:

```
sphinx-apidoc -f -o docs src/cbc_sdk
cd docs
make html
```

The documentation is built in `docs/_build/html`.

### Development Flow

To begin a code change, start by creating a branch off of the develop branch.
```
git checkout develop
git checkout -b {branch-name}
```

When the feature or bug fix is finished you will need to create a pull request to the CarbonBlack repo, the following will push your changes to Github.
```
git push {remote} {branch-name}
```

If your branch is behind the develop branch, you will need to rebase.
```
git checkout {branch-name}
git rebase develop
```

**Note:** if your develop branch is out of sync with the Carbon Black repo then you will need to sync your fork. For information on syncing your fork, see [here](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork).
