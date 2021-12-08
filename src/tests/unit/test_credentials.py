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

"""Tests for the Credentials object."""

import pytest
import requests_mock

from cbc_sdk.credentials import CredentialValue, Credentials
from cbc_sdk.errors import CredentialError


def test_credential_default_values():
    """Tests the default credential values, and also the AttributeError mechanism."""
    creds = Credentials()
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
    with pytest.raises(AttributeError):
        assert creds.notexist is None


@pytest.mark.parametrize(["input_dict"], [
    ({CredentialValue.URL: "http://example.com", CredentialValue.TOKEN: "ABCDEFGH",
      CredentialValue.ORG_KEY: "A1B2C3D4", CredentialValue.SSL_VERIFY: False,
      CredentialValue.SSL_VERIFY_HOSTNAME: False, CredentialValue.SSL_CERT_FILE: "foo.certs",
      CredentialValue.SSL_FORCE_TLS_1_2: True, CredentialValue.PROXY: "proxy.example",
      CredentialValue.IGNORE_SYSTEM_PROXY: True, CredentialValue.INTEGRATION: 'Bronski'}, ),
    ({"url": "http://example.com", "token": "ABCDEFGH", "org_key": "A1B2C3D4", "ssl_verify": "false",
      "ssl_verify_hostname": "no", "ssl_cert_file": "foo.certs", "ssl_force_tls_1_2": "1",
      "proxy": "proxy.example", "ignore_system_proxy": "on", "integration": 'Bronski'}, )
])
def test_credential_dict_value_load(input_dict):
    """Test loading credentials from a dict, and also access through both attributes and get_value."""
    creds = Credentials(input_dict)
    assert creds.url == "http://example.com"
    assert creds.token == "ABCDEFGH"
    assert creds.org_key == "A1B2C3D4"
    assert not creds.ssl_verify
    assert not creds.ssl_verify_hostname
    assert creds.ssl_cert_file == "foo.certs"
    assert creds.ssl_force_tls_1_2
    assert creds.proxy == "proxy.example"
    assert creds.ignore_system_proxy
    assert creds.integration == 'Bronski'
    assert creds.get_value(CredentialValue.URL) == "http://example.com"
    assert creds.get_value(CredentialValue.TOKEN) == "ABCDEFGH"
    assert creds.get_value(CredentialValue.ORG_KEY) == "A1B2C3D4"
    assert not creds.get_value(CredentialValue.SSL_VERIFY)
    assert not creds.get_value(CredentialValue.SSL_VERIFY_HOSTNAME)
    assert creds.get_value(CredentialValue.SSL_CERT_FILE) == "foo.certs"
    assert creds.get_value(CredentialValue.SSL_FORCE_TLS_1_2)
    assert creds.get_value(CredentialValue.PROXY) == "proxy.example"
    assert creds.get_value(CredentialValue.IGNORE_SYSTEM_PROXY)
    assert creds.get_value(CredentialValue.INTEGRATION) == 'Bronski'


def test_credential_partial_loads():
    """Test that we can have credentials with some values from dict and some default."""
    init_dict = {"url": "http://example.com", "ssl_verify": 0}
    creds = Credentials(init_dict)
    assert creds.url == "http://example.com"
    assert creds.token is None
    assert creds.org_key is None
    assert not creds.ssl_verify
    assert creds.ssl_verify_hostname
    assert creds.ssl_cert_file is None
    assert not creds.ssl_force_tls_1_2
    assert creds.proxy is None
    assert not creds.ignore_system_proxy
    assert creds.integration is None


def test_credential_boolean_parsing_failure():
    """Tests failure of parsing a Boolean credential value."""
    init_dict = {"url": "http://example.com", "ssl_verify": "bogus"}
    with pytest.raises(CredentialError):
        Credentials(init_dict)


@pytest.mark.parametrize(["input_dict"], [
    ({CredentialValue.URL: "http://example.com", CredentialValue.TOKEN: "ABCDEFGH",
      CredentialValue.ORG_KEY: "A1B2C3D4", CredentialValue.SSL_VERIFY: False,
      CredentialValue.SSL_VERIFY_HOSTNAME: False, CredentialValue.SSL_CERT_FILE: "foo.certs",
      CredentialValue.SSL_FORCE_TLS_1_2: True, CredentialValue.PROXY: "proxy.example",
      CredentialValue.IGNORE_SYSTEM_PROXY: True, CredentialValue.INTEGRATION: 'Bronski'}, ),
    ({"url": "http://example.com", "token": "ABCDEFGH", "org_key": "A1B2C3D4", "ssl_verify": "false",
      "ssl_verify_hostname": "no", "ssl_cert_file": "foo.certs", "ssl_force_tls_1_2": "1",
      "proxy": "proxy.example", "ignore_system_proxy": "on", "integration": 'Bronski'}, )
])
def test_credential_get_dict(input_dict):
    """Tests if we get the correct dictionary."""
    creds = Credentials(input_dict).to_dict()
    assert creds["url"] == "http://example.com"
    assert creds["token"] == "ABCDEFGH"
    assert creds["org_key"] == "A1B2C3D4"
    assert not creds["ssl_verify"]
    assert not creds["ssl_verify_hostname"]
    assert creds["ssl_cert_file"] == "foo.certs"
    assert creds["ssl_force_tls_1_2"]
    assert creds["proxy"] == "proxy.example"
    assert creds["ignore_system_proxy"]


def test_get_token_api_key():
    """Test get token with Carbon Black Cloud API_KEY"""
    values = {
        "token": "api-key"
    }
    creds = Credentials(values)
    assert creds.get_token_type() == "API_KEY"
    assert creds.get_token() == "api-key"


def test_get_token_missing():
    """Test get token with no token configured"""
    creds = Credentials({})
    assert creds.get_token_type() == "UNKNOWN"
    assert creds.get_token() is None


def test_get_token_api_token():
    """Test get token with CSP API Token configured"""
    with requests_mock.Mocker() as mock_request:
        mock_request.register_uri("POST",
                                  "https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize",
                                  json={"access_token": "valid-token", "scope": "valid-scope"})
        values = {
            "csp_api_token": "test-token"
        }
        creds = Credentials(values)
        assert creds.get_token_type() == "BEARER"
        assert creds.get_token() == "valid-token"

        # Verify Request
        assert mock_request.last_request.text == "api_token=test-token"


def test_get_token_oauth_app():
    """Test get token with CSP OAuth Server App configured"""
    with requests_mock.Mocker() as mock_request:
        mock_request.register_uri("POST",
                                  "http://example.com/csp/gateway/am/api/auth/token",
                                  json={"access_token": "valid-token", "scope": "valid-scope"})
        values = {
            "csp_oauth_app_id": "client-id",
            "csp_oauth_app_secret": "client-secret",
            "csp_url_override": "http://example.com"
        }
        creds = Credentials(values)
        assert creds.get_token_type() == "BEARER"
        assert creds.get_token() == "valid-token"

        # Verify Request
        assert mock_request.last_request.text == "grant_type=client_credentials"
        assert mock_request.last_request.headers.get("Authorization") == "Basic Y2xpZW50LWlkOmNsaWVudC1zZWNyZXQ="
