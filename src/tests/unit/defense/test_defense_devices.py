"""Testing Device object of cbc_sdk.defense"""

import pytest
import logging
from cbc_sdk.defense import Device
from cbc_sdk.defense import Query
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.defense.mock_devices import (DEFENSE_DEVICE_GET_HOSTNAME_RESP,
                                                      DEFENSE_DEVICE_GET_HOSTNAME_EXACT_RESP,
                                                      DEFENSE_DEVICE_GET_OWNERNAME_RESP,
                                                      DEFENSE_DEVICE_GET_OWNERNAME_EXACT_RESP,
                                                      DEFENSE_DEVICE_GET_IP_RESP,
                                                      DEFENSE_DEVICE_GET_HOST_IP_RESP,
                                                      DEFENSE_DEVICE_GET_SPECIFIC_RESP,
                                                      DEFENSE_DEVICE_GET_ALL_RESP)

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

# validate is failing on these Device objects? When it enters the validate() function,
# self = <[TypeError("argument of type 'NoneType' is not iterable") raised in repr()] Device object at 0x10d224a50>
def test_device_query_0(cbcsdk_mock):
    """Testing select() method with .where() hostName"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", DEFENSE_DEVICE_GET_HOSTNAME_RESP)
    api = cbcsdk_mock.api
    hostname_device_query = api.select(Device).where('hostName:Win7x64')
    results = [result for result in hostname_device_query._perform_query()]
    assert len(results) == 1

    hostname_device_query = api.select(Device).where(hostName='Win7x64')
    results = [result for result in hostname_device_query._perform_query()]
    assert len(results) == 1
    assert hostname_device_query._count() == len(results)
    device = results[0]
    assert device._model_unique_id == 43407
    assert device.deviceId == 43407
    assert isinstance(device, Device)
    assert set(device._info.keys()) is not None
    print(device.__repr__())
    # assert device.validate()


# validate is failing on these Device objects? When it enters the validate() function,
# self = <[TypeError("argument of type 'NoneType' is not iterable") raised in repr()] Device object at 0x10d224a50>
def test_device_query_1(cbcsdk_mock):
    """Testing select() method with .where() hostNameExact"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", DEFENSE_DEVICE_GET_HOSTNAME_EXACT_RESP)
    api = cbcsdk_mock.api
    defense_select_hostname_exact_device_query = api.select(Device).where('hostNameExact:Win7x64')
    results = [result for result in defense_select_hostname_exact_device_query._perform_query()]
    assert len(results) == 1
    assert defense_select_hostname_exact_device_query._count() == len(results)
    device = results[0]
    assert device._model_unique_id == 43407
    assert device.deviceId == 43407
    assert isinstance(device, Device)
    # assert device.validate()


# validate is failing on these Device objects? When it enters the validate() function,
# self = <[TypeError("argument of type 'NoneType' is not iterable") raised in repr()] Device object at 0x10d224a50>
def test_device_query_2(cbcsdk_mock):
    """Testing select() method with .where() ownerName"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", DEFENSE_DEVICE_GET_OWNERNAME_RESP)
    api = cbcsdk_mock.api
    defense_select_ownername_device_query = api.select(Device).where('ownerName:smultani@carbonblack.com')
    results = [result for result in defense_select_ownername_device_query._perform_query()]
    assert defense_select_ownername_device_query._count() == len(results)
    device = results[0]
    assert device.email == "smultani@carbonblack.com"
    assert isinstance(device, Device)
    # assert device.validate()


# validate is failing on these Device objects? When it enters the validate() function,
# self = <[TypeError("argument of type 'NoneType' is not iterable") raised in repr()] Device object at 0x10d224a50>
def test_device_query_3(cbcsdk_mock):
    """Testing select() method with .where() ownerNameExact"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", DEFENSE_DEVICE_GET_OWNERNAME_EXACT_RESP)
    api = cbcsdk_mock.api
    defense_select_ownername_exact_device_query = api.select(Device).where('ownerNameExact:smultani@carbonblack.com')
    results = [result for result in defense_select_ownername_exact_device_query._perform_query()]
    assert len(results) == 5
    assert defense_select_ownername_exact_device_query._count() == len(results)
    device = results[0]
    assert device._model_unique_id == 20572
    assert device.deviceId == 20572
    assert isinstance(device, Device)
    # assert device.validate()


# validate is failing on these Device objects? When it enters the validate() function,
# self = <[TypeError("argument of type 'NoneType' is not iterable") raised in repr()] Device object at 0x10d224a50>
def test_device_query_4(cbcsdk_mock):
    """Testing select() method with .where() ipAddress"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", DEFENSE_DEVICE_GET_IP_RESP)
    api = cbcsdk_mock.api
    defense_select_ip_device_query = api.select(Device).where('ipAddress:10.210.34.165')
    results = [result for result in defense_select_ip_device_query._perform_query()]
    assert len(results) == 1
    assert defense_select_ip_device_query._count() == len(results)
    device = results[0]
    assert device._model_unique_id == 43407
    assert device.deviceId == 43407
    assert isinstance(device, Device)
    # assert device.validate()


# validate is failing on these Device objects? When it enters the validate() function,
# self = <[TypeError("argument of type 'NoneType' is not iterable") raised in repr()] Device object at 0x10d224a50>
def test_device_query_with_and(cbcsdk_mock):
    """Testing Device Querying with .where() and .and_()"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", DEFENSE_DEVICE_GET_HOST_IP_RESP)
    api = cbcsdk_mock.api
    select_hostname_and_ip_device_query = api.select(Device).where('hostName:Win7x64').and_('ipAddress:10.210.34.165')
    results = [result for result in select_hostname_and_ip_device_query._perform_query()]
    assert len(results) == 1
    assert select_hostname_and_ip_device_query._count() == len(results)
    device = results[0]
    assert device._model_unique_id == 43407
    assert device.deviceId == 43407
    assert isinstance(device, Device)
    # assert device.validate()


# validate works with this one???
def test_device_query_with_id_in_select(cbcsdk_mock):
    """Testing Device Querying with .select(Device, `device_id`)"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", DEFENSE_DEVICE_GET_SPECIFIC_RESP)
    api = cbcsdk_mock.api
    defense_device_select_with_id = api.select(Device, 12345)
    assert isinstance(defense_device_select_with_id, Device)
    defense_device_select_with_id.refresh()
    assert defense_device_select_with_id._model_unique_id == 12345
    assert defense_device_select_with_id.deviceId == 12345
    assert defense_device_select_with_id.validate()


# validate is failing on these Device objects? When it enters the validate() function,
# self = <[TypeError("argument of type 'NoneType' is not iterable") raised in repr()] Device object at 0x10d224a50>
def test_device_get_all(cbcsdk_mock):
    """Testing Device Querying for all devices"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", DEFENSE_DEVICE_GET_ALL_RESP)
    api = cbcsdk_mock.api
    defense_device_select_all = api.select(Device)
    results = [result for result in defense_device_select_all._perform_query()]
    assert isinstance(defense_device_select_all, Query)
    assert len(results) == 52
    dev = results[0]
    assert isinstance(dev, Device)
    # dev.validate()


def test_device_search(cbcsdk_mock):
    """Testing Device _search()"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", DEFENSE_DEVICE_GET_ALL_RESP)
    api = cbcsdk_mock.api
    defense_device_select_all = api.select(Device)
    assert isinstance(defense_device_select_all, Query)
    query = defense_device_select_all._search(start=0, rows=100)
    results = [result for result in query]
    assert len(results) == 52


def test_device_search_with_where(cbcsdk_mock):
    """Testing Device _search() with hostname and ip where clauses"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", DEFENSE_DEVICE_GET_HOST_IP_RESP)
    api = cbcsdk_mock.api
    defense_device_select_host_ip = api.select(Device).where('hostName:Win7x64').and_('ipAddress:10.210.34.165')
    assert isinstance(defense_device_select_host_ip, Query)
    query = defense_device_select_host_ip._search(start=0, rows=100)
    results = [result for result in query]
    assert len(results) == 1
    found_dev = results[0]
    assert found_dev['deviceId'] == 43407
    assert found_dev['name'] == 'Win7x64'
    dev = Device(api, found_dev['deviceId'], found_dev)
    assert isinstance(dev, Device)
    # dev.validate()
