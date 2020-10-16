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

"""Function which gives us the default credentials handler for use by CBCloudAPI."""

import logging
import os
from .file_credential_provider import FileCredentialProvider
from .environ_credential_provider import EnvironCredentialProvider

log = logging.getLogger(__name__)


class DefaultProvider:
    """Intermediate class defined to allow insertion of a "test point" into default_credential_provider()."""
    def get_default_provider(self, credential_file):
        """
        Return the default credential provider that CBCloudAPI should use.

        Args:
            credential_file (str): Credential file as specified to the initialization of the API.

        Returns:
            CredentialProvider: The default credential provider that CBCloudAPI should use.
        """
        # FUTURE: On Windows possibly return the registry-based provider
        # Note: Using Environmental Variables will override the use of the FileCredentialProvider
        if credential_file is None and (os.environ.get('CBC_TOKEN', False) or os.environ.get('CBAPI_TOKEN', False)) \
                and (os.environ.get('CBC_URL', False) or os.environ.get('CBAPI_URL', False)):
            log.debug("Using EnvironCredentialProvider")
            return EnvironCredentialProvider()
        log.debug("Using FileCredentialProvider")
        return FileCredentialProvider(credential_file=credential_file)


default_provider_object = DefaultProvider()  # the "test point" object


def default_credential_provider(credential_file):
    """
    Return the default credential provider that CBCloudAPI should use.

    Args:
        credential_file (str): Credential file as specified to the initialization of the API.

    Returns:
        CredentialProvider: The default credential provider that CBCloudAPI should use.
    """
    return default_provider_object.get_default_provider(credential_file)
