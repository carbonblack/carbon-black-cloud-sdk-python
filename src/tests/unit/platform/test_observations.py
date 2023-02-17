"""Testing Observation objects of cbc_sdk.endpoint_standard"""

import pytest
import logging
from cbc_sdk.platform import Observation
from cbc_sdk.platform.observations import ObservationQuery
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
    GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP,
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
    obs = api.select(Observation, "8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e")
    assert obs["device_name"] is not None
    assert obs["enriched"] is not None


def test_observation_select_details_async(cbcsdk_mock):
    """Testing Observation Querying with get_details - asynchronous mode"""
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


def test_observations_select_details_sync_zero(cbcsdk_mock):
    """Testing Observation Querying with get_details"""
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
    obs_list = api.select(Observation).where(process_pid=1000).or_(process_pid=1000)
    for obs in obs_list:
        assert obs.device_name is not None
        assert obs.enriched is not None


def test_observations_query_implementation(cbcsdk_mock):
    """Testing Observation querying with where()."""
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
    observation_id = "8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e"
    obs_list = api.select(Observation).where(f"observation_id:{observation_id}")
    assert isinstance(obs_list, ObservationQuery)
    assert obs_list[0].observation_id == observation_id


def test_observations_timeout(cbcsdk_mock):
    """Testing ObservationQuery.timeout()."""
    api = cbcsdk_mock.api
    query = api.select(Observation).where("observation_id:some_id")
    assert query._timeout == 0
    query.timeout(msecs=500)
    assert query._timeout == 500


def test_observations_timeout_error(cbcsdk_mock):
    """Testing that a timeout in Observation querying throws a TimeoutError correctly"""
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
