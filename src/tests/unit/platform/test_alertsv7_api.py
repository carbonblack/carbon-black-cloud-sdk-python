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

from cbc_sdk.errors import ApiError, NonQueryableModel
from cbc_sdk.platform import (
    Alert,
    WatchlistAlert, ContainerRuntimeAlert, Process,
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
    GET_ALERT_RESP
)
from tests.unit.fixtures.platform.mock_process import (
    GET_PROCESS_VALIDATION_RESP,
    POST_PROCESS_SEARCH_JOB_RESP,
    GET_PROCESS_SEARCH_JOB_RESP,
    GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
    GET_PROCESS_SUMMARY_STR,
    GET_PROCESS_NOT_FOUND,
    GET_PROCESS_SEARCH_JOB_RESULTS_RESP_WATCHLIST_ALERT_V7,
)
from tests.unit.fixtures.platform.mock_observations import (
    POST_OBSERVATIONS_SEARCH_JOB_RESP,
    GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP
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
                        "criteria": {"backend_timestamp": {"start": "2019-09-30T12:34:56",
                                                           "end": "2019-10-01T12:00:12"}}}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").set_time_range("backend_timestamp", start="2019-09-30T12:34:56",
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
                        "criteria": {"backend_timestamp": {"start": _timestamp.isoformat(),
                                                           "end": _timestamp.isoformat()}}}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").set_time_range("backend_timestamp", start=_timestamp, end=_timestamp)
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

    query = api.select(Alert).where("Blort").set_time_range("backend_timestamp", range="-3w")
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
        assert body == {"query": "Blort", "criteria": {"backend_update_timestamp": {"start": _timestamp.isoformat(),
                                                                                    "end": _timestamp.isoformat()}},
                        "rows": 2}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").set_time_range("backend_update_timestamp", start=_timestamp,
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

    query = api.select(Alert).where("Blort").set_time_range("backend_update_timestamp", range="-3w")
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
        assert t["workflow"] == ["OPEN"]
        t = body["terms"]
        assert t["rows"] == 0
        assert t["fields"] == ["REPUTATION", "STATUS"]
        return {"results": [{"field": {},
                             "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                            {"field": {},
                             "values": [{"id": "status", "name": "statusX", "total": 9}]}]}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_facet", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").set_workflows(["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
    assert f == [{"field": {}, "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                 {"field": {}, "values": [{"id": "status", "name": "statusX", "total": 9}]}]


def test_query_alert_invalid_backend_timestamp_combinations(cb):
    """Test invalid backend_timestamp combinations being supplied to alert queries."""
    with pytest.raises(ApiError):
        cb.select(Alert).set_time_range("backend_timestamp")
    with pytest.raises(ApiError):
        cb.select(Alert).set_time_range("backend_timestamp", start="2019-09-30T12:34:56", end="2019-10-01T12:00:12",
                                        range="-3w")
    with pytest.raises(ApiError):
        cb.select(Alert).set_time_range("backend_timestamp", start="2019-09-30T12:34:56", range="-3w")
    with pytest.raises(ApiError):
        cb.select(Alert).set_time_range("backend_timestamp", end="2019-10-01T12:00:12", range="-3w")


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
                                     "alert_notes_present": ["True"], "attack_tactic": ["tactic"],
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
        .add_criteria("alert_notes_present", "True").add_criteria("attack_tactic", ["tactic"]).add_criteria(
        "attack_technique", ["technique"]) \
        .add_criteria("blocked_effective_reputation", ["NOT_LISTED"]).add_criteria("blocked_md5",
                                                                                   ["md5_hash"]).add_criteria(
        "blocked_name", ["tim"]) \
        .add_criteria("blocked_sha256", ["sha256_hash"]) \
        .add_criteria("childproc_cmdline", ["/usr/bin/python"]).add_criteria("childproc_effective_reputation", ["PUP"])\
        .add_criteria("childproc_guid", ["12345678"]).add_criteria("childproc_name", ["python"]).add_criteria(
        "childproc_sha256", ["sha256_child"]) \
        .add_criteria("childproc_username", ["steven"]) \
        .add_criteria("parent_cmdline", ["/usr/bin/python"]).add_criteria("parent_effective_reputation", ["PUP"]) \
        .add_criteria("parent_guid", ["12345678"]).add_criteria("parent_name", ["python"])\
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


def test_query_cbanalyticsalert_facets(cbcsdk_mock):
    """Test a CB Analytics alert facet query."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "criteria": {'type': ['CB_ANALYTICS'], "workflow_status": ["OPEN"]},
                        "terms": {"rows": 0, "fields": ["REPUTATION", "STATUS"]}}
        return {"results": [{"field": {},
                             "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                            {"field": {},
                             "values": [{"id": "status", "name": "statusX", "total": 9}]}]}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_facet", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").add_criteria("type", ["CB_ANALYTICS"]).add_criteria("workflow_status",
                                                                                                 ["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
    assert f == [{"field": {}, "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                 {"field": {}, "values": [{"id": "status", "name": "statusX", "total": 9}]}]


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


def test_query_devicecontrolalert_facets(cbcsdk_mock):
    """Test a Device Control alert facet query."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "criteria": {'type': ['DEVICE_CONTROL'], "workflow_status": ["OPEN"]},
                        "terms": {"rows": 0, "fields": ["REPUTATION", "STATUS"]}}
        return {"results": [{"field": {},
                             "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                            {"field": {},
                             "values": [{"id": "status", "name": "statusX", "total": 9}]}]}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_facet", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").add_criteria("type", ["DEVICE_CONTROL"]).add_criteria("workflow_status",
                                                                                                   ["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
    assert f == [{"field": {}, "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                 {"field": {}, "values": [{"id": "status", "name": "statusX", "total": 9}]}]


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
                                     "threat_id": ["B0RG"], "type": ["WATCHLIST"], "workflow_status": ["OPEN"],
                                     "watchlists_id": ["100"], "watchlists_name": ["Gandalf"],
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
        .add_criteria("childproc_cmdline", ["/usr/bin/python"])\
        .add_criteria("childproc_effective_reputation", ["PUP"]) \
        .add_criteria("childproc_guid", ["12345678"]).add_criteria("childproc_name", ["python"]).add_criteria(
        "childproc_sha256", ["sha256_child"]) \
        .add_criteria("childproc_username", ["steven"]) \
        .add_criteria("parent_cmdline", ["/usr/bin/python"]).add_criteria("parent_effective_reputation", ["PUP"]) \
        .add_criteria("parent_guid", ["12345678"]).add_criteria("parent_name", ["python"])\
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


def test_query_watchlistalert_facets(cbcsdk_mock):
    """Test a watchlist alert facet query."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "criteria": {'type': ['WATCHLIST'], "workflow_status": ["OPEN"]},
                        "terms": {"rows": 0, "fields": ["REPUTATION", "STATUS"]}}
        return {"results": [{"field": {},
                             "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                            {"field": {},
                             "values": [{"id": "status", "name": "statusX", "total": 9}]}]}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_facet", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).where("Blort").add_criteria("type", ["WATCHLIST"]).add_criteria("workflow_status",
                                                                                              ["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
    assert f == [{"field": {}, "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                 {"field": {}, "values": [{"id": "status", "name": "statusX", "total": 9}]}]


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
        .add_criteria("k8s_namespace", ['RG']).add_criteria("k8s_rule_id", ['66'])\
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
                        "criteria": {},
                        "rows": 10000,
                        "start": 1,
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
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/887e6bbc-6224-4f36-ad37-084038b7fcab",
                             GET_ALERT_TYPE_WATCHLIST)
    # mock the search validation
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/processes/search_validation?"
                             "process_guid=ABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805"
                             "&q=process_guid%3AABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805"
                             "&query=process_guid%3AABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805",
                             GET_PROCESS_VALIDATION_RESP)
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
    process = alert.get_process()
    assert isinstance(process, Process)
    assert process.process_guid == "ABC12345-0002b226-000015bd-00000000-1d6225bbba74c00"


def test_get_process_zero_found(cbcsdk_mock):
    """Test of getting process through a WatchlistAlert"""
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_TYPE_WATCHLIST)
    # mock the search validation
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/processes/search_validation?"
                             "process_guid=ABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805"
                             "&q=process_guid%3AABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805"
                             "&query=process_guid%3AABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805",
                             GET_PROCESS_VALIDATION_RESP)
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
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/processes/search_validation?"
                             "process_guid=ABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805"
                             "&q=process_guid%3AABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805"
                             "&query=process_guid%3AABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805",
                             GET_PROCESS_VALIDATION_RESP)
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
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/processes/search_validation?"
                             "process_guid=ABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805"
                             "&q=process_guid%3AABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805"
                             "&query=process_guid%3AABC12345%5C-000309c2%5C-00000478%5C-00000000%5C-1d6a1c1f2b02805",
                             GET_PROCESS_VALIDATION_RESP)
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
        api.select(Alert).where("Blort").set_time_range("invalid", range="whatever")
    assert "key must be one of create_time, first_event_time, last_event_time, backend_timestamp," \
           " backend_update_timestamp, or last_update_time" in str(ex.value)

    with pytest.raises(ApiError) as ex:
        api.select(Alert).where("Blort").set_time_range("backend_timestamp",
                                                        start="2019-09-30T12:34:56",
                                                        end="2019-10-01T12:00:12",
                                                        range="-3w")
    assert "cannot specify range= in addition to start= and end=" in str(ex.value)

    with pytest.raises(ApiError) as ex:
        api.select(Alert).where("Blort").set_time_range("backend_timestamp",
                                                        end="2019-10-01T12:00:12",
                                                        range="-3w")
    assert "cannot specify start= or end= in addition to range=" in str(ex.value)

    with pytest.raises(ApiError) as ex:
        api.select(Alert).where("Blort").set_time_range("backend_timestamp")

    assert "must specify either start= and end= or range=" in str(ex.value)


def test_query_alert_sort_error(cbcsdk_mock):
    """Test an alert query with the invalid sort direction"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError) as ex:
        api.select(Alert).where("Blort").sort_by("backend_timestamp", "bla")
    assert "invalid sort direction specified" in str(ex.value)


def test_query_alert_facets_error(cbcsdk_mock):
    """Test an alert facet query with invalid term."""
    api = cbcsdk_mock.api
    query = api.select(Alert).where("Blort").set_workflows(["OPEN"])
    with pytest.raises(ApiError) as ex:
        query.facets(["ALABALA", "STATUS"])
    assert "One or more invalid term field names" in str(ex.value)


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
    assert note[0].note == "I am Grogu"


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
            "rows": 1,
            "start": 1
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
            "rows": 1,
            "start": 1
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
            "rows": 1,
            "start": 1
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
            "rows": 1,
            "start": 1
        }
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"status": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(Alert).set_remote_is_private(True).set_rows(1)
    len(query)
    # no assertions, the check is that the post request is formed correctly.


def test_get_observations(cbcsdk_mock):
    """Test tget_observations method."""
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
