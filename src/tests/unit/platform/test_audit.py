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

"""Tests for the audit logs APIs."""

import pytest
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.platform.audit import AuditLog
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.platform.mock_audit import AUDITLOGS_RESP


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


def test_no_create_object_for_now(cb):
    """Validates that we can't create an AuditLog object. Remove when we have a better implementation."""
    with pytest.raises(NotImplementedError):
        AuditLog(cb, 0)


def test_get_auditlogs(cbcsdk_mock):
    """Tests getting audit logs."""
    cbcsdk_mock.mock_request("GET", "/integrationServices/v3/auditlogs", AUDITLOGS_RESP)
    api = cbcsdk_mock.api
    result = AuditLog.get_auditlogs(api)
    assert len(result) == 5
