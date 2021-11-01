import pytest

from cbc_sdk import CBCloudAPI
from cbc_sdk.errors import ModelNotFound
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_events import EVENT_GET_HOSTNAME_RESP
from tests.unit.fixtures.platform.mock_events import EVENT_SEARCH_VALIDATION_RESP
from tests.unit.fixtures.platform.mock_grants import QUERY_GRANT_RESP
from tests.unit.fixtures.platform.mock_process import (
    GET_PROCESS_VALIDATION_RESP,
    POST_PROCESS_SEARCH_JOB_RESP,
    GET_PROCESS_SEARCH_JOB_RESP,
    GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
    GET_PROCESS_SUMMARY_RESP,
    GET_PROCESS_SUMMARY_STR,
    GET_FACET_SEARCH_RESULTS_RESP,
    GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1,
    POST_TREE_SEARCH_JOB_RESP,
    GET_TREE_SEARCH_JOB_RESP,
    GET_PROCESS_TREE_STR,
)
from tests.unit.fixtures.platform.mock_reputation_override import (
    REPUTATION_OVERRIDE_SHA256_SEARCH_RESPONSE,
)
from tests.unit.fixtures.platform.mock_users import GET_USERS_RESP
from tests.unit.fixtures.platform.mock_vulnerabilities import (
    GET_VULNERABILITY_SUMMARY_ORG_LEVEL_PER_SEVERITY,
    GET_VULNERABILITY_RESP,
)
from tests.unit.fixtures.stubresponse import patch_cbc_sdk_api, StubResponse


@pytest.fixture(scope="function")
def call_cbcloud_api():
    """Call the CBCloudAPI object

    IMPORTANT: Since there are a lot of functions that are doing the same function as this one,
    notice the `org_key` which is currently `Z100` whenever you are testing classes like `Process`
    you are likely to copy the mock requests from there but since it is not instantly apparent notice
    that there the `org_key` is `test` and they won't work without you modifying the mock URLs.
    """
    return CBCloudAPI(
        url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True
    )


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, call_cbcloud_api):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, call_cbcloud_api)


def test_raise_ModelNotFound(cbcsdk_mock):
    """Test ModelNotFound exception when a class isn't found."""
    with pytest.raises(ModelNotFound):
        cbcsdk_mock.api.select("TESTCLASSTEST")


class TestReferenceAlerts:
    """Testing all types of `Alerts`"""

    def test_BaseAlert_select(self, monkeypatch, cbcsdk_mock):
        """Test the dynamic reference for the `BaseAlert` class."""
        stub = StubResponse({"num_found": 1, "results": [{"id": "1"}]})
        patch_cbc_sdk_api(
            monkeypatch, cbcsdk_mock.api, POST=lambda *args, **kwargs: stub
        )
        query = cbcsdk_mock.api.select("BaseAlert").one()
        assert type(query).__qualname__ == "BaseAlert"

    def test_CBAnalyticsAlert_select(self, monkeypatch, cbcsdk_mock):
        """Test the dynamic reference for the `CBAnalyticsAlert` class."""
        stub = StubResponse({"num_found": 1, "results": [{"id": "1"}]})
        patch_cbc_sdk_api(
            monkeypatch, cbcsdk_mock.api, POST=lambda *args, **kwargs: stub
        )
        query = cbcsdk_mock.api.select("CBAnalyticsAlert").where("Blort")
        a = query.one()
        assert type(a).__qualname__ == "CBAnalyticsAlert"

    def test_DeviceControlAlert_select(self, monkeypatch, cbcsdk_mock):
        """Test the dynamic reference for the `DeviceControlAlert` class."""
        stub = StubResponse({"num_found": 1, "results": [{"id": "1"}]})
        patch_cbc_sdk_api(
            monkeypatch, cbcsdk_mock.api, POST=lambda *args, **kwargs: stub
        )
        query = cbcsdk_mock.api.select("DeviceControlAlert").where("Blort").one()
        assert type(query).__qualname__ == "DeviceControlAlert"

    def test_WatchlistAlert_select(self, monkeypatch, cbcsdk_mock):
        """Test the dynamic reference for the `WatchlistAlert` class."""
        stub = StubResponse({"num_found": 1, "results": [{"id": "1"}]})
        patch_cbc_sdk_api(
            monkeypatch, cbcsdk_mock.api, POST=lambda *args, **kwargs: stub
        )
        query = cbcsdk_mock.api.select("WatchlistAlert").one()
        assert type(query).__qualname__ == "WatchlistAlert"


def test_Device_select(monkeypatch, cbcsdk_mock):
    """Test the dynamic reference for the `Device` class."""
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/Z100/devices/6023", {"device_id": 6023}
    )
    rc = cbcsdk_mock.api.select("Device", 6023)
    assert type(rc).__qualname__ == "Device"


def test_Grant_select(cbcsdk_mock):
    """Test the dynamic reference for the `Grant` class."""
    cbcsdk_mock.mock_request("POST", "/access/v2/grants/_fetch", QUERY_GRANT_RESP)
    api = cbcsdk_mock.api
    query = (
        api.select("Grant")
        .add_principal("psc:user:12345678:ABCDEFGH", "psc:org:test")
        .first()
    )
    assert type(query).__qualname__ == "Grant"


def test_Event_select(cbcsdk_mock):
    """Test the dynamic reference for the `Event` class."""
    cbcsdk_mock.mock_request(
        "GET", "/integrationServices/v3/event", EVENT_GET_HOSTNAME_RESP
    )
    search_validate_url = "/api/investigate/v1/orgs/Z100/events/search_validation"
    cbcsdk_mock.mock_request("GET", search_validate_url, EVENT_SEARCH_VALIDATION_RESP)
    events = cbcsdk_mock.api.select("Event").where("hostNameExact:Win7x64")
    results = [event for event in events._perform_query()]
    event = results[0]
    assert type(event).__qualname__ == "Event"


class TestReferenceProcess:
    """Testing all types of `Process` classes"""

    def test_Process_select(self, cbcsdk_mock):
        """Test the dynamic reference for the `Process` class."""
        # mock the search validation
        cbcsdk_mock.mock_request(
            "GET",
            "/api/investigate/v1/orgs/Z100/processes/search_validation",
            GET_PROCESS_VALIDATION_RESP,
        )
        # mock the POST of a search
        cbcsdk_mock.mock_request(
            "POST",
            "/api/investigate/v2/orgs/Z100/processes/search_job",
            POST_PROCESS_SEARCH_JOB_RESP,
        )
        # mock the GET to check search status
        cbcsdk_mock.mock_request(
            "GET",
            (
                "/api/investigate/v1/orgs/Z100/processes/"
                "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"
            ),
            GET_PROCESS_SEARCH_JOB_RESP,
        )
        # mock the GET to get search results
        cbcsdk_mock.mock_request(
            "GET",
            (
                "/api/investigate/v2/orgs/Z100/processes/search_jobs/"
                "2c292717-80ed-4f0d-845f-779e09470920/results"
            ),
            GET_PROCESS_SEARCH_JOB_RESULTS_RESP,
        )
        # mock the POST of a summary search (using same Job ID)
        cbcsdk_mock.mock_request(
            "POST",
            "/api/investigate/v2/orgs/Z100/processes/summary_jobs",
            POST_PROCESS_SEARCH_JOB_RESP,
        )
        # mock the GET to check summary search status
        cbcsdk_mock.mock_request(
            "GET",
            (
                "/api/investigate/v2/orgs/Z100/processes/"
                "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920"
            ),
            GET_PROCESS_SUMMARY_RESP,
        )
        # mock the GET to get summary search results
        cbcsdk_mock.mock_request(
            "GET",
            (
                "/api/investigate/v2/orgs/Z100/processes/"
                "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"
            ),
            GET_PROCESS_SUMMARY_STR,
        )
        guid = "WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00"
        process = cbcsdk_mock.api.select("Process", guid)
        assert type(process).__qualname__ == "Process"

    def test_Process_Summary_select(self, cbcsdk_mock):
        """Test the dynamic reference for the `Process.Summary` class."""
        # mock the POST of a summary search (using same Job ID)
        cbcsdk_mock.mock_request(
            "POST",
            "/api/investigate/v2/orgs/Z100/processes/summary_jobs",
            POST_PROCESS_SEARCH_JOB_RESP,
        )
        # mock the GET to check summary search status
        cbcsdk_mock.mock_request(
            "GET",
            (
                "/api/investigate/v2/orgs/Z100/processes/"
                "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920"
            ),
            GET_PROCESS_SUMMARY_RESP,
        )
        # mock the GET to get summary search results
        cbcsdk_mock.mock_request(
            "GET",
            (
                "/api/investigate/v2/orgs/Z100/processes/"
                "summary_jobs/2c292717-80ed-4f0d-845f-779e09470920/results"
            ),
            GET_PROCESS_SUMMARY_RESP,
        )
        guid = "WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00"
        summary = cbcsdk_mock.api.select("Process.Summary").where(f"process_guid:{guid}")
        assert summary._perform_query() is not None
        assert type(summary).__name__ == "SummaryQuery"

    def test_Process_Tree_select(self, cbcsdk_mock):
        """Test the dynamic reference for the `Process.Tree` class."""
        # mock the search validation
        cbcsdk_mock.mock_request(
            "GET",
            "/api/investigate/v1/orgs/Z100/processes/search_validation",
            GET_PROCESS_VALIDATION_RESP,
        )
        # mock the POST of a search
        cbcsdk_mock.mock_request(
            "POST",
            "/api/investigate/v2/orgs/Z100/processes/search_jobs",
            POST_PROCESS_SEARCH_JOB_RESP,
        )
        # mock the GET to check search status
        cbcsdk_mock.mock_request(
            "GET",
            (
                "/api/investigate/v1/orgs/Z100/processes/"
                "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"
            ),
            GET_PROCESS_SEARCH_JOB_RESP,
        )
        # mock the GET to get search results
        cbcsdk_mock.mock_request(
            "GET",
            (
                "/api/investigate/v2/orgs/Z100/processes/search_jobs/"
                "2c292717-80ed-4f0d-845f-779e09470920/results"
            ),
            GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1,
        )
        # mock the Tree search
        cbcsdk_mock.mock_request(
            "POST",
            "/api/investigate/v2/orgs/Z100/processes/summary_jobs",
            POST_TREE_SEARCH_JOB_RESP,
        )
        # mock the GET to check search status
        cbcsdk_mock.mock_request(
            "GET",
            (
                "/api/investigate/v2/orgs/Z100/processes/summary_jobs"
                "/ee158f11-4dfb-4ae2-8f1a-7707b712226d"
            ),
            GET_TREE_SEARCH_JOB_RESP,
        )
        # mock the GET to get search results
        cbcsdk_mock.mock_request(
            "GET",
            (
                "/api/investigate/v2/orgs/Z100/processes/summary_jobs/"
                "ee158f11-4dfb-4ae2-8f1a-7707b712226d/results"
            ),
            GET_PROCESS_TREE_STR,
        )
        proc_tree = cbcsdk_mock.api.select("Process.Tree").where(
            process_guid="WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00"
        )
        future = proc_tree.execute_async()
        results = future.result()[0]
        assert type(results).__qualname__ == "Process.Tree"

    def test_ProcessFacet_select(self, cbcsdk_mock):
        """Test the dynamic reference for the `ProcessFacet` class."""
        # mock the search request
        cbcsdk_mock.mock_request(
            "POST",
            "/api/investigate/v2/orgs/Z100/processes/facet_jobs",
            {"job_id": "the-job-id"},
        )
        # mock the result call
        cbcsdk_mock.mock_request(
            "GET",
            "/api/investigate/v2/orgs/Z100/processes/facet_jobs/the-job-id/results",
            GET_FACET_SEARCH_RESULTS_RESP,
        )
        facet_query = cbcsdk_mock.api.select("ProcessFacet").where("process_name:svchost.exe")
        facet_query.add_facet_field("test")
        future = facet_query.execute_async()
        res = future.result()
        assert type(res).__name__ == "ProcessFacet"


def test_ReputationOverride_select(cbcsdk_mock):
    """Test the dynamic reference for the `ReputationOverride` class."""
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/Z100/reputations/overrides/_search",
        REPUTATION_OVERRIDE_SHA256_SEARCH_RESPONSE,
    )
    reputation_override = (
        cbcsdk_mock.api.select("ReputationOverride").where("foo").one()
    )
    assert type(reputation_override).__qualname__ == "ReputationOverride"


def test_User_select(cbcsdk_mock):
    """Test the dynamic reference for the `User` class."""
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/Z100/users", GET_USERS_RESP)
    api = cbcsdk_mock.api
    user = api.select("User", 3978)
    assert type(user).__name__ == "User"


class TestReferenceVulnerability:
    """Testing all types of `Vulnerability` classes"""

    def test_Vulnerability_select(self, cbcsdk_mock):
        """Test the dynamic reference for the `Vulnerability` class."""
        cbcsdk_mock.mock_request(
            "POST",
            "/vulnerability/assessment/api/v1/orgs/Z100/devices/vulnerabilities/_search",
            GET_VULNERABILITY_RESP,
        )
        vulnerability = cbcsdk_mock.api.select("Vulnerability", "CVE-2014-4650")
        assert type(vulnerability).__qualname__ == "Vulnerability"

    def test_VulnerabilityOrgSummary_select(self, cbcsdk_mock):
        """Test the dynamic reference for the `Vulnerability.OrgSummary` class."""
        cbcsdk_mock.mock_request(
            "GET",
            "/vulnerability/assessment/api/v1/orgs/Z100/vulnerabilities/summary",
            GET_VULNERABILITY_SUMMARY_ORG_LEVEL_PER_SEVERITY,
        )
        summary = (
            cbcsdk_mock.api.select("Vulnerability.OrgSummary")
            .set_severity("CRITICAL")
            .submit()
        )
        assert type(summary).__qualname__ == "Vulnerability.OrgSummary"
