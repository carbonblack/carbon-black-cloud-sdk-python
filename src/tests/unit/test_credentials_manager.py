# *******************************************************
# Copyright (c) VMware, Inc. 2020. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Tests for the CredentialsManager object."""

import pytest
from cbc_sdk.credentials import Credentials, CredentialProvider, CredentialProviderFactory, CredentialsManager, \
    _known_credentials_providers
from cbc_sdk.errors import CredentialError


class TestCredentialProvider(CredentialProvider):
    """Provider used in testing the CredentialsManager."""
    def get_credentials(self, section=None):
        """
        Return a Credentials object containing the configured credentials.

        Args:
            section (str): The credential section to retrieve.

        Returns:
            Credentials: The credentials retrieved from that source.

        Raises:
            CredentialError: If there is any error retrieving the credentials.
        """
        if section == "default":
            return Credentials({"url": "http://example.com", "token": "ABCDEFGHIJKLM", "org_key": "A1B2C3D4"})
        raise CredentialError(f"credential section {section} not found")


class TestCredentialProviderFactory(CredentialProviderFactory):
    """Provider factory used in testing the CredentialsManager."""
    def get_credential_provider(self, init_params=None):
        """
        Create the credential provider object and return it.

        Args:
            init_params (dict): Initialization parameters for the specific credential provider.

        Returns:
            CredentialProvider: The new credential provider.

        Raises:
            CredentialError: If there is any error creating the credential provider.
        """
        if init_params and init_params.get('testkey', None) == 'testvalue':
            return TestCredentialProvider()
        else:
            raise CredentialError("unable to initialize provider")


@pytest.fixture
def provider_name():
    """Provider factory name to use - also teardown for CredentialsManager"""
    yield "tests.unit.test_credentials_manager.TestCredentialProviderFactory"
    # tear down the CredentialsManager
    CredentialsManager._provider = None
    CredentialsManager._cached_credentials = {}


@pytest.fixture
def short_provider_name():
    """Short name to use to test the short-name lookup."""
    return "test_provider"


@pytest.fixture
def init_params():
    """Initialization parameters to use."""
    return {'testkey': 'testvalue'}


# === UNIT TESTS BELOW === #


def test_get_credentials(provider_name, init_params):
    """Test the basic credentials manager operations."""
    CredentialsManager.load(provider_name, init_params)
    creds = CredentialsManager.get_credentials("default")
    assert creds.url == "http://example.com"
    assert creds.token == "ABCDEFGHIJKLM"
    assert creds.org_key == "A1B2C3D4"
    creds2 = CredentialsManager.get_credentials("default")  # validate object caching
    assert creds is creds2
    with pytest.raises(CredentialError):
        CredentialsManager.get_credentials("notexist")
    with pytest.raises(CredentialError):  # validate double load failure
        CredentialsManager.load(provider_name, init_params)


def test_known_provider(provider_name, init_params, short_provider_name, monkeypatch):
    """Test the "known providers" mechanism to make sure it loads correctly."""
    monkeypatch.setitem(_known_credentials_providers, short_provider_name, provider_name)
    CredentialsManager.load(short_provider_name, init_params)
    creds = CredentialsManager.get_credentials("default")
    assert creds.url == "http://example.com"
    assert creds.token == "ABCDEFGHIJKLM"
    assert creds.org_key == "A1B2C3D4"


def test_exception_cases(provider_name, init_params, short_provider_name):
    """Test the various exception cases in CredentialsManager.load()."""
    with pytest.raises(CredentialError):
        CredentialsManager.get_credentials("default")
    with pytest.raises(CredentialError):
        CredentialsManager.load("test.notexist.NonExistentFactoryObject", init_params)
    with pytest.raises(CredentialError):
        CredentialsManager.load(short_provider_name, init_params)
    with pytest.raises(CredentialError):
        CredentialsManager.load(provider_name)
    with pytest.raises(CredentialError):
        CredentialsManager.load(provider_name, {})
    assert CredentialsManager._provider is None
