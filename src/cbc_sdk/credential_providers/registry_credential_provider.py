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

"""Credentials provider that reads the credentials from the environment."""

import logging
import sys
from cbc_sdk.credentials import CredentialValue, Credentials, CredentialProvider
from cbc_sdk.errors import CredentialError

# The winreg module doesn't exist on Unix, so we have to stub out some functionality if it's not present.
# The functionality we need is in the two top-level key names (HKEY_CURRENT_USER and HKEY_LOCAL_MACHINE)
# and in two API functions, OpenKey and QueryValueEx. (Note that the credential provider won't even initialize if
# sys.platform tells us we're on a non-Windows platform, so the stubs will never get called. This is primarily
# for unit test purposes, since the tests HAVE to run in a Unix environment for Codeship,
# where we fake out sys.platform and mock the internal methods that call those two API functions.)
try:
    import winreg
    HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
    HKEY_LOCAL_MACHINE = winreg.HKEY_LOCAL_MACHINE
    OpenKey = winreg.OpenKey
    QueryValueEx = winreg.QueryValueEx
except ModuleNotFoundError:
    HKEY_CURRENT_USER = object()
    HKEY_LOCAL_MACHINE = object()

    def OpenKey(base, path):
        """Stub to maintain source compatibility"""
        return None

    def QueryValueEx(key, name):
        """Stub to maintain source compatibility"""
        return None

# Define these constants locally so they don't depend on winreg. From the Windows Registry API docs.
REG_SZ = 1
REG_DWORD = 4

log = logging.getLogger(__name__)


DEFAULT_KEYPATH = 'Software\\VMware Carbon Black\\Cloud Credentials'


class RegistryCredentialProvider(CredentialProvider):
    """The credentials provider that reads from the Windows Registry."""
    def __init__(self, keypath=None, userkey=True):
        """
        Initialize the RegistryCredentialProvider.

        Args:
            keypath (str): Path from the selected base key to the key that will contain individual sections.
            userkey (bool): True if the keypath starts at HKEY_CURRENT_USER, False if at HKEY_LOCAL_MACHINE.

        Raises:
            CredentialError: If we attempt to instantiate this provider on a non-Windows system.
        """
        self._cached_credentials = {}
        self._usable = sys.platform.startswith("win32")
        if not self._usable:
            raise CredentialError("Registry credential provider is only usable on Windows systems")
        self._userkey = userkey
        self._keypath = keypath or DEFAULT_KEYPATH

    def _base_key(self):
        """
        Return the base key that we're starting from in finding the credentials, depending on the _userkey flag.

        Returns:
            PyHKEY: Either HKEY_CURRENT_USER or HKEY_LOCAL_MACHINE.
        """
        return HKEY_CURRENT_USER if self._userkey else HKEY_LOCAL_MACHINE

    def _open_key(self, basekey, path):
        """
        Open a key for use.  This is a "test point" intended to be monkeypatched.

        Args:
            basekey (PyHKEY): The base key that the path supplied extends from.
            path (str): The path of the subkey to open from that base key.

        Returns:
            PyHKEY: The new subkey for use.

        Raises:
            CredentialError: If the subkey could not be opened for any reason.
        """
        try:
            return OpenKey(basekey, path)
        except OSError as e:
            raise CredentialError(f"Unable to open registry subkey: {path}") from e

    def _read_value(self, key, value_name):
        """
        Read a value from the registry key specified.  This is a "test point" intended to be monkeypatched.

        Args:
            key (PyHKEY): The key to read a value from.
            value_name (str): The name of the value to be returned.

        Returns:
            tuple: First element of the tuple is the actual value. Second element is the data type as an index.
                May return None if the value was not found.

        Raises:
            CredentialError: If there was an unanticipated error reading the value.
        """
        try:
            return QueryValueEx(key, value_name)
        except FileNotFoundError:
            return None
        except OSError as e:
            raise CredentialError(f"Unable to read registry value: {value_name}") from e

    def _read_str(self, key, value_name):
        """
        Read a string value from the registry key specified.

        Args:
            key (PyHKEY): The key to read a value from.
            value_name (str): The name of the value to be returned.

        Returns:
            str: The value read in. May return None if the value was not found.

        Raises:
            CredentialError: If there was an error reading the value, or if the value was of the wrong type.
        """
        val = self._read_value(key, value_name)
        if val:
            if val[1] != REG_SZ:
                raise CredentialError(f"value '{value_name}` is not of string type")
            return val[0]
        return None

    def _read_bool(self, key, value_name):
        """
        Read a boolean value from the registry key specified.

        Args:
            key (PyHKEY): The key to read a value from.
            value_name (str): The name of the value to be returned.

        Returns:
            bool: The value read in. May return None if the value was not found.

        Raises:
            CredentialError: If there was an error reading the value, or if the value was of the wrong type.
        """
        val = self._read_value(key, value_name)
        if val:
            if val[1] != REG_DWORD:
                raise CredentialError(f"value '{value_name}` is not of integer type")
            return val[0] != 0
        return None

    def _read_credentials(self, key):
        """
        Read in a complete credentials set from a registry key.

        Args:
            key (PyHKEY): The registry key to be read in.

        Returns:
            Credentials: A new credentials object containing the credentials that were read in.

        Raises:
            CredentialError: If there was any issue reading the credentials in.
        """
        input = {}
        for cv in list(CredentialValue):
            if cv.requires_boolean_value():
                value = self._read_bool(key, cv.name.lower())
                if value is not None:
                    input[cv] = value
            else:
                value = self._read_str(key, cv.name.lower())
                if value is not None:
                    input[cv] = value
        return Credentials(input)

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
        if not section:
            raise CredentialError("Section must be specified")
        if section not in self._cached_credentials:
            with self._open_key(self._base_key(), self._keypath) as base_key:
                with self._open_key(base_key, section) as section_key:
                    self._cached_credentials[section] = self._read_credentials(section_key)
        return self._cached_credentials[section]
