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
import copy
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
    l = list(query)
    assert len(l) == 5
    assert l[0].actor == "DEFGHIJKLM"
    assert l[0].actor_ip == "192.168.0.5"
    assert l[1].actor == "BELTALOWDA"
    assert l[1].actor_ip == "192.168.3.5"
    assert l[2].actor == "BELTALOWDA"
    assert l[2].actor_ip == "192.168.3.8"
    assert l[3].actor == "BELTALOWDA"
    assert l[3].actor_ip == "192.168.3.11"
    assert l[4].actor == "BELTALOWDA"
    assert l[4].actor_ip == "192.168.3.14"
