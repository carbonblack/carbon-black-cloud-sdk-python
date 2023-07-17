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

"""Tests of the model object methods in the Platform API."""

import pytest
from cbc_sdk.platform import Device, BaseAlert, WorkflowStatus
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.stubresponse import StubResponse, patch_cbc_sdk_api


class StubScheduler:
    """Stub for the LiveResponse scheduler."""
    def __init__(self, expected_id):
        """
        Initialize the stub scheduler object.

        Args:
            expected_id (int): The expected sensor ID to use on the request.
        """
        self.expected_id = expected_id
        self.was_called = False

    def request_session(self, sensor_id, async_mode=False):
        """
        Stub out the request_session call to the scheduler.

        Args:
            sensor_id (int): Sensor ID the session is being requested for.

        Returns:
            dict: Simple value to prove that this works.
        """
        assert sensor_id == self.expected_id
        self.was_called = True
        return {"itworks": True}


def test_Device_lr_session(monkeypatch):
    """Test the call to set up a Live Response session for a device."""
    def _get_session(url, parms=None, default=None):
        assert url == "/appservices/v6/orgs/Z100/devices/6023"
        return {"id": 6023}

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    sked = StubScheduler(6023)
    api._lr_scheduler = sked
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_session)
    dev = Device(api, 6023, {"id": 6023})
    sess = dev.lr_session()
    assert sess["itworks"]
    assert sked.was_called


def test_Device_background_scan(monkeypatch):
    """Test the call to set the background scan status for a device."""
    _was_called = False

    def _get_device(url, parms=None, default=None):
        assert url == "/appservices/v6/orgs/Z100/devices/6023"
        return {"id": 6023}

    def _background_scan(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "BACKGROUND_SCAN", "device_id": [6023], "options": {"toggle": "ON"}}
        _was_called = True
        return StubResponse(None, 204)

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_device, POST=_background_scan)
    dev = Device(api, 6023, {"id": 6023})
    dev.background_scan(True)
    assert _was_called


def test_Device_bypass(monkeypatch):
    """Test the call to set the bypass status for a device."""
    _was_called = False

    def _get_device(url, parms=None, default=None):
        assert url == "/appservices/v6/orgs/Z100/devices/6023"
        return {"id": 6023}

    def _bypass(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "BYPASS", "device_id": [6023], "options": {"toggle": "OFF"}}
        _was_called = True
        return StubResponse(None, 204)

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_device, POST=_bypass)
    dev = Device(api, 6023, {"id": 6023})
    dev.bypass(False)
    assert _was_called


def test_Device_delete_sensor(monkeypatch):
    """Test the call to delete the sensor for a device."""
    _was_called = False

    def _get_device(url, parms=None, default=None):
        assert url == "/appservices/v6/orgs/Z100/devices/6023"
        return {"id": 6023}

    def _delete_sensor(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "DELETE_SENSOR", "device_id": [6023]}
        _was_called = True
        return StubResponse(None, 204)

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_device, POST=_delete_sensor)
    dev = Device(api, 6023, {"id": 6023})
    dev.delete_sensor()
    assert _was_called


def test_Device_uninstall_sensor(monkeypatch):
    """Test the call to uninstall the sensor for a device."""
    _was_called = False

    def _get_device(url, parms=None, default=None):
        assert url == "/appservices/v6/orgs/Z100/devices/6023"
        return {"id": 6023}

    def _uninstall_sensor(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "UNINSTALL_SENSOR", "device_id": [6023]}
        _was_called = True
        return StubResponse(None, 204)

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_device, POST=_uninstall_sensor)
    dev = Device(api, 6023, {"id": 6023})
    dev.uninstall_sensor()
    assert _was_called


def test_Device_quarantine(monkeypatch):
    """Test the call to set the quarantine status of a device."""
    _was_called = False

    def _get_device(url, parms=None, default=None):
        assert url == "/appservices/v6/orgs/Z100/devices/6023"
        return {"id": 6023}

    def _quarantine(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "QUARANTINE", "device_id": [6023], "options": {"toggle": "ON"}}
        _was_called = True
        return StubResponse(None, 204)

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_device, POST=_quarantine)
    dev = Device(api, 6023, {"id": 6023})
    dev.quarantine(True)
    assert _was_called


def test_Device_update_policy(monkeypatch):
    """Test the call to update policy for a device."""
    _was_called = False

    def _get_device(url, parms=None, default=None):
        assert url == "/appservices/v6/orgs/Z100/devices/6023"
        return {"id": 6023}

    def _update_policy(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "UPDATE_POLICY", "device_id": [6023], "options": {"policy_id": 8675309}}
        _was_called = True
        return StubResponse(None, 204)

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_device, POST=_update_policy)
    dev = Device(api, 6023, {"id": 6023})
    dev.update_policy(8675309)
    assert _was_called


def test_Device_update_sensor_version(monkeypatch):
    """Test the call to update the sensor version for a device."""
    _was_called = False

    def _get_device(url, parms=None, default=None):
        assert url == "/appservices/v6/orgs/Z100/devices/6023"
        return {"id": 6023}

    def _update_sensor_version(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/device_actions"
        assert body == {"action_type": "UPDATE_SENSOR_VERSION", "device_id": [6023],
                        "options": {"sensor_version": {"RHEL": "2.3.4.5"}}}
        _was_called = True
        return StubResponse(None, 204)

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_device, POST=_update_sensor_version)
    dev = Device(api, 6023, {"id": 6023})
    dev.update_sensor_version({"RHEL": "2.3.4.5"})
    assert _was_called


def test_BaseAlert_dismiss(monkeypatch):
    """Test dismissal of an alert."""
    _was_called = False

    def _do_dismiss(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/appservices/v6/orgs/Z100/alerts/ESD14U2C/workflow"
        assert body == {"state": "DISMISSED", "remediation_state": "Fixed", "comment": "Yessir"}
        _was_called = True
        return StubResponse({"state": "DISMISSED", "remediation": "Fixed", "comment": "Yessir",
                             "changed_by": "Robocop", "last_update_time": "2019-10-31T16:03:13.951Z"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_do_dismiss)
    alert = BaseAlert(api, "ESD14U2C", {"id": "ESD14U2C", "workflow": {"state": "OPEN"}})
    alert.dismiss("Fixed", "Yessir")
    assert _was_called
    assert alert.workflow_.changed_by == "Robocop"
    assert alert.workflow_.state == "DISMISSED"
    assert alert.workflow_.remediation == "Fixed"
    assert alert.workflow_.comment == "Yessir"
    assert alert.workflow_.last_update_time == "2019-10-31T16:03:13.951Z"


def test_BaseAlert_undismiss(monkeypatch):
    """Test undismissal of an alert."""
    _was_called = False

    def _do_update(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/api/alerts/v7/orgs/Z100/alerts/ESD14U2C/workflow"
        assert body == {"status": "OPEN", "remediation_state": "Fixed", "comment": "NoSir"}
        _was_called = True
        return StubResponse({"status": "OPEN", "closure_reason": "Fixed", "comment": "NoSir",
                             "changed_by": "Robocop", "change_timestamp": "2019-10-31T16:03:13.951Z"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_do_update)
    alert = BaseAlert(api, "ESD14U2C", {"id": "ESD14U2C", "workflow": {"status": "DISMISS"}})
    alert.update("Fixed", "NoSir")
    assert _was_called
    assert alert.workflow_.changed_by == "Robocop"
    assert alert.workflow_.status == "OPEN"
    assert alert.workflow_.closure_reason == "Fixed"
    assert alert.workflow_.comment == "NoSir"
    assert alert.workflow_.change_timestamp == "2019-10-31T16:03:13.951Z"


def test_BaseAlert_dismiss_threat(monkeypatch):
    """Test dismissal of a threat alert."""
    _was_called = False

    def _do_dismiss(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/api/alerts/v7/orgs/Z100/threat/B0RG/workflow"
        assert body == {"status": "CLOSED", "remediation_state": "Fixed", "comment": "Yessir"}
        _was_called = True
        return StubResponse({"status": "CLOSED", "closure_reason": "Fixed", "comment": "Yessir",
                             "changed_by": "Robocop", "change_timestamp": "2019-10-31T16:03:13.951Z"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_do_dismiss)
    alert = BaseAlert(api, "ESD14U2C", {"id": "ESD14U2C", "threat_id": "B0RG", "workflow": {"status": "OPEN"}})
    wf = alert.dismiss_threat("Fixed", "Yessir")
    assert _was_called
    assert wf.changed_by == "Robocop"
    assert wf.status == "CLOSED"
    assert wf.closure_reason == "Fixed"
    assert wf.comment == "Yessir"
    assert wf.change_timestamp == "2019-10-31T16:03:13.951Z"


def test_BaseAlert_undismiss_threat(monkeypatch):
    """Test undismissal of a threat alert."""
    _was_called = False

    def _do_update(url, body, **kwargs):
        nonlocal _was_called
        assert url == "/api/alerts/v7/orgs/Z100/threat/B0RG/workflow"
        assert body == {"status": "OPEN", "remediation_state": "Fixed", "comment": "NoSir"}
        _was_called = True
        return StubResponse({"status": "OPEN", "closure_reason": "Fixed", "comment": "NoSir",
                             "changed_by": "Robocop", "change_timestamp": "2019-10-31T16:03:13.951Z"})

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, POST=_do_update)
    alert = BaseAlert(api, "ESD14U2C", {"id": "ESD14U2C", "threat_id": "B0RG", "workflow": {"status": "OPEN"}})
    wf = alert.update_threat("Fixed", "NoSir")
    assert _was_called
    assert wf.changed_by == "Robocop"
    assert wf.status == "OPEN"
    assert wf.closure_reason == "Fixed"
    assert wf.comment == "NoSir"
    assert wf.change_timestamp == "2019-10-31T16:03:13.951Z"


def test_WorkflowStatus(monkeypatch):
    """Test retrieval of the workflow status."""
    _times_called = 0

    def _get_workflow(url, parms=None, default=None):
        nonlocal _times_called
        assert url == "/api/alerts/v7/orgs/Z100/workflow/status/W00K13"
        if _times_called >= 0 and _times_called <= 3:
            _stat = "QUEUED"
        elif _times_called >= 4 and _times_called <= 6:
            _stat = "IN_PROGRESS"
        elif _times_called >= 7 and _times_called <= 9:
            _stat = "FINISHED"
        else:
            pytest.fail("_get_workflow called too many times")
        _times_called = _times_called + 1
        return {"errors": [], "failed_ids": [], "id": "W00K13", "num_hits": 0, "num_success": 0, "status": _stat,
                "workflow": {"status": "DISMISSED", "closure_reason": "Fixed", "comment": "Yessir",
                             "changed_by": "Robocop", "change_timestamp": "2019-10-31T16:03:13.951Z"}}

    api = CBCloudAPI(url="https://example.com", token="ABCD/1234", org_key="Z100", ssl_verify=True)
    patch_cbc_sdk_api(monkeypatch, api, GET=_get_workflow)
    wfstat = WorkflowStatus(api, "W00K13")
    assert wfstat.workflow_.changed_by == "Robocop"
    assert wfstat.workflow_.status == "CLOSED"
    assert wfstat.workflow_.closure_reason == "Fixed"
    assert wfstat.workflow_.comment == "Yessir"
    assert wfstat.workflow_.change_timestamp == "2019-10-31T16:03:13.951Z"
    assert _times_called == 1
    assert wfstat.queued
    assert not wfstat.in_progress
    assert not wfstat.finished
    assert _times_called == 4
    assert not wfstat.queued
    assert wfstat.in_progress
    assert not wfstat.finished
    assert _times_called == 7
    assert not wfstat.queued
    assert not wfstat.in_progress
    assert wfstat.finished
    assert _times_called == 10
