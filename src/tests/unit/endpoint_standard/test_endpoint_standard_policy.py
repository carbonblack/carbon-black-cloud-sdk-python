"""Testing Policy object of cbc_sdk.endpoint_standard"""

import pytest
import logging
from cbc_sdk.endpoint_standard import Policy, Query
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_policy import (POLICY_GET_RESP,
                                                               POLICY_POST_RULE_RESP,
                                                               POLICY_GET_WITH_NEW_RULE_RESP,
                                                               POLICY_MODIFY_RULE_RESP,
                                                               POLICY_GET_WITH_MODIFIED_RULE_RESP,
                                                               POLICY_DELETE_RULE_RESP,
                                                               POLICY_GET_WITH_DELETED_RULE_RESP)

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

def test_policy_select_modify(cbcsdk_mock):
    """Testing Policy Querying with .select(Policy, `policy_id`) and add/del rules"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    api = cbcsdk_mock.api
    policy = api.select(Policy, 30241)
    assert policy.id == 30241
    policy.refresh()

    new_rule = {"action": "DENY", "application": {"type": "NAME_PATH", "value": "my_path_test"},
                "operation": "RUN", "required": True}
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    rules = policy.rules.values()
    rule_ids = [rule.pop('id') for rule in rules]
    rules_without_ids = rules
    assert new_rule not in rules_without_ids

    cbcsdk_mock.mock_request("POST", "/integrationServices/v3/policy/30241/rule", POLICY_POST_RULE_RESP)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_WITH_NEW_RULE_RESP)
    policy.add_rule(new_rule)
    rules = policy.rules.values()
    rule_ids = [rule.pop('id') for rule in rules]
    new_rule_id = rule_ids[-1]
    rules_without_ids = rules
    assert new_rule in rules_without_ids

    modified_rule = {"action": "IGNORE", "application": {"type": "NAME_PATH", "value": "new_test_path"},
                     "operation": "RUN", "required": True, "id": new_rule_id}
    cbcsdk_mock.mock_request("PUT", "/integrationServices/v3/policy/30241/rule/22", POLICY_MODIFY_RULE_RESP)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_WITH_MODIFIED_RULE_RESP)
    policy.replace_rule(new_rule_id, modified_rule)
    rules = policy.rules.values()
    modified_rule.pop("id")
    rule_ids = [rule.pop('id') for rule in rules]
    rules_without_ids = rules
    assert modified_rule in rules_without_ids

    cbcsdk_mock.mock_request("DELETE", "/integrationServices/v3/policy/30241/rule/22", POLICY_DELETE_RULE_RESP)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_WITH_DELETED_RULE_RESP)
    policy.delete_rule(rule_ids[-1])
    rules = policy.rules.values()
    rule_ids = [rule.pop('id') for rule in rules]
    rules_without_ids = rules
    assert modified_rule not in rules_without_ids


def test_policy_select(cbcsdk_mock):
    """Testing Policy Querying with .select(Policy)"""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    api = cbcsdk_mock.api
    policy = api.select(Policy, 30241)
    assert isinstance(policy, Policy)
    assert policy.id == 30241
    assert policy.name == "Lyon_test"


def test_policy_query_implementation(cbcsdk_mock):
    """Testing Policy._query_implementation."""
    policy = Policy(cbcsdk_mock.api)
    assert isinstance(policy._query_implementation(cbcsdk_mock.api), Query)
