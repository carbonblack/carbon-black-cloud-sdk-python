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

"""Testing functions which generate a v6 compatible out from using v7 APIs."""
import pytest

# Import Base Alert since we're testing backwards compatibility
from cbc_sdk.platform import BaseAlert
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.platform.mock_alert_v6_v7_compatibility import (
    ALERT_V6_INFO_CB_ANALYTICS_SDK_1_4_3,
    ALERT_V6_INFO_WATCHLIST_SDK_1_4_3,
    ALERT_V6_INFO_DEVICE_CONTROL_SDK_1_4_3,
    ALERT_V6_INFO_HBFW_SDK_1_4_3,
    ALERT_V6_INFO_CONTAINER_RUNTIME_SDK_1_4_3,
    GET_ALERT_v7_CB_ANALYTICS_RESPONSE,
    GET_ALERT_v7_WATCHLIST_RESPONSE,
    GET_ALERT_v7_DEVICE_CONTROL_RESPONSE,
    GET_ALERT_v7_HBFW_RESPONSE,
    GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE
)

from tests.unit.fixtures.CBCSDKMock import CBCSDKMock


@pytest.fixture(scope="function")
def cb():
    """Create CBCloudAPI singleton"""
    return CBCloudAPI(url="https://example.com", org_key="test", token="abcd/1234", ssl_verify=False)


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, cb):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, cb)


# ==================================== UNIT TESTS BELOW ====================================

# Fields that are not tested for mappings while bugs are fixed.
# When all bugs are fixed, SKIP_FIELDS should be empty and all tests should pass
SKIP_FIELDS = {
    "comment",  # cbapi-4969, TO DO DEFECT FOR CLASSIFICATION
    "created_by_event_id",  # CBAPI-4915, should be mapped from "primary_event_id"
    "threat_cause_process_guid",  # CBAPI-4915, should be mapped to process_guid
    "threat_cause_actor_md5",  # CBAPI-4915, should be mapped to process_md5
    "alert_classification",  # will be removed. CBAPI-4971
    # comment out the policy and rules to test these fields for other alert types. Expect container test to then fail
    # until the container alert bug is fixed
    "policy_name", "policy_id", "rule_id", "rule_name"  # CONTAINER_RUNTIME alerts only, CBAPI-4914.
}

# Fields that are special - consider extending tests later
# remediation can be empty string in v6, has "NO_REASON" in v7
COMPLEX_MAPPING_V6 = {
    "remediation",
    "threat_cause_actor_name",  # on CB Analytics, the record is truncated on v6 so will not match
    "process_name"  # just the file name on v6, full path on v7
}

# Fields on the v6 base or common alert object that do not have an equivalent in v7
BASE_FIELDS_V6 = {
    "group_details",
    "category",
    "threat_activity_c2",
    "threat_cause_threat_category",
    "alert_classification",
    "threat_cause_actor_process_pid"
}

# Fields on the v6 CB Analytics alert object that do not have an equivalent in v7
CB_ANALYTICS_FIELDS_V6 = {
    "blocked_threat_category",
    "kill_chain_status",
    "not_blocked_threat_category",
    "threat_activity_c2",
    "threat_activity_dlp",
    "threat_activity_phish",
    "threat_cause_vector"
}

# Fields on the v6 Device Control alert object that do not have an equivalent in v7
DEVICE_CONTROL_FIELDS_V6 = {"threat_cause_vector"}

# Fields on the v6 Container Runtime alert object that do not have an equivalent in v7
CONTAINER_RUNTIME_FIELDS_V6 = {
    "workload_id",
    "target_value"
}

# Fields on the v6 Watchlist alert object that do not have an equivalent in v7
WATCHLIST_FIELDS_V6 = {
    "count",
    "document_guid",
    "threat_cause_vector",
    "threat_indicators"
}

# Aggregate all the alert type fields
ALL_FIELDS_V6 = (CB_ANALYTICS_FIELDS_V6 | BASE_FIELDS_V6 | DEVICE_CONTROL_FIELDS_V6 | WATCHLIST_FIELDS_V6
                 | CONTAINER_RUNTIME_FIELDS_V6 | SKIP_FIELDS)


@pytest.mark.parametrize("url, v7_api_response, v6_sdk_response", [
    ("/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333", GET_ALERT_v7_CB_ANALYTICS_RESPONSE,
     ALERT_V6_INFO_CB_ANALYTICS_SDK_1_4_3),
    ("/api/alerts/v7/orgs/test/alerts/f6af290d-6a7f-461c-a8af-cf0d24311105", GET_ALERT_v7_WATCHLIST_RESPONSE,
     ALERT_V6_INFO_WATCHLIST_SDK_1_4_3),
    ("/api/alerts/v7/orgs/test/alerts/46b419c8-3d67-ead8-dbf1-9d8417610fac", GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE,
     ALERT_V6_INFO_CONTAINER_RUNTIME_SDK_1_4_3),
    ("/api/alerts/v7/orgs/test/alerts/2be0652f-20bc-3311-9ded-8b873e28d830", GET_ALERT_v7_HBFW_RESPONSE,
     ALERT_V6_INFO_HBFW_SDK_1_4_3),
    ("/api/alerts/v7/orgs/test/alerts/b6a7e48b-1d14-11ee-a9e0-888888888788", GET_ALERT_v7_DEVICE_CONTROL_RESPONSE,
     ALERT_V6_INFO_DEVICE_CONTROL_SDK_1_4_3)
])
def test_v7_generate_v6_json(cbcsdk_mock, url, v7_api_response, v6_sdk_response):
    """
    Test the generation of a v6 to_json output

    Compare what is generated by the current SDK with expected from SDK 1.4.3
    Parameterization above is used to call this test multiple times to test different alert types
    """
    # set up the mock request and execute the mock v7 API call
    cbcsdk_mock.mock_request("GET", url, v7_api_response)
    api = cbcsdk_mock.api
    alert = api.select(BaseAlert, v6_sdk_response.get("id"))
    print("\n\nStarting comparison of {} type alerts".format(alert.get("type")))
    # generate the json output from the v7 API response in the v6 format
    alert_v6_from_v7 = alert.to_json("v6")

    # Recursively compare each field in the fixture v6 with that produced using the to_json method in the current SDK.
    # The v6 fixture were generated with an earlier version of the SDK (1.4.3)
    # The v7 fixtures were generated with v7 API calls
    # That the output of the current to_json("v6") method equals the v6 fixture is what is being tested
    for key in v6_sdk_response:
        # print("key = {}".format(key)) # helpful for troubleshooting
        """Check inner dictionaries"""
        if isinstance(v6_sdk_response.get(key), dict):
            check_dict(v6_sdk_response.get(key), alert_v6_from_v7.get(key), key, v6_sdk_response.get("type"))
        else:
            # send the dict containing the field as the field will not always exist in alert_v6_from_v7
            check_field(v6_sdk_response, alert_v6_from_v7, key, v6_sdk_response.get("type"))


def check_dict(alert_v6, alert_v6_from_v7, key, alert_type):
    """
    Make some generic checks for fields

    Key should be the label, and each of alert_v6 and alert_v6_from_v7 should be dicts
    """
    if key in SKIP_FIELDS:
        print("Handling known bug.  Field {}".format(key))
        return
    if key in COMPLEX_MAPPING_V6:
        print("Complex mapping, ignore.  Field {}".format(key))
        return
    # Fields that are deprecated will be in v6 and should not be in v7
    assert not (
        key in BASE_FIELDS_V6 and key in alert_v6_from_v7
    ), ("ERROR: Field is deprecated and does not exist in v7. Expected: Not in to_json(v6). Actual: was incorrectly "
        "included. Source: BASE_FIELDS_V6. Key: {}").format(key)

    # fields from cb analytics that are not in v7. No mapping available
    assert not (
        alert_type == "CB_ANALYTICS" and key in CB_ANALYTICS_FIELDS_V6 and key in alert_v6_from_v7
    ), ("ERROR: Field is deprecated and does not exist in v7. Expected: Not in to_json(v6). Actual: was incorrectly "
        "included. Source: CB_ANALYTICS_FIELDS_V6. Key: {}").format(key)

    # fields from container runtime that are not in v7. No mapping available
    assert not (alert_type == "CONTAINER_RUNTIME" and key in CONTAINER_RUNTIME_FIELDS_V6 and key in alert_v6_from_v7), (
        ("ERROR: Field is deprecated and does not exist in v7. Expected: Not in to_json(v6). Actual: was incorrectly "
         "included. Source: CONTAINER_RUNTIME_FIELDS_V6. Key: {}").format(key))

    # no fields removed in v7 for host based firewall alerts
    # fields from device control that are not in v7. No mapping available
    assert not (
        alert_type == "DEVICE_CONTROL" and key in DEVICE_CONTROL_FIELDS_V6 and key in alert_v6_from_v7
    ), ("ERROR: Field is deprecated and does not exist in v7. Expected: Not in to_json(v6). Actual: was incorrectly "
        "included. Source: DEVICE_CONTROL_FIELDS_V6. Key: {}").format(
        key)

    # fields from watchlist alert that are not in v7. No mapping available
    assert not (
        alert_type == "WATCHLIST" and key in WATCHLIST_FIELDS_V6 and key in alert_v6_from_v7
    ), ("ERROR: Field is deprecated and does not exist in v7. Expected: Not in to_json(v6). Actual: was incorrectly "
        "included. Source: WATCHLIST_FIELDS_V6. Key: {}").format(key)

    # check dict recursively
    # defensively coded.  This method should only be called with dicts, but avoid crashing
    assert(isinstance(alert_v6, dict)), "Function check_dict called with incorrect argument types"

    for inner_key in alert_v6:
        if isinstance(alert_v6.get(inner_key), dict):
            check_dict(alert_v6.get(inner_key), alert_v6_from_v7.get(inner_key), inner_key, alert_type)
        else:
            check_field(alert_v6, alert_v6_from_v7, inner_key, alert_type)


def check_field(alert_v6, alert_v6_from_v7, key, alert_type):
    """
    Check rules about when fields should and should not be mapped

    Orgs are dictionaries, key is the field being evaluated.
    End with a value comparison
    """
    if key in SKIP_FIELDS:
        print("Handling known bug.  Field {}".format(key))
        return
    if key in COMPLEX_MAPPING_V6:
        print("Complex mapping, ignore.  Field {}".format(key))
        return
    # Fields that are deprecated will be in v6 and should not be in v7
    assert not (
        key in BASE_FIELDS_V6 and key in alert_v6_from_v7
    ), ("ERROR: Field is deprecated and does not exist in v7. Expected: Not in to_json(v6). Actual: was incorrectly "
        "included. Source: BASE_FIELDS_V6. Key: {}").format(key)

    # fields from cb analytics that are not in v7. No mapping available
    assert not (
        alert_type == "CB_ANALYTICS" and key in CB_ANALYTICS_FIELDS_V6 and key in alert_v6_from_v7
    ), ("ERROR: Field is deprecated and does not exist in v7. Expected: Not in to_json(v6). Actual: was incorrectly "
        "included. Source: CB_ANALYTICS_FIELDS_V6. Key: {}").format(key)

    # container runtime alerts
    # fields from watchlist alert that are not in v7. No mapping available
    assert not (alert_type == "CONTAINER_RUNTIME" and key in CONTAINER_RUNTIME_FIELDS_V6 and key in alert_v6_from_v7), (
        ("ERROR: Field is deprecated and does not exist in v7. Expected: Not in to_json(v6). Actual: was incorrectly "
         "included. Source: CONTAINER_RUNTIME_FIELDS_V6. Key: {}").format(key))

    # no fields removed in v7 for host based firewall alerts
    # fields from device control that are not in v7. No mapping available
    assert not (
        alert_type == "DEVICE_CONTROL" and key in DEVICE_CONTROL_FIELDS_V6 and key in alert_v6_from_v7
    ), ("ERROR: Field is deprecated and does not exist in v7. Expected: Not in to_json(v6). Actual: was incorrectly "
        "included. Source: DEVICE_CONTROL_FIELDS_V6. Key: {}").format(
        key)

    # fields from watchlist alert that are not in v7. No mapping available
    assert not (
        alert_type == "WATCHLIST" and key in WATCHLIST_FIELDS_V6 and key in alert_v6_from_v7
    ), ("ERROR: Field is deprecated and does not exist in v7. Expected: Not in to_json(v6). Actual: was incorrectly "
        "included. Source: WATCHLIST_FIELDS_V6. Key: {}").format(key)

    if key not in ALL_FIELDS_V6:
        assert (alert_v6.get(key) == alert_v6_from_v7.get(key)
                or (alert_v6.get(key) == "" and alert_v6_from_v7.get(key) is None)
                or (alert_v6.get(key) == 0 and alert_v6_from_v7.get(key) is None)  # device info on CONTAINER_RUNTIME
                ), "ERROR: Values do not match {} - v6: {} v7: {}".format(key, alert_v6.get(key),
                                                                          alert_v6_from_v7.get(key))
