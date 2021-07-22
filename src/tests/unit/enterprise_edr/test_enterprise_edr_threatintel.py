"""Testing Watchlist, Report, Feed objects of cbc_sdk.enterprise_edr"""
import copy

import pytest
import logging
import re
from contextlib import ExitStack as does_not_raise
from cbc_sdk.enterprise_edr import Watchlist, Report, Feed, IOC_V2
from cbc_sdk.errors import InvalidObjectError, ApiError
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.enterprise_edr.mock_threatintel import (WATCHLIST_GET_RESP,
                                                                 WATCHLIST_GET_SPECIFIC_RESP,
                                                                 WATCHLIST_GET_SPECIFIC_RESP_2,
                                                                 WATCHLIST_GET_SPECIFIC_MISSING_FIELDS_RESP,
                                                                 WATCHLIST_GET_SPECIFIC_INVALID_CLASSIFIER_RESP,
                                                                 CREATE_WATCHLIST_DATA,
                                                                 REPORT_GET_RESP,
                                                                 FEED_GET_RESP,
                                                                 FEED_GET_SPECIFIC_RESP,
                                                                 FEED_GET_SPECIFIC_FROM_WATCHLIST_RESP,
                                                                 IOC_GET_IGNORED,
                                                                 REPORT_BUILT_VIA_BUILDER,
                                                                 REPORT_INIT,
                                                                 REPORT_GET_IGNORED,
                                                                 REPORT_GET_SEVERITY,
                                                                 REPORT_UPDATE_AFTER_ADD_IOC,
                                                                 REPORT_UPDATE_AFTER_REMOVE_IOC)

log = logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, filename='log.txt')
GUID_PATTERN = '[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12}'


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
    cbcsdk_mock.mock_request("PATCH", f"/threathunter/watchlistmgr/v2/watchlist/{id}",
                             WATCHLIST_GET_SPECIFIC_RESP)
    watchlist.update(description="My New Description", nonexistant_key="This Is Ignored")
    assert watchlist._info["description"] == "My New Description"
    watchlist._update_object()


def test_watchlist_update_id(cbcsdk_mock):
    """Testing Watchlist.update()."""
    id = "watchlistId2"
    id2 = "watchlistId"
    cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v2/watchlist/{id}", WATCHLIST_GET_SPECIFIC_RESP_2)
    watchlist = Watchlist(cbcsdk_mock.api, model_unique_id="watchlistId2", initial_data=None)
    assert "description" in watchlist._info
    assert "nonexistant_key" not in watchlist._info
    cbcsdk_mock.mock_request("PATCH", "/threathunter/watchlistmgr/v2/watchlist",
                             WATCHLIST_GET_SPECIFIC_RESP)
    watchlist.id = id2
    result_repr = watchlist.__repr__()
    assert 'id watchlistId' in result_repr
    assert '(*)' in result_repr
    watchlist._update_object()


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

    def _test_request(url, body, **kwargs):
        assert len(body["iocs_v2"]) == 1
        return body

    cbcsdk_mock.mock_request("PUT",
                             f"/threathunter/feedmgr/v2/orgs/test/feeds/{feed_id}/"
                             "reports/109027d1-064c-477d-aa34-528606ef72a9", _test_request)
    api = cbcsdk_mock.api
    reports = api.select(Report).where(feed_id="rEVxDoWRAucNZI8utPRrQ")
    results = [res for res in reports._perform_query()]
    assert results is not None
    assert isinstance(results[0], Report)
    assert reports[0].iocs_ is not [] or reports[0].iocs_ is not None

    reports[0].update(iocs_v2=[{
        "id": "109027d2-064c-477d-aa34-528606ef72a1",
        "match_type": "equality",
        "values": [
            "test"
        ],
        "field": "md5"
    }])

    assert reports[0].iocs_v2[0]["values"][0] == "test"


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


def test_create_query_ioc(cb):
    """Tests the creation of a 'query' IOC."""
    with pytest.raises(ApiError):
        IOC_V2.create_query(cb, "foo", None)

    ioc = IOC_V2.create_query(cb, "foo", "process_name:evil.exe")
    assert ioc._info == {'id': 'foo', 'match_type': 'query', 'values': ['process_name:evil.exe']}
    ioc = IOC_V2.create_query(cb, None, "process_name:evil.exe")
    assert ioc.match_type == 'query'
    assert ioc.values == ['process_name:evil.exe']
    assert re.fullmatch(GUID_PATTERN, ioc.id)


def test_create_equality_ioc(cb):
    """Tests the creation of an 'equality' IOC."""
    with pytest.raises(ApiError):
        IOC_V2.create_equality(cb, "foo", None, "Alpha")
    with pytest.raises(ApiError):
        IOC_V2.create_equality(cb, "foo", "process_name")

    ioc = IOC_V2.create_equality(cb, "foo", "process_name", "Alpha", "Bravo", "Charlie")
    assert ioc._info == {'id': 'foo', 'match_type': 'equality', 'field': 'process_name',
                         'values': ['Alpha', 'Bravo', 'Charlie']}
    ioc = IOC_V2.create_equality(cb, None, "process_name", "Alpha")
    assert ioc.match_type == 'equality'
    assert ioc.field == 'process_name'
    assert ioc.values == ['Alpha']
    assert re.fullmatch(GUID_PATTERN, ioc.id)


def test_create_regex_ioc(cb):
    """Tests the creation of a 'regex' IOC."""
    with pytest.raises(ApiError):
        IOC_V2.create_regex(cb, "foo", None, "Alpha")
    with pytest.raises(ApiError):
        IOC_V2.create_regex(cb, "foo", "process_name")

    ioc = IOC_V2.create_regex(cb, "foo", "process_name", "Alpha", "Bravo", "Charlie")
    assert ioc._info == {'id': 'foo', 'match_type': 'regex', 'field': 'process_name',
                         'values': ['Alpha', 'Bravo', 'Charlie']}
    ioc = IOC_V2.create_regex(cb, None, "process_name", "Alpha")
    assert ioc.match_type == 'regex'
    assert ioc.field == 'process_name'
    assert ioc.values == ['Alpha']
    assert re.fullmatch(GUID_PATTERN, ioc._info['id'])


def test_ioc_read_ignored(cbcsdk_mock):
    """Tests reading the ignore status of an IOC."""
    cbcsdk_mock.mock_request("GET", "/threathunter/watchlistmgr/v3/orgs/test/reports/a1b2/iocs/foo/ignore",
                             IOC_GET_IGNORED)
    api = cbcsdk_mock.api
    ioc = IOC_V2.create_equality(api, "foo", "process_name", "Alpha")
    with pytest.raises(InvalidObjectError):
        tmp = ioc.ignored
    ioc._report_id = "a1b2"
    assert ioc.ignored
    ioc._info['id'] = None
    with pytest.raises(InvalidObjectError):
        tmp = ioc.ignored


def test_ioc_set_ignored(cbcsdk_mock):
    """Tests setting the ignore status of an IOC."""
    cbcsdk_mock.mock_request("PUT", "/threathunter/watchlistmgr/v3/orgs/test/reports/a1b2/iocs/foo/ignore",
                             IOC_GET_IGNORED)
    api = cbcsdk_mock.api
    ioc = IOC_V2.create_equality(api, "foo", "process_name", "Alpha")
    with pytest.raises(InvalidObjectError):
        ioc.ignore()
    ioc._report_id = "a1b2"
    ioc.ignore()
    ioc._info['id'] = None
    with pytest.raises(InvalidObjectError):
        ioc.ignore()


def test_ioc_clear_ignored(cbcsdk_mock):
    """Tests clearing the ignore status of an IOC."""
    cbcsdk_mock.mock_request("DELETE", "/threathunter/watchlistmgr/v3/orgs/test/reports/a1b2/iocs/foo/ignore",
                             CBCSDKMock.StubResponse(None, 204))
    api = cbcsdk_mock.api
    ioc = IOC_V2.create_equality(api, "foo", "process_name", "Alpha")
    with pytest.raises(InvalidObjectError):
        ioc.unignore()
    ioc._report_id = "a1b2"
    ioc.unignore()
    ioc._info['id'] = None
    with pytest.raises(InvalidObjectError):
        ioc.unignore()


def test_report_builder_save_watchlist(cbcsdk_mock):
    """Tests the operation of a ReportBuilder and saving the report as a watchlist report."""
    my_info = None

    def on_post(url, body, **kwargs):
        assert my_info
        assert body == my_info
        my_info['id'] = "AaBbCcDdEeFfGg"
        return my_info

    cbcsdk_mock.mock_request("POST", "/threathunter/watchlistmgr/v3/orgs/test/reports", on_post)
    api = cbcsdk_mock.api
    builder = Report.create(api, "NotReal", "Not real description", 2)
    builder.set_title("ReportTitle").set_description("The report description").set_timestamp(1234567890)
    builder.set_severity(5).set_link('https://example.com').add_tag("Alpha").add_tag("Bravo")
    builder.add_ioc(IOC_V2.create_equality(api, "foo", "process_name", "evil.exe"))
    builder.add_ioc(IOC_V2.create_equality(api, "bar", "netconn_ipv4", "10.29.99.1"))
    builder.set_visibility("visible")
    report = builder.build()
    report.validate()
    my_info = copy.deepcopy(report._info)
    assert my_info == REPORT_BUILT_VIA_BUILDER
    report.save_watchlist()
    assert report._from_watchlist
    assert report._info['id'] == "AaBbCcDdEeFfGg"


@pytest.mark.parametrize("init_data, feed, watchlist, do_request, expectation, result", [
    (REPORT_INIT, None, True, True, does_not_raise(), True),
    (REPORT_INIT, None, False, False, pytest.raises(InvalidObjectError), True),
    (REPORT_BUILT_VIA_BUILDER, None, True, False, pytest.raises(InvalidObjectError), True)
])
def test_report_get_ignored(cbcsdk_mock, init_data, feed, watchlist, do_request, expectation, result):
    """Tests the operation of the report.ignored() method."""
    if do_request:
        cbcsdk_mock.mock_request("GET", "/threathunter/watchlistmgr/v3/orgs/test/reports/"
                                        "69e2a8d0-bc36-4970-9834-8687efe1aff7/ignore", REPORT_GET_IGNORED)
    api = cbcsdk_mock.api
    report = Report(api, None, init_data, feed, watchlist)
    with expectation:
        assert report.ignored == result


@pytest.mark.parametrize("init_data, feed, watchlist, do_request, expectation", [
    (REPORT_INIT, None, True, True, does_not_raise()),
    (REPORT_INIT, None, False, False, pytest.raises(InvalidObjectError)),
    (REPORT_BUILT_VIA_BUILDER, None, True, False, pytest.raises(InvalidObjectError))
])
def test_report_set_ignored(cbcsdk_mock, init_data, feed, watchlist, do_request, expectation):
    """Tests the operation of the report.ignore() method."""
    if do_request:
        cbcsdk_mock.mock_request("PUT", "/threathunter/watchlistmgr/v3/orgs/test/reports/"
                                        "69e2a8d0-bc36-4970-9834-8687efe1aff7/ignore", REPORT_GET_IGNORED)
    api = cbcsdk_mock.api
    report = Report(api, None, init_data, feed, watchlist)
    with expectation:
        report.ignore()


@pytest.mark.parametrize("init_data, feed, watchlist, do_request, expectation", [
    (REPORT_INIT, None, True, True, does_not_raise()),
    (REPORT_INIT, None, False, False, pytest.raises(InvalidObjectError)),
    (REPORT_BUILT_VIA_BUILDER, None, True, False, pytest.raises(InvalidObjectError))
])
def test_report_clear_ignored(cbcsdk_mock, init_data, feed, watchlist, do_request, expectation):
    """Tests the operation of the report.unignore() method."""
    if do_request:
        cbcsdk_mock.mock_request("DELETE", "/threathunter/watchlistmgr/v3/orgs/test/reports/"
                                           "69e2a8d0-bc36-4970-9834-8687efe1aff7/ignore",
                                 CBCSDKMock.StubResponse(None, 204))
    api = cbcsdk_mock.api
    report = Report(api, None, init_data, feed, watchlist)
    with expectation:
        report.unignore()


@pytest.mark.parametrize("init_data, feed, watchlist, call_url, expectation", [
    (REPORT_INIT, None, True, "/threathunter/watchlistmgr/v3/orgs/test/reports/69e2a8d0-bc36-4970-9834-8687efe1aff7",
     does_not_raise()),
    (REPORT_INIT, "qwertyuiop", False, "/threathunter/feedmgr/v2/orgs/test/feeds/qwertyuiop/reports/"
                                       "69e2a8d0-bc36-4970-9834-8687efe1aff7", does_not_raise()),
    (REPORT_INIT, None, False, None, pytest.raises(InvalidObjectError)),
    (REPORT_BUILT_VIA_BUILDER, None, True, None, pytest.raises(InvalidObjectError)),
    (REPORT_BUILT_VIA_BUILDER, "qwertyuiop", False, None, pytest.raises(InvalidObjectError))
])
def test_report_delete(cbcsdk_mock, init_data, feed, watchlist, call_url, expectation):
    """Tests the operation of the report.delete() method."""
    if call_url:
        cbcsdk_mock.mock_request("DELETE", call_url, CBCSDKMock.StubResponse(None, 204))
    api = cbcsdk_mock.api
    report = Report(api, None, init_data, feed, watchlist)
    with expectation:
        report.delete()


@pytest.mark.parametrize("init_data, feed, watchlist, do_request, expectation, result", [
    (REPORT_INIT, "qwertyuiop", False, True, does_not_raise(), 8),
    (REPORT_INIT, None, True, False, pytest.raises(InvalidObjectError), -1),
    (REPORT_BUILT_VIA_BUILDER, "qwertyuiop", False, False, pytest.raises(InvalidObjectError), -1)
])
def test_report_get_custom_severity(cbcsdk_mock, init_data, feed, watchlist, do_request, expectation, result):
    """Tests getting the custom severity for a report."""
    if do_request:
        cbcsdk_mock.mock_request("GET", "/threathunter/watchlistmgr/v3/orgs/test/reports/"
                                        "69e2a8d0-bc36-4970-9834-8687efe1aff7/severity", REPORT_GET_SEVERITY)
    api = cbcsdk_mock.api
    report = Report(api, None, init_data, feed, watchlist)
    with expectation:
        severity = report.custom_severity
        assert severity.report_id == report.id
        assert severity.severity == result


@pytest.mark.parametrize("init_data, feed, watchlist, input, http_method, http_return, expectation", [
    (REPORT_INIT, "qwertyuiop", False, 8, "PUT", REPORT_GET_SEVERITY, does_not_raise()),
    (REPORT_INIT, "qwertyuiop", False, None, "DELETE", CBCSDKMock.StubResponse(None, 204), does_not_raise()),
    (REPORT_INIT, None, True, 8, None, None, pytest.raises(InvalidObjectError)),
    (REPORT_BUILT_VIA_BUILDER, "qwertyuiop", False, 8, None, None, pytest.raises(InvalidObjectError))
])
def test_report_set_custom_severity(cbcsdk_mock, init_data, feed, watchlist, input, http_method,
                                    http_return, expectation):
    """Tests setting the custom severity for a report."""
    if http_method:
        cbcsdk_mock.mock_request(http_method, "/threathunter/watchlistmgr/v3/orgs/test/reports/"
                                              "69e2a8d0-bc36-4970-9834-8687efe1aff7/severity", http_return)
    api = cbcsdk_mock.api
    report = Report(api, None, init_data, feed, watchlist)
    with expectation:
        report.custom_severity = input


def test_report_add_ioc(cbcsdk_mock):
    """Test appending a new IOC and then updating the report."""
    def on_put(url, body, **kwargs):
        match_data = copy.deepcopy(REPORT_UPDATE_AFTER_ADD_IOC)
        match_data['timestamp'] = body['timestamp']
        assert body == match_data
        return body

    cbcsdk_mock.mock_request("PUT", "/threathunter/watchlistmgr/v3/orgs/test/reports/"
                                    "69e2a8d0-bc36-4970-9834-8687efe1aff7", on_put)
    api = cbcsdk_mock.api
    report = Report(api, None, copy.deepcopy(REPORT_INIT), None, True)
    report.append_iocs([IOC_V2.create_query(api, "quux", "filemod_name: \"audio.dat\"")])
    report.update()
    assert len(report.iocs_) == 3


def test_report_remove_ioc(cbcsdk_mock):
    """Test removing an IOC and then updating the report."""
    def on_put(url, body, **kwargs):
        match_data = copy.deepcopy(REPORT_UPDATE_AFTER_REMOVE_IOC)
        match_data['timestamp'] = body['timestamp']
        assert body == match_data
        return body

    cbcsdk_mock.mock_request("PUT", "/threathunter/watchlistmgr/v3/orgs/test/reports/"
                                    "69e2a8d0-bc36-4970-9834-8687efe1aff7", on_put)
    api = cbcsdk_mock.api
    report = Report(api, None, copy.deepcopy(REPORT_INIT), None, True)
    ioc = report.iocs_[0]
    assert ioc.id == "foo"
    report.remove_iocs([ioc])
    report.update()
    assert len(report.iocs_) == 1


def test_report_remove_nonexistent_ioc_id(cbcsdk_mock):
    """Test removing an IOC by ID when that ID doesn't actually exist."""
    def on_put(url, body, **kwargs):
        match_data = copy.deepcopy(REPORT_INIT)
        match_data['timestamp'] = body['timestamp']
        assert body == match_data
        return body

    cbcsdk_mock.mock_request("PUT", "/threathunter/watchlistmgr/v3/orgs/test/reports/"
                                    "69e2a8d0-bc36-4970-9834-8687efe1aff7", on_put)
    api = cbcsdk_mock.api
    report = Report(api, None, copy.deepcopy(REPORT_INIT), None, True)
    report.remove_iocs_by_id(['notexist'])
    report.update()
    assert len(report.iocs_) == 2
