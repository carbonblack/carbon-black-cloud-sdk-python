"""Testing Process and Tree objects of cbc_sdk.enterprise_edr"""

import pytest
import logging
from cbc_sdk.enterprise_edr import EnrichedEvent, Query, AsyncEventQuery
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ObjectNotFoundError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.enterprise_edr.mock_enriched_events import (POST_ENRICHED_EVENTS_SEARCH_JOB_RESP,
                                                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP,
                                                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_1,
                                                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_2)


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
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job", POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b", GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results", GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_2)

    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(event_id="27a278d5150911eb86f1011a55e73b72")
    for event in events:
        assert event.device_name is not None
        assert event.enriched is not None

def test_enriched_event_select_compound(cbcsdk_mock):
    """Testing EnrichedEvent Querying with select() and more complex criteria"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job", POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b", GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET", "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results", GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_1)

    api = cbcsdk_mock.api
    events = api.select(EnrichedEvent).where(process_pid=1000).or_(process_pid=1000)
    for event in events:
        assert event.device_name is not None
        assert event.enriched is not None

def test_enriched_event_query_implementation(cbcsdk_mock):
    """Testing EnrichedEvent querying with where()."""
    api = cbcsdk_mock.api
    event_id = '27a278d5150911eb86f1011a55e73b72'
    event = api.select(EnrichedEvent).where(f"event_id:{event_id}")
    assert isinstance(event, AsyncEventQuery)
