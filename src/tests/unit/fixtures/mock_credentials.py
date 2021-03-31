# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Mock for the credentials provider."""

from cbc_sdk.credentials import CredentialProvider
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
