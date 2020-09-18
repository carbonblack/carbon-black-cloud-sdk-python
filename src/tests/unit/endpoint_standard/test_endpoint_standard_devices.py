"""Testing Device object of cbc_sdk.endpoint_standard"""

import pytest
import logging
from cbc_sdk.endpoint_standard import Device, Query
from cbc_sdk.endpoint_standard.base import EndpointStandardMutableModel
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_devices import (ENDPOINT_STANDARD_DEVICE_GET_HOSTNAME_RESP,
                                                      ENDPOINT_STANDARD_DEVICE_GET_HOSTNAME_RESP_0,
                                                      ENDPOINT_STANDARD_DEVICE_GET_HOSTNAME_EXACT_RESP,
                                                      ENDPOINT_STANDARD_DEVICE_GET_OWNERNAME_RESP,
                                                      ENDPOINT_STANDARD_DEVICE_GET_OWNERNAME_EXACT_RESP,
                                                      ENDPOINT_STANDARD_DEVICE_GET_IP_RESP,
                                                      ENDPOINT_STANDARD_DEVICE_GET_HOST_IP_RESP,
                                                      ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP,
                                                      ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP_1,
                                                      ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP_2,
                                                      ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP_3,
                                                      ENDPOINT_STANDARD_DEVICE_GET_ALL_RESP,
                                                      ENDPOINT_STANDARD_DEVICE_PATCH_RESP)

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
    """Testing select() method with .where() hostName"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_GET_HOSTNAME_RESP_0)
    api = cbcsdk_mock.api
    # testing hostName in quotes
    hostname_device_query = api.select(Device).where('hostName:Win7x64')
    results = [result for result in hostname_device_query._perform_query()]
    assert len(results) == 1
    assert results[0].validate()

    # testing hostName with keyword
    keyword_hostname_device_query = api.select(Device).where(hostName='Win7x64')
    results = [result for result in keyword_hostname_device_query._perform_query()]
    assert len(results) == 1
    assert keyword_hostname_device_query._count() == len(results)
    first_device_result = results[0]
    assert isinstance(first_device_result, Device)
    assert first_device_result._model_unique_id == 12345
    assert first_device_result.deviceId == 12345
    assert first_device_result.validate()


def test_device_query_1(cbcsdk_mock):
    """Testing select() method with .where() hostNameExact"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/98765", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP_2)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_GET_HOSTNAME_RESP)
    api = cbcsdk_mock.api
    # testing hostNameExact in quotes
    endpoint_standard_select_hostname_exact_device_query = api.select(Device).where('hostNameExact:Win7x64')
    results = [result for result in endpoint_standard_select_hostname_exact_device_query._perform_query()]
    assert len(results) == 1
    assert endpoint_standard_select_hostname_exact_device_query._count() == len(results)
    device = results[0]
    assert device._model_unique_id == 98765
    assert device.deviceId == 98765
    assert isinstance(device, Device)
    assert device.validate()

    # testing hostNameExact keyword
    keyword_hostname_device_query = api.select(Device).where(hostNameExact='Win7x64')
    results = [result for result in keyword_hostname_device_query._perform_query()]
    assert len(results) == 1
    assert keyword_hostname_device_query._count() == len(results)
    first_device_result = results[0]
    assert isinstance(first_device_result, Device)
    assert first_device_result._model_unique_id == 98765
    assert first_device_result.deviceId == 98765
    assert first_device_result.validate()

def test_device_query_2(cbcsdk_mock):
    """Testing select() method with .where() ownerName"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/23456", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_GET_OWNERNAME_RESP)
    api = cbcsdk_mock.api
    # testing ownerName in quotes
    endpoint_standard_select_ownername_device_query = api.select(Device).where('ownerName:email@example.com')
    results = [result for result in endpoint_standard_select_ownername_device_query._perform_query()]
    assert endpoint_standard_select_ownername_device_query._count() == len(results)
    device = results[0]
    assert device.email == "email@example.com"
    assert isinstance(device, Device)
    assert device.validate()

    # testing ownerName keyword
    keyword_endpoint_standard_select_ownername_device_query = api.select(Device).where(ownerName='email@example.com')
    results = [result for result in keyword_endpoint_standard_select_ownername_device_query._perform_query()]
    assert keyword_endpoint_standard_select_ownername_device_query._count() == len(results)
    device = results[0]
    assert device.email == "email@example.com"
    assert isinstance(device, Device)
    assert device.validate()


def test_device_query_3(cbcsdk_mock):
    """Testing select() method with .where() ownerNameExact"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/23456", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP_3)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_GET_OWNERNAME_EXACT_RESP)
    api = cbcsdk_mock.api
    # testing ownerNameExact in quotes
    endpoint_standard_select_ownername_exact_device_query = api.select(Device).where('ownerNameExact:email@example.com')
    results = [result for result in endpoint_standard_select_ownername_exact_device_query._perform_query()]
    assert len(results) == 2
    assert endpoint_standard_select_ownername_exact_device_query._count() == len(results)
    device = results[0]
    assert device._model_unique_id == 23456
    assert device.deviceId == 23456
    assert isinstance(device, Device)
    assert device.validate()

    print(cbcsdk_mock.mocks.keys())

    # testing ownerNameExact keyword
    keyword_endpoint_standard_select_ownername_exact_device_query = api.select(Device).where(
        ownerNameExact='email@example.com')
    results = [result for result in keyword_endpoint_standard_select_ownername_exact_device_query._perform_query()]
    assert len(results) == 2
    assert keyword_endpoint_standard_select_ownername_exact_device_query._count() == len(results)
    device = results[0]
    assert device._model_unique_id == 23456
    assert device.deviceId == 23456
    assert isinstance(device, Device)
    assert device.validate()


def test_device_query_4(cbcsdk_mock):
    """Testing select() method with .where() ipAddress"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/98765", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP_2)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_GET_IP_RESP)
    api = cbcsdk_mock.api
    # testing ipAddress in quotes
    endpoint_standard_select_ip_device_query = api.select(Device).where('ipAddress:192.10.34.165')
    results = [result for result in endpoint_standard_select_ip_device_query._perform_query()]
    assert len(results) == 1
    assert endpoint_standard_select_ip_device_query._count() == len(results)
    device = results[0]
    assert device._model_unique_id == 98765
    assert device.deviceId == 98765
    assert isinstance(device, Device)
    assert device.validate()

    # testing ipAddress keyword
    keyword_endpoint_standard_select_ip_device_query = api.select(Device).where(ipAddress='192.10.34.165')
    results = [result for result in keyword_endpoint_standard_select_ip_device_query._perform_query()]
    assert len(results) == 1
    assert keyword_endpoint_standard_select_ip_device_query._count() == len(results)
    device = results[0]
    assert device._model_unique_id == 98765
    assert device.deviceId == 98765
    assert isinstance(device, Device)
    assert device.validate()


def test_device_query_with_and(cbcsdk_mock):
    """Testing Device Querying with .where() and .and_()"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/98765", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP_2)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_GET_HOST_IP_RESP)
    api = cbcsdk_mock.api
    # testing multiple where/and clauses
    select_hostname_and_ip_device_query = api.select(Device).where('hostName:Win7x64').and_('ipAddress:192.10.34.165')
    results = [result for result in select_hostname_and_ip_device_query._perform_query()]
    assert len(results) == 1
    assert select_hostname_and_ip_device_query._count() == len(results)
    device = results[0]
    assert device._model_unique_id == 98765
    assert device.deviceId == 98765
    assert isinstance(device, Device)
    assert device.validate()


def test_device_query_with_id_in_select(cbcsdk_mock):
    """Testing Device Querying with .select(Device, `device_id`)"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    api = cbcsdk_mock.api
    endpoint_standard_device_select_with_id = api.select(Device, 12345)
    assert isinstance(endpoint_standard_device_select_with_id, Device)
    endpoint_standard_device_select_with_id.refresh()
    assert endpoint_standard_device_select_with_id._model_unique_id == 12345
    assert endpoint_standard_device_select_with_id.deviceId == 12345
    assert endpoint_standard_device_select_with_id.validate()


def test_device_get_all(cbcsdk_mock):
    """Testing Device Querying for all devices"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_GET_ALL_RESP)
    api = cbcsdk_mock.api
    endpoint_standard_device_select_all = api.select(Device)
    results = [result for result in endpoint_standard_device_select_all._perform_query()]
    assert isinstance(endpoint_standard_device_select_all, Query)
    assert len(results) == 4
    dev = results[0]
    assert isinstance(dev, Device)
    assert dev._model_unique_id == 12345
    dev.validate()


def test_device_search(cbcsdk_mock):
    """Testing Device _search()"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_GET_ALL_RESP)
    api = cbcsdk_mock.api
    endpoint_standard_device_select_all = api.select(Device)
    assert isinstance(endpoint_standard_device_select_all, Query)
    query = endpoint_standard_device_select_all._search(start=0, rows=100)
    results = [result for result in query]
    assert len(results) == 4


def test_device_search_with_where(cbcsdk_mock):
    """Testing Device _search() with hostname and ip where clauses"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/98765", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_GET_HOST_IP_RESP)
    api = cbcsdk_mock.api
    endpoint_standard_device_select_host_ip = api.select(Device).where('hostName:Win7x64').and_('ipAddress:192.10.34.165')
    assert isinstance(endpoint_standard_device_select_host_ip, Query)
    query = endpoint_standard_device_select_host_ip._search(start=0, rows=100)
    results = [result for result in query]
    assert len(results) == 1
    found_dev = results[0]
    assert found_dev['deviceId'] == 98765
    assert found_dev['name'] == 'Win7x64'
    dev = Device(api, found_dev['deviceId'], found_dev)
    assert isinstance(dev, Device)
    dev.validate()


def test_endpoint_mutable_model_query_implementation(cbcsdk_mock):
    """Testing EndpointStandardMutableModel._query_implementation()."""
    model = EndpointStandardMutableModel(cbcsdk_mock.api)
    assert isinstance(model._query_implementation(cbcsdk_mock.api), Query)


def test_endpoint_mutable_model_update_object(cbcsdk_mock):
    """Testing EndpointStandardMutableModel._query_implementation()."""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    model = Device(cbcsdk_mock.api, model_unique_id=12345)
    cbcsdk_mock.mock_request("PATCH", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_PATCH_RESP)
    assert isinstance(model, EndpointStandardMutableModel)
    assert model._change_object_http_method == "PATCH"
    # when _change_object_http_method is PATCH, the _update_object method makes a PATCH API call
    update = model._update_object()
    patch = model._patch_object()
    assert update == patch

    model._change_object_http_method = "POST"
    # when _change_object_http_method is != "PATCH", the _update_object method makes a POST API call
    update = model._update_object()
    update_entire = model._update_entire_object()
    assert update == update_entire


def test_endpoint_mutable_model_update_entire_object(cbcsdk_mock):
    """Testing EndpointStandardDevice._update_entire_object()."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    model = Device(api, model_unique_id=12345)
    cbcsdk_mock.mock_request("PATCH", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_PATCH_RESP)
    # if model_unique_id has not been modified, _update_entire_object method makes a POST API call to update
    update_entire = model._update_entire_object()

    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    updated_obj_resp = cbcsdk_mock.StubResponse({"success": True, "deviceId": 12345}, text="text in response", scode=200)
    refresh = model._refresh_if_needed(updated_obj_resp)
    assert refresh == update_entire

    # if model_unique_id is None or has been modified, _update_entire_object method makes a PATCH API Call
    model._set("deviceId", 54321)
    assert model.__class__.primary_key in model._dirty_attributes.keys()
    cbcsdk_mock.mock_request("PATCH", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_PATCH_RESP)
    update_entire = model._update_entire_object()

    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/54321", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    new_obj_response = cbcsdk_mock.StubResponse({"success": True, "deviceId": 54321}, text="text in response", scode=200)
    refresh = model._refresh_if_needed(new_obj_response)
    assert refresh == update_entire

    # clear _dirty_attributes for further tests
    model.reset()


def test_endpoint_mutable_model_patch_object(cbcsdk_mock):
    """Testing EndpointStandardMutableModel._patch_object()."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    model = Device(api, model_unique_id=12345)
    model._set("deviceId", 56789)
    assert model.deviceId == 56789
    assert model.__class__.primary_key in model._dirty_attributes.keys()
    cbcsdk_mock.mock_request("PATCH", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_PATCH_RESP)
    patch_object_return = model._patch_object()

    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/56789", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    new_obj_response = cbcsdk_mock.StubResponse({"success": True, "deviceId": 56789}, text="text in response", scode=200)
    patched_device = model._refresh_if_needed(new_obj_response)

    assert patch_object_return == patched_device
