"""Testing Observation objects of cbc_sdk.platform"""

import pytest
import logging

from cbc_sdk.base import FacetQuery
from cbc_sdk.platform import Observation
from cbc_sdk.platform.observations import ObservationQuery, ObservationFacet
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError, TimeoutError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock

from tests.unit.fixtures.platform.mock_observations import (
    GET_OBSERVATIONS_SEARCH_JOB_RESULTS_ZERO,
    POST_OBSERVATIONS_SEARCH_JOB_RESP,
    GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_2,
    GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_0,
    GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_ZERO_COMP,
    GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP,
    GET_OBSERVATIONS_DETAIL_JOB_RESULTS_FOR_DEOBFUSCATE,
    OBS_DEOBFUSCATE_CMDLINE_REQUEST,
    OBS_DEOBFUSCATE_CMDLINE_RESPONSE,
    GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    GET_OBSERVATIONS_SEARCH_JOB_RESULTS_NO_RULE_ID_RESP,
    POST_OBSERVATIONS_FACET_SEARCH_JOB_RESP,
    GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_1,
    GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    GET_OBSERVATIONS_GROUPED_RESULTS_RESP,
    OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    OBSERVATIONS_SEARCH_SUGGESTIONS_RESP,
)
from tests.unit.fixtures.platform.mock_network_threat_metadata import (
    GET_NETWORK_THREAT_METADATA_RESP,
)

log = logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    level=logging.DEBUG,
    filename="log.txt",
)


@pytest.fixture(scope="function")
def cb():
    """Create CBCloudAPI singleton"""
    return CBCloudAPI(
        url="https://example.com", org_key="test", token="abcd/1234", ssl_verify=False
    )


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, cb):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, cb)


# ==================================== UNIT TESTS BELOW ====================================


def test_observation_select_where(cbcsdk_mock):
    """Testing Observation Querying with select()"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=observation_id%3A8fbccc2da75f11ed937ae3cb089984c6%5C%3Abe6ff259%5C-88e3%5C-6286%5C-789f%5C-74defa192d2e",  # noqa: E501
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    obs_list = api.select(Observation).where(
        observation_id="8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e"
    )
    for obs in obs_list:
        assert obs.device_name is not None
        assert obs.enriched is not None


def test_observation_select_async(cbcsdk_mock):
    """Testing Observation Querying with select() - asynchronous way"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=observation_id%3A8fbccc2da75f11ed937ae3cb089984c6%5C%3Abe6ff259%5C-88e3%5C-6286%5C-789f%5C-74defa192d2e",  # noqa: E501
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    obs_list = (
        api.select(Observation)
        .where(
            observation_id="8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e"
        )
        .execute_async()
    )
    for obs in obs_list.result():
        assert obs["device_name"] is not None
        assert obs["enriched"] is not None


def test_observation_select_by_id(cbcsdk_mock):
    """Testing Observation Querying with select() - asynchronous way"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=observation_id%3A8fbccc2da75f11ed937ae3cb089984c6%5C%3Abe6ff259%5C-88e3%5C-6286%5C-789f%5C-74defa192d2e",  # noqa: E501
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    obs = api.select(
        Observation,
        "8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e",
    )
    assert obs["device_name"] is not None
    assert obs["enriched"] is not None


def test_observation_select_details_async(cbcsdk_mock):
    """Testing Observation Querying with get_details - asynchronous mode"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A2000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    obs_list = api.select(Observation).where(process_pid=2000)
    obs = obs_list[0]
    details = obs.get_details(async_mode=True, timeout=500)
    results = details.result()
    assert results.device_name is not None
    assert results.enriched is not None
    assert obs._details_timeout == 500
    assert results.process_pid[0] == 2000
    assert results["device_name"] is not None
    assert results["enriched"] is not None
    assert results["process_pid"][0] == 2000


def test_observations_details_only(cbcsdk_mock):
    """Testing Observation with get_details - just the get_details REST API calls"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    obs = Observation(api, initial_data={"observation_id": "test"})
    results = obs._get_detailed_results()
    assert results._info["device_name"] is not None
    assert results._info["enriched"] is not None
    assert results._info["process_pid"][0] == 2000


def test_observations_details_timeout(cbcsdk_mock):
    """Testing Observation get_details() timeout handling"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_ZERO_COMP,
    )

    api = cbcsdk_mock.api
    obs = Observation(api, initial_data={"observation_id": "test"})
    obs._details_timeout = 1
    with pytest.raises(TimeoutError):
        obs._get_detailed_results()


def test_observations_select_details_sync(cbcsdk_mock):
    """Testing Observation Querying with get_details"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A2000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP,
    )

    s_api = cbcsdk_mock.api
    obs_list = s_api.select(Observation).where(process_pid=2000)
    obs = obs_list[0]
    results = obs.get_details()
    assert results["device_name"] is not None
    assert results.device_name is not None
    assert results.enriched is True
    assert results.process_pid[0] == 2000


def test_observations_select_details_refresh(cbcsdk_mock):
    """Testing Observation Querying with get_details"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A2000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP,
    )

    s_api = cbcsdk_mock.api
    obs_list = s_api.select(Observation).where(process_pid=2000)
    obs = obs_list[0]
    assert obs.device_name is not None
    assert obs.enriched is True
    assert obs.process_pid[0] == 2000
    # this one is present only in the details
    assert len(obs.ttp) == 4


def test_observations_select_details_sync_zero(cbcsdk_mock):
    """Testing Observation Querying with get_details"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A2000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_ZERO,
    )

    s_api = cbcsdk_mock.api
    obs_list = s_api.select(Observation).where(process_pid=2000)
    obs = obs_list[0]
    results = obs.get_details()
    assert results["device_name"] is not None
    assert results.get("alert_id") == []


def test_observations_select_compound(cbcsdk_mock):
    """Testing Observation Querying with select() and more complex criteria"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A1000+OR+process_pid%3A1000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    obs_list = api.select(Observation).where(process_pid=1000).or_(process_pid=1000)
    for obs in obs_list:
        assert obs.device_name is not None
        assert obs.enriched is not None


def test_observations_query_implementation(cbcsdk_mock):
    """Testing Observation querying with where()."""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=observation_id%3A8fbccc2da75f11ed937ae3cb089984c6%3Abe6ff259-88e3-6286-789f-74defa192d2e",  # noqa: E501
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    api = cbcsdk_mock.api
    observation_id = (
        "8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e"
    )
    obs_list = api.select(Observation).where(f"observation_id:{observation_id}")
    assert isinstance(obs_list, ObservationQuery)
    assert obs_list[0].observation_id == observation_id


def test_observations_timeout(cbcsdk_mock):
    """Testing ObservationQuery.timeout()."""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=observation_id%3A8fbccc2da75f11ed937ae3cb089984c6%5C%3Abe6ff259%5C-88e3%5C-6286%5C-789f%5C-74defa192d2e",  # noqa: E501
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    api = cbcsdk_mock.api
    query = api.select(Observation).where("observation_id:some_id")
    assert query._timeout == 300000
    query.timeout(msecs=500)
    assert query._timeout == 500
    query.timeout(msecs=999999)
    assert query._timeout == 300000
    query.timeout(msecs=700)
    assert query._timeout == 700
    query.timeout(msecs=0)
    assert query._timeout == 300000


def test_observations_timeout_error(cbcsdk_mock):
    """Testing that a timeout in Observation querying throws a TimeoutError correctly"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=observation_id%3A8fbccc2da75f11ed937ae3cb089984c6%3Abe6ff259-88e3-6286-789f-74defa192d2e",  # noqa: E501
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    )

    api = cbcsdk_mock.api
    obs_list = (
        api.select(Observation)
        .where(
            "observation_id:8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e"
        )
        .timeout(1)
    )
    with pytest.raises(TimeoutError):
        list(obs_list)
    obs_list = (
        api.select(Observation)
        .where(
            "observation_id:8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e"
        )
        .timeout(1)
    )
    with pytest.raises(TimeoutError):
        obs_list._count()


def test_observations_query_sort(cbcsdk_mock):
    """Testing Observation results sort."""
    api = cbcsdk_mock.api
    obs_list = (
        api.select(Observation)
        .where(process_pid=1000)
        .or_(process_pid=1000)
        .sort_by("process_pid", direction="DESC")
    )
    assert obs_list._sort_by == [{"field": "process_pid", "order": "DESC"}]


def test_observations_rows(cbcsdk_mock):
    """Testing Observation results sort."""
    api = cbcsdk_mock.api
    obs_list = api.select(Observation).where(process_pid=1000).set_rows(1500)
    assert obs_list._batch_size == 1500
    with pytest.raises(ApiError) as ex:
        api.select(Observation).where(process_pid=1000).set_rows("alabala")
    assert "Rows must be an integer." in str(ex)
    with pytest.raises(ApiError) as ex:
        api.select(Observation).where(process_pid=1000).set_rows(10001)
    assert "Maximum allowed value for rows is 10000" in str(ex)


def test_observations_time_range(cbcsdk_mock):
    """Testing Observation results sort."""
    api = cbcsdk_mock.api
    obs_list = (
        api.select(Observation)
        .where(process_pid=1000)
        .set_time_range(
            start="2020-10-10T20:34:07Z", end="2020-10-20T20:34:07Z", window="-1d"
        )
    )
    assert obs_list._time_range["start"] == "2020-10-10T20:34:07Z"
    assert obs_list._time_range["end"] == "2020-10-20T20:34:07Z"
    assert obs_list._time_range["window"] == "-1d"


def test_observations_submit(cbcsdk_mock):
    """Test _submit method of ObservationQuery class"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A1000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    api = cbcsdk_mock.api
    obs_list = api.select(Observation).where(process_pid=1000)
    obs_list._submit()
    assert obs_list._query_token == "08ffa932-b633-4107-ba56-8741e929e48b"
    with pytest.raises(ApiError) as ex:
        obs_list._submit()
    assert "Query already submitted: token" in str(ex)


def test_observations_count(cbcsdk_mock):
    """Test _submit method of Observationquery class"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A1000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_2,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    obs_list = api.select(Observation).where(process_pid=1000)
    obs_list._count()
    assert obs_list._count() == 52


def test_observations_search(cbcsdk_mock):
    """Test _search method of Observationquery class"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A2000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_2,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    obs_list = api.select(Observation).where(process_pid=2000)
    obs_list._search()
    assert obs_list[0].process_pid[0] == 2000
    obs_list._search(start=1)
    assert obs_list[0].process_pid[0] == 2000


def test_observations_still_querying(cbcsdk_mock):
    """Test _search method of Observationquery class"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A1000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_0,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    )

    api = cbcsdk_mock.api
    obs_list = api.select(Observation).where(process_pid=1000)
    assert obs_list._still_querying() is True


def test_observations_still_querying2(cbcsdk_mock):
    """Test _search method of Observationquery class"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A1000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_ZERO_COMP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    )

    api = cbcsdk_mock.api
    obs_list = api.select(Observation).where(process_pid=1000)
    assert obs_list._still_querying() is True


def test_observation_deobfuscate_cmdline(cbcsdk_mock):
    """Test the deobfuscate_cmdline() function."""
    def on_post_deobfuscate(url, body, **kwargs):
        assert body == OBS_DEOBFUSCATE_CMDLINE_REQUEST
        return OBS_DEOBFUSCATE_CMDLINE_RESPONSE

    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/observations/detail_jobs",
                             POST_OBSERVATIONS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",
        GET_OBSERVATIONS_DETAIL_JOB_RESULTS_FOR_DEOBFUSCATE)
    cbcsdk_mock.mock_request("POST", "/tau/v2/orgs/test/reveal", on_post_deobfuscate)

    api = cbcsdk_mock.api
    obs = Observation(api, initial_data={"observation_id": "test"})
    observation = obs._get_detailed_results()
    deobfuscation = observation.deobfuscate_cmdline()
    assert len(deobfuscation['identities']) == 1
    assert len(deobfuscation['strings']) == 1
    assert deobfuscation['deobfuscated_code'] == \
           "Write-Output \"No matter how thin you slice it, it's still baloney.\"\n"


# --------------------- ObservationFacet --------------------------------------


def test_observation_facet_select_where(cbcsdk_mock):
    """Testing Observation Querying with select()"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/facet_jobs",
        POST_OBSERVATIONS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/facet_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    observations = (
        api.select(ObservationFacet)
        .where(process_name="chrome.exe")
        .add_facet_field("process_name")
    )
    observation = observations.results
    assert observation.terms is not None
    assert observation.ranges is not None
    assert observation.ranges == []
    assert observation.terms[0]["field"] == "process_name"


def test_observation_facet_select_async(cbcsdk_mock):
    """Testing Observation Querying with select()"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/facet_jobs",
        POST_OBSERVATIONS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/facet_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    future = (
        api.select(ObservationFacet)
        .where(process_name="chrome.exe")
        .add_facet_field("process_name")
        .execute_async()
    )
    observation = future.result()
    assert observation.terms is not None
    assert observation.ranges is not None
    assert observation.ranges == []
    assert observation.terms[0]["field"] == "process_name"


def test_observation_facet_select_compound(cbcsdk_mock):
    """Testing Observation Querying with select() and more complex criteria"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/facet_jobs",
        POST_OBSERVATIONS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/facet_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    observations = (
        api.select(ObservationFacet)
        .where(process_name="chrome.exe")
        .or_(process_name="firefox.exe")
        .add_facet_field("process_name")
    )
    observation = observations.results
    assert observation.terms_.fields == ["process_name"]
    assert observation.ranges == []


def test_observation_facet_query_implementation(cbcsdk_mock):
    """Testing Observation querying with where()."""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A2000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/facet_jobs",
        POST_OBSERVATIONS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/facet_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_1,
    )

    api = cbcsdk_mock.api
    field = "process_name"
    observations = (
        api.select(ObservationFacet)
        .where(process_name="test")
        .add_facet_field("process_name")
    )
    assert isinstance(observations, FacetQuery)
    observation = observations.results
    assert observation.terms[0]["field"] == field
    assert observation.terms_.facets["process_name"] is not None
    assert observation.terms_.fields[0] == "process_name"
    assert observation.ranges_.facets is not None
    assert observation.ranges_.fields[0] == "device_timestamp"
    assert isinstance(observation._query_implementation(api), FacetQuery)


def test_observation_facet_timeout(cbcsdk_mock):
    """Testing ObservationQuery.timeout()."""
    api = cbcsdk_mock.api
    query = (
        api.select(ObservationFacet)
        .where("process_name:some_name")
        .add_facet_field("process_name")
    )
    assert query._timeout == 300000
    query.timeout(msecs=500)
    assert query._timeout == 500
    query.timeout(msecs=999999)
    assert query._timeout == 300000
    query.timeout(msecs=700)
    assert query._timeout == 700
    query.timeout(msecs=0)
    assert query._timeout == 300000


def test_observation_facet_timeout_error(cbcsdk_mock):
    """Testing that a timeout in ObservationQuery throws the right TimeoutError."""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/facet_jobs",
        POST_OBSERVATIONS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/facet_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    )

    api = cbcsdk_mock.api
    query = (
        api.select(ObservationFacet)
        .where("process_name:some_name")
        .add_facet_field("process_name")
        .timeout(1)
    )
    with pytest.raises(TimeoutError):
        query.results()
    query = (
        api.select(ObservationFacet)
        .where("process_name:some_name")
        .add_facet_field("process_name")
        .timeout(1)
    )
    with pytest.raises(TimeoutError):
        query._count()


def test_observation_facet_query_add_range(cbcsdk_mock):
    """Testing Observation results sort."""
    api = cbcsdk_mock.api
    range = ({"bucket_size": 30, "start": "0D", "end": "20D", "field": "something"},)
    observations = (
        api.select(ObservationFacet)
        .where(process_pid=1000)
        .add_range(range)
        .add_facet_field("process_name")
    )
    assert observations._ranges[0]["bucket_size"] == 30
    assert observations._ranges[0]["start"] == "0D"
    assert observations._ranges[0]["end"] == "20D"
    assert observations._ranges[0]["field"] == "something"


def test_observation_facet_query_check_range(cbcsdk_mock):
    """Testing Observation results sort."""
    api = cbcsdk_mock.api
    range = ({"bucket_size": [], "start": "0D", "end": "20D", "field": "something"},)
    with pytest.raises(ApiError):
        api.select(ObservationFacet).where(process_pid=1000).add_range(
            range
        ).add_facet_field("process_name")

    range = ({"bucket_size": 30, "start": [], "end": "20D", "field": "something"},)
    with pytest.raises(ApiError):
        api.select(ObservationFacet).where(process_pid=1000).add_range(
            range
        ).add_facet_field("process_name")

    range = ({"bucket_size": 30, "start": "0D", "end": [], "field": "something"},)
    with pytest.raises(ApiError):
        api.select(ObservationFacet).where(process_pid=1000).add_range(
            range
        ).add_facet_field("process_name")

    range = ({"bucket_size": 30, "start": "0D", "end": "20D", "field": []},)
    with pytest.raises(ApiError):
        api.select(ObservationFacet).where(process_pid=1000).add_range(
            range
        ).add_facet_field("process_name")


def test_observation_facet_query_add_facet_field(cbcsdk_mock):
    """Testing Observation results sort."""
    api = cbcsdk_mock.api
    observations = (
        api.select(ObservationFacet)
        .where(process_pid=1000)
        .add_facet_field("process_name")
    )
    assert observations._facet_fields[0] == "process_name"


def test_observation_facet_query_add_facet_fields(cbcsdk_mock):
    """Testing Observation results sort."""
    api = cbcsdk_mock.api
    observations = (
        api.select(ObservationFacet)
        .where(process_pid=1000)
        .add_facet_field(["process_name", "process_pid"])
    )
    assert "process_pid" in observations._facet_fields
    assert "process_name" in observations._facet_fields


def test_observation_facet_query_add_facet_invalid_fields(cbcsdk_mock):
    """Testing Observation results sort."""
    api = cbcsdk_mock.api
    with pytest.raises(TypeError):
        api.select(ObservationFacet).where(process_pid=1000).add_facet_field(1337)


def test_observation_facet_limit(cbcsdk_mock):
    """Testing Observation results sort."""
    api = cbcsdk_mock.api
    observations = (
        api.select(ObservationFacet)
        .where(process_pid=1000)
        .limit(123)
        .add_facet_field("process_name")
    )
    assert observations._limit == 123


def test_observation_facet_time_range(cbcsdk_mock):
    """Testing Observation results sort."""
    api = cbcsdk_mock.api
    observations = (
        api.select(ObservationFacet)
        .where(process_pid=1000)
        .set_time_range(
            start="2020-10-10T20:34:07Z", end="2020-10-20T20:34:07Z", window="-1d"
        )
        .add_facet_field("process_name")
    )
    assert observations._time_range["start"] == "2020-10-10T20:34:07Z"
    assert observations._time_range["end"] == "2020-10-20T20:34:07Z"
    assert observations._time_range["window"] == "-1d"


def test_observation_facet_submit(cbcsdk_mock):
    """Test _submit method of ObservationQuery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/facet_jobs",
        POST_OBSERVATIONS_FACET_SEARCH_JOB_RESP,
    )
    api = cbcsdk_mock.api
    observations = (
        api.select(ObservationFacet)
        .where(process_pid=1000)
        .add_facet_field("process_name")
    )
    observations._submit()
    assert observations._query_token == "08ffa932-b633-4107-ba56-8741e929e48b"


def test_observation_facet_count(cbcsdk_mock):
    """Test _submit method of ObservationQuery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/facet_jobs",
        POST_OBSERVATIONS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/facet_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_1,
    )

    api = cbcsdk_mock.api
    observations = (
        api.select(ObservationFacet)
        .where(process_pid=1000)
        .add_facet_field("process_name")
    )
    observations._count()
    assert observations._count() == 116


def test_observation_search(cbcsdk_mock):
    """Test _search method of ObservationQuery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/facet_jobs",
        POST_OBSERVATIONS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/facet_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    observations = (
        api.select(ObservationFacet)
        .where(process_pid=1000)
        .add_facet_field("process_name")
    )
    future = observations.execute_async()
    result = future.result()
    assert result.terms is not None
    assert len(result.ranges) == 0
    assert result.terms[0]["field"] == "process_name"


def test_observation_search_async(cbcsdk_mock):
    """Test _search method of ObservationQuery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/facet_jobs",
        POST_OBSERVATIONS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/facet_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    observations = (
        api.select(ObservationFacet)
        .where(process_pid=1000)
        .add_facet_field("process_name")
    )
    future = observations.execute_async()
    result = future.result()
    assert result.terms is not None
    assert len(result.ranges) == 0
    assert result.terms[0]["field"] == "process_name"


def test_observation_aggregation_wrong_field(cbcsdk_mock):
    """Testing passing wrong aggregation_field"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError):
        for i in (
            api.select(Observation)
            .where(process_pid=2000)
            .get_group_results("wrong_field")
        ):
            print(i)
    with pytest.raises(ApiError):
        for i in api.select(Observation).where(process_pid=2000).get_group_results(1):
            print(i)


def test_observation_select_group_results(cbcsdk_mock):
    """Testing Observation Querying with select() and more complex criteria"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=process_pid%3A2000",
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/group_results",  # noqa: E501
        GET_OBSERVATIONS_GROUPED_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    observation_groups = list(
        api.select(Observation)
        .where(process_pid=2000)
        .get_group_results(
            "device_name",
            max_events_per_group=10,
            rows=5,
            start=0,
            range_field="backend_timestamp",
            range_duration="-2y",
            range_method="interval"
        )
    )
    # invoke get_details() on the first Observation in the list
    observation_groups[0].observations[0].get_details()
    assert len(observation_groups[0].observations[0].ttp) == 4
    assert observation_groups[0].group_key is not None
    assert observation_groups[0]["group_key"] is not None
    assert observation_groups[0].observations[0]["enriched"] is not None
    assert observation_groups[0].observations[0]["process_pid"][0] == 2000


# ---------- Network Threat Metadata


def test_observation_get_threat_metadata_api_error(cbcsdk_mock):
    """Testing get network threat metadata through observation - no rule_id"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=observation_id%3A8fbccc2da75f11ed937ae3cb089984c6%5C%3Abe6ff259%5C-88e3%5C-6286%5C-789f%5C-74defa192d2e",  # noqa: E501
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_NO_RULE_ID_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_NO_RULE_ID_RESP,
    )

    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )

    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    obs_list = api.select(Observation).where(
        observation_id="8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e"
    )
    obs = obs_list[0]
    with pytest.raises(ApiError):
        obs.get_network_threat_metadata()


def test_observation_get_threat_metadata(cbcsdk_mock):
    """Testing get network threat metadata through observation"""
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_validation?q=observation_id%3A8fbccc2da75f11ed937ae3cb089984c6%5C%3Abe6ff259%5C-88e3%5C-6286%5C-789f%5C-74defa192d2e",  # noqa: E501
        OBSERVATIONS_SEARCH_VALIDATIONS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/search_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results?start=0&rows=500",  # noqa: E501
        GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
    )

    cbcsdk_mock.mock_request(
        "GET",
        "/threatmetadata/v1/orgs/test/detectors/8a4b43c5-5e0a-4f7d-aa46-bd729f1989a7",
        GET_NETWORK_THREAT_METADATA_RESP,
    )

    api = cbcsdk_mock.api
    obs_list = api.select(Observation).where(
        observation_id="8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e"
    )
    obs = obs_list[0]
    threat_meta_data = obs.get_network_threat_metadata()
    assert threat_meta_data["detector_abstract"]
    assert threat_meta_data["detector_goal"]
    assert threat_meta_data["threat_public_comment"]


def test_observations_search_suggestions(cbcsdk_mock):
    """Tests getting observations search suggestions"""
    api = cbcsdk_mock.api
    q = "suggest.count=10&suggest.q=device_id"
    cbcsdk_mock.mock_request(
        "GET",
        f"/api/investigate/v2/orgs/test/observations/search_suggestions?{q}",
        OBSERVATIONS_SEARCH_SUGGESTIONS_RESP,
    )
    result = Observation.search_suggestions(api, "device_id", 10)
    assert len(result) != 0


def test_observations_search_suggestions_api_error():
    """Tests getting observations search suggestions - no CBCloudAPI arg"""
    with pytest.raises(ApiError):
        Observation.search_suggestions("", "device_id", 10)


def test_bulk_get_details_api_error(cb):
    """Tests bulk_get_details"""
    with pytest.raises(ApiError):
        Observation.bulk_get_details(cb, alert_id="xx")


def test_helper_get_details_api_error(cb):
    """Tests _helper_get_details"""
    with pytest.raises(ApiError):
        Observation._helper_get_details(cb, alert_id="xx")


def test_bulk_get_details_neither(cbcsdk_mock):
    """Tests getting bulk_get_details - no alert_id or observation_ids"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError):
        Observation.bulk_get_details(api)


def test_bulk_get_details_both(cbcsdk_mock):
    """Tests getting bulk_get_details - both alert_id and observation_ids is provided"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError):
        Observation.bulk_get_details(api, "xxx", ["xxx"])


def test_bulk_get_details(cbcsdk_mock):
    """Tests getting bulk_get_details with observation_ids"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    results = Observation.bulk_get_details(
        api,
        observation_ids=[
            "c7bdd379ac2f11ed92c0b59a6de446c9:fbb78467-f63c-ac52-622a-f41c6f07d815"
        ],
    )
    assert len(results) == 1
    assert results[0]["device_name"] is not None
    assert results[0].device_name is not None
    assert results[0].enriched is True
    assert results[0].process_pid[0] == 2000


def test_bulk_get_details_alert_id(cbcsdk_mock):
    """Tests getting bulk_get_details with alert_id"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/observations/detail_jobs",
        POST_OBSERVATIONS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/observations/detail_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
        GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    results = Observation.bulk_get_details(
        api, alert_id="fbb78467-f63c-ac52-622a-f41c6f07d815"
    )
    assert len(results) == 1
    assert results[0]["device_name"] is not None
    assert results[0].device_name is not None
    assert results[0].enriched is True
    assert results[0].process_pid[0] == 2000
