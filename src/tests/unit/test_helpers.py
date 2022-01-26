# *******************************************************
# Copyright (c) VMware, Inc. 2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Test code for the helper functions"""
import pytest
import requests_mock

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object, read_iocs, get_object_by_name_or_id
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.endpoint_standard import USBDevice

from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_usb_devices import (USBDEVICE_GET_RESP,
                                                                    USBDEVICE_QUERY_RESP,
                                                                    USBDEVICE_QUERY_RESP_ZERO_RESULT)


@pytest.fixture(scope="function")
def cb():
    """Create CBCloudAPI singleton"""
    return CBCloudAPI(url="https://example.com",
                      org_key="test",
                      token="abcd/1234",
                      ssl_verify=False)


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, cb):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, cb)


def test_argument_parser_default_values():
    """Tests the default credential values."""
    parser = build_cli_parser("Test helpers.py")
    args = parser.parse_known_args()[0]

    assert args.cburl is None
    assert args.apitoken is None
    assert args.orgkey is None
    assert args.no_ssl_verify is False
    assert args.profile == 'default'
    assert args.verbose is False


def test_apicloudapi_object_with_command_line_arguments():
    """Tests the CBCloudAPI object with command line arguments."""
    parser = build_cli_parser("Test helpers.py")
    args = parser.parse_known_args()[0]

    args.cburl = 'https://example.com'
    args.apitoken = 'ABCDEFGH'
    args.orgkey = 'A1B2C3D4'
    args.no_ssl_verify = 'false'
    args.verbose = True

    api = get_cb_cloud_object(args)

    assert api.credential_profile_name is None


def test_apicloudapi_object_with_proxy():
    """Tests the CBCloudAPI object with command line arguments."""
    parser = build_cli_parser("Test helpers.py")
    args = parser.parse_known_args()[0]

    args.cburl = 'https://example.com'
    args.proxy = 'http://proxy.com'
    args.apitoken = 'ABCDEFGH'
    args.orgkey = 'A1B2C3D4'
    args.no_ssl_verify = 'false'
    args.verbose = True

    api = get_cb_cloud_object(args)

    assert api.credentials.proxy == 'http://proxy.com'


def test_apicloudapi_object_with_command_line_arguments_csp_api_token():
    """Test init credentials from BaseAPI for CSP API Token options"""
    with requests_mock.Mocker() as mock_request:
        mock_request.register_uri("POST",
                                  "https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize",
                                  json={"access_token": "valid-token", "scope": "valid-scope"})

        parser = build_cli_parser("Test helpers.py")
        args = parser.parse_known_args()[0]

        args.cburl = 'https://example.com'
        args.csp_api_token = 'test-token'
        args.orgkey = 'A1B2C3D4'
        args.no_ssl_verify = 'false'
        args.verbose = True

        api = get_cb_cloud_object(args)

        assert api.session.token == "valid-token"

        # Verify Request
        assert mock_request.last_request.text == "api_token=test-token"


def test_apicloudapi_object_with_command_line_arguments_csp_oauth_app():
    """Test init credentials from BaseAPI for CSP OAuth App options"""
    with requests_mock.Mocker() as mock_request:
        mock_request.register_uri("POST",
                                  "https://console.cloud.vmware.com/csp/gateway/am/api/auth/token",
                                  json={"access_token": "valid-token", "scope": "valid-scope"})
        parser = build_cli_parser("Test helpers.py")
        args = parser.parse_known_args()[0]

        args.cburl = 'https://example.com'
        args.csp_oauth_app_id = 'client-id'
        args.csp_oauth_app_secret = 'client-secret'
        args.orgkey = 'A1B2C3D4'
        args.no_ssl_verify = 'false'
        args.verbose = True

        api = get_cb_cloud_object(args)

        assert api.session.token == "valid-token"

        # Verify Request
        assert mock_request.last_request.text == "grant_type=client_credentials"
        assert mock_request.last_request.headers.get("Authorization") == "Basic Y2xpZW50LWlkOmNsaWVudC1zZWNyZXQ="



def test_apicloudapi_object_with_default_arguments():
    """Tests the CBCloudAPI object with default arguments."""
    parser = build_cli_parser("Test helpers.py")
    args = parser.parse_known_args()[0]

    assert args.profile == 'default'


def test_read_iocs(cbcsdk_mock):
    """Test read_iocs method"""
    called = False

    def post_validate(*args):
        nonlocal called
        if not called:
            called = True
            return {"valid": True}
        return {"valid": False}

    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation", post_validate)
    api = cbcsdk_mock.api
    sha256 = '8005557c1614c1e2c89f7db3702199de2b1e4605718fa32ff6ffdb2b41ed3759'
    md5 = 'f586835082f632dc8d9404d83bc16316'
    ipv4 = '127.0.0.1'
    ipv6 = '2001:db8:3333:4444:5555:6666:7777:8888'
    domain = 'google.com'
    query = 'process_name:chrome.exe'
    query2 = 'invalid'
    test_data = [md5, sha256, ipv4, ipv6, domain, query, query2]
    expected = {
        'md5': ['f586835082f632dc8d9404d83bc16316'],
        'sha256': ['8005557c1614c1e2c89f7db3702199de2b1e4605718fa32ff6ffdb2b41ed3759'],
        'ipv4': ['127.0.0.1'],
        'ipv6': ['2001:db8:3333:4444:5555:6666:7777:8888'],
        'dns': ['google.com'],
        'query': [{'search_query': 'process_name:chrome.exe'}]
    }
    result = read_iocs(api, test_data)
    assert result[1] == expected


def test_get_object_by_name_or_id(cbcsdk_mock):
    """Test get object by name"""
    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/devices/_search", USBDEVICE_QUERY_RESP)
    api = cbcsdk_mock.api
    result = get_object_by_name_or_id(api, USBDevice, name_field="device_name", name="\\Device\\HarddiskVolume30")
    assert len(result) == 1
    assert isinstance(result[0], USBDevice)


def test_get_object_by_name_or_id_with_id(cbcsdk_mock):
    """Test get object by id"""
    cbcsdk_mock.mock_request("GET", "/device_control/v3/orgs/test/devices/774", USBDEVICE_GET_RESP)
    api = cbcsdk_mock.api
    result = get_object_by_name_or_id(api, USBDevice, id=774)
    assert len(result) == 1
    assert isinstance(result[0], USBDevice)


def test_get_object_by_name_or_id_no_result(cbcsdk_mock):
    """Test get_object_by_name_or_id with 0 found"""
    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/devices/_search", USBDEVICE_QUERY_RESP_ZERO_RESULT)
    api = cbcsdk_mock.api
    with pytest.raises(Exception):
        get_object_by_name_or_id(api, USBDevice, name_field="device_name", name="\\Device\\HarddiskVolume30")


def test_get_object_by_name_or_id_errors(cbcsdk_mock):
    """Test get_object_by_name_or_id with 0 found"""
    api = cbcsdk_mock.api
    with pytest.raises(Exception):
        get_object_by_name_or_id(api, USBDevice)

    with pytest.raises(Exception):
        get_object_by_name_or_id(api, USBDevice, id=774, name_field="device_name", name="\\Device\\HarddiskVolume30")
