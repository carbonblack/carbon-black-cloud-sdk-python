"""Testing Query object of cbc_sdk.endpoint_standard"""

import pytest
import logging
from cbc_sdk.endpoint_standard import Device, Query
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_devices import (ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP,
                                                                ENDPOINT_STANDARD_DEVICE_GET_HOSTNAME_RESP_0,
                                                                ENDPOINT_STANDARD_DEVICE_GET_HOSTNAME_RESP_EMPTY)

log = logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, filename='log.txt')


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


def test_endpoint_standard_query_clone(cbcsdk_mock):
    """Testing Query._clone()."""
    # This test isn't really doing anything. All of these attrs are None
    # TODO: figure out how to set these attrs, then check for equality
    device_query = cbcsdk_mock.api.select(Device).where(deviceId=12345)
    # device_query._sort_by({"key": "deviceId", "direction": "ASC"})
    cloned = device_query._clone()
    assert cloned._sort_by == device_query._sort_by
    assert cloned._group_by == device_query._group_by
    assert cloned._batch_size == device_query._batch_size
    assert cloned._criteria == device_query._criteria


def test_endpoint_standard_query_mix_raw_structured(cbcsdk_mock):
    """Testing Query with raw 'string' and keyword. Should raise ApiError."""
    with pytest.raises(ApiError):
        cbcsdk_mock.api.select(Device).where(deviceId=1).and_('hostName:Win7x64')


def test_endpoint_standard_query_count(cbcsdk_mock):
    """Testing Query._count()."""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_GET_HOSTNAME_RESP_0)
    api = cbcsdk_mock.api
    hostname_device_query = api.select(Device).where('hostName:Win7x64')
    assert not hostname_device_query._count_valid
    assert hostname_device_query._count() == 1
    assert hostname_device_query._count_valid
