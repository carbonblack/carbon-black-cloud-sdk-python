"""Testing the Query objects of cbc_sdk.base"""

from cbc_sdk.base import BaseQuery, SimpleQuery
from cbc_sdk.enterprise_edr import Feed, FeedQuery
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
    assert str(simpleQuery._doc_class.urlobject) == "/threathunter/feedmgr/v2/orgs/{}/feeds"
    assert str(simpleQuery._urlobject) == "/threathunter/feedmgr/v2/orgs/WNEX/feeds"
    assert isinstance(simpleQuery, SimpleQuery)
    assert simpleQuery._cb == api
    assert simpleQuery._results == []
    assert simpleQuery._query == {}

    clonedSimple = simpleQuery._clone()
    assert clonedSimple._cb == simpleQuery._cb
    assert clonedSimple._results == simpleQuery._results
    assert clonedSimple._query == simpleQuery._query
