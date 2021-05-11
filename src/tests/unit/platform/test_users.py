"""Tests for the User object of the CBC SDK"""
import copy

import pytest
import logging
from cbc_sdk.platform import User
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError, ObjectNotFoundError, ServerError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_users import (GET_USERS_RESP, GET_USERS_AFTER_CREATE_RESP,
                                                     GET_USERS_AFTER_BULK1_RESP, GET_USERS_AFTER_BULK2_RESP,
                                                     EXPECT_USER_ADD, EXPECT_USER_ADD_SMALL, EXPECT_USER_ADD_V1,
                                                     EXPECT_USER_ADD_V2, EXPECT_USER_ADD_BULK1, EXPECT_USER_ADD_BULK2,
                                                     USER_ADD_SUCCESS_RESP, USER_ADD_FAILURE_RESP)
from tests.unit.fixtures.platform.mock_grants import (DETAILS_GRANT1, EXPECT_CHANGE_ROLE_GRANT1,
                                                      DETAILS_GRANT2, EXPECT_CHANGE_ROLE_GRANT2A,
                                                      EXPECT_CHANGE_ROLE_GRANT2B, EXPECT_DISABLE_ALL_GRANT2,
                                                      DETAILS_GRANT3, PROFILE_TEMPLATES_A, EXPECT_ADD_PROFILES_3A)


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

def test_list_all_users(cbcsdk_mock):
    """Tests listing all users for an org."""
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', GET_USERS_RESP)
    api = cbcsdk_mock.api
    list_users = list(api.select(User))
    assert len(list_users) == 5
    assert list_users[0].last_name == 'Mercer'
    assert list_users[1].login_name == 'mreynolds@browncoats.org'
    assert list_users[2].email == 'djackson@stargate-command.af.mil'
    assert list_users[3].phone == '714-555-4567'
    assert list_users[4].first_name == 'Beckett'


def test_list_all_users_async(cbcsdk_mock):
    """Tests listing all users for an org with an async query."""
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', GET_USERS_RESP)
    api = cbcsdk_mock.api
    future = api.select(User).execute_async()
    list_users = future.result()
    assert len(list_users) == 5
    assert list_users[0].last_name == 'Mercer'
    assert list_users[1].login_name == 'mreynolds@browncoats.org'
    assert list_users[2].email == 'djackson@stargate-command.af.mil'
    assert list_users[3].phone == '714-555-4567'
    assert list_users[4].first_name == 'Beckett'


def test_get_and_modify_user(cbcsdk_mock):
    """Tests retrieving and modifying a user."""
    def check_put(url, body, **kwargs):
        assert body['login_id'] == 6942
        assert body['login_name'] == 'jsheridan@babylon5.com'
        assert body['email'] == 'jsheridan@zhadum.net'
        return None

    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', GET_USERS_RESP)
    cbcsdk_mock.mock_request('PUT', '/appservices/v6/orgs/test/users/6942', check_put)
    api = cbcsdk_mock.api
    user = api.select(User, 6942)
    assert user.last_name == 'Sheridan'
    assert user.first_name == 'John'
    assert user.login_name == 'jsheridan@babylon5.com'
    assert user.email == 'jsheridan@babylon5.com'
    assert user.urn == 'psc:user:test:6942'
    user.email = 'jsheridan@zhadum.net'
    user.save()
    assert user.last_name == 'Sheridan'
    assert user.first_name == 'John'
    assert user.login_name == 'jsheridan@babylon5.com'
    assert user.email == 'jsheridan@zhadum.net'


def test_get_and_delete_user(cbcsdk_mock):
    """Tests retrieving and deleting a user."""
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', GET_USERS_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/users/3978', None)
    api = cbcsdk_mock.api
    user = api.select(User, 3978)
    assert user.last_name == 'Mariner'
    assert user.first_name == 'Beckett'
    assert user.login_name == 'bmariner@cerritos.starfleet.mil'
    assert user.email == 'bmariner@cerritos.starfleet.mil'
    assert user.urn == 'psc:user:test:3978'
    user.delete()


def test_get_user_and_reset_googleauth(cbcsdk_mock):
    """Tests retrieving a user and resetting Google authentication."""
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', GET_USERS_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/users/4338/google-auth', None)
    api = cbcsdk_mock.api
    user = api.select(User, 4338)
    assert user.last_name == 'Jackson'
    assert user.first_name == 'Daniel'
    assert user.login_name == 'djackson@stargate-command.af.mil'
    assert user.email == 'djackson@stargate-command.af.mil'
    assert user.urn == 'psc:user:test:4338'
    user.reset_google_authenticator_registration()


def test_get_nonexistent_user(cbcsdk_mock):
    """Test retrieving a nonexistent user."""
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', GET_USERS_RESP)
    api = cbcsdk_mock.api
    with pytest.raises(ObjectNotFoundError):
        api.select(User, 999)


def test_unsupported_create_by_update(cb):
    """Attempt to create a user by just creating one and saving it, which doesn't work."""
    user = User(cb, None)
    user.last_name = 'Rios'
    user.first_name = 'Cristobal'
    user.login_name = 'rios@la-sirena.net'
    user.email = 'rios@la-sirena.net'
    with pytest.raises(ApiError):
        user.save()


def test_create_user(cbcsdk_mock):
    """Test creating a user."""
    post_made = False

    def check_post(uri, body, **kwargs):
        assert body == EXPECT_USER_ADD
        nonlocal post_made
        post_made = True
        return USER_ADD_SUCCESS_RESP

    def check_get(uri, query_params, default):
        nonlocal post_made
        assert post_made
        return GET_USERS_AFTER_CREATE_RESP

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/users', check_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', check_get)
    api = cbcsdk_mock.api
    builder = User.create(api).set_email('rios@la-sirena.net').set_role('psc:role:test:APP_SERVICE_ROLE')
    builder.set_first_name('Cristobal').set_last_name('Rios')
    builder.add_grant_profile(['psc:org:test2'], ['psc:role:test2:DUMMY'])
    builder.add_grant_profile(['test3'], ['psc:role:test3:DUMMY'])
    user = builder.build()
    assert post_made
    assert user.last_name == 'Rios'
    assert user.first_name == 'Cristobal'
    assert user.login_name == 'rios@la-sirena.net'
    assert user.email == 'rios@la-sirena.net'


TEMPLATE1 = {
    "email_id": "rios@la-sirena.net",
    "role_urn": "psc:role:test:APP_SERVICE_ROLE",
    "first_name": "Cristobal",
    "last_name": "Rios",
}

TEMPLATE2 = {
    "email_id": "rios@la-sirena.net",
    "first_name": "Cristobal",
    "last_name": "Rios",
    "profiles": [
        {
            'orgs': {
                'allow': ['psc:org:test2']
            },
            'roles': ['psc:role:test2:DUMMY']
        }
    ]
}


@pytest.mark.parametrize('template, response', [
    (TEMPLATE1, EXPECT_USER_ADD_V1),
    (TEMPLATE2, EXPECT_USER_ADD_V2)
])
def test_create_user_from_template(cbcsdk_mock, template, response):
    """Test creating a user from a template."""
    post_made = False

    def check_post(uri, body, **kwargs):
        nonlocal response, post_made
        assert body == response
        post_made = True
        return USER_ADD_SUCCESS_RESP

    def check_get(uri, query_params, default):
        nonlocal post_made
        assert post_made
        return GET_USERS_AFTER_CREATE_RESP

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/users', check_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', check_get)
    api = cbcsdk_mock.api
    user = User.create(api, template)
    assert post_made
    assert user.last_name == 'Rios'
    assert user.first_name == 'Cristobal'
    assert user.login_name == 'rios@la-sirena.net'
    assert user.email == 'rios@la-sirena.net'


def test_create_user_fails(cbcsdk_mock):
    """Test a failure mode on creating a user."""
    def check_post(uri, body, **kwargs):
        assert body == EXPECT_USER_ADD_SMALL
        return USER_ADD_FAILURE_RESP

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/users', check_post)
    api = cbcsdk_mock.api
    builder = User.create(api).set_email('rios@la-sirena.net').set_role('psc:role:test:APP_SERVICE_ROLE')
    builder.set_first_name('Cristobal').set_last_name('Rios')
    builder.add_grant_profile(['psc:org:test2'], ['psc:role:test2:DUMMY'])
    with pytest.raises(ServerError):
        builder.build()


def test_bulk_create(cbcsdk_mock):
    """Tests the User.bulk_create API."""
    count_posts = 0
    count_gets = 0

    def check_post(uri, body, **kwargs):
        nonlocal count_posts
        rc = None
        if count_posts == 0:
            assert body == EXPECT_USER_ADD_BULK1
            rc = copy.deepcopy(USER_ADD_SUCCESS_RESP)
            rc['login_id'] = 8600
        elif count_posts == 1:
            assert body == EXPECT_USER_ADD_BULK2
            rc = copy.deepcopy(USER_ADD_SUCCESS_RESP)
            rc['login_id'] = 8601
        else:
            pytest.fail(f"invalid count_posts value {count_posts}")
        count_posts = count_posts + 1
        return rc

    def check_get(uri, query_params, default):
        nonlocal count_posts, count_gets
        rc = None
        if count_posts == 1:
            assert count_gets == 0
            rc = GET_USERS_AFTER_BULK1_RESP
        elif count_posts == 2:
            assert count_gets == 1
            rc = GET_USERS_AFTER_BULK2_RESP
        else:
            pytest.fail(f"invalid count_posts value {count_posts}")
        count_gets = count_gets + 1
        return rc

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/users', check_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', check_get)
    api = cbcsdk_mock.api
    bulk_templates = [
        {
            "email_id": "burnham@discovery.starfleet.mil",
            "first_name": "Michael",
            "last_name": "Burnham"
        },
        {
            "email_id": "scully@fbi.gov",
            "first_name": "Dana",
            "last_name": "Scully",
            "profiles": [
                {
                    'orgs': {
                        'allow': ['psc:org:test2']
                    },
                    'roles': ['psc:role:test2:DUMMY']
                }
            ]
        }
    ]
    profile_templates = [
        {
            'orgs': {
                'allow': ['psc:org:testX']
            },
            'roles': ['psc:role:testX:DUMMY']
        }
    ]
    users = User.bulk_create(api, bulk_templates, profile_templates)
    assert count_posts == 2
    assert count_gets == 2
    assert users[0].last_name == 'Burnham'
    assert users[0].first_name == 'Michael'
    assert users[0].login_name == 'burnham@discovery.starfleet.mil'
    assert users[0].email == 'burnham@discovery.starfleet.mil'
    assert users[1].last_name == 'Scully'
    assert users[1].first_name == 'Dana'
    assert users[1].login_name == 'scully@fbi.gov'
    assert users[1].email == 'scully@fbi.gov'


@pytest.mark.parametrize('login_id, grant_get, expect_put', [
    (3934, DETAILS_GRANT2, EXPECT_DISABLE_ALL_GRANT2),
    (3911, DETAILS_GRANT1, None)
])
def test_disable_all_access(cbcsdk_mock, login_id, grant_get, expect_put):
    """Tests the User.disable_all_access method"""
    put_was_called = False

    def on_put(url, body, **kwargs):
        nonlocal put_was_called, expect_put
        assert expect_put is not None
        assert body == expect_put
        put_was_called = True
        return expect_put

    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', GET_USERS_RESP)
    cbcsdk_mock.mock_request('POST', '/access/v2/grants/_fetch', {'additionalProp1': [copy.deepcopy(grant_get)]})
    cbcsdk_mock.mock_request('PUT', f'/access/v2/orgs/test/grants/psc:user:test:{login_id}', on_put)
    api = cbcsdk_mock.api
    user = api.select(User).user_ids([login_id]).one()
    user.disable_all_access()
    if expect_put is None:
        assert not put_was_called
    else:
        assert put_was_called


@pytest.mark.parametrize('user_email, user_loginid, grant_get, new_role, org, expect_put', [
    ('emercer@orville.planetary-union.net', 3911, DETAILS_GRANT1, 'psc:role:test:NEW_ROLE', None,
     EXPECT_CHANGE_ROLE_GRANT1),
    ('emercer@orville.planetary-union.net', 3911, DETAILS_GRANT1, 'psc:role:test:APP_SERVICE_ROLE', None, None),
    ('mreynolds@browncoats.org', 3934, DETAILS_GRANT2, 'psc:role:test:ALPHA_ROLE', None,
     EXPECT_CHANGE_ROLE_GRANT2A),
    ('mreynolds@browncoats.org', 3934, DETAILS_GRANT2, 'psc:role:test:ALPHA_ROLE', 'psc:org:test3',
     EXPECT_CHANGE_ROLE_GRANT2B),
    ('mreynolds@browncoats.org', 3934, DETAILS_GRANT2, 'psc:role:test:ALPHA_ROLE', 'test3',
     EXPECT_CHANGE_ROLE_GRANT2B),
    ('mreynolds@browncoats.org', 3934, DETAILS_GRANT2, 'psc:role::SECOPS_ROLE_MANAGER', None, None)
])
def test_change_role(cbcsdk_mock, user_email, user_loginid, grant_get, new_role, org, expect_put):
    """Tests the User.change_role method"""
    put_was_called = False

    def on_put(url, body, **kwargs):
        nonlocal expect_put, put_was_called
        assert expect_put is not None
        assert body == expect_put
        put_was_called = True
        return expect_put

    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', GET_USERS_RESP)
    cbcsdk_mock.mock_request('POST', '/access/v2/grants/_fetch', {'additionalProp1': [copy.deepcopy(grant_get)]})
    cbcsdk_mock.mock_request('PUT', f'/access/v2/orgs/test/grants/psc:user:test:{user_loginid}', on_put)
    api = cbcsdk_mock.api
    user = api.select(User).email_addresses([user_email]).one()
    user.change_role(new_role, org)
    if expect_put is None:
        assert not put_was_called
    else:
        assert put_was_called


def fixup_profile_uuids(expected, actual):
    """Auxiliary function to fix the profile UUIDs in an "expected" profile return."""
    work = copy.deepcopy(expected)
    if 'profiles' not in work:
        work['profiles'] = []
    if 'profiles' in actual:
        for index, profile in enumerate(actual['profiles']):
            if index >= len(work['profiles']) or 'profile_uuid' not in profile:
                continue
            if 'profile_uuid' not in work['profiles'][index]:
                work['profiles'][index]['profile_uuid'] = profile['profile_uuid']
    return work


def template_matches(profile, template):
    if set(profile['roles']) != set(template['roles']):
        return False
    if set(profile['orgs']['allow']) != set(template['orgs']['allow']):
        return False
    return True


@pytest.mark.parametrize('login_id, grant_get, new_profiles, expect_put, expect_new_profs', [
    (4338, DETAILS_GRANT3, PROFILE_TEMPLATES_A, EXPECT_ADD_PROFILES_3A, 1)  # NOTWORKINGYET
])
def test_add_profiles(cbcsdk_mock, login_id, grant_get, new_profiles, expect_put, expect_new_profs):
    put_was_called = False
    new_profile_count = 0

    def on_put(url, body, **kwargs):
        nonlocal expect_put, put_was_called
        assert expect_put is not None
        fixed_expect_put = fixup_profile_uuids(expect_put, body)
        assert body == fixed_expect_put
        put_was_called = True
        return fixed_expect_put

    def on_profile_post(url, body, **kwargs):
        nonlocal new_profiles, new_profile_count
        matched = False
        for template in new_profiles:
            matched = template_matches(body, template) or matched
        assert matched
        new_profile_count = new_profile_count + 1
        return body

    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/users', GET_USERS_RESP)
    cbcsdk_mock.mock_request('POST', '/access/v2/grants/_fetch', {'additionalProp1': [copy.deepcopy(grant_get)]})
    cbcsdk_mock.mock_request('POST', f'/access/v2/orgs/test/grants/psc:user:test:{login_id}/profiles', on_profile_post)
    cbcsdk_mock.mock_request('PUT', f'/access/v2/orgs/test/grants/psc:user:test:{login_id}', on_put)
    api = cbcsdk_mock.api
    user = api.select(User).user_ids([login_id]).one()
    user.add_profiles(new_profiles)
    if expect_put is None:
        assert not put_was_called
    else:
        assert put_was_called
    assert expect_new_profs == new_profile_count
