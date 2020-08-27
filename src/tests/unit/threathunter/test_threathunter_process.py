"""Testing Process and Tree objects of cbc_sdk.threathunter"""

import pytest
import logging
from cbc_sdk.threathunter import Process, Tree
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.threathunter.mock_process import (GET_PROCESS_SUMMARY_RESP,
                                                           GET_TREE_RESP)

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

def test_process_select(cbcsdk_mock):
    """Testing Process Querying with select()"""
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/summary", GET_PROCESS_SUMMARY_RESP)
    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)
    assert isinstance(process, Process)
    assert process.process_guid == guid
    assert process.summary is not None
    assert process.siblings is not None
    summary = api.select(Process.Summary, guid)
    assert summary is not None


def test_tree_select(cbcsdk_mock):
    """Testing Tree Querying"""
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/tree", GET_TREE_RESP)
    api = cbcsdk_mock.api
    guid = "WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00"
    process = api.select(Process, guid)
    tree = process.tree()
    children = tree.nodes["children"]
    assert len(children) == len(tree.children)
    assert len(children) > 0

    procTree = api.select(Tree).where(process_guid="WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00")
    results = procTree._perform_query()
    assert results is not None
    assert results["nodes"]["children"] is not None
    assert results["incomplete_results"] is False
