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

import pytest
from cbc_sdk.credential_providers import default_credential_provider, FileCredentialProvider, EnvironCredentialProvider


def test_default_credential_providers_file(monkeypatch):
    """Test that we get the FileCredentialProvider out of the default_credential_provider() function."""
    monkeypatch.delenv('CBAPI_TOKEN', False)
    monkeypatch.delenv('CBAPI_URL', False)
    monkeypatch.delenv('CBC_TOKEN', False)
    monkeypatch.delenv('CBC_URL', False)
    val = default_credential_provider("myfile.cbc")
    assert val is not None
    assert isinstance(val, FileCredentialProvider)
    val = default_credential_provider(None)
    assert val is not None
    assert isinstance(val, FileCredentialProvider)


@pytest.mark.parametrize('urlvar, tokenvar', [
    ('CBAPI_URL', 'CBAPI_TOKEN'),
    ('CBAPI_URL', 'CBC_TOKEN'),
    ('CBC_URL', 'CBAPI_TOKEN'),
    ('CBC_URL', 'CBC_TOKEN')
])
def test_default_credential_providers_environ(monkeypatch, urlvar, tokenvar):
    """Test that we get the EnvironCredentialProvider out of the default_credential_provider() function."""
    monkeypatch.delenv('CBAPI_TOKEN', False)
    monkeypatch.delenv('CBAPI_URL', False)
    monkeypatch.delenv('CBC_TOKEN', False)
    monkeypatch.delenv('CBC_URL', False)
    monkeypatch.setenv(tokenvar, 'ABCDEFGH')
    monkeypatch.setenv(urlvar, 'http://example.com')
    val = default_credential_provider(None)
    assert val is not None
    assert isinstance(val, EnvironCredentialProvider)
