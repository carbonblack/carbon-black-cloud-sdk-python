"""Testing Binary, Downloads objects of cbc_sdk.enterprise_edr"""

import pytest
import logging
from cbc_sdk.enterprise_edr import Downloads, Binary
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.enterprise_edr.mock_ubs import (BINARY_GET_METADATA_RESP,
                                                       BINARY_GET_DEVICE_SUMMARY_RESP,
                                                       BINARY_GET_FILE_RESP)

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

def test_binary_query(cbcsdk_mock):
    """Testing Binary Querying"""
    sha256 = "00a16c806ff694b64e566886bba5122655eff89b45226cddc8651df7860e4524"
    cbcsdk_mock.mock_request("GET", f"/ubs/v1/orgs/test/sha256/{sha256}", BINARY_GET_METADATA_RESP)
    api = cbcsdk_mock.api
    bin = api.select(Binary, sha256)
    assert isinstance(bin, Binary)
    cbcsdk_mock.mock_request("GET", f"/ubs/v1/orgs/test/sha256/{sha256}/summary/device", BINARY_GET_DEVICE_SUMMARY_RESP)
    summary = bin.summary
    cbcsdk_mock.mock_request("POST", "/ubs/v1/orgs/test/file/_download", BINARY_GET_FILE_RESP)
    url = bin.download_url
    assert summary is not None
    assert url is not None


def test_downloads_query(cbcsdk_mock):
    """Testing Downloads Querying"""
    sha256 = "00a16c806ff694b64e566886bba5122655eff89b45226cddc8651df7860e4524"
    cbcsdk_mock.mock_request("POST", "/ubs/v1/orgs/test/file/_download", BINARY_GET_FILE_RESP)
    api = cbcsdk_mock.api
    dl = api.select(Downloads, [sha256])
    assert isinstance(dl, Downloads)
    found_items = dl.found
    assert found_items[0].sha256 == sha256
    assert len(found_items) == 1
