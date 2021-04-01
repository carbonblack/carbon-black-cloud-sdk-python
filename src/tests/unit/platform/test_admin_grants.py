"""Tests for the Grant and Profile objects of the CBC SDK"""

import pytest
import logging
import copy
from cbc_sdk.platform import Grant
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_grants import (GET_GRANT_RESP, PUT_GRANT_RESP, POST_GRANT_RESP,
                                                      POST_PROFILE_IN_GRANT_RESP, GET_PROFILE_RESP, PUT_PROFILE_RESP,
                                                      DELETE_PROFILE_RESP, DELETE_GRANT_RESP, QUERY_GRANT_RESP)

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

def test_get_and_set_grant(cbcsdk_mock):
    """Tests elementary loading and saving of a grant."""
    cbcsdk_mock.mock_request('GET', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH', GET_GRANT_RESP)
    cbcsdk_mock.mock_request('PUT', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH', PUT_GRANT_RESP)
    api = cbcsdk_mock.api
    grant = Grant(api, 'psc:user:12345678:ABCDEFGH')
    assert grant.principal == 'psc:user:12345678:ABCDEFGH'
    assert grant.roles == ["psc:role::SECOPS_ROLE_MANAGER", "psc:role:test:APP_SERVICE_ROLE"]
    assert len(grant.profiles_) == 1
    assert grant.org_ref == 'psc:org:test'
    profile = grant.profiles_[0]
    assert profile.profile_uuid == 'c57ba255-1736-4bfa-a59d-c54bb97a41d6'
    assert profile.orgs['allow'] == ["psc:org:test2"]
    assert profile.roles == ["psc:role::SECOPS_ROLE_MANAGER"]
    grant.roles.append('psc:role:test:DUMMY_ROLE')
    profile.orgs['allow'].append('psc:org:test3')
    grant.touch()  # force object to be "dirty"
    grant.save()
    assert grant.roles == ["psc:role::SECOPS_ROLE_MANAGER", "psc:role:test:APP_SERVICE_ROLE",
                           'psc:role:test:DUMMY_ROLE']
    assert profile.orgs['allow'] == ["psc:org:test2", "psc:org:test3"]


def test_create_new_grant(cbcsdk_mock):
    """Test creation of a grant and the profile within the grant."""
    def respond_to_profile_grant(url, body, **kwargs):
        ret = copy.deepcopy(POST_PROFILE_IN_GRANT_RESP)
        ret['profile_uuid'] = body['profile_uuid']
        return ret

    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants', POST_GRANT_RESP)
    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants/psc:user:ABC12345:DEF67890/profiles',
                             respond_to_profile_grant)
    api = cbcsdk_mock.api
    grant = Grant.new_grant(api, 'psc:user:ABC12345:DEF67890')
    grant.roles = ["psc:role::SECOPS_ROLE_MANAGER"]
    grant.org_ref = 'psc:org:test'
    grant.principal_name = 'Doug Jones'
    builder = grant.new_profile().add_allow("psc:org:test2")
    profile = builder.add_role("psc:role::SECOPS_ROLE_MANAGER").build()
    grant.save()
    assert grant.roles == ["psc:role::SECOPS_ROLE_MANAGER"]
    assert profile.orgs['allow'] == ["psc:org:test2"]


def test_create_new_grant_alt1(cbcsdk_mock):
    """Test creation of a grant and the profile within the grant, using alternate strategies for the ProfileBuilder."""
    def respond_to_profile_grant(url, body, **kwargs):
        ret = copy.deepcopy(POST_PROFILE_IN_GRANT_RESP)
        ret['profile_uuid'] = body['profile_uuid']
        return ret

    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants', POST_GRANT_RESP)
    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants/psc:user:ABC12345:DEF67890/profiles',
                             respond_to_profile_grant)
    api = cbcsdk_mock.api
    grant = Grant.new_grant(api, 'psc:user:ABC12345:DEF67890')
    grant.roles = ["psc:role::SECOPS_ROLE_MANAGER"]
    grant.org_ref = 'psc:org:test'
    grant.principal_name = 'Doug Jones'
    builder = grant.new_profile().set_allowed_orgs(["psc:org:test2"]).set_roles(["psc:role::SECOPS_ROLE_MANAGER"])
    profile = builder.set_disabled(False).set_can_manage(False).build()
    grant.save()
    assert grant.roles == ["psc:role::SECOPS_ROLE_MANAGER"]
    assert profile.orgs['allow'] == ["psc:org:test2"]


def test_create_new_grant_fail(cb):
    """Test failure of the creation of a new grant."""
    grant = Grant(cb, None)
    grant.roles = ["psc:role::SECOPS_ROLE_MANAGER"]
    grant.org_ref = 'psc:org:test'
    with pytest.raises(ApiError):
        grant.save()


def test_modify_profile_within_grant(cbcsdk_mock):
    """Test the modification of a profile within a grant."""
    cbcsdk_mock.mock_request('GET', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH', GET_GRANT_RESP)
    cbcsdk_mock.mock_request('GET', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH/profiles/c57ba255-1736-4bfa-a59d-c54bb97a41d6',  # noqa: E501
                             GET_PROFILE_RESP)
    cbcsdk_mock.mock_request('PUT', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH/profiles/c57ba255-1736-4bfa-a59d-c54bb97a41d6',  # noqa: E501
                             PUT_PROFILE_RESP)
    api = cbcsdk_mock.api
    grant = Grant(api, 'psc:user:12345678:ABCDEFGH')
    profile = grant.profiles_[0]
    profile.refresh()
    profile.orgs['allow'].append('psc:org:test22')
    profile.touch()
    profile.save()
    assert profile.orgs['allow'] == ["psc:org:test2", 'psc:org:test22']


def test_delete_profile_within_grant(cbcsdk_mock):
    """Test the deletion of a profile within a grant."""
    cbcsdk_mock.mock_request('GET', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH', GET_GRANT_RESP)
    cbcsdk_mock.mock_request('DELETE', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH/profiles/c57ba255-1736-4bfa-a59d-c54bb97a41d6',  # noqa: E501
                             DELETE_PROFILE_RESP)
    api = cbcsdk_mock.api
    grant = Grant(api, 'psc:user:12345678:ABCDEFGH')
    profile = grant.profiles_[0]
    profile.delete()
    assert profile.conditions['disabled'] is True


def test_delete_grant(cbcsdk_mock):
    """Test the deletion of a grant."""
    cbcsdk_mock.mock_request('GET', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH', GET_GRANT_RESP)
    cbcsdk_mock.mock_request('DELETE', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH', DELETE_GRANT_RESP)
    api = cbcsdk_mock.api
    grant = Grant(api, 'psc:user:12345678:ABCDEFGH')
    grant.delete()
    assert grant.revoked is True


def test_query_grants(cbcsdk_mock):
    """Test bulk querying for grants."""
    cbcsdk_mock.mock_request('POST', '/access/v2/grants/_fetch', QUERY_GRANT_RESP)
    api = cbcsdk_mock.api
    query = api.select(Grant).add_principal('psc:user:12345678:ABCDEFGH', 'psc:org:test')
    query.add_principal('psc:user:87654321:HGFEDCBA', 'psc:org:test')
    assert query._count() == 2
    results = list(query)
    assert results[0].principal == 'psc:user:12345678:ABCDEFGH'
    assert results[0].principal_name == 'J. Random Nerd'
    assert results[1].principal == 'psc:user:87654321:HGFEDCBA'
    assert results[1].principal_name == 'Sally Shears'


def test_query_grants_async(cbcsdk_mock):
    """Test bulk querying for grants with an async query."""
    cbcsdk_mock.mock_request('POST', '/access/v2/grants/_fetch', QUERY_GRANT_RESP)
    api = cbcsdk_mock.api
    query = api.select(Grant).add_principal('psc:user:12345678:ABCDEFGH', 'psc:org:test')
    future = query.add_principal('psc:user:87654321:HGFEDCBA', 'psc:org:test').execute_async()
    results = future.result()
    assert results[0].principal == 'psc:user:12345678:ABCDEFGH'
    assert results[0].principal_name == 'J. Random Nerd'
    assert results[1].principal == 'psc:user:87654321:HGFEDCBA'
    assert results[1].principal_name == 'Sally Shears'


def test_query_grants_fail(cb):
    """Test to ensure the grant query fails if we don't supply a principal."""
    query = cb.select(Grant)
    with pytest.raises(ApiError):
        list(query)
