"""Testing the MutableBaseModel and NewBaseModel objects of cbc_sdk.base"""

import pytest
import logging
from cbc_sdk.base import MutableBaseModel, NewBaseModel
from cbc_sdk.endpoint_standard import Policy
from cbc_sdk.platform import Process
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ServerError, InvalidObjectError, ApiError
from cbc_sdk.enterprise_edr.threat_intelligence import FeedModel
from cbc_sdk.enterprise_edr import Feed
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.endpoint_standard.mock_policy import (POLICY_GET_SPECIFIC_RESP, POLICY_GET_RESP,
                                                               POLICY_UPDATE_RESP, POLICY_GET_RESP_1,
                                                               POLICY_GET_RESP_2, POLICY_POST_RESP)
from tests.unit.fixtures.enterprise_edr.mock_threatintel import FEED_GET_SPECIFIC_RESP
from tests.unit.fixtures.platform.mock_process import (GET_PROCESS_VALIDATION_RESP,
                                                       POST_PROCESS_SEARCH_JOB_RESP,
                                                       GET_PROCESS_SEARCH_JOB_RESP,
                                                       GET_PROCESS_SEARCH_JOB_RESULTS_RESP)

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


class _TestBaseModel(NewBaseModel):
    """Test class allowing testing of multiple scenarios of string representation."""
    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=True):
        """
        Initialize the TestBaseModel.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (Any): The unique ID for this particular instance of the model object.
            initial_data (dict): The data to use when initializing the model object.
            force_init (bool): True to force object initialization.
            full_doc (bool): True to mark the object as fully initialized.
        """
        super(_TestBaseModel, self).__init__(cb, model_unique_id, initial_data, force_init, full_doc)
        self._my_subobjects = {}

    def _subobject(self, name):
        """
        Returns the "subobject value" of the given attribute.

        Args:
            name (str): Name of the subobject value to be returned.

        Returns:
            Any: Subobject value for the attribute, or None if there is none.
        """
        if name in self._my_subobjects:
            return self._my_subobjects[name]
        return super(_TestBaseModel, self)._subobject(name)


# ==================================== UNIT TESTS BELOW ====================================

# test name + _nbm suffix == NewBaseModel
# test name + _mbm suffix == MutableBaseModel

def test_model_unique_id_nbm(cbcsdk_mock):
    """Test _model_unique_id property/method of NewBaseModel"""
    api = cbcsdk_mock.api
    nbm_object = NewBaseModel(cb=api, model_unique_id=123)
    assert nbm_object._model_unique_id == 123
    obj_repr = nbm_object.__repr__()
    assert 'cbc_sdk.base.NewBaseModel:' in obj_repr
    assert 'id 123' in obj_repr

    nbm_object._full_init = False
    result = str(nbm_object)
    assert 'Partially initialized. Use .refresh() to load all attributes' in result


def test_model_attributes_nbm(cbcsdk_mock):
    """Test _model_unique_id property/method of NewBaseModel"""
    initial_data = {
        'id': 123,
        'test': 1,
        'a list': [],
        'a string': 'test'
    }
    api = cbcsdk_mock.api
    nbm_object = NewBaseModel(cb=api, model_unique_id=None, initial_data=initial_data)
    nbm_object._dirty_attributes = {'id': None, 'test': 2}
    assert nbm_object._model_unique_id == 123
    result_str = str(nbm_object)
    assert '{0:s} {1:>8s}:'.format('(+)', 'id') in result_str
    assert '{0:s} {1:>8s}:'.format('(*)', 'test') in result_str


def test_new_object_nbm(cbcsdk_mock):
    """Test new_object class method of NewBaseModel via a Policy object"""
    api = cbcsdk_mock.api
    nbm_object = Policy.new_object(api, {'id': 6681, 'otherData': 'test'})
    assert nbm_object._model_unique_id == 6681


def test_setattr_nbm(cbcsdk_mock):
    """Test __setattr__ method of NewBaseModel"""
    api = cbcsdk_mock.api
    nbm = NewBaseModel(api, 101)
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
    assert object_with_dirty_model_unique_id.refresh() is False

    # refresh() should return True if there's a _model_unique_id and primary_key hasn't been changed
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    refreshable_object = Policy(api, 30241)
    assert refreshable_object._full_init is False
    refreshable_object.refresh()
    assert refreshable_object._full_init is True


def test_build_api_request_uri_nbm(cbcsdk_mock):
    """Test _build_api_request_uri method of NewBaseModel"""
    api = cbcsdk_mock.api

    # if there's no _model_unique_id, _build_api_request_uri should return just cls.urlobject
    policy = Policy(api, model_unique_id=None)
    assert policy._build_api_request_uri() == "/integrationServices/v3/policy"

    # if there's a _model_unique_id, _build_api_request_uri should return cls.urlobect + _model_unique_id
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    policy = Policy(api, 30241)
    assert policy._build_api_request_uri() == "/integrationServices/v3/policy/30241"


def test_retrieve_cb_info_nbm(cbcsdk_mock):
    """Test _retrieve_cb_info method of NewBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    policy = Policy(api, 30241)
    assert policy._build_api_request_uri() == "/integrationServices/v3/policy/30241"
    # _retrieve_cb_info() calls cb.get_object, which makes the API call to retrieve the object
    assert policy._retrieve_cb_info() == POLICY_GET_RESP


def test_parse_nbm(cbcsdk_mock):
    """Test _parse method of NewBaseModel"""
    nbm = NewBaseModel(cbcsdk_mock.api)
    # _parse returns whatever is passed into it as a parameter
    assert nbm._parse(nbm._cb) == cbcsdk_mock.api
    assert nbm._parse(nbm._last_refresh_time) == 0


def test_original_document_nbm(cbcsdk_mock):
    """Test original_document method/property of NewBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    policy = api.select(Policy, 30241)
    # original_document refreshes (if _full_init == False), then returns self._info
    assert policy._full_init is False
    assert policy.original_document == policy._info
    assert policy._full_init is True
    assert policy.original_document['id'] == 30241


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


def test_validate_mbm(cbcsdk_mock):
    """Test validate method of MutableBaseModel"""
    api = cbcsdk_mock.api
    policyMissingFields = Policy(api, model_unique_id="myUniqueId",
                                 initial_data={"description": "Policy objects need more fields here"})
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/myUniqueId", POLICY_GET_SPECIFIC_RESP)

    with pytest.raises(InvalidObjectError):
        assert policyMissingFields.validate() is None


def test_setattr_mbm(cbcsdk_mock):
    """Test validate method of MutableBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    policy = api.select(Policy, 30241)
    assert policy._model_unique_id == 30241
    assert "id" not in policy._dirty_attributes.keys()
    assert policy._refresh() is True

    policy._set("id", 54321)
    assert policy._model_unique_id == 54321
    assert policy.primary_key == "id"
    assert "id" in policy._dirty_attributes.keys()
    assert policy.__class__.primary_key in policy._dirty_attributes.keys()
    assert isinstance(policy, Policy)
    assert policy._refresh() is False
    # refresh at end of tests to clear dirty_attributes
    policy.reset()


def test_is_dirty_mbm(cbcsdk_mock):
    """Test is_dirty method of MutableBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    policy = api.select(Policy, 30241)
    assert policy.is_dirty() is False

    policy._set("id", 99999)
    assert policy.is_dirty()

    # refresh at end of tests to clear dirty_attributes
    policy.reset()


def test_update_object_mbm(cbcsdk_mock):
    """Test _update_object method of MutableBaseModel"""
    # if primary_key hasn't been modified, we use the _change_object_http_method
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30242", POLICY_GET_RESP_1)
    cbcsdk_mock.mock_request("PUT", "/integrationServices/v3/policy/30242", POLICY_UPDATE_RESP)
    policy = api.select(Policy, 30242)
    policy._set("name", "newFakeName")
    policy._set("testId", 1)

    assert policy._update_object() == 30242

    assert policy.id == 30242
    assert policy._info['name'] == 'newFakeName'
    assert policy._info['testId'] == 1

    # refresh at end of tests to clear dirty_attributes
    policy.reset()


def test_query_implementation_error(cbcsdk_mock):
    """Test save method of MutableBaseModel"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError):
        api.select(FeedModel)


def test_update_entire_mbm(cbcsdk_mock):
    """Test save method of MutableBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30242", POLICY_GET_RESP_1)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    mutableBaseModelPolicy = Policy(api, 30242)
    with pytest.raises(AttributeError):
        mutableBaseModelPolicy._model_unique_id = 30241

    mutableBaseModelPolicy.id = 30241
    cbcsdk_mock.mock_request("POST", "/integrationServices/v3/policy", POLICY_POST_RESP)
    assert mutableBaseModelPolicy._update_entire_object()
    assert mutableBaseModelPolicy.id == 30241


def test_patch_entire_mbm(cbcsdk_mock):
    """Test save method of MutableBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30242", POLICY_GET_RESP_1)
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    mutableBaseModelPolicy = Policy(api, 30242)
    mutableBaseModelPolicy.id = 30241
    cbcsdk_mock.mock_request("PUT", "/integrationServices/v3/policy", POLICY_POST_RESP)
    assert mutableBaseModelPolicy._patch_object()
    assert mutableBaseModelPolicy.id == 30241


def test_getattr_nbm(cbcsdk_mock):
    """Test __getattr__ method of NewBaseModel"""
    api = cbcsdk_mock.api
    policy = Policy(api, 30241)
    assert 'name' not in policy._info
    assert policy._model_unique_id == 30241
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30241", POLICY_GET_RESP)
    assert policy.__getattr__("name") == 'Lyon_test'
    assert 'name' in policy._info

    with pytest.raises(AttributeError):
        assert policy.__getattr__("NotExist") is None


def test_reset_mbm(cbcsdk_mock):
    """Test reset method of MutableBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30242", POLICY_GET_RESP_1)
    policy = Policy(api, 30242)
    assert policy._dirty_attributes == {}
    policy._set("name", "somename")
    assert "name" in policy._dirty_attributes
    assert policy.is_dirty()

    policy.reset()
    assert policy.is_dirty() is False
    assert policy._dirty_attributes == {}

    # refresh at end of tests to clear dirty_attributes
    policy.reset()


def test_delete_mbm(cbcsdk_mock):
    """Test delete method of MutableBaseModel"""
    api = cbcsdk_mock.api
    # object without a _model_unique_id can't be deleted
    emptyMutableBase = MutableBaseModel(api)
    assert emptyMutableBase._model_unique_id is None
    assert emptyMutableBase.delete() is None

    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30242", POLICY_GET_RESP_1)
    mutableBaseModelPolicy = Policy(api, 30242)
    assert mutableBaseModelPolicy._model_unique_id == 30242
    cbcsdk_mock.mock_request("DELETE", "/integrationServices/v3/policy/30242", body=None)
    assert mutableBaseModelPolicy.delete() is None

    # receiving a status code outside of (200,204) should raise a ServerError
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30243",
                             POLICY_GET_RESP_2)
    newPolicy = Policy(api, 30243)
    delete_resp = cbcsdk_mock.StubResponse(contents={"success": False}, scode=403,
                                           text="Failed to delete for some reason")
    cbcsdk_mock.mock_request("DELETE", "/integrationServices/v3/policy/30243", delete_resp)
    with pytest.raises(ServerError):
        newPolicy.delete()

    newPolicy.reset()
    mutableBaseModelPolicy.reset()


def test_refresh_if_needed_mbm(cbcsdk_mock):
    """Test _refresh_if_needed method of MutableBaseModel"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/policy/30242", POLICY_GET_RESP_1)
    mutableBaseModelDevice = Policy(api, 30242)

    # 200 status code
    refresh_resp_200 = cbcsdk_mock.StubResponse({"success": True, "policyInfo": {"id": 30242}}, 200)
    model_id = mutableBaseModelDevice._refresh_if_needed(refresh_resp_200)
    assert model_id == 30242

    # 404 status code
    refresh_resp_404 = cbcsdk_mock.StubResponse({}, 404, "Object not found text")
    with pytest.raises(ServerError):
        model_id = mutableBaseModelDevice._refresh_if_needed(refresh_resp_404)
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


def test_print_unrefreshablemodel(cbcsdk_mock):
    """Test printing an UnrefreshableModel"""
    # mock the search validation
    cbcsdk_mock.mock_request("GET", "/api/investigate/v1/orgs/test/processes/search_validation",
                             GET_PROCESS_VALIDATION_RESP)
    # mock the POST of a search
    cbcsdk_mock.mock_request("POST", "/api/investigate/v2/orgs/test/processes/search_job",
                             POST_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to check search status
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v1/orgs/test/processes/"
                                     "search_jobs/2c292717-80ed-4f0d-845f-779e09470920"),
                             GET_PROCESS_SEARCH_JOB_RESP)
    # mock the GET to get search results
    cbcsdk_mock.mock_request("GET", ("/api/investigate/v2/orgs/test/processes/search_jobs/"
                                     "2c292717-80ed-4f0d-845f-779e09470920/results"),
                             GET_PROCESS_SEARCH_JOB_RESULTS_RESP)

    api = cbcsdk_mock.api
    guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
    proc = api.select(Process, guid)
    proc_str = proc.__str__()
    assert "Partially initialized" not in proc_str


def test_str_stringize():
    """Test the _str_stringize() method"""
    assert NewBaseModel._str_stringize(3) == '3'
    assert NewBaseModel._str_stringize('Blort') == 'Blort'
    assert NewBaseModel._str_stringize([1, 2, 3]) == '[1, 2, 3]'
    assert NewBaseModel._str_stringize('If this had been an actual emergency, we would all be dead by now') \
        == 'If this had been an actual emergency, we would ...'


def test_str_attr_line(cb):
    """Test the _str_attr_line method"""
    subobject_data = {
        "id": 4096,
        "soint": 42,
        "sostring": "Boom!",
        "solist": [2, 3, 5, 7, 11]
    }
    listobj_data = {
        'id': 64
    }
    listobj2_data = {
        'id': 128
    }
    object_data = {
        "id": 1024,
        "objint": 105,
        "objstring": "KMFMS",
        "objlong": "If this had been an actual emergency, we would all be dead by now",
        "objlist": [1, 2, 3, 5, 8, 13],
        "empty": [],
        "objdict": {"a": 1, "b": 2, "c": 3},
        "emptydict": {},
        "mini_me": subobject_data,
        "List1": [listobj_data],
        "List2": [listobj_data, listobj2_data]
    }
    my_subobject = _TestBaseModel(cb, subobject_data["id"], subobject_data)
    my_listobj = _TestBaseModel(cb, listobj_data["id"], listobj_data)
    my_listobj2 = _TestBaseModel(cb, listobj2_data["id"], listobj2_data)
    my_object = _TestBaseModel(cb, object_data["id"], object_data)
    my_object._my_subobjects["mini_me"] = my_subobject
    my_object._my_subobjects["List1"] = [my_listobj]
    my_object._my_subobjects["List2"] = [my_listobj, my_listobj2]
    # Test rendering of basic data (subobject mode)
    name_field_len = my_object._str_name_field_len(object_data)
    rendering = my_object._str_attr_line('objint', object_data['objint'], name_field_len, False)
    assert len(rendering) == 1
    assert rendering[0] == '   objint: 105'
    rendering = my_object._str_attr_line('objstring', object_data['objstring'], name_field_len, False)
    assert len(rendering) == 1
    assert rendering[0] == 'objstring: KMFMS'
    rendering = my_object._str_attr_line('objlong', object_data['objlong'], name_field_len, False)
    assert len(rendering) == 1
    assert rendering[0] == '  objlong: If this had been an actual emergency, we would ...'
    # Test rendering of list data (subobject mode)
    rendering = my_object._str_attr_line('objlist', object_data['objlist'], name_field_len, False)
    assert len(rendering) == 5
    assert rendering[0] == '  objlist: [list:6 items]:'
    assert rendering[1] == '           [0]: 1'
    assert rendering[2] == '           [1]: 2'
    assert rendering[3] == '           [2]: 3'
    assert rendering[4] == '           [...]'
    rendering = my_object._str_attr_line('empty', object_data['empty'], name_field_len, False)
    assert len(rendering) == 1
    assert rendering[0] == '    empty: [list:0 items]'
    # Test rendering of dict data (subobject mode)
    rendering = my_object._str_attr_line('objdict', object_data['objdict'], name_field_len, False)
    assert len(rendering) == 1
    assert rendering[0].startswith('  objdict: {')
    rendering = my_object._str_attr_line('emptydict', object_data['emptydict'], name_field_len, False)
    assert len(rendering) == 1
    assert rendering[0].startswith('emptydict: {')
    # Test rendering of subobject data (subobject mode)
    rendering = my_object._str_attr_line('mini_me', object_data['mini_me'], name_field_len, False)
    assert len(rendering) == 1
    assert rendering[0].startswith('  mini_me: {')
    # Test rendering of list-of-subobjects data (subobject mode)
    rendering = my_object._str_attr_line('List1', object_data['List1'], name_field_len, False)
    assert len(rendering) == 2
    assert rendering[0] == '    List1: [list:1 item]:'
    assert rendering[1].startswith('           [0]: {')
    rendering = my_object._str_attr_line('List2', object_data['List2'], name_field_len, False)
    assert len(rendering) == 3
    assert rendering[0] == '    List2: [list:2 items]:'
    assert rendering[1].startswith('           [0]: {')
    assert rendering[2].startswith('           [1]: {')
    # Test rendering of basic data (top-level mode)
    rendering = my_object._str_attr_line('objint', object_data['objint'], name_field_len)
    assert len(rendering) == 1
    assert rendering[0] == '       objint: 105'
    rendering = my_object._str_attr_line('objstring', object_data['objstring'], name_field_len)
    assert len(rendering) == 1
    assert rendering[0] == '    objstring: KMFMS'
    rendering = my_object._str_attr_line('objlong', object_data['objlong'], name_field_len)
    assert len(rendering) == 1
    assert rendering[0] == '      objlong: If this had been an actual emergency, we would ...'
    # Test rendering of list data (top-level mode)
    rendering = my_object._str_attr_line('objlist', object_data['objlist'], name_field_len)
    assert len(rendering) == 5
    assert rendering[0] == '      objlist: [list:6 items]:'
    assert rendering[1] == '               [0]: 1'
    assert rendering[2] == '               [1]: 2'
    assert rendering[3] == '               [2]: 3'
    assert rendering[4] == '               [...]'
    rendering = my_object._str_attr_line('empty', object_data['empty'], name_field_len)
    assert len(rendering) == 1
    assert rendering[0] == '        empty: [list:0 items]'
    # Test rendering of dict data (top-level mode)
    rendering = my_object._str_attr_line('objdict', object_data['objdict'], name_field_len)
    assert len(rendering) == 5
    assert rendering[0] == '      objdict: [dict] {'
    assert rendering[1] == '                   a: 1'
    assert rendering[2] == '                   b: 2'
    assert rendering[3] == '                   c: 3'
    assert rendering[4] == '               }'
    rendering = my_object._str_attr_line('emptydict', object_data['emptydict'], name_field_len)
    assert len(rendering) == 2
    assert rendering[0] == '    emptydict: [dict] {'
    assert rendering[1] == '               }'
    # Test rendering of subobject data (top-level mode) including lists in subobject
    rendering = my_object._str_attr_line('mini_me', object_data['mini_me'], name_field_len)
    assert len(rendering) == 10
    assert rendering[0] == '      mini_me: [_TestBaseModel object]:'
    assert rendering[1] == '                     id: 4096'
    assert rendering[2] == '                  soint: 42'
    assert rendering[3] == '                 solist: [list:5 items]:'
    assert rendering[4] == '                         [0]: 2'
    assert rendering[5] == '                         [1]: 3'
    assert rendering[6] == '                         [2]: 5'
    assert rendering[7] == '                         [...]'
    assert rendering[8] == '               sostring: Boom!'
    assert rendering[9] == ''
    # Test rendering of list-of-subobjects data (top-level mode)
    rendering = my_object._str_attr_line('List1', object_data['List1'], name_field_len)
    assert len(rendering) == 4
    assert rendering[0] == '        List1: [list:1 item]:'
    assert rendering[1] == '               [0]: [_TestBaseModel object]:'
    assert rendering[2] == '                    id: 64'
    assert rendering[3] == ''
    rendering = my_object._str_attr_line('List2', object_data['List2'], name_field_len)
    assert len(rendering) == 7
    assert rendering[0] == '        List2: [list:2 items]:'
    assert rendering[1] == '               [0]: [_TestBaseModel object]:'
    assert rendering[2] == '                    id: 64'
    assert rendering[3] == ''
    assert rendering[4] == '               [1]: [_TestBaseModel object]:'
    assert rendering[5] == '                    id: 128'
    assert rendering[6] == ''
