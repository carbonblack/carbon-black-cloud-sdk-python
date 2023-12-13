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

"""Tests of the asset groups support in the Platform API."""

import pytest
import logging
import copy
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from cbc_sdk.platform import AssetGroup, Device
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_asset_groups import (CREATE_AG_REQUEST, CREATE_AG_RESPONSE, EXISTING_AG_DATA,
                                                            UPDATE_AG_REQUEST, QUERY_REQUEST, QUERY_REQUEST_DEFAULT,
                                                            QUERY_RESPONSE, LIST_MEMBERS_RESPONSE1,
                                                            LIST_MEMBERS_RESPONSE2)
from tests.unit.fixtures.platform.mock_devices import GET_DEVICE_RESP


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

def test_create_asset_group(cbcsdk_mock):
    """Tests the Create Asset Group call."""
    posted = False

    def on_post(uri, body, **kwargs):
        nonlocal posted
        assert body == CREATE_AG_REQUEST
        posted = True
        return CREATE_AG_RESPONSE

    cbcsdk_mock.mock_request('POST', '/asset_groups/v1/orgs/test/groups', on_post)
    api = cbcsdk_mock.api
    group = AssetGroup.create_group(api, "Group Test", "Group Test Description", policy_id=7113785,
                                    query="os_version:Windows")
    assert posted
    assert group is not None
    assert group.id == '4b48a403-e371-4e3d-ae6c-8eb9080fe7ad'
    assert group.name == 'Group Test'
    assert group.description == 'Group Test Description'
    assert group.policy_id == 7113785
    assert group.query == "os_version:Windows"


def test_find_and_update_asset_group(cbcsdk_mock):
    """Tests finding and updating the asset group."""
    did_put = False

    def on_put(url, body, **kwargs):
        nonlocal did_put
        assert body == UPDATE_AG_REQUEST
        did_put = True
        return copy.deepcopy(body)

    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    cbcsdk_mock.mock_request('PUT', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             on_put)
    api = cbcsdk_mock.api
    group = api.select(AssetGroup, 'db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16')
    assert not did_put
    assert group is not None
    assert group.id == 'db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16'
    assert group.name == 'Existing Group'
    assert group.description == 'Some Description'
    assert group.policy_id == 8675309

    group.name = "Renamed Group"
    group.description = 'Change This Too'
    group.policy_id = 9001
    group.save()
    assert did_put


def test_find_and_delete_asset_group(cbcsdk_mock):
    """Tests finding and deleting the asset group."""
    did_delete = False

    def on_delete(url, body):
        nonlocal did_delete
        did_delete = True
        return CBCSDKMock.StubResponse(None, scode=200)

    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    cbcsdk_mock.mock_request('DELETE', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             on_delete)
    api = cbcsdk_mock.api
    group = api.select(AssetGroup, 'db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16')
    assert group is not None
    assert group.id == 'db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16'
    assert group.name == 'Existing Group'
    assert group.description == 'Some Description'
    assert group.policy_id == 8675309

    group.delete()
    assert did_delete


@pytest.mark.parametrize("name, polid, groupid", [
    ("Group Test", 7113785, "9b8b8d84-4a44-4a94-81ec-1f8ef52d4430"),
    (["Group Test"], [7113785], ["9b8b8d84-4a44-4a94-81ec-1f8ef52d4430"]),
])
def test_query_with_all_options(cbcsdk_mock, name, polid, groupid):
    """Tests querying for asset groups with all options set."""

    def on_post(uri, body, **kwargs):
        tbody = copy.deepcopy(body)
        if 'start' not in tbody:
            tbody['start'] = 0
        assert tbody == QUERY_REQUEST
        return QUERY_RESPONSE

    cbcsdk_mock.mock_request('POST', '/asset_groups/v1/orgs/test/groups/_search', on_post)
    api = cbcsdk_mock.api
    query = api.select(AssetGroup).where("test").add_criteria("discovered", False).add_criteria("name", name)
    query.add_criteria("policy_id", polid).add_criteria("group_id", groupid).sort_by("name", "ASC").set_rows(42)
    assert query._count() == 1
    output = list(query)
    assert len(output) == 1
    assert output[0].id == "9b8b8d84-4a44-4a94-81ec-1f8ef52d4430"
    assert output[0].name == "Group Test"
    assert output[0].description == "Group Test"
    assert output[0].policy_id == 7113785


def test_query_with_everything_default(cbcsdk_mock):
    """Tests querying for asset groups with all default options."""

    def on_post(uri, body, **kwargs):
        tbody = copy.deepcopy(body)
        if 'start' not in tbody:
            tbody['start'] = 0
        assert tbody == QUERY_REQUEST_DEFAULT
        return QUERY_RESPONSE

    cbcsdk_mock.mock_request('POST', '/asset_groups/v1/orgs/test/groups/_search', on_post)
    api = cbcsdk_mock.api
    query = api.select(AssetGroup)
    output = list(query)
    assert len(output) == 1
    assert output[0].id == "9b8b8d84-4a44-4a94-81ec-1f8ef52d4430"
    assert output[0].name == "Group Test"
    assert output[0].description == "Group Test"
    assert output[0].policy_id == 7113785


def test_query_async(cbcsdk_mock):
    """Tests async querying for asset groups."""

    def on_post(uri, body, **kwargs):
        tbody = copy.deepcopy(body)
        if 'start' not in tbody:
            tbody['start'] = 0
        assert tbody == QUERY_REQUEST
        return QUERY_RESPONSE

    cbcsdk_mock.mock_request('POST', '/asset_groups/v1/orgs/test/groups/_search', on_post)
    api = cbcsdk_mock.api
    query = api.select(AssetGroup).where("test").add_criteria("discovered", False).add_criteria("name", "Group Test")
    query.add_criteria("policy_id", 7113785).add_criteria("group_id", "9b8b8d84-4a44-4a94-81ec-1f8ef52d4430")
    query.sort_by("name", "ASC").set_rows(42)
    future = query.execute_async()
    output = future.result()
    assert len(output) == 1
    assert output[0].id == "9b8b8d84-4a44-4a94-81ec-1f8ef52d4430"
    assert output[0].name == "Group Test"
    assert output[0].description == "Group Test"
    assert output[0].policy_id == 7113785


def test_query_fail_criteria_set(cb):
    """Tests the failure of validation when setting criteria on a query."""
    query = cb.select(AssetGroup)
    with pytest.raises(ApiError):
        query.sort_by("name", "NOTADIRECTION")


def test_list_member_ids_basic(cbcsdk_mock):
    """Tests the formatting of the 'list members' call with rows and start parameters, and the basic response."""
    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16/members?rows=20&start=0',  # noqa: E501
                             LIST_MEMBERS_RESPONSE1)
    api = cbcsdk_mock.api
    group = api.select(AssetGroup, 'db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16')
    rc = group.list_member_ids(rows=20, start=0)
    assert rc == [12345678, 66760099, 42691014]


@pytest.mark.parametrize("filter_param, expected", [
    ("ALL", [12345678, 66760099, 42691014]),
    ("DYNAMIC", [12345678, 42691014]),
    ("MANUAL", [66760099])
])
def test_list_member_ids_filtering(cbcsdk_mock, filter_param, expected):
    """Tests the filter action on the list_member_ids function."""
    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16/members',
                             LIST_MEMBERS_RESPONSE1)
    api = cbcsdk_mock.api
    group = api.select(AssetGroup, 'db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16')
    rc = group.list_member_ids(filter=filter_param)
    assert rc == expected


def test_list_member_ids_invalid_filter(cbcsdk_mock):
    """Tests the "invalid filter" exception in list_member_ids."""
    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    api = cbcsdk_mock.api
    group = api.select(AssetGroup, 'db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16')
    with pytest.raises(ApiError):
        group.list_member_ids(filter="BOGUS")


def test_list_members(cbcsdk_mock):
    """Tests the device return mechanism of list_members."""
    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16/members',
                             LIST_MEMBERS_RESPONSE2)
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    api = cbcsdk_mock.api
    group = api.select(AssetGroup, 'db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16')
    rc = group.list_members()
    assert len(rc) == 1
    assert isinstance(rc[0], Device)
    assert rc[0].id == 98765


@pytest.mark.parametrize("param1, param2, expected", [
    ("12345678", 14760, ["12345678", "14760"]),
    (303873, "777000", ["303873", "777000"]),
    (None, [16, "24", 99], ["16", "24", "99"]),
    ("obviously_bogus", (12, 23, 34), ["12", "23", "34"]),
    ({4400}, {16384}, ["4400", "16384"]),
    (65536, 3.1416, ["65536", "3"])
])
def test_add_members(cbcsdk_mock, param1, param2, expected):
    """Tests the add_members API with various combinations of parameters."""
    def on_post(url, body, **kwargs):
        assert body['action'] == 'CREATE'
        assert body['external_member_ids'] == expected
        return CBCSDKMock.StubResponse("", scode=204, json_parsable=False)

    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    cbcsdk_mock.mock_request('POST', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16/members',
                             on_post)
    api = cbcsdk_mock.api
    group = api.select(AssetGroup, 'db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16')
    group.add_members(param1, param2)


def test_add_members_with_device(cbcsdk_mock):
    """Tests the add_members API with a Device object."""
    def on_post(url, body, **kwargs):
        assert body['action'] == 'CREATE'
        assert body['external_member_ids'] == ["98765"]
        return CBCSDKMock.StubResponse("", scode=204, json_parsable=False)

    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    cbcsdk_mock.mock_request('POST', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16/members',
                             on_post)
    api = cbcsdk_mock.api
    group = api.select(AssetGroup, 'db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16')
    device = api.select(Device, 98765)
    group.add_members(device)


def test_remove_members(cbcsdk_mock):
    """Tests the remove_members API; it isn't as extensive because we already exercised the normalization."""
    def on_post(url, body, **kwargs):
        assert body['action'] == 'REMOVE'
        assert body['external_member_ids'] == ["70717", "14920"]
        return CBCSDKMock.StubResponse("", scode=204, json_parsable=False)

    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    cbcsdk_mock.mock_request('POST', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16/members',
                             on_post)
    api = cbcsdk_mock.api
    group = api.select(AssetGroup, 'db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16')
    group.remove_members(70717, 14920)
