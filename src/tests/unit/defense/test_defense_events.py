"""Testing Event object of cbc_sdk.defense"""

import pytest
import logging
from cbc_sdk.defense import Event
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.defense.mock_events import (EVENT_GET_HOSTNAME_RESP,
                                                     EVENT_GET_SPECIFIC_RESP)

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

def test_event_query_0(cbcsdk_mock):
    """Testing Event Querying with .select(Event)"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/event", EVENT_GET_HOSTNAME_RESP)
    api = cbcsdk_mock.api
    events = api.select(Event).where('hostNameExact:Win7x64')
    results = [event for event in events._perform_query()]
    event = results[0]
    assert event.deviceDetails['deviceId'] == 43407
    assert event.deviceDetails['deviceName'] == 'Win7x64'


def test_event_query_with_id_in_select(cbcsdk_mock):
    """Testing Event Querying with .select(Event, `id`)"""
    url = "/integrationServices/v3/event/a1e12604d67b11ea920d3d9192a785d1"
    cbcsdk_mock.mock_request("GET", url, EVENT_GET_SPECIFIC_RESP)
    api = cbcsdk_mock.api
    event = api.select(Event, 'a1e12604d67b11ea920d3d9192a785d1')
    assert isinstance(event, Event)
    assert event.eventId == 'a1e12604d67b11ea920d3d9192a785d1'
    assert event.deviceDetails['deviceId'] == 43407
    assert event.deviceDetails['deviceName'] == 'Win7x64'
