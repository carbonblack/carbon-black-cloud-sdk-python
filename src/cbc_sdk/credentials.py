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

"""Dynamic credentials management for the CBC SDK."""

import logging

from enum import Enum, auto
from .errors import CredentialError
from .utils import dynamic_create

log = logging.getLogger(__name__)


# === CREDENTIAL VALUES AND ASSOCIATED DATA === #


class CredentialValue(Enum):
    """All possible credential values."""
    URL = auto()
    TOKEN = auto()
    ORG_KEY = auto()
    SSL_VERIFY = auto()
    SSL_VERIFY_HOSTNAME = auto()
    SSL_CERT_FILE = auto()
    SSL_FORCE_TLS_1_2 = auto()
    PROXY = auto()
    IGNORE_SYSTEM_PROXY = auto()

    def requires_boolean_value(self):
        """
        Return whether or not this credential requires a boolean value.

        Returns:
            bool: True if the credential requires a Boolean value, False if not.
        """
        return self in _bool_valued_credentials


# The credentials that have Boolean values
_bool_valued_credentials = [CredentialValue.SSL_VERIFY, CredentialValue.SSL_VERIFY_HOSTNAME,
                            CredentialValue.SSL_FORCE_TLS_1_2, CredentialValue.IGNORE_SYSTEM_PROXY]

# The possible string values that translate to Boolean
_bool_values = {"0": False, "no": False, "off": False, "false": False,
                "1": True, "yes": True, "on": True, "true": True}

# Default values for credential parameters
_default_values = {
    CredentialValue.URL: None,
    CredentialValue.TOKEN: None,
    CredentialValue.ORG_KEY: None,
    CredentialValue.SSL_VERIFY: True,
    CredentialValue.SSL_VERIFY_HOSTNAME: True,
    CredentialValue.SSL_CERT_FILE: None,
    CredentialValue.SSL_FORCE_TLS_1_2: False,
    CredentialValue.PROXY: None,
    CredentialValue.IGNORE_SYSTEM_PROXY: False
}


# === THE CREDENTIALS DATA OBJECT === #


class Credentials(object):
    """The object that contains credentials retrieved from the credential provider."""

    def __init__(self, values=None, **kwargs):
        """
        Initialize the Credentials object.

        Args:
            values (dict): Dictionary containing values to be set in the credentials.
            **kwargs (dict): Additional values to be set in the credentials.

        Raises:
            CredentialError: If the value is not correct for any credential of boolean type.
        """
        self._values = {}
        if values is not None:
            for k in list(CredentialValue):
                if k in values:
                    self._set_value(k, values[k])
                elif k.name.lower() in values:
                    self._set_value(k, values[k.name.lower()])
        for k in list(CredentialValue):
            if k.name.lower() in kwargs:
                self._set_value(k, kwargs[k.name.lower()])

    def _set_value(self, key, value):
        """
        Set a credential value.

        Args:
            key (CredentialValues): The index of the credential value to set.
            value (object): The credential value to be set.

        Raises:
            CredentialError: If the credential is a boolean type and the value is not correct.
        """
        if key.requires_boolean_value():
            if isinstance(value, bool):
                self._values[key] = value
            elif isinstance(value, int):
                self._values[key] = (value != 0)
            elif value.lower() in _bool_values:
                self._values[key] = _bool_values[value.lower()]
            else:
                raise CredentialError(f"Invalid boolean value '{value}' for credential '{key.name}'")
        else:
            self._values[key] = value

    def get_value(self, key):
        """
        Get the value of a credential.

        Args:
            key (CredentialValues): The credential to be retrieved.

        Returns:
            object: The credential's value, or a default value if the value was not explicitly set.
        """
        if key in self._values:
            return self._values[key]
        else:
            return _default_values[key]

    def __getattr__(self, name):
        """
        Get the value of a credential expressed as an attribute name.

        Args:
            name (str): The name of the attribute (credential) to access.

        Returns:
            object: The credential's value, or a default value if the value was not explicitly set.

        Raises:
            AttributeError: If the name does not correspond to any known credential value.

        Notes:
            The translation applied here is roughly: creds.name => creds.get_value(CredentialValue.NAME)
        """
        if name.upper() in CredentialValue.__members__:
            return self.get_value(CredentialValue[name.upper()])
        else:
            raise AttributeError(f"Attribute {name} not found")

    @staticmethod
    def default():
        """
        Get a Credential instance containing default values for all credentials.

        Returns:
            Credentials: The default value instance.
        """
        return _default_credentials


_default_credentials = Credentials()


# === THE INTERFACES IMPLEMENTED BY CREDENTIAL PROVIDERS === #


class CredentialProvider:
    """The interface implemented by a credential provider."""

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
        raise NotImplementedError("protocol not implemented: get_credentials")


class CredentialProviderFactory:
    """The interface implemented by a credential provider factory."""

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
        raise NotImplementedError("protocol not implemented: get_credential_provider")


# === THE CREDENTIALS MANAGER === #


_known_credentials_providers = {
    # TK
}


class CredentialsManager:
    """The code section that manages the credentials."""
    _provider = None
    _cached_credentials = {}

    @staticmethod
    def load(provider, init_params=None):
        """
        Load the credential provider.

        Args:
            provider (str): The name (class name or "known name") of the credential provider to load.
            init_params (dict): Initialization parameters that should be passed to the provider.

        Raises:
            CredentialError: If there is any error loading the credential provider.
        """
        if CredentialsManager._provider is not None:
            raise CredentialError("CredentialsManager already loaded")
        class_name = provider
        if provider in _known_credentials_providers:
            class_name = _known_credentials_providers[provider]
        try:
            factory = dynamic_create(class_name)
            CredentialsManager._provider = factory.get_credential_provider(init_params)
        except ImportError as e:
            raise CredentialError(f"unknown credentials provider '{provider}") from e

    @staticmethod
    def get_credentials(section=None):
        """
        Return a Credentials object containing the configured credentials.

        Args:
            section (str): The credential section to retrieve.

        Returns:
            Credentials: The credentials retrieved from that source.

        Raises:
            CredentialError: If there is any error retrieving the credentials.
        """
        if section not in CredentialsManager._cached_credentials:
            if CredentialsManager._provider is None:
                raise CredentialError("credentials provider not yet loaded")
            CredentialsManager._cached_credentials[section] = CredentialsManager._provider.get_credentials(section)
        return CredentialsManager._cached_credentials[section]
