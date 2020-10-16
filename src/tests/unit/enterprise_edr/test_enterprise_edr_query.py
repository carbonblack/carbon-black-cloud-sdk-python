"""Testing Query object of cbc_sdk.enterprise_edr"""

import pytest
import logging
from cbc_sdk.enterprise_edr import Process
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.enterprise_edr.mock_process import (GET_PROCESS_SUMMARY_RESP,
                                                             GET_PROCESS_SUMMARY_RESP_1,
                                                             GET_PROCESS_VALIDATION_RESP,
                                                             GET_PROCESS_VALIDATION_RESP_INVALID,
                                                             POST_PROCESS_SEARCH_JOB_RESP,
                                                             GET_PROCESS_SEARCH_JOB_RESP,
                                                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
                                                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1)

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

@pytest.mark.parametrize('get_summary_response, get_process_search_response, guid', [
    (GET_PROCESS_SUMMARY_RESP, GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
     "test-0002b226-000015bd-00000000-1d6225bbba74c00",),
    (GET_PROCESS_SUMMARY_RESP_1, GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1,
     "test-00340b06-00000314-00000000-1d686b9e4d74f52",)])
def test_query_count(cbcsdk_mock, get_summary_response, get_process_search_response, guid):
    """Testing Process.process_pids property."""
    api = cbcsdk_mock.api
    # mock the GET of query parameter validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_job",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results"),
                             get_process_search_response)
    process_query = api.select(Process).where(f"process_guid:{guid}")
    # Query._count() returns `num_available` from the JSON response to a process query
    assert process_query._count() == 1
    assert process_query._count_valid is True


@pytest.mark.parametrize('get_process_search_response, guid', [
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00",),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52",)])
def test_query_get_query_parameters(cbcsdk_mock, get_process_search_response, guid):
    """Testing Query._get_query_parameters()."""
    api = cbcsdk_mock.api
    # mock the GET of query parameter validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_job", POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920"), GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results"), get_process_search_response)
    process_query = api.select(Process).where(f"process_guid:{guid}")
    assert process_query._get_query_parameters() == {"fields": [
        "*",
        "parent_hash",
        "parent_name",
        "process_cmdline",
        "backend_timestamp",
        "device_external_ip",
        "device_group",
        "device_internal_ip",
        "device_os",
        "device_policy",
        "process_effective_reputation",
        "process_reputation",
        "process_start_time",
        "ttp"], "process_guid": guid, "query": f'process_guid:{guid}'}


@pytest.mark.parametrize('get_process_search_response, guid', [
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP, "test-0002b226-000015bd-00000000-1d6225bbba74c00",),
    (GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1, "test-00340b06-00000314-00000000-1d686b9e4d74f52",)])
def test_query_validate_not_valid(cbcsdk_mock, get_process_search_response, guid):
    """Testing Query._validate()."""
    api = cbcsdk_mock.api
    # mock the GET of query parameter validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP_INVALID)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_job", POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920"), GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results"), get_process_search_response)
    process_query = api.select(Process).where(f"process_guid:{guid}")
    with pytest.raises(ApiError):
        params = process_query._get_query_parameters()
        process_query._validate(params)


def test_async_sort_by(cbcsdk_mock):
    """Testing AsyncProcessQuery.sort_by()."""
    api = cbcsdk_mock.api
    async_query = api.select(Process).where("process_guid:someguid")
    # add one key to sort by
    assert async_query._sort == []
    async_query.sort_by("device_timestamp", direction="ASC")
    assert async_query._sort == [{"field": "device_timestamp", "order": "ASC"}]
    assert async_query._default_args == {"sort": [{"field": "device_timestamp", "order": "ASC"}]}
    # add another key to sort by
    async_query.sort_by("key_to_sort_by", direction="DESC")
    assert async_query._sort == [{"field": "device_timestamp", "order": "ASC"},
                                 {"field": "key_to_sort_by", "order": "DESC"}]
    assert async_query._default_args == {"sort": [{"field": "device_timestamp", "order": "ASC"},
                                                  {"field": "key_to_sort_by", "order": "DESC"}]}
    # update the sort direction for a field
    async_query.sort_by("key_to_sort_by", direction="ASC")
    assert async_query._sort == [{"field": "device_timestamp", "order": "ASC"},
                                 {"field": "key_to_sort_by", "order": "ASC"}]
    assert async_query._default_args == {"sort": [{"field": "device_timestamp", "order": "ASC"},
                                                  {"field": "key_to_sort_by", "order": "ASC"}]}


def test_async_timeout(cbcsdk_mock):
    """Testing AsyncProcessQuery.timeout()."""
    api = cbcsdk_mock.api
    async_query = api.select(Process).where("process_guid:someguid")
    assert async_query._timeout == 0
    async_query.timeout(msecs=500)
    assert async_query._timeout == 500


def test_async_submit(cbcsdk_mock):
    """Testing AsyncProcessQuery._submit()."""
    api = cbcsdk_mock.api
    async_query = api.select(Process).where("process_guid:someguid")
    async_query._query_token = "the_job_id_because_this_query_was_already_submitted"
    with pytest.raises(ApiError):
        async_query._submit()
