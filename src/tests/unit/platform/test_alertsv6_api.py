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

"""Tests of the Alerts V6 API queries."""
from datetime import datetime
import pytest

from cbc_sdk.errors import ApiError, TimeoutError, NonQueryableModel
from cbc_sdk.platform import (
    BaseAlert,
    CBAnalyticsAlert,
    WatchlistAlert,
    DeviceControlAlert,
    ContainerRuntimeAlert,
    Process,
)
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.platform.mock_process import (
    POST_PROCESS_VALIDATION_RESP,
    POST_PROCESS_SEARCH_JOB_RESP,
    GET_PROCESS_SEARCH_JOB_RESP,
    GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
    GET_PROCESS_SUMMARY_STR,
    GET_PROCESS_NOT_FOUND,
    GET_PROCESS_SEARCH_JOB_RESULTS_RESP_WATCHLIST_ALERT,
)
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
    GET_ALERT_RESP_WITH_NOTES,
    GET_ALERT_NOTES,
    CREATE_ALERT_NOTE,
)
from tests.unit.fixtures.mock_rest_api import ALERT_SEARCH_SUGGESTIONS_RESP


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

def test_query_basealert_with_all_bells_and_whistles(cbcsdk_mock):
    """Test an alert query with all options selected."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"device_id": [6023], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "id": ["S0L0"],
                                     "legacy_alert_id": ["S0L0_1"], "minimum_severity": 6, "policy_id": [8675309],
                                     "policy_name": ["Strict"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "reputation": ["SUSPECT_MALWARE"], "tag": ["Frood"], "target_value": ["HIGH"],
                                     "threat_id": ["B0RG"], "workflow": ["OPEN"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG", "type": "WATCHLIST",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api
    query = api.select(BaseAlert).where("Blort").set_device_ids([6023]) \
        .set_device_names(["HAL"]).set_device_os(["LINUX"]).set_device_os_versions(["0.1.2"]) \
        .set_device_username(["JRN"]).set_alert_ids(["S0L0"]) \
        .set_legacy_alert_ids(["S0L0_1"]).set_minimum_severity(6).set_policy_ids([8675309]) \
        .set_policy_names(["Strict"]).set_process_names(["IEXPLORE.EXE"]) \
        .set_process_sha256(["0123456789ABCDEF0123456789ABCDEF"]).set_reputations(["SUSPECT_MALWARE"]) \
        .set_tags(["Frood"]).set_target_priorities(["HIGH"]).set_threat_ids(["B0RG"]) \
        .set_workflows(["OPEN"]).sort_by("name", "DESC")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_with_create_time_as_start_end(cbcsdk_mock):
    """Test an alert query with the creation time specified as a start and end time."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"create_time": {"start": "2019-09-30T12:34:56", "end": "2019-10-01T12:00:12"}}}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select("BaseAlert").where("Blort").set_create_time(start="2019-09-30T12:34:56",
                                                                   end="2019-10-01T12:00:12")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_with_create_time_as_start_end_as_objs(cbcsdk_mock):
    """Test an alert query with the creation time specified as a start and end time."""
    _timestamp = datetime.now()

    def on_post(url, body, **kwargs):
        nonlocal _timestamp
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"create_time": {"start": _timestamp.isoformat(), "end": _timestamp.isoformat()}}}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(BaseAlert).where("Blort").set_create_time(start=_timestamp, end=_timestamp)
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_with_create_time_as_range(cbcsdk_mock):
    """Test an alert query with the creation time specified as a range."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "criteria": {"create_time": {"range": "-3w"}}, "rows": 2}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(BaseAlert).where("Blort").set_create_time(range="-3w")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_with_time_range(cbcsdk_mock):
    """Test an alert query with the last_update_time specified as a range."""
    _timestamp = datetime.now()

    def on_post(url, body, **kwargs):
        nonlocal _timestamp
        assert body == {"query": "Blort", "criteria": {"last_update_time": {
            "start": _timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "end": _timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}},
            "rows": 2}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(BaseAlert).where("Blort").set_time_range("last_update_time",
                                                                start=_timestamp,
                                                                end=_timestamp)
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_with_time_range_start_end(cbcsdk_mock):
    """Test an alert query with the last_update_time specified as a range."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "criteria": {"last_update_time": {"range": "-3w"}}, "rows": 2}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(BaseAlert).where("Blort").set_time_range("last_update_time", range="-3w")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_with_time_range_create_time_as_start_end(cbcsdk_mock):
    """Test an alert query with the create_time specified as a range which should also set the global time_range."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "criteria": {"create_time": {"range": "-3w"}}, "rows": 2,
                        'time_range': {'range': '-3w'}}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(BaseAlert).where("Blort").set_time_range("create_time", range="-3w")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_basealert_facets(cbcsdk_mock):
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

    query = api.select(BaseAlert).where("Blort").set_workflows(["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
    assert f == [{"field": {}, "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                 {"field": {}, "values": [{"id": "status", "name": "statusX", "total": 9}]}]


def test_query_basealert_invalid_create_time_combinations(cb):
    """Test invalid create time combinations being supplied to alert queries."""
    with pytest.raises(ApiError):
        cb.select(BaseAlert).set_create_time()
    with pytest.raises(ApiError):
        cb.select(BaseAlert).set_create_time(start="2019-09-30T12:34:56",
                                             end="2019-10-01T12:00:12", range="-3w")
    with pytest.raises(ApiError):
        cb.select(BaseAlert).set_create_time(start="2019-09-30T12:34:56", range="-3w")
    with pytest.raises(ApiError):
        cb.select(BaseAlert).set_create_time(end="2019-10-01T12:00:12", range="-3w")


@pytest.mark.parametrize("method, arg", [
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
def test_query_basealert_invalid_criteria_values(cb, method, arg):
    """Test invalid values being supplied to alert queries."""
    query = cb.select(BaseAlert)
    meth = getattr(query, method, None)
    with pytest.raises(ApiError):
        meth(arg)


def test_query_cbanalyticsalert_with_all_bells_and_whistles(cbcsdk_mock):
    """Test a CB Analytics alert query with all options selected."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"device_id": [6023], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "id": ["S0L0"],
                                     "legacy_alert_id": ["S0L0_1"], "minimum_severity": 6, "policy_id": [8675309],
                                     "policy_name": ["Strict"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "reputation": ["SUSPECT_MALWARE"], "tag": ["Frood"], "target_value": ["HIGH"],
                                     "threat_id": ["B0RG"], "type": ["CB_ANALYTICS"], "workflow": ["OPEN"],
                                     "device_location": ["ONSITE"], "policy_applied": ["APPLIED"],
                                     "reason_code": ["ATTACK_VECTOR"], "run_state": ["RAN"], "sensor_action": ["DENY"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(CBAnalyticsAlert).where("Blort") \
        .set_device_ids([6023]).set_device_names(["HAL"]).set_device_os(["LINUX"]).set_device_os_versions(["0.1.2"]) \
        .set_device_username(["JRN"]).set_alert_ids(["S0L0"]).set_legacy_alert_ids(["S0L0_1"]) \
        .set_minimum_severity(6).set_policy_ids([8675309]).set_policy_names(["Strict"]) \
        .set_process_names(["IEXPLORE.EXE"]).set_process_sha256(["0123456789ABCDEF0123456789ABCDEF"]) \
        .set_reputations(["SUSPECT_MALWARE"]).set_tags(["Frood"]).set_target_priorities(["HIGH"]) \
        .set_threat_ids(["B0RG"]).set_workflows(["OPEN"]).set_device_locations(["ONSITE"]) \
        .set_policy_applied(["APPLIED"]).set_reason_code(["ATTACK_VECTOR"]).set_run_states(["RAN"]) \
        .set_sensor_actions(["DENY"]).sort_by("name", "DESC")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_cbanalyticsalert_facets(cbcsdk_mock):
    """Test a CB Analytics alert facet query."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "criteria": {'type': ['CB_ANALYTICS'], "workflow": ["OPEN"]},
                        "terms": {"rows": 0, "fields": ["REPUTATION", "STATUS"]}}
        return {"results": [{"field": {},
                             "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                            {"field": {},
                             "values": [{"id": "status", "name": "statusX", "total": 9}]}]}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_facet", on_post)
    api = cbcsdk_mock.api

    query = api.select(CBAnalyticsAlert).where("Blort").set_workflows(["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
    assert f == [{"field": {}, "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                 {"field": {}, "values": [{"id": "status", "name": "statusX", "total": 9}]}]


@pytest.mark.parametrize("method, arg", [
    ("set_device_locations", ["NARNIA"]),
    ("set_policy_applied", ["MAYBE"]),
    ("set_reason_code", [55]),
    ("set_run_states", ["MIGHT_HAVE"]),
    ("set_sensor_actions", ["FLIP_A_COIN"])
])
def test_query_cbanalyticsalert_invalid_criteria_values(cb, method, arg):
    """Test invalid values being supplied to CB Analytics alert queries."""
    query = cb.select(CBAnalyticsAlert)
    meth = getattr(query, method, None)
    with pytest.raises(ApiError):
        meth(arg)


def test_query_devicecontrolalert_with_all_bells_and_whistles(cbcsdk_mock):
    """Test a device control alert query with all options selected."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"device_id": [6023], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "id": ["S0L0"],
                                     "legacy_alert_id": ["S0L0_1"], "minimum_severity": 6, "policy_id": [8675309],
                                     "policy_name": ["Strict"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "reputation": ["SUSPECT_MALWARE"], "tag": ["Frood"], "target_value": ["HIGH"],
                                     "threat_id": ["B0RG"], "type": ["DEVICE_CONTROL"], "workflow": ["OPEN"],
                                     "external_device_friendly_name": ["/dev/ice"], "external_device_id": ["626"],
                                     "product_id": ["0x5581"], "product_name": ["Ultra"],
                                     "serial_number": ["4C531001331122115172"], "vendor_id": ["0x0781"],
                                     "vendor_name": ["SanDisk"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(DeviceControlAlert).where("Blort") \
        .set_device_ids([6023]).set_device_names(["HAL"]).set_device_os(["LINUX"]).set_device_os_versions(["0.1.2"]) \
        .set_device_username(["JRN"]).set_alert_ids(["S0L0"]) \
        .set_legacy_alert_ids(["S0L0_1"]).set_minimum_severity(6).set_policy_ids([8675309]) \
        .set_policy_names(["Strict"]).set_process_names(["IEXPLORE.EXE"]) \
        .set_process_sha256(["0123456789ABCDEF0123456789ABCDEF"]).set_reputations(["SUSPECT_MALWARE"]) \
        .set_tags(["Frood"]).set_target_priorities(["HIGH"]).set_threat_ids(["B0RG"]) \
        .set_workflows(["OPEN"]).set_external_device_friendly_names(["/dev/ice"]).set_external_device_ids(["626"]) \
        .set_product_ids(["0x5581"]).set_product_names(["Ultra"]).set_serial_numbers(["4C531001331122115172"]) \
        .set_vendor_ids(["0x0781"]).set_vendor_names(["SanDisk"]).sort_by("name", "DESC")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_devicecontrolalert_facets(cbcsdk_mock):
    """Test a Device Control alert facet query."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "criteria": {'type': ['DEVICE_CONTROL'], "workflow": ["OPEN"]},
                        "terms": {"rows": 0, "fields": ["REPUTATION", "STATUS"]}}
        return {"results": [{"field": {},
                             "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                            {"field": {},
                             "values": [{"id": "status", "name": "statusX", "total": 9}]}]}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_facet", on_post)
    api = cbcsdk_mock.api

    query = api.select(DeviceControlAlert).where("Blort").set_workflows(["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
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
def test_query_devicecontrolalert_invalid_criteria_values(cb, method, arg):
    """Test invalid values being supplied to DeviceControl alert queries."""
    query = cb.select(DeviceControlAlert)
    meth = getattr(query, method, None)
    with pytest.raises(ApiError):
        meth(arg)


def test_query_watchlistalert_with_all_bells_and_whistles(cbcsdk_mock):
    """Test a watchlist alert query with all options selected."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"device_id": [6023], "device_name": ["HAL"],
                                     "device_os": ["LINUX"], "device_os_version": ["0.1.2"],
                                     "device_username": ["JRN"], "id": ["S0L0"],
                                     "legacy_alert_id": ["S0L0_1"], "minimum_severity": 6, "policy_id": [8675309],
                                     "policy_name": ["Strict"], "process_name": ["IEXPLORE.EXE"],
                                     "process_sha256": ["0123456789ABCDEF0123456789ABCDEF"],
                                     "reputation": ["SUSPECT_MALWARE"], "tag": ["Frood"], "target_value": ["HIGH"],
                                     "threat_id": ["B0RG"], "type": ["WATCHLIST"], "workflow": ["OPEN"],
                                     "watchlist_id": ["100"], "watchlist_name": ["Gandalf"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(WatchlistAlert).where("Blort").set_device_ids([6023]) \
        .set_device_names(["HAL"]).set_device_os(["LINUX"]).set_device_os_versions(["0.1.2"]) \
        .set_device_username(["JRN"]).set_alert_ids(["S0L0"]) \
        .set_legacy_alert_ids(["S0L0_1"]).set_minimum_severity(6).set_policy_ids([8675309]) \
        .set_policy_names(["Strict"]).set_process_names(["IEXPLORE.EXE"]) \
        .set_process_sha256(["0123456789ABCDEF0123456789ABCDEF"]).set_reputations(["SUSPECT_MALWARE"]) \
        .set_tags(["Frood"]).set_target_priorities(["HIGH"]).set_threat_ids(["B0RG"]) \
        .set_workflows(["OPEN"]).set_watchlist_ids(["100"]).set_watchlist_names(["Gandalf"]).sort_by("name", "DESC")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


def test_query_watchlistalert_facets(cbcsdk_mock):
    """Test a watchlist alert facet query."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort", "criteria": {'type': ['WATCHLIST'], "workflow": ["OPEN"]},
                        "terms": {"rows": 0, "fields": ["REPUTATION", "STATUS"]}}
        return {"results": [{"field": {},
                             "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                            {"field": {},
                             "values": [{"id": "status", "name": "statusX", "total": 9}]}]}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_facet", on_post)
    api = cbcsdk_mock.api

    query = api.select(WatchlistAlert).where("Blort").set_workflows(["OPEN"])
    f = query.facets(["REPUTATION", "STATUS"])
    assert f == [{"field": {}, "values": [{"id": "reputation", "name": "reputationX", "total": 4}]},
                 {"field": {}, "values": [{"id": "status", "name": "statusX", "total": 9}]}]


def test_query_watchlistalert_invalid_criteria_values(cb):
    """Test error messages for invalid watchlist alert criteria values."""
    with pytest.raises(ApiError):
        cb.select(WatchlistAlert).set_watchlist_ids([888])
    with pytest.raises(ApiError):
        cb.select(WatchlistAlert).set_watchlist_names([69])


def test_query_containeralert_with_all_bells_and_whistles(cbcsdk_mock):
    """Test a container alert query with all options selected."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 2,
                        "criteria": {"cluster_name": ["TURTLE"], 'type': ['CONTAINER_RUNTIME'], "namespace": ["RG"],
                                     "workload_id": ["1234"], "workload_name": ["BUNNY"], "replica_id": ["FAKE"],
                                     "remote_ip": ["10.29.99.1"], "remote_domain": ["example.com"], "protocol": ["TCP"],
                                     "port": [12345], "egress_group_id": ["5150"], "egress_group_name": ["EGRET"],
                                     "ip_reputation": [75], "rule_id": ["66"], "rule_name": ["KITTEH"],
                                     "workload_kind": ["Job"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(ContainerRuntimeAlert).where("Blort").set_cluster_names(['TURTLE']).set_namespaces(['RG']) \
        .set_workload_kinds(['Job']).set_workload_ids(['1234']).set_workload_names(['BUNNY']) \
        .set_replica_ids(['FAKE']).set_remote_ips(['10.29.99.1']).set_remote_domains(['example.com']) \
        .set_protocols(['TCP']).set_ports([12345]).set_egress_group_ids(['5150']).set_egress_group_names(['EGRET']) \
        .set_ip_reputations([75]).set_rule_ids(['66']).set_rule_names(['KITTEH']).sort_by("name", "DESC")
    a = query.one()
    assert a.id == "S0L0"
    assert a.org_key == "test"
    assert a.threat_id == "B0RG"
    assert a.workflow_.state == "OPEN"


@pytest.mark.parametrize("method, arg", [
    ("set_cluster_names", [12345]),
    ("set_namespaces", [12345]),
    ("set_workload_kinds", [12345]),
    ("set_workload_ids", [12345]),
    ("set_workload_names", [12345]),
    ("set_replica_ids", [12345]),
    ("set_remote_ips", [12345]),
    ("set_remote_domains", [12345]),
    ("set_protocols", [12345]),
    ("set_ports", ["BLACKWATER"]),
    ("set_egress_group_ids", [12345]),
    ("set_egress_group_names", [12345]),
    ("set_ip_reputations", ["BLACKWATER"]),
    ("set_rule_ids", [12345]),
    ("set_rule_names", [12345])
])
def test_query_containeralert_invalid_criteria_values(cb, method, arg):
    """Test invalid values being supplied to DeviceControl alert queries."""
    query = cb.select(ContainerRuntimeAlert)
    meth = getattr(query, method, None)
    with pytest.raises(ApiError):
        meth(arg)


def test_query_set_rows(cbcsdk_mock):
    """Test alert query with set rows."""

    def on_post(url, body, **kwargs):
        assert body == {"query": "Blort",
                        "rows": 10000,
                        "start": 1,
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": "S0L0", "org_key": "test", "threat_id": "B0RG",
                             "workflow": {"state": "OPEN"}}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/_search", on_post)
    api = cbcsdk_mock.api

    query = api.select(BaseAlert).where("Blort").sort_by("name", "DESC").set_rows(10000)
    for a in query:
        assert a.id == "S0L0"
        assert a.org_key == "test"
        assert a.threat_id == "B0RG"


# TODO replace bulk tests
# def test_alerts_bulk_dismiss(cbcsdk_mock):
#     """Test dismissing a batch of alerts."""
#
#     def on_post(url, body, **kwargs):
#         assert body == {"query": "Blort", "state": "DISMISSED", "remediation_state": "Fixed", "comment": "Yessir",
#                         "criteria": {"device_name": ["HAL9000"]}}
#         return {"request_id": "497ABX"}
#
#     cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/workflow", on_post)
#     api = cbcsdk_mock.api
#
#     q = api.select(BaseAlert).where("Blort").set_device_names(["HAL9000"])
#     reqid = q.dismiss("Fixed", "Yessir")
#     assert reqid == "497ABX"
#

# def test_alerts_bulk_undismiss(cbcsdk_mock):
#     """Test undismissing a batch of alerts."""
#
#     def on_post(url, body, **kwargs):
#         assert body == {"query": "Blort", "state": "OPEN", "remediation_state": "Fixed", "comment": "NoSir",
#                         "criteria": {"device_name": ["HAL9000"]}}
#         return {"request_id": "497ABX"}
#
#     cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/workflow", on_post)
#     api = cbcsdk_mock.api
#
#     q = api.select(BaseAlert).where("Blort").set_device_names(["HAL9000"])
#     reqid = q.update("Fixed", "NoSir")
#     assert reqid == "497ABX"
#
#
# def test_alerts_bulk_dismiss_watchlist(cbcsdk_mock):
#     """Test dismissing a batch of watchlist alerts."""
#
#     def on_post(url, body, **kwargs):
#         assert body == {"query": "Blort", "state": "DISMISSED", "remediation_state": "Fixed", "comment": "Yessir",
#                         "criteria": {"device_name": ["HAL9000"], 'type': ['WATCHLIST']}}
#         return {"request_id": "497ABX"}
#
#     cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/workflow", on_post)
#     api = cbcsdk_mock.api
#
#     q = api.select(WatchlistAlert).where("Blort").set_device_names(["HAL9000"])
#     reqid = q.dismiss("Fixed", "Yessir")
#     assert reqid == "497ABX"
#
#
# def test_alerts_bulk_dismiss_cbanalytics(cbcsdk_mock):
#     """Test dismissing a batch of CB Analytics alerts."""
#
#     def on_post(url, body, **kwargs):
#         assert body == {"query": "Blort", "state": "DISMISSED", "remediation_state": "Fixed", "comment": "Yessir",
#                         "criteria": {"device_name": ["HAL9000"], 'type': ['CB_ANALYTICS']}}
#         return {"request_id": "497ABX"}
#
#     cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/workflow", on_post)
#     api = cbcsdk_mock.api
#
#     q = api.select(CBAnalyticsAlert).where("Blort").set_device_names(["HAL9000"])
#     reqid = q.dismiss("Fixed", "Yessir")
#     assert reqid == "497ABX"
#
#
# def test_alerts_bulk_dismiss_threat(cbcsdk_mock):
#     """Test dismissing a batch of threat alerts."""
#
#     def on_post(url, body, **kwargs):
#         assert body == {"threat_id": ["B0RG", "F3R3NG1"], "state": "DISMISSED", "remediation_state": "Fixed",
#                         "comment": "Yessir"}
#         return {"request_id": "497ABX"}
#
#     cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/workflow", on_post)
#     api = cbcsdk_mock.api
#
#     reqid = api.bulk_threat_dismiss(["B0RG", "F3R3NG1"], "Fixed", "Yessir")
#     assert reqid == "497ABX"
#
#
# def test_alerts_bulk_undismiss_threat(cbcsdk_mock):
#     """Test undismissing a batch of threat alerts."""
#
#     def on_post(url, body, **kwargs):
#         assert body == {"threat_id": ["B0RG", "F3R3NG1"], "state": "OPEN", "remediation_state": "Fixed",
#                         "comment": "NoSir"}
#         return {"request_id": "497ABX"}
#
#     cbcsdk_mock.mock_request('POST', "/api/alerts/v7/orgs/test/alerts/workflow", on_post)
#     api = cbcsdk_mock.api
#
#     reqid = api.bulk_threat_update(["B0RG", "F3R3NG1"], "Fixed", "NoSir")
#     assert reqid == "497ABX"
#
#
# def test_alerts_bulk_threat_error(cb):
#     """Test error raise from bulk threat update status"""
#     with pytest.raises(ApiError):
#         cb.bulk_threat_dismiss([123], "Fixed", "Yessir")

# TODO rework workflow tests after workflow updated
# def test_load_workflow(cbcsdk_mock):
#     """Test loading a workflow status."""
#     cbcsdk_mock.mock_request('GET', "/api/alerts/v7/orgs/test/workflow/497ABX",
#                              {"errors": [], "failed_ids": [], "id": "497ABX", "num_hits": 0, "num_success": 0,
#                               "status": "QUEUED", "workflow": {"state": "DISMISSED", "remediation": "Fixed",
#                                                                "comment": "Yessir", "changed_by": "Robocop",
#                                                                "last_update_time": "2019-10-31T16:03:13.951Z"}})
#     api = cbcsdk_mock.api
#
#     workflow = api.select(WorkflowStatus, "497ABX")
#     assert workflow.id_ == "497ABX"


def test_get_process(cbcsdk_mock):
    """Test of getting process through a WatchlistAlert"""
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6b2348cb-87c1-4076-bc8e-7c717e8af608",
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
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_WATCHLIST_ALERT)
    # mock the POST of a summary search (using same Job ID)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/summary_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
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
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_TYPE_WATCHLIST)
    # mock the search validation
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_validation",
                             POST_PROCESS_VALIDATION_RESP)
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
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6b2348cb-87c1-4076-bc8e-7c717e8af608",
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
        alert = api.select(WatchlistAlert, "6b2348cb-87c1-4076-bc8e-7c717e8af608")
        alert.get_process()


def test_get_process_async(cbcsdk_mock):
    """Test of getting process through a WatchlistAlert async"""
    # mock the alert request
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6b2348cb-87c1-4076-bc8e-7c717e8af608",
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
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_WATCHLIST_ALERT)
    # mock the POST of a summary search (using same Job ID)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/summary_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
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
                             "/api/alerts/v7/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56"
                             "-8741e929e48b",
                             # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56"
                             "-8741e929e48b/results",
                             # noqa: E501
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
                             "/api/alerts/v7/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56"
                             "-8741e929e48b",
                             # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56"
                             "-8741e929e48b/results",
                             # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_ZERO)

    api = cbcsdk_mock.api
    alert = api.select(CBAnalyticsAlert, '86123310980efd0b38111eba4bfa5e98aa30b19')
    events = alert.get_events()
    assert len(events) == 0


def test_get_events_timeout(cbcsdk_mock):
    """Test that get_events() throws a timeout appropriately."""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56"
                             "-8741e929e48b",
                             # noqa: E501
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
                             "/api/alerts/v7/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56"
                             "-8741e929e48b",
                             # noqa: E501
                             get_validate)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56"
                             "-8741e929e48b/results",
                             # noqa: E501
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
                             "/api/alerts/v7/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP_INVALID_ALERT_ID)

    api = cbcsdk_mock.api
    alert = api.select(CBAnalyticsAlert, '86123310980efd0b38111eba4bfa5e98aa30b19')
    with pytest.raises(ApiError):
        alert.get_events()


def test_get_events_async(cbcsdk_mock):
    """Test async get_events method"""
    cbcsdk_mock.mock_request("GET",
                             "/api/alerts/v7/orgs/test/alerts/86123310980efd0b38111eba4bfa5e98aa30b19",
                             GET_ALERT_RESP)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56"
                             "-8741e929e48b",
                             # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56"
                             "-8741e929e48b/results",
                             # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_ALERTS)

    api = cbcsdk_mock.api
    alert = api.select(CBAnalyticsAlert, '86123310980efd0b38111eba4bfa5e98aa30b19')
    events = alert.get_events(async_mode=True).result()
    assert len(events) == 2
    for event in events:
        assert event.alert_id == ['62802DCE']


def test_query_basealert_with_time_range_errors(cbcsdk_mock):
    """Test exceptions in alert query"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError) as ex:
        api.select(BaseAlert).where("Blort").set_time_range("invalid", range="whatever")
    assert "key must be one of create_time, first_event_time, last_event_time, backend_timestamp, " \
           "backend_update_timestamp, or last_update_time" in str(ex.value)

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


def test_get_notes_for_alert(cbcsdk_mock):
    """Test retrieving notes for an alert"""
    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/1ba0c35f-9c01-4413-afd8-fe4f01365e35",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/1ba0c35f-9c01-4413-afd8-fe4f01365e35/notes",
                             GET_ALERT_NOTES)

    api = cbcsdk_mock.api
    alert = api.select(BaseAlert, "1ba0c35f-9c01-4413-afd8-fe4f01365e35")
    notes = alert.notes_()
    assert len(notes) == 2
    assert notes[0].author == "Grogu"
    assert notes[0].id == "1"
    assert notes[0].create_time == "2021-05-13T00:20:46.474Z"
    assert notes[0].note == "I am a note"


def test_base_alert_create_note(cbcsdk_mock):
    """Test creating a new note on an alert"""

    def on_post(url, body, **kwargs):
        body == {"note": "I am Grogu"}
        return CREATE_ALERT_NOTE

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/1ba0c35f-9c01-4413-afd8-fe4f01365e35",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('POST',
                             "/api/alerts/v7/orgs/test/alerts/1ba0c35f-9c01-4413-afd8-fe4f01365e35/notes",
                             on_post)

    api = cbcsdk_mock.api
    alert = api.select(BaseAlert, "1ba0c35f-9c01-4413-afd8-fe4f01365e35")
    note = alert.create_note("I am Grogu")
    assert note[0].note == "I am Grogu"


def test_base_alert_delete_note(cbcsdk_mock):
    """Test deleting a note from an alert"""
    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/1ba0c35f-9c01-4413-afd8-fe4f01365e35",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/1ba0c35f-9c01-4413-afd8-fe4f01365e35/notes",
                             GET_ALERT_NOTES)

    cbcsdk_mock.mock_request('DELETE',
                             "/api/alerts/v7/orgs/test/alerts/1ba0c35f-9c01-4413-afd8-fe4f01365e35/notes/1",
                             None)

    api = cbcsdk_mock.api
    alert = api.select(BaseAlert, "1ba0c35f-9c01-4413-afd8-fe4f01365e35")
    notes = alert.notes_()
    notes[0].delete()
    assert notes[0]._is_deleted


def test_base_alert_unsupported_query_notes(cbcsdk_mock):
    """Testing that error is thrown when querying notes directly"""
    with pytest.raises(NonQueryableModel):
        api = cbcsdk_mock.api
        api.select(BaseAlert.Note)


def test_base_alert_refresh_note(cbcsdk_mock):
    """Testing single note refresh"""
    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/1ba0c35f-9c01-4413-afd8-fe4f01365e35",
                             GET_ALERT_RESP_WITH_NOTES)

    cbcsdk_mock.mock_request('GET',
                             "/api/alerts/v7/orgs/test/alerts/1ba0c35f-9c01-4413-afd8-fe4f01365e35/notes",
                             GET_ALERT_NOTES)

    api = cbcsdk_mock.api
    alert = api.select(BaseAlert, "1ba0c35f-9c01-4413-afd8-fe4f01365e35")
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
    result = BaseAlert.search_suggestions(api, "")
    assert len(result) == 20


def test_alert_search_suggestions_api_error():
    """Tests getting alert search suggestions - no CBCloudAPI arg"""
    with pytest.raises(ApiError):
        BaseAlert.search_suggestions("", "")
