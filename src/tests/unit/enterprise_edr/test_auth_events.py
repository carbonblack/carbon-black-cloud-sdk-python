"""Testing AuthEvents objects of cbc_sdk.enterprise_edr"""

import pytest
import logging

from cbc_sdk.base import FacetQuery
from cbc_sdk.enterprise_edr import AuthEvents
from cbc_sdk.enterprise_edr.auth_events import AuthEventsQuery, AuthEventsFacet
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError, TimeoutError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock

from tests.unit.fixtures.enterprise_edr.mock_auth_events import (
    POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    GET_AUTH_EVENTS_DETAIL_JOB_RESULTS_RESP,
    GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_ZERO_COMP,
    GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_ZERO,
    GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_2,
    GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_0,
    POST_AUTH_EVENTS_FACET_SEARCH_JOB_RESP,
    GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_1,
    GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    GET_AUTH_EVENTS_GROUPED_RESULTS_RESP,
    AUTH_EVENTS_SEARCH_VALIDATIONS_RESP,
    AUTH_EVENTS_SEARCH_SUGGESTIONS_RESP
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


def test_auth_events_select_where(cbcsdk_mock):
    """Testing AuthEvents Querying with select()"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where("auth_username:SYSTEM")
    for event in events_list:
        assert event.device_name is not None


def test_auth_events_select_async(cbcsdk_mock):
    """Testing AuthEvents Querying with select() - asynchronous way"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where(event_id="DA9E269E-421D-469D-A212-9062888A02F4").execute_async()
    for event in events_list.result():
        assert event["device_name"] is not None


def test_auth_events_select_by_id(cbcsdk_mock):
    """Testing AuthEvents Querying with select() - asynchronous way"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    auth_events = api.select(AuthEvents, "DA9E269E-421D-469D-A212-9062888A02F4")
    assert auth_events["device_name"] is not None


def test_auth_events_select_details_async(cbcsdk_mock):
    """Testing AuthEvents Querying with get_details - asynchronous mode"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    # events_list = api.select(AuthEvents).where(process_pid=2000)
    events_list = api.select(AuthEvents).where(event_id="DA9E269E-421D-469D-A212-9062888A02F4")
    events = events_list[0]
    details = events.get_details(async_mode=True, timeout=500)
    results = details.result()
    assert results.device_name is not None
    assert events._details_timeout == 500
    assert results.process_pid[0] == 764
    assert results["device_name"] is not None
    assert results["process_pid"][0] == 764


def test_auth_events_details_only(cbcsdk_mock):
    """Testing AuthEvents with get_details - just the get_details REST API calls"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    events = AuthEvents(api, initial_data={"event_id": "D06DC822-B25E-4162-A5A7-6166BFA9B8DF"})
    results = events._get_detailed_results()
    assert results._info["device_name"] is not None
    assert results._info["process_pid"][0] == 764


def test_auth_events_details_timeout(cbcsdk_mock):
    """Testing AuthEvents get_details() timeout handling"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_ZERO_COMP,
    )

    api = cbcsdk_mock.api
    events = AuthEvents(api, initial_data={"event_id": "D06DC822-B25E-4162-A5A7-6166BFA9B8DF"})
    events._details_timeout = 1
    with pytest.raises(TimeoutError):
        events._get_detailed_results()


def test_auth_events_select_details_sync(cbcsdk_mock):
    """Testing AuthEvents Querying with get_details"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where(process_pid=2000)
    events = events_list[0]
    results = events.get_details()
    assert results["device_name"] is not None
    assert results.device_name is not None
    assert results.process_pid[0] == 764


def test_auth_events_select_details_refresh(cbcsdk_mock):
    """Testing AuthEvents Querying with get_details"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where(event_id="DA9E269E-421D-469D-A212-9062888A02F4")
    events = events_list[0]
    assert events.device_name is not None
    assert events.process_pid[0] == 776


def test_auth_events_select_details_sync_zero(cbcsdk_mock):
    """Testing AuthEvents Querying with get_details"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_ZERO,
    )

    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where(process_pid=2000)
    events = events_list[0]
    results = events.get_details()
    assert results["device_name"] is not None
    assert results.get("alert_id") == []


def test_auth_events_select_compound(cbcsdk_mock):
    """Testing AuthEvents Querying with select() and more complex criteria"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where(process_pid=776).or_(parent_pid=608)
    for events in events_list:
        assert events.device_name is not None


def test_auth_events_query_implementation(cbcsdk_mock):
    """Testing AuthEvents querying with where()."""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP,
    )
    api = cbcsdk_mock.api
    event_id = (
        "DA9E269E-421D-469D-A212-9062888A02F4"
    )
    events_list = api.select(AuthEvents).where(f"event_id:{event_id}")
    assert isinstance(events_list, AuthEventsQuery)
    assert events_list[0].event_id == event_id


def test_auth_events_timeout(cbcsdk_mock):
    """Testing AuthEventsQuery.timeout()."""
    api = cbcsdk_mock.api
    query = api.select(AuthEvents).where("event_id:some_id")
    assert query._timeout == 0
    query.timeout(msecs=500)
    assert query._timeout == 500


def test_auth_events_timeout_error(cbcsdk_mock):
    """Testing that a timeout in AuthEvents querying throws a TimeoutError correctly"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    )

    api = cbcsdk_mock.api
    events_list = (api.select(AuthEvents).where("event_id:DA9E269E-421D-469D-A212-9062888A02F4").timeout(1))
    with pytest.raises(TimeoutError):
        list(events_list)
    events_list = (api.select(AuthEvents).where("event_id:DA9E269E-421D-469D-A212-9062888A02F4").timeout(1))
    with pytest.raises(TimeoutError):
        events_list._count()


def test_auth_events_query_sort(cbcsdk_mock):
    """Testing AuthEvents results sort."""
    api = cbcsdk_mock.api
    events_list = (
        api.select(AuthEvents)
        .where(process_pid=1000)
        .or_(process_pid=1000)
        .sort_by("process_pid", direction="DESC")
    )
    assert events_list._sort_by == [{"field": "process_pid", "order": "DESC"}]


def test_auth_events_rows(cbcsdk_mock):
    """Testing AuthEvents results sort."""
    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where(process_pid=1000).set_rows(1500)
    assert events_list._batch_size == 1500
    with pytest.raises(ApiError) as ex:
        api.select(AuthEvents).where(process_pid=1000).set_rows("alabala")
    assert "Rows must be an integer." in str(ex)
    with pytest.raises(ApiError) as ex:
        api.select(AuthEvents).where(process_pid=1000).set_rows(10001)
    assert "Maximum allowed value for rows is 10000" in str(ex)


def test_auth_events_time_range(cbcsdk_mock):
    """Testing AuthEvents results sort."""
    api = cbcsdk_mock.api
    events_list = (
        api.select(AuthEvents)
        .where(process_pid=1000)
        .set_time_range(
            start="2020-10-10T20:34:07Z", end="2020-10-20T20:34:07Z", window="-1d"
        )
    )
    assert events_list._time_range["start"] == "2020-10-10T20:34:07Z"
    assert events_list._time_range["end"] == "2020-10-20T20:34:07Z"
    assert events_list._time_range["window"] == "-1d"


def test_auth_events_submit(cbcsdk_mock):
    """Test _submit method of AuthEventsQuery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where(process_pid=1000)
    events_list._submit()
    assert events_list._query_token == "62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs"
    with pytest.raises(ApiError) as ex:
        events_list._submit()
    assert "Query already submitted: token" in str(ex)


def test_auth_events_count(cbcsdk_mock):
    """Test _submit method of AuthEventsquery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_2,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where(process_pid=1000)
    events_list._count()
    assert events_list._count() == 198


def test_auth_events_search(cbcsdk_mock):
    """Test _search method of AuthEventsquery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_2,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where(process_pid=828)
    events_list._search()
    assert events_list[0].process_pid[0] == 828
    events_list._search(start=1)
    assert events_list[0].process_pid[0] == 828


def test_auth_events_still_querying(cbcsdk_mock):
    """Test _search method of AuthEventsquery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_0,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    )

    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where(process_pid=1000)
    assert events_list._still_querying() is True


def test_auth_events_still_querying2(cbcsdk_mock):
    """Test _search method of AuthEventsquery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_ZERO_COMP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results?start=0&rows=500",  # noqa: E501
        GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    )

    api = cbcsdk_mock.api
    events_list = api.select(AuthEvents).where(process_pid=1000)
    assert events_list._still_querying() is True


# --------------------- AuthEventsFacet --------------------------------------


def test_auth_events_facet_select_where(cbcsdk_mock):
    """Testing AuthEvents Querying with select()"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs",
        POST_AUTH_EVENTS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_name="chrome.exe")
        .add_facet_field("process_name")
    )
    event = auth_events.results
    assert event.terms is not None
    assert event.ranges is not None
    assert event.ranges == []
    assert event.terms[0]["field"] == "process_name"


def test_auth_events_facet_select_async(cbcsdk_mock):
    """Testing AuthEvents Querying with select()"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs",
        POST_AUTH_EVENTS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    future = (
        api.select(AuthEventsFacet)
        .where(process_name="chrome.exe")
        .add_facet_field("process_name")
        .execute_async()
    )
    event = future.result()
    assert event.terms is not None
    assert event.ranges is not None
    assert event.ranges == []
    assert event.terms[0]["field"] == "process_name"


def test_auth_events_facet_select_compound(cbcsdk_mock):
    """Testing AuthEvents Querying with select() and more complex criteria"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs",
        POST_AUTH_EVENTS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_name="chrome.exe")
        .or_(process_name="firefox.exe")
        .add_facet_field("process_name")
    )
    event = auth_events.results
    assert event.terms_.fields == ["process_name"]
    assert event.ranges == []


def test_auth_events_facet_query_implementation(cbcsdk_mock):
    """Testing AuthEvents querying with where()."""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs",
        POST_AUTH_EVENTS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_1,
    )

    api = cbcsdk_mock.api
    field = "process_name"
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_name="test")
        .add_facet_field("process_name")
    )
    assert isinstance(auth_events, FacetQuery)
    event = auth_events.results
    assert event.terms[0]["field"] == field
    assert event.terms_.facets["process_name"] is not None
    assert event.terms_.fields[0] == "process_name"
    assert event.ranges_.facets is not None
    assert event.ranges_.fields[0] == "device_timestamp"
    assert isinstance(event._query_implementation(api), FacetQuery)


def test_auth_events_facet_timeout(cbcsdk_mock):
    """Testing AuthEventsQuery.timeout()."""
    api = cbcsdk_mock.api
    query = (
        api.select(AuthEventsFacet)
        .where("process_name:some_name")
        .add_facet_field("process_name")
    )
    assert query._timeout == 0
    query.timeout(msecs=500)
    assert query._timeout == 500


def test_auth_events_facet_timeout_error(cbcsdk_mock):
    """Testing that a timeout in AuthEventsQuery throws the right TimeoutError."""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs",
        POST_AUTH_EVENTS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING,
    )

    api = cbcsdk_mock.api
    query = (
        api.select(AuthEventsFacet)
        .where("process_name:some_name")
        .add_facet_field("process_name")
        .timeout(1)
    )
    with pytest.raises(TimeoutError):
        query.results()
    query = (
        api.select(AuthEventsFacet)
        .where("process_name:some_name")
        .add_facet_field("process_name")
        .timeout(1)
    )
    with pytest.raises(TimeoutError):
        query._count()


def test_auth_events_facet_query_add_range(cbcsdk_mock):
    """Testing AuthEvents results sort."""
    api = cbcsdk_mock.api
    range = ({"bucket_size": 30, "start": "0D", "end": "20D", "field": "something"},)
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_pid=1000)
        .add_range(range)
        .add_facet_field("process_name")
    )
    assert auth_events._ranges[0]["bucket_size"] == 30
    assert auth_events._ranges[0]["start"] == "0D"
    assert auth_events._ranges[0]["end"] == "20D"
    assert auth_events._ranges[0]["field"] == "something"


def test_auth_events_facet_query_check_range(cbcsdk_mock):
    """Testing AuthEvents results sort."""
    api = cbcsdk_mock.api
    range = ({"bucket_size": [], "start": "0D", "end": "20D", "field": "something"},)
    with pytest.raises(ApiError):
        api.select(AuthEventsFacet).where(process_pid=1000).add_range(
            range
        ).add_facet_field("process_name")

    range = ({"bucket_size": 30, "start": [], "end": "20D", "field": "something"},)
    with pytest.raises(ApiError):
        api.select(AuthEventsFacet).where(process_pid=1000).add_range(
            range
        ).add_facet_field("process_name")

    range = ({"bucket_size": 30, "start": "0D", "end": [], "field": "something"},)
    with pytest.raises(ApiError):
        api.select(AuthEventsFacet).where(process_pid=1000).add_range(
            range
        ).add_facet_field("process_name")

    range = ({"bucket_size": 30, "start": "0D", "end": "20D", "field": []},)
    with pytest.raises(ApiError):
        api.select(AuthEventsFacet).where(process_pid=1000).add_range(
            range
        ).add_facet_field("process_name")


def test_auth_events_facet_query_add_facet_field(cbcsdk_mock):
    """Testing AuthEvents results sort."""
    api = cbcsdk_mock.api
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_pid=1000)
        .add_facet_field("process_name")
    )
    assert auth_events._facet_fields[0] == "process_name"


def test_auth_events_facet_query_add_facet_fields(cbcsdk_mock):
    """Testing AuthEvents results sort."""
    api = cbcsdk_mock.api
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_pid=1000)
        .add_facet_field(["process_name", "process_pid"])
    )
    assert "process_pid" in auth_events._facet_fields
    assert "process_name" in auth_events._facet_fields


def test_auth_events_facet_query_add_facet_invalid_fields(cbcsdk_mock):
    """Testing AuthEvents results sort."""
    api = cbcsdk_mock.api
    with pytest.raises(TypeError):
        api.select(AuthEventsFacet).where(process_pid=1000).add_facet_field(1337)


def test_auth_events_facet_limit(cbcsdk_mock):
    """Testing AuthEvents results limit."""
    api = cbcsdk_mock.api
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_pid=1000)
        .limit(123)
        .add_facet_field("process_name")
    )
    assert auth_events._limit == 123


def test_auth_events_facet_time_range(cbcsdk_mock):
    """Testing AuthEvents results range."""
    api = cbcsdk_mock.api
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_pid=1000)
        .set_time_range(
            start="2020-10-10T20:34:07Z", end="2020-10-20T20:34:07Z", window="-1d"
        )
        .add_facet_field("process_name")
    )
    assert auth_events._time_range["start"] == "2020-10-10T20:34:07Z"
    assert auth_events._time_range["end"] == "2020-10-20T20:34:07Z"
    assert auth_events._time_range["window"] == "-1d"


def test_auth_events_facet_submit(cbcsdk_mock):
    """Test _submit method of AuthEventsQuery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs",
        POST_AUTH_EVENTS_FACET_SEARCH_JOB_RESP,
    )
    api = cbcsdk_mock.api
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_pid=1000)
        .add_facet_field("process_name")
    )
    auth_events._submit()
    assert auth_events._query_token == "62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs"


def test_auth_events_facet_count(cbcsdk_mock):
    """Test _submit method of AuthEventsQuery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs",
        POST_AUTH_EVENTS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_1,
    )

    api = cbcsdk_mock.api
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_pid=1000)
        .add_facet_field("process_name")
    )
    auth_events._count()
    assert auth_events._count() == 116


def test_auth_events_search(cbcsdk_mock):
    """Test _search method of AuthEventsQuery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs",
        POST_AUTH_EVENTS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_pid=1000)
        .add_facet_field("process_name")
    )
    future = auth_events.execute_async()
    result = future.result()
    assert result.terms is not None
    assert len(result.ranges) == 0
    assert result.terms[0]["field"] == "process_name"


def test_auth_events_search_async(cbcsdk_mock):
    """Test _search method of AuthEventsQuery class"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs",
        POST_AUTH_EVENTS_FACET_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/facet_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_2,
    )

    api = cbcsdk_mock.api
    auth_events = (
        api.select(AuthEventsFacet)
        .where(process_pid=1000)
        .add_facet_field("process_name")
    )
    future = auth_events.execute_async()
    result = future.result()
    assert result.terms is not None
    assert len(result.ranges) == 0
    assert result.terms[0]["field"] == "process_name"


def test_auth_events_aggregation_wrong_field(cbcsdk_mock):
    """Testing passing wrong aggregation_field"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError):
        for i in (
            api.select(AuthEvents)
            .where(process_pid=2000)
            .group_results("wrong_field")
        ):
            print(i)
    with pytest.raises(ApiError):
        for i in api.select(AuthEvents).where(process_pid=2000).group_results(1):
            print(i)


def test_auth_events_select_group_results(cbcsdk_mock):
    """Testing AuthEvents Querying with select() and more complex criteria"""
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/search_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/group_results",  # noqa: E501
        GET_AUTH_EVENTS_GROUPED_RESULTS_RESP,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs",
        POST_AUTH_EVENTS_SEARCH_JOB_RESP,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/auth_events/detail_jobs/62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs/results",  # noqa: E501
        GET_AUTH_EVENTS_DETAIL_JOB_RESULTS_RESP,
    )

    api = cbcsdk_mock.api
    event_groups = list(
        api.select(AuthEvents)
        .where(process_pid=2000)
        .group_results(
            "device_name",
            max_events_per_group=10,
            rows=5,
            start=0,
            range_field="backend_timestamp",
            range_duration="-2y"
        )
    )
    # invoke get_details() on the first AuthEvents in the list
    event_groups[0].auth_events[0].get_details()
    assert event_groups[0].group_key is not None
    assert event_groups[0]["group_key"] is not None
    assert event_groups[0].auth_events[0]["process_pid"][0] == 764

def test_auth_events_search_validations(cbcsdk_mock):
    """Tests getting auth_events search validations"""
    api = cbcsdk_mock.api
    q = 'q=auth_username'
    cbcsdk_mock.mock_request(
        "GET",
        f"/api/investigate/v2/orgs/test/auth_events/search_validation?{q}",
        AUTH_EVENTS_SEARCH_VALIDATIONS_RESP,
    )
    result = api.select(AuthEvents).search_validation('auth_username')
    assert result is True

def test_auth_events_search_suggestions(cbcsdk_mock):
    """Tests getting auth_events search suggestions"""
    api = cbcsdk_mock.api
    q = "suggest.q=auth"
    cbcsdk_mock.mock_request(
        "GET",
        f"/api/investigate/v2/orgs/test/auth_events/search_suggestions?{q}",
        AUTH_EVENTS_SEARCH_SUGGESTIONS_RESP,
    )
    result = api.select(AuthEvents).search_suggestions('auth')

    assert len(result) != 0
