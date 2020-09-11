"""Testing Watchlist, Report, Feed objects of cbc_sdk.enterprise_edr"""

import pytest
import logging
from cbc_sdk.enterprise_edr import Watchlist, Report, Feed
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.enterprise_edr.mock_threatintel import (WATCHLIST_GET_RESP,
                                                               REPORT_GET_RESP,
                                                               FEED_GET_RESP,
                                                               FEED_GET_SPECIFIC_RESP)

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

def test_watchlist_query(cbcsdk_mock):
    """Testing Watchlist Querying"""
    cbcsdk_mock.mock_request("GET", "/threathunter/watchlistmgr/v2/watchlist", WATCHLIST_GET_RESP)
    api = cbcsdk_mock.api
    watchlist = api.select(Watchlist)
    results = [res for res in watchlist._perform_query()]
    assert results is not None
    assert isinstance(results[0], Watchlist)


def test_report_query(cbcsdk_mock):
    """Testing Report Querying"""
    feed_id = "rEVxDoWRAucNZI8utPRrQ"
    cbcsdk_mock.mock_request("GET", f"/threathunter/feedmgr/v2/orgs/test/feeds/{feed_id}/reports", REPORT_GET_RESP)
    api = cbcsdk_mock.api
    reports = api.select(Report).where(feed_id="rEVxDoWRAucNZI8utPRrQ")
    results = [res for res in reports._perform_query()]
    assert results is not None
    assert isinstance(results[0], Report)
    assert reports[0].iocs_ is not None


def test_feed_query_all(cbcsdk_mock):
    """Testing Feed Querying for all Feeds"""
    cbcsdk_mock.mock_request("GET", "/threathunter/feedmgr/v2/orgs/test/feeds", FEED_GET_RESP)
    api = cbcsdk_mock.api
    feed = api.select(Feed).where(include_public=True)
    results = [res for res in feed._perform_query()]
    assert isinstance(results[0], Feed)
    assert results[0].id is not None


def test_feed_query_specific(cbcsdk_mock):
    """Testing Feed Querying for specific Feed"""
    feed_id = "pv65TYVQy8YWMX9KsQUg"
    cbcsdk_mock.mock_request("GET", f"/threathunter/feedmgr/v2/orgs/test/feeds/{feed_id}", FEED_GET_SPECIFIC_RESP)
    api = cbcsdk_mock.api
    feed = api.select(Feed, "pv65TYVQy8YWMX9KsQUg")
    assert isinstance(feed, Feed)
    assert feed.id == "pv65TYVQy8YWMX9KsQUg"
