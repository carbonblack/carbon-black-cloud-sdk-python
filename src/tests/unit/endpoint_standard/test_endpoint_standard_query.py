"""Testing Query object of cbc_sdk.endpoint_standard"""

import pytest
import logging
from cbc_sdk.endpoint_standard import Device
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_devices import (ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP,
                                                                ENDPOINT_STANDARD_DEVICE_GET_HOSTNAME_RESP_0)

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
    device_query = cbcsdk_mock.api.select(Device).where(deviceId=12345)
    cloned = device_query._clone()
    # cloned query should be identical, but have unique _query_builders
    assert device_query._batch_size == cloned._batch_size
    assert device_query._query_builder._collapse() == cloned._query_builder._collapse()
    assert device_query._batch_size == cloned._batch_size
    assert device_query._query_builder != cloned._query_builder

    # updated query should not affect the cloned query
    # Query.batch_size() clones a query
    new_device_query = device_query.batch_size(1000)
    assert new_device_query._batch_size != cloned._batch_size
    # updated query should not affect the cloned query
    new_device_query = new_device_query.and_(hostNameExact='Win7x64')
    assert cloned._query_builder._collapse() != new_device_query._query_builder._collapse()


def test_endpoint_standard_query_mix_raw_structured(cbcsdk_mock):
    """Testing Query with raw 'string' and keyword. Should raise ApiError."""
    with pytest.raises(ApiError):
        cbcsdk_mock.api.select(Device).where(deviceId=1).and_('hostName:Win7x64')


def test_endpoint_standard_query_count(cbcsdk_mock):
    """Testing Query._count()."""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device", ENDPOINT_STANDARD_DEVICE_GET_HOSTNAME_RESP_0)
    api = cbcsdk_mock.api
    hostname_device_query = api.select(Device).where('hostName:Win7x64')
    assert not hostname_device_query._count_valid
    assert hostname_device_query._count() == 1
    assert hostname_device_query._count_valid


def test_endpoint_standard_query_or_apierror(cbcsdk_mock):
    """Testing raising ApiError when using or_() on a Endpoint Standard query."""
    api = cbcsdk_mock.api
    device_query = api.select(Device).where(hostName='Win7x64').and_(ipAddress='10.0.0.1')
    # integrationServices v3 doesn't support logical OR with parameters
    with pytest.raises(ApiError):
        device_query.or_(ipAddress='10.0.0.2')


def test_endpoint_standard_query_and(cbcsdk_mock):
    """Testing handling multiple and_() clauses on a query, esp. query._query_builder._collapse()."""
    api = cbcsdk_mock.api
    device_query = api.select(Device).where(hostName='Win7x64').and_(ipAddress='10.0.0.1')
    device_query.and_(ownerName='DevRel')
    # the query has parentheses added when doing third parameter
    assert device_query._query_builder._collapse() == '(hostName:Win7x64 AND ipAddress:10.0.0.1) AND ownerName:DevRel'
    request = device_query.prepare_query({})
    assert request == {'hostName': 'Win7x64', 'ipAddress': '10.0.0.1', 'ownerName': 'DevRel'}

    another_dev_query = api.select(Device).where(hostName='Win7')
    another_dev_query.and_(hostNameExact='Win7x64')
    another_dev_query.and_(ownerName='Dev')
    another_dev_query.and_(ownerNameExact='DeveloperRelations')
    assert another_dev_query._query_builder._collapse() == \
           '((hostName:Win7 AND hostNameExact:Win7x64) AND ownerName:Dev) AND ownerNameExact:DeveloperRelations'
    request = another_dev_query.prepare_query({})
    assert request == {'hostName': 'Win7', 'hostNameExact': 'Win7x64', 'ownerName': 'Dev',
                       'ownerNameExact': 'DeveloperRelations'}
