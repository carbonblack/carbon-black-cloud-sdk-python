# Carbon Black Cloud Python SDK

**Latest Version:** 1.0.0a1
<br>
**Release Date:** TBD

[![Coverage Status](https://coveralls.io/repos/github/carbonblack/cbc-sdk-python/badge.svg?t=cwMaub)](https://coveralls.io/github/carbonblack/cbc-sdk-python)
[![Codeship Status for carbonblack/cbc-sdk-python](https://app.codeship.com/projects/9e55a370-a772-0138-aae4-129773225755/status?branch=develop)](https://app.codeship.com/projects/402767)


## Recent updates

View the latest release notes [here](https://github.com/carbonblack/cbc-sdk-python/releases).


## License

Use of the Carbon Black API is governed by the license found in [LICENSE](LICENSE).

## Support

1. View all API and integration offerings on the [Developer Network](https://developer.carbonblack.com) along with reference documentation, video tutorials, and how-to guides.
2. Use the [Developer Community Forum](https://community.carbonblack.com/) to discuss issues and get answers from other API developers in the Carbon Black Community.
3. Create a github issue for bugs and change requests. Formal [Carbon Black Support](http://carbonblack.com/resources/support/) coming with v1.0.

## Requirements

The Carbon Black Cloud Python SDK is design to work on Python 3.6 and above.

All requirements are installed as part of `pip install cbc_sdk` or if you're planning on pushing changes to the Carbon Black Cloud Python SDK, the following can be used after cloning the repo `pip install -r requirements.txt`

### Carbon Black Cloud
* [Platform](https://developer.carbonblack.com/reference/carbon-black-cloud/platform-apis/)
* [Endpoint Standard](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-defense/)
* [Audit and Remediation](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/)
* [Enterprise EDR](https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/)


### Python Packages
| Product | Package |
| ------- | ------- |
| Audit and Remediation | [cbc_sdk.audit_remediation](src/cbc_sdk/audit_remediation) |
| Endpoint Standard | [cbc_sdk.endpoint_standard](src/cbc_sdk/endpoint_standard) |
| Enterprise EDR | [cbc_sdk.enterprise_edr](src/cbc_sdk/enterprise_edr) |
| Platform | [cbc_sdk.platform](src/cbc_sdk/platform) |


## Getting Started

Visit the [Getting Started Guide](carbon-black-cloud-python-sdk.readthedocs.io/en/latest/getting-started.html) for an example of authenticating and making an API call using the SDK.


## Developing Improvements for the Carbon Black Cloud Python SDK

Use the following steps if you want to provide additional examples, fix a bug, or add a feature to the SDK.

### Installing for SDK development

You will need to fork the repo in order to create pull requests when submitting code for review. For details on forking a repo, see [here](https://help.github.com/en/github/getting-started-with-github/fork-a-repo).

```
git clone https://github.com/{fork-name}/cbc-sdk-python
cd cbc-sdk-python
pip install -r requirements.txt
```

If you want to test/execute the eample scripts from the repo then install the SDK with the following command. This will install the SDK in editable mode so changes to the repo modify the installed package.

```
pip install -e .
```

**Note: The above command needs to be run from the base folder of the repo**


### Running the SDK tests

From the parent directory `cbc-sdk-python`, run the following command:

``pytest``

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

**Note:** if your develop branch is out of sync with the CarbonBlack repo then you will need to sync your fork. For information on syncing your fork, see [here](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork).
