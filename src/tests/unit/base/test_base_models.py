"""Testing the MutableBaseModel and NewBaseModel objects of cbc_sdk.base"""

import pytest
import logging
from cbc_sdk.base import MutableBaseModel, NewBaseModel
from cbc_sdk.endpoint_standard import Device as EndpointStandardDevice
from cbc_sdk.endpoint_standard import Policy, Event
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ServerError, InvalidObjectError
from cbc_sdk.enterprise_edr import Feed
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_events import EVENT_GET_SPECIFIC_RESP
from tests.unit.fixtures.endpoint_standard.mock_devices import (ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP,
                                                                ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP_1,
                                                                POLICY_GET_SPECIFIC_RESP,
                                                                ENDPOINT_STANDARD_DEVICE_PATCH_RESP)
from tests.unit.fixtures.enterprise_edr.mock_threatintel import FEED_GET_SPECIFIC_RESP

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

# test name + _nbm suffix == NewBaseModel
# test name + _mbm suffix == MutableBaseModel

def test_model_unique_id_nbm(cbcsdk_mock):
    """Test _model_unique_id property/method of NewBaseModel"""
    api = cbcsdk_mock.api
    nbm_object = NewBaseModel(cb=api, model_unique_id=123)
    assert nbm_object._model_unique_id == 123


def test_new_object_nbm(cbcsdk_mock):
    """Test new_object class method of NewBaseModel via an Event object"""
    api = cbcsdk_mock.api
    nbm_object = Event.new_object(api, {"eventId": "testEventId", "otherData": "test"})
    assert nbm_object._model_unique_id == "testEventId"


def test_getattr_nbm(cbcsdk_mock):
    """Test __getattr__ method of NewBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    containsIdMutableBase = api.select(EndpointStandardDevice, 12345)
    assert containsIdMutableBase._model_unique_id == 12345
    assert containsIdMutableBase.__getattr__("avMaster") is False

    event = Event(api, 1234)
    assert 'eventTime' not in event._info
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/event/1234", {"eventInfo": {"eventTime": 1}})
    assert event.__getattr__("eventTime") == 1
    assert 'eventTime' in event._info

    with pytest.raises(AttributeError):
        assert event.__getattr__("missingInfoTag") is None


def test_setattr_nbm(cbcsdk_mock):
    """Test __setattr__ method of NewBaseModel"""
    api = cbcsdk_mock.api
    nbm = Event(api, 101)
    nbm.__setattr__("_my_attr", "attr_val")
    assert nbm._my_attr == "attr_val"

    # attribute name must start with "_", otherwise it's immutable
    with pytest.raises(AttributeError):
        nbm.__setattr__("immutable_attr", "immutable_val")


def test_get_nbm(cbcsdk_mock):
    """Test get method of NewBaseModel"""
    api = cbcsdk_mock.api
    nbm = NewBaseModel(api)
    assert nbm.get("_mutable_attr", default_val="def") == "def"

    nbm.__setattr__("_mutable_attr", "new_value")
    assert nbm.get("_mutable_attr", default_val="def") == "new_value"


def test_refresh_nbm(cbcsdk_mock):
    """Test refresh and _refresh methods of NewBaseModel"""
    api = cbcsdk_mock.api
    # refresh() should return False if there is no _model_unique_id
    object_without_model_unique_id = NewBaseModel(api)
    assert object_without_model_unique_id.refresh() is False

    # refresh() should return False if cls.primary_key is in _dirty_attributes
    object_with_dirty_model_unique_id = NewBaseModel(api, 1)
    object_with_dirty_model_unique_id._dirty_attributes["id"] = 2
    assert object_with_dirty_model_unique_id.primary_key == "id"
    assert "id" in object_with_dirty_model_unique_id._dirty_attributes
    object_with_dirty_model_unique_id.refresh() is False

    # refresh() should return True if there's a _model_unique_id and primary_key hasn't been changed
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/event/a1e12604d67b11ea920d3d9192a785d1",
                             EVENT_GET_SPECIFIC_RESP)
    refreshable_object = Event(api, "a1e12604d67b11ea920d3d9192a785d1")
    assert refreshable_object._full_init is False
    assert refreshable_object.refresh() is True
    assert refreshable_object._full_init is True


def test_build_api_request_uri_nbm(cbcsdk_mock):
    """Test _build_api_request_uri method of NewBaseModel"""
    api = cbcsdk_mock.api

    # if there's no _model_unique_id, _build_api_request_uri should return just cls.urlobject
    event = Event(api, model_unique_id=None)
    assert event._build_api_request_uri() == "/integrationServices/v3/event"

    # if there's a _model_unique_id, _build_api_request_uri should return cls.urlobect + _model_unique_id
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/event/a1e12604d67b11ea920d3d9192a785d1",
                             EVENT_GET_SPECIFIC_RESP)
    event = Event(api, "a1e12604d67b11ea920d3d9192a785d1")
    assert event._build_api_request_uri() == "/integrationServices/v3/event/a1e12604d67b11ea920d3d9192a785d1"


def test_retrieve_cb_info_nbm(cbcsdk_mock):
    """Test _retrieve_cb_info method of NewBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/event/a1e12604d67b11ea920d3d9192a785d1",
                             EVENT_GET_SPECIFIC_RESP)
    event = Event(api, "a1e12604d67b11ea920d3d9192a785d1")
    assert event._build_api_request_uri() == "/integrationServices/v3/event/a1e12604d67b11ea920d3d9192a785d1"
    # _retrieve_cb_info() calls cb.get_object, which makes the API call to retrieve the object
    assert event._retrieve_cb_info() == EVENT_GET_SPECIFIC_RESP


def test_parse_nbm(cbcsdk_mock):
    """Test _parse method of NewBaseModel"""
    nbm = NewBaseModel(cbcsdk_mock.api)
    # _parse returns whatever is passed into it as a parameter
    assert nbm._parse(nbm._cb) == cbcsdk_mock.api
    assert nbm._parse(nbm._last_refresh_time) == 0


def test_original_document_nbm(cbcsdk_mock):
    """Test original_document method/property of NewBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/event/a1e12604d67b11ea920d3d9192a785d1",
                             EVENT_GET_SPECIFIC_RESP)
    event = api.select(Event, "a1e12604d67b11ea920d3d9192a785d1")
    # original_document refreshes (if _full_init == False), then returns self._info
    assert event._full_init is False
    assert event.original_document == event._info
    assert event._full_init is True
    assert event.original_document['eventId'] == "a1e12604d67b11ea920d3d9192a785d1"


def test_set_attr_mbm(cbcsdk_mock):
    """Test methods __setattr__ and _set of MutableBaseModel"""
    feed_id_1 = "pv65TYVQy8YWMX9KsQUg"
    feed_id_2 = "qw76UZWRz9ZXNY0LtRVh"
    cbcsdk_mock.mock_request("GET", f"/threathunter/feedmgr/v2/orgs/test/feeds/{feed_id_1}", FEED_GET_SPECIFIC_RESP)
    api = cbcsdk_mock.api
    mutable_base = api.select(Feed, "pv65TYVQy8YWMX9KsQUg")

    assert isinstance(mutable_base, MutableBaseModel)
    assert isinstance(mutable_base, NewBaseModel)
    assert isinstance(mutable_base, Feed)

    assert mutable_base._model_unique_id == feed_id_1

    mutable_base.__setattr__("id", feed_id_2)
    assert mutable_base._model_unique_id == feed_id_2

    cbcsdk_mock.mock_request("GET", f"/threathunter/feedmgr/v2/orgs/test/feeds/{feed_id_2}", FEED_GET_SPECIFIC_RESP)

    mutable_base._set("id", "aaaaaaaaaaaaaaaaaaaa")

    assert mutable_base._model_unique_id == "aaaaaaaaaaaaaaaaaaaa"

    # refresh at end of tests to clear dirty_attributes
    mutable_base.reset()


def test_refresh_mbm(cbcsdk_mock):
    """Test _refresh and refresh methods of MutableBaseModel"""
    api = cbcsdk_mock.api
    # _refresh() should fail without a model_unique_id set
    emptyMutableBase = MutableBaseModel(api)
    assert emptyMutableBase._refresh() is False

    # _refresh() should return True if there's a set model_unique_id and the
    # primary_key hasn't been modified
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    containsIdMutableBase = api.select(EndpointStandardDevice, 12345)
    assert containsIdMutableBase._model_unique_id == 12345
    assert "deviceId" not in containsIdMutableBase._dirty_attributes.keys()
    assert containsIdMutableBase._refresh() is True

    # _refresh() should return False if the primary_key has been modified
    # cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/54321",
    #                          ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    containsIdMutableBase._set("deviceId", 54321)
    assert containsIdMutableBase._model_unique_id == 54321
    assert containsIdMutableBase.primary_key == "deviceId"
    assert "deviceId" in containsIdMutableBase._dirty_attributes.keys()
    assert containsIdMutableBase.__class__.primary_key in containsIdMutableBase._dirty_attributes.keys()
    assert isinstance(containsIdMutableBase, EndpointStandardDevice)
    assert containsIdMutableBase._refresh() is False

    # refresh at end of tests to clear dirty_attributes
    containsIdMutableBase.reset()


def test_is_dirty_mbm(cbcsdk_mock):
    """Test is_dirty method of MutableBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    mutableBaseModelDevice = EndpointStandardDevice(api, 12345)
    assert mutableBaseModelDevice.is_dirty() is False

    mutableBaseModelDevice._set("deviceId", 99999)
    assert mutableBaseModelDevice.is_dirty()

    # refresh at end of tests to clear dirty_attributes
    mutableBaseModelDevice.reset()


def test_update_object_mbm(cbcsdk_mock):
    """Test _update_object method of MutableBaseModel"""
    # if primary_key hasn't been modified, we use the _change_object_http_method
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    mutableBaseModelDevice = EndpointStandardDevice(api, 12345)
    cbcsdk_mock.mock_request("PATCH", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_PATCH_RESP)
    print(mutableBaseModelDevice._info)
    mutableBaseModelDevice._set("name", "newFakeName")
    mutableBaseModelDevice._set("testId", 1)

    assert mutableBaseModelDevice._update_object() == 12345
    print(mutableBaseModelDevice._info)

    assert mutableBaseModelDevice.deviceId == 12345
    assert mutableBaseModelDevice._info['name'] == 'newFakeName'
    assert mutableBaseModelDevice._info['testId'] == 1

    # refresh at end of tests to clear dirty_attributes
    mutableBaseModelDevice.reset()


def test_refresh_if_needed_mbm(cbcsdk_mock):
    """Test _refresh_if_needed method of MutableBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    mutableBaseModelDevice = EndpointStandardDevice(api, 12345)

    # 200 status code
    refresh_resp_200 = cbcsdk_mock.StubResponse({"success": True, "deviceInfo": {"deviceId": 12345}}, 200)
    model_id = mutableBaseModelDevice._refresh_if_needed(refresh_resp_200)
    assert model_id == 12345

    # 404 status code
    refresh_resp_400 = cbcsdk_mock.StubResponse({}, 404, "Object not found text")
    with pytest.raises(ServerError):
        model_id = mutableBaseModelDevice._refresh_if_needed(refresh_resp_400)
        assert model_id == 12345

    # 200 status code with "result": "error"
    refresh_resp = cbcsdk_mock.StubResponse({"success": False, "message": "Couldn't update the record :("}, 200)
    with pytest.raises(ServerError):
        model_id = mutableBaseModelDevice._refresh_if_needed(refresh_resp)
        assert model_id == 12345

    # 200 status code with a response that isn't a dictionary
    refresh_unknown_resp = cbcsdk_mock.StubResponse("not_a_dictionary", 200)
    with pytest.raises(ServerError):
        model_id = mutableBaseModelDevice._refresh_if_needed(refresh_unknown_resp)

    # refresh at end of tests to clear dirty_attributes
    mutableBaseModelDevice.reset()


def test_save_mbm(cbcsdk_mock):
    """Test save method of MutableBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    mutableBaseModelDevice = EndpointStandardDevice(api, 12345)

    assert mutableBaseModelDevice.save() is None
    assert mutableBaseModelDevice._info["firstName"] is None

    # now make dirty
    mutableBaseModelDevice._set("firstName", "newName")
    cbcsdk_mock.mock_request("PATCH", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_PATCH_RESP)
    # fails on PATCH unimplemented
    assert mutableBaseModelDevice.save() == mutableBaseModelDevice
    assert mutableBaseModelDevice._info["firstName"] == "newName"

    # refresh at end of tests to clear dirty_attributes
    mutableBaseModelDevice.reset()


def test_reset_mbm(cbcsdk_mock):
    """Test reset method of MutableBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    device = EndpointStandardDevice(api, 12345)
    assert device._dirty_attributes == {}
    device._set("lastName", "restNewName")
    assert "lastName" in device._dirty_attributes
    assert device.is_dirty()

    device.reset()
    assert device.is_dirty() is False
    assert device._dirty_attributes == {}

    # refresh at end of tests to clear dirty_attributes
    device.reset()


def test_delete_mbm(cbcsdk_mock):
    """Test delete method of MutableBaseModel"""
    api = cbcsdk_mock.api
    # object without a _model_unique_id can't be deleted
    emptyMutableBase = MutableBaseModel(api)
    assert emptyMutableBase._model_unique_id is None
    assert emptyMutableBase.delete() is None

    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/12345", ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP)
    mutableBaseModelDevice = EndpointStandardDevice(api, 12345)
    assert mutableBaseModelDevice._model_unique_id == 12345
    cbcsdk_mock.mock_request("DELETE", "/integrationServices/v3/device/12345", body=None)
    assert mutableBaseModelDevice.delete() is None

    # receiving a status code outside of (200,204) should raise a ServerError
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/device/54321",
                             ENDPOINT_STANDARD_DEVICE_GET_SPECIFIC_RESP_1)
    newDevice = EndpointStandardDevice(api, 54321)
    delete_resp = cbcsdk_mock.StubResponse(contents={"success": False}, scode=403,
                                           text="Failed to delete for some reason")
    cbcsdk_mock.mock_request("DELETE", "/integrationServices/v3/device/54321", delete_resp)
    with pytest.raises(ServerError):
        newDevice.delete()

    newDevice.reset()
    mutableBaseModelDevice.reset()


def test_validate_mbm(cbcsdk_mock):
    """Test validate method of MutableBaseModel"""
    api = cbcsdk_mock.api
    policyMissingFields = Policy(api, model_unique_id="myUniqueId",
                                 initial_data={"description": "Policy objects need more fields here"})
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/myUniqueId", POLICY_GET_SPECIFIC_RESP)

    with pytest.raises(InvalidObjectError):
        assert policyMissingFields.validate() is None
