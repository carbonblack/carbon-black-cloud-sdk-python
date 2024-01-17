"""Testing Device object of cbc_sdk.platform"""

import pytest
import logging
from cbc_sdk.platform import Device, DeviceSearchQuery
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_devices import (GET_DEVICE_RESP,
                                                       POST_DEVICE_SEARCH_RESP)

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

def test_device_query_0(cbcsdk_mock):
    """Testing Device Querying with .select(Device, `device_id`)"""
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    api = cbcsdk_mock.api
    platform_device_select_with_id = api.select(Device, 98765)
    platform_device_select_with_id.refresh()
    assert platform_device_select_with_id._model_unique_id == 98765
    assert platform_device_select_with_id.id == 98765
    assert isinstance(platform_device_select_with_id, Device)


def test_device_query_with_where_and(cbcsdk_mock):
    """Testing Device Querying with .where() and .and_()"""
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    api = cbcsdk_mock.api
    platform_device_select_with_where_stmt = api.select(Device).where(deviceId='98765').and_(name='win7x64')
    assert isinstance(platform_device_select_with_where_stmt, DeviceSearchQuery)

    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/devices/_search", POST_DEVICE_SEARCH_RESP)

    assert platform_device_select_with_where_stmt._count() == 1
    results = [res for res in platform_device_select_with_where_stmt._perform_query()]

    # compare select with ID inside the select method vs using .where() and .and_()
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    platform_device_select_with_id = api.select(Device, 98765)
    platform_device_select_with_id.refresh()
    assert results[0]._info['id'] == platform_device_select_with_id._info['id']
    assert len(results[0]._info) == len(platform_device_select_with_id._info)
    assert len(results[0]._info) != 0


def test_device_query_async(cbcsdk_mock):
    """Testing a device query with execute_async()"""
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/devices/_search", POST_DEVICE_SEARCH_RESP)
    api = cbcsdk_mock.api
    future = api.select(Device).where(deviceId='98765').and_(name='win7x64').execute_async()
    results = future.result()
    assert len(results) == 1
    assert results[0].policy_id == 11200


def test_device_id_property(cbcsdk_mock):
    """Testing raising AttributeError on call to device.deviceId."""
    with pytest.raises(AttributeError):
        cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
        a = Device(cbcsdk_mock.api, 98765)
        a.deviceId


def test_device_max_rows(cbcsdk_mock):
    """Testing Device Querying with .set_max_rows"""
    api = cbcsdk_mock.api
    query = api.select(Device).set_max_rows(10)
    assert query.max_rows == 10

    with pytest.raises(ApiError):
        query.set_max_rows(-1)

    with pytest.raises(ApiError):
        query.set_max_rows(10001)


def test_device_tojson_inheritance(cbcsdk_mock):
    """Testing Device tojson() with .select(Device, `device_id`)"""
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    api = cbcsdk_mock.api
    platform_device_select_with_id = api.select(Device, 98765)
    platform_device_select_with_id.refresh()
    assert platform_device_select_with_id.to_json() == GET_DEVICE_RESP
