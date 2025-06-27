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

from __future__ import absolute_import

from .file_credential_provider import FileCredentialProvider
from .environ_credential_provider import EnvironCredentialProvider
from .registry_credential_provider import RegistryCredentialProvider
from .aws_sm_credential_provider import AWSCredentialProvider

import platform

# Only import if macOS
if platform.system() == 'Darwin':
    from .keychain_credential_provider import KeychainCredentialProvider
