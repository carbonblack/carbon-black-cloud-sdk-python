"""Testing Audit and Remediation."""

import pytest
import logging
from cbc_sdk.audit_remediation import Run, Result, ResultQuery, DeviceSummary, ResultFacet, RunHistoryQuery, RunHistory
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ServerError, ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.audit_remediation.mock_runs import (GET_RUN_RESP,
                                                             GET_RUN_RESULTS_RESP,
                                                             GET_RUN_RESULTS_RESP_1,
                                                             GET_RUN_RESULTS_RESP_2,
                                                             GET_RUN_RESULTS_RESP_3,
                                                             GET_DEVICE_SUMMARY_RESP_1,
                                                             GET_RESULTS_FACETS_RESP,
                                                             POST_RUN_HISTORY_RESP)

log = logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, filename='log.txt')


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

def test_run_stop_exception(cbcsdk_mock):
    """Testing Run.stop() when response from server is not JSON parsable."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/livequery/v1/orgs/test/runs/run_id", GET_RUN_RESP)
    unparsable_response = CBCSDKMock.StubResponse(contents="ThisIsntJSONParsable", scode=200, json_parsable=False)
    cbcsdk_mock.mock_request("PUT", "/livequery/v1/orgs/test/runs/run_id/status", unparsable_response)
    assert unparsable_response._json_parsable is False
    run = Run(api, model_unique_id="run_id")
    with pytest.raises(ServerError):
        run.stop()


def test_result_query_implementation(cbcsdk_mock):
    """Testing Run._query_implementation()."""
    api = cbcsdk_mock.api
    result = Result(api, initial_data=GET_RUN_RESULTS_RESP)
    assert isinstance(result._query_implementation(api), ResultQuery)


def test_result_device(cbcsdk_mock):
    """Testing Result.device_ property."""
    api = cbcsdk_mock.api
    result = Result(api, initial_data=GET_RUN_RESULTS_RESP)
    device = result.device_
    assert isinstance(device, Result.Device)
    assert device._info == GET_RUN_RESULTS_RESP["device"]
    assert device.id == 1234567
    assert device.name == "WIN-A1B2C3D4"


def test_result_fields(cbcsdk_mock):
    """Testing Result.fields_ property."""
    api = cbcsdk_mock.api
    result = Result(api, initial_data=GET_RUN_RESULTS_RESP)
    fields = result.fields_
    assert fields._info == {"status", "device.id"}
    metrics = result.metrics_
    assert isinstance(metrics, Result.Metrics)
    assert metrics._info == {}


def test_result_fields_with_metrics(cbcsdk_mock):
    """Testing Result.metrics_ property with Device Summary results."""
    api = cbcsdk_mock.api
    result = Result(api, initial_data=GET_RUN_RESULTS_RESP_1)
    metrics = result.metrics_
    assert metrics._info == {"cpu": 24.3, "memory": 8.0}


def test_result_query_criteria(cbcsdk_mock):
    """Testing set_* criteria methods for ResultQuery."""
    api = cbcsdk_mock.api
    result_q = api.select(Result).run_id(1).set_device_os(["WINDOWS"]).set_device_ids([1, 2, 3])\
        .set_device_names(["Win7x64", "Win10"]).set_policy_ids([1, 2]).set_policy_names(["default", "policy2"])\
        .set_statuses(["not_started", "matched"])
    assert result_q._build_request(start=0, rows=100) == {"criteria": {
        "device.os": ["WINDOWS"],
        "device.id": [1, 2, 3],
        "device.name": ["Win7x64", "Win10"],
        "device.policy_id": [1, 2],
        "device.policy_name": ["default", "policy2"],
        "status": ["not_started", "matched"]
    }, "start": 0, "rows": 100, "query": "*:*"}


def test_result_query_update_criteria(cbcsdk_mock):
    """Testing the public update_criteria() function accessing private _update_criteria()."""
    api = cbcsdk_mock.api
    query = api.select(Result).run_id(2).update_criteria("my.key.dot.notation", ["criteria_val_1", "criteria_val_2"])
    assert query._build_request(start=0, rows=100) == {"criteria": {
        "my.key.dot.notation": ["criteria_val_1", "criteria_val_2"]
    }, "start": 0, "rows": 100, "query": "*:*"}


def test_facet_query_criteria(cbcsdk_mock):
    """Testing set_* criteria for FacetQuery."""
    api = cbcsdk_mock.api
    facet_q = api.select(ResultFacet).run_id(1).set_device_os(["WINDOWS"]).set_device_ids([1,2,3])\
                .set_device_names(["Win7x64", "Win10"]).set_policy_ids([1,2]).set_policy_names(["default", "policy2"])\
                .set_statuses(["not_started", "matched"])
    assert facet_q._build_request(rows=100) == {"criteria": {
        "device.os": ["WINDOWS"],
        "device.id": [1,2,3],
        "device.name": ["Win7x64", "Win10"],
        "device.policy_id": [1,2],
        "device.policy_name": ["default", "policy2"],
        "status": ["not_started", "matched"]
    }, "query": "*:*", "terms": {"fields": [], "rows": 100}}


def test_result_facet_query_update_criteria(cbcsdk_mock):
    """Testing the public update_criteria() function accessing private _update_criteria()."""
    api = cbcsdk_mock.api
    query = api.select(ResultFacet).run_id(2).update_criteria("my.key.dot.notation", ["criteria_val_1", "criteria_val_2"])
    assert query._build_request(rows=100) == {"criteria": {
        "my.key.dot.notation": ["criteria_val_1", "criteria_val_2"]
    }, "query": "*:*", "terms": {"fields": [], "rows": 100}}


def test_device_summary_metrics(cbcsdk_mock):
    """Testing DeviceSummary.metrics_ property."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/run_id/results/_search", GET_RUN_RESULTS_RESP_2)
    results = api.select(Result).run_id("run_id")
    res0 = results.first()
    summaries = res0.query_device_summaries()
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/run_id/results/device_summaries/_search", GET_DEVICE_SUMMARY_RESP_1)
    for summary in summaries:
        metrics = summary.metrics_
        assert isinstance(metrics, DeviceSummary.Metrics)
        assert isinstance(summary, DeviceSummary)
        assert isinstance(metrics.total_cpu_peak, float)
        assert "average_system_memory_in_use" in metrics._info


def test_result_facet_values(cbcsdk_mock):
    """Testing ResultFacet.values_ property."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/run_id/results/_search", GET_RUN_RESULTS_RESP_2)
    results = api.select(Result).run_id("run_id")
    res0 = results.first()
    facets = res0.query_result_facets()
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/run_id/results/_facet", GET_RESULTS_FACETS_RESP)
    for facet in facets:
        assert isinstance(facet, ResultFacet)
        assert facet.field == "device.policy_id"
        assert facet.values_._info == [{'id': 'idOfFieldBeingEnumerated', 'name': 'policyId1', 'total': 1}]


def test_run_query_submit_exceptions(cbcsdk_mock):
    """Testing RunQuery.submit() raising ApiError."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/livequery/v1/orgs/test/runs/run_id", GET_RUN_RESP)
    run_query = api.select(Run).where("SELECT path, DATETIME(atime,\"unixepoch\",\"localtime\") AS \"Last Accessed\", DATETIME(mtime,\"unixepoch\",\"localtime\") AS \"Last Modified\", DATETIME(ctime,\"unixepoch\",\"localtime\") AS \"Created\" FROM file WHERE path LIKE \"\\users\\%\\AppData\\%.exe\";")
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs", GET_RUN_RESP)
    result = run_query.submit()
    assert run_query._query_token is not None
    # raise ApiError when the query has already been submitted
    with pytest.raises(ApiError):
        run_query.submit()
    assert result.status == "COMPLETE"
    # raise ApiError when the query is missing SQL to run
    new_query = api.select(Run).name("myRunName")
    with pytest.raises(ApiError):
        new_query.submit()


def test_run_history_query_build_request(cbcsdk_mock):
    """Testing RunHistoryQuery._build_request() rows."""
    api = cbcsdk_mock.api
    run_history_query = api.select(RunHistory).where("SELECT path FROM file;")
    request = run_history_query._build_request(start=0, rows=1)
    assert request["rows"] == 1


def test_run_history_query_count(cbcsdk_mock):
    """Testing RunHistoryQuery._count()."""
    api = cbcsdk_mock.api
    run_history_query = api.select(RunHistory).where("SELECT path FROM file;")
    assert run_history_query._count_valid is False
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/_search", POST_RUN_HISTORY_RESP)
    num_results = run_history_query._count()
    assert run_history_query._count_valid is True
    assert num_results == 7
    assert run_history_query._count() == run_history_query._total_results


def test_result_query_build_request(cbcsdk_mock):
    """Testing Result._build_request() rows."""
    api = cbcsdk_mock.api
    result_query = api.select(Result).where("deviceId:12345")
    request = result_query._build_request(start=0, rows=1)
    assert request["rows"] == 1


def test_result_query_count(cbcsdk_mock):
    """Testing Result._count()."""
    api = cbcsdk_mock.api
    # result_query = api.select(Result).criteria(username="foo")
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/run_id/results/_search", GET_RUN_RESULTS_RESP_2)
    result_query = api.select(Result).run_id("run_id")
    assert result_query._count_valid is False
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/_search", POST_RUN_HISTORY_RESP)
    num_results = result_query._count()
    assert result_query._count_valid is True
    assert num_results == 6
    assert result_query._count() == result_query._total_results


def test_result_query_no_run_id_exception(cbcsdk_mock):
    """Testing Result._count() and ._perform_query() raising ApiError when a run_id is not supplied."""
    api = cbcsdk_mock.api
    result_query = api.select(Result)
    # raise ApiError when missing run_id (from the select statement)
    with pytest.raises(ApiError):
        result_query._count()
    assert result_query._run_id is None
    with pytest.raises(ApiError):
        results = [res for res in result_query._perform_query()]
