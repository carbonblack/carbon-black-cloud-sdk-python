"""Testing EnrichedEvent objects of cbc_sdk.endpoint_standard"""

import pytest
import logging
from cbc_sdk.endpoint_standard import EnrichedEvent, EnrichedEventQuery
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_enriched_events import (POST_ENRICHED_EVENTS_SEARCH_JOB_RESP,
                                                                        GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP,
                                                                        GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_1,
                                                                        GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_2,
                                                                        GET_ENRICHED_EVENTS_AGG_JOB_RESULTS_RESP_1)
                                                                        GET_ENRICHED_EVENTS_DETAIL_JOB_RESULTS_RESP_1,
                                                                        )

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

def test_enriched_event_select_where(cbcsdk_mock):
    """Testing EnrichedEvent Querying with select()"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_2)

    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(event_id="27a278d5150911eb86f1011a55e73b72")
    for event in events:
        assert event.device_name is not None
        assert event.enriched is not None


def test_enriched_event_select_async(cbcsdk_mock):
    """Testing EnrichedEvent Querying with select() - asynchronous way"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_2)

    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(event_id="27a278d5150911eb86f1011a55e73b72").execute_async()
    for event in events.result():
        assert event["device_name"] is not None
        assert event["enriched"] is not None


def test_enriched_event_select_details_async(cbcsdk_mock):
    """Testing EnrichedEvent Querying with get_details - asynchronous mode"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_1)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_DETAIL_JOB_RESULTS_RESP_1)

    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(process_pid=2000)
    event = events[0]
    details = event.get_details(async_mode=True, timeout=500)
    results = details.result()
    assert event._details_timeout == 500
    assert results["device_name"] is not None
    assert results["enriched"] is not None
    assert results["process_pid"][0] == 2000


def test_enriched_event_details_only(cbcsdk_mock):
    """Testing EnrichedEvent with get_details - just the get_details REST API calls"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_DETAIL_JOB_RESULTS_RESP_1)

    api = cbcsdk_mock.api
    event = EnrichedEvent(api, initial_data={'event_id': 'test'})
    results = event._get_detailed_results()
    assert results._info["device_name"] is not None
    assert results._info["enriched"] is not None
    assert results._info["process_pid"][0] == 2000


def test_enriched_event_select_details_sync(cbcsdk_mock):
    """Testing EnrichedEvent Querying with get_details"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_1)
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_DETAIL_JOB_RESULTS_RESP_1)

    s_api = cbcsdk_mock.api
    events = s_api.select(EnrichedEvent).where(process_pid=2000)
    event = events[0]
    results = event.get_details()
    assert results["device_name"] is not None
    assert results["enriched"] is True
    assert results["process_pid"][0] == 2000


def test_enriched_event_select_compound(cbcsdk_mock):
    """Testing EnrichedEvent Querying with select() and more complex criteria"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_1)

    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(process_pid=1000).or_(process_pid=1000)
    for event in events:
        assert event.device_name is not None
        assert event.enriched is not None


def test_enriched_event_select_aggregation(cbcsdk_mock):
    """Testing EnrichedEvent Querying with select() and more complex criteria"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v1/orgs/test/enriched_events/aggregation_jobs/process_sha256",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/enriched_events/aggregation_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_AGG_JOB_RESULTS_RESP_1)

    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(process_pid=2000).aggregation("process_sha256")
    assert events._aggregation is True
    assert events._aggregation_field == "process_sha256"
    for event in events:
        assert event.device_name is not None
        assert event.enriched is not None
        assert event.process_pid[0] == 2000


def test_enriched_event_query_implementation(cbcsdk_mock):
    """Testing EnrichedEvent querying with where()."""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_2)
    api = cbcsdk_mock.api
    event_id = '27a278d5150911eb86f1011a55e73b72'
    events = api.select(EnrichedEvent).where(f"event_id:{event_id}")
    assert isinstance(events, EnrichedEventQuery)
    assert events[0].event_id == '27a278d5150911eb86f1011a55e73b72'


def test_enriched_event_timeout(cbcsdk_mock):
    """Testing EnrichedEventQuery.timeout()."""
    api = cbcsdk_mock.api
    query = api.select(EnrichedEvent).where("event_id:some_id")
    assert query._timeout == 0
    query.timeout(msecs=500)
    assert query._timeout == 500


def test_enriched_event_query_sort(cbcsdk_mock):
    """Testing EnrichedEvent results sort."""
    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(process_pid=1000).or_(process_pid=1000).sort_by("process_pid",
                                                                                             direction="DESC")
    assert events._sort == [{"field": "process_pid", "order": "DESC"}]


def test_enriched_event_rows(cbcsdk_mock):
    """Testing EnrichedEvent results sort."""
    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(process_pid=1000).set_rows(1500)
    assert events._rows == 1500


def test_enriched_event_time_range(cbcsdk_mock):
    """Testing EnrichedEvent results sort."""
    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(process_pid=1000).set_time_range(start="2020-10-10T20:34:07Z",
                                                                              end="2020-10-20T20:34:07Z",
                                                                              window="-1d")
    assert events._time_range["start"] == "2020-10-10T20:34:07Z"
    assert events._time_range["end"] == "2020-10-20T20:34:07Z"
    assert events._time_range["window"] == "-1d"


def test_enriched_events_submit(cbcsdk_mock):
    """Test _submit method of enrichedeventquery class"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(process_pid=1000)
    events._submit()
    assert events._query_token == "08ffa932-b633-4107-ba56-8741e929e48b"


def test_enriched_events_count(cbcsdk_mock):
    """Test _submit method of enrichedeventquery class"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_2)

    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(process_pid=1000)
    events._count()
    assert events._count() == 52


def test_enriched_events_search(cbcsdk_mock):
    """Test _search method of enrichedeventquery class"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_2)

    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(process_pid=1000)
    events._search()
    assert events[0].process_pid[0] == 1000
