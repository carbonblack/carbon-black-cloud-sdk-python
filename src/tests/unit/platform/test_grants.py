"""Tests for the Grant and Profile objects of the CBC SDK"""

import pytest
import logging
import copy
from cbc_sdk.platform import Grant
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError, NonQueryableModel
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_grants import (GET_GRANT_RESP, PUT_GRANT_RESP, POST_GRANT_RESP,
                                                      POST_PROFILE_IN_GRANT_RESP, POST_PROFILE_IN_GRANT_RESP_2,
                                                      PUT_PROFILE_RESP, DELETE_PROFILE_RESP, DELETE_GRANT_RESP,
                                                      QUERY_GRANT_RESP, PERMITTED_ROLES_RESP)

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
    grant = api.select(Grant, 'psc:user:12345678:ABCDEFGH')
    assert grant.principal == 'psc:user:12345678:ABCDEFGH'
    assert grant.roles == ["psc:role::SECOPS_ROLE_MANAGER", "psc:role:test:APP_SERVICE_ROLE"]
    assert len(grant.profiles_) == 1
    assert grant.org_ref == 'psc:org:test'
    profile = grant.profiles_[0]
    assert profile.profile_uuid == 'c57ba255-1736-4bfa-a59d-c54bb97a41d6'
    assert profile.orgs['allow'] == ["psc:org:test2"]
    assert profile.allowed_orgs == ["psc:org:test2"]
    assert profile.roles == ["psc:role::SECOPS_ROLE_MANAGER"]
    assert profile.matches_template({'roles': ["psc:role::SECOPS_ROLE_MANAGER"],
                                     'orgs': {'allow': ["psc:org:test2"]}})
    assert not profile.matches_template({'roles': ["psc:role::NONEXISTENT_ROLE"],
                                         'orgs': {'allow': ["psc:org:test2"]}})
    assert not profile.matches_template({'roles': ["psc:role::SECOPS_ROLE_MANAGER"],
                                         'orgs': {'allow': ["psc:org:notexist"]}})
    with pytest.raises(ApiError):
        profile.refresh()  # these can't be refreshed
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
    grant_builder = Grant.create(api, org_key='ABC12345', userid='DEF67890')
    grant_builder.set_org('psc:org:test').set_roles(["psc:role::SECOPS_ROLE_MANAGER"]).set_principal_name('Doug Jones')
    profile = grant_builder.create_profile().add_org("test2").add_role("psc:role::SECOPS_ROLE_MANAGER").build()
    grant = grant_builder.build()
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
    grant_builder = Grant.create(api, org_key='ABC12345', userid='DEF67890')
    grant_builder.set_org('test').add_role("psc:role::SECOPS_ROLE_MANAGER").set_principal_name('Doug Jones')
    profile_builder = grant_builder.create_profile().set_orgs(["test2"]).set_roles(["psc:role::SECOPS_ROLE_MANAGER"])
    profile = profile_builder.set_disabled(False).build()
    grant = grant_builder.build()
    assert grant.roles == ["psc:role::SECOPS_ROLE_MANAGER"]
    assert profile.orgs['allow'] == ["psc:org:test2"]


def test_create_new_grant_alt2(cbcsdk_mock):
    """Test creation of a grant and the profile inside it with more options."""
    def respond_to_profile_grant(url, body, **kwargs):
        ret = copy.deepcopy(POST_PROFILE_IN_GRANT_RESP_2)
        ret['profile_uuid'] = body['profile_uuid']
        return ret

    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants', POST_GRANT_RESP)
    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants/psc:user:ABC12345:DEF67890/profiles',
                             respond_to_profile_grant)
    api = cbcsdk_mock.api
    grant_builder = Grant.create(api, org_key='ABC12345', userid='DEF67890')
    grant_builder.set_org('test').add_role("psc:role::SECOPS_ROLE_MANAGER").set_principal_name('Doug Jones')
    profile_builder = grant_builder.create_profile().set_orgs(["test2"]).set_roles(["psc:role::SECOPS_ROLE_MANAGER"])
    profile = profile_builder.set_disabled(True).set_expiration('20211031T12:34:56').build()
    grant = grant_builder.build()
    assert grant.roles == ["psc:role::SECOPS_ROLE_MANAGER"]
    assert profile.orgs['allow'] == ["psc:org:test2"]
    assert profile.conditions['expiration'] == '20211031T12:34:56'
    assert profile.conditions['disabled']


def test_create_new_grant_alt3(cbcsdk_mock):
    """Test creation of a grant and the profile inside it with more options in a different way."""
    def respond_to_profile_grant(url, body, **kwargs):
        ret = copy.deepcopy(POST_PROFILE_IN_GRANT_RESP_2)
        ret['profile_uuid'] = body['profile_uuid']
        return ret

    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants', POST_GRANT_RESP)
    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants/psc:user:ABC12345:DEF67890/profiles',
                             respond_to_profile_grant)
    api = cbcsdk_mock.api
    grant_builder = Grant.create(api, org_key='ABC12345', userid='DEF67890')
    grant_builder.set_org('test').add_role("psc:role::SECOPS_ROLE_MANAGER").set_principal_name('Doug Jones')
    profile_builder = grant_builder.create_profile().set_orgs(["test2"]).set_roles(["psc:role::SECOPS_ROLE_MANAGER"])
    profile = profile_builder.set_conditions({'expiration': '20211031T12:34:56', 'disabled': True}).build()
    grant = grant_builder.build()
    assert grant.roles == ["psc:role::SECOPS_ROLE_MANAGER"]
    assert profile.orgs['allow'] == ["psc:org:test2"]
    assert profile.conditions['expiration'] == '20211031T12:34:56'
    assert profile.conditions['disabled']


def test_create_new_grant_without_keywords(cbcsdk_mock):
    """Tests that Grant.create fails if you don't supply the keyword arguments."""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError):
        Grant.create(api, org_key='ABC12345')
    with pytest.raises(ApiError):
        Grant.create(api, userid='DEF67890')
    with pytest.raises(ApiError):
        Grant.create(api)


def test_create_grant_from_template(cbcsdk_mock):
    """Test creation of a new grant from a template."""
    def respond_to_profile_grant(url, body, **kwargs):
        ret = copy.deepcopy(POST_PROFILE_IN_GRANT_RESP)
        ret['profile_uuid'] = body['profile_uuid']
        return ret

    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants', POST_GRANT_RESP)
    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants/psc:user:ABC12345:DEF67890/profiles',
                             respond_to_profile_grant)
    api = cbcsdk_mock.api
    grant_template = {
        "principal": 'psc:user:ABC12345:DEF67890',
        "roles": [
            "psc:role::SECOPS_ROLE_MANAGER"
        ],
        "profiles": [
            {
                "orgs": {
                    "allow": [
                        "psc:org:test2"
                    ]
                },
                "roles": [
                    "psc:role::SECOPS_ROLE_MANAGER"
                ],
                "conditions": {
                    "expiration": 0,
                    "disabled": False
                }
            }
        ],
        "org_ref": 'psc:org:test',
        "principal_name": 'Doug Jones'
    }
    grant = Grant.create(api, grant_template)
    assert grant.roles == ["psc:role::SECOPS_ROLE_MANAGER"]
    profile = grant.profiles_[0]
    assert profile.orgs['allow'] == ["psc:org:test2"]


def test_create_grant_from_template_without_principal(cbcsdk_mock):
    """Test that creating a grant from a template fails if the template does not specify the principal."""
    api = cbcsdk_mock.api
    grant_template = {
        "roles": [
            "psc:role::SECOPS_ROLE_MANAGER"
        ],
        "profiles": [
            {
                "orgs": {
                    "allow": [
                        "psc:org:test2"
                    ]
                },
                "roles": [
                    "psc:role::SECOPS_ROLE_MANAGER"
                ],
                "conditions": {
                    "expiration": 0,
                    "disabled": False
                }
            }
        ],
        "org_ref": 'psc:org:test',
        "principal_name": 'Doug Jones'
    }
    with pytest.raises(ApiError):
        Grant.create(api, grant_template)


def test_create_new_grant_with_profile_template(cbcsdk_mock):
    """Tests creating a new grant via builder, with a profile created via a template."""
    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants', POST_GRANT_RESP)
    api = cbcsdk_mock.api
    grant_builder = Grant.create(api, org_key='ABC12345', userid='DEF67890')
    grant_builder.set_org('psc:org:test').set_roles(["psc:role::SECOPS_ROLE_MANAGER"]).set_principal_name('Doug Jones')
    profile_template = {
        "profile_uuid": "to-be-deleted",  # this member should be explicitly stripped by create_profile()
        "orgs": {
            "allow": [
                "psc:org:test2"
            ]
        },
        "roles": [
            "psc:role::SECOPS_ROLE_MANAGER"
        ],
        "conditions": {
            "expiration": 0,
            "disabled": False
        }
    }
    profile = grant_builder.create_profile(profile_template)
    grant = grant_builder.build()
    assert grant.roles == ["psc:role::SECOPS_ROLE_MANAGER"]
    assert profile.orgs['allow'] == ["psc:org:test2"]


def test_create_profile_on_existing_grant(cbcsdk_mock):
    """Test the creation of a new profile within a grant via a builder."""
    def respond_to_profile_grant(url, body, **kwargs):
        ret = copy.deepcopy(POST_PROFILE_IN_GRANT_RESP)
        return ret

    cbcsdk_mock.mock_request('GET', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH', GET_GRANT_RESP)
    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH/profiles',
                             respond_to_profile_grant)
    api = cbcsdk_mock.api
    grant = api.select(Grant, 'psc:user:12345678:ABCDEFGH')
    profile = grant.create_profile().add_org("test2").add_role("psc:role::SECOPS_ROLE_MANAGER").build()
    assert profile.orgs['allow'] == ["psc:org:test2"]


def test_create_profile_from_template(cbcsdk_mock):
    """Test the creation of a new profile within a grant via a template."""
    def respond_to_profile_grant(url, body, **kwargs):
        ret = copy.deepcopy(POST_PROFILE_IN_GRANT_RESP)
        return ret

    cbcsdk_mock.mock_request('GET', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH', GET_GRANT_RESP)
    cbcsdk_mock.mock_request('POST', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH/profiles',
                             respond_to_profile_grant)
    api = cbcsdk_mock.api
    grant = Grant(api, 'psc:user:12345678:ABCDEFGH')
    template = {
        "profile_uuid": "to-be-deleted",  # this member should be explicitly stripped by create_profile()
        "orgs": {
            "allow": [
                "psc:org:test2"
            ],
        },
        "roles": [
            "psc:role::SECOPS_ROLE_MANAGER"
        ],
        "conditions": {
            "expiration": 0,
            "disabled": False
        }
    }
    profile = grant.create_profile(template)
    assert profile.orgs['allow'] == ["psc:org:test2"]


def test_modify_profile_within_grant(cbcsdk_mock):
    """Test the modification of a profile within a grant."""
    cbcsdk_mock.mock_request('GET', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH', GET_GRANT_RESP)
    cbcsdk_mock.mock_request('PUT', '/access/v2/orgs/test/grants/psc:user:12345678:ABCDEFGH/profiles/c57ba255-1736-4bfa-a59d-c54bb97a41d6',  # noqa: E501
                             PUT_PROFILE_RESP)
    api = cbcsdk_mock.api
    grant = api.select(Grant, 'psc:user:12345678:ABCDEFGH')
    profile = grant.profiles_[0]
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
    grant = api.select(Grant, 'psc:user:12345678:ABCDEFGH')
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


def test_unsupported_query_profiles(cb):
    """Make sure trying to do a direct query on Profile fails."""
    with pytest.raises(NonQueryableModel):
        cb.select(Grant.Profile)


def test_get_permitted_roles(cbcsdk_mock):
    """Test the get_permitted_roles function."""
    cbcsdk_mock.mock_request('GET', '/access/v3/orgs/test/principals/1234/roles/permitted?type=USER',
                             PERMITTED_ROLES_RESP)
    api = cbcsdk_mock.api
    roles = Grant.get_permitted_role_urns(api)
    assert set(roles) == {"psc:role::ALPHA", "psc:role::BRAVO", "psc:role::CHARLIE"}
