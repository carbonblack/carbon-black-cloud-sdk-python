"""Testing Watchlist, Report, Feed objects of cbc_sdk.enterprise_edr"""

import pytest
import logging
from cbc_sdk.enterprise_edr import Watchlist, Report, Feed
from cbc_sdk.errors import InvalidObjectError, ApiError
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.enterprise_edr.mock_threatintel import (WATCHLIST_GET_RESP,
                                                                 WATCHLIST_GET_SPECIFIC_RESP,
                                                                 WATCHLIST_GET_SPECIFIC_MISSING_FIELDS_RESP,
                                                                 WATCHLIST_GET_SPECIFIC_INVALID_CLASSIFIER_RESP,
                                                                 CREATE_WATCHLIST_DATA,
                                                                 REPORT_GET_RESP,
                                                                 FEED_GET_RESP,
                                                                 FEED_GET_SPECIFIC_RESP,
                                                                 FEED_GET_SPECIFIC_FROM_WATCHLIST_RESP)

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


def test_watchlist_init(cbcsdk_mock):
    """Testing Watchlist.__init__()."""
    id = "watchlistId"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}", WATCHLIST_GET_SPECIFIC_RESP)
    watchlist = Watchlist(cbcsdk_mock.api, model_unique_id="watchlistId", initial_data=None)
    assert watchlist._model_unique_id == "watchlistId"


def test_watchlist_save(cbcsdk_mock):
    """Testing Watchlist.save()."""
    api = cbcsdk_mock.api
    id = "watchlistId"
    cbcsdk_mock.mock_request("POST", "/threathunter/watchlistmgr/v3/orgs/test/watchlists", WATCHLIST_GET_SPECIFIC_RESP)
    watchlist = Watchlist(api, model_unique_id="watchlistId", initial_data=CREATE_WATCHLIST_DATA)
    watchlist.validate()
    watchlist.save()

    # if Watchlist response is missing a required field per enterprise_edr.models.Watchlist, raise InvalidObjectError
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}",
                             WATCHLIST_GET_SPECIFIC_MISSING_FIELDS_RESP)
    watchlist = api.select(Watchlist, "watchlistId")
    with pytest.raises(InvalidObjectError):
        watchlist.validate()
    with pytest.raises(InvalidObjectError):
        watchlist.save()


def test_watchlist_update(cbcsdk_mock):
    """Testing Watchlist.update()."""
    id = "watchlistId"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}", WATCHLIST_GET_SPECIFIC_RESP)
    watchlist = Watchlist(cbcsdk_mock.api, model_unique_id="watchlistId", initial_data=None)
    assert "description" in watchlist._info
    assert "nonexistant_key" not in watchlist._info
    assert watchlist._info["description"] == "Existing description for the watchlist."
    cbcsdk_mock.mock_request("PUT", f"/threathunter/watchlistmgr/v3/orgs/test/watchlists/{id}",
                             WATCHLIST_GET_SPECIFIC_RESP)
    watchlist.update(description="My New Description", nonexistant_key="This Is Ignored")
    assert watchlist._info["description"] == "My New Description"


def test_watchlist_update_invalid_object(cbcsdk_mock):
    """Testing Watchlist.update() raising InvalidObjectError when Watchlist ID is missing."""
    watchlist = Watchlist(cbcsdk_mock.api, model_unique_id=None, initial_data=None)
    with pytest.raises(InvalidObjectError):
        watchlist.update(nonexistant_key="This is ignored")


def test_watchlist_update_api_error(cbcsdk_mock):
    """Testing Watchlist.update() raising ApiError when passing in "report_ids" with empty list."""
    id = "watchlistId"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}", WATCHLIST_GET_SPECIFIC_RESP)
    watchlist = Watchlist(cbcsdk_mock.api, model_unique_id="watchlistId", initial_data=None)
    cbcsdk_mock.mock_request("PUT", f"/threathunter/watchlistmgr/v3/orgs/test/watchlists/{id}",
                             WATCHLIST_GET_SPECIFIC_RESP)
    with pytest.raises(ApiError):
        watchlist.update(report_ids=[])


def test_watchlist_classifier(cbcsdk_mock):
    """Testing Watchlist.classifier_ property."""
    watchlist = Watchlist(cbcsdk_mock.api, model_unique_id="watchlistId", initial_data=WATCHLIST_GET_SPECIFIC_RESP)
    assert watchlist.classifier_ == ("feed_id", "feed_id_associated")


def test_watchlist_classifier_empty(cbcsdk_mock):
    """Testing Watchlist.classifier_ when "classifier" is not in self._info."""
    watchlist = Watchlist(cbcsdk_mock.api)
    assert "classifier" not in watchlist._info
    assert watchlist.classifier_ is None


def test_watchlist_delete(cbcsdk_mock):
    """Testing Watchlist.delete()."""
    id = "watchlistId"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}", WATCHLIST_GET_SPECIFIC_RESP)
    cbcsdk_mock.mock_request("DELETE", f"/threathunter/watchlistmgr/v3/orgs/test/watchlists/{id}", None)
    watchlist = Watchlist(cbcsdk_mock.api, model_unique_id="watchlistId")
    watchlist.delete()


def test_watchlist_delete_no_id(cbcsdk_mock):
    """Testing Watchlist.delete() raising InvalidObjectError when ID is missing."""
    watchlist = Watchlist(cbcsdk_mock.api, model_unique_id=None)
    with pytest.raises(InvalidObjectError):
        watchlist.delete()


def test_enable_alerts(cbcsdk_mock):
    """Testing Watchlist.enable_alerts()."""
    api = cbcsdk_mock.api
    id = "watchlistId"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}", WATCHLIST_GET_SPECIFIC_RESP)
    watchlist = Watchlist(api, model_unique_id="watchlistId")
    cbcsdk_mock.mock_request("PUT", f"/threathunter/watchlistmgr/v3/orgs/test/watchlists/{id}/alert", {"alert": True})
    watchlist.enable_alerts()


def test_enable_alerts_no_id(cbcsdk_mock):
    """Testing Watchlist.enable_alerts() raising InvalidObjectError when ID is missing."""
    api = cbcsdk_mock.api
    watchlist = Watchlist(api, model_unique_id=None)
    with pytest.raises(InvalidObjectError):
        watchlist.enable_alerts()


def test_disable_alerts(cbcsdk_mock):
    """Testing Watchlist.disable_alerts()."""
    api = cbcsdk_mock.api
    id = "watchlistId"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}", WATCHLIST_GET_SPECIFIC_RESP)
    watchlist = Watchlist(api, model_unique_id="watchlistId")
    cbcsdk_mock.mock_request("DELETE", f"/threathunter/watchlistmgr/v3/orgs/test/watchlists/{id}/alert", None)
    watchlist.disable_alerts()


def test_disable_alerts_no_id(cbcsdk_mock):
    """Testing Watchlist.disable_alerts() raising InvalidObjectError when ID is missing."""
    api = cbcsdk_mock.api
    watchlist = Watchlist(api, model_unique_id=None)
    with pytest.raises(InvalidObjectError):
        watchlist.disable_alerts()


def test_watchlist_enable_tags(cbcsdk_mock):
    """Testing Watchlist.enable_tags()."""
    api = cbcsdk_mock.api
    id = "watchlistId"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}", WATCHLIST_GET_SPECIFIC_RESP)
    watchlist = Watchlist(api, model_unique_id="watchlistId")
    cbcsdk_mock.mock_request("PUT", f"/threathunter/watchlistmgr/v3/orgs/test/watchlists/{id}/tag", {"tag": True})
    watchlist.enable_tags()


def test_watchlist_enable_tags_no_id(cbcsdk_mock):
    """Testing Watchlist.enable_tags() raising InvalidObjectError when ID is missing."""
    api = cbcsdk_mock.api
    watchlist = Watchlist(api, model_unique_id=None)
    with pytest.raises(InvalidObjectError):
        watchlist.enable_tags()


def test_watchlist_disable_tags(cbcsdk_mock):
    """Testing Watchlist.disable_tags()."""
    api = cbcsdk_mock.api
    id = "watchlistId"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}", WATCHLIST_GET_SPECIFIC_RESP)
    watchlist = Watchlist(api, model_unique_id="watchlistId")
    cbcsdk_mock.mock_request("DELETE", f"/threathunter/watchlistmgr/v3/orgs/test/watchlists/{id}/tag", None)
    watchlist.disable_tags()


def test_watchlist_disable_tags_no_id(cbcsdk_mock):
    """Testing Watchlist.disable_tags() raising InvalidObjectError when ID is missing."""
    api = cbcsdk_mock.api
    watchlist = Watchlist(api, model_unique_id=None)
    with pytest.raises(InvalidObjectError):
        watchlist.disable_tags()


def test_watchlist_feed(cbcsdk_mock):
    """Testing Watchlist.feed property."""
    api = cbcsdk_mock.api
    id = "watchlistId"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}",
                             WATCHLIST_GET_SPECIFIC_RESP)
    watchlist = api.select(Watchlist, "watchlistId")
    cbcsdk_mock.mock_request("GET", "/threathunter/feedmgr/v2/orgs/test/feeds/feed_id_associated",
                             FEED_GET_SPECIFIC_FROM_WATCHLIST_RESP)

    feed_assoc_with_watchlist = watchlist.feed
    assert feed_assoc_with_watchlist.id == "feed_id_associated"


def test_watchlist_feed_missing_classifier(cbcsdk_mock):
    """Testing Watchlist.feed property."""
    api = cbcsdk_mock.api
    id = "watchlistMissingFieldsWithID"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}",
                             WATCHLIST_GET_SPECIFIC_MISSING_FIELDS_RESP)
    watchlist = api.select(Watchlist, "watchlistMissingFieldsWithID")
    assert not watchlist.classifier
    assert watchlist.feed is None


def test_watchlist_feed_invalid_classifier(cbcsdk_mock):
    """Testing Watchlist.feed property when "classifier" is missing."""
    api = cbcsdk_mock.api
    id = "watchlistInvalidClassifier"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}",
                             WATCHLIST_GET_SPECIFIC_INVALID_CLASSIFIER_RESP)
    watchlist = api.select(Watchlist, "watchlistInvalidClassifier")
    assert watchlist.classifier
    assert watchlist.feed is None


def test_watchlist_reports(cbcsdk_mock):
    """Testing Watchlist.reports property."""
    api = cbcsdk_mock.api
    id = "watchlistInvalidClassifier"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}",
                             WATCHLIST_GET_SPECIFIC_RESP)
    watchlist = api.select(Watchlist, "watchlistInvalidClassifier")
    cbcsdk_mock.mock_request("GET", "/threathunter/watchlistmgr/v3/orgs/test/reports/reportId0",
                             FEED_GET_SPECIFIC_RESP)
    cbcsdk_mock.mock_request("GET", "/threathunter/watchlistmgr/v3/orgs/test/reports/reportId1",
                             FEED_GET_SPECIFIC_RESP)
    cbcsdk_mock.mock_request("GET", "/threathunter/watchlistmgr/v3/orgs/test/reports/reportId2",
                             FEED_GET_SPECIFIC_RESP)
    assert watchlist.reports is not None
    assert isinstance(watchlist.reports, list)
    assert [isinstance(report, Report) for report in watchlist.reports]


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
