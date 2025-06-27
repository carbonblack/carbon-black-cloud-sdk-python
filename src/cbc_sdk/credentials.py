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

"""Credentials management for the CBC SDK."""

import logging
import requests

from enum import Enum, auto
from .errors import CredentialError

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
    INTEGRATION = auto()
    CSP_OAUTH_APP_ID = auto()
    CSP_OAUTH_APP_SECRET = auto()
    CSP_API_TOKEN = auto()
    CSP_URL_OVERRIDE = auto()
    DEFAULT_TIMEOUT = auto()

    def requires_boolean_value(self):
        """
        Return whether or not this credential requires a boolean value.

        Returns:
            bool: True if the credential requires a Boolean value, False if not.
        """
        return self in _bool_valued_credentials

    def requires_integer_value(self):
        """
        Return whether or not this credential requires an integer value.

        Returns:
            bool: True if the credential requires an integer value, False if not.
        """
        return self in _int_valued_credentials


# The credentials that have Boolean values
_bool_valued_credentials = [CredentialValue.SSL_VERIFY, CredentialValue.SSL_VERIFY_HOSTNAME,
                            CredentialValue.SSL_FORCE_TLS_1_2, CredentialValue.IGNORE_SYSTEM_PROXY]

# The credentials that have integer values
_int_valued_credentials = [CredentialValue.DEFAULT_TIMEOUT]

# The possible string values that translate to Boolean
_bool_values = {"0": False, "no": False, "off": False, "false": False,
                "1": True, "yes": True, "on": True, "true": True}

# The maximum value that the default timeout may have under any circumstances.
MAX_DEFAULT_TIMEOUT = 300000


# === THE CREDENTIALS DATA OBJECT === #


class Credentials(object):
    """The object that contains credentials retrieved from the credential provider."""

    def __init__(self, values=None):
        """
        Initialize the Credentials object.

        Args:
            values (dict): Dictionary containing values to be set in the credentials.

        Raises:
            CredentialError: If the value is not correct for any credential of boolean type.
        """
        self._values = {  # default values
            CredentialValue.URL: None,
            CredentialValue.TOKEN: None,
            CredentialValue.ORG_KEY: None,
            CredentialValue.SSL_VERIFY: True,
            CredentialValue.SSL_VERIFY_HOSTNAME: True,
            CredentialValue.SSL_CERT_FILE: None,
            CredentialValue.SSL_FORCE_TLS_1_2: False,
            CredentialValue.PROXY: None,
            CredentialValue.IGNORE_SYSTEM_PROXY: False,
            CredentialValue.INTEGRATION: None,
            CredentialValue.CSP_OAUTH_APP_ID: None,
            CredentialValue.CSP_OAUTH_APP_SECRET: None,
            CredentialValue.CSP_API_TOKEN: None,
            CredentialValue.CSP_URL_OVERRIDE: "https://console.cloud.vmware.com",
            CredentialValue.DEFAULT_TIMEOUT: MAX_DEFAULT_TIMEOUT
        }
        if values is not None:
            for k in list(CredentialValue):
                if k in values:
                    self._set_value(k, values[k])
                elif k.name.lower() in values:
                    self._set_value(k, values[k.name.lower()])

        if self.get_value(CredentialValue.DEFAULT_TIMEOUT) > MAX_DEFAULT_TIMEOUT:
            self._set_value(CredentialValue.DEFAULT_TIMEOUT, MAX_DEFAULT_TIMEOUT)

        self._token_type = "UNKNOWN"
        if self.get_value(CredentialValue.TOKEN) is not None:
            self._token_type = "API_KEY"

        elif self.get_value(CredentialValue.CSP_API_TOKEN) is not None:
            self._token_type = "API_TOKEN"

        elif self.get_value(CredentialValue.CSP_OAUTH_APP_ID) is not None and \
                self.get_value(CredentialValue.CSP_OAUTH_APP_SECRET) is not None:
            self._token_type = "OAUTH_APP"

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
        elif key.requires_integer_value():
            if isinstance(value, int):
                self._values[key] = value
            elif isinstance(value, str):
                try:
                    self._values[key] = int(value)
                except ValueError:
                    raise CredentialError(f"Invalid integer value '{value}' for credential '{key.name}'")
            else:
                raise CredentialError(f"Invalid integer value '{value}' for credential '{key.name}'")
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
        return self._values.get(key)

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

    def to_dict(self):
        """
        Serializes the credentials into a dictionary.

        Returns:
            dict: Dictionary with the credentials.

        """
        _dict = {}
        for i in list(CredentialValue):
            _dict[i.name.lower()] = self.get_value(i)
        return _dict

    def get_token_type(self):
        """
        Get token type API_KEY or BEARER

        Returns:
            str: The token type
        """
        if self._token_type == "API_KEY":
            return "API_KEY"
        elif self._token_type == "API_TOKEN" or self._token_type == "OAUTH_APP":
            return "BEARER"
        return "UNKNOWN"

    def get_token(self):
        """
        Get token required to authenticate with VMware Carbon Black Cloud

        Returns:
            str: Token string for VMware Carbon Black Cloud
        """
        if self._token_type == "UNKNOWN":
            return None
        elif self._token_type == "API_KEY":
            return self.get_value(CredentialValue.TOKEN)

        csp_url = self.get_value(CredentialValue.CSP_URL_OVERRIDE).rstrip("/")

        if self._token_type == "API_TOKEN":
            api_token_url = f"{csp_url}/csp/gateway/am/api/auth/api-tokens/authorize"
            resp = requests.post(api_token_url, {"api_token": self.get_value(CredentialValue.CSP_API_TOKEN)})
            json_body = resp.json()
            if resp.status_code != 200:
                raise CredentialError(json_body.get("message"))

            # Check that token has scope
            if json_body.get("scope") is None:
                raise CredentialError("Access token created with empty scope")
            return json_body.get("access_token")

        if self._token_type == "OAUTH_APP":
            oauth_app_token_url = f"{csp_url}/csp/gateway/am/api/auth/token"

            # Construct Authorization header Basic Base64(client_id:client_secret)
            client_id = self.get_value(CredentialValue.CSP_OAUTH_APP_ID)
            client_secret = self.get_value(CredentialValue.CSP_OAUTH_APP_SECRET)
            client_credentials = (client_id, client_secret)

            resp = requests.post(oauth_app_token_url, {"grant_type": "client_credentials"}, auth=client_credentials)
            json_body = resp.json()
            if resp.status_code != 200:
                raise CredentialError(json_body.get("message"))

            # Check that token has scope
            if json_body.get("scope") is None:
                raise CredentialError("Access token created with empty scope")
            return json_body.get("access_token")

        return None

# === THE INTERFACES IMPLEMENTED BY CREDENTIAL PROVIDERS === #


class CredentialProvider:
    """The interface implemented by a credential provider."""

    def get_credentials(self, section=None):  # pragma: no cover
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
