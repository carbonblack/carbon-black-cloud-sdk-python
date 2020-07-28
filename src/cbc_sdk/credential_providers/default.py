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

from .file_credential_provider import FileCredentialProvider


def default_credential_provider():
    """
    Return the default credential provider that CBCloudAPI should use.

    Returns:
        CredentialProvider: The default credential provider that CBCloudAPI should use.
    """
    # FUTURE: On Windows return the registry-based provider
    return FileCredentialProvider()
