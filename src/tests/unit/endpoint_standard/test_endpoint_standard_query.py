"""Testing Query object of cbc_sdk.endpoint_standard"""

import pytest
import logging
from cbc_sdk.endpoint_standard import Policy
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_policy import (POLICY_GET_RESP)

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


def test_endpoint_standard_query_clone(cbcsdk_mock):
    """Testing Query._clone()."""
    policy_query = cbcsdk_mock.api.select(Policy).where(id=12345)
    cloned = policy_query._clone()
    # cloned query should be identical, but have unique _query_builders
    assert policy_query._batch_size == cloned._batch_size
    assert policy_query._query_builder._collapse() == cloned._query_builder._collapse()
    assert policy_query._batch_size == cloned._batch_size
    assert policy_query._query_builder != cloned._query_builder

    # updated query should not affect the cloned query
    # Query.batch_size() clones a query
    new_policy_query = policy_query.batch_size(1000)
    assert new_policy_query._batch_size != cloned._batch_size


def test_endpoint_standard_query_count(cbcsdk_mock):
    """Testing Query._count()."""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/12345", POLICY_GET_RESP)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy", POLICY_GET_RESP)
    api = cbcsdk_mock.api
    hostname_policy_query = api.select(Policy)
    assert not hostname_policy_query._count_valid
    assert hostname_policy_query._count() == 0
    assert hostname_policy_query._count_valid
