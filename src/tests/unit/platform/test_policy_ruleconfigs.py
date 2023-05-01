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

"""Tests of the policy rule configurations support in the Platform API."""

import copy
import pytest
import logging
from contextlib import ExitStack as does_not_raise
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.platform import Policy, PolicyRuleConfig
from cbc_sdk.platform.policy_ruleconfigs import CorePreventionRuleConfig
from cbc_sdk.errors import ApiError, InvalidObjectError, ServerError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_policies import (FULL_POLICY_1, BASIC_CONFIG_TEMPLATE_RETURN,
                                                        TEMPLATE_RETURN_BOGUS_TYPE, POLICY_CONFIG_PRESENTATION,
                                                        REPLACE_RULECONFIG, FULL_POLICY_5)
from tests.unit.fixtures.platform.mock_policy_ruleconfigs import (CORE_PREVENTION_RETURNS, CORE_PREVENTION_UPDATE_1,
                                                                  HBFW_GET_RESULT, HBFW_MODIFY_PUT_REQUEST,
                                                                  HBFW_MODIFY_PUT_RESPONSE, HBFW_ADD_RULE_PUT_REQUEST,
                                                                  HBFW_ADD_RULE_PUT_RESPONSE,
                                                                  HBFW_ADD_RULE_GROUP_PUT_REQUEST,
                                                                  HBFW_ADD_RULE_GROUP_PUT_RESPONSE,
                                                                  HBFW_REMOVE_RULE_PUT_REQUEST,
                                                                  HBFW_REMOVE_RULE_PUT_RESPONSE,
                                                                  HBFW_REMOVE_RULE_GROUP_PUT_REQUEST,
                                                                  HBFW_REMOVE_RULE_GROUP_PUT_RESPONSE)


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


@pytest.fixture(scope="function")
def policy(cb):
    """Mocks a sample policy for unit tests"""
    return Policy(cb, 65536, copy.deepcopy(FULL_POLICY_1), False, True)


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
def test_rule_config_validate_inside_policy(cbcsdk_mock, policy, new_data, get_id, handler, message):
    """Tests rule configuration validation when it's part of a policy."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    rule_config_id = get_id if get_id is not None else new_data['id']
    rule_config = policy.object_rule_configs[rule_config_id]
    rule_config._info = copy.deepcopy(new_data)
    with handler as h:
        rule_config.validate()
    if message is not None:
        assert h.value.args[0] == message


def test_rule_config_refresh(cbcsdk_mock, policy):
    """Tests the rule config refresh() operation."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536', FULL_POLICY_1)
    # Replace all rule configs with the base class for purposes of this test
    cfgs = policy._info.get("rule_configs", [])
    ruleconfigobjects = [PolicyRuleConfig(cbcsdk_mock.api, policy, cfg['id'], cfg, force_init=False, full_doc=True)
                         for cfg in cfgs]
    policy._object_rule_configs = dict([(rconf.id, rconf) for rconf in ruleconfigobjects])
    policy._object_rule_configs_need_load = False
    # proceed with test
    for rule_config in policy.object_rule_configs_list:
        old_name = rule_config.name
        old_category = rule_config.category
        old_parameters = rule_config.parameters
        rule_config.refresh()
        assert rule_config.name == old_name
        assert rule_config.category == old_category
        assert rule_config.parameters == old_parameters


def test_rule_config_add_base_not_implemented(cbcsdk_mock):
    """Verifies that adding a new BaseRuleConfig is not implemented."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    api = cbcsdk_mock.api
    policy_data = copy.deepcopy(FULL_POLICY_1)
    rule_config_data1 = [p for p in enumerate(policy_data['rule_configs'])
                         if p[1]['id'] == '88b19232-7ebb-48ef-a198-2a75a282de5d']
    rule_config_data = rule_config_data1[0][1]
    del policy_data['rule_configs'][rule_config_data1[0][0]]
    policy = Policy(api, 65536, policy_data, False, True)  # this policy HAS to be created here because data was altered
    new_rule_config = PolicyRuleConfig(api, policy, '88b19232-7ebb-48ef-a198-2a75a282de5d', rule_config_data,
                                       force_init=False, full_doc=True)
    new_rule_config.touch()
    with pytest.raises(NotImplementedError):
        new_rule_config.save()


def test_rule_config_delete_base_not_implemented(cbcsdk_mock, policy):
    """Verifies that deleting a BaseRuleConfig is not implemented."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    # Replace all rule configs with the base class for purposes of this test
    cfgs = policy._info.get("rule_configs", [])
    ruleconfigobjects = [PolicyRuleConfig(cbcsdk_mock.api, policy, cfg['id'], cfg, force_init=False, full_doc=True)
                         for cfg in cfgs]
    policy._object_rule_configs = dict([(rconf.id, rconf) for rconf in ruleconfigobjects])
    policy._object_rule_configs_need_load = False
    # proceed with test
    with pytest.raises(NotImplementedError):
        policy.delete_rule_config('88b19232-7ebb-48ef-a198-2a75a282de5d')


def test_rule_config_modify_by_base_method_invalid_id(policy):
    """Tests modifying a PolicyRuleConfig object using replace_rule_config, but with an invalid ID."""
    with pytest.raises(ApiError):
        policy.replace_rule_config('88b19266-7ebb-48ef-a198-2a75a282de5d', REPLACE_RULECONFIG)


def test_rule_config_delete_by_base_method_nonexistent(policy):
    """Tests what happens when you try to delete a nonexistent rule configuration via delete_rule_config."""
    with pytest.raises(ApiError):
        policy.delete_rule_config('88b19266-7ebb-48ef-a198-2a75a282de5d')


def test_rule_config_initialization_matches_categories(policy):
    """Tests that rule configurations are initialized with the correct classes."""
    for cfg in policy.object_rule_configs.values():
        if cfg.category == "core_prevention":
            assert isinstance(cfg, CorePreventionRuleConfig)
        else:
            assert not isinstance(cfg, CorePreventionRuleConfig)


def test_core_prevention_refresh(cbcsdk_mock, policy):
    """Tests the refresh operation for a CorePreventionRuleConfig."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/rule_configs/core_prevention',
                             CORE_PREVENTION_RETURNS)
    for rule_config in policy.core_prevention_rule_configs_list:
        rule_config.refresh()


def test_core_prevention_set_assignment_mode(policy):
    """Tests the assignment mode setting, which uses the underlying parameter setting."""
    for rule_config in policy.core_prevention_rule_configs_list:
        old_mode = rule_config.get_assignment_mode()
        assert not rule_config.is_dirty()
        rule_config.set_assignment_mode(old_mode)
        assert not rule_config.is_dirty()
        rule_config.set_assignment_mode('BLOCK' if old_mode == 'REPORT' else 'REPORT')
        assert rule_config.is_dirty()
        with pytest.raises(ApiError):
            rule_config.set_assignment_mode('BOGUSVALUE')


def test_core_prevention_update_and_save(cbcsdk_mock, policy):
    """Tests updating the core prevention data and saving it."""
    put_called = False

    def on_put(url, body, **kwargs):
        nonlocal put_called
        assert body == CORE_PREVENTION_UPDATE_1
        put_called = True
        return copy.deepcopy(body)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536/rule_configs/core_prevention', on_put)
    rule_config = policy.core_prevention_rule_configs['c4ed61b3-d5aa-41a9-814f-0f277451532b']
    assert rule_config.name == 'Carbon Black Threat Intel'
    assert rule_config.get_assignment_mode() == 'REPORT'
    rule_config.set_assignment_mode('BLOCK')
    rule_config.save()
    assert put_called


def test_core_prevention_update_via_replace(cbcsdk_mock, policy):
    """Tests updating the core prevention data and saving it via replace_rule_config."""
    put_called = False

    def on_put(url, body, **kwargs):
        nonlocal put_called
        assert body == CORE_PREVENTION_UPDATE_1
        put_called = True
        return copy.deepcopy(body)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536/rule_configs/core_prevention', on_put)
    rule_config = policy.core_prevention_rule_configs['c4ed61b3-d5aa-41a9-814f-0f277451532b']
    assert rule_config.name == 'Carbon Black Threat Intel'
    assert rule_config.get_assignment_mode() == 'REPORT'
    new_data = copy.deepcopy(rule_config._info)
    new_data["parameters"]["WindowsAssignmentMode"] = "BLOCK"
    policy.replace_rule_config('c4ed61b3-d5aa-41a9-814f-0f277451532b', new_data)
    assert put_called
    assert rule_config.get_assignment_mode() == "BLOCK"


def test_core_prevention_delete(cbcsdk_mock, policy):
    """Tests delete of a core prevention data item."""
    delete_called = False

    def on_delete(url, body):
        nonlocal delete_called
        delete_called = True
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('DELETE', '/policyservice/v1/orgs/test/policies/65536/rule_configs/core_prevention'
                                       '/c4ed61b3-d5aa-41a9-814f-0f277451532b', on_delete)
    rule_config = policy.core_prevention_rule_configs['c4ed61b3-d5aa-41a9-814f-0f277451532b']
    assert rule_config.name == 'Carbon Black Threat Intel'
    rule_config.delete()
    assert delete_called


def test_host_based_firewall_contents(policy):
    """Tests the contents of the host-based firewall rule configuration, along with the refresh."""
    rule_config = policy.host_based_firewall_rule_config
    assert not rule_config.enabled
    assert rule_config.default_action == "ALLOW"
    groups = rule_config.rule_groups
    assert len(groups) == 1
    assert groups[0].name == "Argon_firewall"
    rules = groups[0].rules_
    assert len(rules) == 1
    assert rules[0].action == "ALLOW"
    assert rules[0].direction == "IN"
    assert rules[0].local_ip_address == "1.2.3.4"
    assert rules[0].name == "my_first_rule"
    assert rules[0].remote_ip_address == "5.6.7.8"


def test_host_based_firewall_refresh(cbcsdk_mock):
    """Tests that refresh() restores values in the rule configuration."""
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/rule_configs/host_based_firewall',
                             HBFW_GET_RESULT)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_config = policy.host_based_firewall_rule_config
    rule_config.set_default_action("BLOCK")
    groups = rule_config.rule_groups
    assert len(groups) == 1
    rules = groups[0].rules_
    assert len(rules) == 1
    rules[0].local_ip_address = "127.0.0.1"
    rules[0].remote_ip_address = "10.29.99.1"
    rule_config.refresh()
    assert not rule_config.enabled
    assert rule_config.default_action == "ALLOW"
    groups = rule_config.rule_groups
    assert len(groups) == 1
    rules = groups[0].rules_
    assert len(rules) == 1
    assert rules[0].local_ip_address == "1.2.3.4"
    assert rules[0].remote_ip_address == "5.6.7.8"


def test_delete_host_based_firewall(cbcsdk_mock):
    """Tests that delete resets the host-based firewall rule configuration."""
    delete_called = False
    get_called = 0

    def on_delete(url, body):
        nonlocal delete_called
        delete_called = True
        return CBCSDKMock.StubResponse(None, scode=204)

    def on_get(url, params, default):
        nonlocal delete_called, get_called
        assert delete_called
        get_called += 1
        return HBFW_GET_RESULT

    cbcsdk_mock.mock_request('DELETE', '/policyservice/v1/orgs/test/policies/65536/rule_configs/host_based_firewall'
                                       '/df181779-f623-415d-879e-91c40246535d', on_delete)
    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/rule_configs/host_based_firewall',
                             on_get)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_config = policy.host_based_firewall_rule_config
    rule_config.delete()
    assert delete_called
    assert get_called == 0
    assert not rule_config.enabled
    assert rule_config.default_action == "ALLOW"
    assert get_called == 1


def test_modify_host_based_firewall(cbcsdk_mock):
    """Tests modifying a host-based firewall rule configuration's data."""
    put_called = False

    def on_put(url, body, **kwargs):
        nonlocal put_called
        assert body == HBFW_MODIFY_PUT_REQUEST
        put_called = True
        return copy.deepcopy(HBFW_MODIFY_PUT_RESPONSE)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536/rule_configs/host_based_firewall',
                             on_put)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_config = policy.host_based_firewall_rule_config
    rule_config.set_enabled(True)
    rule_config.set_default_action("BLOCK")
    groups = rule_config.rule_groups
    groups[0].description = "Starship go BOOM"
    rules = groups[0].rules_
    rules[0].remote_ip_address = "199.201.128.1"
    rules[0].direction = "BOTH"
    rule_config.save()
    assert put_called
    assert rule_config.enabled
    assert rule_config.default_action == "BLOCK"
    groups = rule_config.rule_groups
    assert groups[0].description == "Starship go BOOM"
    rules = groups[0].rules_
    assert rules[0].remote_ip_address == "199.201.128.1"
    assert rules[0].direction == "BOTH"


def test_host_based_firewall_parameter_errors(cb, policy):
    """Tests bad values for host-based firewall parameters."""
    rule_config = policy.host_based_firewall_rule_config
    with pytest.raises(ApiError):
        rule_config.set_default_action("NOTEXIST")


def test_modify_add_rule_to_host_based_firewall(cbcsdk_mock):
    """Tests modifying a host-based firewall rule configuration by adding a rule."""
    put_called = False

    def on_put(url, body, **kwargs):
        nonlocal put_called
        assert body == HBFW_ADD_RULE_PUT_REQUEST
        put_called = True
        return copy.deepcopy(HBFW_ADD_RULE_PUT_RESPONSE)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536/rule_configs/host_based_firewall',
                             on_put)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_config = policy.host_based_firewall_rule_config
    groups = rule_config.rule_groups
    new_rule = rule_config.new_rule("DoomyDoomsOfDoom", "BLOCK", "BOTH", "TCP", "199.201.128.1")
    new_rule.remote_port_ranges = "666"
    new_rule.local_ip_address = "10.29.99.1"
    new_rule.application_path = "C:\\DOOM\\DOOM.EXE"
    groups[0].append_rule(new_rule)
    rule_config.save()
    assert put_called
    groups = rule_config.rule_groups
    assert len(groups) == 1
    rules = groups[0].rules_
    assert len(rules) == 2
    assert rules[0].name == "my_first_rule"
    assert rules[1].name == "DoomyDoomsOfDoom"
    assert rules[1].action == "BLOCK"
    assert rules[1].application_path == "C:\\DOOM\\DOOM.EXE"
    assert rules[1].direction == "BOTH"
    assert rules[1].enabled
    assert rules[1].local_ip_address == "10.29.99.1"
    assert rules[1].local_port_ranges == "*"
    assert rules[1].protocol == "TCP"
    assert rules[1].remote_ip_address == "199.201.128.1"
    assert rules[1].remote_port_ranges == "666"
    assert not rules[1].test_mode


def test_new_rule_parameter_errors(cb, policy):
    """Tests the parameter check errors on the new_rule() method."""
    rule_config = policy.host_based_firewall_rule_config
    with pytest.raises(ApiError):
        rule_config.new_rule("DoomyDoomsOfDoom", "NOTEXIST", "BOTH", "TCP", "199.201.128.1")
    with pytest.raises(ApiError):
        rule_config.new_rule("DoomyDoomsOfDoom", "BLOCK", "NOTEXIST", "TCP", "199.201.128.1")
    with pytest.raises(ApiError):
        rule_config.new_rule("DoomyDoomsOfDoom", "BLOCK", "BOTH", "NOTEXIST", "199.201.128.1")


def test_modify_add_rule_group_to_host_based_firewall(cbcsdk_mock):
    """Tests modifying a host-based firewall rule configuration by adding a rule group."""
    put_called = False

    def on_put(url, body, **kwargs):
        nonlocal put_called
        assert body == HBFW_ADD_RULE_GROUP_PUT_REQUEST
        put_called = True
        return copy.deepcopy(HBFW_ADD_RULE_GROUP_PUT_RESPONSE)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/65536/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/65536/rule_configs/host_based_firewall',
                             on_put)
    api = cbcsdk_mock.api
    policy = Policy(api, 65536, copy.deepcopy(FULL_POLICY_1), False, True)
    rule_config = policy.host_based_firewall_rule_config
    new_group = rule_config.new_rule_group("DOOM_firewall", "No playing DOOM!")
    new_rule = rule_config.new_rule("DoomyDoomsOfDoom", "BLOCK", "BOTH", "TCP", "199.201.128.1")
    new_rule.remote_port_ranges = "666"
    new_rule.local_ip_address = "10.29.99.1"
    new_rule.application_path = "C:\\DOOM\\DOOM.EXE"
    new_group.append_rule(new_rule)
    rule_config.append_rule_group(new_group)
    rule_config.save()
    assert put_called
    groups = rule_config.rule_groups
    assert len(groups) == 2
    assert groups[0].name == "Argon_firewall"
    assert groups[0].description == "Whatever"
    rules = groups[0].rules_
    assert len(rules) == 1
    assert rules[0].name == "my_first_rule"
    assert groups[1].name == "DOOM_firewall"
    assert groups[1].description == "No playing DOOM!"
    rules = groups[1].rules_
    assert len(rules) == 1
    assert rules[0].name == "DoomyDoomsOfDoom"


def test_modify_remove_rule_from_host_based_firewall(cbcsdk_mock):
    """Tests modifying a host-based firewall rule configuration by removing a rule."""
    put_called = False

    def on_put(url, body, **kwargs):
        nonlocal put_called
        assert body == HBFW_REMOVE_RULE_PUT_REQUEST
        put_called = True
        return copy.deepcopy(HBFW_REMOVE_RULE_PUT_RESPONSE)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/1492/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/1492/rule_configs/host_based_firewall',
                             on_put)
    api = cbcsdk_mock.api
    policy = Policy(api, 1492, copy.deepcopy(FULL_POLICY_5), False, True)
    rule_config = policy.host_based_firewall_rule_config
    result_groups = [group for group in rule_config.rule_groups if group.name == "Crapco_firewall"]
    assert len(result_groups) == 1
    result_rules = [rule for rule in result_groups[0].rules_ if rule.name == "DoomyDoomsOfDoom"]
    assert len(result_rules) == 1
    result_rules[0].remove()
    rule_config.save()
    assert put_called
    result_groups = [group for group in rule_config.rule_groups if group.name == "Crapco_firewall"]
    assert len(result_groups) == 1
    result_rules = result_groups[0].rules_
    assert len(result_rules) == 1
    assert result_rules[0].name == "my_first_rule"


def test_modify_remove_rule_group_from_host_based_firewall(cbcsdk_mock):
    """Tests modifying a host-based firewall rule configuration by removing a rule group."""
    put_called = False

    def on_put(url, body, **kwargs):
        nonlocal put_called
        assert body == HBFW_REMOVE_RULE_GROUP_PUT_REQUEST
        put_called = True
        return copy.deepcopy(HBFW_REMOVE_RULE_GROUP_PUT_RESPONSE)

    cbcsdk_mock.mock_request('GET', '/policyservice/v1/orgs/test/policies/1492/configs/presentation',
                             POLICY_CONFIG_PRESENTATION)
    cbcsdk_mock.mock_request('PUT', '/policyservice/v1/orgs/test/policies/1492/rule_configs/host_based_firewall',
                             on_put)
    api = cbcsdk_mock.api
    policy = Policy(api, 1492, copy.deepcopy(FULL_POLICY_5), False, True)
    rule_config = policy.host_based_firewall_rule_config
    result_groups = [group for group in rule_config.rule_groups if group.name == "Isolate"]
    assert len(result_groups) == 1
    result_groups[0].remove()
    rule_config.save()
    assert put_called
    result_groups = rule_config.rule_groups
    assert len(result_groups) == 1
    assert result_groups[0].name == "Crapco_firewall"
