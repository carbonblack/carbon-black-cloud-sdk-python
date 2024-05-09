# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2024. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Tests of the Alerts V6 features that are not supported in Alerts v7, SDK v1.5.0 onwards."""
import pytest

from cbc_sdk.errors import FunctionalityDecommissioned
from cbc_sdk.platform import (
    Alert,
    BaseAlert,
    CBAnalyticsAlert,
    WatchlistAlert,
    DeviceControlAlert,
    ContainerRuntimeAlert,
    HostBasedFirewallAlert
)
from cbc_sdk.rest_api import CBCloudAPI

from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_alert_v6_v7_compatibility import (
    GET_ALERT_v7_CB_ANALYTICS_RESPONSE,
    GET_ALERT_v7_WATCHLIST_RESPONSE,
    GET_ALERT_v7_DEVICE_CONTROL_RESPONSE,
    GET_ALERT_v7_HBFW_RESPONSE,
    GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE
)

# Legacy alert types to test methods against as each sub-type may override the baseAlert implementation
# Base Alert does not support the string as class name, called as the base case in each test.
ALERT_TYPES = [
    "CBAnalyticsAlert",
    "WatchlistAlert",
    "DeviceControlAlert",
    "ContainerRuntimeAlert",
    "HostBasedFirewallAlert"
]

DEPRECATED_FIELDS_CB_ANALYTICS = [
    "blocked_threat_category",
    "kill_chain_status",
    "not_blocked_threat_category",
    "threat_activity_dlp",
    "threat_activity_phish",
    "threat_cause_vector",
    "category",
    "group_details",
    "threat_cause_threat_category"
]

DEPRECATED_FIELDS_WATCHLISTS = [
    "category",
    "group_details",
    "threat_cause_threat_category",
    "threat_cause_vector",
    "count",
    "document_guid",
    "threat_indicators"
]

DEPRECATED_FIELDS_DEVICE_CONTROL = [
    "category",
    "group_details",
    "threat_cause_threat_category",
    "threat_cause_vector"
]

DEPRECATED_FIELDS_CONTAINER_RUNTIME = [
    "target_value",
    "category",
    "group_details",
    "workload_id",
    "threat_cause_threat_category"
]

DEPRECATED_FIELDS_HBFW = [
    "category",
    "group_details",
    "threat_cause_threat_category"
]


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

def test_set_categories(cb):
    """Test the set_categories method on each legacy alert class."""
    with pytest.raises(FunctionalityDecommissioned):
        cb.select(BaseAlert).set_categories(["MONITORED"])

    for a_type in ALERT_TYPES:
        with pytest.raises(FunctionalityDecommissioned):
            cb.select(a_type).set_categories(["MONITORED"])


def test_set_group_results(cb):
    """Test the set_categories method on each legacy alert class."""
    with pytest.raises(FunctionalityDecommissioned):
        cb.select(BaseAlert).set_group_results(False)

    for a_type in ALERT_TYPES:
        with pytest.raises(FunctionalityDecommissioned):
            cb.select(a_type).set_group_results(False)


def test_set_kill_chain_statuses(cb):
    """Test the set_kill_chain_statuses method on each legacy alert class."""
    with pytest.raises(FunctionalityDecommissioned):
        cb.select(BaseAlert).set_kill_chain_statuses(["WEAPONIZE"])

    for a_type in ALERT_TYPES:
        with pytest.raises(FunctionalityDecommissioned):
            cb.select(a_type).set_kill_chain_statuses(["WEAPONIZE"])


def test_set_blocked_threat_categories(cb):
    """Test the set_kill_chain_statuses method on base and CBAnalytics legacy alert class."""
    with pytest.raises(FunctionalityDecommissioned):
        cb.select(BaseAlert).set_blocked_threat_categories(["UNKNOWN"])

    with pytest.raises(FunctionalityDecommissioned):
        cb.select(CBAnalyticsAlert).set_blocked_threat_categories(["UNKNOWN"])


def test_set_not_blocked_threat_categories(cb):
    """Test the set_kill_chain_statuses method on base and CBAnalytics legacy alert class."""
    with pytest.raises(FunctionalityDecommissioned):
        cb.select(BaseAlert).set_not_blocked_threat_categories(["UNKNOWN"])

    with pytest.raises(FunctionalityDecommissioned):
        cb.select(CBAnalyticsAlert).set_not_blocked_threat_categories(["UNKNOWN"])


def test_set_threat_cause_vectors(cb):
    """Test the set_kill_chain_statuses method on base and CBAnalytics legacy alert class."""
    with pytest.raises(FunctionalityDecommissioned):
        cb.select(BaseAlert).set_threat_cause_vectors(["EMAIL"])

    with pytest.raises(FunctionalityDecommissioned):
        cb.select(CBAnalyticsAlert).set_threat_cause_vectors(["EMAIL"])

    with pytest.raises(FunctionalityDecommissioned):
        cb.select(DeviceControlAlert).set_threat_cause_vectors(["EMAIL"])

    with pytest.raises(FunctionalityDecommissioned):
        cb.select(WatchlistAlert).set_threat_cause_vectors(["EMAIL"])


def test_set_workload_ids(cb):
    """Test the set_kill_chain_statuses method on base and CBAnalytics legacy alert class."""
    with pytest.raises(FunctionalityDecommissioned):
        cb.select(BaseAlert).set_workload_ids(["UNKNOWN"])

    with pytest.raises(FunctionalityDecommissioned):
        cb.select(ContainerRuntimeAlert).set_workload_ids(["UNKNOWN"])


def test_get_attr_cb_analytics_alert(cbcsdk_mock):
    """Test the __get_attr_ method for each attribute that applies to cb_analytics alerts."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(BaseAlert, GET_ALERT_v7_CB_ANALYTICS_RESPONSE.get("id"))

    for f in DEPRECATED_FIELDS_CB_ANALYTICS:
        with (pytest.raises(FunctionalityDecommissioned)):
            alert.get(f)

    # test again with CBAnalyticsAlert class
    alert = cb.select(CBAnalyticsAlert, GET_ALERT_v7_CB_ANALYTICS_RESPONSE.get("id"))

    for f in DEPRECATED_FIELDS_CB_ANALYTICS:
        with (pytest.raises(FunctionalityDecommissioned)):
            alert.get(f)


def test_get_on_basealert_class(cbcsdk_mock):
    """Test the get() method for one valid v7 attribute for the BaseAlert.get() method that overrides base.py."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(BaseAlert, GET_ALERT_v7_CB_ANALYTICS_RESPONSE.get("id"))

    val = alert.get("reason_code")
    assert "T_REP_VIRUS" == val


def test_get_on_alert_class(cbcsdk_mock):
    """Test the get() method for one valid v7 attribute for the new Alert.get() method that overrides base.py."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(Alert, GET_ALERT_v7_CB_ANALYTICS_RESPONSE.get("id"))

    val = alert.get("reason_code")
    assert "T_REP_VIRUS" == val


def test_get_on_cbanalytics_alert_class(cbcsdk_mock):
    """Test the get() method for one valid v7 attribute for the CBAnalyticsAlert.get() method that overrides base.py."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(CBAnalyticsAlert, GET_ALERT_v7_CB_ANALYTICS_RESPONSE.get("id"))

    val = alert.get("reason_code")
    assert "T_REP_VIRUS" == val


def test_get_attr_container_runtime_alert(cbcsdk_mock):
    """Test the __get_attr_ method for each attribute that applies to container runtime alerts."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/46b419c8-3d67-ead8-dbf1-9d8417610fac",
                             GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(BaseAlert, GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE.get("id"))

    for f in DEPRECATED_FIELDS_CONTAINER_RUNTIME:
        with (pytest.raises(FunctionalityDecommissioned)):
            alert.get(f)

    # test again with Container Runtime class
    alert = cb.select(ContainerRuntimeAlert, GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE.get("id"))

    for f in DEPRECATED_FIELDS_CONTAINER_RUNTIME:
        with (pytest.raises(FunctionalityDecommissioned)):
            alert.get(f)


def test_get_attr_device_control_alert(cbcsdk_mock):
    """Test the __get_attr_ method for each attribute that applies to device control alerts."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/b6a7e48b-1d14-11ee-a9e0-888888888788",
                             GET_ALERT_v7_DEVICE_CONTROL_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(BaseAlert, GET_ALERT_v7_DEVICE_CONTROL_RESPONSE.get("id"))

    for f in DEPRECATED_FIELDS_DEVICE_CONTROL:
        with (pytest.raises(FunctionalityDecommissioned)):
            alert.get(f)

    # test again with Device Control class
    alert = cb.select(DeviceControlAlert, GET_ALERT_v7_DEVICE_CONTROL_RESPONSE.get("id"))

    for f in DEPRECATED_FIELDS_DEVICE_CONTROL:
        with (pytest.raises(FunctionalityDecommissioned)):
            alert.get(f)


def test_get_attr_hbfw_alert(cbcsdk_mock):
    """Test the __get_attr_ method for each attribute that applies to host based firewall alerts."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/2be0652f-20bc-3311-9ded-8b873e28d830",
                             GET_ALERT_v7_HBFW_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(BaseAlert, GET_ALERT_v7_HBFW_RESPONSE.get("id"))

    for f in DEPRECATED_FIELDS_HBFW:
        with (pytest.raises(FunctionalityDecommissioned)):
            alert.get(f)

    # test again with Host Based Firewall class
    alert = cb.select(HostBasedFirewallAlert, GET_ALERT_v7_HBFW_RESPONSE.get("id"))

    for f in DEPRECATED_FIELDS_HBFW:
        with (pytest.raises(FunctionalityDecommissioned)):
            alert.get(f)


def test_get_attr_watchlists_alert(cbcsdk_mock):
    """Test the __get_attr_ method for each attribute that applies to watchlist alerts."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/f6af290d-6a7f-461c-a8af-cf0d24311105",
                             GET_ALERT_v7_WATCHLIST_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(BaseAlert, GET_ALERT_v7_WATCHLIST_RESPONSE.get("id"))

    for f in DEPRECATED_FIELDS_WATCHLISTS:
        with (pytest.raises(FunctionalityDecommissioned)):
            alert.get(f)

    # test again with Watchlist class
    alert = cb.select(WatchlistAlert, GET_ALERT_v7_WATCHLIST_RESPONSE.get("id"))

    for f in DEPRECATED_FIELDS_WATCHLISTS:
        with (pytest.raises(FunctionalityDecommissioned)):
            alert.get(f)


def test_get_attr_alert_invalid_attrib(cbcsdk_mock):
    """Test the __get_attr_ method for an invalid attribute on Alert."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(Alert, GET_ALERT_v7_CB_ANALYTICS_RESPONSE.get("id"))

    with (pytest.raises(AttributeError)):
        alert.invalid_field


def test_get_attr_basealert_invalid_attrib(cbcsdk_mock):
    """Test the __get_attr_ method for an invalid attribute on BaseAlert."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(BaseAlert, GET_ALERT_v7_CB_ANALYTICS_RESPONSE.get("id"))

    with (pytest.raises(AttributeError)):
        alert.invalid_field


def test_get_attr_cbalnalyticsalert_invalid_attrib(cbcsdk_mock):
    """Test the __get_attr_ method for an invalid attribute on CBAnalyticsAlert."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(CBAnalyticsAlert, GET_ALERT_v7_CB_ANALYTICS_RESPONSE.get("id"))

    with (pytest.raises(AttributeError)):
        alert.invalid_field


def test_get_attr_alert_deprecated_v6_attrib(cbcsdk_mock):
    """Test the __get_attr_ method for a v6 attribute that has been deprecated."""
    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333",
                             GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    cb = cbcsdk_mock.api
    alert = cb.select(Alert, GET_ALERT_v7_CB_ANALYTICS_RESPONSE.get("id"))

    with (pytest.raises(FunctionalityDecommissioned)):
        alert.kill_chain_status
