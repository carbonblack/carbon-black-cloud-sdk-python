"""Testing Process and Tree objects of cbc_sdk.enterprise_edr"""

import pytest
import logging
from cbc_sdk.enterprise_edr import Process, Tree, Event, Query, AsyncProcessQuery
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ObjectNotFoundError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.enterprise_edr.mock_process import (GET_PROCESS_SUMMARY_RESP,
                                                             GET_PROCESS_SUMMARY_RESP_1,
                                                             GET_PROCESS_SUMMARY_RESP_2,
                                                             GET_TREE_RESP,
                                                             GET_PROCESS_VALIDATION_RESP,
                                                             POST_PROCESS_SEARCH_JOB_RESP,
                                                             GET_PROCESS_SEARCH_JOB_RESP,
                                                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
                                                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1,
                                                             GET_PROCESS_SEARCH_PARENT_JOB_RESULTS_RESP,
                                                             GET_SUMMARY_NOT_FOUND)

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

def test_process_select(cbcsdk_mock):
    """Testing Process Querying with select()"""
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary", GET_PROCESS_SUMMARY_RESP)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    assert isinstance(process, Process)
    assert process.process_guid == guid
    assert process.summary is not None
    assert process.siblings is not None
    summary = api.select(Process.Summary, guid)
    assert summary is not None


def test_summary_select(cbcsdk_mock):
    """Test querying for a Proc Summary."""
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    summary = api.select(Process.Summary).where(f"process_guid:{guid}")
    assert isinstance(summary, Query)


def test_process_events(cbcsdk_mock):
    """Testing Process.events()."""
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    assert isinstance(process.events(), Query)
    # create the events query object to compare
    events = process.events(event_type="modload")
    # emulate the manual select in Process.events()
    query = api.select(Event).where(process_guid=guid)
    assert [isinstance(q, Query) for q in [events, query]]
    # extract and compare the parameters from each Query
    events_query_params = events._query_builder._collapse()
    query_params = query.and_(event_type="modload")._query_builder._collapse()
    expected_params = ("process_guid:WNEXFKQ7\\-0002b226\\-000015bd\\-00000000\\-"
                       "1d6225bbba74c00 AND event_type:modload")
    assert events_query_params == query_params
    assert events_query_params == expected_params


@pytest.mark.parametrize('get_summary_response, guid, process_search_results, has_parent_process', [
    (GET_PROCESS_SUMMARY_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00",
     GET_PROCESS_SEARCH_PARENT_JOB_RESULTS_RESP, True),
    (GET_PROCESS_SUMMARY_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52",
     None, False),
    (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205",
     GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1, True)
    ])
def test_process_parents(cbcsdk_mock, get_summary_response, guid, process_search_results, has_parent_process):
    """Testing Process.parents property/method."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation", GET_PROCESS_VALIDATION_RESP)
    # query for a Process
    process = api.select(Process, guid)
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary", get_summary_response)
    # the process has a parent process (manually flagged)
    if has_parent_process:
        # Process.parents property returns a Process object, or [] if None
        assert isinstance(process.parents, Process)

        # mock the POST of a search
        cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_job", POST_PROCESS_SEARCH_JOB_RESP)
        # mock the GET to check search status
        cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_jobs/2c292717-80ed-4f0d-845f-779e09470920", GET_PROCESS_SEARCH_JOB_RESP)
        # mock the GET to get search results
        cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/processes/search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results", process_search_results)

        # query for a Process that has a guid == the guid of the parent process
        parent_process = api.select(Process).where(process_guid=process.parents.process_guid)

        parent_search_results = [process for process in parent_process._perform_query()]

        # check that the search for parent_process yields result consistent with the original process's parent
        assert parent_search_results[0].process_guid == process.parents.process_guid
    else:
        # the process has no parent
        assert process.parents == []


@pytest.mark.parametrize('get_summary_response, guid, expected_num_children', [
    (GET_PROCESS_SUMMARY_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00", 0),
    (GET_PROCESS_SUMMARY_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52", 3),
    (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205", 2)
    ])
def test_process_children(cbcsdk_mock, get_summary_response, guid, expected_num_children):
    """Testing Process.children property."""
    api = cbcsdk_mock.api
    process = api.select(Process, guid)
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary", get_summary_response)
    # if there's children, check that Process.children returns the right objects
    if isinstance(process.summary.children, list):
        assert isinstance(process.children, list)
        assert [isinstance(child, Process) for child in process.children]
    else:
        assert process.children == []
    assert len(process.children) == expected_num_children


@pytest.mark.parametrize('get_summary_response, guid, md5', [
    (GET_PROCESS_SUMMARY_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00", None),
    (GET_PROCESS_SUMMARY_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52", "e83650f70459a027aa596e1a73c961a1"),
    (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205", "708c8760385810080c4d17fa84d325ca")
    ])
def test_process_md5(cbcsdk_mock, get_summary_response, guid, md5):
    """Testing Process.process_md5 property."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary", get_summary_response)
    process = api.select(Process, guid)
    assert process.process_md5 == md5


def test_process_md5_not_found(cbcsdk_mock):
    """Testing error raising when receiving 404 for a Process."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary", ObjectNotFoundError(uri='uri_to_get_summ'))
    process = api.select(Process, "someNonexistantGuid")
    with pytest.raises(ObjectNotFoundError):
        process.summary


@pytest.mark.parametrize('get_summary_response, guid, sha256', [
    (GET_PROCESS_SUMMARY_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00", "5920199e4fbfa47c1717b863814722148a353e54f8c10912cf1f991a1c86309d"),
    (GET_PROCESS_SUMMARY_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52", "d5e122606054fa0b03db3ee8cf9ea7701e523875e2bdb87581ad7232ffc9308e"),
    (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205", None)
    ])
def test_process_sha256(cbcsdk_mock, get_summary_response, guid, sha256):
    """Testing Process.process_sha256 property."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary", get_summary_response)
    process = api.select(Process, guid)
    assert process.process_sha256 == sha256


@pytest.mark.parametrize('get_summary_response, guid, pids', [
    (GET_PROCESS_SUMMARY_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00", [5565]),
    (GET_PROCESS_SUMMARY_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52", [788]),
    (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205", [860])
    ])
def test_process_pids(cbcsdk_mock, get_summary_response, guid, pids):
    """Testing Process.process_pids property."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary", get_summary_response)
    process = api.select(Process, guid)
    assert process.process_pids == pids


def test_process_select_where(cbcsdk_mock):
    """Testing Process querying with where()."""
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process).where(f"process_guid:{guid}")
    assert isinstance(process, AsyncProcessQuery)


def test_tree_select(cbcsdk_mock):
    """Testing Tree Querying"""
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/tree", GET_TREE_RESP)
    api = cbcsdk_mock.api
    guid = "WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00"
    process = api.select(Process, guid)
    tree = process.tree()
    children = tree.nodes["children"]
    assert len(children) == len(tree.children)
    assert len(children) > 0

    procTree = api.select(Tree).where(process_guid="WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00")
    results = procTree._perform_query()
    assert results is not None
    assert results["nodes"]["children"] is not None
    assert results["incomplete_results"] is False
