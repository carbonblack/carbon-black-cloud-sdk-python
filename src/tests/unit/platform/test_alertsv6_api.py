# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Tests of the Alerts V6 API queries."""
from datetime import datetime
import pytest

from cbc_sdk.errors import ApiError, TimeoutError
from cbc_sdk.platform import (
    BaseAlert,
    CBAnalyticsAlert,
    WatchlistAlert,
    DeviceControlAlert,
    WorkflowStatus,
    Process,
)
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.platform.mock_process import (
    GET_PROCESS_VALIDATION_RESP,
    POST_PROCESS_SEARCH_JOB_RESP,
    GET_PROCESS_SEARCH_JOB_RESP,
    GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
    GET_PROCESS_SUMMARY_RESP,
    GET_PROCESS_SUMMARY_STR,
    GET_PROCESS_NOT_FOUND,
    GET_PROCESS_SUMMARY_NOT_FOUND,
    GET_PROCESS_SEARCH_JOB_RESULTS_RESP_WATCHLIST_ALERT,
)
from tests.unit.fixtures.stubresponse import StubResponse, patch_cbc_sdk_api
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_enriched_events import (
    POST_ENRICHED_EVENTS_SEARCH_JOB_RESP,
    GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_ZERO_COMP,
    GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_ZERO,
    GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP,
    GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_ALERTS,
)
from tests.unit.fixtures.platform.mock_alerts import (
    GET_ALERT_RESP,
    GET_ALERT_RESP_INVALID_ALERT_ID,
    GET_ALERT_TYPE_WATCHLIST,
    GET_ALERT_TYPE_WATCHLIST_INVALID,
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

def test_query_basealert_with_all_bells_and_whistles(monkeypatch):
    """Test an alert query with all options selected."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/_search"
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"category": ["MONITORED", "THREAT"], "device_id": [6023], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "group_results": True, "id": ["S0L0"],
                                     "legacy_alert_id": ["S0L0_1"], "minimum_severity": 6, "policy_id": [8675309],
                                     "policy_name": ["Strict"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "reputation": ["SUSPECT_MALWARE"], "tag": ["Frood"], "target_value": ["HIGH"],
                                     "threat_id": ["B0RG"], "type": ["WATCHLIST"], "workflow": ["OPEN"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        _was_called = True
        return StubResponse({"results": [{"id": "S0L0", "org_key": "Z100", "threat_id": "B0RG",
                                          "workflow": {"state": "OPEN"}}], "num_found": 1})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(BaseAlert).where("Blort").set_categories(["MONITORED", "THREAT"]).set_device_ids([6023]) \
        .set_device_names(["HAL"]).set_device_os(["LINUX"]).set_device_os_versions(["0.1.2"]) \
        .set_device_username(["JRN"]).set_group_results(True).set_alert_ids(["S0L0"]) \
        .set_legacy_alert_ids(["S0L0_1"]).set_minimum_severity(6).set_policy_ids([8675309]) \
        .set_policy_names(["Strict"]).set_process_names(["IEXPLORE.EXE"]) \
        .set_process_sha256(["0123456789ABCDEF0123456789ABCDEF"]).set_reputations(["SUSPECT_MALWARE"]) \
        .set_tags(["Frood"]).set_target_priorities(["HIGH"]).set_threat_ids(["B0RG"]).set_types(["WATCHLIST"]) \
        .set_workflows(["OPEN"]).sort_by("name", "DESC")
    a = query.one()
    assert _was_called
    assert a.id == "S0L0"
    assert a.org_key == "Z100"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_with_create_time_as_start_end(monkeypatch):
    """Test an alert query with the creation time specified as a start and end time."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/_search"
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"create_time": {"start": "2019-09-30T12:34:56", "end": "2019-10-01T12:00:12"}}}
        _was_called = True
        return StubResponse({"results": [{"id": "S0L0", "org_key": "Z100", "threat_id": "B0RG",
                                          "workflow": {"state": "OPEN"}}], "num_found": 1})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(BaseAlert).where("Blort").set_create_time(start="2019-09-30T12:34:56",
                                                                 end="2019-10-01T12:00:12")
    a = query.one()
    assert _was_called
    assert a.id == "S0L0"
    assert a.org_key == "Z100"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_with_create_time_as_start_end_as_objs(monkeypatch):
    """Test an alert query with the creation time specified as a start and end time."""
    _was_called = False
    _timestamp = datetime.now()

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        nonlocal _timestamp
        assert url == "/appservices/v6/orgs/Z100/alerts/_search"
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"create_time": {"start": _timestamp.isoformat(), "end": _timestamp.isoformat()}}}
        _was_called = True
        return StubResponse({"results": [{"id": "S0L0", "org_key": "Z100", "threat_id": "B0RG",
                                          "workflow": {"state": "OPEN"}}], "num_found": 1})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(BaseAlert).where("Blort").set_create_time(start=_timestamp,
                                                                 end=_timestamp)
    a = query.one()
    assert _was_called
    assert a.id == "S0L0"
    assert a.org_key == "Z100"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_with_create_time_as_range(monkeypatch):
    """Test an alert query with the creation time specified as a range."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/_search"
        assert body == {"query": "Blort", "criteria": {"create_time": {"range": "-3w"}},
                        "rows": 2}
        _was_called = True
        return StubResponse({"results": [{"id": "S0L0", "org_key": "Z100", "threat_id": "B0RG",
                                          "workflow": {"state": "OPEN"}}], "num_found": 1})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(BaseAlert).where("Blort").set_create_time(range="-3w")
    a = query.one()
    assert _was_called
    assert a.id == "S0L0"
    assert a.org_key == "Z100"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_with_time_range(monkeypatch):
    """Test an alert query with the last_update_time specified as a range."""
    _was_called = False
    _timestamp = datetime.now()

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        nonlocal _timestamp
        assert url == "/appservices/v6/orgs/Z100/alerts/_search"
        assert body == {"query": "Blort", "criteria": {"last_update_time": {"start": _timestamp.isoformat(),
                                                                            "end": _timestamp.isoformat()}},
                        "rows": 2}
        _was_called = True
        return StubResponse({"results": [{"id": "S0L0", "org_key": "Z100", "threat_id": "B0RG",
                                          "workflow": {"state": "OPEN"}}], "num_found": 1})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(BaseAlert).where("Blort").set_time_range("last_update_time",
                                                                start=_timestamp,
                                                                end=_timestamp)
    a = query.one()
    assert _was_called
    assert a.id == "S0L0"
    assert a.org_key == "Z100"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_with_time_range_start_end(monkeypatch):
    """Test an alert query with the last_update_time specified as a range."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/_search"
        assert body == {"query": "Blort", "criteria": {"last_update_time": {"range": "-3w"}},
                        "rows": 2}
        _was_called = True
        return StubResponse({"results": [{"id": "S0L0", "org_key": "Z100", "threat_id": "B0RG",
                                          "workflow": {"state": "OPEN"}}], "num_found": 1})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(BaseAlert).where("Blort").set_time_range("last_update_time", range="-3w")
    a = query.one()
    assert _was_called
    assert a.id == "S0L0"
    assert a.org_key == "Z100"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_facets(monkeypatch):
    """Test an alert facet query."""
    _was_called = False

    def _run_facet_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/_facet"
        assert body["query"] == "Blort"
        t = body["criteria"]
        assert t["workflow"] == ["OPEN"]
        t = body["terms"]
        assert t["rows"] == 0
        assert t["fields"] == ["REPUTATION", "STATUS"]
        _was_called = True
        return StubResponse({"results": [{"field": {},
                                          "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                                         {"field": {},
                                          "values": [{"id": "status", "name": "statusX", "total": 9}]}]})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_facet_query)
    query = api.select(BaseAlert).where("Blort").set_workflows(["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
    assert _was_called
    assert f == [{"field": {}, "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                 {"field": {}, "values": [{"id": "status", "name": "statusX", "total": 9}]}]


def test_query_basealert_invalid_create_time_combinations():
    """Test invalid create time combinations being supplied to alert queries."""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    with pytest.raises(ApiError):
        api.select(BaseAlert).set_create_time()
    with pytest.raises(ApiError):
        api.select(BaseAlert).set_create_time(start="2019-09-30T12:34:56",
                                              end="2019-10-01T12:00:12", range="-3w")
    with pytest.raises(ApiError):
        api.select(BaseAlert).set_create_time(start="2019-09-30T12:34:56", range="-3w")
    with pytest.raises(ApiError):
        api.select(BaseAlert).set_create_time(end="2019-10-01T12:00:12", range="-3w")


@pytest.mark.parametrize("method, arg", [
    ("set_categories", ["SERIOUS", "CRITICAL"]),
    ("set_device_ids", ["Bogus"]),
    ("set_device_names", [42]),
    ("set_device_os", ["TI994A"]),
    ("set_device_os_versions", [8808]),
    ("set_device_username", [-1]),
    ("set_alert_ids", [9001]),
    ("set_legacy_alert_ids", [9001]),
    ("set_policy_ids", ["Bogus"]),
    ("set_policy_names", [323]),
    ("set_process_names", [7071]),
    ("set_process_sha256", [123456789]),
    ("set_reputations", ["MICROSOFT_FUDWARE"]),
    ("set_tags", [-1]),
    ("set_target_priorities", ["DOGWASH"]),
    ("set_threat_ids", [4096]),
    ("set_types", ["ERBOSOFT"]),
    ("set_workflows", ["IN_LIMBO"])
])
def test_query_basealert_invalid_criteria_values(method, arg):
    """Test invalid values being supplied to alert queries."""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    query = api.select(BaseAlert)
    meth = getattr(query, method, None)
    with pytest.raises(ApiError):
        meth(arg)


def test_query_cbanalyticsalert_with_all_bells_and_whistles(monkeypatch):
    """Test a CB Analytics alert query with all options selected."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/cbanalytics/_search"
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"category": ["THREAT", "MONITORED"], "device_id": [6023], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "group_results": True, "id": ["S0L0"],
                                     "legacy_alert_id": ["S0L0_1"], "minimum_severity": 6, "policy_id": [8675309],
                                     "policy_name": ["Strict"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "reputation": ["SUSPECT_MALWARE"], "tag": ["Frood"], "target_value": ["HIGH"],
                                     "threat_id": ["B0RG"], "type": ["WATCHLIST"], "workflow": ["OPEN"],
                                     "blocked_threat_category": ["RISKY_PROGRAM"], "device_location": ["ONSITE"],
                                     "kill_chain_status": ["EXECUTE_GOAL"],
                                     "not_blocked_threat_category": ["NEW_MALWARE"], "policy_applied": ["APPLIED"],
                                     "reason_code": ["ATTACK_VECTOR"], "run_state": ["RAN"], "sensor_action": ["DENY"],
                                     "threat_cause_vector": ["WEB"]}, "sort": [{"field": "name", "order": "DESC"}]}
        _was_called = True
        return StubResponse({"results": [{"id": "S0L0", "org_key": "Z100", "threat_id": "B0RG",
                                          "workflow": {"state": "OPEN"}}], "num_found": 1})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(CBAnalyticsAlert).where("Blort").set_categories(["THREAT", "MONITORED"]) \
        .set_device_ids([6023]).set_device_names(["HAL"]).set_device_os(["LINUX"]).set_device_os_versions(["0.1.2"]) \
        .set_device_username(["JRN"]).set_group_results(True).set_alert_ids(["S0L0"]).set_legacy_alert_ids(["S0L0_1"]) \
        .set_minimum_severity(6).set_policy_ids([8675309]).set_policy_names(["Strict"]) \
        .set_process_names(["IEXPLORE.EXE"]).set_process_sha256(["0123456789ABCDEF0123456789ABCDEF"]) \
        .set_reputations(["SUSPECT_MALWARE"]).set_tags(["Frood"]).set_target_priorities(["HIGH"]) \
        .set_threat_ids(["B0RG"]).set_types(["WATCHLIST"]).set_workflows(["OPEN"]) \
        .set_blocked_threat_categories(["RISKY_PROGRAM"]).set_device_locations(["ONSITE"]) \
        .set_kill_chain_statuses(["EXECUTE_GOAL"]).set_not_blocked_threat_categories(["NEW_MALWARE"]) \
        .set_policy_applied(["APPLIED"]).set_reason_code(["ATTACK_VECTOR"]).set_run_states(["RAN"]) \
        .set_sensor_actions(["DENY"]).set_threat_cause_vectors(["WEB"]).sort_by("name", "DESC")
    a = query.one()
    assert _was_called
    assert a.id == "S0L0"
    assert a.org_key == "Z100"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_cbanalyticsalert_facets(monkeypatch):
    """Test a CB Analytics alert facet query."""
    _was_called = False

    def _run_facet_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/cbanalytics/_facet"
        assert body == {"query": "Blort", "criteria": {"workflow": ["OPEN"]},
                        "terms": {"rows": 0, "fields": ["REPUTATION", "STATUS"]},
                        "rows": 100}
        _was_called = True
        return StubResponse({"results": [{"field": {},
                                          "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                                         {"field": {},
                                          "values": [{"id": "status", "name": "statusX", "total": 9}]}]})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_facet_query)
    query = api.select(CBAnalyticsAlert).where("Blort").set_workflows(["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
    assert _was_called
    assert f == [{"field": {}, "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                 {"field": {}, "values": [{"id": "status", "name": "statusX", "total": 9}]}]


@pytest.mark.parametrize("method, arg", [
    ("set_blocked_threat_categories", ["MINOR"]),
    ("set_device_locations", ["NARNIA"]),
    ("set_kill_chain_statuses", ["SPAWN_COPIES"]),
    ("set_not_blocked_threat_categories", ["MINOR"]),
    ("set_policy_applied", ["MAYBE"]),
    ("set_reason_code", [55]),
    ("set_run_states", ["MIGHT_HAVE"]),
    ("set_sensor_actions", ["FLIP_A_COIN"]),
    ("set_threat_cause_vectors", ["NETWORK"])
])
def test_query_cbanalyticsalert_invalid_criteria_values(method, arg):
    """Test invalid values being supplied to CB Analytics alert queries."""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    query = api.select(CBAnalyticsAlert)
    meth = getattr(query, method, None)
    with pytest.raises(ApiError):
        meth(arg)


def test_query_devicecontrolalert_with_all_bells_and_whistles(monkeypatch):
    """Test a device control alert query with all options selected."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/devicecontrol/_search"
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"category": ["MONITORED", "THREAT"], "device_id": [6023], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "group_results": True, "id": ["S0L0"],
                                     "legacy_alert_id": ["S0L0_1"], "minimum_severity": 6, "policy_id": [8675309],
                                     "policy_name": ["Strict"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "reputation": ["SUSPECT_MALWARE"], "tag": ["Frood"], "target_value": ["HIGH"],
                                     "threat_id": ["B0RG"], "type": ["WATCHLIST"], "workflow": ["OPEN"],
                                     "external_device_friendly_name": ["/dev/ice"], "external_device_id": ["626"],
                                     "product_id": ["0x5581"], "product_name": ["Ultra"],
                                     "serial_number": ["4C531001331122115172"], "vendor_id": ["0x0781"],
                                     "vendor_name": ["SanDisk"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        _was_called = True
        return StubResponse({"results": [{"id": "S0L0", "org_key": "Z100", "threat_id": "B0RG",
                                          "workflow": {"state": "OPEN"}}], "num_found": 1})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(DeviceControlAlert).where("Blort").set_categories(["MONITORED", "THREAT"]) \
        .set_device_ids([6023]).set_device_names(["HAL"]).set_device_os(["LINUX"]).set_device_os_versions(["0.1.2"]) \
        .set_device_username(["JRN"]).set_group_results(True).set_alert_ids(["S0L0"]) \
        .set_legacy_alert_ids(["S0L0_1"]).set_minimum_severity(6).set_policy_ids([8675309]) \
        .set_policy_names(["Strict"]).set_process_names(["IEXPLORE.EXE"]) \
        .set_process_sha256(["0123456789ABCDEF0123456789ABCDEF"]).set_reputations(["SUSPECT_MALWARE"]) \
        .set_tags(["Frood"]).set_target_priorities(["HIGH"]).set_threat_ids(["B0RG"]).set_types(["WATCHLIST"]) \
        .set_workflows(["OPEN"]).set_external_device_friendly_names(["/dev/ice"]).set_external_device_ids(["626"]) \
        .set_product_ids(["0x5581"]).set_product_names(["Ultra"]).set_serial_numbers(["4C531001331122115172"]) \
        .set_vendor_ids(["0x0781"]).set_vendor_names(["SanDisk"]).sort_by("name", "DESC")
    a = query.one()
    assert _was_called
    assert a.id == "S0L0"
    assert a.org_key == "Z100"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_devicecontrolalert_facets(monkeypatch):
    """Test a Device Control alert facet query."""
    _was_called = False

    def _run_facet_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/devicecontrol/_facet"
        assert body == {"query": "Blort", "criteria": {"workflow": ["OPEN"]},
                        "terms": {"rows": 0, "fields": ["REPUTATION", "STATUS"]},
                        "rows": 100}
        _was_called = True
        return StubResponse({"results": [{"field": {},
                                          "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                                         {"field": {},
                                          "values": [{"id": "status", "name": "statusX", "total": 9}]}]})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_facet_query)
    query = api.select(DeviceControlAlert).where("Blort").set_workflows(["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
    assert _was_called
    assert f == [{"field": {}, "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                 {"field": {}, "values": [{"id": "status", "name": "statusX", "total": 9}]}]


@pytest.mark.parametrize("method, arg", [
    ("set_external_device_friendly_names", [12345]),
    ("set_external_device_ids", [12345]),
    ("set_product_ids", [12345]),
    ("set_product_names", [12345]),
    ("set_serial_numbers", [12345]),
    ("set_vendor_ids", [12345]),
    ("set_vendor_names", [12345])
])
def test_query_devicecontrolalert_invalid_criteria_values(method, arg):
    """Test invalid values being supplied to DeviceControl alert queries."""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    query = api.select(DeviceControlAlert)
    meth = getattr(query, method, None)
    with pytest.raises(ApiError):
        meth(arg)


def test_query_watchlistalert_with_all_bells_and_whistles(monkeypatch):
    """Test a watchlist alert query with all options selected."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/watchlist/_search"
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"category": ["THREAT", "MONITORED"], "device_id": [6023], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "group_results": True, "id": ["S0L0"],
                                     "legacy_alert_id": ["S0L0_1"], "minimum_severity": 6, "policy_id": [8675309],
                                     "policy_name": ["Strict"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "reputation": ["SUSPECT_MALWARE"], "tag": ["Frood"], "target_value": ["HIGH"],
                                     "threat_id": ["B0RG"], "type": ["WATCHLIST"], "workflow": ["OPEN"],
                                     "watchlist_id": ["100"], "watchlist_name": ["Gandalf"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        _was_called = True
        return StubResponse({"results": [{"id": "S0L0", "org_key": "Z100", "threat_id": "B0RG",
                                          "workflow": {"state": "OPEN"}}], "num_found": 1})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(WatchlistAlert).where("Blort").set_categories(["THREAT", "MONITORED"]).set_device_ids([6023]) \
        .set_device_names(["HAL"]).set_device_os(["LINUX"]).set_device_os_versions(["0.1.2"]) \
        .set_device_username(["JRN"]).set_group_results(True).set_alert_ids(["S0L0"]) \
        .set_legacy_alert_ids(["S0L0_1"]).set_minimum_severity(6).set_policy_ids([8675309]) \
        .set_policy_names(["Strict"]).set_process_names(["IEXPLORE.EXE"]) \
        .set_process_sha256(["0123456789ABCDEF0123456789ABCDEF"]).set_reputations(["SUSPECT_MALWARE"]) \
        .set_tags(["Frood"]).set_target_priorities(["HIGH"]).set_threat_ids(["B0RG"]).set_types(["WATCHLIST"]) \
        .set_workflows(["OPEN"]).set_watchlist_ids(["100"]).set_watchlist_names(["Gandalf"]).sort_by("name", "DESC")
    a = query.one()
    assert _was_called
    assert a.id == "S0L0"
    assert a.org_key == "Z100"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_watchlistalert_facets(monkeypatch):
    """Test a watchlist alert facet query."""
    _was_called = False

    def _run_facet_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/watchlist/_facet"
        assert body == {"query": "Blort", "criteria": {"workflow": ["OPEN"]},
                        "terms": {"rows": 0, "fields": ["REPUTATION", "STATUS"]},
                        "rows": 100}
        _was_called = True
        return StubResponse({"results": [{"field": {},
                                          "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                                         {"field": {},
                                          "values": [{"id": "status", "name": "statusX", "total": 9}]}]})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_facet_query)
    query = api.select(WatchlistAlert).where("Blort").set_workflows(["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
    assert _was_called
    assert f == [{"field": {}, "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                 {"field": {}, "values": [{"id": "status", "name": "statusX", "total": 9}]}]


def test_query_watchlistalert_invalid_criteria_values():
    """Test error messages for invalid watchlist alert criteria values."""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    with pytest.raises(ApiError):
        api.select(WatchlistAlert).set_watchlist_ids([888])
    with pytest.raises(ApiError):
        api.select(WatchlistAlert).set_watchlist_names([69])


def test_alerts_bulk_dismiss(monkeypatch):
    """Test dismissing a batch of alerts."""
    _was_called = False

    def _do_dismiss(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/workflow/_criteria"
        assert body == {"query": "Blort", "state": "DISMISSED", "remediation_state": "Fixed", "comment": "Yessir",
                        "criteria": {"device_name": ["HAL9000"]}}
        _was_called = True
        return StubResponse({"request_id": "497ABX"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_do_dismiss)
    q = api.select(BaseAlert).where("Blort").set_device_names(["HAL9000"])
    reqid = q.dismiss("Fixed", "Yessir")
    assert _was_called
    assert reqid == "497ABX"


def test_alerts_bulk_undismiss(monkeypatch):
    """Test undismissing a batch of alerts."""
    _was_called = False

    def _do_update(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/workflow/_criteria"
        assert body == {"query": "Blort", "state": "OPEN", "remediation_state": "Fixed", "comment": "NoSir",
                        "criteria": {"device_name": ["HAL9000"]}}
        _was_called = True
        return StubResponse({"request_id": "497ABX"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_do_update)
    q = api.select(BaseAlert).where("Blort").set_device_names(["HAL9000"])
    reqid = q.update("Fixed", "NoSir")
    assert _was_called
    assert reqid == "497ABX"


def test_alerts_bulk_dismiss_watchlist(monkeypatch):
    """Test dismissing a batch of watchlist alerts."""
    _was_called = False

    def _do_dismiss(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/watchlist/workflow/_criteria"
        assert body == {"query": "Blort", "state": "DISMISSED", "remediation_state": "Fixed", "comment": "Yessir",
                        "criteria": {"device_name": ["HAL9000"]}}
        _was_called = True
        return StubResponse({"request_id": "497ABX"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_do_dismiss)
    q = api.select(WatchlistAlert).where("Blort").set_device_names(["HAL9000"])
    reqid = q.dismiss("Fixed", "Yessir")
    assert _was_called
    assert reqid == "497ABX"


def test_alerts_bulk_dismiss_cbanalytics(monkeypatch):
    """Test dismissing a batch of CB Analytics alerts."""
    _was_called = False

    def _do_dismiss(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/cbanalytics/workflow/_criteria"
        assert body == {"query": "Blort", "state": "DISMISSED", "remediation_state": "Fixed", "comment": "Yessir",
                        "criteria": {"device_name": ["HAL9000"]}}
        _was_called = True
        return StubResponse({"request_id": "497ABX"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_do_dismiss)
    q = api.select(CBAnalyticsAlert).where("Blort").set_device_names(["HAL9000"])
    reqid = q.dismiss("Fixed", "Yessir")
    assert _was_called
    assert reqid == "497ABX"


def test_alerts_bulk_dismiss_vmware(monkeypatch):
    """Test dismissing a batch of VMware alerts."""
    _was_called = False

    def _do_dismiss(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/cbanalytics/workflow/_criteria"
        assert body == {"query": "Blort", "state": "DISMISSED", "remediation_state": "Fixed", "comment": "Yessir",
                        "criteria": {"device_name": ["HAL9000"]}}
        _was_called = True
        return StubResponse({"request_id": "497ABX"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_do_dismiss)
    q = api.select(CBAnalyticsAlert).where("Blort").set_device_names(["HAL9000"])
    reqid = q.dismiss("Fixed", "Yessir")
    assert _was_called
    assert reqid == "497ABX"


def test_alerts_bulk_dismiss_threat(monkeypatch):
    """Test dismissing a batch of threat alerts."""
    _was_called = False

    def _do_dismiss(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/threat/workflow/_criteria"
        assert body == {"threat_id": ["B0RG", "F3R3NG1"], "state": "DISMISSED", "remediation_state": "Fixed",
                        "comment": "Yessir"}
        _was_called = True
        return StubResponse({"request_id": "497ABX"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_do_dismiss)
    reqid = api.bulk_threat_dismiss(["B0RG", "F3R3NG1"], "Fixed", "Yessir")
    assert _was_called
    assert reqid == "497ABX"


def test_alerts_bulk_undismiss_threat(monkeypatch):
    """Test undismissing a batch of threat alerts."""
    _was_called = False

    def _do_update(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/threat/workflow/_criteria"
        assert body == {"threat_id": ["B0RG", "F3R3NG1"], "state": "OPEN", "remediation_state": "Fixed",
                        "comment": "NoSir"}
        _was_called = True
        return StubResponse({"request_id": "497ABX"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_do_update)
    reqid = api.bulk_threat_update(["B0RG", "F3R3NG1"], "Fixed", "NoSir")
    assert _was_called
    assert reqid == "497ABX"


def test_alerts_bulk_threat_error(monkeypatch):
    """Test error raise from bulk threat update status"""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    with pytest.raises(ApiError):
        api.bulk_threat_dismiss([123], "Fixed", "Yessir")


def test_load_workflow(monkeypatch):
    """Test loading a workflow status."""
    _was_called = False

    def _get_workflow(url, parms=None, default=None):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/workflow/status/497ABX"
        _was_called = True
        return {"errors": [], "failed_ids": [], "id": "497ABX", "num_hits": 0, "num_success": 0, "status": "QUEUED",
                "workflow": {"state": "DISMISSED", "remediation": "Fixed", "comment": "Yessir",
                             "changed_by": "Robocop", "last_update_time": "2019-10-31T16:03:13.951Z"}}

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_workflow)
    workflow = api.select(WorkflowStatus, "497ABX")
    assert _was_called
    assert workflow.id_ == "497ABX"


def test_get_process(cbcsdk_mock):
    """Test of getting process through a WatchlistAlert"""
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/alerts/6b2348cb-87c1-4076-bc8e-7c717e8af608",
                             GET_ALERT_TYPE_WATCHLIST)
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_job",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_WATCHLIST_ALERT)
    # mock the POST of a summary search (using same Job ID)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/summary_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check summary search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SUMMARY_RESP)
    # mock the GET to get summary search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SUMMARY_STR)
    api = cbcsdk_mock.api
    alert = api.select(WatchlistAlert, "6b2348cb-87c1-4076-bc8e-7c717e8af608")
    process = alert.get_process()
    assert isinstance(process, Process)
    assert process.process_guid == "WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00"


def test_get_process_zero_found(cbcsdk_mock):
    """Test of getting process through a WatchlistAlert"""
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_TYPE_WATCHLIST)
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_job",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_WATCHLIST_ALERT)
    # mock the POST of a summary search (using same Job ID)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/summary_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get process search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_NOT_FOUND)
    # mock the GET to get summary search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SUMMARY_NOT_FOUND)
    api = cbcsdk_mock.api
    alert = api.select(WatchlistAlert, "86123310980efd0b38111eba4bfa5e98aa30b19")
    process = alert.get_process()
    assert not process


def test_get_process_raises_api_error(cbcsdk_mock):
    """Test of getting process through a WatchlistAlert"""
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/alerts/6b2348cb-87c1-4076-bc8e-7c717e8af608",
                             GET_ALERT_TYPE_WATCHLIST_INVALID)
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP)
    api = cbcsdk_mock.api
    with pytest.raises(ApiError):
        alert = api.select(WatchlistAlert, "6b2348cb-87c1-4076-bc8e-7c717e8af608")
        alert.get_process()


def test_get_process_async(cbcsdk_mock):
    """Test of getting process through a WatchlistAlert async"""
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/alerts/6b2348cb-87c1-4076-bc8e-7c717e8af608",
                             GET_ALERT_TYPE_WATCHLIST)
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_job",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_WATCHLIST_ALERT)
    # mock the POST of a summary search (using same Job ID)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/summary_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check summary search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SUMMARY_RESP)
    # mock the GET to get summary search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SUMMARY_STR)
    api = cbcsdk_mock.api
    alert = api.select(WatchlistAlert, "6b2348cb-87c1-4076-bc8e-7c717e8af608")
    process = alert.get_process(async_mode=True).result()
    assert isinstance(process, Process)
    assert process.process_guid == "WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00"


def test_get_events(cbcsdk_mock):
    """Test get_events method"""
    cbcsdk_mock.mock_request("GET",
                             "/appservices/v6/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_ALERTS)

    api = cbcsdk_mock.api
    alert = api.select(CBAnalyticsAlert, '86123310980efd0b38111eba4bfa5e98aa30b19')
    events = alert.get_events()
    assert len(events) == 2
    for event in events:
        assert event.alert_id == ['62802DCE']


def test_get_events_zero_found(cbcsdk_mock):
    """Test get_events method - zero enriched events found"""
    cbcsdk_mock.mock_request("GET",
                             "/appservices/v6/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_ZERO)

    api = cbcsdk_mock.api
    alert = api.select(CBAnalyticsAlert, '86123310980efd0b38111eba4bfa5e98aa30b19')
    events = alert.get_events()
    assert len(events) == 0


def test_get_events_timeout(cbcsdk_mock):
    """Test that get_events() throws a timeout appropriately."""
    cbcsdk_mock.mock_request("GET",
                             "/appservices/v6/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING)

    api = cbcsdk_mock.api
    alert = api.select(CBAnalyticsAlert, '86123310980efd0b38111eba4bfa5e98aa30b19')
    with pytest.raises(TimeoutError):
        alert.get_events(timeout=1)


def test_get_events_detail_jobs_resp_handling(cbcsdk_mock):
    """Test get_events method - different resps from details jobs request"""
    called = 0

    def get_validate(*args):
        nonlocal called
        called += 1
        if called == 1:
            return GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING
        if called == 2:
            return GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_ZERO_COMP
        return GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP
    cbcsdk_mock.mock_request("GET",
                             "/appservices/v6/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             get_validate)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_ALERTS)

    api = cbcsdk_mock.api
    alert = api.select(CBAnalyticsAlert, '86123310980efd0b38111eba4bfa5e98aa30b19')
    events = alert.get_events()
    assert len(events) == 2
    for event in events:
        assert event.alert_id == ['62802DCE']


def test_get_events_invalid_alert_id(cbcsdk_mock):
    """Test get_events method with invalid alert_id"""
    cbcsdk_mock.mock_request("GET",
                             "/appservices/v6/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP_INVALID_ALERT_ID)

    api = cbcsdk_mock.api
    alert = api.select(CBAnalyticsAlert, '86123310980efd0b38111eba4bfa5e98aa30b19')
    with pytest.raises(ApiError):
        alert.get_events()


def test_get_events_async(cbcsdk_mock):
    """Test async get_events method"""
    cbcsdk_mock.mock_request("GET",
                             "/appservices/v6/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_ALERTS)

    api = cbcsdk_mock.api
    alert = api.select(CBAnalyticsAlert, '86123310980efd0b38111eba4bfa5e98aa30b19')
    events = alert.get_events(async_mode=True).result()
    assert len(events) == 2
    for event in events:
        assert event.alert_id == ['62802DCE']


def test_query_basealert_with_time_range_errors(cbcsdk_mock):
    """Test exeptions in alert query"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError) as ex:
        api.select(BaseAlert).where("Blort").set_time_range("invalid", range="whatever")
    assert "key must be one of create_time, first_event_time, last_event_time, or last_update_time" in str(ex.value)

    with pytest.raises(ApiError) as ex:
        api.select(BaseAlert).where("Blort").set_time_range("create_time",
                                                            start="2019-09-30T12:34:56",
                                                            end="2019-10-01T12:00:12",
                                                            range="-3w")
    assert "cannot specify range= in addition to start= and end=" in str(ex.value)

    with pytest.raises(ApiError) as ex:
        api.select(BaseAlert).where("Blort").set_time_range("create_time",
                                                            end="2019-10-01T12:00:12",
                                                            range="-3w")
    assert "cannot specify start= or end= in addition to range=" in str(ex.value)

    with pytest.raises(ApiError) as ex:
        api.select(BaseAlert).where("Blort").set_time_range("create_time")

    assert "must specify either start= and end= or range=" in str(ex.value)


def test_query_basealert_sort_error(cbcsdk_mock):
    """Test an alert query with the invalid sort direction"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError) as ex:
        api.select(BaseAlert).where("Blort").sort_by("create_time", "bla")
    assert "invalid sort direction specified" in str(ex.value)


def test_query_basealert_facets_error(cbcsdk_mock):
    """Test an alert facet query with invalid term."""
    api = cbcsdk_mock.api
    query = api.select(BaseAlert).where("Blort").set_workflows(["OPEN"])
    with pytest.raises(ApiError) as ex:
        query.facets(["ALABALA", "STATUS"])
    assert "One or more invalid term field names" in str(ex.value)
