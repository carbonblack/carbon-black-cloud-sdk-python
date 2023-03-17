#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020-2023. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Unit test code for USBDeviceApproval"""

import pytest
import logging
from cbc_sdk.endpoint_standard import USBDevice
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_usb_devices import (USBDEVICE_GET_RESP, USBDEVICE_GET_ENDPOINTS_RESP,
                                                                    USBDEVICE_GET_RESP_BEFORE_APPROVE,
                                                                    USBDEVICE_APPROVE_RESP,
                                                                    USBDEVICE_GET_RESP_AFTER_APPROVE,
                                                                    USBDEVICE_QUERY_RESP, USBDEVICE_FACET_RESP,
                                                                    USBDEVICE_GET_PRODUCTS_RESP,
                                                                    USBDEVICE_MULTIPLE_QUERY_RESP)


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

def test_usb_get_and_get_endpoints(cbcsdk_mock):
    """Tests getting a USB device by ID and getting its endpoints."""
    cbcsdk_mock.mock_request("GET", "/device_control/v3/orgs/test/devices/774", USBDEVICE_GET_RESP)
    cbcsdk_mock.mock_request("GET", "/device_control/v3/orgs/test/devices/774/endpoints", USBDEVICE_GET_ENDPOINTS_RESP)
    api = cbcsdk_mock.api
    usb = USBDevice(api, "774")
    assert usb._model_unique_id == "774"
    assert usb.vendor_name == "SanDisk"
    assert usb.product_name == "Ultra"
    assert usb.status == "APPROVED"
    endpoints = usb.get_endpoints()
    assert len(endpoints) == 2
    assert endpoints[0]["id"] == "53"
    assert endpoints[0]["endpoint_id"] == 7590378
    assert endpoints[0]["policy_id"] == 6997287
    assert endpoints[1]["id"] == "50"
    assert endpoints[1]["endpoint_id"] == 7579317
    assert endpoints[1]["policy_id"] == 6997287


def test_usb_get_and_approve(cbcsdk_mock):
    """Tests getting a USB device by ID and approving it, checking the resulting USBDeviceApproval as well."""
    approval_saved = False
    get_calls = 0

    def getter_func(url, query_parameters, default):
        nonlocal approval_saved, get_calls
        get_calls = get_calls + 1
        if approval_saved:
            return USBDEVICE_GET_RESP_AFTER_APPROVE
        else:
            return USBDEVICE_GET_RESP_BEFORE_APPROVE

    def approval_call(url, body, **kwargs):
        assert len(body) == 1
        request = body[0]
        assert request["vendor_id"] == "0x0781"
        assert request['product_id'] == "0x5581"
        assert request['serial_number'] == "4C531001331122115172"
        assert request['approval_name'] == 'ApproveTest'
        assert request['notes'] == 'Approval notes'
        nonlocal approval_saved
        approval_saved = True
        return USBDEVICE_APPROVE_RESP

    cbcsdk_mock.mock_request("GET", "/device_control/v3/orgs/test/devices/808", getter_func)
    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/approvals/_bulk", approval_call)
    api = cbcsdk_mock.api
    usb = USBDevice(api, "808")
    assert usb.vendor_name == "SanDisk"
    assert usb.product_name == "Ultra"
    assert usb.status == 'UNAPPROVED'
    approval = usb.approve('ApproveTest', 'Approval notes')
    assert approval.id == "12703"
    assert approval.vendor_id == usb.vendor_id
    assert approval.product_id == usb.product_id
    assert approval.serial_number == usb.serial_number
    assert approval.approval_name == 'ApproveTest'
    assert approval.notes == 'Approval notes'
    assert usb.status == 'APPROVED'
    assert get_calls == 2


def test_usb_query_with_all_bells_and_whistles(cbcsdk_mock):
    """Tests the USB query with all options set."""
    def post_validate(url, body, **kwargs):
        assert body['query'] == '*'
        crits = body['criteria']
        assert crits['endpoint.endpoint_name'] == ["DESKTOP-IL2ON7C", "ALPHA"]
        assert crits['product_name'] == ['Ultra']
        assert crits['serial_number'] == ['4C531001331122115172']
        assert crits['status'] == ['APPROVED']
        assert crits['vendor_name'] == ["SanDisk"]
        sorting = body['sort'][0]
        assert sorting['field'] == 'vendor_name'
        assert sorting['order'] == 'ASC'
        assert body['rows'] == 10
        return USBDEVICE_QUERY_RESP

    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/devices/_search", post_validate)
    api = cbcsdk_mock.api
    query = api.select(USBDevice).where('*').set_endpoint_names(["DESKTOP-IL2ON7C"]).set_product_names(["Ultra"]) \
               .set_serial_numbers(['4C531001331122115172']).set_statuses(['APPROVED']).set_vendor_names(["SanDisk"]) \
               .set_endpoint_names(["ALPHA"]).sort_by("vendor_name").set_max_rows(10)
    assert query._count() == 1
    results = [result for result in query._perform_query()]
    assert len(results) == 1
    usb = results[0]
    assert usb._model_unique_id == "774"
    assert usb.vendor_name == "SanDisk"
    assert usb.product_name == "Ultra"
    assert usb.status == "APPROVED"


def test_usb_query_length_num_available(cbcsdk_mock):
    """Tests the USB query with all options set."""
    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/devices/_search", USBDEVICE_MULTIPLE_QUERY_RESP)
    api = cbcsdk_mock.api
    query = api.select(USBDevice).where('*').set_max_rows(10)
    assert len(query) == 10
    results = [result for result in query._perform_query()]
    assert len(results) == 10


def test_usb_query_async(cbcsdk_mock):
    """Test running the query in asynchronous mode."""
    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/devices/_search", USBDEVICE_QUERY_RESP)
    api = cbcsdk_mock.api
    future = api.select(USBDevice).where('*').execute_async()
    results = future.result()
    assert len(results) == 1
    usb = results[0]
    assert usb._model_unique_id == "774"
    assert usb.vendor_name == "SanDisk"
    assert usb.product_name == "Ultra"
    assert usb.status == "APPROVED"


def test_usb_query_parameters_validate_fail(cbcsdk_mock):
    """Test that we get the appropriate exceptions when we pass in bogus parameters."""
    query = cbcsdk_mock.api.select(USBDevice)
    with pytest.raises(ApiError):
        query.set_endpoint_names([1])
    with pytest.raises(ApiError):
        query.set_product_names([2])
    with pytest.raises(ApiError):
        query.set_serial_numbers([3])
    with pytest.raises(ApiError):
        query.set_statuses(['BOGUS'])
    with pytest.raises(ApiError):
        query.set_vendor_names([4])
    with pytest.raises(ApiError):
        query.sort_by('thisfield', 'BOGUS')


def test_usb_query_facets(cbcsdk_mock):
    """Test the facet functionality of the USB device query."""
    def post_validate(url, body, **kwargs):
        assert body['query'] == '*'
        crits = body['criteria']
        assert crits['status'] == ['APPROVED']
        terms = body['terms']
        assert terms['fields'] == ['product_name']
        assert terms['rows'] == 0
        return USBDEVICE_FACET_RESP

    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/devices/_facet", post_validate)
    api = cbcsdk_mock.api
    query = api.select(USBDevice).where('*').set_statuses(['APPROVED'])
    results = query.facets(['product_name'])
    assert results[0]['field'] == 'product_name'
    values = results[0]['values']
    assert values[0]['name'] == 'Cruzer Dial'
    assert values[1]['name'] == 'Cruzer Glide'
    assert values[2]['name'] == 'U3 Cruzer Micro'
    assert values[3]['name'] == 'Ultra'
    assert values[4]['name'] == 'Ultra USB 3.0'


def test_usb_query_facets_not_valid(cbcsdk_mock):
    """Tests the error thrown when and invalid field name is passed to the facets function."""
    api = cbcsdk_mock.api
    query = api.select(USBDevice).where('*')
    with pytest.raises(ApiError):
        query.facets(['bogus'])


def test_usb_query_products_seen(cbcsdk_mock):
    """Test the get_vendors_and_products_seen function."""
    cbcsdk_mock.mock_request("GET", "/device_control/v3/orgs/test/products", USBDEVICE_GET_PRODUCTS_RESP)
    api = cbcsdk_mock.api
    results = USBDevice.get_vendors_and_products_seen(api)
    assert len(results) == 1
    assert results[0]['vendor_name'] == 'SanDisk'
    assert results[0]['devices_count'] == 5
    products = results[0]['products']
    assert len(products) == 5
    assert products[0]['product_name'] == 'U3 Cruzer Micro'
    assert products[1]['product_name'] == 'Cruzer Glide'
    assert products[2]['product_name'] == 'Ultra'
    assert products[3]['product_name'] == 'Ultra USB 3.0'
    assert products[4]['product_name'] == 'Cruzer Dial'
