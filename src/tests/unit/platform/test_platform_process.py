"""Testing Process and Tree objects of cbc_sdk.platform"""

import pytest
import logging
from cbc_sdk.platform import Process, ProcessFacet, Event, AsyncProcessQuery, SummaryQuery
from cbc_sdk.base import FacetQuery, Query
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError, TimeoutError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_process import (GET_PROCESS_SUMMARY_RESP,
                                                       GET_PROCESS_SUMMARY_RESP_1,
                                                       GET_PROCESS_SUMMARY_RESP_2,
                                                       GET_PROCESS_SUMMARY_RESP_NO_CHILDREN,
                                                       GET_PROCESS_SUMMARY_RESP_STILL_QUERYING,
                                                       GET_PROCESS_SUMMARY_RESP_ZERO_CONTACTED,
                                                       GET_PROCESS_SUMMARY_RESP_NO_HASH,
                                                       GET_PROCESS_SUMMARY_RESP_NO_PID,
                                                       GET_PROCESS_VALIDATION_RESP,
                                                       POST_PROCESS_SEARCH_JOB_RESP,
                                                       POST_TREE_SEARCH_JOB_RESP,
                                                       GET_TREE_SEARCH_JOB_RESP,
                                                       GET_PROCESS_NOT_FOUND,
                                                       GET_PROCESS_SUMMARY_NOT_FOUND,
                                                       GET_PROCESS_SEARCH_JOB_RESP,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP_2,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP_3,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP_ZERO,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP_NO_PID,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP_NO_PARENT_GUID,
                                                       GET_PROCESS_SEARCH_PARENT_JOB_RESULTS_RESP,
                                                       GET_PROCESS_SEARCH_PARENT_JOB_RESULTS_RESP_1,
                                                       POST_PROCESS_DETAILS_JOB_RESP,
                                                       GET_PROCESS_DETAILS_JOB_STATUS_RESP,
                                                       GET_PROCESS_DETAILS_JOB_STATUS_IN_PROGRESS_RESP,
                                                       GET_PROCESS_DETAILS_JOB_RESULTS_RESP,
                                                       GET_FACET_SEARCH_RESULTS_RESP,
                                                       EXPECTED_PROCESS_FACETS,
                                                       EXPECTED_PROCESS_RANGES_FACETS,
                                                       GET_PROCESS_TREE_STR,
                                                       GET_PROCESS_SUMMARY_STR)

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
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP)
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
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    actual = process.summary.__str__()

    process_info = {
        "device_id": 199106,
        "device_name": "w10prov1703x86",
        "parent_guid": "WNEXFKQ7-000309c2-000002c4-00000000-1d6a1c1f161a86a",
        "parent_hash": [
            "bd3036f60f1438c82900a29221e3a4912a89bfe904d01aad70c781ef514df0b3"
        ],
        "parent_name": "c:\\windows\\system32\\services.exe",
        "parent_pid": 708,
        "process_hash": [
            "a7296c1245ee76768d581c6330dade06",
            "5be0de7f915ba819d4ba048db7a2a87f6f3253fdd4865dc418181a0d6a031caa"
        ],
        "process_name": "c:\\windows\\system32\\svchost.exe",
        "process_pid": [1144]
    }
    sibling_info = {
        "process_guid": "WNEXFKQ7-000309c2-00000980-00000000-1d6a1c1f41ae014",
        "process_hash": [
            "b5a2c3084251ad5ce53e02f071fa7dc9",
            "ae600593a0a6915cf5ecbf96b4cb1d0e1d165339bde136c351bf606127c5dcec"
        ],
        "process_name": "c:\\windows\\carbonblack\\cb.exe",
        "process_pid": [2432]
    }
    parent_info = {
        "process_guid": "ABCD1234-0002b226-00000001-00000000-1d6225bbba75e43",
        "process_hash": [
            "e4b9902024ac32b3ca37f6b4c9b841e8",
            "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
        ],
        "process_name": "/usr/lib/systemd/systemd",
        "process_pid": [1]
    }
    child_info = {
        "process_guid": "WNEXFKQ7-000309c2-000004f8-00000000-1d6a88e80c541a3",
        "process_hash": [
            "2ae75e810f4dd1fb36607f66e7e1d80b",
            "db703055ec0641e7e96e22a62bf075547b480c51ea9e163d94e33452894b885c"
        ],
        "process_name": "c:\\windows\\system32\\wermgr.exe",
        "process_pid": [1272]
    }
    info = {
        'process:': process_info,
        'siblings (1):': sibling_info,
        'parent:': parent_info,
        'children (1):': child_info
    }
    lines = []
    for top in info:
        lines.append(top)
        for key in info[top]:
            val = str(info[top][key])
            lines.append(u"{0:s} {1:>20s}: {2:s}".format("    ", key, val))
        if top != 'process:' and top != 'parent:':
            lines.append("")

    expected = "\n".join(lines)
    assert actual == expected

    assert process.summary is not None
    assert process.siblings is not None
    summary = api.select(Process.Summary, guid)
    assert summary is not None


def test_summary_select(cbcsdk_mock):
    """Test querying for a Proc Summary."""
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
                             GET_PROCESS_SUMMARY_RESP)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    summary = api.select(Process.Summary).where(f"process_guid:{guid}")
    assert summary._perform_query() is not None
    assert isinstance(summary, SummaryQuery)
    summary._query_token = None
    summary._still_querying()


def test_summary_select_failures(cbcsdk_mock):
    """Test querying for a Proc Summary."""
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
                             GET_PROCESS_SUMMARY_RESP)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    summary = api.select(Process.Summary).where(f"process_guid:{guid}")
    assert isinstance(summary, SummaryQuery)
    with pytest.raises(ApiError) as ex:
        summary._count()
    assert 'The result is not iterable' in ex.value.message
    summary._query_token = 'something'
    with pytest.raises(ApiError) as ex:
        summary._submit()
    assert 'Query already submitted:' in ex.value.message
    summary._query_token = None
    with pytest.raises(ApiError) as ex:
        summary._run_async_query('someother')
    assert ex.value.message == 'Async query not properly started'


def test_summary_still_querying_zero(cbcsdk_mock):
    """Testing edge cases for _still_querying"""
    # mock the POST of a summary search (using same Job ID)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/summary_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check summary search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SUMMARY_RESP_ZERO_CONTACTED)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    summary = api.select(Process.Summary).where(f"process_guid:{guid}")
    assert summary._still_querying() is True


def test_summary_still_querying(cbcsdk_mock):
    """Testing edge cases for _still_querying"""
    # mock the POST of a summary search (using same Job ID)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/summary_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check summary search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SUMMARY_RESP_STILL_QUERYING)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    summary = api.select(Process.Summary).where(f"process_guid:{guid}")
    assert summary._still_querying() is True


def test_summary_select_set_time_range(cbcsdk_mock):
    """Test set_time_range for a Process Summary."""
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    summary = api.select(Process.Summary).where(f"process_guid:{guid}").where(f"parent_guid:{guid}")
    assert isinstance(summary, SummaryQuery)
    summary = summary.set_time_range(start="2020-01-21T18:34:04Z")
    summary = summary.set_time_range(end="2020-02-21T18:34:04Z")
    summary = summary.set_time_range(window="-1w")
    summary.timeout(1000)
    query_params = summary._get_query_parameters()
    expected = {'time_range': {'start': '2020-01-21T18:34:04Z', 'end': '2020-02-21T18:34:04Z', 'window': '-1w'},
                'process_guid': 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00',
                'parent_guid': 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'}

    assert query_params == expected


def test_summary_select_set_time_range_failures(cbcsdk_mock):
    """Test set_time_range failures for a Process Summary."""
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    summary = api.select(Process.Summary).where(f"process_guid:{guid}")

    with pytest.raises(ApiError) as ex:
        summary.set_time_range(start=50)
    assert 'Start time must be a string in ISO 8601 format.' in ex.value.message
    with pytest.raises(ApiError) as ex:
        summary.set_time_range(end=60)
    assert 'End time must be a string in ISO 8601 format.' in ex.value.message
    with pytest.raises(ApiError) as ex:
        summary.set_time_range(window=20)
    assert 'Window must be a string.' in ex.value.message


def test_process_events(cbcsdk_mock):
    """Testing Process.events()."""
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
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP)
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
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    assert isinstance(process.events(), Query)
    # create the events query object to compare
    events = process.events(event_type="modload").add_criteria("crossproc_action", ["ACTION_PROCESS_API_CALL"]) \
                                                 .add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    events.update_criteria("crossproc_action", "SOME_OTHER_CRIT")
    # emulate the manual select in Process.events()
    query = api.select(Event).where(process_guid=guid).add_criteria("crossproc_action", ["ACTION_PROCESS_API_CALL"]) \
                                                      .add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    query.update_criteria("crossproc_action", "SOME_OTHER_CRIT")
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
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    assert isinstance(process.events(), Query)
    # use a criteria value that's not a string or list
    with pytest.raises(ApiError):
        process.events(event_type="modload").add_criteria("crossproc_action", 0)
    # use an exclusion value that's not a string or list
    with pytest.raises(ApiError):
        process.events().add_exclusions("crossproc_effective_reputation", 0)


def test_process_with_criteria_exclusions(cbcsdk_mock):
    """Testing AsyncProcessQuery.add_criteria() and AsyncProcessQuery.add_exclusions()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions(
        "crossproc_effective_reputation", ["REP_WHITE"])
    process.timeout(1000)
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
    assert p.process_md5 == '12384336325dc8eadfb1e8ff876921c4'

    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       }}
    assert process_q_params == expected_params


def test_process_with_overwrite_criteria(cbcsdk_mock):
    """Testing AsyncProcessQuery.add_criteria() and AsyncProcessQuery.add_exclusions()."""
    api = cbcsdk_mock.api
    # use the update methods
    process_query = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234])

    process_query.add_criteria("device_id", [5678])

    query_params = process_query._get_query_parameters()
    assert query_params == {
        "query": "event_type:modload",
        "criteria": {
            "device_id": [5678]
        }
    }


def test_process_fields(cbcsdk_mock):
    """Testing AsyncProcessQuery.set_fields()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions(
        "crossproc_effective_reputation", ["REP_WHITE"])
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
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions(
        "crossproc_effective_reputation", ["REP_WHITE"])
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
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions(
        "crossproc_effective_reputation", ["REP_WHITE"])
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
                       "start": 10
                       }
    assert process_q_params == expected_params
    assert process._batch_size == 102


def test_process_sort(cbcsdk_mock):
    """Testing AsyncProcessQuery.sort_by()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions(
        "crossproc_effective_reputation", ["REP_WHITE"])
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


def test_process_events_query_with_criteria_exclusions(cbcsdk_mock):
    """Testing the add_criteria() method when selecting events."""
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
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    assert isinstance(process.events(), Query)
    # create the events query object to compare
    events = process.events(event_type="modload").add_criteria("crossproc_action", ["ACTION_PROCESS_API_CALL"]) \
                                                 .add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    events.update_criteria("crossproc_action", "SOME_OTHER_CRIT")
    events.add_exclusions("exclusion_key", "exclusion_value")
    # emulate the manual select in Process.events()
    query = api.select(Event).where(process_guid=guid).add_criteria("crossproc_action", ["ACTION_PROCESS_API_CALL"]) \
                                                      .add_exclusions("crossproc_effective_reputation", ["REP_WHITE"])
    query.update_criteria("crossproc_action", "SOME_OTHER_CRIT")
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


def test_process_events_raise_exceptions(cbcsdk_mock):
    """Testing raising an Exception when using Query.add_criteria() and Query.add_exclusions()."""
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
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    assert isinstance(process.events(), Query)
    # use a criteria value that's not a string or list
    with pytest.raises(ApiError):
        process.events(event_type="modload").add_criteria("crossproc_action", 0)
    # use an exclusion value that's not a string or list
    with pytest.raises(ApiError):
        process.events().add_exclusions("crossproc_effective_reputation", 0)


def test_process_query_with_criteria_exclusions(cbcsdk_mock):
    """Testing AsyncProcessQuery.add_criteria() and AsyncProcessQuery.add_exclusions()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions(
        "crossproc_effective_reputation", ["REP_WHITE"])
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
    assert p.process_md5 == '12384336325dc8eadfb1e8ff876921c4'

    process_q_params = process._get_query_parameters()
    expected_params = {"query": "event_type:modload",
                       "criteria": {
                           "device_id": [1234]
                       },
                       "exclusions": {
                           "crossproc_effective_reputation": ["REP_WHITE"]
                       }}
    assert process_q_params == expected_params


def test_process_query_set_fields(cbcsdk_mock):
    """Testing AsyncProcessQuery.set_fields()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions(
        "crossproc_effective_reputation", ["REP_WHITE"])
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


def test_process_query_time_range(cbcsdk_mock):
    """Testing AsyncProcessQuery.set_fields()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions(
        "crossproc_effective_reputation", ["REP_WHITE"])
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


def test_process_query_start_rows(cbcsdk_mock):
    """Testing AsyncProcessQuery.set_start() and AsyncProcessQuery.set_rows()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions(
        "crossproc_effective_reputation", ["REP_WHITE"])
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


def test_process_sort_by(cbcsdk_mock):
    """Testing AsyncProcessQuery.sort_by()."""
    api = cbcsdk_mock.api
    # use the update methods
    process = api.select(Process).where("event_type:modload").add_criteria("device_id", [1234]).add_exclusions(
        "crossproc_effective_reputation", ["REP_WHITE"])
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
                           GET_PROCESS_SEARCH_PARENT_JOB_RESULTS_RESP_1, False),
                          (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205",
                           GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1, True),
                          (GET_PROCESS_SUMMARY_RESP_2, "WNEXFKQ7-00050603-00000270-00000000-1d6c86e280fbff8",
                           GET_PROCESS_SEARCH_JOB_RESULTS_RESP_NO_PARENT_GUID, True)
                          ])
def test_process_parents(cbcsdk_mock, get_summary_response, guid, process_search_results, has_parent_process):
    """Testing Process.parents property/method."""
    api = cbcsdk_mock.api
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
                             process_search_results)
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
                             get_summary_response)
    # query for a Process
    process = api.select(Process, guid)
    # the process has a parent process (manually flagged)
    if has_parent_process:
        # Process.parents property returns a Process object, or [] if None
        assert isinstance(process.parents, Process)
        # query for a Process that has a guid == the guid of the parent process
        parent_process = api.select(Process).where(process_guid=process.parents.process_guid)

        parent_search_results = [process for process in parent_process]

        # check that the search for parent_process yields result consistent with the original process's parent
        assert parent_search_results[0].process_guid == process.parents.process_guid
    elif process.summary.parent:
        parent = process.summary.parent
        assert isinstance(parent, Process)
        assert process.parents == parent
    else:
        # the process has no parent
        assert process.parents == []


@pytest.mark.parametrize('get_summary_response, guid, expected_num_children', [
    (GET_PROCESS_SUMMARY_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00", 2),
    (GET_PROCESS_SUMMARY_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52", 3),
    (GET_PROCESS_SUMMARY_RESP_2, "test-003513bc-0000035c-00000000-1d640200c9a6205", 2),
    (GET_PROCESS_SUMMARY_RESP_NO_CHILDREN, "test-003513bc-0000035c-00000000-1d640200c9a6205", 0)])
def test_process_children(cbcsdk_mock, get_summary_response, guid, expected_num_children):
    """Testing Process.children property."""
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a process search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the POST of a summary search (using same Job ID)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/summary_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check process search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check summary search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SUMMARY_RESP)
    # mock the GET to get process search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get summary search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             get_summary_response)
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


@pytest.mark.parametrize('get_process_search_response, get_summary_response, guid, md5', [
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP, GET_PROCESS_SUMMARY_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00",
     "c7084336325dc8eadfb1e8ff876921c4"),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1, GET_PROCESS_SUMMARY_RESP_1,
     "test-00340b06-00000314-00000000-1d686b9e4d74f52",
     "12384336325dc8eadfb1e8ff876921c4"),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_3, GET_PROCESS_SUMMARY_RESP_2,
     "test-003513bc-0000035c-00000000-1d640200c9a6205",
     "45684336325dc8eadfb1e8ff876921c4"),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_3, GET_PROCESS_SUMMARY_RESP_NO_HASH,
     "test-003513bc-0000035c-00000000-1d640200c9a6205", None)])
def test_process_md5(cbcsdk_mock, get_process_search_response, get_summary_response, guid, md5):
    """Testing Process.process_md5 property."""
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a process search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check process search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get process search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             get_process_search_response)
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
                             get_summary_response)
    api = cbcsdk_mock.api
    process = api.select(Process, guid)
    if "process_hash" in process.summary._info["process"]:
        md5_hash = next((hash for hash in process.summary._info["process"]["process_hash"] if len(hash) == 32), None)
        assert process.process_md5 == md5_hash
    elif "process_hash" in process._info:
        assert process.process_md5 == md5
    else:
        assert process.process_md5 is None


def test_process_md5_not_found(cbcsdk_mock):
    """Testing error raising when receiving 404 for a Process."""
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a process search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the POST of a summary search (using same Job ID)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/summary_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check process search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check summary search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SUMMARY_RESP)
    # mock the GET to get process search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_NOT_FOUND)
    # mock the GET to get summary search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SUMMARY_NOT_FOUND)
    api = cbcsdk_mock.api
    process = api.select(Process, "someNonexistantGuid")
    with pytest.raises(ApiError):
        process.summary
    with pytest.raises(ApiError):
        process.tree


@pytest.mark.parametrize('get_process_response, get_summary_response, guid, sha256', [
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP, GET_PROCESS_SUMMARY_RESP,
     "test-0002b226-000015bd-00000000-1d6225bbba74c00",
     "5920199e4fbfa47c1717b863814722148a353e54f8c10912cf1f991a1c86309d"),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1, GET_PROCESS_SUMMARY_RESP_1,
     "test-00340b06-00000314-00000000-1d686b9e4d74f52",
     "d5e122606054fa0b03db3ee8cf9ea7701e523875e2bdb87581ad7232ffc9308e"),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_3, GET_PROCESS_SUMMARY_RESP_2,
     "test-003513bc-0000035c-00000000-1d640200c9a6205",
     "63d423ea882264dbb157a965c200306212fc5e1c6ddb8cbbb0f1d3b51ecd82e6"),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_3, GET_PROCESS_SUMMARY_RESP_NO_HASH,
     "test-003513bc-0000035c-00000000-1d640200c9a6205", None)])
def test_process_sha256(cbcsdk_mock, get_process_response, get_summary_response, guid, sha256):
    """Testing Process.process_sha256 property."""
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a process search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check process search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get process search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             get_process_response)
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
                             get_summary_response)
    api = cbcsdk_mock.api
    process = api.select(Process, guid)
    if "process_hash" in process.summary._info["process"]:
        sha256_hash = next((hash for hash in process.summary._info["process"]["process_hash"] if len(hash) == 64), None)
        assert process.process_sha256 == sha256_hash
    elif "process_hash" in process._info:
        assert process.process_sha256 == sha256
    else:
        assert process.process_sha256 is None


@pytest.mark.parametrize('get_process_response, get_summary_response, guid, pids', [
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP, GET_PROCESS_SUMMARY_RESP,
     "test-0002b226-000015bd-00000000-1d6225bbba74c00", [5653, 16139]),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1, GET_PROCESS_SUMMARY_RESP_1,
     "test-00340b06-00000314-00000000-1d686b9e4d74f52", [3909]),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_2, GET_PROCESS_SUMMARY_RESP_2,
     "test-003513bc-0000035c-00000000-1d640200c9a6205", [788]),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_NO_PID, GET_PROCESS_SUMMARY_RESP_2,
     "test-003513bc-0000035c-00000000-1d640200c9a6205", [788]),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_NO_PID, GET_PROCESS_SUMMARY_RESP_NO_PID,
     "test-003513bc-0000035c-00000000-1d640200c9a6205", None)])
def test_process_pids(cbcsdk_mock, get_process_response, get_summary_response, guid, pids):
    """Testing Process.process_pids property."""
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a process search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check process search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get process search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"),
                             get_process_response)
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
                             get_summary_response)
    api = cbcsdk_mock.api
    process = api.select(Process, guid)
    if "process_pid" in process.summary._info["process"]:
        assert process.process_pids == process.summary._info["process"]["process_pid"]
    assert process.process_pids == pids


def test_process_select_where(cbcsdk_mock):
    """Testing Process querying with where()."""
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
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process).where(f"process_guid:{guid}")
    assert isinstance(process, AsyncProcessQuery)
    process._count_valid = True
    assert process._count() == 0


def test_process_still_querying(cbcsdk_mock):
    """Testing Process"""
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_ZERO)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process).where(f"process_guid:{guid}")
    assert isinstance(process, AsyncProcessQuery)
    assert process._still_querying() is True


def test_process_still_querying_zero(cbcsdk_mock):
    """Testing Process"""
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process).where(f"process_guid:{guid}")
    assert isinstance(process, AsyncProcessQuery)
    assert process._still_querying() is True


def test_process_get_details(cbcsdk_mock):
    """Test get_details on a process."""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/detail_jobs",
                             POST_PROCESS_DETAILS_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/detail_jobs/ccc47a52-9a61-4c77-8652-8a03dc187b98",  # noqa: E501
                             GET_PROCESS_DETAILS_JOB_STATUS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/detail_jobs/ccc47a52-9a61-4c77-8652-8a03dc187b98/results",  # noqa: E501
                             GET_PROCESS_DETAILS_JOB_RESULTS_RESP)

    api = cbcsdk_mock.api
    process = Process(api, '80dab519-3b5f-4502-afad-da87cd58a4c3',
                      {'process_guid': '80dab519-3b5f-4502-afad-da87cd58a4c3'})
    results = process.get_details()
    assert results['process_guid'] == '80dab519-3b5f-4502-afad-da87cd58a4c3'
    assert results['process_cmdline'][0] == '/usr/bin/gitea'
    assert 10222 in results['process_pid']


def test_process_get_details_async(cbcsdk_mock):
    """Test get_details on a process in async mode."""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/detail_jobs",
                             POST_PROCESS_DETAILS_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/detail_jobs/ccc47a52-9a61-4c77-8652-8a03dc187b98",  # noqa: E501
                             GET_PROCESS_DETAILS_JOB_STATUS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/detail_jobs/ccc47a52-9a61-4c77-8652-8a03dc187b98/results",  # noqa: E501
                             GET_PROCESS_DETAILS_JOB_RESULTS_RESP)

    api = cbcsdk_mock.api
    process = Process(api, '80dab519-3b5f-4502-afad-da87cd58a4c3',
                      {'process_guid': '80dab519-3b5f-4502-afad-da87cd58a4c3'})
    future = process.get_details(0, True)
    results = future.result()
    assert results['process_guid'] == '80dab519-3b5f-4502-afad-da87cd58a4c3'
    assert results['process_cmdline'][0] == '/usr/bin/gitea'
    assert 10222 in results['process_pid']


def test_process_get_details_timeout(cbcsdk_mock):
    """Test the timeout of a get_details request."""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/detail_jobs",
                             POST_PROCESS_DETAILS_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/detail_jobs/ccc47a52-9a61-4c77-8652-8a03dc187b98",  # noqa: E501
                             GET_PROCESS_DETAILS_JOB_STATUS_IN_PROGRESS_RESP)
    api = cbcsdk_mock.api
    process = Process(api, '80dab519-3b5f-4502-afad-da87cd58a4c3',
                      {'process_guid': '80dab519-3b5f-4502-afad-da87cd58a4c3'})
    with pytest.raises(TimeoutError):
        process.get_details(1000)


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
    cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/processes/facet_jobs/the-job-id/results",
                             GET_FACET_SEARCH_RESULTS_RESP)
    future = facet_query.execute_async()
    res = future.result()
    assert res.terms_.fields == ['backend_timestamp', 'device_timestamp']
    assert res.terms_.facets == EXPECTED_PROCESS_FACETS
    assert isinstance(res.terms_, ProcessFacet.Terms)
    assert res.ranges_.fields == ['backend_timestamp']
    assert res.ranges_.facets == EXPECTED_PROCESS_RANGES_FACETS
    assert isinstance(res.ranges_, ProcessFacet.Ranges)
    # if already, submitted, the query shouldn't be submitted again
    with pytest.raises(ApiError):
        future = facet_query.execute_async()
        res = future.result()


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
    cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/processes/facet_jobs/the-job-id/results",
                             GET_FACET_SEARCH_RESULTS_RESP)
    api = cbcsdk_mock.api
    process = api.select(Process).where(process_guid="WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00")
    results = [proc for proc in process]
    process_facet_query = results[0].facets()
    assert isinstance(process_facet_query, FacetQuery)
    process_facet_query.add_facet_field(["backend_timestamp", "device_timestamp"])
    future = process_facet_query.execute_async()
    result = future.result()
    assert result.terms_.fields == ['backend_timestamp', 'device_timestamp']


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
    """Testing Process.Tree Querying"""
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
    # mock the Tree search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/summary_jobs", POST_TREE_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/summary_jobs"
                                     "/ee158f11-4dfb-4ae2-8f1a-7707b712226d"),
                             GET_TREE_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/summary_jobs/"
                                     "ee158f11-4dfb-4ae2-8f1a-7707b712226d/results"),
                             GET_PROCESS_TREE_STR)

    api = cbcsdk_mock.api
    guid = "WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00"
    process = api.select(Process, guid)
    tree = process.tree
    process_info = {
        "device_id": 176678,
        "device_name": "devr-dev",
        "process_hash": [
            "e4b9902024ac32b3ca37f6b4c9b841e8",
            "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
        ],
        "process_name": "/usr/lib/systemd/systemd",
        "process_pid": [1],
    }
    child_info = {
        "process_guid": "WNEXFKQ7-000309c2-00000454-00000000-1d6a2b6252ba18e",
        "process_hash": [
            "f9a3eee1c3a4067702bc9a59bc894285",
            "8e2aa014d7729cbfee95671717646ee480561f22e2147dae87a75c18d7369d99"
        ],
        "process_name": "c:\\windows\\system32\\msiexec.exe",
        "process_pid": [1108]
    }
    actual = tree.__str__()
    info = {
        'process:': process_info,
        'children (1):': child_info
    }
    lines = []
    for top in info:
        lines.append(top)
        for key in info[top]:
            val = str(info[top][key])
            lines.append(u"{0:s} {1:>20s}: {2:s}".format("    ", key, val))
        if top != 'process:':
            lines.append("")
    expected = "\n".join(lines)
    assert actual == expected
    children = tree.children
    assert len(children) == len(tree.children)
    assert len(children) > 0

    procTree = api.select(Process.Tree).where(process_guid="WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00")
    future = procTree.execute_async()
    results = future.result()[0]
    assert results is not None
    assert results.children is not None
    assert results.device_os is not None

    procTree = api.select(Process.Tree, "WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00")
    assert procTree is not None
