# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Tests for the EnvironCredentialProvider"""

import pytest
from cbc_sdk.credential_providers import EnvironCredentialProvider


@pytest.mark.parametrize('name1, name2, name3, name4', [
    ('CBAPI_URL', 'CBAPI_TOKEN', 'CBAPI_ORG_KEY', 'CBAPI_SSL_VERIFY'),
    ('CBAPI_URL', 'CBAPI_TOKEN', 'CBAPI_ORG_KEY', 'CBC_SSL_VERIFY'),
    ('CBAPI_URL', 'CBAPI_TOKEN', 'CBC_ORG_KEY', 'CBAPI_SSL_VERIFY'),
    ('CBAPI_URL', 'CBAPI_TOKEN', 'CBC_ORG_KEY', 'CBC_SSL_VERIFY'),
    ('CBAPI_URL', 'CBC_TOKEN', 'CBAPI_ORG_KEY', 'CBAPI_SSL_VERIFY'),
    ('CBAPI_URL', 'CBC_TOKEN', 'CBAPI_ORG_KEY', 'CBC_SSL_VERIFY'),
    ('CBAPI_URL', 'CBC_TOKEN', 'CBC_ORG_KEY', 'CBAPI_SSL_VERIFY'),
    ('CBAPI_URL', 'CBC_TOKEN', 'CBC_ORG_KEY', 'CBC_SSL_VERIFY'),
    ('CBC_URL', 'CBAPI_TOKEN', 'CBAPI_ORG_KEY', 'CBAPI_SSL_VERIFY'),
    ('CBC_URL', 'CBAPI_TOKEN', 'CBAPI_ORG_KEY', 'CBC_SSL_VERIFY'),
    ('CBC_URL', 'CBAPI_TOKEN', 'CBC_ORG_KEY', 'CBAPI_SSL_VERIFY'),
    ('CBC_URL', 'CBAPI_TOKEN', 'CBC_ORG_KEY', 'CBC_SSL_VERIFY'),
    ('CBC_URL', 'CBC_TOKEN', 'CBAPI_ORG_KEY', 'CBAPI_SSL_VERIFY'),
    ('CBC_URL', 'CBC_TOKEN', 'CBAPI_ORG_KEY', 'CBC_SSL_VERIFY'),
    ('CBC_URL', 'CBC_TOKEN', 'CBC_ORG_KEY', 'CBAPI_SSL_VERIFY'),
    ('CBC_URL', 'CBC_TOKEN', 'CBC_ORG_KEY', 'CBC_SSL_VERIFY')
])
def test_environ_credentials(monkeypatch, name1, name2, name3, name4):
    """Test that environment credentials get read in properly."""
    monkeypatch.setenv(name1, 'http://example.com')
    monkeypatch.setenv(name2, 'ABCDEFGH')
    monkeypatch.setenv(name3, 'A1B2C3D4')
    monkeypatch.setenv(name4, 'false')
    sut = EnvironCredentialProvider()
    creds = sut.get_credentials()
    assert creds.url == "http://example.com"
    assert creds.token == "ABCDEFGH"
    assert creds.org_key == "A1B2C3D4"
    assert not creds.ssl_verify
    assert creds.ssl_verify_hostname
    assert creds.ssl_cert_file is None
    assert not creds.ssl_force_tls_1_2
    assert creds.proxy is None
    assert not creds.ignore_system_proxy
    assert creds.integration is None
    creds2 = sut.get_credentials("arbitrary")
    assert creds2 is creds


def test_environ_credentials_override_correctly(monkeypatch):
    """Test that the CBC_xxx environment values correctly override the CBAPI_xxx environment values."""
    monkeypatch.setenv('CBC_URL', 'http://example.com')
    monkeypatch.setenv('CBC_TOKEN', 'ABCDEFGH')
    monkeypatch.setenv('CBC_ORG_KEY', 'A1B2C3D4')
    monkeypatch.setenv('CBC_SSL_VERIFY', 'false')
    monkeypatch.setenv('CBAPI_URL', 'http://WRONG')
    monkeypatch.setenv('CBAPI_TOKEN', 'WRONG')
    monkeypatch.setenv('CBAPI_ORG_KEY', 'VERYWRONG')
    monkeypatch.setenv('CBAPI_SSL_VERIFY', 'true')
    sut = EnvironCredentialProvider()
    creds = sut.get_credentials()
    assert creds.url == "http://example.com"
    assert creds.token == "ABCDEFGH"
    assert creds.org_key == "A1B2C3D4"
    assert not creds.ssl_verify


def test_environ_no_credentials(monkeypatch):
    """Test that we do the right thing with missing environment credentials."""
    monkeypatch.delenv('CBAPI_URL', False)
    monkeypatch.delenv('CBAPI_TOKEN', False)
    monkeypatch.delenv('CBAPI_ORG_KEY', False)
    monkeypatch.delenv('CBAPI_SSL_VERIFY', False)
    monkeypatch.delenv('CBC_URL', False)
    monkeypatch.delenv('CBC_TOKEN', False)
    monkeypatch.delenv('CBC_ORG_KEY', False)
    monkeypatch.delenv('CBC_SSL_VERIFY', False)
    sut = EnvironCredentialProvider()
    creds = sut.get_credentials()
    assert creds.url is None
    assert creds.token is None
    assert creds.org_key is None
    assert creds.ssl_verify
    assert creds.ssl_verify_hostname
    assert creds.ssl_cert_file is None
    assert not creds.ssl_force_tls_1_2
    assert creds.proxy is None
    assert not creds.ignore_system_proxy
    assert creds.integration is None
