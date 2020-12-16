"""Tests for audit and remediation queries."""

import pytest
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.audit_remediation import Run, RunQuery, RunHistoryQuery
from cbc_sdk.errors import ApiError, CredentialError
from tests.unit.fixtures.stubresponse import StubResponse, patch_cbc_sdk_api


def test_no_org_key():
    """Test that a CredentialError is raised when no org key is present."""
    with pytest.raises(CredentialError):
        CBCloudAPI(url="https://example.com", token="ABCD/1234", ssl_verify=True)  # note: no org_key


def test_async_submit():
    """Test the functionality of _async_submit() in the CBCloudAPI object."""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    future = api._async_submit(lambda arg, kwarg: list(range(arg[0])), 4)
    result = future.result()
    assert result == [0, 1, 2, 3]


def test_simple_get(monkeypatch):
    """Test a simple "get" of a run status object."""
    _was_called = False

    def _get_run(url, parms=None, default=None):
        nonlocal _was_called
        assert url == "/livequery/v1/orgs/Z100/runs/abcdefg"
        _was_called = True
        return {"org_key": "Z100", "name": "FoobieBletch", "id": "abcdefg"}

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_run)
    run = api.select(Run, "abcdefg")
    assert _was_called
    assert run.org_key == "Z100"
    assert run.name == "FoobieBletch"
    assert run.id == "abcdefg"


def test_audit_remediation(monkeypatch):
    """Test a simple query run."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/livequery/v1/orgs/Z100/runs"
        assert body == {"sql": "select * from whatever;", "device_filter": {}}
        _was_called = True
        return StubResponse({"org_key": "Z100", "name": "FoobieBletch", "id": "abcdefg"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.audit_remediation("select * from whatever;")
    assert isinstance(query, RunQuery)
    run = query.submit()
    assert _was_called
    assert run.org_key == "Z100"
    assert run.name == "FoobieBletch"
    assert run.id == "abcdefg"


def test_audit_remediation_with_everything(monkeypatch):
    """Test an audit remediation query with all possible options."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/livequery/v1/orgs/Z100/runs"
        assert body == {"sql": "select * from whatever;", "name": "AmyWasHere", "notify_on_finish": True,
                        "device_filter": {"device_id": [1, 2, 3], "os": ["Alpha", "Bravo", "Charlie"],
                                          "policy_id": [16]}}
        _was_called = True
        return StubResponse({"org_key": "Z100", "name": "FoobieBletch", "id": "abcdefg"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.audit_remediation("select * from whatever;").device_ids([1, 2, 3]) \
        .device_types(["Alpha", "Bravo", "Charlie"]).policy_id(16).name("AmyWasHere").notify_on_finish()
    assert isinstance(query, RunQuery)
    run = query.submit()
    assert _was_called
    assert run.org_key == "Z100"
    assert run.name == "FoobieBletch"
    assert run.id == "abcdefg"


def test_audit_remediation_device_ids_broken():
    """Test submitting a bad device ID to a query."""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    query = api.audit_remediation("select * from whatever;")
    with pytest.raises(ApiError):
        query = query.device_ids(["Bogus"])


def test_audit_remediation_device_types_broken():
    """Test submitting a bad device type to a query."""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    query = api.audit_remediation("select * from whatever;")
    with pytest.raises(ApiError):
        query = query.device_types([420])


def test_audit_remediation_policy_id_broken():
    """Test submitting a bad policy ID to a query."""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    query = api.audit_remediation("select * from whatever;")
    with pytest.raises(ApiError):
        query = query.policy_id(["Bogus"])


def test_audit_remediation_history(monkeypatch):
    """Test a query of run history."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/livequery/v1/orgs/Z100/runs/_search"
        assert body == {"query": "xyzzy", "start": 0}
        _was_called = True
        return StubResponse({"org_key": "Z100", "num_found": 3,
                             "results": [{"org_key": "Z100", "name": "FoobieBletch", "id": "abcdefg"},
                                         {"org_key": "Z100", "name": "Aoxomoxoa", "id": "cdefghi"},
                                         {"org_key": "Z100", "name": "Read_Me", "id": "efghijk"}]})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.audit_remediation_history("xyzzy")
    assert isinstance(query, RunHistoryQuery)
    count = 0
    for item in query.all():
        assert item.org_key == "Z100"
        if item.id == "abcdefg":
            assert item.name == "FoobieBletch"
        elif item.id == "cdefghi":
            assert item.name == "Aoxomoxoa"
        elif item.id == "efghijk":
            assert item.name == "Read_Me"
        else:
            pytest.fail("Unknown item ID: %s" % item.id)
        count = count + 1
    assert _was_called
    assert count == 3


def test_audit_remediation_history_with_everything(monkeypatch):
    """Test a query of run history with all possible options."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/livequery/v1/orgs/Z100/runs/_search"
        assert body == {"query": "xyzzy", "sort": [{"field": "id", "order": "ASC"}], "start": 0}
        _was_called = True
        return StubResponse({"org_key": "Z100", "num_found": 3,
                             "results": [{"org_key": "Z100", "name": "FoobieBletch", "id": "abcdefg"},
                                         {"org_key": "Z100", "name": "Aoxomoxoa", "id": "cdefghi"},
                                         {"org_key": "Z100", "name": "Read_Me", "id": "efghijk"}]})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.audit_remediation_history("xyzzy").sort_by("id")
    assert isinstance(query, RunHistoryQuery)
    count = 0
    for item in query.all():
        assert item.org_key == "Z100"
        if item.id == "abcdefg":
            assert item.name == "FoobieBletch"
        elif item.id == "cdefghi":
            assert item.name == "Aoxomoxoa"
        elif item.id == "efghijk":
            assert item.name == "Read_Me"
        else:
            pytest.fail("Unknown item ID: %s" % item.id)
        count = count + 1
    assert _was_called
    assert count == 3
