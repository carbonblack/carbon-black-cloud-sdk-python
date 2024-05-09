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

"""Testing NetworkThreatMetadata objects of cbc_sdk.platform"""

import pytest
import logging

from cbc_sdk.platform.network_threat_metadata import NetworkThreatMetadata
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.errors import ApiError
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_network_threat_metadata import GET_NETWORK_THREAT_METADATA_RESP

log = logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    level=logging.DEBUG,
    filename="log.txt",
)


@pytest.fixture(scope="function")
def cb():
    """Create CBCloudAPI singleton"""
    return CBCloudAPI(
        url="https://example.com", org_key="test", token="abcd/1234", ssl_verify=False
    )


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, cb):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, cb)


# ==================================== UNIT TESTS BELOW ====================================

def test_get_threat_metadata(cbcsdk_mock):
    """Testing get network threat metadata"""
    cbcsdk_mock.mock_request(
        "GET",
        "/threatmetadata/v1/orgs/test/detectors/8a4b43c5-5e0a-4f7d-aa46-bd729f1989a7",
        GET_NETWORK_THREAT_METADATA_RESP,
    )

    api = cbcsdk_mock.api
    threat_meta_data = api.select(
        NetworkThreatMetadata, "8a4b43c5-5e0a-4f7d-aa46-bd729f1989a7"
    )
    assert threat_meta_data["detector_abstract"]
    assert threat_meta_data["detector_goal"]
    assert threat_meta_data["threat_public_comment"]


def test_get_threat_metadata_without_id(cbcsdk_mock):
    """Testing get network threat metadata - exception"""
    api = cbcsdk_mock.api
    with pytest.raises(ApiError):
        api.select(NetworkThreatMetadata, "")


def test_get_threat_metadata_query(cbcsdk_mock):
    """Testing get network threat metadata - exception"""
    api = cbcsdk_mock.api
    with pytest.raises(NotImplementedError):
        api.select(NetworkThreatMetadata)
