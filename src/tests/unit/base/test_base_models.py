"""Testing the Query objects of cbc_sdk.base"""

import pytest
import logging
from cbc_sdk.base import MutableBaseModel, NewBaseModel
from cbc_sdk.platform import Device
from cbc_sdk.defense import Device as DefenseDevice
from cbc_sdk.defense import Policy
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ServerError, InvalidObjectError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.mock_devices import (DEVICE_GET_SPECIFIC_RESP, DEFENSE_DEVICE_GET_SPECIFIC_RESP,
                                              POLICY_GET_SPECIFIC_RESP)

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


def test_mutable_base_model_set_attr(cbcsdk_mock):
    """Test methods __setattr__ and _set of MutableBaseModel"""
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/12345", DEVICE_GET_SPECIFIC_RESP)
    api = cbcsdk_mock.api
    mutableBase = api.select(Device, 12345)

    assert isinstance(mutableBase, MutableBaseModel)
    assert isinstance(mutableBase, NewBaseModel)
    assert isinstance(mutableBase, Device)
    assert mutableBase._model_unique_id == 12345

    mutableBase.__setattr__("id", 54321)

    assert mutableBase._model_unique_id == 54321

    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/54321", DEVICE_GET_SPECIFIC_RESP)

    mutableBase._set("id", 00000)

    assert mutableBase._model_unique_id == 00000


def test_refresh(cbcsdk_mock):
    """Test _refresh and refresh methods"""
    api = cbcsdk_mock.api
    # _refresh() should fail without a model_unique_id set
    emptyMutableBase = MutableBaseModel(api)
    assert emptyMutableBase._refresh() is False

    # _refresh() should return True if there's a set model_unique_id and the
    # primary_key hasn't been modified
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", DEFENSE_DEVICE_GET_SPECIFIC_RESP)
    containsIdMutableBase = api.select(DefenseDevice, 12345)
    assert containsIdMutableBase._model_unique_id == 12345
    assert "deviceId" not in containsIdMutableBase._dirty_attributes.keys()
    assert containsIdMutableBase._refresh() is True

    # _refresh() should return False if the primary_key has been modified
    # cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/54321", DEFENSE_DEVICE_GET_SPECIFIC_RESP)
    containsIdMutableBase._set("deviceId", 54321)
    assert containsIdMutableBase._model_unique_id == 54321
    assert containsIdMutableBase.primary_key == "deviceId"
    assert "deviceId" in containsIdMutableBase._dirty_attributes.keys()
    assert containsIdMutableBase.__class__.primary_key in containsIdMutableBase._dirty_attributes.keys()
    assert isinstance(containsIdMutableBase, DefenseDevice)
    assert containsIdMutableBase._refresh() is False

    # refresh at end of tests to clear dirty_attributes
    containsIdMutableBase.reset()


def test_is_dirty(cbcsdk_mock):
    """Test is_dirty method"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", DEFENSE_DEVICE_GET_SPECIFIC_RESP)
    mutableBaseModelDevice = DefenseDevice(api, 12345)
    assert mutableBaseModelDevice.is_dirty() is False

    mutableBaseModelDevice._set("deviceId", 99999)
    assert mutableBaseModelDevice.is_dirty()

    # refresh at end of tests to clear dirty_attributes
    mutableBaseModelDevice.reset()


def test_update_object(cbcsdk_mock):
    """Test _update_object method"""
    # if primary_key hasn't been modified, use the _change_object_http_method
    # api = cbcsdk_mock.api
    # cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", DEFENSE_DEVICE_GET_SPECIFIC_RESP)
    # mutableBaseModelDevice = DefenseDevice(api, 12345)
    # cbcsdk_mock.mock_request("PATCH", "/integrationServices/v3/device/12345", "body")
    # mutableBaseModelDevice._set("name", "fakeName")
    # mutableBaseModelDevice._update_object()
    # struggling with this one cause of PATCH
    pass

# TODO: figure out why "result": [something != "success"] doesn't raise ServerError
def test_refresh_if_needed(cbcsdk_mock):
    """Test _refresh_if_needed method"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", DEFENSE_DEVICE_GET_SPECIFIC_RESP)
    mutableBaseModelDevice = DefenseDevice(api, 12345)

    # 200 status code
    refresh_resp_200 = cbcsdk_mock.StubResponse({"result": "success"}, 200)
    model_id = mutableBaseModelDevice._refresh_if_needed(refresh_resp_200)
    assert model_id == 12345

    # 404 status code
    refresh_resp_400 = cbcsdk_mock.StubResponse({}, 404, "Object not found text")
    with pytest.raises(ServerError):
        model_id = mutableBaseModelDevice._refresh_if_needed(refresh_resp_400)
        assert model_id == 12345

    # 200 status code with "result": "error"
    refresh_resp = cbcsdk_mock.StubResponse({"result": "error"}, 200)
    assert list(refresh_resp.json().keys()) == ["result"]
    mess = refresh_resp.json()
    post_res = mess.get("result", None)
    assert post_res and post_res != "success"
    assert refresh_resp.status_code == 200
    print(post_res)
    # with pytest.raises(ServerError):
    # this should raise ServerError???
    mutableBaseModelDevice._refresh_if_needed(refresh_resp)
        # assert model_id == 12345

# TODO: Need to implement PATCH in mock for dirty test
def test_save(cbcsdk_mock):
    """Test save method"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", DEFENSE_DEVICE_GET_SPECIFIC_RESP)
    mutableBaseModelDevice = DefenseDevice(api, 12345)

    assert mutableBaseModelDevice.save() is None

    # now make dirty
    mutableBaseModelDevice._set("firstName", "myName")
    # fails on PATCH unimplemented
    # assert mutableBaseModelDevice.save() == mutableBaseModelDevice

    # refresh at end of tests to clear dirty_attributes
    mutableBaseModelDevice.reset()


def test_reset(cbcsdk_mock):
    """Test reset method"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", DEFENSE_DEVICE_GET_SPECIFIC_RESP)
    mutableBaseModelDevice = DefenseDevice(api, 12345)
    assert mutableBaseModelDevice._dirty_attributes == {}
    mutableBaseModelDevice._set("firstName", "myName")
    assert "firstName" in mutableBaseModelDevice._dirty_attributes.keys()
    assert mutableBaseModelDevice.is_dirty()

    mutableBaseModelDevice.reset()
    assert mutableBaseModelDevice.is_dirty() is False

    # refresh at end of tests to clear dirty_attributes
    mutableBaseModelDevice.reset()


def test_delete(cbcsdk_mock):
    """Test delete method"""
    api = cbcsdk_mock.api
    # object without a _model_unique_id can't be deleted
    emptyMutableBase = MutableBaseModel(api)
    assert emptyMutableBase.delete() is None

    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", DEFENSE_DEVICE_GET_SPECIFIC_RESP)
    mutableBaseModelDevice = DefenseDevice(api, 12345)
    cbcsdk_mock.mock_request("DELETE", "/integrationServices/v3/device/12345", body=None)
    assert mutableBaseModelDevice.delete() is None

    # not sure how to get the ServerError to be raised here
    # Need to get the response status code for the DELETE outside of (200,204)
    newDevice = DefenseDevice(api, 12345)
    cbcsdk_mock.mock_request("DELETE", "/integrationServices/v3/device/12345", Exception)
    newDevice.delete()

    newDevice.reset()
    mutableBaseModelDevice.reset()


def test_validate(cbcsdk_mock):
    """Test validate method"""
    api = cbcsdk_mock.api
    policyMissingFields = Policy(api, model_unique_id="myUniqueId", initial_data={"description": "myDesc"})
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/myUniqueId", POLICY_GET_SPECIFIC_RESP)

    with pytest.raises(InvalidObjectError):
        assert policyMissingFields.validate() is None
