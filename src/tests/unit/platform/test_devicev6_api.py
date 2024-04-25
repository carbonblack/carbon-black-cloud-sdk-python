# *******************************************************
# Copyright (c) VMware, Inc. 2020-2023. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Tests of the devices v6 API."""

import pytest
from cbc_sdk.errors import ApiError, ServerError
from cbc_sdk.platform import Device, DeviceFacet, Job
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_devices import (FACET_RESPONSE, FACET_INIT_1, FACET_INIT_2, FACET_INIT_3,
                                                       FACET_INIT_4, FACET_INIT_5, FACET_INIT_6, FACET_INIT_7,
                                                       GET_SCROLL_DEVICES, EXPORT_JOB_REDIRECT)


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


def test_get_device(cbcsdk_mock):
    """Test simple retrieval of a Device object by ID."""
    cbcsdk_mock.mock_request('GET', "/appservices/v6/orgs/test/devices/6023",
                             {"device_id": 6023, "organization_name": "thistestworks"})
    api = cbcsdk_mock.api
    rc = api.select(Device, 6023)
    assert isinstance(rc, Device)
    assert rc.device_id == 6023
    assert rc.organization_name == "thistestworks"


def test_device_background_scan(cbcsdk_mock):
    """Test setting the background scan status of a device."""
    def on_bgscan(url, body, **kwargs):
        assert body == {"action_type": "BACKGROUND_SCAN", "device_id": [6023], "options": {"toggle": "ON"}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_bgscan)
    api = cbcsdk_mock.api
    api.device_background_scan([6023], True)


def test_device_bypass(cbcsdk_mock):
    """Test setting the bypass status of a device."""
    def on_bypass(url, body, **kwargs):
        assert body == {"action_type": "BYPASS", "device_id": [6023], "options": {"toggle": "OFF"}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_bypass)
    api = cbcsdk_mock.api
    api.device_bypass([6023], False)


def test_device_delete_sensor(cbcsdk_mock):
    """Test deleting the sensor for a device."""
    def on_delete(url, body, **kwargs):
        assert body == {"action_type": "DELETE_SENSOR", "device_id": [6023]}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_delete)
    api = cbcsdk_mock.api
    api.device_delete_sensor([6023])


def test_device_uninstall_sensor(cbcsdk_mock):
    """Test uninstalling the sensor for a device."""
    def on_uninstall(url, body, **kwargs):
        assert body == {"action_type": "UNINSTALL_SENSOR", "device_id": [6023]}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_uninstall)
    api = cbcsdk_mock.api
    api.device_uninstall_sensor([6023])


def test_device_quarantine(cbcsdk_mock):
    """Test setting the quarantine status of a device."""
    def on_quarantine(url, body, **kwargs):
        assert body == {"action_type": "QUARANTINE", "device_id": [6023], "options": {"toggle": "ON"}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_quarantine)
    api = cbcsdk_mock.api
    api.device_quarantine([6023], True)


def test_device_update_policy(cbcsdk_mock):
    """Test updating the policy of a device."""
    def on_update(url, body, **kwargs):
        assert body == {"action_type": "UPDATE_POLICY", "device_id": [6023], "options": {"policy_id": 8675309}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_update)
    api = cbcsdk_mock.api
    api.device_update_policy([6023], 8675309)


def test_device_update_policy_error(cbcsdk_mock):
    """Test updating the policy of a device."""
    def on_update(url, body, **kwargs):
        assert body == {"action_type": "UPDATE_POLICY", "device_id": [6023], "options": {"policy_id": 8675309}}
        return CBCSDKMock.StubResponse(None, scode=500)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_update)
    api = cbcsdk_mock.api
    with pytest.raises(ServerError):
        api.device_update_policy([6023], 8675309)


def test_device_update_sensor_version(cbcsdk_mock):
    """Test updating the sensor version of a device."""
    def on_update(url, body, **kwargs):
        assert body == {"action_type": "UPDATE_SENSOR_VERSION", "device_id": [6023],
                        "options": {"sensor_version": {"RHEL": "2.3.4.5"}}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_update)
    api = cbcsdk_mock.api
    api.device_update_sensor_version([6023], {"RHEL": "2.3.4.5"})


def test_query_device_with_all_bells_and_whistles(cbcsdk_mock):
    """Test a device query with all options set."""
    def on_query(url, body, **kwargs):
        assert body == {"query": "foobar",
                        "rows": 2,
                        "criteria": {"ad_group_id": [14, 25], "os": ["LINUX"], "policy_id": [8675309],
                                     "status": ["ALL"], "target_priority": ["HIGH"], "deployment_type": ["ENDPOINT"]},
                        "exclusions": {"sensor_version": ["0.1"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        return {"results": [{"id": 6023, "organization_name": "thistestworks"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/devices/_search", on_query)
    api = cbcsdk_mock.api
    query = api.select(Device).where("foobar").set_ad_group_ids([14, 25]).set_os(["LINUX"]) \
        .set_policy_ids([8675309]).set_status(["ALL"]).set_target_priorities(["HIGH"]) \
        .set_exclude_sensor_versions(["0.1"]).sort_by("name", "DESC").set_deployment_type(["ENDPOINT"])
    d = query.one()
    assert d.id == 6023
    assert d.organization_name == "thistestworks"


def test_query_device_with_last_contact_time_as_start_end(cbcsdk_mock):
    """Test a device query with last_contact_time specified as starting and ending times."""
    def on_query(url, body, **kwargs):
        assert body == {"query": "foobar",
                        "rows": 2,
                        "criteria": {"last_contact_time": {"start": "2019-09-30T12:34:56",
                                                           "end": "2019-10-01T12:00:12"}}}
        return {"results": [{"id": 6023, "organization_name": "thistestworks"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/devices/_search", on_query)
    api = cbcsdk_mock.api
    query = api.select(Device).where("foobar") \
        .set_last_contact_time(start="2019-09-30T12:34:56", end="2019-10-01T12:00:12")
    d = query.one()
    assert d.id == 6023
    assert d.organization_name == "thistestworks"


def test_query_device_with_last_contact_time_as_range(cbcsdk_mock):
    """Test a device query with last_contact_time specified as a range."""
    def on_query(url, body, **kwargs):
        assert body == {
            "query": "foobar",
            "rows": 2,
            "criteria": {"last_contact_time": {"range": "-3w"}}
        }
        return {"results": [{"id": 6023, "organization_name": "thistestworks"}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/devices/_search", on_query)
    api = cbcsdk_mock.api
    query = api.select(Device).where("foobar").set_last_contact_time(range="-3w")
    d = query.one()
    assert d.id == 6023
    assert d.organization_name == "thistestworks"


def test_query_device_invalid_last_contact_time_combinations(cb):
    """Test handling of invalid value combinations for set_last_contact_time()."""
    with pytest.raises(ApiError):
        cb.select(Device).set_last_contact_time()
    with pytest.raises(ApiError):
        cb.select(Device).set_last_contact_time(start="2019-09-30T12:34:56", end="2019-10-01T12:00:12",
                                                range="-3w")
    with pytest.raises(ApiError):
        cb.select(Device).set_last_contact_time(start="2019-09-30T12:34:56", range="-3w")
    with pytest.raises(ApiError):
        cb.select(Device).set_last_contact_time(end="2019-10-01T12:00:12", range="-3w")


@pytest.mark.parametrize("method, arg", [
    ("set_ad_group_ids", ["Bogus"]),
    ("set_policy_ids", ["Bogus"]),
    ("set_os", ["COMMODORE_64"]),
    ("set_status", ["Bogus"]),
    ("set_target_priorities", ["Bogus"]),
    ("set_exclude_sensor_versions", [12703])
])
def test_query_device_invalid_criteria_values(cb, method, arg):
    """Test setting invalid values for device query criteria."""
    query = cb.select(Device)
    meth = getattr(query, method, None)
    with pytest.raises(ApiError):
        meth(arg)


def test_query_device_invalid_sort_direction(cb):
    """Test an attempt to sort device query results in an invalid direction."""
    with pytest.raises(ApiError):
        cb.select(Device).sort_by("policy_name", "BOGUS")


def test_query_device_facet(cbcsdk_mock):
    """Test the query faceting operation."""
    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/devices/_facet", FACET_RESPONSE)
    api = cbcsdk_mock.api
    query = api.select(Device).where('')
    facets = query.facets(['policy_id'])
    assert len(facets) == 1
    assert facets[0].field == 'policy_id'
    assert len(facets[0].values_) == 10
    with pytest.raises(ApiError):
        query.facets(['notexist'])
    with pytest.raises(ApiError):
        query.facets([])


@pytest.mark.parametrize('init_facet, desired_criteria', [
    (FACET_INIT_1, {'policy_id': [68727]}),
    (FACET_INIT_2, {'status': ['ACTIVE']}),
    (FACET_INIT_3, {'os': ['LINUX']}),
    (FACET_INIT_4, {'ad_group_id': [955]}),
    (FACET_INIT_5, {'cloud_provider_account_id': ['303']}),
    (FACET_INIT_6, {'auto_scaling_group_name': ['ARGON']}),
    (FACET_INIT_7, {'virtual_private_cloud_id': ['65534']})
])
def test_facet_generated_queries(cb, init_facet, desired_criteria):
    """Test to make sure the query_devices() API generates queries with the correct criteria."""
    facet = DeviceFacet(cb, None, init_facet)
    query = facet.values_[0].query_devices()
    request = query._build_request(-1, -1)
    assert request['criteria'] == desired_criteria


def test_query_device_download(cbcsdk_mock):
    """Test downloading the results of a device query as CSV."""
    def on_download(url, query_params, default):
        assert query_params == {"status": "ALL", "ad_group_id": "14,25", "policy_id": "8675309",
                                "target_priority": "HIGH", "query_string": "foobar", "sort_field": "name",
                                "sort_order": "DESC"}
        return "123456789,123456789,123456789"

    cbcsdk_mock.mock_request('RAW_GET', "/appservices/v6/orgs/test/devices/_search/download", on_download)
    api = cbcsdk_mock.api
    rc = api.select(Device).where("foobar").set_ad_group_ids([14, 25]).set_policy_ids([8675309]) \
        .set_status(["ALL"]).set_target_priorities(["HIGH"]).sort_by("name", "DESC").download()
    assert rc == "123456789,123456789,123456789"


def test_query_device_do_background_scan(cbcsdk_mock):
    """Test setting the background scan status on devices matched by a query."""
    def on_bgscan(url, body, **kwargs):
        assert body == {"action_type": "BACKGROUND_SCAN",
                        "search": {"query": "foobar"}, "options": {"toggle": "ON"}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_bgscan)
    api = cbcsdk_mock.api
    api.select(Device).where("foobar").background_scan(True)


def test_query_device_do_bypass(cbcsdk_mock):
    """Test setting the bypass status on devices matched by a query."""
    def on_bypass(url, body, **kwargs):
        assert body == {"action_type": "BYPASS",
                        "search": {"query": "foobar"}, "options": {"toggle": "OFF"}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_bypass)
    api = cbcsdk_mock.api
    api.select(Device).where("foobar").bypass(False)


def test_query_device_do_delete_sensor(cbcsdk_mock):
    """Test deleting the sensor on devices matched by a query."""
    def on_delete(url, body, **kwargs):
        assert body == {"action_type": "DELETE_SENSOR",
                        "search": {"query": "foobar"}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_delete)
    api = cbcsdk_mock.api
    api.select(Device).where("foobar").delete_sensor()


def test_query_device_do_uninstall_sensor(cbcsdk_mock):
    """Test uninstalling the sensor on devices matched by a query."""
    def on_uninstall(url, body, **kwargs):
        assert body == {"action_type": "UNINSTALL_SENSOR",
                        "search": {"query": "foobar"}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_uninstall)
    api = cbcsdk_mock.api
    api.select(Device).where("foobar").uninstall_sensor()


def test_query_device_do_quarantine(cbcsdk_mock):
    """Test setting the quarantine status on devices matched by a query."""
    def on_quarantine(url, body, **kwargs):
        assert body == {"action_type": "QUARANTINE",
                        "search": {"query": "foobar"}, "options": {"toggle": "ON"}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_quarantine)
    api = cbcsdk_mock.api
    api.select(Device).where("foobar").quarantine(True)


def test_query_device_do_update_policy(cbcsdk_mock):
    """Test updating the policy on devices matched by a query."""
    def on_update(url, body, **kwargs):
        assert body == {"action_type": "UPDATE_POLICY",
                        "search": {"query": "foobar"},
                        "options": {"policy_id": 8675309}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_update)
    api = cbcsdk_mock.api
    api.select(Device).where("foobar").update_policy(8675309)


def test_query_device_do_update_sensor_version(cbcsdk_mock):
    """Test updating the sensor version on devices matched by a query."""
    def on_update(url, body, **kwargs):
        assert body == {"action_type": "UPDATE_SENSOR_VERSION",
                        "search": {"query": "foobar"},
                        "options": {"sensor_version": {"RHEL": "2.3.4.5"}}}
        return CBCSDKMock.StubResponse(None, scode=204)

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/device_actions", on_update)
    api = cbcsdk_mock.api
    api.select(Device).where("foobar").update_sensor_version({"RHEL": "2.3.4.5"})


def test_query_deployment_type(cbcsdk_mock):
    """Test deployment type query with correct and incorrect params."""
    def on_query(url, body, **kwargs):
        assert body == {"rows": 2,
                        "criteria": {"deployment_type": ["ENDPOINT"]}}
        return {"results": [{"id": 6023, "deployment_type": ["ENDPOINT"]}], "num_found": 1}

    cbcsdk_mock.mock_request('POST', "/appservices/v6/orgs/test/devices/_search", on_query)
    api = cbcsdk_mock.api
    with pytest.raises(ApiError):
        api.select(Device).set_deployment_type(["BOGUS"])
    query = api.select(Device).set_deployment_type(["ENDPOINT"])
    d = query.one()
    assert d.deployment_type[0] in ["ENDPOINT", "WORKLOAD"]


def test_device_scroll(cbcsdk_mock):
    """Testing DeviceSearchQuery scroll"""
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/devices/_scroll",
                             GET_SCROLL_DEVICES(100, 200, 100))

    api = cbcsdk_mock.api
    query = api.select(Device).set_deployment_type(["ENDPOINT"])

    results = query.scroll(100)

    assert query.num_remaining == 100
    assert query._search_after == "MTcwMjMyMTM2MDU3OSwyMT"

    def on_post(url, body, **kwargs):
        """Test 2nd scroll request"""
        assert body == {
            "criteria": {
                "deployment_type": ["ENDPOINT"]
            },
            "rows": 10000,
            "search_after": "MTcwMjMyMTM2MDU3OSwyMT"
        }
        return GET_SCROLL_DEVICES(100, 200, 0)

    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/devices/_scroll",
                             on_post)

    results.extend(query.scroll(20000))

    assert len(results) == 200

    assert query.scroll(100) == []


def test_device_export(cbcsdk_mock):
    """Test the export functionality of the DeviceSearchQuery."""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/jobs/v1/orgs/test/jobs/11608915", EXPORT_JOB_REDIRECT)

    def post_validate(url, body, **kwargs):
        nonlocal api
        assert body['format'] == "CSV"

        # CBC Backend uses 303 Redirect which has been mocked out with follow up API call
        return api.get_object("/jobs/v1/orgs/test/jobs/11608915")

    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/devices/_export", post_validate)

    query = api.select(Device).set_status(["ACTIVE"])
    job = query.export()
    assert job
    assert isinstance(job, Job)
    assert job.id == 11608915
