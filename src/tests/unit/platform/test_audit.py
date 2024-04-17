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

"""Tests for the audit logs APIs."""

import pytest
from cbc_sdk.errors import ApiError
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.platform import AuditLog, AuditLogRecord
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_audit import AUDITLOGS_RESP, AUDIT_SEARCH_REQUEST, AUDIT_SEARCH_RESPONSE


@pytest.fixture(scope="function")
def cb():
    """Create CBCloudAPI singleton"""
    return CBCloudAPI(
        url="https://example.com", org_key="test", token="abcd/1234", ssl_verify=False
    )


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, cb):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, cb)


# ==================================== UNIT TESTS BELOW ====================================


def test_get_auditlogs(cbcsdk_mock):
    """Tests getting audit logs."""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/auditlogs", AUDITLOGS_RESP)
    api = cbcsdk_mock.api
    result = AuditLog.get_auditlogs(api)
    assert len(result) == 5


def test_search_audit_logs_with_all_bells_and_whistles(cbcsdk_mock):
    """Tests the generation and execution of a search request."""

    def on_post(url, body, **kwargs):
        assert body == AUDIT_SEARCH_REQUEST
        return AUDIT_SEARCH_RESPONSE

    cbcsdk_mock.mock_request("POST", "/audit_log/v1/orgs/test/logs/_search", on_post)
    api = cbcsdk_mock.api
    query = api.select(AuditLogRecord).where("description:FOO").add_criteria("actor_ip", ["10.29.99.1"])
    query.add_criteria("actor", ["ABCDEFGHIJ"]).add_criteria("request_url", ["https://inclusiveladyship.com"])
    query.add_criteria("description", ["FOOBAR"]).add_boolean_criteria("flagged", True)
    query.add_boolean_criteria("verbose", False)
    query.add_time_criteria(start="2024-03-01T00:00:00", end="2024-03-31T22:00:00")
    query.add_exclusions("actor_ip", ["10.29.99.254"]).add_exclusions("actor", ["JIHGFEDCBA"])
    query.add_exclusions("request_url", ["https://links.inclusiveladyship.com"])
    query.add_exclusions("description", ["BLORT"]).add_boolean_criteria("flagged", False, exclude=True)
    query.add_boolean_criteria("verbose", True, exclude=True)
    query.add_time_criteria(range="-5d", exclude=True).sort_by("actor_ip", "ASC")
    result_list = list(query)
    assert len(result_list) == 5
    assert query._count() == 5
    assert result_list[0].actor == "DEFGHIJKLM"
    assert result_list[0].actor_ip == "192.168.0.5"
    assert result_list[1].actor == "BELTALOWDA"
    assert result_list[1].actor_ip == "192.168.3.5"
    assert result_list[2].actor == "BELTALOWDA"
    assert result_list[2].actor_ip == "192.168.3.8"
    assert result_list[3].actor == "BELTALOWDA"
    assert result_list[3].actor_ip == "192.168.3.11"
    assert result_list[4].actor == "BELTALOWDA"
    assert result_list[4].actor_ip == "192.168.3.14"


def test_criteria_errors(cb):
    """Tests error handling in the criteria-setting functions on the query object."""
    query = cb.select(AuditLogRecord)
    with pytest.raises(ApiError):
        query.add_time_criteria(start="2024-03-01T00:00:00", end="2024-03-31T22:00:00", range="-5d")
    with pytest.raises(ApiError):
        query.add_time_criteria(start="2024-03-01T00:00:00")
    with pytest.raises(ApiError):
        query.add_time_criteria(end="2024-03-31T22:00:00")
    with pytest.raises(ApiError):
        query.add_time_criteria(start="2024-03-01T00:00:00", range="-5d")
    with pytest.raises(ApiError):
        query.add_time_criteria(end="2024-03-31T22:00:00", range="-5d")
    with pytest.raises(ApiError):
        query.add_time_criteria(start="BOGUS", end="2024-03-31T22:00:00")
    with pytest.raises(ApiError):
        query.sort_by("actor_ip", "BOGUS")


def test_async_search_audit_logs(cbcsdk_mock):
    """Tests async query of audit logs."""
    cbcsdk_mock.mock_request("POST", "/audit_log/v1/orgs/test/logs/_search", AUDIT_SEARCH_RESPONSE)
    api = cbcsdk_mock.api
    query = api.select(AuditLogRecord)
    future = query.execute_async()
    result_list = future.result()
    assert isinstance(result_list, list)
    assert len(result_list) == 5
    assert result_list[0].actor == "DEFGHIJKLM"
    assert result_list[0].actor_ip == "192.168.0.5"
    assert result_list[1].actor == "BELTALOWDA"
    assert result_list[1].actor_ip == "192.168.3.5"
    assert result_list[2].actor == "BELTALOWDA"
    assert result_list[2].actor_ip == "192.168.3.8"
    assert result_list[3].actor == "BELTALOWDA"
    assert result_list[3].actor_ip == "192.168.3.11"
    assert result_list[4].actor == "BELTALOWDA"
    assert result_list[4].actor_ip == "192.168.3.14"
