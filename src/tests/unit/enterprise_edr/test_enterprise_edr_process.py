"""Testing Process and Tree objects of cbc_sdk.enterprise_edr"""

import pytest
import logging
from cbc_sdk.enterprise_edr import Process, ProcessFacet, Tree, Event, Query, AsyncProcessQuery, AsyncFacetQuery
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ObjectNotFoundError, ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.enterprise_edr.mock_process import (GET_PROCESS_SUMMARY_RESP,
                                                             GET_PROCESS_SUMMARY_RESP_1,
                                                             GET_PROCESS_SUMMARY_RESP_2,
                                                             GET_TREE_RESP,
                                                             GET_PROCESS_VALIDATION_RESP,
                                                             POST_PROCESS_SEARCH_JOB_RESP,
                                                             GET_PROCESS_SEARCH_JOB_RESP,
                                                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1,
                                                             GET_PROCESS_SEARCH_PARENT_JOB_RESULTS_RESP,
                                                             GET_FACET_SEARCH_RESULTS_RESP,
                                                             EXPECTED_PROCESS_FACETS,
                                                             EXPECTED_PROCESS_RANGES_FACETS)

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
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
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


def test_process_events_with_criteria_exclusions(cbcsdk_mock):
    """Testing the add_criteria() method when selecting events."""
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    assert isinstance(process.events(), Query)
    # create the events query object to compare
    events = process.events(event_type="modload").add_criteria("crossproc_action", ["ACTION_PROCESS_API_CALL"]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    events.add_criteria("crossproc_action", "SOME_OTHER_CRIT")
    # emulate the manual select in Process.events()
    query = api.select(Event).where(process_guid=guid).add_criteria("crossproc_action", ["ACTION_PROCESS_API_CALL"]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    query.add_criteria("crossproc_action", "SOME_OTHER_CRIT")
    assert [isinstance(q, Query) for q in [events, query]]
    # extract and compare the parameters from each Query
    events_query_params = events._get_query_parameters()
    query_params = query.and_(event_type="modload")._get_query_parameters()
    expected_params = {"query": "process_guid:WNEXFKQ7\\-0002b226\\-000015bd\\-00000000\\-"
                       "1d6225bbba74c00 AND event_type:modload",
                       "criteria": {
                           "crossproc_action": ["ACTION_PROCESS_API_CALL",
                                                "SOME_OTHER_CRIT"],
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       },
                       "process_guid": "WNEXFKQ7\\-0002b226\\-000015bd\\-00000000\\-1d6225bbba74c00"
                       }
    assert events_query_params == query_params
    assert events_query_params == expected_params


def test_process_events_exceptions(cbcsdk_mock):
    """Testing raising an Exception when using Query.add_criteria() and Query.add_exclusions()."""
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    assert isinstance(process.events(), Query)
    # use a criteria value that's not a string or list
    with pytest.raises(ApiError):
        events = process.events(event_type="modload").add_criteria("crossproc_action", 0)
    # use an exclusion value that's not a string or list
    with pytest.raises(ApiError):
        events = process.events().add_exclusions("crossproc_effective_reputation", 0)


def test_process_with_criteria_exclusions(cbcsdk_mock):
    """Testing AsyncProcessQuery.add_criteria() and AsyncProcessQuery.add_exclusions()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
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
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1)
    p = process[0]
    assert p.process_md5 == 'c7084336325dc8eadfb1e8ff876921c4'

    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       }}
    assert process_q_params == expected_params


def test_process_fields(cbcsdk_mock):
    """Testing AsyncProcessQuery.set_fields()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    process = process.set_fields(["parent_hash", "device_policy"])

    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       },
                       "fields": [
                           "parent_hash",
                           "device_policy"
                       ]}
    assert process_q_params == expected_params


def test_process_time_range(cbcsdk_mock):
    """Testing AsyncProcessQuery.set_fields()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    process = process.set_time_range(start="2020-01-21T18:34:04Z")
    process = process.set_time_range(end="2020-02-21T18:34:04Z")
    process = process.set_time_range(window="-1w")

    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       },
                       "time_range": {
                           "start": "2020-01-21T18:34:04Z",
                           "end": "2020-02-21T18:34:04Z",
                           "window": "-1w"
                       }}
    assert process_q_params == expected_params


def test_process_start_rows(cbcsdk_mock):
    """Testing AsyncProcessQuery.set_start() and AsyncProcessQuery.set_rows()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    process = process.set_start(10)
    process = process.set_rows(102)

    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       },
                       "start": 10,
                       "rows": 102
                       }
    assert process_q_params == expected_params


def test_process_sort(cbcsdk_mock):
    """Testing AsyncProcessQuery.sort_by()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    process = process.sort_by("process_pid", direction="DESC")
    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       },
                       "sort": [{
                           "field": "process_pid",
                           "order": "DESC"
                       }]}
    assert process_q_params == expected_params


def test_process_events_with_criteria_exclusions(cbcsdk_mock):
    """Testing the add_criteria() method when selecting events."""
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    assert isinstance(process.events(), Query)
    # create the events query object to compare
    events = process.events(event_type="modload").add_criteria("crossproc_action", ["ACTION_PROCESS_API_CALL"]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    events.add_criteria("crossproc_action", "SOME_OTHER_CRIT")
    events.add_exclusions("exclusion_key", "exclusion_value")
    # emulate the manual select in Process.events()
    query = api.select(Event).where(process_guid=guid).add_criteria("crossproc_action", ["ACTION_PROCESS_API_CALL"]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    query.add_criteria("crossproc_action", "SOME_OTHER_CRIT")
    query.add_exclusions("exclusion_key", "exclusion_value")
    assert [isinstance(q, Query) for q in [events, query]]
    # extract and compare the parameters from each Query
    events_query_params = events._get_query_parameters()
    query_params = query.and_(event_type="modload")._get_query_parameters()
    expected_params = {"query": "process_guid:WNEXFKQ7\\-0002b226\\-000015bd\\-00000000\\-"
                       "1d6225bbba74c00 AND event_type:modload",
                       "criteria": {
                           "crossproc_action": ["ACTION_PROCESS_API_CALL",
                                                "SOME_OTHER_CRIT"],
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"],
                           "exclusion_key": ["exclusion_value"]
                       },
                       "process_guid": "WNEXFKQ7\\-0002b226\\-000015bd\\-00000000\\-1d6225bbba74c00"
                       }
    assert events_query_params == query_params
    assert events_query_params == expected_params


def test_process_events_exceptions(cbcsdk_mock):
    """Testing raising an Exception when using Query.add_criteria() and Query.add_exclusions()."""
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    assert isinstance(process.events(), Query)
    # use a criteria value that's not a string or list
    with pytest.raises(ApiError):
        events = process.events(event_type="modload").add_criteria("crossproc_action", 0)
    # use an exclusion value that's not a string or list
    with pytest.raises(ApiError):
        events = process.events().add_exclusions("crossproc_effective_reputation", 0)


def test_process_with_criteria_exclusions(cbcsdk_mock):
    """Testing AsyncProcessQuery.add_criteria() and AsyncProcessQuery.add_exclusions()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
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
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1)
    p = process[0]
    assert p.process_md5 == 'c7084336325dc8eadfb1e8ff876921c4'

    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       }}
    assert process_q_params == expected_params


def test_process_fields(cbcsdk_mock):
    """Testing AsyncProcessQuery.set_fields()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    process = process.set_fields(["parent_hash", "device_policy"])

    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       },
                       "fields": [
                           "parent_hash",
                           "device_policy"
                       ]}
    assert process_q_params == expected_params


def test_process_time_range(cbcsdk_mock):
    """Testing AsyncProcessQuery.set_fields()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    process = process.set_time_range(start="2020-01-21T18:34:04Z")
    process = process.set_time_range(end="2020-02-21T18:34:04Z")
    process = process.set_time_range(window="-1w")

    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       },
                       "time_range": {
                           "start": "2020-01-21T18:34:04Z",
                           "end": "2020-02-21T18:34:04Z",
                           "window": "-1w"
                       }}
    assert process_q_params == expected_params


def test_process_start_rows(cbcsdk_mock):
    """Testing AsyncProcessQuery.set_start() and AsyncProcessQuery.set_rows()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    process = process.set_start(10)
    process = process.set_rows(102)

    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       },
                       "start": 10,
                       "rows": 102
                       }
    assert process_q_params == expected_params


def test_process_sort(cbcsdk_mock):
    """Testing AsyncProcessQuery.sort_by()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    process = process.sort_by("process_pid", direction="DESC")
    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       },
                       "sort": [{
                           "field": "process_pid",
                           "order": "DESC"
                       }]}
    assert process_q_params == expected_params


@pytest.mark.parametrize('get_summary_response, guid, process_search_results, has_parent_process',
                         [(GET_PROCESS_SUMMARY_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00",
                           GET_PROCESS_SEARCH_PARENT_JOB_RESULTS_RESP, True),
                          (GET_PROCESS_SUMMARY_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52",
                           None, False),
                          (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205",
                           GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1, True)
                          ])
def test_process_parents(cbcsdk_mock, get_summary_response, guid, process_search_results, has_parent_process):
    """Testing Process.parents property/method."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # query for a Process
    process = api.select(Process, guid)
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary", get_summary_response)
    # the process has a parent process (manually flagged)
    if has_parent_process:
        # Process.parents property returns a Process object, or [] if None
        assert isinstance(process.parents, Process)

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
                                 process_search_results)

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
    (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205", 2)])
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
    (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205",
     "708c8760385810080c4d17fa84d325ca")])
def test_process_md5(cbcsdk_mock, get_summary_response, guid, md5):
    """Testing Process.process_md5 property."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary", get_summary_response)
    process = api.select(Process, guid)
    assert process.process_md5 == md5


def test_process_md5_not_found(cbcsdk_mock):
    """Testing error raising when receiving 404 for a Process."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary",
                             ObjectNotFoundError(uri='uri_to_get_summ'))
    process = api.select(Process, "someNonexistantGuid")
    with pytest.raises(ObjectNotFoundError):
        process.summary


@pytest.mark.parametrize('get_summary_response, guid, sha256', [
    (GET_PROCESS_SUMMARY_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00",
     "5920199e4fbfa47c1717b863814722148a353e54f8c10912cf1f991a1c86309d"),
    (GET_PROCESS_SUMMARY_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52",
     "d5e122606054fa0b03db3ee8cf9ea7701e523875e2bdb87581ad7232ffc9308e"),
    (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205", None)])
def test_process_sha256(cbcsdk_mock, get_summary_response, guid, sha256):
    """Testing Process.process_sha256 property."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary", get_summary_response)
    process = api.select(Process, guid)
    assert process.process_sha256 == sha256


@pytest.mark.parametrize('get_summary_response, guid, pids', [
    (GET_PROCESS_SUMMARY_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00", [5565]),
    (GET_PROCESS_SUMMARY_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52", [788]),
    (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205", [860])])
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


def test_process_facet_select(cbcsdk_mock):
    """Testing ProcessFacet select(), ranges_, terms_."""
    api = cbcsdk_mock.api
    facet_query = api.select(ProcessFacet).where("process_name:svchost.exe").add_range({"bucket_size": "+1DAY",
                                                                                        "start": "2020-10-16T00:00:00Z",
                                                                                        "end": "2020-11-12T00:00:00Z",
                                                                                        "field": "backend_timestamp"})

    facet_query.add_facet_field(["device_timestamp", "backend_timestamp"]).timeout(60000)
    facet_query.set_time_range(start="2020-10-16T00:00:00Z", end="2020-11-12T00:00:00Z")
    # mock the search request
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/facet_jobs", {"job_id": "the-job-id"})
    # mock the result call
    cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/processes/facet_jobs/the-job-id/results", GET_FACET_SEARCH_RESULTS_RESP)
    future = facet_query.execute_async()
    res = future.result()[0]
    assert res.terms_.fields == ['backend_timestamp', 'device_timestamp']
    assert res.terms_.facets == EXPECTED_PROCESS_FACETS
    assert isinstance(res.terms_, ProcessFacet.Terms)
    assert res.ranges_.fields == ['backend_timestamp']
    assert res.ranges_.facets == EXPECTED_PROCESS_RANGES_FACETS
    assert isinstance(res.ranges_, ProcessFacet.Ranges)
    # if already, submitted, the query shouldn't be submitted again
    with pytest.raises(ApiError):
        future = facet_query.execute_async()
        res = future.result()[0]


def test_process_facets(cbcsdk_mock):
    """Testing Process.facets() method."""
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
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1)
    # mock the search request
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/facet_jobs", {"job_id": "the-job-id"})
    # mock the result call
    cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/processes/facet_jobs/the-job-id/results", GET_FACET_SEARCH_RESULTS_RESP)
    api = cbcsdk_mock.api
    process = api.select(Process).where(process_guid="WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00")
    results = [proc for proc in process]
    process_facet_query = results[0].facets()
    assert isinstance(process_facet_query, AsyncFacetQuery)
    process_facet_query.add_facet_field(["backend_timestamp", "device_timestamp"])
    future = process_facet_query.execute_async()
    results = future.result()
    assert results[0].terms_.fields == ['backend_timestamp', 'device_timestamp']


@pytest.mark.parametrize("bucket_size, start, end, field", [
    # empty values
    ([], 0, 2, "some_field"),
    (30, [], 2, "some_field"),
    (30, 0, [], "some_field"),
    (30, 0, 2, []),
    # invalid types
    (30.5, 0, 2, "some_field"),
    (30, 0.5, 2, "some_field"),
    (30, 0, 2.5, "some_field"),
    (30, 0, 2, 1),
    # more empty values
    (None, 0, 2, "some_field"),
    (30, None, 2, "some_field"),
    (30, 0, None, "some_field"),
    (30, 0, 2, None)
])
def test_process_facet_query_check_range(cbcsdk_mock, bucket_size, start, end, field):
    """Testing AsyncFacetQuery._check_range()."""
    api = cbcsdk_mock.api
    range = {
        "bucket_size": bucket_size,
        "start": start,
        "end": end,
        "field": field
    }
    with pytest.raises(ApiError):
        api.select(ProcessFacet)._check_range(range)


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
