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
from cbc_sdk.errors import ApiError
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.workload.sensor_lifecycle import SensorType, SensorInfo, SensorRequest
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.workload.mock_sensor_lifecycle import (MOCK_SENSOR_INFO)


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
