# *******************************************************
# Copyright (c) VMware, Inc. 2020-2022. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Tests of the policies support in the Platform API."""

import pytest
import logging
from contextlib import ExitStack as does_not_raise
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.platform import Policy
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_policies import (FULL_POLICY_1, SUMMARY_POLICY_1, SUMMARY_POLICY_2,
                                                        SUMMARY_POLICY_3, OLD_POLICY_1)


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

def test_policy_compatibility_aliases(cb):
    """Test the compatibility aliases that mimic the behavior of the old policy object."""
    policy = Policy(cb, 65536, FULL_POLICY_1, False, True)
    assert policy.priorityLevel == "HIGH"
    assert policy.systemPolicy is False
    assert policy.version == 2
    assert policy.latestRevision == 2
    assert policy.policy == OLD_POLICY_1
    assert policy.rules == FULL_POLICY_1["rules"]
    objs = policy.object_rules
    for raw_rule in FULL_POLICY_1["rules"]:
        assert objs[raw_rule["id"]]._info == raw_rule


def test_policy_autoload(cbcsdk_mock):
    """Tests automatic loading of a "partial" policy."""
    called_full_get = False

    def on_get(uri, query_params, default):
        nonlocal called_full_get
        called_full_get = True
        return FULL_POLICY_1

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536', on_get)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, SUMMARY_POLICY_1, False, False)
    assert policy.name == "A Dummy Policy"
    assert called_full_get is False
    assert policy.priority_level == "HIGH"
    assert called_full_get is False
    assert policy.auto_delete_known_bad_hashes_delay == 86400000
    assert called_full_get is True
    assert policy.rules == FULL_POLICY_1["rules"]


def test_policy_lookup_by_id(cbcsdk_mock):
    """Tests a basic policy lookup by ID."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536', FULL_POLICY_1)
    api = cbcsdk_mock.api
    policy = api.select(Policy, 65536)
    assert policy.name == "A Dummy Policy"
    assert policy.priority_level == "HIGH"
    assert policy.auto_delete_known_bad_hashes_delay == 86400000
    assert policy.rules == FULL_POLICY_1["rules"]


def test_policy_get_summaries(cbcsdk_mock):
    """Tests getting the list of policy summaries."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies',
                             {"policies": [SUMMARY_POLICY_1, SUMMARY_POLICY_2, SUMMARY_POLICY_3]})
    api = cbcsdk_mock.api
    my_list = list(api.select(Policy))
    assert len(my_list) == 3
    assert my_list[0].name == "A Dummy Policy"
    assert my_list[0].priority_level == "HIGH"
    assert my_list[1].name == "Forescout Policy"
    assert my_list[1].priority_level == "MEDIUM"
    assert my_list[2].name == "Remediant AC Policy"
    assert my_list[2].priority_level == "LOW"


def test_policy_get_summaries_async(cbcsdk_mock):
    """Tests an async query of policy summaries."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/summary',
                             {"policies": [SUMMARY_POLICY_1, SUMMARY_POLICY_2, SUMMARY_POLICY_3]})
    api = cbcsdk_mock.api
    future = api.select(Policy).execute_async()
    my_list = future.result()
    assert len(my_list) == 3
    assert my_list[0].name == "A Dummy Policy"
    assert my_list[0].priority_level == "HIGH"
    assert my_list[1].name == "Forescout Policy"
    assert my_list[1].priority_level == "MEDIUM"
    assert my_list[2].name == "Remediant AC Policy"
    assert my_list[2].priority_level == "LOW"


def test_policy_filter_by_id(cbcsdk_mock):
    """Tests filtering the policy summaries by ID."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies',
                             {"policies": [SUMMARY_POLICY_1, SUMMARY_POLICY_2, SUMMARY_POLICY_3]})
    api = cbcsdk_mock.api
    query = api.select(Policy).add_policy_ids([10191, 74656])
    my_list = list(query)
    assert len(my_list) == 2
    assert my_list[0].name == "Forescout Policy"
    assert my_list[0].priority_level == "MEDIUM"
    assert my_list[1].name == "Remediant AC Policy"
    assert my_list[1].priority_level == "LOW"
    query = api.select(Policy).add_policy_ids(10191)
    my_list = list(query)
    assert len(my_list) == 1
    assert my_list[0].name == "Forescout Policy"
    assert my_list[0].priority_level == "MEDIUM"


def test_policy_filter_by_system(cbcsdk_mock):
    """Tests filtering the policy summaries by system status."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/summary',
                             {"policies": [SUMMARY_POLICY_1, SUMMARY_POLICY_2, SUMMARY_POLICY_3]})
    api = cbcsdk_mock.api
    query = api.select(Policy).set_system(True)
    my_list = list(query)
    assert len(my_list) == 1
    assert my_list[0].name == "Remediant AC Policy"
    assert my_list[0].priority_level == "LOW"
    query = api.select(Policy).set_system(False)
    my_list = list(query)
    assert len(my_list) == 2
    assert my_list[0].name == "A Dummy Policy"
    assert my_list[0].priority_level == "HIGH"
    assert my_list[1].name == "Forescout Policy"
    assert my_list[1].priority_level == "MEDIUM"


def test_policy_filter_by_name(cbcsdk_mock):
    """Tests filtering the policy summaries by name."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/summary',
                             {"policies": [SUMMARY_POLICY_1, SUMMARY_POLICY_2, SUMMARY_POLICY_3]})
    api = cbcsdk_mock.api
    query = api.select(Policy).add_names(["Dummy", "Remediant"])
    my_list = list(query)
    assert len(my_list) == 2
    assert my_list[0].name == "A Dummy Policy"
    assert my_list[0].priority_level == "HIGH"
    assert my_list[1].name == "Remediant AC Policy"
    assert my_list[1].priority_level == "LOW"
    query = api.select(Policy).add_names("A")
    my_list = list(query)
    assert len(my_list) == 2
    assert my_list[0].name == "A Dummy Policy"
    assert my_list[0].priority_level == "HIGH"
    assert my_list[1].name == "Remediant AC Policy"
    assert my_list[1].priority_level == "LOW"


def test_policy_filter_by_description(cbcsdk_mock):
    """Tests filtering the policy summaries by description."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/summary',
                             {"policies": [SUMMARY_POLICY_1, SUMMARY_POLICY_2, SUMMARY_POLICY_3]})
    api = cbcsdk_mock.api
    query = api.select(Policy).add_descriptions(["protection", "capabilities"])
    my_list = list(query)
    assert len(my_list) == 2
    assert my_list[0].name == "Forescout Policy"
    assert my_list[0].priority_level == "MEDIUM"
    assert my_list[1].name == "Remediant AC Policy"
    assert my_list[1].priority_level == "LOW"
    query = api.select(Policy).add_descriptions("protection")
    my_list = list(query)
    assert len(my_list) == 1
    assert my_list[0].name == "Forescout Policy"
    assert my_list[0].priority_level == "MEDIUM"


def test_policy_filter_by_priority(cbcsdk_mock):
    """Tests filtering the policy summaries by priority."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/summary',
                             {"policies": [SUMMARY_POLICY_1, SUMMARY_POLICY_2, SUMMARY_POLICY_3]})
    api = cbcsdk_mock.api
    query = api.select(Policy).add_priorities(["HIGH", "LOW"])
    my_list = list(query)
    assert len(my_list) == 2
    assert my_list[0].name == "A Dummy Policy"
    assert my_list[0].priority_level == "HIGH"
    assert my_list[1].name == "Remediant AC Policy"
    assert my_list[1].priority_level == "LOW"
    query = api.select(Policy).add_priorities("MEDIUM")
    my_list = list(query)
    assert len(my_list) == 1
    assert my_list[0].name == "Forescout Policy"
    assert my_list[0].priority_level == "MEDIUM"


def test_bogus_policy_query_arguments(cb):
    """Tests that exceptions get thrown when policy query arguments are bogus."""
    query = cb.select(Policy)
    with pytest.raises(ApiError):
        query.add_policy_ids([33, "Frosting", 667])
    with pytest.raises(ApiError):
        query.add_policy_ids(ApiError)
    with pytest.raises(ApiError):
        query.set_system("FILE_NOT_FOUND")
    with pytest.raises(ApiError):
        query.add_names(["Alpha", 213])
    with pytest.raises(ApiError):
        query.add_names(90710)
    with pytest.raises(ApiError):
        query.add_descriptions([14, "Ninety Two"])
    with pytest.raises(ApiError):
        query.add_descriptions(714)
    with pytest.raises(ApiError):
        query.add_priorities(["MEDIUM", "LOW", "DOGWASH"])
    with pytest.raises(ApiError):
        query.add_priorities(["MEDIUM", "LOW", 42])
    with pytest.raises(ApiError):
        query.add_priorities("APOCALYPTIC")
    with pytest.raises(ApiError):
        query.add_priorities(8675309)
