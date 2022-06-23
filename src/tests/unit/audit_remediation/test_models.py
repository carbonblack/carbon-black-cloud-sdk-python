"""Tests for the model object for audit and remediation."""

import pytest
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.audit_remediation import Run, Result, ResultQuery, FacetQuery
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock


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


def test_run_refresh(cbcsdk_mock):
    """Test refreshing a query view."""
    cbcsdk_mock.mock_request("GET", "/livequery/v1/orgs/test/runs/abcdefg",
                             {"org_key": "test", "name": "FoobieBletch", "id": "abcdefg", "status": "COMPLETE"})
    api = cbcsdk_mock.api
    run = Run(api, "abcdefg", {"org_key": "test", "name": "FoobieBletch", "id": "abcdefg", "status": "ACTIVE"})
    rc = run.refresh()
    assert rc
    assert run.org_key == "test"
    assert run.name == "FoobieBletch"
    assert run.id == "abcdefg"
    assert run.status == "COMPLETE"


def test_run_stop(cbcsdk_mock):
    """Test stopping a running query."""

    def _execute_stop(url, body, **kwargs):
        assert body == {"status": "CANCELLED"}
        return {"org_key": "test", "name": "FoobieBletch", "id": "abcdefg", "status": "CANCELLED"}

    cbcsdk_mock.mock_request("PUT", "/livequery/v1/orgs/test/runs/abcdefg/status", _execute_stop)
    api = cbcsdk_mock.api
    run = Run(api, "abcdefg", {"org_key": "test", "name": "FoobieBletch", "id": "abcdefg", "status": "ACTIVE"})
    rc = run.stop()
    assert rc
    assert run.org_key == "test"
    assert run.name == "FoobieBletch"
    assert run.id == "abcdefg"
    assert run.status == "CANCELLED"


def test_run_stop_failed(cbcsdk_mock):
    """Test the failure to stop a running query."""

    def _execute_stop(url, body, **kwargs):
        assert body == {"status": "CANCELLED"}
        return CBCSDKMock.StubResponse({"error_message": "The query is not presently running."}, 409)

    cbcsdk_mock.mock_request("PUT", "/livequery/v1/orgs/test/runs/abcdefg/status", _execute_stop)
    api = cbcsdk_mock.api
    run = Run(api, "abcdefg", {"org_key": "test", "name": "FoobieBletch", "id": "abcdefg", "status": "CANCELLED"})
    rc = run.stop()
    assert not rc


def test_run_delete(cbcsdk_mock):
    """Test deleting a query."""
    _was_called = False

    def _execute_delete(url, body):
        nonlocal _was_called
        assert not _was_called, "_execute_delete should not be called twice!"
        _was_called = True
        return CBCSDKMock.StubResponse(None)

    cbcsdk_mock.mock_request("DELETE", "/livequery/v1/orgs/test/runs/abcdefg", _execute_delete)
    api = cbcsdk_mock.api
    run = Run(api, "abcdefg", {"org_key": "test", "name": "FoobieBletch", "id": "abcdefg", "status": "ACTIVE"})
    rc = run.delete()
    assert _was_called
    assert rc
    assert run._is_deleted
    # Now ensure that certain operations that don't make sense on a deleted object raise ApiError
    with pytest.raises(ApiError):
        run.refresh()
    with pytest.raises(ApiError):
        run.stop()
    with pytest.raises(ApiError):
        run.query_results()
    with pytest.raises(ApiError):
        run.query_device_summaries()
    with pytest.raises(ApiError):
        run.query_facets()
    # And make sure that deleting a deleted object returns True immediately
    rc = run.delete()
    assert rc


def test_run_delete_failed(cbcsdk_mock):
    """Test a failure in the attempt to delete a query."""
    cbcsdk_mock.mock_request("DELETE", "/livequery/v1/orgs/test/runs/abcdefg", CBCSDKMock.StubResponse(None, 403))
    api = cbcsdk_mock.api
    run = Run(api, "abcdefg", {"org_key": "test", "name": "FoobieBletch", "id": "abcdefg", "status": "ACTIVE"})
    rc = run.delete()
    assert not rc
    assert not run._is_deleted


def test_result_device_summaries(cbcsdk_mock):
    """Test result of a device summary query."""

    def _run_summaries(url, body, **kwargs):
        assert body == {"query": "foo", "criteria": {"device.name": ["AxCx", "A7X"]},
                        "sort": [{"field": "device_name", "order": "ASC"}], "start": 0}
        return {"org_key": "Z100", "num_found": 2, "results": [
            {"id": "ghijklm", "total_results": 2, "device": {"id": 314159, "name": "device1"},
             "metrics": [{"key": "aaa", "value": 0.0}, {"key": "bbb", "value": 0.0}]},
            {"id": "mnopqrs", "total_results": 3, "device": {"id": 271828, "name": "device2"},
             "metrics": [{"key": "aaa", "value": 0.0}, {"key": "bbb", "value": 0.0}]}
        ]}

    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/abcdefg/results/device_summaries/_search",
                             _run_summaries)
    api = cbcsdk_mock.api
    result = Result(api, {"id": "abcdefg", "device": {"id": "abcdefg"}, "fields": {}, "metrics": {}})
    query = result.query_device_summaries().where("foo").set_device_names(["AxCx", "A7X"]).sort_by("device_name")
    assert isinstance(query, ResultQuery)
    count = 0
    for item in query.all():
        if item.id == 314159:
            # assert item.total_results == 2
            assert item.device_id == 314159
            assert item.name == "device1"
        elif item.id == 271828:
            # assert item.total_results == 3
            assert item.device_id == 271828
            assert item.name == "device2"
        else:
            pytest.fail("Invalid object with ID %s seen" % item.id)
        count = count + 1
    assert count == 2


def test_result_query_result_facets(cbcsdk_mock):
    """Test a facet query on query results."""

    def _run_facets(url, body, **kwargs):
        assert body == {"query": "xyzzy", "criteria": {"device.name": ["AxCx", "A7X"]},
                        "terms": {"fields": ["alpha", "bravo", "charlie"]}}
        return {"terms": [{"field": "alpha", "values": [{"total": 1, "id": "alpha1", "name": "alpha1"},
                                                        {"total": 2, "id": "alpha2", "name": "alpha2"}]},
                          {"field": "bravo", "values": [{"total": 1, "id": "bravo1", "name": "bravo1"},
                                                        {"total": 2, "id": "bravo2", "name": "bravo2"}]},
                          {"field": "charlie", "values": [{"total": 1, "id": "charlie1", "name": "charlie1"},
                                                          {"total": 2, "id": "charlie2", "name": "charlie2"}]}]}

    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/abcdefg/results/_facet", _run_facets)
    api = cbcsdk_mock.api
    result = Result(api, {"id": "abcdefg", "device": {"id": "abcdefg"}, "fields": {}, "metrics": {}})
    query = result.query_result_facets().where("xyzzy").facet_field("alpha").facet_field(["bravo", "charlie"]) \
        .set_device_names(["AxCx", "A7X"])
    assert isinstance(query, FacetQuery)
    count = 0
    for item in query.all():
        vals = item.values
        if item.field == "alpha":
            assert vals[0]["id"] == "alpha1"
            assert vals[1]["id"] == "alpha2"
        elif item.field == "bravo":
            assert vals[0]["id"] == "bravo1"
            assert vals[1]["id"] == "bravo2"
        elif item.field == "charlie":
            assert vals[0]["id"] == "charlie1"
            assert vals[1]["id"] == "charlie2"
        else:
            pytest.fail("Unknown field name %s seen" % item.field)
        count = count + 1
    assert count == 3


def test_result_query_device_summary_facets(cbcsdk_mock):
    """Test a facet query on device summary."""

    def _run_facets(url, body, **kwargs):
        assert body == {"query": "xyzzy", "criteria": {"device.name": ["AxCx", "A7X"]},
                        "terms": {"fields": ["alpha", "bravo", "charlie"]}}
        return {"terms": [{"field": "alpha", "values": [{"total": 1, "id": "alpha1", "name": "alpha1"},
                                                        {"total": 2, "id": "alpha2", "name": "alpha2"}]},
                          {"field": "bravo", "values": [{"total": 1, "id": "bravo1", "name": "bravo1"},
                                                        {"total": 2, "id": "bravo2", "name": "bravo2"}]},
                          {"field": "charlie", "values": [{"total": 1, "id": "charlie1", "name": "charlie1"},
                                                          {"total": 2, "id": "charlie2", "name": "charlie2"}]}]}

    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/abcdefg/results/device_summaries/_facet",
                             _run_facets)
    api = cbcsdk_mock.api
    result = Result(api, {"id": "abcdefg", "device": {"id": "abcdefg"}, "fields": {}, "metrics": {}})
    query = result.query_device_summary_facets().where("xyzzy").facet_field("alpha") \
        .facet_field(["bravo", "charlie"]).set_device_names(["AxCx", "A7X"])
    assert isinstance(query, FacetQuery)
    count = 0
    for item in query.all():
        vals = item.values
        if item.field == "alpha":
            assert vals[0]["id"] == "alpha1"
            assert vals[1]["id"] == "alpha2"
        elif item.field == "bravo":
            assert vals[0]["id"] == "bravo1"
            assert vals[1]["id"] == "bravo2"
        elif item.field == "charlie":
            assert vals[0]["id"] == "charlie1"
            assert vals[1]["id"] == "charlie2"
        else:
            pytest.fail("Unknown field name %s seen" % item.field)
        count = count + 1
    assert count == 3
