# *******************************************************
# Copyright (c) VMware, Inc. 2021-2022. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Testing ReputationOverride objects of cbc_sdk.platform"""

import pytest
import logging
from cbc_sdk.platform import ReputationOverride, Process
from cbc_sdk.endpoint_standard import EnrichedEvent
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_reputation_override import (REPUTATION_OVERRIDE_SHA256_REQUEST,
                                                                   REPUTATION_OVERRIDE_SHA256_RESPONSE,
                                                                   REPUTATION_OVERRIDE_SHA256_SEARCH_RESPONSE)

from tests.unit.fixtures.platform.mock_process import (GET_PROCESS_VALIDATION_RESP,
                                                       POST_PROCESS_SEARCH_JOB_RESP,
                                                       GET_PROCESS_SEARCH_JOB_RESP,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP)

from tests.unit.fixtures.endpoint_standard.mock_enriched_events import (POST_ENRICHED_EVENTS_SEARCH_JOB_RESP,
                                                                        GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP,
                                                                        GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_1)

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

def test_reputation_override_create(cbcsdk_mock):
    """Testing Reputation Override with .create(api, {})"""
    def _test_request(url, body, **kwargs):
        assert body == REPUTATION_OVERRIDE_SHA256_REQUEST
        return REPUTATION_OVERRIDE_SHA256_RESPONSE

    cbcsdk_mock.mock_request("POST",
                             "/appservices/v6/orgs/test/reputations/overrides",
                             _test_request)
    api = cbcsdk_mock.api

    reputation_override = ReputationOverride.create(api, REPUTATION_OVERRIDE_SHA256_REQUEST)

    assert isinstance(reputation_override, ReputationOverride)
    assert reputation_override.sha256_hash == "af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a"


def test_reputation_override_select(cbcsdk_mock):
    """Testing Reputation Override with .select(ReputationOverride)"""
    def _test_request(url, body, **kwargs):
        assert body == {
            "criteria": {
                "override_list": "BLACK_LIST",
                "override_type": "SHA256"
            },
            "query": "foo",
            "sort_field": "create_time",
            "sort_order": "asc"
        }
        return REPUTATION_OVERRIDE_SHA256_SEARCH_RESPONSE

    cbcsdk_mock.mock_request("POST",
                             "/appservices/v6/orgs/test/reputations/overrides/_search",
                             _test_request)
    api = cbcsdk_mock.api

    reputation_override_query = api.select(ReputationOverride) \
                                   .where("foo") \
                                   .set_override_list("BLACK_LIST") \
                                   .set_override_type("SHA256") \
                                   .sort_by("create_time", "asc")

    assert len(reputation_override_query) == 1
    reputation_override = list(reputation_override_query)[0]
    assert isinstance(reputation_override, ReputationOverride)
    assert reputation_override.sha256_hash == "af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a"


def test_reputation_override_select_async(cbcsdk_mock):
    """Testing Reputation Override with .select(ReputationOverride) async"""
    def _test_request(url, body, **kwargs):
        assert body == {
            "criteria": {
                "override_list": "BLACK_LIST",
                "override_type": "SHA256"
            },
            "query": "foo",
            "sort_field": "create_time",
            "sort_order": "asc"
        }
        return REPUTATION_OVERRIDE_SHA256_SEARCH_RESPONSE

    cbcsdk_mock.mock_request("POST",
                             "/appservices/v6/orgs/test/reputations/overrides/_search",
                             _test_request)
    api = cbcsdk_mock.api

    future = api.select(ReputationOverride) \
                .where("foo") \
                .set_override_list("BLACK_LIST") \
                .set_override_type("SHA256") \
                .sort_by("create_time", "asc") \
                .execute_async()

    results = future.result()
    assert len(results) == 1
    assert isinstance(results[0], ReputationOverride)
    assert results[0].sha256_hash == "af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a"


def test_reputation_override_select_by_id(cbcsdk_mock):
    """Testing Reputation Override with .select(ReputationOverride, "id")"""
    cbcsdk_mock.mock_request("GET",
                             "/appservices/v6/orgs/test/reputations/overrides/e9410b754ea011ebbfd0db2585a41b07",
                             REPUTATION_OVERRIDE_SHA256_RESPONSE)
    api = cbcsdk_mock.api

    reputation_override = api.select(ReputationOverride, "e9410b754ea011ebbfd0db2585a41b07")
    reputation_override.refresh()

    assert isinstance(reputation_override, ReputationOverride)
    assert reputation_override.sha256_hash == "af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a"


def test_reputation_override_delete(cbcsdk_mock):
    """Testing Reputation Override with .delete()"""
    cbcsdk_mock.mock_request("GET",
                             "/appservices/v6/orgs/test/reputations/overrides/e9410b754ea011ebbfd0db2585a41b07",
                             REPUTATION_OVERRIDE_SHA256_RESPONSE)

    cbcsdk_mock.mock_request("DELETE",
                             "/appservices/v6/orgs/test/reputations/overrides/e9410b754ea011ebbfd0db2585a41b07",
                             None)
    api = cbcsdk_mock.api

    reputation_override = api.select(ReputationOverride, "e9410b754ea011ebbfd0db2585a41b07")
    reputation_override.delete()
    assert reputation_override._is_deleted


def test_reputation_override_bulk_delete(cbcsdk_mock):
    """Testing Reputation Override with .bulk_delete()"""
    def _test_request(url, body, **kwargs):
        assert body == ["ID_1", "ID_2"]
        return {
            "results": body,
            "errors": []
        }

    cbcsdk_mock.mock_request("POST",
                             "/appservices/v6/orgs/test/reputations/overrides/_delete",
                             _test_request)

    api = cbcsdk_mock.api
    response = ReputationOverride.bulk_delete(api, ["ID_1", "ID_2"])
    response["results"] == ["ID_1", "ID_2"]


def test_reputation_override_process_ban_process_sha256(cbcsdk_mock):
    """Testing Reputation Override creation from process"""
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_job",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP)

    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)

    def _test_request(url, body, **kwargs):
        resp = body
        resp.update({
            "id": "e9410b754ea011ebbfd0db2585a41b07",
            "created_by": "example@example.com",
            "create_time": "2021-01-04T15:24:18.002Z"
        })
        return resp

    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/reputations/overrides",
                             _test_request)

    reputation_override = process.ban_process_sha256("Test ban application")
    assert isinstance(reputation_override, ReputationOverride)
    assert reputation_override.override_list == "BLACK_LIST"
    assert reputation_override.override_type == "SHA256"
    assert reputation_override.sha256_hash == "5920199e4fbfa47c1717b863814722148a353e54f8c10912cf1f991a1c86309d"
    assert reputation_override.filename == "vmtoolsd.exe"


def test_reputation_override_process_approve_process_sha256(cbcsdk_mock):
    """Testing Reputation Override creation from process"""
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_job",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP)

    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    process = api.select(Process, guid)

    def _test_request(url, body, **kwargs):
        resp = body
        resp.update({
            "id": "e9410b754ea011ebbfd0db2585a41b07",
            "created_by": "example@example.com",
            "create_time": "2021-01-04T15:24:18.002Z"
        })
        return resp

    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/reputations/overrides",
                             _test_request)

    reputation_override = process.approve_process_sha256("Test approve application")
    assert isinstance(reputation_override, ReputationOverride)
    assert reputation_override.override_list == "WHITE_LIST"
    assert reputation_override.override_type == "SHA256"
    assert reputation_override.sha256_hash == "5920199e4fbfa47c1717b863814722148a353e54f8c10912cf1f991a1c86309d"
    assert reputation_override.filename == "vmtoolsd.exe"


def test_reputation_override_enriched_event_ban_process_sha256(cbcsdk_mock):
    """Testing Reputation Override creation from enriched event"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_1)

    api = cbcsdk_mock.api

    event = api.select(EnrichedEvent, "27a278d5150911eb86f1011a55e73b72")

    def _test_request(url, body, **kwargs):
        resp = body
        resp.update({
            "id": "e9410b754ea011ebbfd0db2585a41b07",
            "created_by": "example@example.com",
            "create_time": "2021-01-04T15:24:18.002Z"
        })
        return resp

    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/reputations/overrides",
                             _test_request)

    reputation_override = event.ban_process_sha256("Test ban application")
    assert isinstance(reputation_override, ReputationOverride)
    assert reputation_override.override_list == "BLACK_LIST"
    assert reputation_override.override_type == "SHA256"
    assert reputation_override.sha256_hash == "6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786"
    assert reputation_override.filename == "scrcons.exe"


def test_reputation_override_enriched_event_approve_process_sha256(cbcsdk_mock):
    """Testing Reputation Override creation from enriched event"""
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/enriched_events/search_job",
                             POST_ENRICHED_EVENTS_SEARCH_JOB_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/search_jobs/08ffa932-b633-4107-ba56-8741e929e48b/results",  # noqa: E501
                             GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_1)

    api = cbcsdk_mock.api
    event = api.select(EnrichedEvent, "27a278d5150911eb86f1011a55e73b72")

    def _test_request(url, body, **kwargs):
        resp = body
        resp.update({
            "id": "e9410b754ea011ebbfd0db2585a41b07",
            "created_by": "example@example.com",
            "create_time": "2021-01-04T15:24:18.002Z"
        })
        return resp

    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/reputations/overrides",
                             _test_request)

    reputation_override = event.approve_process_sha256("Test approve application")
    assert isinstance(reputation_override, ReputationOverride)
    assert reputation_override.override_list == "WHITE_LIST"
    assert reputation_override.override_type == "SHA256"
    assert reputation_override.sha256_hash == "6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786"
    assert reputation_override.filename == "scrcons.exe"
