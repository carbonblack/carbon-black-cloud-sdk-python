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
from cbc_sdk.workload.sensor_lifecycle import SensorKit
from cbc_sdk.workload.vm_workloads_search import ComputeResource
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.workload.mock_sensor_lifecycle import (GET_CONFIG_TEMPLATE_RESP, GET_SENSOR_INFO_RESP,
                                                                REQUEST_SENSOR_INSTALL_RESP)


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


def create_stub_compute_resource(cb, id, uuid, vcenter_uuid):
    """Create a stub ComputeResource object with the data we need."""
    return ComputeResource(cb, id, {'id': id, 'uuid': uuid, 'vcenter_uuid': vcenter_uuid})


# ==================================== UNIT TESTS BELOW ====================================

def test_sensorkit_from_type(cb):
    """Test creation code for SensorKit and make sure data slots in correctly."""
    skit = SensorKit.from_type(cb, 'LINUX', '64', 'SUSE', '1.2.3.4')
    assert skit.sensor_type == {'device_type': 'LINUX', 'architecture': '64', 'type': 'SUSE', 'version': '1.2.3.4'}
    assert skit.sensor_type['architecture'] == '64'
    assert skit.sensor_type['type'] == 'SUSE'
    assert skit.sensor_type['version'] == '1.2.3.4'
    skit2 = SensorKit(cb, {'sensor_type': {'device_type': 'LINUX', 'architecture': '64', 'type': 'SUSE',
                                           'version': '1.2.3.4'},
                           'sensor_url': 'X', 'sensor_config_url': 'Y', 'error_code': None, 'message': None})
    assert skit2.sensor_type == skit.sensor_type


@pytest.mark.parametrize("device_type, arch, sensor_type", [
    ('NOTEXIST', '32', 'WINDOWS'),
    ('MAC', 'UNKNOWN', 'MAC'),
    ('LINUX', '64', 'FROM_SCRATCH')
])
def test_sensorkit_from_type_fail(cb, device_type, arch, sensor_type):
    """Test errors raised with bogus values for SensorKit."""
    with pytest.raises(ApiError):
        SensorKit.from_type(cb, device_type, arch, sensor_type, '1.2.3.4')


def test_get_config_template(cbcsdk_mock):
    """Test the get_config_template function."""
    cbcsdk_mock.mock_request("RAW_GET", "/lcm/v1/orgs/test/sensor/config_template", GET_CONFIG_TEMPLATE_RESP)
    api = cbcsdk_mock.api
    result = SensorKit.get_config_template(api)
    assert "ALSK12KHG83B110DKK" in result
    assert "ABCD1234" in result
    assert "backendserver.org" in result


def test_sensor_query(cbcsdk_mock):
    """Test the sensor kit query."""
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
    query = api.select(SensorKit)
    query.add_sensor_kit_type(device_type='LINUX', architecture='64', sensor_type='SUSE', version='1.2.3.4')
    skit = SensorKit.from_type(api, 'MAC', '64', 'MAC', '5.6.7.8')
    query.add_sensor_kit_type(skit).expires('2021-04-01T23:39:52Z').config_params('SampleConfParams')
    assert query._count() == 2
    result = list(query)
    assert len(result) == 2
    assert result[0].sensor_type == {'device_type': 'LINUX', 'architecture': '64', 'type': 'SUSE', 'version': '1.2.3.4'}
    assert result[0].sensor_url == "https://SensorURL1"
    assert result[0].sensor_config_url == "https://SensorConfigURL1"
    assert result[0].error_code == "NoErr1"
    assert result[0].message == "Message1"
    assert result[1].sensor_type == {'device_type': 'MAC', 'architecture': '64', 'type': 'MAC', 'version': '5.6.7.8'}
    assert result[1].sensor_url == "https://SensorURL2"
    assert result[1].sensor_config_url == "https://SensorConfigURL2"
    assert result[1].error_code == "NoErr2"
    assert result[1].message == "Message2"


def test_sensor_query_async(cbcsdk_mock):
    """Test the sensor kit query."""
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
    query = api.select(SensorKit)
    query.add_sensor_kit_type(device_type='LINUX', architecture='64', sensor_type='SUSE', version='1.2.3.4')
    skit = SensorKit.from_type(api, 'MAC', '64', 'MAC', '5.6.7.8')
    future = query.add_sensor_kit_type(skit).expires('2021-04-01T23:39:52Z') \
                  .config_params('SampleConfParams').execute_async()
    result = future.result()
    assert len(result) == 2
    assert result[0].sensor_type == {'device_type': 'LINUX', 'architecture': '64', 'type': 'SUSE', 'version': '1.2.3.4'}
    assert result[0].sensor_url == "https://SensorURL1"
    assert result[0].sensor_config_url == "https://SensorConfigURL1"
    assert result[0].error_code == "NoErr1"
    assert result[0].message == "Message1"
    assert result[1].sensor_type == {'device_type': 'MAC', 'architecture': '64', 'type': 'MAC', 'version': '5.6.7.8'}
    assert result[1].sensor_url == "https://SensorURL2"
    assert result[1].sensor_config_url == "https://SensorConfigURL2"
    assert result[1].error_code == "NoErr2"
    assert result[1].message == "Message2"


def test_sensor_install_bulk(cbcsdk_mock):
    """Test the bulk_install function on ComputeResource."""
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
    resource1 = create_stub_compute_resource(api, '123', 'Zulu', 'Alpha')
    resource2 = create_stub_compute_resource(api, '234', 'Yankee', 'Bravo')
    skit1 = SensorKit.from_type(api, 'LINUX', '64', 'SUSE', '1.2.3.4')
    skit2 = SensorKit.from_type(api, 'MAC', '64', 'MAC', '5.6.7.8')
    result = ComputeResource.bulk_install(api, [resource1, resource2], [skit1, skit2], 'MyConfigFile')
    assert result == {'type': "INFO", 'code': "INSTALL_SENSOR_REQUEST_PROCESSED"}


def test_sensor_install_single(cbcsdk_mock):
    """Test the install_sensor function on ComputeResource."""
    def validate_post(url, **kwargs):
        assert kwargs['action_type'] == 'INSTALL'
        assert kwargs['file'] == 'MyConfigFile'
        r = json.loads(kwargs['install_request'])
        assert r == {'compute_resources': [{'resource_manager_id': 'Alpha', 'compute_resource_id': 'Zulu'}],
                     'sensor_types': [{'device_type': 'LINUX', 'architecture': '64', 'type': 'SUSE',
                                       'version': '1.2.3.4'},
                                      {'device_type': 'MAC', 'architecture': '64', 'type': 'MAC',
                                       'version': '5.6.7.8'}]}
        return REQUEST_SENSOR_INSTALL_RESP

    cbcsdk_mock.mock_request("POST_MULTIPART", "/lcm/v1/orgs/test/workloads/actions", validate_post)
    api = cbcsdk_mock.api
    resource = create_stub_compute_resource(api, '123', 'Zulu', 'Alpha')
    skit1 = SensorKit.from_type(api, 'LINUX', '64', 'SUSE', '1.2.3.4')
    skit2 = SensorKit.from_type(api, 'MAC', '64', 'MAC', '5.6.7.8')
    result = resource.install_sensor([skit1, skit2], 'MyConfigFile')
    assert result == {'type': "INFO", 'code': "INSTALL_SENSOR_REQUEST_PROCESSED"}
