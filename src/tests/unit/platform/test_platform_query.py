"""Testing Query object of cbc_sdk.enterprise_edr"""

import pytest
import logging
import time
from cbc_sdk.platform import Process, Event, ProcessFacet
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_process import (GET_PROCESS_SUMMARY_RESP,
                                                       GET_PROCESS_SUMMARY_RESP_1,
                                                       POST_PROCESS_VALIDATION_RESP,
                                                       POST_PROCESS_VALIDATION_RESP_INVALID,
                                                       POST_PROCESS_SEARCH_JOB_RESP,
                                                       GET_PROCESS_SEARCH_JOB_RESP,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1,
                                                       GET_FACET_SEARCH_RESULTS_RESP,
                                                       GET_FACET_SEARCH_RESULTS_RESP_1,
                                                       GET_FACET_SEARCH_RESULTS_RESP_NOT_COMPLETE)

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

@pytest.mark.parametrize('get_summary_response, get_process_search_response, guid', [
    (GET_PROCESS_SUMMARY_RESP, GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
     "test-0002b226-000015bd-00000000-1d6225bbba74c00",),
    (GET_PROCESS_SUMMARY_RESP_1, GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1,
     "test-00340b06-00000314-00000000-1d686b9e4d74f52",)])
def test_query_count(cbcsdk_mock, get_summary_response, get_process_search_response, guid):
    """Testing Process.process_pids property."""
    api = cbcsdk_mock.api
    # mock the GET of query parameter validation
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_validation",
                             POST_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=0"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results"),
                             get_process_search_response)
    process_query = api.select(Process).where(f"process_guid:{guid}")
    # Query._count() returns `num_available` from the JSON response to a process query
    assert process_query._count() == 1
    assert process_query._count_valid is True


@pytest.mark.parametrize('get_process_search_response, guid', [
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00",),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52",)])
def test_query_get_query_parameters(cbcsdk_mock, get_process_search_response, guid):
    """Testing Query._get_query_parameters()."""
    api = cbcsdk_mock.api
    # mock the GET of query parameter validation
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_validation",
                             POST_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST",
                             "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/search_jobs/"
                             "2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=0",
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/search_jobs/"
                             "2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=500",
                             get_process_search_response)
    process_query = api.select(Process).where(f"process_guid:{guid}")
    assert process_query._get_query_parameters() == {"process_guid": guid, "query": f'process_guid:{guid}'}


@pytest.mark.parametrize('get_process_search_response, guid', [
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00",),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52",)])
def test_query_validate_not_valid(cbcsdk_mock, get_process_search_response, guid):
    """Testing Query._validate()."""
    api = cbcsdk_mock.api
    # mock the GET of query parameter validation
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_validation",
                             POST_PROCESS_VALIDATION_RESP_INVALID)

    process_query = api.select(Process).where(f"process_guid:{guid}")
    with pytest.raises(ApiError):
        params = process_query._get_query_parameters()
        process_query._validate(params)


def test_query_set_fields_exception(cbcsdk_mock):
    """Testing raising ApiError in Query.set_fields()."""
    api = cbcsdk_mock.api
    event = api.select(Event)
    assert event._fields == ["*"]
    event.set_fields(["event_type"])
    assert event._get_query_parameters()["fields"] == ["event_type"]
    event.set_fields("another_field")
    assert event._get_query_parameters()["fields"] == ["another_field"]
    with pytest.raises(ApiError):
        event.set_fields(0)


def test_query_set_start_exception(cbcsdk_mock):
    """Testing raising ApiError in Query.set_start()."""
    api = cbcsdk_mock.api
    event = api.select(Event)
    assert event._start == 0
    event.set_start(5)
    assert event._get_query_parameters()["start"] == 5
    with pytest.raises(ApiError):
        event.set_start('not_an_integer')


def test_query_set_rows(cbcsdk_mock):
    """Testing raising ApiError in Query.set_rows()."""
    api = cbcsdk_mock.api
    event = api.select(Event)
    assert event._batch_size == 500
    event.set_rows(10)
    assert event._get_query_parameters()["rows"] == 10
    with pytest.raises(ApiError):
        event.set_rows("not_an_integer")


def test_query_set_time_range(cbcsdk_mock):
    """Testing raising ApiError in Query.set_time_range()."""
    api = cbcsdk_mock.api
    event = api.select(Event)
    assert "time_range" not in event._get_query_parameters()
    event.set_time_range(start="2020-10-30T20:34:07")
    assert event._get_query_parameters()["time_range"] == {"start": "2020-10-30T20:34:07"}
    event.set_time_range(end="2020-10-31T20:34:07")
    assert event._get_query_parameters()["time_range"] == {"start": "2020-10-30T20:34:07",
                                                           "end": "2020-10-31T20:34:07"}
    event.set_time_range(window="-4h")
    assert event._get_query_parameters()["time_range"] == {"start": "2020-10-30T20:34:07",
                                                           "end": "2020-10-31T20:34:07",
                                                           "window": "-4h"}
    with pytest.raises(ApiError):
        event.set_time_range(start=1)
    with pytest.raises(ApiError):
        event.set_time_range(end=9)
    with pytest.raises(ApiError):
        event.set_time_range(window=100)


def test_async_sort_by(cbcsdk_mock):
    """Testing AsyncProcessQuery.sort_by()."""
    api = cbcsdk_mock.api
    async_query = api.select(Process).where("process_guid:someguid")
    # add one key to sort by
    assert async_query._sort_by == []
    async_query.sort_by("device_timestamp", direction="ASC")
    assert async_query._sort_by == [{"field": "device_timestamp", "order": "ASC"}]
    assert async_query._default_args == {"sort": [{"field": "device_timestamp", "order": "ASC"}]}
    # add another key to sort by
    async_query.sort_by("key_to_sort_by", direction="DESC")
    assert async_query._sort_by == [{"field": "device_timestamp", "order": "ASC"},
                                    {"field": "key_to_sort_by", "order": "DESC"}]
    assert async_query._default_args == {"sort": [{"field": "device_timestamp", "order": "ASC"},
                                                  {"field": "key_to_sort_by", "order": "DESC"}]}
    # update the sort direction for a field
    async_query.sort_by("key_to_sort_by", direction="ASC")
    assert async_query._sort_by == [{"field": "device_timestamp", "order": "ASC"},
                                    {"field": "key_to_sort_by", "order": "ASC"}]
    assert async_query._default_args == {"sort": [{"field": "device_timestamp", "order": "ASC"},
                                                  {"field": "key_to_sort_by", "order": "ASC"}]}


def test_async_timeout(cbcsdk_mock):
    """Testing AsyncProcessQuery.timeout()."""
    api = cbcsdk_mock.api
    async_query = api.select(Process).where("process_guid:someguid")
    assert async_query._timeout == 0
    async_query.timeout(msecs=500)
    assert async_query._timeout == 500


def test_async_submit(cbcsdk_mock):
    """Testing AsyncProcessQuery._submit()."""
    api = cbcsdk_mock.api
    async_query = api.select(Process).where("process_guid:someguid")
    async_query._query_token = "the_job_id_because_this_query_was_already_submitted"
    with pytest.raises(ApiError):
        async_query._submit()


@pytest.mark.parametrize('get_summary_response, get_process_search_response, guid, pid', [
    (GET_PROCESS_SUMMARY_RESP, GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
     "test-0002b226-000015bd-00000000-1d6225bbba74c00", 5653),
    (GET_PROCESS_SUMMARY_RESP_1, GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1,
     "test-00340b06-00000314-00000000-1d686b9e4d74f52", 3909)])
def test_query_execute_async(cbcsdk_mock, get_summary_response, get_process_search_response, guid, pid):
    """Testing Process.process_pids property."""
    api = cbcsdk_mock.api
    # mock the GET of query parameter validation
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_validation",
                             POST_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_jobs",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/search_jobs/"
                             "2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=0",
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/search_jobs/"
                             "2c292717-80ed-4f0d-845f-779e09470920/results?start=0&rows=500",
                             get_process_search_response)
    process_query = api.select(Process).where(f"process_guid:{guid}")
    future = process_query.execute_async()
    results = future.result()
    assert len(results) == 1
    assert results[0]['process_pid'][0] == pid


def test_async_facet_query_timeout(cbcsdk_mock):
    """Testing AsyncFacetQuery timeout()"""
    api = cbcsdk_mock.api
    facet_query = api.select(ProcessFacet).where("process_name:svchost.exe")
    assert facet_query._timeout == 0
    facet_query.timeout(5000)
    assert facet_query._timeout == 5000


def test_async_facet_limit(cbcsdk_mock):
    """Testing AsyncFacetQuery timeout()"""
    api = cbcsdk_mock.api
    facet_query = api.select(ProcessFacet).where("process_name:svchost.exe")
    assert facet_query._limit is None
    facet_query.limit(50)
    assert facet_query._limit == 50


def test_async_facet_field(cbcsdk_mock):
    """Testing AsyncFacetQuery add_facet_field()"""
    api = cbcsdk_mock.api
    facet_query = api.select(ProcessFacet).where("process_name:svchost.exe")
    assert facet_query._facet_fields == []
    facet_query.add_facet_field("my_field")
    assert facet_query._facet_fields == ["my_field"]
    facet_query.add_facet_field(["another", "third_field"])
    assert facet_query._facet_fields == ["my_field", "another", "third_field"]


def test_async_facet_ranges(cbcsdk_mock):
    """Testing AsyncFacetQuery add_range()"""
    api = cbcsdk_mock.api
    facet_query = api.select(ProcessFacet).where("process_name:svchost.exe")
    assert facet_query._ranges == []
    facet_query.add_range({"bucket_size": 5, "start": 0, "end": 10, "field": "netconn_count"})
    assert facet_query._ranges == [{"bucket_size": 5, "start": 0, "end": 10, "field": "netconn_count"}]
    facet_query.add_range([{"bucket_size": 50, "start": 10, "end": 100, "field": "second_field"},
                           {"bucket_size": 5, "start": 0, "end": 1000, "field": "another_field"}])
    assert facet_query._ranges == [{"bucket_size": 5, "start": 0, "end": 10, "field": "netconn_count"},
                                   {"bucket_size": 50, "start": 10, "end": 100, "field": "second_field"},
                                   {"bucket_size": 5, "start": 0, "end": 1000, "field": "another_field"}]


def test_async_facet_query_still_querying(cbcsdk_mock):
    """Testing AsyncFacetQuery._still_querying()."""
    api = cbcsdk_mock.api
    facet_query = api.select(ProcessFacet).where("process_name:svchost.exe").add_facet_field("device_name")
    # mock the search request
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/facet_jobs", {"job_id": "the-job-id"})
    # mock the result call, with 0 contacted and 0 completed
    cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/processes/facet_jobs/the-job-id/results",
                             GET_FACET_SEARCH_RESULTS_RESP_1)
    # with 0 searchers contacted, the query is still running
    assert facet_query._still_querying() is True
    # if a query hasn't timed out, and num_conacted != num_completed, the query is still running
    facet_query.timeout(60000)
    # mock another result call with num_conacted != num_completed
    cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/processes/facet_jobs/the-job-id/results",
                             GET_FACET_SEARCH_RESULTS_RESP_NOT_COMPLETE)
    assert facet_query._still_querying() is True
    # force a timeout, and the query should be over
    facet_query.timeout(1)
    time.sleep(0.5)
    assert facet_query._timeout == 1
    assert (time.time() * 1000) - facet_query._submit_time > facet_query._timeout
    cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/processes/facet_jobs/the-job-id/results",
                             GET_FACET_SEARCH_RESULTS_RESP_NOT_COMPLETE)
    assert facet_query._still_querying() is False
    assert facet_query._timed_out is True


def test_async_facet_get_query_params(cbcsdk_mock):
    """Testing AsyncFacetQuery._get_query_parameters()."""
    api = cbcsdk_mock.api
    # query without facet fields is invalid
    facet_query = api.select(ProcessFacet).where("process_name:svchost.exe")
    with pytest.raises(ApiError):
        facet_query._get_query_parameters()
    facet_query = api.select(ProcessFacet).add_facet_field("device_name")
    # query with rows
    facet_query.set_rows(500)
    assert facet_query._get_query_parameters()["terms"]["rows"] == 500
    # query with criteria
    facet_query.add_criteria("device_name", "my_device_name")
    assert facet_query._get_query_parameters()["criteria"] == {"device_name": ["my_device_name"]}
    # query with exclusions
    facet_query.add_exclusions("device_name", "my_device_name")
    assert facet_query._get_query_parameters()["exclusions"] == {"device_name": ["my_device_name"]}
    # query with process_guid in a where() stmt
    facet_query.where("process_guid:myguid")
    assert facet_query._get_query_parameters()["query"] == "process_guid:myguid"


def test_async_facet_count(cbcsdk_mock):
    """Testing AsyncFacetQuery._count()."""
    api = cbcsdk_mock.api
    facet_query = api.select(ProcessFacet).add_facet_field("device_name")
    # mock the search request
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/facet_jobs", {"job_id": "the-job-id"})
    # mock the result call, with 0 contacted and 0 completed
    cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/processes/facet_jobs/the-job-id/results",
                             GET_FACET_SEARCH_RESULTS_RESP)
    assert facet_query._count() == 23753
    assert facet_query._count_valid
    assert facet_query._count() == facet_query._total_results


def test_async_facet_query(cbcsdk_mock):
    """Testing AsyncFacetQuery execution."""
    api = cbcsdk_mock.api
    facet_query = api.select(ProcessFacet).add_facet_field(["device_timestamp", "backend_timestamp"])
    # mock the search request
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/facet_jobs", {"job_id": "the-job-id"})
    # mock the result call, with 0 contacted and 0 completed
    cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/processes/facet_jobs/the-job-id/results",
                             GET_FACET_SEARCH_RESULTS_RESP)

    results = facet_query.results
    assert isinstance(results, ProcessFacet)
    assert results.terms_.fields == ["backend_timestamp", "device_timestamp"]
