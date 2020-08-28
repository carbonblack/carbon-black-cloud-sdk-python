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

"""Tests for the BaseAPI object."""

import pytest
import sys
from cbc_sdk import __version__
from cbc_sdk.connection import BaseAPI
from cbc_sdk.credentials import Credentials
from cbc_sdk.errors import CredentialError
from cbc_sdk.credential_providers.default import default_provider_object
from tests.unit.fixtures.mock_credentials import MockCredentialProvider


def test_BaseAPI_init_with_raw_credential_params():
    """Test initializing the credentials from raw parameters to the BaseAPI."""
    sut = BaseAPI(integration_name='test1', url='https://example.com', token='ABCDEFGHIJKLM', org_key='A1B2C3D4')
    assert sut.credentials.url == 'https://example.com'
    assert sut.credentials.token == 'ABCDEFGHIJKLM'
    assert sut.credentials.org_key == 'A1B2C3D4'
    assert sut.credential_profile_name is None
    assert sut.credential_provider is None
    assert sut.session.server == 'https://example.com'
    assert sut.session.token == 'ABCDEFGHIJKLM'
    assert sut.session.token_header['User-Agent'].startswith('test1')


def test_BaseAPI_init_selecting_the_default_credential_provider(monkeypatch):
    """
    Test initializing the credentials from the default provider.

    This test's purpose is to show that we can create BaseAPI and have it pick a default credential provider
    successfully using default_credential_provider(). We use the environment provider here because it's easiest
    to set up consistently using an automated unit test.  The possible outputs of default_credential_provider() are
    tested exhaustively elsewhere.
    """
    monkeypatch.setenv('CBAPI_URL', 'https://example.com')
    monkeypatch.setenv('CBAPI_TOKEN', 'ABCDEFGHIJKLM')
    monkeypatch.setenv('CBAPI_ORG_KEY', 'A1B2C3D4')
    sut = BaseAPI(integration_name='test2', credential_file=None, profile='anything')
    assert sut.credentials.url == 'https://example.com'
    assert sut.credentials.token == 'ABCDEFGHIJKLM'
    assert sut.credentials.org_key == 'A1B2C3D4'
    assert sut.credential_profile_name == 'anything'
    assert sut.session.server == 'https://example.com'
    assert sut.session.token == 'ABCDEFGHIJKLM'
    assert sut.session.token_header['User-Agent'].startswith('test2')


def test_BaseAPI_init_external_credential_provider():
    """Test initializing the credentials from an externally-supplied provider."""
    creds = Credentials({'url': 'https://example.com', 'token': 'ABCDEFGHIJKLM', 'org_key': 'A1B2C3D4'})
    mock_provider = MockCredentialProvider({'my_section': creds})
    sut = BaseAPI(integration_name='test3', credential_provider=mock_provider, profile='my_section')
    assert sut.credentials is creds
    assert sut.credentials.url == 'https://example.com'
    assert sut.credentials.token == 'ABCDEFGHIJKLM'
    assert sut.credentials.org_key == 'A1B2C3D4'
    assert sut.credential_profile_name == 'my_section'
    assert sut.credential_provider is mock_provider
    assert sut.session.server == 'https://example.com'
    assert sut.session.token == 'ABCDEFGHIJKLM'
    assert sut.session.token_header['User-Agent'].startswith('test3')


def test_BaseAPI_init_credential_provider_raises_error():
    """Test initializing the credentials when the provider raises an error."""
    creds = Credentials({'url': 'https://example.com', 'token': 'ABCDEFGHIJKLM', 'org_key': 'A1B2C3D4'})
    mock_provider = MockCredentialProvider({'my_section': creds})
    with pytest.raises(CredentialError):
        BaseAPI(integration_name='test4', credential_provider=mock_provider, profile='notexist')


def test_BaseAPI_init_with_no_profile():
    """
    Test the case where an empty profile string and nothing else is specified.

    This test case will force the use of the FileCredentialProvider, which will search for the "default" locations
    of credential files, and may or may not find them depending on the environment. Whether it does or not is
    irrelevant, though, as the empty profile string will be trapped by FileCredentialProvider before it attempts to
    read any files.
    """
    with pytest.raises(CredentialError):
        BaseAPI(profile='')


def test_BaseAPI_init_with_only_profile_specified(mox):
    """Test the case where we only supply a profile string to the BaseAPI."""
    mox.StubOutWithMock(default_provider_object, 'get_default_provider')
    creds = Credentials({'url': 'https://example.com', 'token': 'ABCDEFGHIJKLM', 'org_key': 'A1B2C3D4'})
    mock_provider = MockCredentialProvider({'Valid': creds})
    default_provider_object.get_default_provider(None).AndReturn(mock_provider)
    mox.ReplayAll()
    sut = BaseAPI(profile='Valid')
    assert sut.credentials is creds
    assert sut.credentials.url == 'https://example.com'
    assert sut.credentials.token == 'ABCDEFGHIJKLM'
    assert sut.credentials.org_key == 'A1B2C3D4'
    assert sut.credential_profile_name == 'Valid'
    assert sut.session.server == 'https://example.com'
    assert sut.session.token == 'ABCDEFGHIJKLM'
    mox.VerifyAll()


PYTHON_VERS = f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"


@pytest.mark.parametrize("integration, expected_line", [
    ('Anon/0.5.0', f"Anon/0.5.0 CBCSDK/{__version__} Python/{PYTHON_VERS}"),
    (None, f"CBCSDK/{__version__} Python/{PYTHON_VERS}")
])
def test_BaseAPI_generate_user_agent(integration, expected_line):
    """Test the generation of the User-Agent header."""
    sut = BaseAPI(integration_name=integration, url='https://example.com', token='ABCDEFGHIJKLM', org_key='A1B2C3D4')
    assert sut.session.token_header['User-Agent'] == expected_line
