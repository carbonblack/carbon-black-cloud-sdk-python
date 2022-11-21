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
from cbc_sdk.platform import AssetGroup
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_asset_groups import (CREATE_AG_REQUEST, CREATE_AG_RESPONSE, EXISTING_AG_DATA,
                                                            UPDATE_AG_REQUEST)


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

    cbcsdk_mock.mock_request('POST', '/asset_groups/v1beta/orgs/test/groups', on_post)
    api = cbcsdk_mock.api
    group = AssetGroup.create_group(api, "Group Test", "Group Test Description", 7113785)
    assert posted
    assert group is not None
    assert group.id == '4b48a403-e371-4e3d-ae6c-8eb9080fe7ad'
    assert group.name == 'Group Test'
    assert group.description == 'Group Test Description'
    assert group.policy_id == 7113785


def test_find_and_update_asset_group(cbcsdk_mock):
    """Tests finding and updating the asset group."""
    did_put = False

    def on_put(url, body, **kwargs):
        nonlocal did_put
        assert body == UPDATE_AG_REQUEST
        did_put = True
        return copy.deepcopy(body)

    cbcsdk_mock.mock_request('GET', '/asset_groups/v1beta/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    cbcsdk_mock.mock_request('PUT', '/asset_groups/v1beta/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
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

    cbcsdk_mock.mock_request('GET', '/asset_groups/v1beta/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    cbcsdk_mock.mock_request('DELETE', '/asset_groups/v1beta/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
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
