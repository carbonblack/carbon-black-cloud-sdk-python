"""Tests for audit and remediation queries."""

import pytest
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.audit_remediation import Run, RunQuery, RunHistoryQuery
from cbc_sdk.errors import ApiError, CredentialError
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


def test_no_org_key():
    """Test that a CredentialError is raised when no org key is present."""
    with pytest.raises(CredentialError):
        CBCloudAPI(url="https://example.com", token="ABCD/1234", ssl_verify=True)  # note: no org_key


def test_async_submit(cb):
    """Test the functionality of _async_submit() in the CBCloudAPI object."""
    future = cb._async_submit(lambda arg, kwarg: list(range(arg[0])), 4)
    result = future.result()
    assert result == [0, 1, 2, 3]


def test_simple_get(cbcsdk_mock):
    """Test a simple "get" of a run status object."""
    cbcsdk_mock.mock_request("GET", "/livequery/v1/orgs/test/runs/abcdefg",
                             {"org_key": "test", "name": "FoobieBletch", "id": "abcdefg"})
    api = cbcsdk_mock.api
    run = api.select(Run, "abcdefg")
    assert run.org_key == "test"
    assert run.name == "FoobieBletch"
    assert run.id == "abcdefg"


def test_audit_remediation(cbcsdk_mock):
    """Test a simple query run."""
    def _run_query(url, body, **kwargs):
        assert body == {"sql": "select * from whatever;", "device_filter": {}}
        return {"org_key": "test", "name": "FoobieBletch", "id": "abcdefg"}

    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs", _run_query)
    api = cbcsdk_mock.api
    query = api.audit_remediation("select * from whatever;")
    assert isinstance(query, RunQuery)
    run = query.submit()
    assert run.org_key == "test"
    assert run.name == "FoobieBletch"
    assert run.id == "abcdefg"


def test_audit_remediation_with_everything(cbcsdk_mock):
    """Test an audit remediation query with all possible options."""
    def _run_query(url, body, **kwargs):
        assert body == {"sql": "select * from whatever;", "name": "AmyWasHere", "notify_on_finish": True,
                        "device_filter": {"device_id": [1, 2, 3], "os": ["Alpha", "Bravo", "Charlie"],
                                          "policy_id": [16]}}
        return {"org_key": "test", "name": "FoobieBletch", "id": "abcdefg"}

    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs", _run_query)
    api = cbcsdk_mock.api
    query = api.audit_remediation("select * from whatever;").device_ids([1, 2, 3]) \
        .device_types(["Alpha", "Bravo", "Charlie"]).policy_id(16).name("AmyWasHere").notify_on_finish()
    assert isinstance(query, RunQuery)
    run = query.submit()
    assert run.org_key == "test"
    assert run.name == "FoobieBletch"
    assert run.id == "abcdefg"


def test_audit_remediation_device_ids_broken(cb):
    """Test submitting a bad device ID to a query."""
    query = cb.audit_remediation("select * from whatever;")
    with pytest.raises(ApiError):
        query = query.device_ids(["Bogus"])


def test_audit_remediation_device_types_broken(cb):
    """Test submitting a bad device type to a query."""
    query = cb.audit_remediation("select * from whatever;")
    with pytest.raises(ApiError):
        query = query.device_types([420])


def test_audit_remediation_policy_id_broken(cb):
    """Test submitting a bad policy ID to a query."""
    query = cb.audit_remediation("select * from whatever;")
    with pytest.raises(ApiError):
        query = query.policy_id(["Bogus"])


def test_audit_remediation_history(cbcsdk_mock):
    """Test a query of run history."""
    def _run_query(url, body, **kwargs):
        assert body == {"query": "xyzzy", "start": 0}
        return {"org_key": "test", "num_found": 3,
                "results": [{"org_key": "test", "name": "FoobieBletch", "id": "abcdefg"},
                            {"org_key": "test", "name": "Aoxomoxoa", "id": "cdefghi"},
                            {"org_key": "test", "name": "Read_Me", "id": "efghijk"}]}

    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/_search", _run_query)
    api = cbcsdk_mock.api
    query = api.audit_remediation_history("xyzzy")
    assert isinstance(query, RunHistoryQuery)
    count = 0
    for item in query.all():
        assert item.org_key == "test"
        if item.id == "abcdefg":
            assert item.name == "FoobieBletch"
        elif item.id == "cdefghi":
            assert item.name == "Aoxomoxoa"
        elif item.id == "efghijk":
            assert item.name == "Read_Me"
        else:
            pytest.fail("Unknown item ID: %s" % item.id)
        count = count + 1
    assert count == 3


def test_audit_remediation_history_with_everything(cbcsdk_mock):
    """Test a query of run history with all possible options."""
    def _run_query(url, body, **kwargs):
        assert body == {"query": "xyzzy", "sort": [{"field": "id", "order": "ASC"}], "start": 0}
        return {"org_key": "test", "num_found": 3,
                "results": [{"org_key": "test", "name": "FoobieBletch", "id": "abcdefg"},
                            {"org_key": "test", "name": "Aoxomoxoa", "id": "cdefghi"},
                            {"org_key": "test", "name": "Read_Me", "id": "efghijk"}]}

    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/runs/_search", _run_query)
    api = cbcsdk_mock.api
    query = api.audit_remediation_history("xyzzy").sort_by("id")
    assert isinstance(query, RunHistoryQuery)
    count = 0
    for item in query.all():
        assert item.org_key == "test"
        if item.id == "abcdefg":
            assert item.name == "FoobieBletch"
        elif item.id == "cdefghi":
            assert item.name == "Aoxomoxoa"
        elif item.id == "efghijk":
            assert item.name == "Read_Me"
        else:
            pytest.fail("Unknown item ID: %s" % item.id)
        count = count + 1
    assert count == 3
