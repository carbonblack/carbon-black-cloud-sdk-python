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

"""Tests of the Alerts V7 API queries."""
from datetime import datetime

import pytest

from cbc_sdk.errors import ApiError, TimeoutError, NonQueryableModel, ModelNotFound, FunctionalityDecommissioned
from cbc_sdk.platform import (
    BaseAlert,
    Alert,
    CBAnalyticsAlert,
    WatchlistAlert,
    ContainerRuntimeAlert,
    HostBasedFirewallAlert,
    IntrusionDetectionSystemAlert,
    DeviceControlAlert,
    Process
)
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.mock_rest_api import ALERT_SEARCH_SUGGESTIONS_RESP
from tests.unit.fixtures.platform.mock_alerts_v7 import (
    GET_ALERT_TYPE_WATCHLIST,
    GET_ALERT_TYPE_WATCHLIST_INVALID,
    GET_ALERT_RESP_WITH_NOTES,
    GET_ALERT_NOTES,
    CREATE_ALERT_NOTE_RESP,
    GET_ALERT_RESP,
    GET_ALERT_FACET_RESP_INVALID,
    GET_ALERT_FACET_RESP,
    GET_ALERT_v7_INTRUSION_DETECTION_SYSTEM_RESPONSE,
    GET_NEW_ALERT_TYPE_RESP
)
from tests.unit.fixtures.platform.mock_process import (
    POST_PROCESS_VALIDATION_RESP,
    POST_PROCESS_SEARCH_JOB_RESP,
    GET_PROCESS_SEARCH_JOB_RESP,
    GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
    GET_PROCESS_SUMMARY_STR,
    GET_PROCESS_NOT_FOUND,
    GET_PROCESS_SEARCH_JOB_RESULTS_RESP_WATCHLIST_ALERT_V7
)
from tests.unit.fixtures.platform.mock_observations import (
    POST_OBSERVATIONS_SEARCH_JOB_RESP,
    GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP,
    GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING
)

from tests.unit.fixtures.platform.mock_alert_v6_v7_compatibility import (
    GET_ALERT_v7_CB_ANALYTICS_RESPONSE,
    GET_ALERT_v7_WATCHLIST_RESPONSE,
    GET_ALERT_v7_DEVICE_CONTROL_RESPONSE,
    GET_ALERT_v7_HBFW_RESPONSE,
    GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE,
    GET_ALERT_HISTORY,
    GET_THREAT_HISTORY
)


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

def test_query_alert_with_all_bells_and_whistles(cbcsdk_mock):
    """Test an alert query with all options selected."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"device_id": ["6023"], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "id": ["S0L0"],
                                     "severity": ["6"], "device_policy_id": ["8675309"],
                                     "device_policy": ["Strict"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "process_reputation": ["SUSPECT_MALWARE"], "device_target_value": ["HIGH"],
                                     "threat_id": ["B0RG"], "workflow_status": ["OPEN"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG", "type": "WATCHLIST",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").add_criteria("device_id", ["6023"]) \
        .add_criteria("device_name", ["HAL"]).add_criteria("device_os", ["LINUX"]) \
        .add_criteria("device_os_version", ["0.1.2"]) \
        .add_criteria("device_username", ["JRN"]).add_criteria("id", ["S0L0"]) \
        .add_criteria("severity", "6").add_criteria("device_policy_id", ["8675309"]) \
        .add_criteria("device_policy", ["Strict"]).add_criteria("process_name", ["IEXPLORE.EXE"]) \
        .add_criteria("process_sha256", ["0123456789ABCDEF0123456789ABCDEF"]) \
        .add_criteria("process_reputation", ["SUSPECT_MALWARE"]) \
        .add_criteria("device_target_value", ["HIGH"]).add_criteria("threat_id", ["B0RG"]) \
        .add_criteria("workflow_status", ["OPEN"]).sort_by("name", "DESC")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.status == "OPEN"


def test_query_alert_with_backend_timestamp_as_start_end(cbcsdk_mock):
    """Test an alert query with the backend_timestamp specified as a start and end time."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"backend_timestamp": {"start": "2019-09-30T12:34:56.000000Z",
                                                           "end": "2019-10-01T12:00:12.000000Z"}}}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").add_time_criteria("backend_timestamp", start="2019-09-30T12:34:56",
                                                               end="2019-10-01T12:00:12")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.status == "OPEN"


def test_query_alert_with_backend_timestamp_as_start_end_as_objs(cbcsdk_mock):
    """Test an alert query with the backend_timestamp specified as a start and end time."""
    _timestamp = datetime.now()

    def on_post(url, body, **kwargs):
        nonlocal _timestamp
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"backend_timestamp": {"start": _timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                                           "end": _timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}}}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").add_time_criteria("backend_timestamp", start=_timestamp,
                                                               end=_timestamp)
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.status == "OPEN"


def test_query_alert_with_backend_timestamp_as_range(cbcsdk_mock):
    """Test an alert query with the creation time specified as a range."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "criteria": {"backend_timestamp": {"range": "-3w"}}, "rows": 2}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").add_time_criteria("backend_timestamp", range="-3w")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.status == "OPEN"


def test_query_alert_with_backend_update_timestamp_as_start_end(cbcsdk_mock):
    """Test an alert query with the backend_update_timestamp specified as a range."""
    _timestamp = datetime.now()

    def on_post(url, body, **kwargs):
        nonlocal _timestamp
        assert body == {"query": "Blort", "criteria": {"backend_update_timestamp": {
            "start": _timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "end": _timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}},
            "rows": 2}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").add_time_criteria("backend_update_timestamp", start=_timestamp,
                                                               end=_timestamp)
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.status == "OPEN"


def test_query_alert_with_backend_update_timestamp_as_range(cbcsdk_mock):
    """Test an alert query with the backend_update_timestamp specified as a range."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "criteria": {"backend_update_timestamp": {"range": "-3w"}}, "rows": 2}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api
    query = api.select(Alert).where("Blort").add_time_criteria("backend_update_timestamp", range="-3w")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.status == "OPEN"


def test_query_alert_with_time_range_as_start_end(cbcsdk_mock):
    """Test an alert query with the time_range specified as a start and end time."""
    _timestamp = datetime.now()

    def on_post(url, body, **kwargs):
        nonlocal _timestamp
        assert body == {"query": "Blort",
                        "rows": 2,
                        "time_range": {"start": _timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                       "end": _timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")},
                        }
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").set_time_range(start=_timestamp, end=_timestamp)
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.status == "OPEN"


def test_query_alert_with_time_range_as_range(cbcsdk_mock):
    """Test an alert query with the time_range specified as a range."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "time_range": {"range": "-3w"}, "rows": 2}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api
    query = api.select(Alert).where("Blort").set_time_range(range="-3w")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.status == "OPEN"


def test_query_alert_facets(cbcsdk_mock):
    """Test an alert facet query."""

    def on_post(url, body, **kwargs):
        assert body["query"] == "Blort"
        t = body["criteria"]
        assert t["minimum_severity"] == 3
        t = body["terms"]
        assert t["rows"] == 0
        assert t["fields"] == ["type"]
        return GET_ALERT_FACET_RESP
    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_facet", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").set_minimum_severity(3)
    f = query.facets(["type"])
    assert f == [{"field": "type", "values": [{"id": 'WATCHLIST', "name": 'WATCHLIST', "total": 1916},
                                              {"id": "CB_ANALYTICS", "name": "CB_ANALYTICS", "total": 41}]}]


def test_query_alert_invalid_backend_timestamp_combinations(cb):
    """Test invalid backend_timestamp combinations being supplied to alert queries."""
    with pytest.raises(ApiError):
        cb.select(Alert).add_time_criteria("backend_timestamp")
    with pytest.raises(ApiError):
        cb.select(Alert).add_time_criteria("backend_timestamp", start="2019-09-30T12:34:56",
                                           end="2019-10-01T12:00:12", range="-3w")
    with pytest.raises(ApiError):
        cb.select(Alert).add_time_criteria("backend_timestamp", start="2019-09-30T12:34:56", range="-3w")
    with pytest.raises(ApiError):
        cb.select(Alert).add_time_criteria("backend_timestamp", end="2019-10-01T12:00:12", range="-3w")


def test_query_cbanalyticsalert_with_all_bells_and_whistles(cbcsdk_mock):
    """Test a CB Analytics alert query with all options selected."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"device_id": ["6023"], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "id": ["S0L0"],
                                     "severity": ["6"], "device_policy_id": ["8675309"],
                                     "device_policy": ["Strict"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "process_reputation": ["SUSPECT_MALWARE"], "device_target_value": ["HIGH"],
                                     "threat_id": ["B0RG"], "type": ["CB_ANALYTICS"], "workflow_status": ["OPEN"],
                                     "device_location": ["ONSITE"],
                                     "policy_applied": ["APPLIED"],
                                     "reason_code": ["ATTACK_VECTOR"], "run_state": ["RAN"], "sensor_action": ["DENY"],
                                     "alert_notes_present": True, "attack_tactic": ["tactic"],
                                     "attack_technique": ["technique"],
                                     "blocked_effective_reputation": ["NOT_LISTED"], "blocked_md5": ["md5_hash"],
                                     "blocked_name": ["tim"],
                                     "blocked_sha256": ["sha256_hash"],
                                     "netconn_remote_ip": ["10.29.99.1"], "netconn_remote_domain": ["example.com"],
                                     "netconn_protocol": ["TCP"], "netconn_remote_port": ["54321"],
                                     "netconn_local_port": ["12345"],
                                     "childproc_cmdline": ["/usr/bin/python"],
                                     "childproc_effective_reputation": ["PUP"],
                                     "childproc_guid": ["12345678"], "childproc_name": ["python"],
                                     "childproc_sha256": ["sha256_child"], "childproc_username": ["steven"],
                                     "parent_cmdline": ["/usr/bin/python"],
                                     "parent_effective_reputation": ["PUP"],
                                     "parent_guid": ["12345678"], "parent_name": ["python"],
                                     "parent_sha256": ["sha256_parent"], "parent_username": ["steven"],
                                     "process_cmdline": ["/usr/bin/python"],
                                     "process_effective_reputation": ["PUP"],
                                     "process_guid": ["12345678"], "process_username": ["steven"],
                                     "process_issuer": ["Microsoft"], "process_publisher": ["Microsoft"]
                                     },
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api
    query = api.select(Alert).where("Blort").add_criteria("device_id", ["6023"]) \
        .add_criteria("device_name", ["HAL"]).add_criteria("device_os", ["LINUX"]) \
        .add_criteria("device_os_version", ["0.1.2"]) \
        .add_criteria("device_username", ["JRN"]).add_criteria("id", ["S0L0"]) \
        .add_criteria("severity", "6").add_criteria("device_policy_id", ["8675309"]) \
        .add_criteria("device_policy", ["Strict"]).add_criteria("process_name", ["IEXPLORE.EXE"]) \
        .add_criteria("process_sha256", ["0123456789ABCDEF0123456789ABCDEF"]) \
        .add_criteria("process_reputation", ["SUSPECT_MALWARE"]) \
        .add_criteria("device_target_value", ["HIGH"]).add_criteria("threat_id", ["B0RG"]) \
        .add_criteria("workflow_status", ["OPEN"]).add_criteria("type", ["CB_ANALYTICS"]) \
        .add_criteria("netconn_remote_ip", ['10.29.99.1']).add_criteria("netconn_remote_domain", ['example.com']) \
        .add_criteria("netconn_protocol", ['TCP']).add_criteria("netconn_local_port", ["12345"]) \
        .add_criteria("netconn_remote_port", ["54321"]) \
        .add_criteria("device_location", ["ONSITE"]) \
        .add_criteria("policy_applied", ["APPLIED"]).add_criteria("reason_code", ["ATTACK_VECTOR"]).add_criteria(
        "run_state", ["RAN"]) \
        .set_alert_notes_present(True).add_criteria("attack_tactic", ["tactic"]).add_criteria(
        "attack_technique", ["technique"]) \
        .add_criteria("blocked_effective_reputation", ["NOT_LISTED"]).add_criteria("blocked_md5",
                                                                                   ["md5_hash"]).add_criteria(
        "blocked_name", ["tim"]) \
        .add_criteria("blocked_sha256", ["sha256_hash"]).add_criteria("childproc_cmdline", ["/usr/bin/python"]) \
        .add_criteria("childproc_effective_reputation", ["PUP"]) \
        .add_criteria("childproc_guid", ["12345678"]).add_criteria("childproc_name", ["python"]).add_criteria(
        "childproc_sha256", ["sha256_child"]) \
        .add_criteria("childproc_username", ["steven"]) \
        .add_criteria("parent_cmdline", ["/usr/bin/python"]).add_criteria("parent_effective_reputation", ["PUP"]) \
        .add_criteria("parent_guid", ["12345678"]).add_criteria("parent_name", ["python"]) \
        .add_criteria("parent_sha256", ["sha256_parent"]) \
        .add_criteria("parent_username", ["steven"]) \
        .add_criteria("process_cmdline", ["/usr/bin/python"]).add_criteria("process_effective_reputation", ["PUP"]) \
        .add_criteria("process_guid", ["12345678"]).add_criteria("process_issuer", ["Microsoft"]).add_criteria(
        "process_publisher", ["Microsoft"]) \
        .add_criteria("process_username", ["steven"]) \
        .add_criteria("sensor_action", ["DENY"]).sort_by("name", "DESC")

    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_devicecontrolalert_with_all_bells_and_whistles(cbcsdk_mock):
    """Test a device control alert query with all options selected."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"device_id": ["626"], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "id": ["S0L0"],
                                     "severity": ["6"], "device_policy_id": ["8675309"],
                                     "device_policy": ["Strict"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "process_reputation": ["SUSPECT_MALWARE"], "device_target_value": ["HIGH"],
                                     "threat_id": ["B0RG"], "type": ["DEVICE_CONTROL"], "workflow_status": ["OPEN"],
                                     "external_device_friendly_name": ["/dev/ice"],
                                     "product_id": ["0x5581"], "product_name": ["Ultra"],
                                     "serial_number": ["4C531001331122115172"], "vendor_id": ["0x0781"],
                                     "vendor_name": ["SanDisk"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").add_criteria("device_id", ["6023"]) \
        .add_criteria("device_name", ["HAL"]).add_criteria("device_os", ["LINUX"]) \
        .add_criteria("device_os_version", ["0.1.2"]) \
        .add_criteria("device_username", ["JRN"]).add_criteria("id", ["S0L0"]) \
        .add_criteria("severity", "6").add_criteria("type", ["DEVICE_CONTROL"]).add_criteria("device_policy_id",
                                                                                             ["8675309"]) \
        .add_criteria("device_policy", ["Strict"]).add_criteria("process_name", ["IEXPLORE.EXE"]) \
        .add_criteria("process_sha256", ["0123456789ABCDEF0123456789ABCDEF"]) \
        .add_criteria("process_reputation", ["SUSPECT_MALWARE"]) \
        .add_criteria("external_device_friendly_name", ["/dev/ice"]).add_criteria("product_id", ["0x5581"]) \
        .add_criteria("product_name", ["Ultra"]).add_criteria("serial_number", ["4C531001331122115172"]) \
        .add_criteria("vendor_id", ["0x0781"]).add_criteria("vendor_name", ["SanDisk"]) \
        .add_criteria("device_target_value", ["HIGH"]).add_criteria("threat_id", ["B0RG"]) \
        .add_criteria("workflow_status", ["OPEN"]).sort_by("name", "DESC") \
        .add_criteria("device_id", ["626"]) \
        .sort_by("name", "DESC")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_watchlistalert_with_all_bells_and_whistles(cbcsdk_mock):
    """Test a watchlist alert query with all options selected."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"device_id": ["6023"], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "id": ["S0L0"],
                                     "severity": ["6"], "device_policy_id": ["8675309"],
                                     "device_policy": ["Strict"],
                                     "device_target_value": ["HIGH"],
                                     "watchlists_id": ["100"], "watchlists_name": ["Gandalf"],
                                     "threat_id": ["B0RG"], "type": ["WATCHLIST"], "workflow_status": ["OPEN"],
                                     "netconn_remote_ip": ["10.29.99.1"], "netconn_remote_domain": ["example.com"],
                                     "netconn_protocol": ["TCP"], "netconn_remote_port": ["54321"],
                                     "netconn_local_port": ["12345"],
                                     "childproc_cmdline": ["/usr/bin/python"],
                                     "childproc_effective_reputation": ["PUP"],
                                     "childproc_guid": ["12345678"], "childproc_name": ["python"],
                                     "childproc_sha256": ["sha256_child"], "childproc_username": ["steven"],
                                     "parent_cmdline": ["/usr/bin/python"],
                                     "parent_effective_reputation": ["PUP"],
                                     "parent_guid": ["12345678"], "parent_name": ["python"],
                                     "parent_sha256": ["sha256_parent"], "parent_username": ["steven"],
                                     "process_cmdline": ["/usr/bin/python"],
                                     "process_effective_reputation": ["PUP"],
                                     "process_guid": ["12345678"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "process_username": ["steven"],
                                     "process_reputation": ["SUSPECT_MALWARE"],
                                     "process_issuer": ["Microsoft"], "process_publisher": ["Microsoft"],
                                     "reason_code": ["XDF"],
                                     "report_id": [""], "report_link": [""], "report_name": ["FinalReport"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").add_criteria("type", ["WATCHLIST"]).add_criteria("device_id", ["6023"]) \
        .add_criteria("device_name", ["HAL"]).add_criteria("device_os", ["LINUX"]) \
        .add_criteria("device_os_version", ["0.1.2"]) \
        .add_criteria("device_username", ["JRN"]).add_criteria("id", ["S0L0"]) \
        .add_criteria("severity", "6").add_criteria("device_policy_id", ["8675309"]) \
        .add_criteria("device_policy", ["Strict"]).add_criteria("process_name", ["IEXPLORE.EXE"]) \
        .add_criteria("process_sha256", ["0123456789ABCDEF0123456789ABCDEF"]) \
        .add_criteria("process_reputation", ["SUSPECT_MALWARE"]) \
        .add_criteria("netconn_remote_ip", ['10.29.99.1']).add_criteria("netconn_remote_domain", ['example.com']) \
        .add_criteria("netconn_protocol", ['TCP']).add_criteria("netconn_local_port", ["12345"]) \
        .add_criteria("netconn_remote_port", ["54321"]) \
        .add_criteria("device_target_value", ["HIGH"]).add_criteria("threat_id", ["B0RG"]) \
        .add_criteria("workflow_status", ["OPEN"]).add_criteria("watchlists_id", ["100"]).add_criteria(
        "watchlists_name", ["Gandalf"]) \
        .add_criteria("childproc_cmdline", ["/usr/bin/python"]) \
        .add_criteria("childproc_effective_reputation", ["PUP"]) \
        .add_criteria("childproc_guid", ["12345678"]).add_criteria("childproc_name", ["python"]).add_criteria(
        "childproc_sha256", ["sha256_child"]) \
        .add_criteria("childproc_username", ["steven"]) \
        .add_criteria("parent_cmdline", ["/usr/bin/python"]).add_criteria("parent_effective_reputation", ["PUP"]) \
        .add_criteria("parent_guid", ["12345678"]).add_criteria("parent_name", ["python"]) \
        .add_criteria("parent_sha256", ["sha256_parent"]) \
        .add_criteria("parent_username", ["steven"]) \
        .add_criteria("process_cmdline", ["/usr/bin/python"]).add_criteria("process_effective_reputation", ["PUP"]) \
        .add_criteria("process_guid", ["12345678"]).add_criteria("process_issuer", ["Microsoft"]).add_criteria(
        "process_publisher", ["Microsoft"]) \
        .add_criteria("reason_code", ["XDF"]).add_criteria("report_id", [""]).add_criteria("report_link",
                                                                                           [""]).add_criteria(
        "report_name", ["FinalReport"]) \
        .add_criteria("process_username", ["steven"]) \
        .sort_by("name", "DESC")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.status == "OPEN"


def test_query_intrusion_detection_system_with_all_bells_and_whistles(cbcsdk_mock):
    """Test a IDS alert query with all options selected."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"device_id": ["6023"], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"],
                                     "device_internal_ip": ["10.10.8.2"], "device_external_ip": ["10.10.10.55"],
                                     "id": ["S0L0"],
                                     "severity": ["6"], "device_policy_id": ["8675309"],
                                     "device_policy": ["Strict"], "device_uem_id": ["uemId"],
                                     "device_target_value": ["HIGH"], "threat_name": ["dangerous"],
                                     "threat_id": ["B0RG"], "type": ["INTRUSION_DETECTION_SYSTEM"],
                                     "policy_applied": ["APPLIED"],
                                     "reason_code": ["ATTACK_VECTOR"], "run_state": ["RAN"], "sensor_action": ["DENY"],
                                     "alert_notes_present": True, "attack_tactic": ["tactic"],
                                     "attack_technique": ["technique"], "blocked_effective_reputation": ["NOT_LISTED"],
                                     "blocked_md5": ["md5_hash"], "blocked_name": ["tim"],
                                     "blocked_sha256": ["sha256_hash"],
                                     "ttps": ["malicious"], "tms_rule_id": ["xtvr"],
                                     "workflow_status": ["OPEN"],
                                     "netconn_remote_ip": ["10.29.99.1"], "netconn_remote_domain": ["example.com"],
                                     "netconn_protocol": ["TCP"], "netconn_remote_port": ["54321"],
                                     "netconn_local_port": ["12345"],
                                     "childproc_cmdline": ["/usr/bin/python"],
                                     "childproc_effective_reputation": ["PUP"],
                                     "childproc_guid": ["12345678"], "childproc_name": ["python"],
                                     "childproc_sha256": ["sha256_child"], "childproc_username": ["steven"],
                                     "primary_event_id": ["123456"],
                                     "parent_cmdline": ["/usr/bin/python"],
                                     "parent_effective_reputation": ["PUP"],
                                     "parent_guid": ["12345678"], "parent_name": ["python"],
                                     "parent_sha256": ["sha256_parent"], "parent_username": ["steven"],
                                     "process_cmdline": ["/usr/bin/python"],
                                     "process_effective_reputation": ["PUP"],
                                     "process_guid": ["12345678"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "process_username": ["steven"],
                                     "process_reputation": ["SUSPECT_MALWARE"],
                                     "process_issuer": ["Microsoft"], "process_publisher": ["Microsoft"]},
                        "sort": [{"field": "severity", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").add_criteria("type", ["INTRUSION_DETECTION_SYSTEM"])\
        .add_criteria("device_id", ["6023"]) \
        .add_criteria("device_name", ["HAL"]).add_criteria("device_os", ["LINUX"]) \
        .add_criteria("device_os_version", ["0.1.2"]).add_criteria("device_internal_ip", ["10.10.8.2"]) \
        .add_criteria("device_username", ["JRN"]).add_criteria("id", ["S0L0"])\
        .add_criteria("device_external_ip", ["10.10.10.55"]).add_criteria("device_uem_id", ["uemId"]) \
        .add_criteria("severity", "6").add_criteria("device_policy_id", ["8675309"]) \
        .add_criteria("device_policy", ["Strict"]).add_criteria("process_name", ["IEXPLORE.EXE"]) \
        .add_criteria("process_sha256", ["0123456789ABCDEF0123456789ABCDEF"]) \
        .add_criteria("process_reputation", ["SUSPECT_MALWARE"]) \
        .add_criteria("netconn_remote_ip", ['10.29.99.1']).add_criteria("netconn_remote_domain", ['example.com']) \
        .add_criteria("netconn_protocol", ['TCP']).add_criteria("netconn_local_port", ["12345"]) \
        .add_criteria("netconn_remote_port", ["54321"]) \
        .add_criteria("policy_applied", ["APPLIED"]).add_criteria("reason_code", ["ATTACK_VECTOR"]).add_criteria(
        "run_state", ["RAN"]) \
        .add_criteria("device_target_value", ["HIGH"]).add_criteria("threat_id", ["B0RG"]) \
        .add_criteria("threat_name", ["dangerous"]).set_alert_notes_present(True) \
        .add_criteria("attack_tactic", ["tactic"]).add_criteria("attack_technique", ["technique"]) \
        .add_criteria("workflow_status", ["OPEN"]).add_criteria("blocked_effective_reputation", ["NOT_LISTED"]).\
        add_criteria("blocked_md5", ["md5_hash"]).add_criteria("blocked_name", ["tim"]) \
        .add_criteria("blocked_sha256", ["sha256_hash"]) \
        .add_criteria("childproc_cmdline", ["/usr/bin/python"]).add_criteria("primary_event_id", ["123456"]) \
        .add_criteria("childproc_effective_reputation", ["PUP"]) \
        .add_criteria("childproc_guid", ["12345678"]).add_criteria("childproc_name", ["python"]).add_criteria(
        "childproc_sha256", ["sha256_child"]) \
        .add_criteria("childproc_username", ["steven"]) \
        .add_criteria("parent_cmdline", ["/usr/bin/python"]).add_criteria("parent_effective_reputation", ["PUP"]) \
        .add_criteria("parent_guid", ["12345678"]).add_criteria("parent_name", ["python"]) \
        .add_criteria("parent_sha256", ["sha256_parent"]) \
        .add_criteria("parent_username", ["steven"]) \
        .add_criteria("process_cmdline", ["/usr/bin/python"]).add_criteria("process_effective_reputation", ["PUP"]) \
        .add_criteria("process_guid", ["12345678"]).add_criteria("process_issuer", ["Microsoft"]).add_criteria(
        "process_publisher", ["Microsoft"]) \
        .add_criteria("reason_code", ["ATTACK_VECTOR"]).add_criteria("sensor_action", ["DENY"])\
        .add_criteria("process_username", ["steven"]) \
        .add_criteria("ttps", ["malicious"]).add_criteria("tms_rule_id", ["xtvr"]) \
        .sort_by("severity", "DESC")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.status == "OPEN"


def test_query_containeralert_with_all_bells_and_whistles(cbcsdk_mock):
    """Test a container alert query with all options selected."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"k8s_cluster": ["TURTLE"], 'type': ['CONTAINER_RUNTIME'], "k8s_namespace": ["RG"],
                                     "k8s_workload_kind": ["Job"], "k8s_policy": [""], "k8s_policy_id": [""],
                                     "k8s_workload_name": ["BUNNY"], "k8s_pod_name": ["FAKE"],
                                     "netconn_remote_ip": ["10.29.99.1"], "netconn_remote_domain": ["example.com"],
                                     "netconn_protocol": ["TCP"],
                                     "netconn_remote_port": ["54321"], "netconn_local_port": ["12345"],
                                     "egress_group_id": ["5150"], "egress_group_name": ["EGRET"],
                                     "ip_reputation": ["75"], "k8s_rule_id": ["66"], "k8s_rule": ["KITTEH"],
                                     "remote_k8s_kind": [""], "remote_k8s_namespace": [""], "remote_k8s_pod_name": [""],
                                     "remote_k8s_workload_name": [""]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(ContainerRuntimeAlert).where("Blort").add_criteria("k8s_cluster", ['TURTLE']) \
        .add_criteria("k8s_namespace", ['RG']).add_criteria("k8s_rule_id", ['66']) \
        .add_criteria("k8s_rule", ['KITTEH']) \
        .add_criteria("k8s_policy_id", ['']).add_criteria("k8s_policy", ['']).add_criteria("k8s_pod_name", ['FAKE']) \
        .add_criteria("k8s_workload_kind", ['Job']).add_criteria("k8s_workload_name", ['BUNNY']) \
        .add_criteria("netconn_remote_ip", ['10.29.99.1']).add_criteria("netconn_remote_domain", ['example.com']) \
        .add_criteria("netconn_protocol", ['TCP']).add_criteria("netconn_local_port", ["12345"]).add_criteria(
        "netconn_remote_port", ["54321"]) \
        .add_criteria("remote_k8s_namespace", [""]).add_criteria("remote_k8s_pod_name", [""]).add_criteria(
        "remote_k8s_kind", [""]) \
        .add_criteria("remote_k8s_workload_name", [""]) \
        .add_criteria("egress_group_id", ['5150']).add_criteria("egress_group_name", ['EGRET']) \
        .add_criteria("ip_reputation", ["75"]).sort_by("name", "DESC")

    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.status == "OPEN"


def test_query_set_rows(cbcsdk_mock):
    """Test alert query with set rows."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 10000,
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").sort_by("name", "DESC").set_rows(10000)
    for a in query:
        assert a.id == "S0L0"
        assert a.org_key == "test"
        assert a.threat_id == "B0RG"


# TODO Alerts workflow tests


def test_get_process(cbcsdk_mock):
    """Test of getting process through a WatchlistAlert"""
    def on_validation_post(url, body, **kwargs):
        assert body == {"query": "process_guid:ABC12345\\-000309c2\\-00000478\\-00000000\\-1d6a1c1f2b02805"}
        return POST_PROCESS_VALIDATION_RESP
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/887e6bbc-6224-4f36-ad37-084038b7fcab",
                             GET_ALERT_TYPE_WATCHLIST)
    # mock the search validation
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_validation", on_validation_post)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=0"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=500"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_WATCHLIST_ALERT_V7)
    api = cbcsdk_mock.api
    alert = api.select(WatchlistAlert, "887e6bbc-6224-4f36-ad37-084038b7fcab")
    process = alert.get_process()
    assert isinstance(process, Process)
    assert process.process_guid == "ABC12345-0002b226-000015bd-00000000-1d6225bbba74c00"


def test_get_process_zero_found(cbcsdk_mock):
    """Test of getting process through a WatchlistAlert"""
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_TYPE_WATCHLIST)

    def on_validation_post(url, body, **kwargs):
        assert body == {"query": "process_guid:ABC12345\\-000309c2\\-00000478\\-00000000\\-1d6a1c1f2b02805"}
        return POST_PROCESS_VALIDATION_RESP
    # mock the search validation
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_validation", on_validation_post)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get process search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=0"),
                             GET_PROCESS_NOT_FOUND)
    # mock the GET to get process search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=500"),
                             GET_PROCESS_NOT_FOUND)
    api = cbcsdk_mock.api
    alert = api.select(WatchlistAlert, "86123310980efd0b38111eba4bfa5e98aa30b19")
    process = alert.get_process()
    assert not process


def test_get_process_raises_api_error(cbcsdk_mock):
    """Test of getting process through a WatchlistAlert"""
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/887e6bbc-6224-4f36-ad37-084038b7fcab",
                             GET_ALERT_TYPE_WATCHLIST_INVALID)
    # mock the search validation
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_validation",
                             POST_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=0"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=500"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP)
    api = cbcsdk_mock.api
    with pytest.raises(ApiError):
        alert = api.select(WatchlistAlert, "887e6bbc-6224-4f36-ad37-084038b7fcab")
        alert.get_process()


def test_get_process_async(cbcsdk_mock):
    """Test of getting process through a WatchlistAlert async"""
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/887e6bbc-6224-4f36-ad37-084038b7fcab",
                             GET_ALERT_TYPE_WATCHLIST)
    # mock the search validation
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_validation",
                             POST_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=0"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=500"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_WATCHLIST_ALERT_V7)
    # mock the POST of a summary search (using same Job ID)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/summary_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get summary search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SUMMARY_STR)
    api = cbcsdk_mock.api
    alert = api.select(WatchlistAlert, "887e6bbc-6224-4f36-ad37-084038b7fcab")
    process = alert.get_process(async_mode=True).result()
    assert isinstance(process, Process)
    assert process.process_guid == "ABC12345-0002b226-000015bd-00000000-1d6225bbba74c00"


# TODO  enriched_event tests to be replaced with observations tests


def test_query_alert_with_time_range_errors(cbcsdk_mock):
    """Test exceptions in alert query"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError) as ex:
        api.select(Alert).where("Blort").add_time_criteria("invalid", range="whatever")
    assert "key must be one of backend_timestamp, backend_update_timestamp, detection_timestamp, " \
           "first_event_timestamp, last_event_timestamp, mdr_determination_change_timestamp, " \
           "mdr_workflow_change_timestamp, user_update_timestamp, or workflow_change_timestamp" in str(ex.value)

    with pytest.raises(ApiError) as ex:
        api.select(Alert).where("Blort").add_time_criteria("backend_timestamp",
                                                           start="2019-09-30T12:34:56",
                                                           end="2019-10-01T12:00:12",
                                                           range="-3w")
    assert "cannot specify range= in addition to start= and end=" in str(ex.value)

    with pytest.raises(ApiError) as ex:
        api.select(Alert).where("Blort").add_time_criteria("backend_timestamp",
                                                           end="2019-10-01T12:00:12",
                                                           range="-3w")
    assert "cannot specify start= or end= in addition to range=" in str(ex.value)

    with pytest.raises(ApiError) as ex:
        api.select(Alert).where("Blort").add_time_criteria("backend_timestamp")

    assert "must specify either start= and end= or range=" in str(ex.value)


def test_query_alert_sort_error(cbcsdk_mock):
    """Test an alert query with the invalid sort direction"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError) as ex:
        api.select(Alert).where("Blort").sort_by("backend_timestamp", "bla")
    assert "invalid sort direction specified" in str(ex.value)


def test_query_alert_facets_functionality_decommissioned_error(cbcsdk_mock):
    """Test an alert facet query with invalid term."""
    cbcsdk_mock.mock_request('POST',
                             "/api/alerts/v7/orgs/test/alerts/_facet",
                             GET_ALERT_FACET_RESP_INVALID)

    api = cbcsdk_mock.api
    query = api.select(Alert).where("Blort").set_workflows(["OPEN"])
    with pytest.raises(FunctionalityDecommissioned) as ex:
        query.facets(["ALABALA", "STATUS"])
    assert "The Field 'STATUS' does is not a valid facet name because it was deprecated in Alerts v7. functionality " \
           "has been decommissioned." in str(ex.value)


def test_query_alert_facets_api_error(cbcsdk_mock):
    """Test an alert facet query with invalid term."""
    cbcsdk_mock.mock_request('POST',
                             "/api/alerts/v7/orgs/test/alerts/_facet",
                             GET_ALERT_FACET_RESP_INVALID)
    cbcsdk_mock.mocks['POST:/api/alerts/v7/orgs/test/alerts/_facet'].__setattr__("status_code", 400)
    api = cbcsdk_mock.api
    query = api.select(Alert).where("Blort").set_workflows(["OPEN"])
    with pytest.raises(ApiError) as ex:
        query.facets(["jager"])
    assert "'error_code': 'INVALID_ENUM_VALUE'" in str(ex.value)


def test_get_notes_for_alert(cbcsdk_mock):
    """Test retrieving notes for an alert"""
    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81/notes",
                             GET_ALERT_NOTES)

    api = cbcsdk_mock.api
    alert = api.select(Alert, "52dbd1b6-539b-a3f7-34bd-f6eb13a99b81")
    notes = alert.notes_()
    assert len(notes) == 2
    assert notes[0].author == "Grogu"
    assert notes[0].id == "3gsgsfds"
    assert notes[0].create_timestamp == "2023-04-18T03:25:44.397Z"
    assert notes[0].last_update_timestamp == "2023-04-18T03:25:44.397Z"
    assert notes[0].note == "I am Grogu"
    assert notes[0].source == "CUSTOMER"


def test_base_alert_create_note(cbcsdk_mock):
    """Test creating a new note on an alert"""

    def on_post(url, body, **kwargs):
        body == {"note": "I am Grogu"}
        return CREATE_ALERT_NOTE_RESP

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('POST',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81/notes",
                             on_post)

    api = cbcsdk_mock.api
    alert = api.select(Alert, "52dbd1b6-539b-a3f7-34bd-f6eb13a99b81")
    note = alert.create_note("I am Grogu")
    assert note.note == "I am Grogu"


def test_base_alert_delete_note(cbcsdk_mock):
    """Test deleting a note from an alert"""
    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81/notes",
                             GET_ALERT_NOTES)

    cbcsdk_mock.mock_request('DELETE',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81/notes/3gsgsfds",
                             None)

    api = cbcsdk_mock.api
    alert = api.select(Alert, "52dbd1b6-539b-a3f7-34bd-f6eb13a99b81")
    notes = alert.notes_()
    notes[0].delete()
    assert notes[0]._is_deleted


def test_base_alert_unsupported_query_notes(cbcsdk_mock):
    """Testing that error is thrown when querying notes directly"""
    with pytest.raises(NonQueryableModel):
        api = cbcsdk_mock.api
        api.select(Alert.Note)


def test_base_alert_refresh_note(cbcsdk_mock):
    """Testing single note refresh"""
    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81/notes",
                             GET_ALERT_NOTES)

    api = cbcsdk_mock.api
    alert = api.select(Alert, "52dbd1b6-539b-a3f7-34bd-f6eb13a99b81")
    notes = alert.notes_()
    assert notes[0]._refresh() is True


def test_get_threat_notes_for_alert(cbcsdk_mock):
    """Test retrieving threat notes for an alert"""
    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/threats/"
                             "78de82d612a7d3d4a6caffa4ce7e7bb718e23d926dcd9a5047f6e9f129279d44/notes",
                             GET_ALERT_NOTES)

    api = cbcsdk_mock.api
    alert = api.select(Alert, "52dbd1b6-539b-a3f7-34bd-f6eb13a99b81")
    notes = alert.notes_(threat_note=True)
    assert len(notes) == 2
    assert notes[0].author == "Grogu"
    assert notes[0].id == "3gsgsfds"
    assert notes[0].create_timestamp == "2023-04-18T03:25:44.397Z"
    assert notes[0].last_update_timestamp == "2023-04-18T03:25:44.397Z"
    assert notes[0].note == "I am Grogu"
    assert notes[0].source == "CUSTOMER"


def test_base_alert_create_threat_note(cbcsdk_mock):
    """Test creating a new threat note on an alert"""

    def on_post(url, body, **kwargs):
        body == {"note": "I am Grogu"}
        return CREATE_ALERT_NOTE_RESP

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('POST',
                             "/api/alerts/v7/orgs/test/threats/"
                             "78de82d612a7d3d4a6caffa4ce7e7bb718e23d926dcd9a5047f6e9f129279d44/notes",
                             on_post)

    api = cbcsdk_mock.api
    alert = api.select(Alert, "52dbd1b6-539b-a3f7-34bd-f6eb13a99b81")
    note = alert.create_note("I am Grogu", threat_note=True)
    assert note.note == "I am Grogu"


def test_base_alert_delete_threat_note(cbcsdk_mock):
    """Test deleting a note from an alert"""
    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/threats/"
                             "78de82d612a7d3d4a6caffa4ce7e7bb718e23d926dcd9a5047f6e9f129279d44/notes",
                             GET_ALERT_NOTES)

    cbcsdk_mock.mock_request('DELETE',
                             "/api/alerts/v7/orgs/test/threats/"
                             "78de82d612a7d3d4a6caffa4ce7e7bb718e23d926dcd9a5047f6e9f129279d44/notes/3gsgsfds",
                             None)

    api = cbcsdk_mock.api
    alert = api.select(Alert, "52dbd1b6-539b-a3f7-34bd-f6eb13a99b81")
    notes = alert.notes_(threat_note=True)
    notes[0].delete()
    assert notes[0]._is_deleted


def test_base_alert_refresh_threat_note(cbcsdk_mock):
    """Testing single note refresh"""
    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/52dbd1b6-539b-a3f7-34bd-f6eb13a99b81",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/threats/"
                             "78de82d612a7d3d4a6caffa4ce7e7bb718e23d926dcd9a5047f6e9f129279d44/notes",
                             GET_ALERT_NOTES)

    api = cbcsdk_mock.api
    alert = api.select(Alert, "52dbd1b6-539b-a3f7-34bd-f6eb13a99b81")
    notes = alert.notes_(threat_note=True)
    assert notes[0]._refresh() is True


def test_alert_search_suggestions(cbcsdk_mock):
    """Tests getting alert search suggestions"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/api/alerts/v7/orgs/test/alerts/search_suggestions?suggest.q=",
        ALERT_SEARCH_SUGGESTIONS_RESP,
    )
    result = Alert.search_suggestions(api, "")
    assert len(result) == 20


def test_alert_search_suggestions_api_error():
    """Tests getting alert search suggestions - no CBCloudAPI arg"""
    with pytest.raises(ApiError):
        Alert.search_suggestions("", "")


def test_query_set_minimum_severity(cbcsdk_mock):
    """Test a search setting minimum severity."""

    def on_post(url, body, **kwargs):
        assert body == {
            "criteria": {
                "minimum_severity": 3
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).set_minimum_severity(3).set_rows(1)
    len(query)
    # no assertions, the check is that the post request is formed correctly.


def test_query_set_threat_notes_present(cbcsdk_mock):
    """Test a search setting whether threat notes are present or not."""

    def on_post(url, body, **kwargs):
        assert body == {
            "criteria": {
                "threat_notes_present": False
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).set_threat_notes_present(False).set_rows(1)
    len(query)
    # no assertions, the check is that the post request is formed correctly.


def test_query_set_alert_notes_present(cbcsdk_mock):
    """Test a search setting whether alert notes are present or not."""

    def on_post(url, body, **kwargs):
        assert body == {
            "criteria": {
                "alert_notes_present": False
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).set_alert_notes_present(False).set_rows(1)
    len(query)
    # no assertions, the check is that the post request is formed correctly.


def test_query_set_remote_is_private(cbcsdk_mock):
    """Test a search setting whether remote_is_private is true or false."""

    def on_post(url, body, **kwargs):
        assert body == {
            "criteria": {
                "remote_is_private": True
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).set_remote_is_private(True).set_rows(1)
    len(query)
    # no assertions, the check is that the post request is formed correctly.


def test_get_observations(cbcsdk_mock):
    """Test get_observations method."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/12ab345cd6-e2d1-4118-8a8d-04f521ae66aa",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",
        # noqa: E501
        GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    alert = api.select(Alert, '12ab345cd6-e2d1-4118-8a8d-04f521ae66aa')
    obs = alert.get_observations()
    assert len(obs) == 1


def test_get_observations_invalid(cbcsdk_mock):
    """Test get_observations method with invalid alert id."""
    def on_post(url, body, **kwargs):
        return {"results": [{"id": "", "org_key": "invalid_alert"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api
    alert_list = api.select(Alert)
    alert = alert_list.first()
    with pytest.raises(ApiError):
        alert.get_observations()


def test_get_observations_with_timeout(cbcsdk_mock):
    """Test get_observations method."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING
    )

    api = cbcsdk_mock.api
    alert = api.select(Alert, '86123310980efd0b38111eba4bfa5e98aa30b19')
    with pytest.raises(TimeoutError):
        alert.get_observations(timeout=1)
        print("the end")


def test_alert_subtype_alert_class(cbcsdk_mock):
    """Test Alert class instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select(Alert, '6f1173f5-f921-8e11-2160-edf42b799333')
    assert isinstance(alert, Alert)


def test_alert_subtype_alert_string_class(cbcsdk_mock):
    """Test Alert class using string instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select('Alert', '6f1173f5-f921-8e11-2160-edf42b799333')
    assert isinstance(alert, Alert)


def test_alert_subtype_basealert_class(cbcsdk_mock):
    """Test BaseAlert class instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select(BaseAlert, '6f1173f5-f921-8e11-2160-edf42b799333')
    assert isinstance(alert, BaseAlert)


def test_alert_subtype_basealert_string_class(cbcsdk_mock):
    """Test BaseAlert class using string instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select('BaseAlert', '6f1173f5-f921-8e11-2160-edf42b799333')
    assert isinstance(alert, BaseAlert)


def test_alert_subtype_cbanalyticsalert_class(cbcsdk_mock):
    """Test CBAnalyticsAlert class instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select(CBAnalyticsAlert, '6f1173f5-f921-8e11-2160-edf42b799333')
    assert isinstance(alert, CBAnalyticsAlert)


def test_alert_subtype_cbanalyticsalert_string_class(cbcsdk_mock):
    """Test CBAnalyticsAlert class using string instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select('CBAnalyticsAlert', '6f1173f5-f921-8e11-2160-edf42b799333')
    assert isinstance(alert, CBAnalyticsAlert)


def test_alert_subtype_watchlistalert_class(cbcsdk_mock):
    """Test WatchlistAlert class instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/f6af290d-6a7f-461c-a8af-cf0d24311105",
                             GET_ALERT_v7_WATCHLIST_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select(WatchlistAlert, 'f6af290d-6a7f-461c-a8af-cf0d24311105')
    assert isinstance(alert, WatchlistAlert)


def test_alert_subtype_watchlistalert_string_class(cbcsdk_mock):
    """Test WatchlistAlert class as string instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/f6af290d-6a7f-461c-a8af-cf0d24311105",
                             GET_ALERT_v7_WATCHLIST_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select('WatchlistAlert', 'f6af290d-6a7f-461c-a8af-cf0d24311105')
    assert isinstance(alert, WatchlistAlert)


def test_alert_subtype_devicecontrolalert_class(cbcsdk_mock):
    """Test DeviceControlAlert class instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/b6a7e48b-1d14-11ee-a9e0-888888888788",
                             GET_ALERT_v7_DEVICE_CONTROL_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select(DeviceControlAlert, 'b6a7e48b-1d14-11ee-a9e0-888888888788')
    assert isinstance(alert, DeviceControlAlert)


def test_alert_subtype_devicecontrolalert_string_class(cbcsdk_mock):
    """Test DeviceControlAlert class as string instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/b6a7e48b-1d14-11ee-a9e0-888888888788",
                             GET_ALERT_v7_DEVICE_CONTROL_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select('DeviceControlAlert', 'b6a7e48b-1d14-11ee-a9e0-888888888788')
    assert isinstance(alert, DeviceControlAlert)


def test_alert_subtype_hostbasedfirewallalert_class(cbcsdk_mock):
    """Test HostBasedFirewallAlert class instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/2be0652f-20bc-3311-9ded-8b873e28d830",
                             GET_ALERT_v7_HBFW_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select(HostBasedFirewallAlert, '2be0652f-20bc-3311-9ded-8b873e28d830')
    assert isinstance(alert, HostBasedFirewallAlert)


def test_alert_subtype_hostbasedfirewallalert_string_class(cbcsdk_mock):
    """Test HostBasedFirewallAlert class as string instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/2be0652f-20bc-3311-9ded-8b873e28d830",
                             GET_ALERT_v7_HBFW_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select('HostBasedFirewallAlert', '2be0652f-20bc-3311-9ded-8b873e28d830')
    assert isinstance(alert, HostBasedFirewallAlert)


def test_alert_subtype_containerruntimealert_class(cbcsdk_mock):
    """Test ContainerRuntimeAlert class instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/46b419c8-3d67-ead8-dbf1-9d8417610fac",
                             GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select(ContainerRuntimeAlert, '46b419c8-3d67-ead8-dbf1-9d8417610fac')
    assert isinstance(alert, ContainerRuntimeAlert)


def test_alert_subtype_containerruntimealert_string_class(cbcsdk_mock):
    """Test ContainerRuntimeAlert class as string instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/46b419c8-3d67-ead8-dbf1-9d8417610fac",
                             GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select('ContainerRuntimeAlert', '46b419c8-3d67-ead8-dbf1-9d8417610fac')
    assert isinstance(alert, ContainerRuntimeAlert)


def test_alert_subtype_intrusiondetectionsystemalert_class(cbcsdk_mock):
    """Test IntrusionDetectionSystemAlert class instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/ca316d99-a808-3779-8aab-62b2b6d9541c",
                             GET_ALERT_v7_INTRUSION_DETECTION_SYSTEM_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select(IntrusionDetectionSystemAlert, 'ca316d99-a808-3779-8aab-62b2b6d9541c')
    assert isinstance(alert, IntrusionDetectionSystemAlert)


def test_alert_subtype_intrusiondetectionsystemalert_string_class(cbcsdk_mock):
    """Test IntrusionDetectionSystemAlert class as string instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/ca316d99-a808-3779-8aab-62b2b6d9541c",
                             GET_ALERT_v7_INTRUSION_DETECTION_SYSTEM_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select('IntrusionDetectionSystemAlert', 'ca316d99-a808-3779-8aab-62b2b6d9541c')
    assert isinstance(alert, IntrusionDetectionSystemAlert)


def test_alert_subtype_invalid_string_class(cbcsdk_mock):
    """Test invalidAlertType class as string instantiation."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/ca316d99-a808-3779-8aab-62b2b6d9541c",
                             GET_ALERT_v7_INTRUSION_DETECTION_SYSTEM_RESPONSE)
    api = cbcsdk_mock.api
    with (pytest.raises(ModelNotFound)):
        api.select('invalidAlertType', 'ca316d99-a808-3779-8aab-62b2b6d9541c')


def test_new_alert_type(cbcsdk_mock):
    """Test Alert class instantiation with an alert type unknown to CBC SDK."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/MYVERYFIRSTNEWALERTTYPE0001",
                             GET_NEW_ALERT_TYPE_RESP)
    api = cbcsdk_mock.api
    alert = api.select(Alert, 'MYVERYFIRSTNEWALERTTYPE0001')
    assert isinstance(alert, Alert)
    assert alert.id == "MYVERYFIRSTNEWALERTTYPE0001"
    assert alert.type == "FIRST_NEW_TEST_ALERT_TYPE"


def test_new_alert_type_search(cbcsdk_mock):
    """Test Alert class instantiation with an alert type unknown to CBC SDK. Expect success."""
    def on_post(url, body, **kwargs):
        assert body == {
            "criteria": {
                "type": [
                    "FIRST_NEW_TEST_ALERT_TYPE"
                ]
            },
            "rows": 1
        }
        return {"results": [{"org_key": "ABCD1234",
                             "alert_url": "https://defense.conferdeploy.net/alerts?s[c][query_string]="
                                          "id:MYVERYFIRSTNEWALERTTYPE0001&orgKey=ABCD1234",
                             "id": "MYVERYFIRSTNEWALERTTYPE0001",
                             "type": "FIRST_NEW_TEST_ALERT_TYPE",
                             "backend_timestamp": "2023-04-14T21:30:40.570Z",
                             "user_update_timestamp": None}],
                "num_found": 1}
    cbcsdk_mock.mock_request("POST",
                             "/api/alerts/v7/orgs/test/alerts/_search",
                             on_post)
    api = cbcsdk_mock.api
    alert_list = api.select(Alert).add_criteria('type', 'FIRST_NEW_TEST_ALERT_TYPE').set_rows(1)
    assert len(alert_list) == 1
    alert = alert_list.first()
    assert alert.id == "MYVERYFIRSTNEWALERTTYPE0001"
    assert alert.type == "FIRST_NEW_TEST_ALERT_TYPE"


def test_container_alert_v6_field(cbcsdk_mock):
    """Test that when a container specific field is used it is mapped correctly on get()"""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/46b419c8-3d67-ead8-dbf1-9d8417610fac",
                             GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE)
    api = cbcsdk_mock.api
    alert = api.select(Alert, "46b419c8-3d67-ead8-dbf1-9d8417610fac")
    print(alert.get("policy_id"))
    print(alert.get("k8s_policy_id"))
    print(alert.policy_id)
    print(alert.k8s_policy_id)
    assert alert.policy_id == alert.k8s_policy_id


def test_exclusion_single_list(cbcsdk_mock):
    """Test a single exclusion in an array"""
    def on_post(url, body, **kwargs):
        assert body == {
            "exclusions": {
                "type": [
                    "WATCHLIST"
                ]
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "type": "WATCHLIST"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).add_exclusions("type", ["WATCHLIST"]).set_rows(1)
    len(query)
    # no assertions, the check is that the post request is formed correctly.


def test_exclusion_two_list(cbcsdk_mock):
    """Test a single exclusion in an array"""
    def on_post(url, body, **kwargs):
        assert body == {
            "exclusions": {
                "process_effective_reputation": [
                    "TRUSTED_WHITE_LIST"
                ],
                "type": [
                    "WATCHLIST"
                ]
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "type": "WATCHLIST"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).add_exclusions("type", ["WATCHLIST"])\
        .add_exclusions("type", ["WATCHLIST"]) \
        .add_exclusions("process_effective_reputation", ["TRUSTED_WHITE_LIST"]) \
        .set_rows(1)
    len(query)
    # no assertions, the check is that the post request is formed correctly.


def test_exclusion_singleton(cbcsdk_mock):
    """Test a single value exclusion"""
    def on_post(url, body, **kwargs):
        assert body == {
            "exclusions": {
                "alert_notes_present": False
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "type": "WATCHLIST"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).set_alert_notes_present(False, True) \
        .set_rows(1)
    len(query)
    # no assertions, the check is that the post request is formed correctly.


def test_exclusion_list_and_singleton(cbcsdk_mock):
    """Test a single value and list exclusion in an array"""
    def on_post(url, body, **kwargs):
        assert body == {
            "exclusions": {
                "alert_notes_present": True,
                "type": [
                    "CB_ANALYTICS"
                ]
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "type": "WATCHLIST"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).add_exclusions("type", ["CB_ANALYTICS"])\
        .set_alert_notes_present(True, True) \
        .set_rows(1)
    len(query)
    # no assertions, the check is that the post request is formed correctly.


def test_exclusion_remote_is_private(cbcsdk_mock):
    """Test a single value for remote_is_private"""
    def on_post(url, body, **kwargs):
        assert body == {
            "exclusions": {
                "remote_is_private": True
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "type": "WATCHLIST"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).set_remote_is_private(True, True) \
        .set_rows(1)
    len(query)
    # no assertions, the check is that the post request is formed correctly.


def test_exclusion_threat_notes_present(cbcsdk_mock):
    """Test a single value for threat_notes_present"""
    def on_post(url, body, **kwargs):
        assert body == {
            "exclusions": {
                "threat_notes_present": True
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "type": "WATCHLIST"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).set_threat_notes_present(True, True) \
        .set_rows(1)
    len(query)
    # no assertions, the check is that the post request is formed correctly.


def test_add_time_criteria_detection_timestamp(cbcsdk_mock):
    """Test an alert query with the detection timestamp specified as a range."""

    def on_post(url, body, **kwargs):
        assert body == {
            "criteria": {
                "detection_timestamp": {
                    "range": "-2h"
                }
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "type": "CB_ANALYTICS"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api
    alerts = api.select(Alert).add_time_criteria("detection_timestamp", range="-2h").set_rows(1)
    len(alerts)


def test_exclusion_detection_timestamp(cbcsdk_mock):
    """Test a timerange object in exclusions"""
    def on_post(url, body, **kwargs):
        assert body == {
            "exclusions": {
                "detection_timestamp": {
                    "range": "-2h"
                }
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "type": "WATCHLIST"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    alerts = api.select(Alert).add_time_criteria("detection_timestamp", range="-2h", exclude=True).set_rows(1)
    len(alerts)


def test_all_timestamp_positions(cbcsdk_mock):
    """Test a request with time_range, a timestamp in criteria and a timestamp in exclusions"""
    def on_post(url, body, **kwargs):
        assert body == {
            "time_range": {
                "range": "-1m"
            },
            "criteria": {
                "detection_timestamp": {
                    "range": "-2d"
                }
            },
            "exclusions": {
                "backend_update_timestamp": {
                    "range": "-3h"
                }
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "type": "WATCHLIST"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api
    alerts = api.select(Alert).set_time_range(range="-1m"). \
        add_time_criteria("detection_timestamp", range="-2d", exclude=False).\
        add_time_criteria("backend_update_timestamp", range="-3h", exclude=True).\
        set_rows(1)
    len(alerts)


def test_exclusion_invalid_attrib(cbcsdk_mock):
    """Test an invalid exclusion field in an array.  No error, backend ignores"""
    def on_post(url, body, **kwargs):
        assert body == {
            "exclusions": {
                "invalidfield": ["invalidvalue"]
            },
            "rows": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "type": "WATCHLIST"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api
    api.select(Alert).add_exclusions("invalidfield", ["invalidvalue"])


def test_criteria_integer(cbcsdk_mock):
    """Test criteria as an integer"""
    def on_post(url, body, **kwargs):
        assert body == {
            "criteria": {
                "device_id": [
                    12345678
                ]
            },
            "rows": 1
        }
        return {"results": [
            {"id": "S0L0", "org_key": "test", "type": "WATCHLIST", "device_id": 12345678}
        ],
            "num_found": 1
        }
    device_id = 12345678
    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).add_criteria("device_id", device_id).set_rows(1)
    alert = query.first()
    assert alert.device_id == device_id
    assert alert.get("device_id") == device_id


def test_exclusion_integer(cbcsdk_mock):
    """Test an exclusion as an integer"""
    def on_post(url, body, **kwargs):
        assert body == {
            "exclusions": {
                "device_id": [
                    12345678
                ]
            },
            "rows": 1
        }
        return {"results": [
            {"id": "S0L0", "org_key": "test", "type": "WATCHLIST", "device_id": 12345678}
        ],
            "num_found": 1
        }
    device_id = 12345678
    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).add_exclusions("device_id", device_id).set_rows(1)
    alert = query.first()
    assert alert.device_id == device_id
    assert alert.get("device_id") == device_id


def test_alert_history(cbcsdk_mock):
    """Test get_history for alerts"""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)

    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333/history",
                             GET_ALERT_HISTORY)

    api = cbcsdk_mock.api
    alert = api.select(Alert, "6f1173f5-f921-8e11-2160-edf42b799333")
    history = alert.get_history()

    assert history == GET_ALERT_HISTORY["history"]


def test_threat_history(cbcsdk_mock):
    """Test get_history for threats"""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)

    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/threats/"
                             "9e0afc389c1acc43b382b1ba590498d2/history",
                             GET_THREAT_HISTORY)

    api = cbcsdk_mock.api
    alert = api.select(Alert, "6f1173f5-f921-8e11-2160-edf42b799333")

    history = alert.get_history(threat=True)

    assert history == GET_THREAT_HISTORY["history"]


def test_add_threat_tags(cbcsdk_mock):
    """Test add_threat_tags"""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)

    tags = ["tag1", "tag2"]

    cbcsdk_mock.mock_request("POST",
                             "/api/alerts/v7/orgs/test/threats/"
                             "9e0afc389c1acc43b382b1ba590498d2/tags",
                             {"tags": tags})

    api = cbcsdk_mock.api
    alert = api.select(Alert, "6f1173f5-f921-8e11-2160-edf42b799333")

    assert tags == alert.add_threat_tags(tags)


def test_add_threat_tags_error(cbcsdk_mock):
    """Test add_threat_tags raises ApiError"""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)

    api = cbcsdk_mock.api
    alert = api.select(Alert, "6f1173f5-f921-8e11-2160-edf42b799333")

    with pytest.raises(ApiError):
        alert.add_threat_tags(5)


def test_get_threat_tags(cbcsdk_mock):
    """Test get_threat_tags"""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)

    tags = ["tag1", "tag2"]

    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/threats/"
                             "9e0afc389c1acc43b382b1ba590498d2/tags",
                             {"list": tags})

    api = cbcsdk_mock.api
    alert = api.select(Alert, "6f1173f5-f921-8e11-2160-edf42b799333")

    assert tags == alert.get_threat_tags()


def test_delete_threat_tag(cbcsdk_mock):
    """Test delete_threat_tag"""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)

    tags = ["tag1"]

    cbcsdk_mock.mock_request("DELETE",
                             "/api/alerts/v7/orgs/test/threats/"
                             "9e0afc389c1acc43b382b1ba590498d2/tags/tag2",
                             {"tags": tags})

    api = cbcsdk_mock.api
    alert = api.select(Alert, "6f1173f5-f921-8e11-2160-edf42b799333")

    assert tags == alert.delete_threat_tag("tag2")
