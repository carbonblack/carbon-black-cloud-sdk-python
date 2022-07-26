"""Testing the Query objects of cbc_sdk.base"""
import pytest
from unittest.mock import patch

from cbc_sdk.base import BaseQuery, SimpleQuery, IterableQueryMixin
from cbc_sdk.enterprise_edr import Feed, FeedQuery
from cbc_sdk.errors import ModelNotFound
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.stubresponse import patch_cbc_sdk_api


def test_base_query():
    """Test BaseQuery methods"""
    queryObject = BaseQuery(query="process_name='malicious.exe'")
    assert queryObject._query == "process_name='malicious.exe'"

    clonedQuery = queryObject._clone()
    assert clonedQuery._query == queryObject._query

    for item in clonedQuery._perform_query():
        # Won't execute since this will perform an empty iterator
        raise Exception("BaseQuery object is not iterable is not raised")


def test_simple_query(monkeypatch):
    """Test SimpleQuery methods using a FeedQuery for API calls"""
    _was_called = False

    def _get_results(url, **kwargs):
        nonlocal _was_called
        assert url == "/threathunter/feedmgr/v2/orgs/WNEX/feeds"
        _was_called = True
        return {
            "results": [
                {
                    "name": "My Feed",
                    "owner": "WNEX",
                    "provider_url": "https://exampleprovider.com",
                    "summary": "this is the summary",
                    "category": "this is the category",
                    "source_label": None,
                    "access": "public",
                    "id": "my_feed_id"
                }]}

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="WNEX", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_results)
    feed = api.select(Feed).where(include_public=True)

    assert isinstance(feed, SimpleQuery)
    assert isinstance(feed, FeedQuery)

    results = feed.results

    assert isinstance(results, list)
    assert len(feed) == 1
    assert isinstance(results[0], Feed)
    assert results[0].id == "my_feed_id"
    assert results[0].name == "My Feed"
    assert _was_called

    simpleQuery = SimpleQuery(Feed, api)
    assert simpleQuery._doc_class == Feed
    assert str(simpleQuery._urlobject) == "/threathunter/feedmgr/v2/orgs/{}/feeds"
    assert isinstance(simpleQuery, SimpleQuery)
    assert simpleQuery._cb == api
    assert simpleQuery._results == []
    assert simpleQuery._query == {}

    clonedSimple = simpleQuery._clone()
    assert clonedSimple._cb == simpleQuery._cb
    assert clonedSimple._results == simpleQuery._results
    assert clonedSimple._query == simpleQuery._query


def test_select_calls_select_class_instance():
    """Test if the `select` method calls the `select_class_instance` function."""
    with patch("cbc_sdk.connection.select_class_instance") as fn:
        api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="WNEX", ssl_verify=True)
        api.select("a")
        fn.assert_called()


def test_raise_ModelNotFound():
    """Test ModelNotFound exception when a class isn't found."""
    with pytest.raises(ModelNotFound):
        api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="WNEX", ssl_verify=True)
        api.select("NON_EXISTENT")


@pytest.mark.parametrize(
    "klass_name, query_expected", [
        # Audit and Remediation
        ("DeviceSummary", "ResultQuery"),
        ("DeviceSummaryFacet", "FacetQuery"),
        ("Result", "ResultQuery"),
        ("ResultFacet", "FacetQuery"),
        ("Run", "RunQuery"),
        ("RunHistory", "RunHistoryQuery"),
        ("Template", "RunQuery"),
        ("TemplateHistory", "TemplateHistoryQuery"),

        # Endpoint Standard
        ("Recommendation", "RecommendationQuery"),
        ("EnrichedEvent", "EnrichedEventQuery"),
        ("EnrichedEventFacet", "FacetQuery"),
        ("USBDevice", "USBDeviceQuery"),
        ("USBDeviceApproval", "USBDeviceApprovalQuery"),
        ("USBDeviceBlock", "USBDeviceBlockQuery"),

        # Enterprise EDR
        ("Feed", "FeedQuery"),
        ("Report", "ReportQuery"),
        ("Watchlist", "WatchlistQuery"),

        # Platform
        ("BaseAlert", "BaseAlertSearchQuery"),
        ("CBAnalyticsAlert", "CBAnalyticsAlertSearchQuery"),
        ("DeviceControlAlert", "DeviceControlAlertSearchQuery"),
        ("WatchlistAlert", "WatchlistAlertSearchQuery"),
        ("Device", "DeviceSearchQuery"),
        ("Event", "EventQuery"),
        ("EventFacet", "EventFacetQuery"),
        ("Grant", "GrantQuery"),
        ("Policy", "PolicyQuery"),
        ("Process", "AsyncProcessQuery"),
        ("Process.Summary", "SummaryQuery"),
        ("Process.Tree", "SummaryQuery"),
        ("ProcessFacet", "FacetQuery"),
        ("ReputationOverride", "ReputationOverrideQuery"),
        ("User", "UserQuery"),
        ("Vulnerability", "VulnerabilityQuery"),
        ("Vulnerability.OrgSummary", "VulnerabilityOrgSummaryQuery"),

        # Workload
        ("SensorKit", "SensorKitQuery"),
        ("ComputeResource", "ComputeResourceQuery"),
    ],
)
def test_select_class_instance(klass_name, query_expected):
    """Test the `select_class_instance` function"""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="WNEX", ssl_verify=True)
    q = api.select(str(klass_name))
    assert type(q).__qualname__ == query_expected


class _TestQuery(BaseQuery, IterableQueryMixin):
    """Test Query for Slicing"""

    # Prevent pytest from trying to collect webtest's TestApp as tests:
    __test__ = False

    def _count():
        """Mock Count"""
        pass


def test_query_index(monkeypatch):
    """Test query by index"""

    def _mock_query(**kwargs):
        assert kwargs.get("from_row") == 5
        assert kwargs.get("max_rows") == 1
        return [0, 1, 2, 3, 4, 5]

    query = _TestQuery()
    monkeypatch.setattr(query, "_perform_query", _mock_query)
    query[5] == 5


def test_query_slice_start_and_stop(monkeypatch):
    """Test query by start and stop slicing"""

    def _mock_query(**kwargs):
        assert kwargs.get("from_row") == 5
        assert kwargs.get("max_rows") == 5
        return []

    query = _TestQuery()
    monkeypatch.setattr(query, "_perform_query", _mock_query)
    query[5:10]


def test_query_slice_start(monkeypatch):
    """Test query by start slicing"""

    def _mock_query(**kwargs):
        assert kwargs.get("from_row") == 5
        assert kwargs.get("max_rows") == -1
        return []

    query = _TestQuery()
    monkeypatch.setattr(query, "_perform_query", _mock_query)
    query[5:]


def test_query_slice_stop(monkeypatch):
    """Test query by stop slicing"""

    def _mock_query(**kwargs):
        assert kwargs.get("from_row") == 0
        assert kwargs.get("max_rows") == 1
        return []

    query = _TestQuery()
    monkeypatch.setattr(query, "_perform_query", _mock_query)
    query[:1]


def test_query_slice_neg_start(monkeypatch):
    """Test query by negative start slicing"""
    mock_list = [0, 1, 2, 3]

    def _mock_query(**kwargs):
        assert kwargs.get("from_row") is None
        assert kwargs.get("max_rows") is None
        for item in mock_list:
            yield item

    def _mock_count():
        return len(mock_list)

    query = _TestQuery()
    monkeypatch.setattr(query, "_perform_query", _mock_query)
    monkeypatch.setattr(query, "_count", _mock_count)
    assert query[-2:] == [2, 3]


def test_query_slice_neg_stop(monkeypatch):
    """Test query by negative stop slicing"""
    mock_list = [0, 1, 2, 3]

    def _mock_query(**kwargs):
        assert kwargs.get("from_row") is None
        assert kwargs.get("max_rows") is None
        for item in mock_list:
            yield item

    def _mock_count():
        return len(mock_list)

    query = _TestQuery()
    monkeypatch.setattr(query, "_perform_query", _mock_query)
    monkeypatch.setattr(query, "_count", _mock_count)
    assert query[:-2] == [0, 1]


def test_query_slice_type_error(monkeypatch):
    """Test query where _perform_query returns TypeError"""
    mock_list = [0, 1, 2, 3]

    def _mock_query():
        for item in mock_list:
            yield item

    def _mock_count():
        return len(mock_list)

    query = _TestQuery()
    monkeypatch.setattr(query, "_perform_query", _mock_query)
    monkeypatch.setattr(query, "_count", _mock_count)
    assert query[1:3] == [1, 2]
