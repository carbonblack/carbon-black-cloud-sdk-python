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

"""Test for the default credential provider function."""

from cbc_sdk.credentials import CredentialProvider
from cbc_sdk.credential_providers.default import default_credential_provider


def test_default_credential_provider():
    """Test that we get a proper value out of the default_credential_provider() function."""
    val = default_credential_provider()
    assert val is not None
    assert isinstance(val, CredentialProvider)
