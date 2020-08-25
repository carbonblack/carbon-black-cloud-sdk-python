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

from cbc_sdk.credential_providers import default_credential_provider, FileCredentialProvider, EnvironCredentialProvider


def test_default_credential_providers(monkeypatch):
    """Test that we get a proper value out of the default_credential_provider() function."""
    monkeypatch.delenv('CBAPI_TOKEN', False)
    monkeypatch.delenv('CBAPI_URL', False)
    val = default_credential_provider("myfile.cbc")
    assert val is not None
    assert isinstance(val, FileCredentialProvider)
    val = default_credential_provider(None)
    assert val is not None
    assert isinstance(val, FileCredentialProvider)
    monkeypatch.setenv('CBAPI_TOKEN', 'ABCDEFGH')
    monkeypatch.setenv('CBAPI_URL', 'http://example.com')
    val = default_credential_provider(None)
    assert val is not None
    assert isinstance(val, EnvironCredentialProvider)
