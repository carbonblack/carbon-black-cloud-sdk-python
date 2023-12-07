# *******************************************************
# Copyright (c) VMware, Inc. 2020-2023. All Rights Reserved.
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
from cbc_sdk.platform import Policy, PolicyRule, PolicyRuleConfig, PolicyRankChangePreview
from cbc_sdk.platform.devices import DeviceSearchQuery
from cbc_sdk.errors import ApiError, InvalidObjectError, ServerError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_policies import (FULL_POLICY_1, SUMMARY_POLICY_1, SUMMARY_POLICY_2,
                                                        SUMMARY_POLICY_3, OLD_POLICY_1, FULL_POLICY_2, OLD_POLICY_2,
                                                        RULE_ADD_1, RULE_ADD_2, RULE_MODIFY_1, NEW_POLICY_CONSTRUCT_1,
                                                        NEW_POLICY_RETURN_1, BASIC_CONFIG_TEMPLATE_RETURN,
                                                        BUILD_RULECONFIG_1, PREVIEW_POLICY_CHANGES_REQUEST1,
                                                        PREVIEW_POLICY_CHANGES_RESPONSE1,
                                                        PREVIEW_POLICY_CHANGES_REQUEST2,
                                                        PREVIEW_POLICY_CHANGES_RESPONSE2, FULL_POLICY_5)


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

def test_policy_compatibility_aliases_read(cb):
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
    rule_configs = policy.object_rule_configs
    assert rule_configs["1f8a5e4b-34f2-4d31-9f8f-87c56facaec8"].name == "Advanced Scripting Prevention"
    assert rule_configs["ac67fa14-f6be-4df9-93f2-6de0dbd96061"].name == "Credential Theft"
    assert rule_configs["c4ed61b3-d5aa-41a9-814f-0f277451532b"].name == "Carbon Black Threat Intel"
    assert rule_configs["88b19232-7ebb-48ef-a198-2a75a282de5d"].name == "Privilege Escalation"


def test_policy_compatibility_aliases_write(cb):
    """Test the compatibility aliases that mimic the behavior of the old policy object."""
    policy = cb.create(Policy)
    policy.policy = copy.deepcopy(OLD_POLICY_2)
    policy.description = "Hoopy Frood"
    policy.name = "default - S1"
    policy.position = 2
    policy.priorityLevel = "MEDIUM"
    policy.version = 2
    new_policy_data = copy.deepcopy(policy._info)
    assert new_policy_data == FULL_POLICY_2


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
    rule_configs = policy.object_rule_configs
    assert rule_configs["1f8a5e4b-34f2-4d31-9f8f-87c56facaec8"].name == "Advanced Scripting Prevention"


def test_policy_lookup_by_id(cbcsdk_mock):
    """Tests a basic policy lookup by ID."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536', FULL_POLICY_1)
    api = cbcsdk_mock.api
    policy = api.select(Policy, 65536)
    assert policy.name == "A Dummy Policy"
    assert policy.priority_level == "HIGH"
    assert policy.auto_delete_known_bad_hashes_delay == 86400000
    assert policy.rules == FULL_POLICY_1["rules"]
    rule_configs = policy.object_rule_configs
    assert rule_configs["1f8a5e4b-34f2-4d31-9f8f-87c56facaec8"].name == "Advanced Scripting Prevention"


def test_policy_get_summaries(cbcsdk_mock):
    """Tests getting the list of policy summaries."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/summary',
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
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/summary',
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


def test_rule_add_by_compatibility_method(cbcsdk_mock):
    """Tests using the compatibility method to add a rule."""
    def on_post(uri, body, **kwargs):
        assert body == RULE_ADD_1
        rc = copy.deepcopy(body)
        rc['id'] = 16
        return rc

    cbcsdk_mock.mock_request('POST', '/policyservice/v1/orgs/test/policies/65536/rules', on_post)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_count = len(policy.object_rules)
    policy.add_rule(copy.deepcopy(RULE_ADD_1))
    assert len(policy.object_rules) == rule_count + 1
    assert len(policy.rules) == rule_count + 1
    assert 16 in [rd['id'] for rd in policy.rules]


def test_rule_modify_by_object(cbcsdk_mock):
    """Tests modifying a PolicyRule object within a policy."""
    def on_put(url, body, **kwargs):
        assert body == RULE_MODIFY_1
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


def test_rule_modify_by_compatibility_method(cbcsdk_mock):
    """Tests modifying a PolicyRule object using the replace_rule method."""
    def on_put(url, body, **kwargs):
        assert body == RULE_MODIFY_1
        return copy.deepcopy(body)

    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536/rules/2', on_put)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_count = len(policy.object_rules)
    policy.replace_rule(2, RULE_MODIFY_1)
    assert len(policy.object_rules) == rule_count
    assert len(policy.rules) == rule_count
    rule = policy.object_rules[2]
    assert rule.action == "TERMINATE"
    raw_pointer = [rd for rd in policy.rules if rd['id'] == 2][0]
    assert raw_pointer['action'] == "TERMINATE"


def test_rule_modify_by_compatibility_method_with_server_error(cbcsdk_mock):
    """Tests modifying a PolicyRule object using the replace_rule method, but it returns a server error."""
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536/rules/2',
                             CBCSDKMock.StubResponse(None, scode=500))
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_count = len(policy.object_rules)
    with pytest.raises(ServerError):
        policy.replace_rule(2, RULE_MODIFY_1)
    assert len(policy.object_rules) == rule_count
    assert len(policy.rules) == rule_count
    rule = policy.object_rules[2]
    assert rule.action == "DENY"
    raw_pointer = [rd for rd in policy.rules if rd['id'] == 2][0]
    assert raw_pointer['action'] == "DENY"


def test_rule_modify_by_compatibility_method_invalid_index(cb):
    """Tests modifying a PolicyRule object using the replace_rule method, but it uses an invalid index."""
    policy = Policy(cb, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    with pytest.raises(ApiError):
        policy.replace_rule(6, RULE_MODIFY_1)


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


def test_rule_delete_by_compatibility_method(cbcsdk_mock):
    """Tests deleting a rule from a policy via the compatibility method."""
    cbcsdk_mock.mock_request('DELETE', '/policyservice/v1/orgs/test/policies/65536/rules/1',
                             CBCSDKMock.StubResponse(None, scode=204))
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_count = len(policy.object_rules)
    policy.delete_rule(1)
    assert len(policy.object_rules) == rule_count - 1
    assert len(policy.rules) == rule_count - 1
    assert 1 not in [rd['id'] for rd in policy.rules]


def test_rule_delete_by_compatibility_method_nonexistent(cb):
    """Tests what happens when you try to delete a nonexistent rule by compatibility method."""
    policy = Policy(cb, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_count = len(policy.object_rules)
    with pytest.raises(ApiError):
        policy.delete_rule(6)
    assert len(policy.object_rules) == rule_count
    assert len(policy.rules) == rule_count


def test_rule_delete_is_new(cb):
    """Tests deleting a new PolicyRule raises an error."""
    policy = Policy(cb, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    new_rule = PolicyRule(cb, policy, None, RULE_ADD_1, False, True)
    with pytest.raises(ApiError):
        new_rule.delete()


def test_policy_builder_make_policy(cbcsdk_mock):
    """Tests using a policy builder to create a new policy."""
    def on_post(uri, body, **kwargs):
        assert body == NEW_POLICY_CONSTRUCT_1
        return NEW_POLICY_RETURN_1

    cbcsdk_mock.mock_request('GET', "/policyservice/v1/orgs/test/rule_configs/"
                                    "88b19232-7ebb-48ef-a198-2a75a282de5d/parameters/schema",
                             BASIC_CONFIG_TEMPLATE_RETURN)
    cbcsdk_mock.mock_request('GET', "/policyservice/v1/orgs/test/rule_configs/"
                                    "ac67fa14-f6be-4df9-93f2-6de0dbd96061/parameters/schema",
                             BASIC_CONFIG_TEMPLATE_RETURN)
    cbcsdk_mock.mock_request('POST', '/policyservice/v1/orgs/test/policies', on_post)
    api = cbcsdk_mock.api
    builder = Policy.create(api)
    builder.set_name("New Policy Name").set_priority("HIGH").set_description("Foobar")
    builder.set_auto_deregister_interval(1000).set_auto_delete_bad_hash_delay(500)
    builder.set_avira_protection_cloud(True, 3600, 1024, 5).set_on_access_scan(True, "AGGRESSIVE")
    builder.set_on_demand_scan(True, "AGGRESSIVE", "DISABLED", "DISABLED")
    builder.set_on_demand_scan_schedule(["MONDAY", "WEDNESDAY", "FRIDAY"], 6, 4, False)
    builder.set_signature_update(True).set_signature_update_schedule(12, 3, 6)
    builder.set_update_servers_override(["http://contoso.com/foo"])
    builder.set_update_servers_onsite(["http://example.com/foo", "http://example.org/foo"], ["http://example.org/foo"])
    builder.set_update_servers_offsite(["http://amytapie.com/foo"])
    builder.add_directory_action_rule("/usr", True, True).add_directory_action_rule("/tmp", False, False)
    rule = PolicyRule(api, None, 409, RULE_ADD_2, False, True)
    builder.add_rule_copy(rule).add_rule("REPUTATION", "COMPANY_BLACK_LIST", "RUN", "DENY", False)
    builder.add_sensor_setting("SCAN_EXECUTE_ON_NETWORK_DRIVE", "false").add_sensor_setting("UBS_OPT_IN", "true")
    builder.add_sensor_setting("SCAN_EXECUTE_ON_NETWORK_DRIVE", "true").add_sensor_setting("ALLOW_UNINSTALL", "true")
    builder.set_managed_detection_response_permissions(False, True)
    rule_config = PolicyRuleConfig(api, None, BUILD_RULECONFIG_1['id'], BUILD_RULECONFIG_1, False, True)
    builder.add_rule_config_copy(rule_config)
    builder.add_rule_config("ac67fa14-f6be-4df9-93f2-6de0dbd96061", "Credential Theft", "core_prevention",
                            WindowsAssignmentMode='REPORT')
    policy = builder.build()
    assert policy._info == NEW_POLICY_CONSTRUCT_1
    policy.save()
    assert policy.id == 30250


def test_policy_builder_error_handling(cb):
    """Tests the error handling in the various PolicyBuilder setter functions."""
    builder = Policy.create(cb)
    with pytest.raises(ApiError):
        builder.set_priority("DOGWASH")
    with pytest.raises(ApiError):
        builder.set_on_access_scan(True, "SLOW")
    with pytest.raises(ApiError):
        builder.set_on_demand_scan(True, "ABNORMAL")
    with pytest.raises(ApiError):
        builder.set_on_demand_scan(True, "NORMAL", "JUNKVALUE")
    with pytest.raises(ApiError):
        builder.set_on_demand_scan(True, "NORMAL", "AUTOSCAN", "JUNKVALUE")
    with pytest.raises(ApiError):
        builder.set_on_demand_scan_schedule(["WEDNESDAY", "FRIDAY", "HELLDAY"], 0, 6)
    with pytest.raises(ApiError):
        builder.add_sensor_setting("LONG_RANGE", "true")


@pytest.mark.parametrize("element", [
    {"id": 10240, "position": 1},
    [10240, 1],
    (10240, 1)
])
def test_preview_policy_changes(cbcsdk_mock, element):
    """Tests the preview_policy_changes function on the Policy class."""
    def on_post(uri, body, **kwargs):
        assert body == PREVIEW_POLICY_CHANGES_REQUEST1
        return PREVIEW_POLICY_CHANGES_RESPONSE1

    cbcsdk_mock.mock_request('POST', '/policy-assignment/v1/orgs/test/policies/preview', on_post)
    api = cbcsdk_mock.api
    results = Policy.preview_policy_changes(api, [element])
    assert len(results) == 2
    assert results[0].current_policy_id == 70722
    assert results[0].current_policy_position == 2
    assert results[0].new_policy_id == 10240
    assert results[0].new_policy_position == 1
    assert results[0].asset_count == 5
    assert results[1].current_policy_id == 142857
    assert results[1].current_policy_position == 1
    assert results[1].new_policy_id == 10240
    assert results[1].new_policy_position == 1
    assert results[1].asset_count == 2


def test_preview_rank_change(cbcsdk_mock):
    """Tests the preview_rank_change function on the policy class."""
    def on_post(uri, body, **kwargs):
        assert body == PREVIEW_POLICY_CHANGES_REQUEST2
        return PREVIEW_POLICY_CHANGES_RESPONSE2

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536', FULL_POLICY_1)
    cbcsdk_mock.mock_request('POST', '/policy-assignment/v1/orgs/test/policies/preview', on_post)
    api = cbcsdk_mock.api
    policy = api.select(Policy, 65536)
    results = policy.preview_rank_change(1)
    assert results[0].current_policy_id == 1492
    assert results[0].current_policy_position == 2
    assert results[0].new_policy_id == 65536
    assert results[0].new_policy_position == 1
    assert results[0].asset_count == 5
    assert results[1].current_policy_id == 74656
    assert results[1].current_policy_position == 1
    assert results[1].new_policy_id == 65536
    assert results[1].new_policy_position == 1
    assert results[1].asset_count == 2


def test_policy_rank_change_preview_helper_methods(cbcsdk_mock):
    """Tests the helper methods on the PolicyRankChangePreview object."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536', FULL_POLICY_1)
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/1492', FULL_POLICY_5)
    api = cbcsdk_mock.api
    preview = PolicyRankChangePreview(api, PREVIEW_POLICY_CHANGES_RESPONSE2['preview'][0])
    policy = preview.current_policy
    assert policy.id == 1492
    policy = preview.new_policy
    assert policy.id == 65536
    query = preview.asset_query
    assert isinstance(query, DeviceSearchQuery)
    request = query._build_request(-1, -1)
    assert request['query'] == "(-_exists_:ag_agg_key_dynamic AND ag_agg_key_manual:1790b51e683c8a20c2b2bbe3e41eacdc53e3632087bb5a3f2868588e99157b06 AND policy_override:false) OR (-_exists_:ag_agg_key_dynamic AND ag_agg_key_manual:aa8bd7e69c4ee45918bb126a17d90a1c8368b46f9bb5bf430cb0250c317cd1dc AND policy_override:false)"  # noqa: E501
