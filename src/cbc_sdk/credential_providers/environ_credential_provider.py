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
import os
from cbc_sdk.credentials import CredentialValue, Credentials, CredentialProvider

log = logging.getLogger(__name__)


class EnvironCredentialProvider(CredentialProvider):
    """The object which provides credentials based on variables in the environment."""
    def __init__(self):
        """Initializes the EnvironCredentialProvider."""
        log.warning("Security warning: Storing credentials in environment variables "
                    "is insecure and is not recommended.")
        url = os.environ.get('CBC_URL', os.environ.get('CBAPI_URL', None))
        token = os.environ.get('CBC_TOKEN', os.environ.get('CBAPI_TOKEN', None))
        ssl_verify = os.environ.get('CBC_SSL_VERIFY', os.environ.get('CBAPI_SSL_VERIFY', True))
        org_key = os.environ.get('CBC_ORG_KEY', os.environ.get('CBAPI_ORG_KEY', None))
        self._credentials = Credentials({CredentialValue.URL: url, CredentialValue.TOKEN: token,
                                         CredentialValue.ORG_KEY: org_key, CredentialValue.SSL_VERIFY: ssl_verify})

    def get_credentials(self, section=None):
        """
        Return a Credentials object containing the configured credentials.

        Args:
            section (str): The credential section to retrieve (not used in this provider).

        Returns:
            Credentials: The credentials retrieved from that source.

        Raises:
            CredentialError: If there is any error retrieving the credentials.
        """
        return self._credentials
