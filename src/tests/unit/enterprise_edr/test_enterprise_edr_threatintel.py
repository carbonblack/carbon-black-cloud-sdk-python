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
                                                                 REPORT_INIT2,
                                                                 REPORT_GET_IGNORED,
                                                                 REPORT_GET_SEVERITY,
                                                                 REPORT_UPDATE_AFTER_ADD_IOC,
                                                                 REPORT_UPDATE_AFTER_REMOVE_IOC,
                                                                 FEED_BUILT_VIA_BUILDER,
                                                                 FEED_INIT,
                                                                 FEED_UPDATE_INFO_1,
                                                                 REPORT_INIT_2,
                                                                 WATCHLIST_BUILDER_IN,
                                                                 WATCHLIST_BUILDER_OUT,
                                                                 WATCHLIST_FROM_FEED_IN,
                                                                 WATCHLIST_FROM_FEED_OUT,
                                                                 ADD_REPORT_IDS_LIST,
                                                                 ADD_REPORTS_LIST)

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
        assert ioc.ignored
    ioc._report_id = "a1b2"
    assert ioc.ignored
    ioc._info['id'] = None
    with pytest.raises(InvalidObjectError):
        assert ioc.ignored


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


@pytest.mark.parametrize("input, output, expectation", [
    ('::1', '00000000000000000000000000000001', does_not_raise()),
    ('2601:280:c300:294::6bd', '26010280C300029400000000000006BD', does_not_raise()),
    ('fd9f:6dd0:e01b:0:1b7:daf8:b54d:4916', 'FD9F6DD0E01B000001B7DAF8B54D4916', does_not_raise()),
    ('fe80::3c0c:73f:845b:8243', 'FE800000000000003C0C073F845B8243', does_not_raise()),
    ('fd9f:6dd0:e01b:0:1b7:daf8:4916', None, pytest.raises(ApiError)),
    ('fd9f:6dd0:e01b:0:1b7:daf8:b54d:4916:909', None, pytest.raises(ApiError)),
    ('fd9f:6dd0:e01b:0:1b7:daef8:b54d:4916', None, pytest.raises(ApiError)),
    ('fe80:3:C0:8080::3c0c:73f:845b:8243', None, pytest.raises(ApiError)),
    ('2601::c300:294::6bd', None, pytest.raises(ApiError)),
    ('fe80::3c0c:73g:845b:8243', None, pytest.raises(ApiError)),
    ("10.8.16.254", None, pytest.raises(ApiError))
])
def test_ipv6_equality_format(input, output, expectation):
    """Tests the ipv6_equality_format() function."""
    with expectation:
        assert IOC_V2.ipv6_equality_format(input) == output


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


@pytest.mark.parametrize("init_data, feed, watchlist, do_request, url_id, expectation, result", [
    (REPORT_INIT, None, True, True, "69e2a8d0-bc36-4970-9834-8687efe1aff7", does_not_raise(), True),
    (REPORT_INIT, None, False, False, "", pytest.raises(InvalidObjectError), True),
    (REPORT_BUILT_VIA_BUILDER, None, True, False, "", pytest.raises(InvalidObjectError), True),
    (REPORT_INIT2, "abcdefgh", True, True, "Compound", does_not_raise(), True),
    (REPORT_INIT2, "abcdefgh", False, True, "abcdefgh-Compound", does_not_raise(), True)
])
def test_report_get_ignored(cbcsdk_mock, init_data, feed, watchlist, do_request, url_id, expectation, result):
    """Tests the operation of the report.ignored() method."""
    if do_request:
        cbcsdk_mock.mock_request("GET", f"/threathunter/watchlistmgr/v3/orgs/test/reports/{url_id}/ignore",
                                 REPORT_GET_IGNORED)
    api = cbcsdk_mock.api
    report = Report(api, None, init_data, feed, watchlist)
    with expectation:
        assert report.ignored == result


@pytest.mark.parametrize("init_data, feed, watchlist, do_request, url_id, expectation", [
    (REPORT_INIT, None, True, True, "69e2a8d0-bc36-4970-9834-8687efe1aff7", does_not_raise()),
    (REPORT_INIT, None, False, False, "", pytest.raises(InvalidObjectError)),
    (REPORT_BUILT_VIA_BUILDER, None, True, False, "", pytest.raises(InvalidObjectError)),
    (REPORT_INIT2, "abcdefgh", True, True, "Compound", does_not_raise()),
    (REPORT_INIT2, "abcdefgh", False, True, "abcdefgh-Compound", does_not_raise())
])
def test_report_set_ignored(cbcsdk_mock, init_data, feed, watchlist, do_request, url_id, expectation):
    """Tests the operation of the report.ignore() method."""
    if do_request:
        cbcsdk_mock.mock_request("PUT", f"/threathunter/watchlistmgr/v3/orgs/test/reports/{url_id}/ignore",
                                 REPORT_GET_IGNORED)
    api = cbcsdk_mock.api
    report = Report(api, None, init_data, feed, watchlist)
    with expectation:
        report.ignore()


@pytest.mark.parametrize("init_data, feed, watchlist, do_request, url_id, expectation", [
    (REPORT_INIT, None, True, True, "69e2a8d0-bc36-4970-9834-8687efe1aff7", does_not_raise()),
    (REPORT_INIT, None, False, False, "", pytest.raises(InvalidObjectError)),
    (REPORT_BUILT_VIA_BUILDER, None, True, False, "", pytest.raises(InvalidObjectError)),
    (REPORT_INIT2, "abcdefgh", True, True, "Compound", does_not_raise()),
    (REPORT_INIT2, "abcdefgh", False, True, "abcdefgh-Compound", does_not_raise())
])
def test_report_clear_ignored(cbcsdk_mock, init_data, feed, watchlist, do_request, url_id, expectation):
    """Tests the operation of the report.unignore() method."""
    if do_request:
        cbcsdk_mock.mock_request("DELETE", f"/threathunter/watchlistmgr/v3/orgs/test/reports/{url_id}/ignore",
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


def test_feed_builder_save(cbcsdk_mock):
    """Tests the operation of the FeedBuilder and the save() function."""
    def on_post(url, body, **kwargs):
        body_data = copy.deepcopy(body)
        for r in body_data['reports']:
            if 'id' in r:
                assert re.fullmatch(GUID_PATTERN, r['id'])
                del r['id']
        assert body_data == FEED_BUILT_VIA_BUILDER
        return_value = copy.deepcopy(body['feedinfo'])
        return_value["id"] = "qwertyuiop"
        return_value["owner"] = "JRN"
        return_value["access"] = "private"
        return return_value

    cbcsdk_mock.mock_request("POST", "/threathunter/feedmgr/v2/orgs/test/feeds", on_post)
    api = cbcsdk_mock.api
    # Start by building a report for the new feed to contain.
    report_builder = Report.create(api, "NotReal", "Not real description", 2)
    report_builder.set_title("ReportTitle").set_description("The report description").set_timestamp(1234567890)
    report_builder.set_severity(5).set_link('https://example.com').add_tag("Alpha").add_tag("Bravo")
    report_builder.add_ioc(IOC_V2.create_equality(api, "foo", "process_name", "evil.exe"))
    report_builder.add_ioc(IOC_V2.create_equality(api, "bar", "netconn_ipv4", "10.29.99.1"))
    report_builder.set_visibility("visible")
    report = report_builder.build()
    # Now build the feed.
    builder = Feed.create(api, "NotReal", "http://127.0.0.1", "Not a real summary", "Fake")
    builder.set_name("FeedName").set_provider_url("http://example.com").set_summary("Summary information")
    builder.set_category("Intrusion").set_source_label("SourceLabel").add_reports([report])
    feed = builder.build()
    feed.save()
    assert feed.id == "qwertyuiop"
    assert len(feed._reports) == 1


@pytest.mark.parametrize("feed_init, do_operation, expectation", [
    (FEED_INIT, True, does_not_raise()),
    (FEED_BUILT_VIA_BUILDER, False, pytest.raises(InvalidObjectError))
])
def test_delete_feed(cbcsdk_mock, feed_init, do_operation, expectation):
    """Tests the delete() function."""
    if do_operation:
        cbcsdk_mock.mock_request("DELETE", "/threathunter/feedmgr/v2/orgs/test/feeds/qwertyuiop",
                                 CBCSDKMock.StubResponse(None, 204))
    api = cbcsdk_mock.api
    feed = Feed(api, initial_data=feed_init)
    with expectation:
        feed.delete()


@pytest.mark.parametrize("feed_init, change_item, new_value, do_operation, new_info, expectation", [
    (FEED_INIT, 'name', 'NewName', True, FEED_UPDATE_INFO_1, does_not_raise()),
    (FEED_BUILT_VIA_BUILDER, 'name', 'NewName', False, None, pytest.raises(InvalidObjectError))
])
def test_update_feed_info(cbcsdk_mock, feed_init, change_item, new_value, do_operation, new_info, expectation):
    """Tests the update() function."""
    def on_put(url, body, **kwargs):
        assert body == new_info
        return new_info

    if do_operation:
        cbcsdk_mock.mock_request("PUT", "/threathunter/feedmgr/v2/orgs/test/feeds/qwertyuiop/feedinfo", on_put)
    api = cbcsdk_mock.api
    feed = Feed(api, initial_data=copy.deepcopy(feed_init))
    params = {change_item: new_value}
    with expectation:
        feed.update(**params)
        assert feed._info[change_item] == new_value


@pytest.mark.parametrize("feed_init, do_request, expectation", [
    (FEED_INIT, True, does_not_raise()),
    (FEED_BUILT_VIA_BUILDER, False, pytest.raises(InvalidObjectError))
])
def test_get_feed_reports(cbcsdk_mock, feed_init, do_request, expectation):
    """Tests the reports() property."""
    if do_request:
        cbcsdk_mock.mock_request("GET", "/threathunter/feedmgr/v2/orgs/test/feeds/qwertyuiop/reports", REPORT_GET_RESP)
    api = cbcsdk_mock.api
    feed = Feed(api, initial_data=feed_init)
    with expectation:
        reports = feed.reports
        assert len(reports) == 1
        assert reports[0].id == '109027d1-064c-477d-aa34-528606ef72a9'


@pytest.mark.parametrize("feed_init, do_request, expectation", [
    (FEED_INIT, True, does_not_raise()),
    (FEED_BUILT_VIA_BUILDER, False, pytest.raises(InvalidObjectError))
])
def test_replace_reports(cbcsdk_mock, feed_init, do_request, expectation):
    """Tests the replace_reports method."""
    def on_post(url, body, **kwargs):
        array = body['reports']
        assert len(array) == 1
        assert array[0]['id'] == "065fb68d-42a8-4b2e-8f91-17f925f54356"
        return {"success": True}

    if do_request:
        cbcsdk_mock.mock_request("POST", "/threathunter/feedmgr/v2/orgs/test/feeds/qwertyuiop/reports", on_post)
    api = cbcsdk_mock.api
    feed = Feed(api, initial_data=feed_init)
    new_report = Report(api, None, REPORT_INIT_2)
    with expectation:
        feed.replace_reports([new_report])


@pytest.mark.parametrize("feed_init, do_request, expectation", [
    (FEED_INIT, True, does_not_raise()),
    (FEED_BUILT_VIA_BUILDER, False, pytest.raises(InvalidObjectError))
])
def test_append_reports(cbcsdk_mock, feed_init, do_request, expectation):
    """Tests the append_reports method."""
    def on_post(url, body, **kwargs):
        array = body['reports']
        assert len(array) == 2
        assert array[0]['id'] == "69e2a8d0-bc36-4970-9834-8687efe1aff7"
        assert array[1]['id'] == "065fb68d-42a8-4b2e-8f91-17f925f54356"
        return {"success": True}

    if do_request:
        cbcsdk_mock.mock_request("POST", "/threathunter/feedmgr/v2/orgs/test/feeds/qwertyuiop/reports", on_post)
    api = cbcsdk_mock.api
    feed = Feed(api, initial_data=feed_init)
    new_report = Report(api, None, REPORT_INIT_2)
    with expectation:
        feed.append_reports([new_report])


def test_watchlist_builder(cbcsdk_mock):
    """Tests the function of the watchlist builder."""
    def on_post(url, body, **kwargs):
        assert body == WATCHLIST_BUILDER_IN
        return WATCHLIST_BUILDER_OUT

    cbcsdk_mock.mock_request('POST', "/threathunter/watchlistmgr/v3/orgs/test/watchlists", on_post)
    api = cbcsdk_mock.api
    report = Report(api, None, REPORT_INIT)
    report._from_watchlist = True
    builder = Watchlist.create(api, "NameErased")
    builder.set_name('NewWatchlist').set_description('I am a watchlist').set_tags_enabled(False)
    builder.set_alerts_enabled(True).add_report_ids(['47474d40-1f94-4995-b6d9-1d1eea3528b3']).add_reports([report])
    watchlist = builder.build()
    watchlist.save()
    assert watchlist.id == "ABCDEFGHabcdefgh"


def test_create_watchlist_from_feed(cbcsdk_mock):
    """Tests the function of create_from_feed()."""
    def on_post(url, body, **kwargs):
        assert body == WATCHLIST_FROM_FEED_IN
        return WATCHLIST_FROM_FEED_OUT

    cbcsdk_mock.mock_request('POST', "/threathunter/watchlistmgr/v3/orgs/test/watchlists", on_post)
    api = cbcsdk_mock.api
    feed = Feed(api, initial_data=FEED_INIT)
    watchlist = Watchlist.create_from_feed(feed)
    watchlist.save()
    assert watchlist.id == "ABCDEFGHabcdefgh"


def test_watchlist_add_report_ids(cbcsdk_mock):
    """Tests the add_report_ids() method."""
    def on_put(url, body, **kwargs):
        assert body['report_ids'] == ADD_REPORT_IDS_LIST
        return_value = copy.deepcopy(WATCHLIST_BUILDER_OUT)
        return_value['report_ids'] = ADD_REPORT_IDS_LIST
        return return_value

    cbcsdk_mock.mock_request("PUT", "/threathunter/watchlistmgr/v3/orgs/test/watchlists/ABCDEFGHabcdefgh", on_put)
    api = cbcsdk_mock.api
    watchlist = Watchlist(api, initial_data=copy.deepcopy(WATCHLIST_BUILDER_OUT))
    watchlist.add_report_ids(['64414d1f-66d5-4b32-9b8a-b778e13ab836', 'c9826407-0d5a-467f-bc98-7da2035de1bc'])
    assert watchlist.report_ids == ADD_REPORT_IDS_LIST


def test_watchlist_add_reports(cbcsdk_mock):
    """Tests the add_reports() method."""
    def on_put(url, body, **kwargs):
        assert body['report_ids'] == ADD_REPORTS_LIST
        return_value = copy.deepcopy(WATCHLIST_BUILDER_OUT)
        return_value['report_ids'] = ADD_REPORTS_LIST
        return return_value

    cbcsdk_mock.mock_request("PUT", "/threathunter/watchlistmgr/v3/orgs/test/watchlists/ABCDEFGHabcdefgh", on_put)
    api = cbcsdk_mock.api
    watchlist = Watchlist(api, initial_data=copy.deepcopy(WATCHLIST_BUILDER_OUT))
    report = Report(api, None, REPORT_INIT_2)
    report._from_watchlist = True
    watchlist.add_reports([report])
    assert watchlist.report_ids == ADD_REPORTS_LIST


@pytest.mark.parametrize("data, expectation, message", [
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, does_not_raise(), None),
    ({"title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Missing key: 'id'"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Missing key: 'title'"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Missing key: 'description'"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Missing key: 'timestamp'"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Missing key: 'severity'"),
    ({"id": 123, "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Report field 'id' is not a string"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": 6781, "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Report field 'title' is not a string"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": 8,
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Report field 'description' is not a string"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": "1234567890", "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Report field 'timestamp' is not an integer"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": "5", "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Report field 'severity' is not an integer"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": 8888, "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Report field 'link' is not a string"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": "Alpha",
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Report field 'tags' is not a list"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": {"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]},
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Report field 'iocs_v2' is not a list"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": 6681}, pytest.raises(InvalidObjectError), "Report field 'visibility' is not a string"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": -123456, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Timestamp cannot be negative"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 18, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Severity value out of range"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", 16],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Report tag is not a string"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Missing key: 'iocs_v2'"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Report should have at least one IOC"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{'match_type': 'query', 'values': ['foo']}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Missing key: 'id'"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{'id': 'foo', 'values': ['foo']}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Missing key: 'match_type'"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{'id': 'foo', 'match_type': 'query'}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "Missing key: 'values'"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{'id': 14, 'match_type': 'query', 'values': ['foo']}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "IOC field 'id' is not a string"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{'id': 'foo', 'match_type': 303, 'values': ['foo']}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "IOC field 'match_type' is not a string"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{'id': 'foo', 'match_type': 'query', 'values': 'blort'}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "IOC field 'values' is not a list"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{'id': 'foo', 'match_type': 'query', 'values': ['foo'], 'field': 15}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "IOC field 'field' is not a string"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{'id': 'foo', 'match_type': 'query', 'values': ['foo'], 'link': 15}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "IOC field 'link' is not a string"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{'id': 'foo', 'match_type': 'notdef', 'values': ['foo']}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError),
     "error in IOC 'match_type' value: Invalid match type"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "values": ["evil.exe"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "IOC of type equality must have a 'field' value"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "equality", "field": "process_name", "values": ["evil.exe", 9]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "IOC value is not a string"),
    ({"id": "69e2a8d0-bc36-4970-9834-8687efe1aff7", "title": "ReportTitle", "description": "The report description",
      "timestamp": 1234567890, "severity": 5, "link": "https://example.com", "tags": ["Alpha", "Bravo"],
      "iocs_v2": [{"id": "foo", "match_type": "query", "values": ["process_name:evil.exe", "netconn_ipv4:10.0.0.1"]}],
      "visibility": "visible"}, pytest.raises(InvalidObjectError), "query IOC should have one and only one value"),
])
def test_feed_report_validation(data, expectation, message):
    """Tests the _validate_report_rawdata method."""
    look_at_message = True
    with expectation as e:
        Feed._validate_report_rawdata([data])
        look_at_message = False
    if look_at_message:
        assert e.type is InvalidObjectError
        assert e.value.args[0] == message


@pytest.mark.parametrize("feed_init, do_request, expectation", [
    (FEED_INIT, True, does_not_raise()),
    (FEED_BUILT_VIA_BUILDER, False, pytest.raises(InvalidObjectError))
])
def test_replace_reports_rawdata(cbcsdk_mock, feed_init, do_request, expectation):
    """Tests the replace_reports_rawdata method."""
    def on_post(url, body, **kwargs):
        array = body['reports']
        assert len(array) == 1
        assert array[0]['id'] == "065fb68d-42a8-4b2e-8f91-17f925f54356"
        return {"success": True}

    if do_request:
        cbcsdk_mock.mock_request("POST", "/threathunter/feedmgr/v2/orgs/test/feeds/qwertyuiop/reports", on_post)
    api = cbcsdk_mock.api
    feed = Feed(api, initial_data=feed_init)
    with expectation:
        feed.replace_reports_rawdata([REPORT_INIT_2])


@pytest.mark.parametrize("feed_init, do_request, expectation", [
    (FEED_INIT, True, does_not_raise()),
    (FEED_BUILT_VIA_BUILDER, False, pytest.raises(InvalidObjectError))
])
def test_append_reports_rawdata(cbcsdk_mock, feed_init, do_request, expectation):
    """Tests the append_reports_rawdata method."""
    def on_post(url, body, **kwargs):
        array = body['reports']
        assert len(array) == 2
        assert array[0]['id'] == "69e2a8d0-bc36-4970-9834-8687efe1aff7"
        assert array[1]['id'] == "065fb68d-42a8-4b2e-8f91-17f925f54356"
        return {"success": True}

    if do_request:
        cbcsdk_mock.mock_request("POST", "/threathunter/feedmgr/v2/orgs/test/feeds/qwertyuiop/reports", on_post)
    api = cbcsdk_mock.api
    feed = Feed(api, initial_data=feed_init)
    with expectation:
        feed.append_reports_rawdata([REPORT_INIT_2])
