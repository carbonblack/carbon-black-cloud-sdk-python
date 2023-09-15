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

"""Tests of the Alerts V6 features that are not supported in Alerts v7, SDK v1.5.0 onwards."""
import pytest

from cbc_sdk.errors import FunctionalityDecommissioned
from cbc_sdk.platform import (
    BaseAlert,
    CBAnalyticsAlert,
    WatchlistAlert,
    DeviceControlAlert,
    ContainerRuntimeAlert,
    WorkflowStatus,
    Process,
)
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.platform.mock_alert_v6_v7_compatibility import (
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
    return CBCloudAPI(url="https://example.com",
                      org_key="test",
                      token="abcd/1234",
                      ssl_verify=False)


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, cb):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, cb)


# ==================================== UNIT TESTS BELOW ====================================


# @pytest.mark.parametrize("url, v7_api_response", [
#    ("/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333", GET_ALERT_v7_CB_ANALYTICS_RESPONSE),
#    ("/api/alerts/v7/orgs/test/alerts/f6af290d-6a7f-461c-a8af-cf0d24311105", GET_ALERT_v7_WATCHLIST_RESPONSE),
#    ("/api/alerts/v7/orgs/test/alerts/46b419c8-3d67-ead8-dbf1-9d8417610fac", GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE),
#    ("/api/alerts/v7/orgs/test/alerts/2be0652f-20bc-3311-9ded-8b873e28d830", GET_ALERT_v7_HBFW_RESPONSE),
#    ("/api/alerts/v7/orgs/test/alerts/b6a7e48b-1d14-11ee-a9e0-888888888788", GET_ALERT_v7_DEVICE_CONTROL_RESPONSE)
# ])

def test_set_categories(cbcsdk_mock): #, url, v7_api_response):
    """Test the set_categories method on each legacy alert class."""

    cbcsdk_mock.mock_request("GET", "/api/alerts/v7/orgs/test/alerts/6f1173f5-f921-8e11-2160-edf42b799333", GET_ALERT_v7_CB_ANALYTICS_RESPONSE)
    api = cbcsdk_mock.api
    with pytest.raises(FunctionalityDecommissioned) as e_info:
        alert_list = api.select(BaseAlert).set_categories("MONITORED")

