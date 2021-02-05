#!/usr/bin/env python3

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

"""Unit test code for sensor lifecycle"""

import pytest
import logging
import json
from cbc_sdk.errors import ApiError
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.workload.sensor_lifecycle import SensorType, SensorInfo, SensorRequest
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.workload.mock_sensor_lifecycle import (MOCK_SENSOR_INFO, GET_CONFIG_TEMPLATE_RESP,
                                                                GET_SENSOR_INFO_RESP, REQUEST_SENSOR_INSTALL_RESP)


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, filename='log.txt')


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


# ==================================== UNIT TESTS BELOW ====================================

def test_create_sensor_type(cb):
    """Test creation code for sensor types and make sure data slots in correctly."""
    stype = SensorType.create(cb, 'LINUX', '64', 'SUSE', '1.2.3.4')
    assert stype.device_type == 'LINUX'
    assert stype.architecture == '64'
    assert stype.sensor_type == 'SUSE'
    assert stype.version == '1.2.3.4'
    output = stype._as_dict()
    assert output == {'device_type': 'LINUX', 'architecture': '64', 'type': 'SUSE', 'version': '1.2.3.4'}
    stype2 = SensorType(cb, output)
    assert stype.device_type == stype2.device_type
    assert stype.architecture == stype2.architecture
    assert stype.sensor_type == stype2.sensor_type
    assert stype.version == stype2.version


@pytest.mark.parametrize("device_type, arch, sensor_type", [
    ('NOTEXIST', '32', 'WINDOWS'),
    ('MAC', 'UNKNOWN', 'MAC'),
    ('LINUX', '64', 'FROM_SCRATCH')
])
def test_create_sensor_type_fail(cb, device_type, arch, sensor_type):
    """Test errors raised with bogus values for SensorType."""
    with pytest.raises(ApiError):
        SensorType.create(cb, device_type, arch, sensor_type, '1.2.3.4')


def test_sensor_info(cb):
    """Test the creation and associated code of SensorInfo."""
    sinfo = SensorInfo(cb, MOCK_SENSOR_INFO)
    stype = sinfo.sensor_type_
    assert stype.device_type == 'WINDOWS'
    assert stype.architecture == '64'
    assert stype.sensor_type == 'WINDOWS'
    assert stype.version == '3.6.0.1719'
    assert sinfo.sensor_url == 'https://sensor-url'
    assert sinfo.sensor_config_url == 'https://sensor-config-url'
    assert sinfo.error_code == '808'
    assert sinfo.message == 'NoMessage'


def test_get_config_template(cbcsdk_mock):
    """Test the get_config_template function."""
    cbcsdk_mock.mock_request("RAW_GET", "/lcm/v1/orgs/test/sensor/config_template", GET_CONFIG_TEMPLATE_RESP)
    api = cbcsdk_mock.api
    result = SensorRequest.get_config_template(api)
    assert "ALSK12KHG83B110DKK" in result
    assert "ABCD1234" in result
    assert "backendserver.org" in result


def test_get_sensor_info(cbcsdk_mock):
    """Test the get_sensor_info function."""
    def validate_post(url, **kwargs):
        assert kwargs['configParams'] == 'SampleConfParams'
        r = json.loads(kwargs['sensor_url_request'])
        assert r == {'sensor_types': [{'device_type': 'LINUX', 'architecture': '64', 'type': 'SUSE',
                                       'version': '1.2.3.4'},
                                      {'device_type': 'MAC', 'architecture': '64', 'type': 'MAC',
                                       'version': '5.6.7.8'}],
                     'expires_at': '2021-04-01T23:39:52Z'}
        return GET_SENSOR_INFO_RESP

    cbcsdk_mock.mock_request("POST_MULTIPART", "/lcm/v1/orgs/test/sensor/_download", validate_post)
    api = cbcsdk_mock.api
    req = SensorRequest(api)
    req.add_sensor_type(device_type='LINUX', architecture='64', sensor_type='SUSE', version='1.2.3.4')
    stype = SensorType.create(api, 'MAC', '64', 'MAC', '5.6.7.8')
    req.add_sensor_type(stype)
    infos = req.get_sensor_info('2021-04-01T23:39:52Z', 'SampleConfParams')
    assert len(infos) == 2
    stype = infos[0].sensor_type_
    assert stype.device_type == 'LINUX'
    assert stype.architecture == '64'
    assert stype.sensor_type == 'SUSE'
    assert stype.version == '1.2.3.4'
    assert infos[0].sensor_url == "https://SensorURL1"
    assert infos[0].sensor_config_url == "https://SensorConfigURL1"
    assert infos[0].error_code == "NoErr1"
    assert infos[0].message == "Message1"
    stype = infos[1].sensor_type_
    assert stype.device_type == 'MAC'
    assert stype.architecture == '64'
    assert stype.sensor_type == 'MAC'
    assert stype.version == '5.6.7.8'
    assert infos[1].sensor_url == "https://SensorURL2"
    assert infos[1].sensor_config_url == "https://SensorConfigURL2"
    assert infos[1].error_code == "NoErr2"
    assert infos[1].message == "Message2"


def test_request_sensor_install(cbcsdk_mock):
    """Test the request_sensor_install function."""
    def validate_post(url, **kwargs):
        assert kwargs['action_type'] == 'INSTALL'
        assert kwargs['file'] == 'MyConfigFile'
        r = json.loads(kwargs['install_request'])
        assert r == {'compute_resources': [{'resource_manager_id': 'Alpha', 'compute_resource_id': 'Zulu'},
                                           {'resource_manager_id': 'Bravo', 'compute_resource_id': 'Yankee'}],
                     'sensor_types': [{'device_type': 'LINUX', 'architecture': '64', 'type': 'SUSE',
                                       'version': '1.2.3.4'},
                                      {'device_type': 'MAC', 'architecture': '64', 'type': 'MAC',
                                       'version': '5.6.7.8'}]}
        return REQUEST_SENSOR_INSTALL_RESP

    cbcsdk_mock.mock_request("POST_MULTIPART", "/lcm/v1/orgs/test/workloads/actions", validate_post)
    api = cbcsdk_mock.api
    req = SensorRequest(api)
    req.add_sensor_type(device_type='LINUX', architecture='64', sensor_type='SUSE', version='1.2.3.4')
    stype = SensorType.create(api, 'MAC', '64', 'MAC', '5.6.7.8')
    req.add_sensor_type(stype)
    req.add_compute_resource("Alpha", "Zulu")
    req.add_compute_resource("Bravo", "Yankee")
    result = req.request_sensor_install('MyConfigFile')
    assert result == {'type': "INFO", 'code': "INSTALL_SENSOR_REQUEST_PROCESSED"}
