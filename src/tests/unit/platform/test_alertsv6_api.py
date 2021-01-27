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

"""Tests of the Alerts V6 API queries."""

import pytest
from cbc_sdk.errors import ApiError
from cbc_sdk.platform import BaseAlert, CBAnalyticsAlert, WatchlistAlert, WorkflowStatus
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.stubresponse import StubResponse, patch_cbc_sdk_api


def test_query_basealert_with_all_bells_and_whistles(monkeypatch):
    """Test an alert query with all options selected."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/_search"
        assert body == {"query": "Blort",
                        "rows": 100,
                        "criteria": {"category": ["SERIOUS", "CRITICAL"], "device_id": [6023], "device_name": ["HAL"],
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
    query = api.select(BaseAlert).where("Blort").set_categories(["SERIOUS", "CRITICAL"]).set_device_ids([6023]) \
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
                        "rows": 100,
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


def test_query_basealert_with_create_time_as_range(monkeypatch):
    """Test an alert query with the creation time specified as a range."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/_search"
        assert body == {"query": "Blort", "criteria": {"create_time": {"range": "-3w"}},
                        "rows": 100}
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

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/_search"
        assert body == {"query": "Blort", "criteria": {"last_update_time": {"range": "-3w"}},
                        "rows": 100}
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
    ("set_categories", ["DOUBLE_DARE"]),
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
                        "rows": 100,
                        "criteria": {"category": ["SERIOUS", "CRITICAL"], "device_id": [6023], "device_name": ["HAL"],
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
    query = api.select(CBAnalyticsAlert).where("Blort").set_categories(["SERIOUS", "CRITICAL"]) \
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


def test_query_watchlistalert_with_all_bells_and_whistles(monkeypatch):
    """Test a watchlist alert query with all options selected."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/watchlist/_search"
        assert body == {"query": "Blort",
                        "rows": 100,
                        "criteria": {"category": ["SERIOUS", "CRITICAL"], "device_id": [6023], "device_name": ["HAL"],
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
    query = api.select(WatchlistAlert).where("Blort").set_categories(["SERIOUS", "CRITICAL"]).set_device_ids([6023]) \
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
