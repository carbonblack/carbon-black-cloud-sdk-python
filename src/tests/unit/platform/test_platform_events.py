"""Testing Event object of cbc_sdk.platform"""

import pytest
import logging
from cbc_sdk.platform import Event, Process, EventFacet
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_events import (EVENT_SEARCH_VALIDATION_RESP,
                                                      EVENT_SEARCH_RESP_INTERIM,
                                                      EVENT_SEARCH_RESP,
                                                      EVENT_SEARCH_RESP_PART_ONE,
                                                      EVENT_SEARCH_RESP_PART_TWO,
                                                      EVENT_FACETS_RESP)
from tests.unit.fixtures.platform.mock_process import (GET_PROCESS_VALIDATION_RESP,
                                                       POST_PROCESS_SEARCH_JOB_RESP,
                                                       GET_PROCESS_SEARCH_JOB_RESP,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP)

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

def test_event_query_process_select_with_guid(cbcsdk_mock):
    """Test Event Querying with GUID inside process.select()"""
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
    guid = "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e"
    process = api.select(Process, guid)
    assert isinstance(process, Process)
    assert process.process_guid == guid

    search_validate_url = "/api/investigate/v1/orgs/test/events/search_validation"
    cbcsdk_mock.mock_request("GET", search_validate_url, EVENT_SEARCH_VALIDATION_RESP)
    url = r"/api/investigate/v2/orgs/test/events/J7G6DTLN\\-006633e3\\-00000334\\-00000000\\-1d677bedfbb1c2e/_search"
    cbcsdk_mock.mock_request("POST", url, EVENT_SEARCH_RESP_INTERIM)
    cbcsdk_mock.mock_request("POST", url, EVENT_SEARCH_RESP)

    events = [event for event in process.events()]
    assert events[0].process_guid == guid


def test_event_query_select_with_guid(cbcsdk_mock):
    """Test Event Querying with GUID inside event.select()"""
    api = cbcsdk_mock.api
    guid = "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e"
    events = api.select(Event, guid)
    assert events.process_guid == guid


def test_event_query_select_with_where(cbcsdk_mock):
    """Test Event Querying with where() clause"""
    search_validate_url = "/api/investigate/v1/orgs/test/events/search_validation"
    cbcsdk_mock.mock_request("GET", search_validate_url, EVENT_SEARCH_VALIDATION_RESP)

    url = r"/api/investigate/v2/orgs/test/events/J7G6DTLN\\-006633e3\\-00000334\\-00000000\\-1d677bedfbb1c2e/_search"
    cbcsdk_mock.mock_request("POST", url, EVENT_SEARCH_RESP)

    api = cbcsdk_mock.api
    guid = "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e"

    # test .where(process_guid=...)
    events = api.select(Event).where(process_guid=guid)
    results = [res for res in events._perform_query(numrows=10)]
    assert len(results) == 10
    first_event = results[0]
    assert first_event.process_guid == guid

    # test .where('process_guid:...')
    url = "/api/investigate/v2/orgs/test/events/J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e/_search"
    cbcsdk_mock.mock_request("POST", url, EVENT_SEARCH_RESP)
    events = api.select(Event).where('process_guid:J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e')
    results = [res for res in events._perform_query(numrows=10)]
    first_event = results[0]
    assert first_event.process_guid == guid

    # test ._perform_query(numrows)
    assert len(results) == 10

    # test ._perform_query(numrows)
    results = [result for result in events._perform_query(numrows=100)]
    assert len(results) == 100
    first_result = results[0]
    assert first_result.process_guid == guid


def test_event_query_select_asynchronous(cbcsdk_mock):
    """Test Event Querying with where() clause as asynchronous"""
    search_validate_url = "/api/investigate/v1/orgs/test/events/search_validation"
    cbcsdk_mock.mock_request("GET", search_validate_url, EVENT_SEARCH_VALIDATION_RESP)

    url = r"/api/investigate/v2/orgs/test/events/J7G6DTLN\\-006633e3\\-00000334\\-00000000\\-1d677bedfbb1c2e/_search"
    cbcsdk_mock.mock_request("POST", url, EVENT_SEARCH_RESP)

    api = cbcsdk_mock.api
    guid = "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e"

    events = api.select(Event).where(process_guid=guid)
    future = events.execute_async()
    results = future.result()
    assert len(results) == 250  # we get all of them when we run in background
    first_event = results[0]
    assert first_event['process_guid'] == guid


def test_event_query_with_multiple_fetches(cbcsdk_mock):
    """Test event query for multiple network requests"""
    http_request_count = 0

    def _fake_multiple_fetches(url, body, **kwargs):
        nonlocal http_request_count

        if http_request_count == 0:
            http_request_count += 1
            return EVENT_SEARCH_RESP_PART_ONE
        else:
            assert body['start'] == 1
            return EVENT_SEARCH_RESP_PART_TWO

    search_validate_url = "/api/investigate/v1/orgs/test/events/search_validation"
    cbcsdk_mock.mock_request("GET", search_validate_url, EVENT_SEARCH_VALIDATION_RESP)

    url = r"/api/investigate/v2/orgs/test/events/J7G6DTLN\\-006633e3\\-00000334\\-00000000\\-1d677bedfbb1c2e/_search"
    cbcsdk_mock.mock_request("POST", url, _fake_multiple_fetches)

    api = cbcsdk_mock.api
    guid = "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e"
    event_query = api.select(Event).where(process_guid=guid)
    events = [ev for ev in event_query]
    assert len(events) == 3


def test_event_facet_query(cbcsdk_mock):
    """Test event facet querying"""
    # mock the POST of an event facet search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/events/"
                             "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e/_facet",
                             EVENT_FACETS_RESP)
    api = cbcsdk_mock.api
    event_facet_query = api.select(EventFacet).add_facet_field("event_type")
    event_facet_query.where("process_guid:J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e")
    facets = event_facet_query.results
    assert isinstance(facets, EventFacet)
