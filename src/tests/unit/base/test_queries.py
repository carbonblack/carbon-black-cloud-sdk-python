"""Testing the Query objects of cbc_sdk.base"""

from cbc_sdk.base import BaseQuery, SimpleQuery, PaginatedQuery
from cbc_sdk.enterprise_edr import Feed, FeedQuery
from cbc_sdk.platform import Process
from cbc_sdk.endpoint_standard import Query, Device
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.stubresponse import patch_cbapi


def test_base_query():
    """Test BaseQuery methods"""
    queryObject = BaseQuery(query="process_name='malicious.exe'")
    assert queryObject._query == "process_name='malicious.exe'"

    clonedQuery = queryObject._clone()
    assert clonedQuery._query == queryObject._query

    assert list(queryObject.all()) == []
    assert queryObject[:1] is None


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
    patch_cbapi(monkeypatch, api, GET=_get_results)
    feed = api.select(Feed).where(include_public=True)

    assert isinstance(feed, SimpleQuery)
    assert isinstance(feed, FeedQuery)

    results = feed.results

    assert isinstance(results, list)
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


def test_paginated_query(monkeypatch):
    """Test PaginatedQuery methods"""
    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="WNEX", ssl_verify=True)
    paginatedQuery = PaginatedQuery(Process, api, query="process_name='malicious.exe'")
    assert isinstance(paginatedQuery, PaginatedQuery)
    assert isinstance(paginatedQuery, BaseQuery)
    assert paginatedQuery._doc_class == Process
    assert paginatedQuery._query == "process_name='malicious.exe'"

    clonedPaginated = paginatedQuery._clone()
    assert clonedPaginated._doc_class == paginatedQuery._doc_class
    assert clonedPaginated._cb == paginatedQuery._cb
    assert clonedPaginated._total_results == paginatedQuery._total_results
    assert clonedPaginated._count_valid == paginatedQuery._count_valid
    assert clonedPaginated._batch_size == paginatedQuery._batch_size

    _devices_was_called = False

    def _get_devices(url, **kwargs):
        nonlocal _devices_was_called
        assert url == "/integrationServices/v3/device"
        _devices_was_called = True
        return {"results": [{"deviceId": "my_device_id"}]}

    deviceQuery = Query(Device, api)
    deviceQuery = deviceQuery.where("deviceId:'my_device_id'")

    assert isinstance(deviceQuery, PaginatedQuery)
    assert isinstance(deviceQuery, Query)

    patch_cbapi(monkeypatch, api, GET=_get_devices)

    x = deviceQuery.__getitem__(1)
    # assert x is not None
    assert _devices_was_called

    # Devices needs to be updated to v6 routes, this x test does nothing


def test_query_builder():
    """Test the Base QueryBuilder methods"""
    pass
