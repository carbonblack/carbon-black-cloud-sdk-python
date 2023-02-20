# *******************************************************
# Copyright (c) VMware, Inc. 2020-2022. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Tests for the Live Response API."""

import pytest
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.mock_rest_api import (
    NOTIFICATIONS_RESP,
    AUDITLOGS_RESP,
    ALERT_SEARCH_SUGGESTIONS_RESP,
    PROCESS_SEARCH_VALIDATIONS_RESP,
    CUSTOM_SEVERITY_RESP,
    PROCESS_LIMITS_RESP,
    FETCH_PROCESS_QUERY_RESP,
    CONVERT_FEED_QUERY_RESP,
    OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    OBSERVATIONS_SEARCH_SUGGESTIONS_RESP,
)


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


def test_org_urn(cbcsdk_mock):
    """Tests the org_urn property."""
    api = cbcsdk_mock.api
    assert api.org_urn == "psc:org:test"


def test_get_notifications(cbcsdk_mock):
    """Tests getting notifications"""
    cbcsdk_mock.mock_request(
        "GET", "/integrationServices/v3/notification", NOTIFICATIONS_RESP
    )
    api = cbcsdk_mock.api
    result = api.get_notifications()
    assert len(result) == 2


def test_get_auditlogs(cbcsdk_mock):
    """Tests getting audit logs"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/auditlogs", AUDITLOGS_RESP)
    api = cbcsdk_mock.api
    result = api.get_auditlogs()
    assert len(result) == 5


def test_alert_search_suggestions(cbcsdk_mock):
    """Tests getting alert search suggestions"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/alerts/search_suggestions?suggest.q=",
        ALERT_SEARCH_SUGGESTIONS_RESP,
    )
    result = api.alert_search_suggestions("")
    assert len(result) == 20


def test_process_search_validations(cbcsdk_mock):
    """Tests getting process search validations"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v1/orgs/test/processes/search_validation?q=process",
        PROCESS_SEARCH_VALIDATIONS_RESP,
    )
    result = api.validate_process_query("process")
    assert result


def test_custom_severities(cbcsdk_mock):
    """Tests getting custom severities"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/severity",
        CUSTOM_SEVERITY_RESP,
    )
    result = api.custom_severities
    assert len(result) == 1
    assert result[0].report_id == "id"
    assert result[0].severity == 10


def test_process_limits(cbcsdk_mock):
    """Tests getting process limits"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/api/investigate/v1/orgs/test/processes/limits", PROCESS_LIMITS_RESP
    )
    result = api.process_limits()
    assert result["time_bounds"].get("upper") is not None
    assert result["time_bounds"].get("lower") is not None


def test_fetch_process_queries(cbcsdk_mock):
    """Tests getting process queries"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v1/orgs/test/processes/search_jobs",
        FETCH_PROCESS_QUERY_RESP,
    )
    result = api.fetch_process_queries()
    assert len(result) == 2
    assert result[0] == "4JDT3MX9Q/3867b4e7-b329-4caa-8f80-76899b1360fa"


def test_convert_feed_query(cbcsdk_mock):
    """Tests getting process queries"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/threathunter/feedmgr/v2/query/translate", CONVERT_FEED_QUERY_RESP
    )
    result = api.convert_feed_query("id:123")
    assert "process_guid:123" in result


def test_observations_search_validations(cbcsdk_mock):
    """Tests getting observations search validations"""
    api = cbcsdk_mock.api
    q = "?cb.max_backend_timestamp=2020-08-05T08%3A01%3A32.077Z&cb.min_backend_timestamp=" \
        "2020-08-04T08%3A01%3A32.077Z&suggest.q=device_id"
    cbcsdk_mock.mock_request(
        "GET",
        f"/api/investigate/v2/orgs/test/observations/search_validation{q}",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    result = api.observations_search_validation(
        "device_id", "2020-08-04T08:01:32.077Z", "2020-08-05T08:01:32.077Z"
    )
    assert result


def test_observations_search_suggestions(cbcsdk_mock):
    """Tests getting observations search suggestions"""
    api = cbcsdk_mock.api
    q = "suggest.count=10&suggest.q=device_id"
    cbcsdk_mock.mock_request(
        "GET",
        f"/api/investigate/v2/orgs/test/observations/search_suggestions?{q}",
        OBSERVATIONS_SEARCH_SUGGESTIONS_RESP,
    )
    result = api.observations_search_suggestions("device_id", 10)
    assert len(result) != 0
