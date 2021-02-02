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

"""Unit test code for USBDeviceApproval"""

import pytest
import logging
from cbc_sdk.endpoint_standard import USBDeviceApproval, USBDevice
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_usb_devices import (USBDEVICE_APPROVAL_GET_RESP,
                                                                    USBDEVICE_APPROVAL_PUT_RESP,
                                                                    USBDEVICE_APPROVAL_QUERY_RESP,
                                                                    USBDEVICE_APPROVAL_BULK_CREATE_REQ,
                                                                    USBDEVICE_APPROVAL_BULK_CREATE_RESP,
                                                                    USBDEVICE_GET_RESP)

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

def test_approval_get_and_modify(cbcsdk_mock):
    """Tests a simple load, modify, and store of an approval object."""
    def put_validate(url, body, **kwargs):
        assert body["approval_name"] == "Altered Approval"
        assert body["notes"] == "Altered state"
        assert body["vendor_id"] == "0x0781"
        assert body["product_id"] == "0x5581"
        return USBDEVICE_APPROVAL_PUT_RESP

    cbcsdk_mock.mock_request("GET", "/device_control/v3/orgs/test/approvals/10373", USBDEVICE_APPROVAL_GET_RESP)
    cbcsdk_mock.mock_request("PUT", "/device_control/v3/orgs/test/approvals/10373", put_validate)
    api = cbcsdk_mock.api
    approval = USBDeviceApproval(api, "10373")
    assert approval._model_unique_id == "10373"
    assert approval.vendor_id == "0x0781"
    assert approval.vendor_name == "SanDisk"
    assert approval.product_id == "0x5581"
    assert approval.product_name == "Ultra"
    assert approval.approval_name == "Example Approval"

    approval.notes = "Altered state"
    approval.approval_name = "Altered Approval"
    approval.save()
    assert approval.vendor_id == "0x0781"
    assert approval.vendor_name == "SanDisk"
    assert approval.product_id == "0x5581"
    assert approval.product_name == "Ultra"
    assert approval.notes == "Altered state"
    assert approval.approval_name == "Altered Approval"


def test_approval_create_and_save(cbcsdk_mock):
    """Tests a new approval being created and saved."""
    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/approvals/_bulk",
                             USBDEVICE_APPROVAL_BULK_CREATE_RESP)
    api = cbcsdk_mock.api
    approval = USBDeviceApproval(api, None)
    approval.vendor_id = "0x0781"
    approval.product_id = "0x5581"
    approval.serial_number = "4C531001331122115172"
    approval.notes = "A few notes"
    approval.approval_name = "Example Approval"
    approval.save()
    assert approval._model_unique_id == "10373"
    assert approval.vendor_id == "0x0781"
    assert approval.vendor_name == "SanDisk"
    assert approval.product_id == "0x5581"
    assert approval.product_name == "Ultra"
    assert approval.approval_name == "Example Approval"
    assert approval.notes == "A few notes"


def test_approval_query_and_delete(cbcsdk_mock):
    """Tests a simple query and delete of an approval object."""
    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/approvals/_search", USBDEVICE_APPROVAL_QUERY_RESP)
    cbcsdk_mock.mock_request("DELETE", "/device_control/v3/orgs/test/approvals/10373",
                             CBCSDKMock.StubResponse(None, scode=204))
    api = cbcsdk_mock.api
    query = api.select(USBDeviceApproval).where('*')
    results = [result for result in query._perform_query()]
    assert len(results) == 1
    assert query._count() == len(results)
    approval = results[0]
    assert approval._model_unique_id == "10373"
    assert approval.vendor_id == "0x0781"
    assert approval.vendor_name == "SanDisk"
    assert approval.product_id == "0x5581"
    assert approval.product_name == "Ultra"
    assert approval.approval_name == "Example Approval"
    approval.delete()


def test_approval_query_with_all_bells_and_whistles(cbcsdk_mock):
    """Tests running the query with all values set."""
    def post_validate(url, body, **kwargs):
        assert body['query'] == '*'
        crits = body['criteria']
        assert crits['device.id'] == ['A1000', 'B1000', 'C1000']
        assert crits['vendor_name'] == ['SanDisk']
        assert crits['product_name'] == ['Ultra']
        return USBDEVICE_APPROVAL_QUERY_RESP

    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/approvals/_search", post_validate)
    api = cbcsdk_mock.api
    query = api.select(USBDeviceApproval).where('*').set_device_ids(['A1000', 'B1000']).set_vendor_names(['SanDisk']) \
                                         .set_product_names(['Ultra']).set_device_ids(['C1000'])
    assert query._count() == 1
    results = [result for result in query._perform_query()]
    assert len(results) == 1
    approval = results[0]
    assert approval._model_unique_id == "10373"
    assert approval.vendor_id == "0x0781"
    assert approval.vendor_name == "SanDisk"
    assert approval.product_id == "0x5581"
    assert approval.product_name == "Ultra"
    assert approval.approval_name == "Example Approval"


def test_approval_query_async(cbcsdk_mock):
    """Test running the query in asynchronous mode."""
    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/approvals/_search", USBDEVICE_APPROVAL_QUERY_RESP)
    api = cbcsdk_mock.api
    future = api.select(USBDeviceApproval).where('*').execute_async()
    results = future.result()
    assert len(results) == 1
    approval = results[0]
    assert approval._model_unique_id == "10373"
    assert approval.vendor_id == "0x0781"
    assert approval.vendor_name == "SanDisk"
    assert approval.product_id == "0x5581"
    assert approval.product_name == "Ultra"
    assert approval.approval_name == "Example Approval"


def test_approval_query_parameters_validate_fail(cbcsdk_mock):
    """Test that we get the appropriate exceptions when we pass in bogus parameters."""
    query = cbcsdk_mock.api.select(USBDeviceApproval)
    with pytest.raises(ApiError):
        query.set_device_ids([1])
    with pytest.raises(ApiError):
        query.set_vendor_names([2])
    with pytest.raises(ApiError):
        query.set_product_names([3])


def test_approval_create_from_usb_device(cbcsdk_mock):
    """Test the create_from_usb_device function."""
    api = cbcsdk_mock.api
    usb = USBDevice(api, USBDEVICE_GET_RESP["id"], USBDEVICE_GET_RESP)
    approval = USBDeviceApproval.create_from_usb_device(usb)
    assert approval.serial_number == "4C531001331122115172"
    assert approval.vendor_id == "0x0781"
    assert approval.product_id == "0x5581"


def test_approval_bulk_create(cbcsdk_mock):
    """Test the bulk_create function."""
    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/approvals/_bulk",
                             USBDEVICE_APPROVAL_BULK_CREATE_RESP)
    api = cbcsdk_mock.api
    results = USBDeviceApproval.bulk_create(api, USBDEVICE_APPROVAL_BULK_CREATE_REQ)
    assert len(results) == 2
    approval = results[0]
    assert approval._model_unique_id == "10373"
    assert approval.vendor_id == "0x0781"
    assert approval.vendor_name == "SanDisk"
    assert approval.product_id == "0x5581"
    assert approval.product_name == "Ultra"
    assert approval.approval_name == "Example Approval"
    approval = results[1]
    assert approval._model_unique_id == "10444"
    assert approval.vendor_id == "0x0666"
    assert approval.vendor_name == "Sirius Cybernetics Corp."
    assert approval.product_id == "0x6969"
    assert approval.product_name == "Happy Hard Drive"
    assert approval.approval_name == "Example Approval2"


def test_approval_bulk_create_csv(cbcsdk_mock):
    """Test the bulk_create_csv function."""
    req = "vendor_id,product_id,serial_number,approval_name,notes\n" \
          "0x0781,0x5581,4C531001331122115172,Example Approval,A few notes\n" \
          "0x0666,0x6969,4Q2123456789,Example Approval2,Whatever"

    def post_validate(url, body, **kwargs):
        assert body == req
        headers = kwargs.pop('headers')
        assert headers['Content-Type'] == 'text/csv'
        return USBDEVICE_APPROVAL_BULK_CREATE_RESP

    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/approvals/_bulk", post_validate)
    api = cbcsdk_mock.api
    results = USBDeviceApproval.bulk_create_csv(api, req)
    assert len(results) == 2
    approval = results[0]
    assert approval._model_unique_id == "10373"
    assert approval.vendor_id == "0x0781"
    assert approval.vendor_name == "SanDisk"
    assert approval.product_id == "0x5581"
    assert approval.product_name == "Ultra"
    assert approval.approval_name == "Example Approval"
    approval = results[1]
    assert approval._model_unique_id == "10444"
    assert approval.vendor_id == "0x0666"
    assert approval.vendor_name == "Sirius Cybernetics Corp."
    assert approval.product_id == "0x6969"
    assert approval.product_name == "Happy Hard Drive"
    assert approval.approval_name == "Example Approval2"
