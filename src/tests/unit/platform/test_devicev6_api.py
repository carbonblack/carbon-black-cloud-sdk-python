# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
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
from cbc_sdk.errors import ApiError
from cbc_sdk.platform import Device
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.stubresponse import StubResponse, patch_cbc_sdk_api


def call_cbcloud_api():
    """Call the CBCloudAPI object"""
    return CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)


def test_get_device(monkeypatch):
    """Test simple retrieval of a Device object by ID."""
    _was_called = False

    def _get_device(url):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/devices/6023"
        _was_called = True
        return {"device_id": 6023, "organization_name": "thistestworks"}

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_device)
    rc = api.select(Device, 6023)
    assert _was_called
    assert isinstance(rc, Device)
    assert rc.device_id == 6023
    assert rc.organization_name == "thistestworks"


def test_device_background_scan(monkeypatch):
    """Test setting the background scan status of a device."""
    _was_called = False

    def _call_background_scan(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "BACKGROUND_SCAN", "device_id": [6023], "options": {"toggle": "ON"}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_call_background_scan)
    api.device_background_scan([6023], True)
    assert _was_called


def test_device_bypass(monkeypatch):
    """Test setting the bypass status of a device."""
    _was_called = False

    def _call_bypass(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "BYPASS", "device_id": [6023], "options": {"toggle": "OFF"}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_call_bypass)
    api.device_bypass([6023], False)
    assert _was_called


def test_device_delete_sensor(monkeypatch):
    """Test deleting the sensor for a device."""
    _was_called = False

    def _call_delete_sensor(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "DELETE_SENSOR", "device_id": [6023]}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_call_delete_sensor)
    api.device_delete_sensor([6023])
    assert _was_called


def test_device_uninstall_sensor(monkeypatch):
    """Test uninstalling the sensor for a device."""
    _was_called = False

    def _call_uninstall_sensor(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "UNINSTALL_SENSOR", "device_id": [6023]}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_call_uninstall_sensor)
    api.device_uninstall_sensor([6023])
    assert _was_called


def test_device_quarantine(monkeypatch):
    """Test setting the quarantine status of a device."""
    _was_called = False

    def _call_quarantine(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "QUARANTINE", "device_id": [6023], "options": {"toggle": "ON"}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_call_quarantine)
    api.device_quarantine([6023], True)
    assert _was_called


def test_device_update_policy(monkeypatch):
    """Test updating the policy of a device."""
    _was_called = False

    def _call_update_policy(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "UPDATE_POLICY", "device_id": [6023], "options": {"policy_id": 8675309}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_call_update_policy)
    api.device_update_policy([6023], 8675309)
    assert _was_called


def test_device_update_sensor_version(monkeypatch):
    """Test updating the sensor version of a device."""
    _was_called = False

    def _call_update_sensor_version(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "UPDATE_SENSOR_VERSION", "device_id": [6023],
                        "options": {"sensor_version": {"RHEL": "2.3.4.5"}}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_call_update_sensor_version)
    api.device_update_sensor_version([6023], {"RHEL": "2.3.4.5"})
    assert _was_called


def test_query_device_with_all_bells_and_whistles(monkeypatch):
    """Test a device query with all options set."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/devices/_search"
        assert body == {"query": "foobar",
                        "criteria": {"ad_group_id": [14, 25], "os": ["LINUX"], "policy_id": [8675309],
                                     "status": ["ALL"], "target_priority": ["HIGH"], "deployment_type": ["ENDPOINT"]},
                        "exclusions": {"sensor_version": ["0.1"]},
                        "sort": [{"field": "name", "order": "DESC"}]}
        _was_called = True
        return StubResponse({"results": [{"id": 6023, "organization_name": "thistestworks"}],
                             "num_found": 1})

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(Device).where("foobar").set_ad_group_ids([14, 25]).set_os(["LINUX"]) \
        .set_policy_ids([8675309]).set_status(["ALL"]).set_target_priorities(["HIGH"]) \
        .set_exclude_sensor_versions(["0.1"]).sort_by("name", "DESC").set_deployment_type(["ENDPOINT"])
    d = query.one()
    assert _was_called
    assert d.id == 6023
    assert d.organization_name == "thistestworks"


def test_query_device_with_last_contact_time_as_start_end(monkeypatch):
    """Test a device query with last_contact_time specified as starting and ending times."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/devices/_search"
        assert body == {"query": "foobar",
                        "criteria": {"last_contact_time": {"start": "2019-09-30T12:34:56",
                                                           "end": "2019-10-01T12:00:12"}}, "exclusions": {}}
        _was_called = True
        return StubResponse({"results": [{"id": 6023, "organization_name": "thistestworks"}],
                             "num_found": 1})

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(Device).where("foobar") \
        .set_last_contact_time(start="2019-09-30T12:34:56", end="2019-10-01T12:00:12")
    d = query.one()
    assert _was_called
    assert d.id == 6023
    assert d.organization_name == "thistestworks"


def test_query_device_with_last_contact_time_as_range(monkeypatch):
    """Test a device query with last_contact_time specified as a range."""
    _was_called = False

    def _run_query(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/devices/_search"
        assert body == {"query": "foobar", "criteria": {"last_contact_time": {"range": "-3w"}}, "exclusions": {}}
        _was_called = True
        return StubResponse({"results": [{"id": 6023, "organization_name": "thistestworks"}],
                             "num_found": 1})

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_run_query)
    query = api.select(Device).where("foobar").set_last_contact_time(range="-3w")
    d = query.one()
    assert _was_called
    assert d.id == 6023
    assert d.organization_name == "thistestworks"


def test_query_device_invalid_last_contact_time_combinations():
    """Test handling of invalid value combinations for set_last_contact_time()."""
    api = call_cbcloud_api()
    with pytest.raises(ApiError):
        api.select(Device).set_last_contact_time()
    with pytest.raises(ApiError):
        api.select(Device).set_last_contact_time(start="2019-09-30T12:34:56", end="2019-10-01T12:00:12",
                                                 range="-3w")
    with pytest.raises(ApiError):
        api.select(Device).set_last_contact_time(start="2019-09-30T12:34:56", range="-3w")
    with pytest.raises(ApiError):
        api.select(Device).set_last_contact_time(end="2019-10-01T12:00:12", range="-3w")


@pytest.mark.parametrize("method, arg", [
    ("set_ad_group_ids", ["Bogus"]),
    ("set_policy_ids", ["Bogus"]),
    ("set_os", ["COMMODORE_64"]),
    ("set_status", ["Bogus"]),
    ("set_target_priorities", ["Bogus"]),
    ("set_exclude_sensor_versions", [12703])
])
def test_query_device_invalid_criteria_values(method, arg):
    """Test setting invalid values for device query criteria."""
    api = call_cbcloud_api()
    query = api.select(Device)
    meth = getattr(query, method, None)
    with pytest.raises(ApiError):
        meth(arg)


def test_query_device_invalid_sort_direction():
    """Test an attempt to sort device query results in an invalid direction."""
    api = call_cbcloud_api()
    with pytest.raises(ApiError):
        api.select(Device).sort_by("policy_name", "BOGUS")


def test_query_device_download(monkeypatch):
    """Test downloading the results of a device query as CSV."""
    _was_called = False

    def _run_download(url, query_params, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/devices/_search/download"
        assert query_params == {"status": "ALL", "ad_group_id": "14,25", "policy_id": "8675309",
                                "target_priority": "HIGH", "query_string": "foobar", "sort_field": "name",
                                "sort_order": "DESC"}
        _was_called = True
        return "123456789,123456789,123456789"

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, RAW_GET=_run_download)
    rc = api.select(Device).where("foobar").set_ad_group_ids([14, 25]).set_policy_ids([8675309]) \
        .set_status(["ALL"]).set_target_priorities(["HIGH"]).sort_by("name", "DESC").download()
    assert _was_called
    assert rc == "123456789,123456789,123456789"


def test_query_device_do_background_scan(monkeypatch):
    """Test setting the background scan status on devices matched by a query."""
    _was_called = False

    def _background_scan(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "BACKGROUND_SCAN",
                        "search": {"query": "foobar", "criteria": {}, "exclusions": {}}, "options": {"toggle": "ON"}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_background_scan)
    api.select(Device).where("foobar").background_scan(True)
    assert _was_called


def test_query_device_do_bypass(monkeypatch):
    """Test setting the bypass status on devices matched by a query."""
    _was_called = False

    def _bypass(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "BYPASS",
                        "search": {"query": "foobar", "criteria": {}, "exclusions": {}}, "options": {"toggle": "OFF"}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_bypass)
    api.select(Device).where("foobar").bypass(False)
    assert _was_called


def test_query_device_do_delete_sensor(monkeypatch):
    """Test deleting the sensor on devices matched by a query."""
    _was_called = False

    def _delete_sensor(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "DELETE_SENSOR",
                        "search": {"query": "foobar", "criteria": {}, "exclusions": {}}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_delete_sensor)
    api.select(Device).where("foobar").delete_sensor()
    assert _was_called


def test_query_device_do_uninstall_sensor(monkeypatch):
    """Test uninstalling the sensor on devices matched by a query."""
    _was_called = False

    def _uninstall_sensor(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "UNINSTALL_SENSOR",
                        "search": {"query": "foobar", "criteria": {}, "exclusions": {}}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_uninstall_sensor)
    api.select(Device).where("foobar").uninstall_sensor()
    assert _was_called


def test_query_device_do_quarantine(monkeypatch):
    """Test setting the quarantine status on devices matched by a query."""
    _was_called = False

    def _quarantine(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "QUARANTINE",
                        "search": {"query": "foobar", "criteria": {}, "exclusions": {}}, "options": {"toggle": "ON"}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_quarantine)
    api.select(Device).where("foobar").quarantine(True)
    assert _was_called


def test_query_device_do_update_policy(monkeypatch):
    """Test updating the policy on devices matched by a query."""
    _was_called = False

    def _update_policy(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "UPDATE_POLICY",
                        "search": {"query": "foobar", "criteria": {}, "exclusions": {}},
                        "options": {"policy_id": 8675309}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_update_policy)
    api.select(Device).where("foobar").update_policy(8675309)
    assert _was_called


def test_query_device_do_update_sensor_version(monkeypatch):
    """Test updating the sensor version on devices matched by a query."""
    _was_called = False

    def _update_sensor_version(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "UPDATE_SENSOR_VERSION",
                        "search": {"query": "foobar", "criteria": {}, "exclusions": {}},
                        "options": {"sensor_version": {"RHEL": "2.3.4.5"}}}
        _was_called = True
        return StubResponse(None, 204)

    api = call_cbcloud_api()
    patch_cbc_sdk_api(monkeypatch, api, POST=_update_sensor_version)
    api.select(Device).where("foobar").update_sensor_version({"RHEL": "2.3.4.5"})
    assert _was_called


def test_query_deployment_type(monkeypatch):
    """Test deployment type query with correct and incorrect params."""
    api = call_cbcloud_api()

    def _invalid_deployment_type():
        with pytest.raises(ApiError):
            api.select(Device).set_deployment_type(["BOGUS"])

    _invalid_deployment_type()

    def _valid_deployment_type(url, body, **kwargs):
        assert url == "/appservices/v6/orgs/Z100/devices/_search"
        assert body == {"query": "",
                        "criteria": {"deployment_type": ["ENDPOINT"]},
                        "exclusions": {}}
        return StubResponse({"results": [{"id": 6023, "deployment_type": ["ENDPOINT"]}],
                             "num_found": 1})

    patch_cbc_sdk_api(monkeypatch, api, POST=_valid_deployment_type)
    query = api.select(Device).set_deployment_type(["ENDPOINT"])
    d = query.one()
    assert d.deployment_type[0] in ["ENDPOINT", "WORKLOAD"]
