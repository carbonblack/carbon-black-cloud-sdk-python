# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2025. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Credentials provider that reads the credentials from the macOS's keychain."""

import sys
import keyring
import json
from cbc_sdk.credentials import Credentials, CredentialProvider
from cbc_sdk.errors import CredentialError


class KeychainCredentialProvider(CredentialProvider):
    """This credential provider reads from the macOS's Keychain."""
    def __init__(self, keychain_name, keychain_username):
        """
        Initialize the KeychainCredentialProvider.

        Args:
            keychain_name (str): The name of the entry in the Keychain.
            keychain_username (str): The username which you've set in the Keychain.

        Raises:
            CredentialError: If we attempt to instantiate this provider on a non-macOS system.
        """
        self._usable = "darwin" in sys.platform
        if not self._usable:
            raise CredentialError("Keychain credential provider is only usable on macOS systems")
        self._keychain_name = keychain_name
        self._keychain_username = keychain_username
        self._cached_credentials = None

    def _get_keyring_credentials(self):
        """
        Reading the credentials from the macOS's Keychain.

        Returns:
            str: The raw entry from the keychain.
                May return None if there is no match from the keychain.
        """
        return keyring.get_password(self._keychain_name, self._keychain_username)

    @staticmethod
    def _parse_credentials(password):
        """
        Parses the given keychain password.

        Args:
            password (str): The password which we get from the keychain.

        Returns:
            dict: The parsed credentials.

        Raises:
            CredentialError: If the password is not in a json format.
        """
        try:
            credentials = json.loads(password.replace("\n", ""))
        except json.JSONDecodeError:
            raise CredentialError("The given password is not in a json format.")
        return credentials

    def get_credentials(self, section=None):
        """
        Return a Credentials object containing the configured credentials.

        Args:
            section (None): Since Keychain doesn't support sections it is left
            to satisfy the Signature of `CredentialProvider`

        Returns:
            Credentials: The credentials retrieved from that source.

        Raises:
            CredentialError: If there is any error retrieving the credentials.
        """
        if self._cached_credentials:
            return self._cached_credentials
        raw_credentials = self._get_keyring_credentials()
        if raw_credentials is None:
            raise CredentialError("Unable to find the credentials within the Keychain")
        self._cached_credentials = Credentials(self._parse_credentials(raw_credentials))
        return self._cached_credentials
