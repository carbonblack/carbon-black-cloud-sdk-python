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
from cbc_sdk.endpoint_standard import USBDeviceBlock
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ServerError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_usb_devices import (USBDEVICE_BLOCK_GET_RESP,
                                                                    USBDEVICE_BLOCK_GET_ALL_RESP,
                                                                    USBDEVICE_BLOCK_CREATE_RESP,
                                                                    USBDEVICE_BLOCK_BULK_CREATE_RESP)


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

def test_block_get_and_delete(cbcsdk_mock):
    """Tests a simple load and delete of a block object."""
    cbcsdk_mock.mock_request("GET", "/device_control/v3/orgs/test/blocks/55", USBDEVICE_BLOCK_GET_RESP)
    cbcsdk_mock.mock_request("DELETE", "/device_control/v3/orgs/test/blocks/55",
                             CBCSDKMock.StubResponse(None, scode=204))
    api = cbcsdk_mock.api
    block = USBDeviceBlock(api, 55)
    assert block._model_unique_id == 55
    assert block.policy_id == "6997287"
    block.delete()


def test_block_get_all_and_fail_delete(cbcsdk_mock):
    """Tests the load of all block objects and a failed delete."""
    cbcsdk_mock.mock_request("GET", "/device_control/v3/orgs/test/blocks", USBDEVICE_BLOCK_GET_ALL_RESP)
    cbcsdk_mock.mock_request("DELETE", "/device_control/v3/orgs/test/blocks/55",
                             CBCSDKMock.StubResponse(None, scode=500, text="Blow Up", json_parsable=False))
    api = cbcsdk_mock.api
    query = api.select(USBDeviceBlock)
    assert query._count() == 1
    results = [result for result in query._perform_query()]
    assert len(results) == 1
    block = results[0]
    assert block._model_unique_id == 55
    assert block.policy_id == "6997287"
    with pytest.raises(ServerError):
        block.delete()


def test_block_get_all_async(cbcsdk_mock):
    """Tests the load of all block objects asynchronously."""
    cbcsdk_mock.mock_request("GET", "/device_control/v3/orgs/test/blocks", USBDEVICE_BLOCK_GET_ALL_RESP)
    api = cbcsdk_mock.api
    future = api.select(USBDeviceBlock).execute_async()
    results = future.result()
    assert len(results) == 1
    block = results[0]
    assert block._model_unique_id == 55
    assert block.policy_id == "6997287"


def test_block_create(cbcsdk_mock):
    """Tests the create function."""
    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/blocks/_bulk", USBDEVICE_BLOCK_CREATE_RESP)
    api = cbcsdk_mock.api
    block = USBDeviceBlock.create(api, "9686969")
    assert block._model_unique_id == 44
    assert block.policy_id == "9686969"


def test_block_bulk_create(cbcsdk_mock):
    """Tests the bulk_create function."""
    cbcsdk_mock.mock_request("POST", "/device_control/v3/orgs/test/blocks/_bulk",
                             USBDEVICE_BLOCK_BULK_CREATE_RESP)
    api = cbcsdk_mock.api
    results = USBDeviceBlock.bulk_create(api, ["6997287", "6998088"])
    assert len(results) == 2
    block = results[0]
    assert block._model_unique_id == 55
    assert block.policy_id == "6997287"
    block = results[1]
    assert block._model_unique_id == 65
    assert block.policy_id == "6998088"
