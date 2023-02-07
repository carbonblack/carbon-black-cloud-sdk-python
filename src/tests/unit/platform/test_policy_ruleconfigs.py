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

"""Tests of the policy rule configurations support in the Platform API."""

import copy
import pytest
import logging
import random
from contextlib import ExitStack as does_not_raise
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.platform import Policy, PolicyRuleConfig
from cbc_sdk.errors import ApiError, InvalidObjectError, ServerError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_policies import (FULL_POLICY_1, BASIC_CONFIG_TEMPLATE_RETURN,
                                                        TEMPLATE_RETURN_BOGUS_TYPE, POLICY_CONFIG_PRESENTATION,
                                                        REPLACE_RULECONFIG)


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

@pytest.mark.parametrize("initial_data, param_schema_return, handler, message", [
    ({"id": "88b19232-7ebb-48ef-a198-2a75a282de5d", "name": "Privilege Escalation", "inherited_from": "",
      "category": "core_prevention", "parameters": {"WindowsAssignmentMode": "BLOCK"}},
     BASIC_CONFIG_TEMPLATE_RETURN, does_not_raise(), None),
    ({"id": "88b19232-7ebb-48ef-a198-2a75a282de5d", "name": "Privilege Escalation", "inherited_from": "",
      "category": "core_prevention", "parameters": {"WindowsAssignmentMode": "BLOCK"}},
     ServerError(error_code=400, message="blah"), pytest.raises(InvalidObjectError),
     "invalid rule config ID 88b19232-7ebb-48ef-a198-2a75a282de5d"),
    ({"id": "88b19232-7ebb-48ef-a198-2a75a282de5d", "name": "Privilege Escalation", "inherited_from": "",
      "category": "core_prevention", "parameters": {}},
     BASIC_CONFIG_TEMPLATE_RETURN, does_not_raise(), None),
    ({"id": "88b19232-7ebb-48ef-a198-2a75a282de5d", "name": "Privilege Escalation", "inherited_from": "",
      "category": "core_prevention", "parameters": {"WindowsAssignmentMode": "BLOCK"}},
     TEMPLATE_RETURN_BOGUS_TYPE, pytest.raises(ApiError),
     "internal error: 'bogus' is not valid under any of the given schemas"),
    ({"id": "88b19232-7ebb-48ef-a198-2a75a282de5d", "name": "Privilege Escalation", "inherited_from": "",
      "category": "core_prevention", "parameters": {"WindowsAssignmentMode": 666}},
     BASIC_CONFIG_TEMPLATE_RETURN, pytest.raises(InvalidObjectError),
     "parameter error: 666 is not of type 'string'"),
    ({"id": "88b19232-7ebb-48ef-a198-2a75a282de5d", "name": "Privilege Escalation", "inherited_from": "",
      "category": "core_prevention", "parameters": {"WindowsAssignmentMode": "BOGUSVALUE"}},
     BASIC_CONFIG_TEMPLATE_RETURN, pytest.raises(InvalidObjectError),
     "parameter error: 'BOGUSVALUE' is not one of ['REPORT', 'BLOCK']"),
])
def test_rule_config_validate(cbcsdk_mock, initial_data, param_schema_return, handler, message):
    """Tests rule configuration validation."""
    def param_schema(uri, query_params, default):
        if isinstance(param_schema_return, Exception):
            raise param_schema_return
        return param_schema_return

    cbcsdk_mock.mock_request('GET', f"/policyservice/v1/orgs/test/rule_configs/{initial_data['id']}/parameters/schema",
                             param_schema)
    api = cbcsdk_mock.api
    rule_config = Policy._create_rule_config(api, None, initial_data)
    with handler as h:
        rule_config.validate()
    if message is not None:
        assert h.value.args[0] == message


@pytest.mark.parametrize("new_data, get_id, handler, message", [
    ({"id": "88b19232-7ebb-48ef-a198-2a75a282de5d", "name": "Privilege Escalation", "inherited_from": "",
      "category": "core_prevention", "parameters": {"WindowsAssignmentMode": "BLOCK"}},
     None, does_not_raise(), None),
    ({"id": "88b19236-7ebb-48ef-a198-2a75a282de5d", "name": "Privilege Escalation", "inherited_from": "",
      "category": "core_prevention", "parameters": {"WindowsAssignmentMode": "BLOCK"}},
     "88b19232-7ebb-48ef-a198-2a75a282de5d", pytest.raises(InvalidObjectError),
     "invalid rule config ID 88b19236-7ebb-48ef-a198-2a75a282de5d"),
    ({"id": "88b19232-7ebb-48ef-a198-2a75a282de5d", "name": "Privilege Escalation", "inherited_from": "",
      "category": "core_prevention", "parameters": {}},
     None, does_not_raise(), None),
    ({"id": "88b19232-7ebb-48ef-a198-2a75a282de5d", "name": "Privilege Escalation", "inherited_from": "",
      "category": "core_prevention", "parameters": {"WindowsAssignmentMode": 666}},
     None, pytest.raises(InvalidObjectError), "parameter error: 666 is not of type 'string'"),
    ({"id": "88b19232-7ebb-48ef-a198-2a75a282de5d", "name": "Privilege Escalation", "inherited_from": "",
      "category": "core_prevention", "parameters": {"WindowsAssignmentMode": "BOGUSVALUE"}},
     None, pytest.raises(InvalidObjectError), "parameter error: 'BOGUSVALUE' is not one of ['REPORT', 'BLOCK']"),
])
def test_rule_config_validate_inside_policy(cbcsdk_mock, new_data, get_id, handler, message):
    """Tests rule configuration validation when it's part of a policy."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65535/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    api = cbcsdk_mock.api
    policy = Policy(api, 65535, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_config_id = get_id if get_id is not None else new_data['id']
    rule_config = policy.object_rule_configs[rule_config_id]
    rule_config._info = copy.deepcopy(new_data)
    with handler as h:
        rule_config.validate()
    if message is not None:
        assert h.value.args[0] == message


def test_rule_config_refresh(cbcsdk_mock):
    """Tests the rule config refresh() operation."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536', FULL_POLICY_1)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, FULL_POLICY_1, False, True)
    rule_config = random.choice(list(policy.object_rule_configs.values()))
    old_name = rule_config.name
    old_category = rule_config.category
    old_parameters = rule_config.parameters
    rule_config.refresh()
    assert rule_config.name == old_name
    assert rule_config.category == old_category
    assert rule_config.parameters == old_parameters


@pytest.mark.parametrize("give_error, handler", [
    (False, does_not_raise()),
    (True, pytest.raises(ServerError))
])
def test_rule_config_add_by_object(cbcsdk_mock, give_error, handler):
    """Tests using a PolicyRuleConfig object to add a rule configuration."""
    def on_put(url, body, **kwargs):
        assert body == FULL_POLICY_1
        if give_error:
            return CBCSDKMock.StubResponse("Failure", scode=404)
        rc = copy.deepcopy(body)
        return rc

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536', on_put)
    api = cbcsdk_mock.api
    policy_data = copy.deepcopy(FULL_POLICY_1)
    rule_config_data1 = [p for p in enumerate(policy_data['rule_configs'])
                         if p[1]['id'] == '88b19232-7ebb-48ef-a198-2a75a282de5d']
    rule_config_data = rule_config_data1[0][1]
    del policy_data['rule_configs'][rule_config_data1[0][0]]
    policy = Policy(api, 65536, policy_data, False, True)
    rule_config_count = len(policy.object_rule_configs)
    new_rule_config = Policy._create_rule_config(api, policy, rule_config_data)
    new_rule_config.touch()
    with handler:
        new_rule_config.save()
        assert len(policy.object_rule_configs) == rule_config_count + 1
        assert '88b19232-7ebb-48ef-a198-2a75a282de5d' in policy.object_rule_configs


def test_rule_config_add_by_base_method(cbcsdk_mock):
    """Tests using the base method on Policy to add a rule."""
    def on_put(url, body, **kwargs):
        assert body == FULL_POLICY_1
        return copy.deepcopy(body)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536', on_put)
    api = cbcsdk_mock.api
    policy_data = copy.deepcopy(FULL_POLICY_1)
    rule_config_data1 = [p for p in enumerate(policy_data['rule_configs'])
                         if p[1]['id'] == '88b19232-7ebb-48ef-a198-2a75a282de5d']
    rule_config_data = rule_config_data1[0][1]
    del policy_data['rule_configs'][rule_config_data1[0][0]]
    policy = Policy(api, 65536, policy_data, False, True)
    rule_config_count = len(policy.object_rule_configs)
    policy.add_rule_config(rule_config_data)
    assert len(policy.object_rule_configs) == rule_config_count + 1
    assert '88b19232-7ebb-48ef-a198-2a75a282de5d' in policy.object_rule_configs


def test_rule_config_modify_by_object(cbcsdk_mock):
    """Tests modifying a PolicyRuleConfig object within the policy."""
    def on_put(url, body, **kwargs):
        nonlocal new_data
        assert body == new_data
        return copy.deepcopy(body)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536', on_put)
    api = cbcsdk_mock.api
    new_data = copy.deepcopy(FULL_POLICY_1)
    new_data['rule_configs'][3]['parameters']['WindowsAssignmentMode'] = 'REPORT'
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_config_count = len(policy.object_rule_configs)
    rule_config = policy.object_rule_configs['88b19232-7ebb-48ef-a198-2a75a282de5d']
    rule_config.set_parameter('WindowsAssignmentMode', 'REPORT')
    rule_config.save()
    assert len(policy.object_rule_configs) == rule_config_count
    rule_config = policy.object_rule_configs['88b19232-7ebb-48ef-a198-2a75a282de5d']
    assert rule_config.get_parameter('WindowsAssignmentMode') == 'REPORT'


def test_rule_config_modify_by_base_method(cbcsdk_mock):
    """Tests modifying a PolicyRuleConfig object using the replace_rule_config method."""
    def on_put(url, body, **kwargs):
        nonlocal new_data
        assert body == new_data
        return copy.deepcopy(body)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536', on_put)
    api = cbcsdk_mock.api
    new_data = copy.deepcopy(FULL_POLICY_1)
    new_data['rule_configs'][3]['parameters']['WindowsAssignmentMode'] = 'REPORT'
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_config_count = len(policy.object_rule_configs)
    policy.replace_rule_config('88b19232-7ebb-48ef-a198-2a75a282de5d', REPLACE_RULECONFIG)
    assert len(policy.object_rule_configs) == rule_config_count
    rule_config = policy.object_rule_configs['88b19232-7ebb-48ef-a198-2a75a282de5d']
    assert rule_config.get_parameter('WindowsAssignmentMode') == 'REPORT'


def test_rule_config_modify_by_base_method_invalid_id(cb):
    """Tests modifying a PolicyRuleConfig object using replace_rule_config, but with an invalid ID."""
    policy = Policy(cb, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    with pytest.raises(ApiError):
        policy.replace_rule_config('88b19266-7ebb-48ef-a198-2a75a282de5d', REPLACE_RULECONFIG)


def test_rule_config_delete_by_object(cbcsdk_mock):
    """Tests deleting a PolicyRuleConfig object from a policy."""
    def on_put(url, body, **kwargs):
        nonlocal new_data
        assert body == new_data
        return copy.deepcopy(body)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536', on_put)
    api = cbcsdk_mock.api
    new_data = copy.deepcopy(FULL_POLICY_1)
    rule_config_data1 = [p for p in enumerate(new_data['rule_configs'])
                         if p[1]['id'] == '88b19232-7ebb-48ef-a198-2a75a282de5d']
    del new_data['rule_configs'][rule_config_data1[0][0]]
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_config_count = len(policy.object_rule_configs)
    rule_config = policy.object_rule_configs['88b19232-7ebb-48ef-a198-2a75a282de5d']
    assert not rule_config.is_deleted
    rule_config.delete()
    assert len(policy.object_rule_configs) == rule_config_count - 1
    assert '88b19232-7ebb-48ef-a198-2a75a282de5d' not in policy.object_rule_configs
    assert rule_config.is_deleted


def test_rule_config_delete_by_base_method(cbcsdk_mock):
    """Tests deleting a rule configuration from a policy via the delete_rule_config method."""
    def on_put(url, body, **kwargs):
        nonlocal new_data
        assert body == new_data
        return copy.deepcopy(body)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536', on_put)
    api = cbcsdk_mock.api
    new_data = copy.deepcopy(FULL_POLICY_1)
    rule_config_data1 = [p for p in enumerate(new_data['rule_configs'])
                         if p[1]['id'] == '88b19232-7ebb-48ef-a198-2a75a282de5d']
    del new_data['rule_configs'][rule_config_data1[0][0]]
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_config_count = len(policy.object_rule_configs)
    policy.delete_rule_config('88b19232-7ebb-48ef-a198-2a75a282de5d')
    assert len(policy.object_rule_configs) == rule_config_count - 1
    assert '88b19232-7ebb-48ef-a198-2a75a282de5d' not in policy.object_rule_configs


def test_rule_config_delete_by_base_method_nonexistent(cb):
    """Tests what happens when you try to delete a nonexistent rule configuration via delete_rule_config."""
    policy = Policy(cb, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    with pytest.raises(ApiError):
        policy.delete_rule_config('88b19266-7ebb-48ef-a198-2a75a282de5d')


def test_rule_config_delete_is_new(cb):
    """Tests that deleting a new PolicyRuleConfig raises an error."""
    policy = Policy(cb, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    new_rule_config = PolicyRuleConfig(cb, policy, None, REPLACE_RULECONFIG, False, True)
    with pytest.raises(ApiError):
        new_rule_config.delete()
