# *******************************************************
# Copyright (c) VMware, Inc. 2020-2023. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Tests for the macOS Registry credential provider."""

import sys
import pytest
import platform

if platform.system() == 'Darwin':
    from cbc_sdk.credential_providers.keychain_credential_provider import KeychainCredentialProvider

from cbc_sdk.errors import CredentialError

INVALID_JSON = """{\nurl: "http://example.test/",\n"token" : "TTTTT/TTTTT",\n"org_key": "TT123TT",
    \n"ssl_verify": true,\n"ssl_verify_hostname": true,\n"ssl_cert_file": "test.cert",\n"ssl_force_tls_1_2": true,
    \n"proxy": "proxy.example",\n"ignore_system_proxy": true,\n"integration": "test"\n} """
VALID_JSON = """{\n"url": "http://example.test/",\n"token" : "TTTTT/TTTTT",\n"org_key": "TT123TT",
    \n"ssl_verify": true,\n"ssl_verify_hostname": true,\n"ssl_cert_file": "test.cert",\n"ssl_force_tls_1_2": true,
    \n"proxy": "proxy.example",\n"ignore_system_proxy": true,\n"integration": "test"\n} """


@pytest.mark.skipif(platform.system() != 'Darwin', reason="only run on mac os")
def test_breaks_not_on_macos(monkeypatch):
    """Test that creating the KeychainCredentialProvider breaks if we're not on macOS."""
    monkeypatch.setattr(sys, "platform", "linux")
    with pytest.raises(CredentialError):
        KeychainCredentialProvider("test", "test")


@pytest.mark.skipif(platform.system() != 'Darwin', reason="only run on mac os")
def test_password_parser(monkeypatch):
    """Test that checks if the password is parsed correctly."""
    monkeypatch.setattr(sys, "platform", "darwin")
    parsed = KeychainCredentialProvider("test", "test")._parse_credentials(VALID_JSON)
    assert isinstance(parsed, dict)
    assert parsed["url"] == "http://example.test/"
    assert parsed["token"] == "TTTTT/TTTTT"
    assert parsed["org_key"] == "TT123TT"
    assert parsed["ssl_verify"]
    assert parsed["ssl_verify_hostname"]
    assert parsed["ssl_cert_file"] == "test.cert"
    assert parsed["ssl_force_tls_1_2"]
    assert parsed["proxy"] == "proxy.example"
    assert parsed["ignore_system_proxy"]
    assert parsed["integration"] == "test"


@pytest.mark.skipif(platform.system() != 'Darwin', reason="only run on mac os")
def test_password_parser_invalid_json(monkeypatch):
    """Test that checks if the password is parsed correctly."""
    monkeypatch.setattr(sys, "platform", "darwin")
    with pytest.raises(CredentialError):
        KeychainCredentialProvider("test", "test")._parse_credentials(INVALID_JSON)


@pytest.mark.skipif(platform.system() != 'Darwin', reason="only run on mac os")
def test_get_credentials_valid(monkeypatch):
    """Tests if it parses the Credential data correctly."""
    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(KeychainCredentialProvider, "_get_keyring_credentials", lambda c: VALID_JSON)
    keychain_provider = KeychainCredentialProvider("test", "test").get_credentials()
    assert keychain_provider.url == "http://example.test/"
    assert keychain_provider.token == "TTTTT/TTTTT"
    assert keychain_provider.org_key == "TT123TT"
    assert keychain_provider.ssl_verify
    assert keychain_provider.ssl_verify_hostname
    assert keychain_provider.ssl_cert_file == "test.cert"
    assert keychain_provider.ssl_force_tls_1_2
    assert keychain_provider.proxy == "proxy.example"
    assert keychain_provider.ignore_system_proxy
    assert keychain_provider.integration == "test"


@pytest.mark.skipif(platform.system() != 'Darwin', reason="only run on mac os")
def test_get_credentials_invalid(monkeypatch):
    """Tests if it raises the CredentialError with the given invalid json."""
    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(KeychainCredentialProvider, "_get_keyring_credentials", lambda c: INVALID_JSON)
    with pytest.raises(CredentialError):
        KeychainCredentialProvider("test", "test").get_credentials()


@pytest.mark.skipif(platform.system() != 'Darwin', reason="only run on mac os")
def test_get_credentials_none_found(monkeypatch):
    """Tests if it raises the CredentialError if credentials are not found."""
    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setattr(KeychainCredentialProvider, "_get_keyring_credentials", lambda c: None)
    with pytest.raises(CredentialError):
        KeychainCredentialProvider("test", "test").get_credentials()
