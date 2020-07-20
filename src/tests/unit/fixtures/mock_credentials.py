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

"""Mock for the credentials provider and credentials provider factory."""

from cbc_sdk.credentials import Credentials, CredentialProvider, CredentialProviderFactory
from cbc_sdk.errors import CredentialError


class MockCredentialProvider(CredentialProvider):
    """A mock version of the credentials provider."""
    def __init__(self, init_creds):
        """
        Initialize the MockCredentialProvider.

        Args:
            init_creds (dict): A dict mapping section names to Credentials objects.
        """
        self._creds = init_creds

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
        if section in self._creds:
            return self._creds[section]
        else:
            raise CredentialError(f"section {section} not found in credentials")


class MockCredentialProviderFactory(CredentialProviderFactory):
    """A mock version of the credentials provider factory."""
    PROVIDER = "tests.unit.fixtures.mock_credentials.MockCredentialProviderFactory"
    _known_credentials = {}

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
        return MockCredentialProvider(dict(MockCredentialProviderFactory._known_credentials))


# Shortcut definition to be loaded
MOCK_PROVIDER = MockCredentialProviderFactory.PROVIDER


def mock_credentials(section, init_data=None, **kwargs):
    """
    Used by test code to configure the credentials returned by the mock.

    Args:
        section (str): The name of the section for the credentials.
        init_data (object): Either a Credentials object or a dict mapping credential names to values.
        **kwargs (dict): Additional credential values to be used in constructing a credentials object.
    """
    if isinstance(init_data, Credentials):
        MockCredentialProviderFactory._known_credentials[section] = init_data
    else:
        MockCredentialProviderFactory._known_credentials[section] = Credentials(init_data, kwargs)
