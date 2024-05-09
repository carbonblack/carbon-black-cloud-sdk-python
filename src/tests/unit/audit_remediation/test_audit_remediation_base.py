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

"""Testing Audit and Remediation."""

import pytest
import logging
import io
import os
from contextlib import ExitStack as does_not_raise
from tempfile import mkstemp
from cbc_sdk.audit_remediation import Run, Result, Template, ResultQuery, DeviceSummary, ResultFacet, RunHistory
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ServerError, ApiError, TimeoutError, OperationCancelled
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.audit_remediation.mock_runs import (GET_RUN_RESP, GET_RUN_RESULTS_RESP, GET_RUN_RESULTS_RESP_1,
                                                             GET_RUN_RESULTS_RESP_2, GET_DEVICE_SUMMARY_RESP_1,
                                                             GET_RESULTS_FACETS_RESP, POST_RUN_HISTORY_RESP,
                                                             GET_RUN_RESULTS_RESP_OVER_10k, ASYNC_START_QUERY,
                                                             ASYNC_GET_QUERY_1, ASYNC_GET_QUERY_2, ASYNC_GET_RESULTS,
                                                             ASYNC_BROKEN_1, ASYNC_BROKEN_2, ASYNC_BROKEN_3,
                                                             ASYNC_FACETING)
from tests.unit.fixtures.platform.mock_jobs import JOB_DETAILS_1
from tests.unit.fixtures.audit_remediation.mock_scroll import GET_SCROLL_RESULTS, SINGLE_RESULT


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


def new_tempfile():
    """Create a temporary file and return the name of it."""
    rc = mkstemp()
    os.close(rc[0])
    return rc[1]


def file_contents(filename):
    """Return a string containing the contents of the file."""
    with io.open(filename, "r", encoding="utf-8") as f:
        return f.read()


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
    run = Run(api, "1", {"org_key": "test", "name": "FoobieBletch", "id": "1", "status": "COMPLETE"})
    result_q = run.query_results().set_device_os(["WINDOWS"]).set_device_ids([1, 2, 3]) \
        .set_device_names(["Win7x64", "Win10"]).set_policy_ids([1, 2]).set_policy_names(["default", "policy2"]) \
        .set_statuses(["not_started", "matched"])
    assert result_q._run_id == "1"
    assert result_q._build_request(start=0, rows=100) == {"criteria": {
        "device.os": ["WINDOWS"],
        "device.id": [1, 2, 3],
        "device.name": ["Win7x64", "Win10"],
        "device.policy_id": [1, 2],
        "device.policy_name": ["default", "policy2"],
        "status": ["not_started", "matched"]
    }, "start": 0, "rows": 100}


def test_result_query_update_criteria(cbcsdk_mock):
    """Testing the public update_criteria() function accessing private _update_criteria()."""
    api = cbcsdk_mock.api
    query = api.select(Result).run_id("qcu6wghci1oqfrsgvcrrm1o71bzcy7cx") \
                              .update_criteria("my.key.dot.notation", ["criteria_val_1"])
    query = query.update_criteria("my.key.dot.notation", ["criteria_val_2"])
    assert query._build_request(start=0, rows=100) == {"criteria": {
        "my.key.dot.notation": ["criteria_val_1", "criteria_val_2"]
    }, "start": 0, "rows": 100}


def test_facet_query_criteria(cbcsdk_mock):
    """Testing set_* criteria for FacetQuery."""
    api = cbcsdk_mock.api
    run = Run(api, "1", {"org_key": "test", "name": "FoobieBletch", "id": "1", "status": "COMPLETE"})
    facet_q = run.query_facets().set_device_os(["WINDOWS"]).set_device_ids([1, 2, 3]) \
        .set_device_names(["Win7x64", "Win10"]).set_policy_ids([1, 2]).set_policy_names(["default", "policy2"]) \
        .set_statuses(["not_started", "matched"])
    assert facet_q._run_id == "1"
    assert facet_q._build_request(rows=100) == {"criteria": {
        "device.os": ["WINDOWS"],
        "device.id": [1, 2, 3],
        "device.name": ["Win7x64", "Win10"],
        "device.policy_id": [1, 2],
        "device.policy_name": ["default", "policy2"],
        "status": ["not_started", "matched"]
    }, "terms": {"fields": [], "rows": 100}}


def test_result_facet_query_update_criteria(cbcsdk_mock):
    """Testing the public update_criteria() function accessing private _update_criteria()."""
    api = cbcsdk_mock.api
    query = api.select(ResultFacet).run_id("qcu6wghci1oqfrsgvcrrm1o71bzcy7cx") \
                                   .update_criteria("my.key.dot.notation", ["criteria_val_1", "criteria_val_2"])
    assert query._build_request(rows=100) == {"criteria": {
        "my.key.dot.notation": ["criteria_val_1", "criteria_val_2"]
    }, "terms": {"fields": [], "rows": 100}}


def test_device_summary_metrics(cbcsdk_mock):
    """Testing DeviceSummary.metrics_ property."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/run_id/results/_search", GET_RUN_RESULTS_RESP_2)
    results = api.select(Result).run_id("run_id")
    res0 = results.first()
    summaries = res0.query_device_summaries()
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/run_id/results/device_summaries/_search",
                             GET_DEVICE_SUMMARY_RESP_1)
    for summary in summaries:
        metrics = summary.metrics_
        assert isinstance(metrics, DeviceSummary.Metrics)
        assert isinstance(summary, DeviceSummary)
        assert isinstance(metrics.total_cpu_peak, float)
        assert "average_system_memory_in_use" in metrics._info


def test_device_summary_metrics_alternate_route(cbcsdk_mock):
    """Testing getting device summaries through Run."""
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/run_id/results/device_summaries/_search",
                             GET_DEVICE_SUMMARY_RESP_1)
    api = cbcsdk_mock.api
    run = Run(api, "run_id", {"org_key": "test", "name": "FoobieBletch", "id": "run_id", "status": "COMPLETE"})
    summaries = run.query_device_summaries()
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
    run_query = api.select(Run).where(
        "SELECT path, DATETIME(atime,\"unixepoch\",\"localtime\") AS \"Last Accessed\", "
        "DATETIME(mtime,\"unixepoch\",\"localtime\") AS \"Last Modified\", "
        "DATETIME(ctime,\"unixepoch\",\"localtime\") AS \"Created\" FROM file "
        "WHERE path LIKE \"\\users\\%\\AppData\\%.exe\";")
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


def test_run_history_query_async(cbcsdk_mock):
    """Test RunHistoryQuery running asynchronously."""
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/_search", POST_RUN_HISTORY_RESP)
    api = cbcsdk_mock.api
    run_history_query = api.select(RunHistory).where("SELECT path FROM file;")
    future = run_history_query.execute_async()
    result = future.result()
    assert len(result) == 7


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


def test_result_query_async(cbcsdk_mock):
    """Testing ResultQuery running asynchronously."""
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/run_id/results/_search", GET_RUN_RESULTS_RESP_2)
    api = cbcsdk_mock.api
    result_query = api.select(Result).run_id("run_id")
    future = result_query.execute_async()
    result = future.result()
    assert len(result) == 6


def test_result_query_export_string(cbcsdk_mock):
    """Tests exporting the results of a query as a string."""
    cbcsdk_mock.mock_request("STREAM:POST", "/livequery/v1/orgs/test/runs/run_id/results/_search?format=csv",
                             CBCSDKMock.StubResponse("ThisIsFine", 200, "ThisIsFine", False))
    api = cbcsdk_mock.api
    result_query = api.select(Result).run_id("run_id")
    output = result_query.export_csv_as_string()
    assert output == "ThisIsFine"


def test_result_query_export_file(cbcsdk_mock):
    """Tests exporting the results of a query as a file."""
    cbcsdk_mock.mock_request("STREAM:POST", "/livequery/v1/orgs/test/runs/run_id/results/_search?format=csv",
                             CBCSDKMock.StubResponse("ThisIsFine", 200, "ThisIsFine", False))
    api = cbcsdk_mock.api
    result_query = api.select(Result).run_id("run_id")
    tempfile = new_tempfile()
    try:
        result_query.export_csv_as_file(tempfile)
        assert file_contents(tempfile) == "ThisIsFine"
    finally:
        os.remove(tempfile)


@pytest.mark.parametrize("ref_url, func_raises, get_job", [
    ('https://example.com/jobs/v1/orgs/test/jobs/12345', does_not_raise(), True),
    ('https://example.com/jobs/v1/orgs/test/jobs/NOTVALID', pytest.raises(ApiError), False),
    (None, pytest.raises(ApiError), False),
])
def test_result_query_async_export(cbcsdk_mock, ref_url, func_raises, get_job):
    """Tests getting a Job from the SDK to asynchronously export a query's results."""
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/run_id/results/_search?format=csv&async=true",
                             {"ref_url": ref_url})
    if get_job:
        cbcsdk_mock.mock_request('GET', '/jobs/v1/orgs/test/jobs/12345', JOB_DETAILS_1)
    api = cbcsdk_mock.api
    result_query = api.select(Result).run_id("run_id")
    with func_raises:
        job = result_query.async_export()
        assert job.id == 12345
        assert job.status == 'COMPLETED'
        assert job.progress['num_total'] == 18
        assert job.progress['num_completed'] == 18


def test_result_query_export_lines(cbcsdk_mock):
    """Tests exporting the results of a query as a list of lines."""
    input = "AAA\r\nBBB\r\nCCC"
    cbcsdk_mock.mock_request("ITERATE:POST", "/livequery/v1/orgs/test/runs/run_id/results/_search?format=csv",
                             CBCSDKMock.StubResponse(input, 200, input, False))
    api = cbcsdk_mock.api
    result_query = api.select(Result).run_id("run_id")
    output = list(result_query.export_csv_as_lines())
    assert output == ["AAA", "BBB", "CCC"]


def test_result_query_export_zip(cbcsdk_mock):
    """Tests exporting the results of a query as a zip file."""
    cbcsdk_mock.mock_request("STREAM:POST",
                             "/livequery/v1/orgs/test/runs/run_id/results/_search?format=csv&download=true",
                             CBCSDKMock.StubResponse("ThisIsFine", 200, "ThisIsFine", False))
    api = cbcsdk_mock.api
    result_query = api.select(Result).run_id("run_id")
    tempfile = new_tempfile()
    try:
        result_query.export_zipped_csv(tempfile)
        assert file_contents(tempfile) == "ThisIsFine"
    finally:
        os.remove(tempfile)


def test_result_query_exports_fail_without_run_id(cb):
    """Tests that the export methods fail if the run ID is not specified."""
    result_query = cb.select(Result)
    with io.BytesIO() as stream:
        with pytest.raises(ApiError):
            result_query.export_csv_as_stream(stream)
    with pytest.raises(ApiError):
        result_query.export_csv_as_string()
    with pytest.raises(ApiError):
        result_query.export_csv_as_file('blort.txt')
    with pytest.raises(ApiError):
        list(result_query.export_csv_as_lines())
    with pytest.raises(ApiError):
        result_query.export_zipped_csv('blort.zip')
    with pytest.raises(ApiError):
        result_query.async_export()


def test_result_query_no_run_id_exception(cbcsdk_mock):
    """Testing Result._count() and ._perform_query() raising ApiError when a run_id is not supplied."""
    api = cbcsdk_mock.api
    result_query = api.select(Result)
    # raise ApiError when missing run_id (from the select statement)
    with pytest.raises(ApiError):
        result_query._count()
    assert result_query._run_id is None
    results = None
    with pytest.raises(ApiError):
        results = [res for res in result_query._perform_query()]
    assert results is None


def test_result_query_over_10k(cbcsdk_mock):
    """Testing Result._count() and ._perform_query() raising ApiError when a run_id is not supplied."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("POST",
                             "/livequery/v1/orgs/test/runs/run_id/results/_search",
                             GET_RUN_RESULTS_RESP_OVER_10k)
    result_query = api.select(Result).run_id("run_id")

    list(result_query._perform_query())
    assert result_query._total_results == 10000


def test_run_history_criteria(cbcsdk_mock):
    """Testing RunHistory criteria"""
    def _test_request(url, body, **kwargs):
        assert body["template_id"][0] == "TEST_ID"
        assert body["custom"][0] == "values"

    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs//_search", _test_request)
    template = Template(api, "TEST_ID", {"org_key": "test", "name": "FoobieBletch", "id": "TEST_ID",
                                         "status": "COMPLETE"})
    template.query_runs().update_criteria("custom", ["values"])


def test_run_async_query(cbcsdk_mock):
    """Tests running an asynchronous LiveQuery."""
    get_calls = 0

    def on_status_get(url, params, default):
        nonlocal get_calls
        get_calls += 1
        if get_calls >= 3:
            return ASYNC_GET_QUERY_2
        return ASYNC_GET_QUERY_1

    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs", ASYNC_START_QUERY)
    cbcsdk_mock.mock_request("GET", "/livequery/v1/orgs/test/runs/abcdefghijklmnopqrstuvwxyz123456", on_status_get)
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/abcdefghijklmnopqrstuvwxyz123456/results/_search",
                             ASYNC_GET_RESULTS)
    api = cbcsdk_mock.api
    query = api.select(Run).where("SELECT * FROM kernel_info;")
    future = query.execute_async()
    results = future.result()
    assert len(results) == 4
    assert results[0].fields['version'] == "5.11.0-38-generic"
    assert results[1].fields['version'] == "10.0.19041.1288"
    assert results[2].fields['version'] == "17.7.0"
    assert results[3].fields['version'] == "4.14.186-146.268.amzn2.x86_64"


@pytest.mark.parametrize("response, expectation", [
    (ASYNC_BROKEN_1, pytest.raises(TimeoutError)),
    (ASYNC_BROKEN_2, pytest.raises(OperationCancelled)),
    (ASYNC_BROKEN_3, pytest.raises(ApiError))
])
def test_run_async_query_breaks(cbcsdk_mock, response, expectation):
    """Tests running an asynchronous LiveQuery that returns a broken response."""
    get_calls = 0

    def on_status_get(url, params, default):
        nonlocal get_calls
        get_calls += 1
        if get_calls >= 3:
            return response
        return ASYNC_GET_QUERY_1

    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs", ASYNC_START_QUERY)
    cbcsdk_mock.mock_request("GET", "/livequery/v1/orgs/test/runs/abcdefghijklmnopqrstuvwxyz123456", on_status_get)
    api = cbcsdk_mock.api
    query = api.select(Run).where("SELECT * FROM kernel_info;")
    future = query.execute_async()
    with expectation:
        future.result()


def test_run_async_faceting_query(cbcsdk_mock):
    """Tests running a FacetQuery asynchronously."""
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/abcdefghijklmnopqrstuvwxyz123456/results/_facet",
                             ASYNC_FACETING)
    api = cbcsdk_mock.api
    query = api.select(ResultFacet).run_id("abcdefghijklmnopqrstuvwxyz123456").facet_field("fields.version")
    future = query.execute_async()
    result = future.result()
    assert len(result) == 1
    assert result[0].field == 'fields.version'
    assert len(result[0].values) == 4


def test_result_set_run_ids(cbcsdk_mock):
    """Testing set_run_ids"""
    api = cbcsdk_mock.api
    query = api.select(Result).set_run_ids(["abcdefghijklmnopqrstuvwxyz123456", "fckjyssfusuuutlkpocky82luvnl0sol"])
    assert query._criteria["run_id"] == ["abcdefghijklmnopqrstuvwxyz123456", "fckjyssfusuuutlkpocky82luvnl0sol"]


def test_result_set_time_received(cbcsdk_mock):
    """Testing set_time_received"""
    api = cbcsdk_mock.api
    query = api.select(Result).set_time_received(range="-3h")
    assert query._criteria["time_received"] == {"range": "-3h"}

    query.set_time_received(start="2023-12-10T00:00:00.000Z", end="2023-12-11T00:00:00.000Z")
    assert query._criteria["time_received"] == {
        "start": "2023-12-10T00:00:00.000Z",
        "end": "2023-12-11T00:00:00.000Z"
    }

    with pytest.raises(ApiError):
        query.set_time_received(start="2023-12-10T00:00:00.000Z", end="2023-12-11T00:00:00.000Z", range="-3h")


def test_result_scroll(cbcsdk_mock):
    """Testing ResultQuery scroll"""
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/results/_scroll",
                             GET_SCROLL_RESULTS(100, 200, 100))

    api = cbcsdk_mock.api
    query = api.select(Result).set_time_received(range="-3h")

    results = query.scroll(100)

    assert query.num_remaining == 100
    assert query._search_after == "MTcwMjMyMTM2MDU3OSwyMT"

    def on_post(url, body, **kwargs):
        """Test 2nd scroll request"""
        assert body == {
            "criteria": {
                "time_received": {"range": "-3h"}},
            "rows": 10000,
            "search_after": "MTcwMjMyMTM2MDU3OSwyMT"
        }
        return GET_SCROLL_RESULTS(100, 200, 0)

    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/results/_scroll",
                             on_post)

    results.extend(query.scroll(20000))

    assert len(results) == 200

    assert query.scroll(100) == []


def test_result_to_json(cbcsdk_mock):
    """Testing ResultQuery scroll"""
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/results/_scroll",
                             GET_SCROLL_RESULTS(1, 1, 1))

    api = cbcsdk_mock.api
    query = api.select(Result).set_time_received(range="-3h")

    results = query.scroll(1)

    results[0].to_json() == SINGLE_RESULT
