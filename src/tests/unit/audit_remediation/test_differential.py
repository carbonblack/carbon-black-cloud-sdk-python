#!/usr/bin/env python3

# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2024. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Unit test code for Differential Analysis API"""

import logging
import pytest
from cbc_sdk.audit_remediation import Differential
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.audit_remediation.mock_differential import (QUERY_COMPARISON_COUNT_ONLY,
                                                                     QUERY_COMPARISON_ACTUAL_CHANGES,
                                                                     QUERY_COMPARISON_SET_DEVICE_ID)


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


def test_differential_bogus_parameters(cbcsdk_mock):
    """Test that we get the appropriate exceptions when we pass in bogus or no parameters."""
    cbcsdk_mock.mock_request("POST",
                             "/livequery/v1/orgs/test/differential/runs/_search",
                             QUERY_COMPARISON_COUNT_ONLY)
    api = cbcsdk_mock.api
    query = api.select(Differential).newer_run_id("qpopjb82whlmthlo0x1wrwcnoyxmrueu")
    with pytest.raises(ApiError):
        query.older_run_id("")
    with pytest.raises(ApiError):
        query.older_run_id(1)
    with pytest.raises(ApiError):
        query.set_device_ids(["BOGUS"])
    with pytest.raises(ApiError):
        query.set_device_ids([""])
    with pytest.raises(ApiError):
        query.set_device_ids(["BOGUS", 12345])
    with pytest.raises(ApiError):
        query.count_only("")
    with pytest.raises(ApiError):
        query.count_only("BOGUS")
    with pytest.raises(ApiError):
        query.newer_run_id("")
    with pytest.raises(ApiError):
        query.newer_run_id(1)


def test_newer_run_id(cbcsdk_mock):
    """Test the required newer_run_id with default values for diff."""
    cbcsdk_mock.mock_request("POST",
                             "/livequery/v1/orgs/test/differential/runs/_search",
                             QUERY_COMPARISON_COUNT_ONLY)
    api = cbcsdk_mock.api
    query = api.select(Differential).newer_run_id("qpopjb82whlmthlo0x1wrwcnoyxmrueu")
    resp = query.submit()
    assert resp.older_run_id == "kibloccplynombvigcgtu2et2zayhzal"
    assert resp.diff_results[0]["changes"] == "null"


def test_older_run_id(cbcsdk_mock):
    """Test the older_run_id with default values for diff."""
    cbcsdk_mock.mock_request("POST",
                             "/livequery/v1/orgs/test/differential/runs/_search",
                             QUERY_COMPARISON_COUNT_ONLY)
    api = cbcsdk_mock.api
    query = api.select(Differential).newer_run_id("qpopjb82whlmthlo0x1wrwcnoyxmrueu") \
                                    .older_run_id("kibloccplynombvigcgtu2et2zayhzal")
    resp = query.submit()
    assert resp.older_run_id == "kibloccplynombvigcgtu2et2zayhzal"
    assert resp.diff_results[0]["changes"] == "null"


def test_count_only_false(cbcsdk_mock):
    """Test the required newer_run_id with actual changes."""
    cbcsdk_mock.mock_request("POST",
                             "/livequery/v1/orgs/test/differential/runs/_search",
                             QUERY_COMPARISON_ACTUAL_CHANGES)
    api = cbcsdk_mock.api
    query = api.select(Differential).newer_run_id("qpopjb82whlmthlo0x1wrwcnoyxmrueu").count_only(False)
    resp = query.submit()
    assert resp.diff_results[0]["changes"] != "null"


def test_count_only_true(cbcsdk_mock):
    """Test the required newer_run_id with actual changes."""
    cbcsdk_mock.mock_request("POST",
                             "/livequery/v1/orgs/test/differential/runs/_search",
                             QUERY_COMPARISON_COUNT_ONLY)
    api = cbcsdk_mock.api
    query = api.select(Differential).newer_run_id("qpopjb82whlmthlo0x1wrwcnoyxmrueu").count_only(True)
    resp = query.submit()
    assert resp.diff_results[0]["changes"] == "null"


def test_set_device_ids(cbcsdk_mock):
    """Test the device_ids criteria."""
    cbcsdk_mock.mock_request("POST",
                             "/livequery/v1/orgs/test/differential/runs/_search",
                             QUERY_COMPARISON_SET_DEVICE_ID)
    api = cbcsdk_mock.api
    query = api.select(Differential).newer_run_id("qpopjb82whlmthlo0x1wrwcnoyxmrueu").set_device_ids([11412673])
    resp = query.submit()
    assert len(resp.diff_results) == 1
    assert resp.diff_results[0]["device_id"] == 11412673


def test_build_url(cbcsdk_mock):
    """Test the _build_url that appends a prefix to the end of the url."""
    cbcsdk_mock.mock_request("POST",
                             "/livequery/v1/orgs/test/differential/runs/_search",
                             QUERY_COMPARISON_COUNT_ONLY)
    api = cbcsdk_mock.api
    resp = api.select(Differential).newer_run_id("qpopjb82whlmthlo0x1wrwcnoyxmrueu")
    url = resp._build_url("/hello")
    assert url == "/livequery/v1/orgs/test/differential/runs/_search/hello"
