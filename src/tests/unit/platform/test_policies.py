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
import copy

import pytest
import logging
import random
from contextlib import ExitStack as does_not_raise
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.platform import Policy, PolicyRule
from cbc_sdk.errors import ApiError, InvalidObjectError, ServerError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_policies import (FULL_POLICY_1, SUMMARY_POLICY_1, SUMMARY_POLICY_2,
                                                        SUMMARY_POLICY_3, OLD_POLICY_1, RULE_ADD_1, RULE_ADD_2)


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


@pytest.mark.parametrize("initial_data, handler, message", [
    ({"required": True, "action": "DENY", "application": {"type": "REPUTATION", "value": "PUP"},
      "operation": "MEMORY_SCRAPE"}, does_not_raise(), None),
    ({"action": "DENY", "application": {"type": "REPUTATION", "value": "PUP"},
      "operation": "MEMORY_SCRAPE"}, pytest.raises(InvalidObjectError), "Missing fields: [required]"),
    ({"required": True, "application": {"type": "REPUTATION", "value": "PUP"},
      "operation": "MEMORY_SCRAPE"}, pytest.raises(InvalidObjectError), "Missing fields: [action]"),
    ({"required": True, "action": "DENY", "operation": "MEMORY_SCRAPE"},
     pytest.raises(InvalidObjectError), "Missing fields: [application]"),
    ({"required": True, "action": "DENY", "application": {"type": "REPUTATION", "value": "PUP"}},
     pytest.raises(InvalidObjectError), "Missing fields: [operation]"),
    ({"required": ApiError, "action": "DENY", "application": {"type": "REPUTATION", "value": "PUP"},
      "operation": "MEMORY_SCRAPE"}, pytest.raises(InvalidObjectError), "'required' field not valid type"),
    ({"required": True, "action": "PUNT", "application": {"type": "REPUTATION", "value": "PUP"},
      "operation": "MEMORY_SCRAPE"}, pytest.raises(InvalidObjectError), "'action' field value not valid"),
    ({"required": True, "action": "DENY", "application": "NOT VALID",
      "operation": "MEMORY_SCRAPE"}, pytest.raises(InvalidObjectError), "'application' field not valid type/structure"),
    ({"required": True, "action": "DENY", "application": {"value": "PUP"},
      "operation": "MEMORY_SCRAPE"}, pytest.raises(InvalidObjectError), "'application' field not valid type/structure"),
    ({"required": True, "action": "DENY", "application": {"type": "REPUTATION"},
      "operation": "MEMORY_SCRAPE"}, pytest.raises(InvalidObjectError), "'application' field not valid type/structure"),
    ({"required": True, "action": "DENY", "application": {"type": "REPUTATION", "value": "PUP", "extra": "ignore"},
      "operation": "MEMORY_SCRAPE"}, pytest.raises(InvalidObjectError), "'application' field not valid type/structure"),
    ({"required": True, "action": "DENY", "application": {"type": "WHATEVER", "value": "WHATEVER"},
      "operation": "MEMORY_SCRAPE"}, pytest.raises(InvalidObjectError), "'application' 'type' value not valid"),
    ({"required": True, "action": "DENY", "application": {"type": "REPUTATION", "value": 3.1416},
      "operation": "MEMORY_SCRAPE"}, pytest.raises(InvalidObjectError), "'application' 'value' not valid type"),
    ({"required": True, "action": "DENY", "application": {"type": "REPUTATION", "value": "NIHILIST"},
      "operation": "MEMORY_SCRAPE"}, pytest.raises(InvalidObjectError),
     "'application' 'value' not valid value for type REPUTATION"),
    ({"required": True, "action": "DENY", "application": {"type": "REPUTATION", "value": "PUP"},
      "operation": "RANDOM_VALUE"}, pytest.raises(InvalidObjectError), "'operation' field value not valid")
])
def test_rule_validate(cb, initial_data, handler, message):
    """Tests rule validation."""
    rule = PolicyRule(cb, None, None, initial_data, False, True)
    with handler as h:
        rule.validate()
    if message is not None:
        assert h.value.args[0] == message


def test_rule_refresh(cbcsdk_mock):
    """Tests the rule refresh() mechanism."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536', FULL_POLICY_1)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, FULL_POLICY_1, False, True)
    rule = random.choice(list(policy.object_rules.values()))
    old_id = rule.id
    old_action = rule.action
    old_operation = rule.operation
    rule.refresh()
    assert rule.id == old_id
    assert rule.action == old_action
    assert rule.operation == old_operation


@pytest.mark.parametrize("rule_data, give_error, handler", [
    (RULE_ADD_1, False, does_not_raise()),
    (RULE_ADD_2, False, does_not_raise()),
    (RULE_ADD_1, True, pytest.raises(ServerError))
])
def test_rule_add_by_object(cbcsdk_mock, rule_data, give_error, handler):
    """Tests using a PolicyRule object to add a rule."""
    def on_post(uri, body, **kwargs):
        assert body == RULE_ADD_1
        if give_error:
            return CBCSDKMock.StubResponse("Failure", scode=404)
        rc = copy.deepcopy(body)
        rc['id'] = 16
        return rc

    cbcsdk_mock.mock_request('POST', '/policyservice/v1/orgs/test/policies/65536/rules', on_post)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_count = len(policy.object_rules)
    new_rule = PolicyRule(api, policy, None, rule_data, False, True)
    with handler:
        new_rule.save()
        assert new_rule.id == 16
        assert len(policy.object_rules) == rule_count + 1
        assert policy.object_rules[new_rule.id] is new_rule
        assert len(policy.rules) == rule_count + 1
        assert 16 in [rd['id'] for rd in policy.rules]


def test_rule_modify_by_object(cbcsdk_mock):
    """Tests modifying a PolicyRule object within a policy."""
    def on_put(url, body, **kwargs):
        assert body == {"id": 2, "required": True, "action": "TERMINATE",
                        "application": {"type": "NAME_PATH", "value": "data"}, "operation": "MEMORY_SCRAPE"}
        return copy.deepcopy(body)

    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536/rules/2', on_put)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_count = len(policy.object_rules)
    rule = policy.object_rules[2]
    rule.action = "TERMINATE"
    rule.save()
    assert len(policy.object_rules) == rule_count
    assert len(policy.rules) == rule_count
    raw_pointer = [rd for rd in policy.rules if rd['id'] == 2][0]
    assert raw_pointer['action'] == "TERMINATE"


def test_rule_delete_by_object(cbcsdk_mock):
    """Tests deleting a PolicyRule object from a policy."""
    cbcsdk_mock.mock_request('DELETE', '/policyservice/v1/orgs/test/policies/65536/rules/1',
                             CBCSDKMock.StubResponse(None, scode=204))
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_count = len(policy.object_rules)
    rule = policy.object_rules[1]
    assert not rule.is_deleted
    rule.delete()
    assert len(policy.object_rules) == rule_count - 1
    assert rule not in list(policy.object_rules.values())
    assert len(policy.rules) == rule_count - 1
    assert 1 not in [rd['id'] for rd in policy.rules]
    assert rule.is_deleted


def test_rule_delete_is_new(cb):
    """Tests deleting a new PolicyRule raises an error."""
    policy = Policy(cb, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    new_rule = PolicyRule(cb, policy, None, RULE_ADD_1, False, True)
    with pytest.raises(ApiError):
        new_rule.delete()
