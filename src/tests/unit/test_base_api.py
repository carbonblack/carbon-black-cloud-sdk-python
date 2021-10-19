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

"""Tests for the BaseAPI object."""

import pytest
import json
import sys
from cbc_sdk import __version__
from cbc_sdk.connection import BaseAPI
from cbc_sdk.credentials import Credentials
from cbc_sdk.errors import CredentialError, ServerError
from cbc_sdk.credential_providers.default import default_provider_object
from tests.unit.fixtures.mock_credentials import MockCredentialProvider
from tests.unit.fixtures.stubresponse import StubResponse
from mox import Func


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


def test_BaseAPI_init_external_credential_provider_with_integration():
    """Test initializing the credentials from an externally-supplied provider."""
    creds = Credentials({'url': 'https://example.com', 'token': 'ABCDEFGHIJKLM', 'org_key': 'A1B2C3D4',
                         'integration': 'Anthrax'})
    mock_provider = MockCredentialProvider({'my_section': creds})
    sut = BaseAPI(credential_provider=mock_provider, profile='my_section')
    assert sut.credentials is creds
    assert sut.credentials.url == 'https://example.com'
    assert sut.credentials.token == 'ABCDEFGHIJKLM'
    assert sut.credentials.org_key == 'A1B2C3D4'
    assert sut.credential_profile_name == 'my_section'
    assert sut.credential_provider is mock_provider
    assert sut.session.server == 'https://example.com'
    assert sut.session.token == 'ABCDEFGHIJKLM'
    assert sut.session.token_header['User-Agent'].startswith('Anthrax')


def test_BaseAPI_all_options():
    """Test initializing BaseAPI with all options."""
    sut = BaseAPI(url='https://example.com',
                  token='ABCDEFGHIJKLM',
                  org_key='A1B2C3D4',
                  integration_name='Anthrax',
                  proxy='https://proxy.io:8080',
                  ssl_verify=True,
                  ssl_verify_hostname=True,
                  ssl_force_tls_1_2=True)
    assert sut.credentials.url == 'https://example.com'
    assert sut.credentials.token == 'ABCDEFGHIJKLM'
    assert sut.credentials.org_key == 'A1B2C3D4'
    assert sut.credentials.integration == 'Anthrax'
    assert sut.credentials.proxy == 'https://proxy.io:8080'
    assert sut.credentials.ssl_verify is True
    assert sut.credentials.ssl_verify_hostname is True
    assert sut.credentials.ssl_force_tls_1_2 is True
    assert sut.credential_profile_name is None
    assert sut.session.server == 'https://example.com'
    assert sut.session.token == 'ABCDEFGHIJKLM'
    assert sut.session.token_header['User-Agent'].startswith('Anthrax')


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
    ('Anon/0.5.0', f"Anon/0.5.0 CBC_SDK/{__version__} Python/{PYTHON_VERS}"),
    (None, f"CBC_SDK/{__version__} Python/{PYTHON_VERS}")
])
def test_BaseAPI_generate_user_agent(integration, expected_line):
    """Test the generation of the User-Agent header."""
    sut = BaseAPI(integration_name=integration, url='https://example.com', token='ABCDEFGHIJKLM', org_key='A1B2C3D4')
    assert sut.session.token_header['User-Agent'] == expected_line


@pytest.mark.parametrize("response, expected, scode", [
    (StubResponse({'color': 'green'}, 400), {}, 400),
    (StubResponse({'color': 'green'}), {'color': 'blue'}, 200),
    (StubResponse({'color': 'green'}), {'color': 'green', 'mode': 3}, 200)
])
def test_BaseAPI_raise_unless_json_raises(response, expected, scode):
    """Test the "raise" cases of raise_unless_json."""
    sut = BaseAPI(url='https://example.com', token='ABCDEFGH', org_key='A1B2C3D4')
    with pytest.raises(ServerError) as excinfo:
        sut.raise_unless_json(response, expected)
    assert excinfo.value.error_code == scode


@pytest.mark.parametrize("expath, response, params, default, expected", [
    ('/path', StubResponse({'a': 1, 'b': 2}), None, {'a': 8, 'b': 9}, {'a': 1, 'b': 2}),
    ('/path?x=1&y=2', StubResponse({'a': 1, 'b': 2}), [('x', 1), ('y', 2)], {'a': 8, 'b': 9}, {'a': 1, 'b': 2}),
    ('/path?x=1&y=2', StubResponse({'a': 1, 'b': 2}), {'x': 1, 'y': 2}, {'a': 8, 'b': 9}, {'a': 1, 'b': 2}),
    ('/path', StubResponse({'a': 1, 'b': 2}, 204), None, {'a': 8, 'b': 9}, {'a': 8, 'b': 9})
])
def test_BaseAPI_get_object_returns(mox, expath, response, params, default, expected):
    """Test the cases where get_object returns a value."""
    sut = BaseAPI(url='https://example.com', token='ABCDEFGH', org_key='A1B2C3D4')
    mox.StubOutWithMock(sut.session, 'http_request')
    sut.session.http_request('GET', expath, headers={}, data=None).AndReturn(response)
    mox.ReplayAll()
    rc = sut.get_object('/path', params, default)
    assert rc == expected
    mox.VerifyAll()


@pytest.mark.parametrize("response, errcode, prefix", [
    (StubResponse({'errorMessage': 'Test Alpha Message'}), 200, 'Test Alpha Message'),
    (StubResponse(None, 200, "{'a': 14"), 200, 'Cannot parse response as JSON:'),
    (StubResponse({'a': 1}, 404), 404, 'Unknown error:')
])
def test_BaseAPI_get_object_raises_from_returns(mox, response, errcode, prefix):
    """Test the cases where get_object raises an exception based on what it receives."""
    sut = BaseAPI(url='https://example.com', token='ABCDEFGH', org_key='A1B2C3D4')
    mox.StubOutWithMock(sut.session, 'http_request')
    sut.session.http_request('GET', '/path', headers={}, data=None).AndReturn(response)
    mox.ReplayAll()
    with pytest.raises(ServerError) as excinfo:
        sut.get_object('/path')
    assert excinfo.value.error_code == errcode
    assert excinfo.value.message.startswith(prefix)
    mox.VerifyAll()


@pytest.mark.parametrize("expath, code, response, params, default, expected", [
    ('/path', 200, 'Boston1', None, 'Denver0', 'Boston1'),
    ('/path?x=1&y=2', 200, 'Boston1', [('x', 1), ('y', 2)], 'Denver0', 'Boston1'),
    ('/path?x=1&y=2', 200, 'Boston1', {'x': 1, 'y': 2}, 'Denver0', 'Boston1'),
    ('/path', 204, 'Boston1', None, 'Denver0', 'Denver0')
])
def test_BaseAPI_get_raw_data_returns(mox, expath, code, response, params, default, expected):
    """Test the cases where get_raw_data returns a value."""
    sut = BaseAPI(url='https://example.com', token='ABCDEFGH', org_key='A1B2C3D4')
    mox.StubOutWithMock(sut.session, 'http_request')
    sut.session.http_request('GET', expath, headers={}, data=None).AndReturn(StubResponse(None, code, response))
    mox.ReplayAll()
    rc = sut.get_raw_data('/path', params, default)
    assert rc == expected
    mox.VerifyAll()


@pytest.mark.parametrize("response, errcode, prefix", [
    (StubResponse({'errorMessage': 'Test Alpha Message'}), 200, 'Test Alpha Message'),
    (StubResponse(None, 404, 'Test text'), 404, 'Unknown error:')
])
def test_BaseAPI_get_raw_data_raises_from_returns(mox, response, errcode, prefix):
    """Test the cases where get_raw_data raises an exception based on what it receives."""
    sut = BaseAPI(url='https://example.com', token='ABCDEFGH', org_key='A1B2C3D4')
    mox.StubOutWithMock(sut.session, 'http_request')
    sut.session.http_request('GET', '/path', headers={}, data=None).AndReturn(response)
    mox.ReplayAll()
    with pytest.raises(ServerError) as excinfo:
        sut.get_raw_data('/path')
    assert excinfo.value.error_code == errcode
    assert excinfo.value.message.startswith(prefix)
    mox.VerifyAll()


def test_BaseAPI_post_object(mox):
    """Test the operation of post_object."""
    def validate_header(hdrs):
        assert hdrs['Content-Type'] == 'application/json'
        return True

    def validate_data(data):
        real_data = json.loads(data)
        assert real_data == {'a': 1, 'b': 2}
        return True

    sut = BaseAPI(url='https://example.com', token='ABCDEFGH', org_key='A1B2C3D4')
    mox.StubOutWithMock(sut.session, 'http_request')
    sut.session.http_request('POST', '/path', headers=Func(validate_header), data=Func(validate_data)) \
        .AndReturn(StubResponse({'zyx': 100}))
    mox.ReplayAll()
    rc = sut.post_object('/path', {'a': 1, 'b': 2})
    assert rc.json() == {'zyx': 100}
    mox.VerifyAll()


def test_BaseAPI_post_multipart(mox):
    """Test the operation of post_multipart."""
    def validate_header(hdrs):
        assert 'Content-Type' not in hdrs
        return True

    def validate_files(files):
        assert len(files) == 2
        assert files['name'][0] == 'name.txt'
        assert files['name'][1] == 'Cheeseburger'
        assert files['name'][2] == 'text/plain'
        assert files['config'][0] is None
        assert files['config'][1] == 'abc\ndef\nghi'
        assert files['config'][2] is None
        return True

    trans_table = {'name': {'filename': 'name.txt', 'type': 'text/plain'}, 'config': {}}
    sut = BaseAPI(url='https://example.com', token='ABCDEFGH', org_key='A1B2C3D4')
    mox.StubOutWithMock(sut.session, 'http_request')
    sut.session.http_request('POST', '/path', headers=Func(validate_header), data=None, files=Func(validate_files)) \
        .AndReturn(StubResponse({'zyx': 100}))
    mox.ReplayAll()
    rc = sut.post_multipart('/path', trans_table, name='Cheeseburger', config='abc\ndef\nghi', notused='Not used')
    assert rc.json() == {'zyx': 100}
    mox.VerifyAll()


def test_BaseAPI_put_object(mox):
    """Test the operation of put_object."""
    def validate_header(hdrs):
        assert hdrs['Content-Type'] == 'application/json'
        return True

    def validate_data(data):
        real_data = json.loads(data)
        assert real_data == {'a': 1, 'b': 2}
        return True

    sut = BaseAPI(url='https://example.com', token='ABCDEFGH', org_key='A1B2C3D4')
    mox.StubOutWithMock(sut.session, 'http_request')
    sut.session.http_request('PUT', '/path', headers=Func(validate_header), data=Func(validate_data)) \
        .AndReturn(StubResponse({'zyx': 100}))
    mox.ReplayAll()
    rc = sut.put_object('/path', {'a': 1, 'b': 2})
    assert rc.json() == {'zyx': 100}
    mox.VerifyAll()


def test_BaseAPI_delete_object(mox):
    """Test the operation of delete_object."""
    sut = BaseAPI(url='https://example.com', token='ABCDEFGH', org_key='A1B2C3D4')
    mox.StubOutWithMock(sut.session, 'http_request')
    sut.session.http_request('DELETE', '/path', headers={}, data=None).AndReturn(StubResponse({'zyx': 100}))
    mox.ReplayAll()
    rc = sut.delete_object('/path')
    assert rc.json() == {'zyx': 100}
    mox.VerifyAll()
