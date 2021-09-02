#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.


"""Unit test code for recommendations API"""

import pytest
import logging
from cbc_sdk.endpoint_standard import Recommendation
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_recommendation import (SEARCH_REQ, SEARCH_RESP, ACTION_INIT,
                                                                       ACTION_REQS)


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, filename='log.txt')


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


def test_search_with_options(cbcsdk_mock):
    """Test specifying the options for a search, and what we get back."""
    def post_validate(url, body, **kwargs):
        assert SEARCH_REQ == body
        return SEARCH_RESP

    cbcsdk_mock.mock_request("POST", "/recommendation-service/v1/orgs/test/recommendation/_search", post_validate)
    api = cbcsdk_mock.api
    query = api.select(Recommendation).set_policy_types(['reputation_override']) \
        .set_statuses(['NEW', 'REJECTED', 'ACCEPTED']).set_hashes(['111', '222']).sort_by('impact_score', 'DESC')
    output = list(query)
    assert len(output) == 3
    assert output[0].recommendation_id == "91e9158f-23cc-47fd-af7f-8f56e2206523"
    assert output[0].policy_id == 0
    assert output[0].rule_type == "reputation_override"
    impact = output[0].impact_
    assert impact.org_adoption == "LOW"
    assert impact.event_count == 76
    assert impact.impacted_devices == 45
    assert impact.impact_score == 0
    new_rule = output[0].new_rule_
    assert new_rule.override_type == "SHA256"
    assert new_rule.override_list == "WHITE_LIST"
    assert new_rule.filename == "XprotectService"
    application = new_rule.application_
    assert application.type == 'EXE'
    assert application.value == 'FOO'
    workflow = output[0].workflow_
    assert workflow.status == 'NEW'
    assert workflow.changed_by == 'rbaratheon@example.com'
    assert workflow.comment == "Ours is the fury"
    assert output[1].recommendation_id == "bd50c2b2-5403-4e9e-8863-9991f70df026"
    assert output[2].recommendation_id == "0d9da444-cfa7-4488-9fad-e2abab099b68"


def test_search_async(cbcsdk_mock):
    """Test async search capability."""
    cbcsdk_mock.mock_request("POST", "/recommendation-service/v1/orgs/test/recommendation/_search", SEARCH_RESP)
    api = cbcsdk_mock.api
    future = api.select(Recommendation).execute_async()
    output = future.result()
    assert len(output) == 3
    assert output[0].recommendation_id == "91e9158f-23cc-47fd-af7f-8f56e2206523"
    assert output[1].recommendation_id == "bd50c2b2-5403-4e9e-8863-9991f70df026"
    assert output[2].recommendation_id == "0d9da444-cfa7-4488-9fad-e2abab099b68"


def test_search_bogus_parameters(cb):
    """Test error handling on bogus search parameters."""
    query = cb.select(Recommendation)
    with pytest.raises(ApiError):
        query.set_policy_types(['thepolicy'])
    with pytest.raises(ApiError):
        query.set_statuses(['UNKNOWN'])
    with pytest.raises(ApiError):
        query.set_hashes([42])
    with pytest.raises(ApiError):
        query.sort_by('impact_score', 'QUOI')


def test_actions(cbcsdk_mock):
    """Tests the three "action" methods."""
    count = 0

    def put_validate(url, body, **kwargs):
        nonlocal count
        assert body == ACTION_REQS[count]
        count += 1
        return None

    cbcsdk_mock.mock_request("PUT", "/recommendation-service/v1/orgs/test/recommendation/"
                                    "0d9da444-cfa7-4488-9fad-e2abab099b68/workflow", put_validate)
    api = cbcsdk_mock.api
    recommendation = Recommendation(api, ACTION_INIT['recommendation_id'], ACTION_INIT)
    recommendation.accept('Alpha')
    recommendation.reset()
    recommendation.reject('Charlie')
    assert count == 3
