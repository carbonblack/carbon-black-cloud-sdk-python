"""Testing Device object of cbc_sdk.platform"""

import pytest
import logging
import copy
from cbc_sdk.platform import AssetGroup, Device, DeviceSearchQuery
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_asset_groups import EXISTING_AG_DATA, EXISTING_AG_DATA_2
from tests.unit.fixtures.platform.mock_devices import (GET_DEVICE_RESP, POST_DEVICE_SEARCH_RESP,
                                                       ASSET_GROUPS_RESPONSE_1, ASSET_GROUPS_OUTPUT_1,
                                                       ASSET_GROUPS_RESPONSE_2, ASSET_GROUPS_OUTPUT_2,
                                                       ASSET_GROUPS_RESPONSE_3, ASSET_GROUPS_OUTPUT_3,
                                                       ASSET_GROUPS_RESPONSE_SINGLE, ASSET_GROUPS_OUTPUT_SINGLE)

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

def test_device_query_0(cbcsdk_mock):
    """Testing Device Querying with .select(Device, `device_id`)"""
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    api = cbcsdk_mock.api
    platform_device_select_with_id = api.select(Device, 98765)
    platform_device_select_with_id.refresh()
    assert platform_device_select_with_id._model_unique_id == 98765
    assert platform_device_select_with_id.id == 98765
    assert isinstance(platform_device_select_with_id, Device)


def test_device_query_with_where_and(cbcsdk_mock):
    """Testing Device Querying with .where() and .and_()"""
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    api = cbcsdk_mock.api
    platform_device_select_with_where_stmt = api.select(Device).where(deviceId='98765').and_(name='win7x64')
    assert isinstance(platform_device_select_with_where_stmt, DeviceSearchQuery)

    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/devices/_search", POST_DEVICE_SEARCH_RESP)

    assert platform_device_select_with_where_stmt._count() == 1
    results = [res for res in platform_device_select_with_where_stmt._perform_query()]

    # compare select with ID inside the select method vs using .where() and .and_()
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    platform_device_select_with_id = api.select(Device, 98765)
    platform_device_select_with_id.refresh()
    assert results[0]._info['id'] == platform_device_select_with_id._info['id']
    assert len(results[0]._info) == len(platform_device_select_with_id._info)
    assert len(results[0]._info) != 0


def test_device_query_async(cbcsdk_mock):
    """Testing a device query with execute_async()"""
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/devices/_search", POST_DEVICE_SEARCH_RESP)
    api = cbcsdk_mock.api
    future = api.select(Device).where(deviceId='98765').and_(name='win7x64').execute_async()
    results = future.result()
    assert len(results) == 1
    assert results[0].policy_id == 11200


def test_device_id_property(cbcsdk_mock):
    """Testing raising AttributeError on call to device.deviceId."""
    with pytest.raises(AttributeError):
        cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
        a = Device(cbcsdk_mock.api, 98765)
        a.deviceId


def test_device_max_rows(cbcsdk_mock):
    """Testing Device Querying with .set_max_rows"""
    api = cbcsdk_mock.api
    query = api.select(Device).set_max_rows(10)
    assert query.max_rows == 10

    with pytest.raises(ApiError):
        query.set_max_rows(-1)

    with pytest.raises(ApiError):
        query.set_max_rows(10001)


@pytest.mark.parametrize("param, filt, memberids, response, output", [
    ([98765, 3031, 1777], "ALL", ["98765", "3031", "1777"], ASSET_GROUPS_RESPONSE_1, ASSET_GROUPS_OUTPUT_1),
    ([98765, 3031, 1777], "DYNAMIC", ["98765", "3031", "1777"], ASSET_GROUPS_RESPONSE_2, ASSET_GROUPS_OUTPUT_2),
    ([98765, 3031, 1777], "MANUAL", ["98765", "3031", "1777"], ASSET_GROUPS_RESPONSE_3, ASSET_GROUPS_OUTPUT_3),
    (98765, "ALL", ["98765"], ASSET_GROUPS_RESPONSE_SINGLE, ASSET_GROUPS_OUTPUT_SINGLE)
])
def test_get_asset_groups_for_devices(cbcsdk_mock, param, filt, memberids, response, output):
    """Tests the get_asset_groups_for_devices function."""
    def on_post(url, body, **kwargs):
        assert body['external_member_ids'] == memberids
        if filt == "ALL":
            assert 'membership_type' not in body
        else:
            assert body['membership_type'] == [filt]
        return response

    cbcsdk_mock.mock_request('POST', '/asset_groups/v1/orgs/test/members', on_post)
    api = cbcsdk_mock.api
    rc = Device.get_asset_groups_for_devices(api, param, membership=filt)
    assert rc == output


def test_get_asset_groups_for_devices_with_device(cbcsdk_mock):
    """Tests get_asset_groups_for_devices with a Device parameter."""
    def on_post(url, body, **kwargs):
        assert body['external_member_ids'] == ["98765"]
        assert 'membership_type' not in body
        return ASSET_GROUPS_RESPONSE_SINGLE

    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    cbcsdk_mock.mock_request('POST', '/asset_groups/v1/orgs/test/members', on_post)
    api = cbcsdk_mock.api
    device = api.select(Device, 98765)
    rc = Device.get_asset_groups_for_devices(api, device)
    assert rc == ASSET_GROUPS_OUTPUT_SINGLE
    rc = Device.get_asset_groups_for_devices(api, [device])
    assert rc == ASSET_GROUPS_OUTPUT_SINGLE


def test_get_asset_groups_for_devices_null_and_error_responses(cb):
    """Tests the error responses from test_get_asset_groups_for_devices."""
    assert Device.get_asset_groups_for_devices(cb, "bogus_value") == {}
    with pytest.raises(ApiError):
        Device.get_asset_groups_for_devices(cb, 98765, membership="BOGUS")


@pytest.mark.parametrize("membership", [
    "ALL",
    "DYNAMIC",
    "MANUAL"
])
def test_device_get_asset_group_ids(cbcsdk_mock, membership):
    """Tests the get_asset_group_ids Device function."""
    def on_post(url, body, **kwargs):
        assert body['external_member_ids'] == ["98765"]
        if membership == "ALL":
            assert 'membership_type' not in body
        else:
            assert body['membership_type'] == [membership]
        return ASSET_GROUPS_RESPONSE_SINGLE

    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    cbcsdk_mock.mock_request('POST', '/asset_groups/v1/orgs/test/members', on_post)
    api = cbcsdk_mock.api
    device = api.select(Device, 98765)
    assert device.get_asset_group_ids(membership=membership) == ["db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
                                                                 "509f437f-6b9a-4b8e-996e-9183b35f9069"]


def test_device_get_asset_groups(cbcsdk_mock):
    """Tests the get_asset_groups Device function."""
    def on_post(url, body, **kwargs):
        assert body['external_member_ids'] == ["98765"]
        assert 'membership_type' not in body
        return ASSET_GROUPS_RESPONSE_SINGLE

    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/98765", GET_DEVICE_RESP)
    cbcsdk_mock.mock_request('POST', '/asset_groups/v1/orgs/test/members', on_post)
    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16',
                             copy.deepcopy(EXISTING_AG_DATA))
    cbcsdk_mock.mock_request('GET', '/asset_groups/v1/orgs/test/groups/509f437f-6b9a-4b8e-996e-9183b35f9069',
                             copy.deepcopy(EXISTING_AG_DATA_2))
    api = cbcsdk_mock.api
    device = api.select(Device, 98765)
    result = device.get_asset_groups()
    assert len(result) == 2
    assert isinstance(result[0], AssetGroup)
    assert isinstance(result[1], AssetGroup)
    assert result[0].id == "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16"
    assert result[1].id == "509f437f-6b9a-4b8e-996e-9183b35f9069"
