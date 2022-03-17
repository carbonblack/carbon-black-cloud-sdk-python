#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Unit test code for NSX remediation"""
import copy

import pytest
import logging
from cbc_sdk.errors import ApiError, ServerError
from cbc_sdk.platform import Device
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from cbc_sdk.workload.nsx_remediation import NSXRemediationJob
from tests.unit.fixtures.workload.mock_nsx_remediation import (NSX_REQUEST_1, NSX_RESPONSE_1, JOB_STATUS_RUNNING,
                                                               NSX_REQUEST_2, NSX_RESPONSE_2, NSX_REQUEST_2A,
                                                               NSX_RESPONSE_2A, NSX_REQUEST_3, NSX_RESPONSE_3,
                                                               NSX_LIFECYCLE_1, NSX_DEVICE_DATA_1,
                                                               NSX_DEVICE_DATA_1A, NSX_DEVICE_DATA_2,
                                                               NSX_DEVICE_DATA_3, NSX_DEVICE_DATA_3A)


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


class MockResponseToJobStatus:
    """Handles getting a mock response to the job status call."""
    def __init__(self, job_states):
        self._job_states = job_states
        self._jobs_to_run = set(job_states.keys())
        self._phase = 0

    def handle_get(self, url):
        """
        Called when we are handling a GET request.

        Args:
            url (str): The URL that we're getting.

        Returns:
            dict: The response to send back.
        """
        components = url.split('/')
        assert len(components) == 8, f"Invalid URL supplied: {url}"
        assert not components[0], f"Invalid URL supplied: {url}"
        assert components[1] == 'applianceservice', f"Invalid URL supplied: {url}"
        assert components[2] == 'v1', f"Invalid URL supplied: {url}"
        assert components[3] == 'orgs', f"Invalid URL supplied: {url}"
        assert components[4] == 'test', f"Invalid URL supplied: {url}"
        assert components[5] == 'jobs', f"Invalid URL supplied: {url}"
        assert components[7] == 'status', f"Invalid URL supplied: {url}"
        if len(self._jobs_to_run) == 0:
            self._phase += 1
            self._jobs_to_run = set([k for k, v in self._job_states.items() if len(v) > self._phase])
        states = self._job_states.get(components[6], None)
        assert states, f"Invalid URL supplied: {url}"
        assert self._phase < len(states), f"URL should no longer be referenced: {url}"
        self._jobs_to_run.discard(components[6])
        return {'error_code': '', 'reason': 'Dummy message', 'status': states[self._phase]}

    def jobs_list(self):
        """Returns a list of all job IDs."""
        return list(self._job_states.keys())

    def count_still_running(self):
        """Returns the number of jobs still running."""
        return len([len(v) for v in self._job_states.values() if len(v) > (self._phase + 1)])

    def current_status(self, jobid):
        """Returns what the current status for a job should be."""
        states = self._job_states.get(jobid, None)
        assert states, f"Invalid job ID supplied: {jobid}"
        return states[self._phase if self._phase < len(states) else -1]


# ==================================== UNIT TESTS BELOW ====================================

@pytest.mark.parametrize("reqbody, respbody, devid, tag, onoff, jobids", [
    (NSX_REQUEST_1, NSX_RESPONSE_1, [142, 857], "CB-NSX-Quarantine", True, ["7ff05537-350a-420c-bfa8-3408ac70ce53"]),
    (NSX_REQUEST_2, NSX_RESPONSE_2, 5150, "CB-NSX-Isolate", False, ["540d3f7f-65f6-47c7-b581-692d2c892e22"]),
    (NSX_REQUEST_3, NSX_RESPONSE_3, [12, 23, 34, 45, 56, 67, 78, 89, 90], "CB-NSX-Custom", True,
     ["8b45115f-2827-4b8e-a0ab-5919c00213ac", "18acf87a-9b92-4fd9-82a1-a3b75592e348",
      "7fd50527-3cdb-4996-b316-6ad45ec18af6"])
])
def test_start_request(cbcsdk_mock, reqbody, respbody, devid, tag, onoff, jobids):
    """Tests the start_request operation."""

    def on_post(url, body, **kwargs):
        assert body == reqbody
        return CBCSDKMock.StubResponse(respbody, 201)

    cbcsdk_mock.mock_request("POST", "/applianceservice/v1/orgs/test/device_actions", on_post)
    for jobid in jobids:
        cbcsdk_mock.mock_request("GET", f"/applianceservice/v1/orgs/test/jobs/{jobid}/status", JOB_STATUS_RUNNING)
    api = cbcsdk_mock.api
    output = NSXRemediationJob.start_request(api, devid, tag, onoff)
    assert len(output._running_jobs) == len(jobids)
    for jobid in jobids:
        assert jobid in output._running_jobs
    assert len(output._status) == len(jobids)
    for jobid in jobids:
        assert output._status[jobid]['status'] == "RUNNING"


def test_start_request_with_errors(cbcsdk_mock):
    """Test error-raising behavior of start_request."""
    cbcsdk_mock.mock_request("POST", "/applianceservice/v1/orgs/test/device_actions",
                             CBCSDKMock.StubResponse(NSX_RESPONSE_1, 200))  # note wrong status code
    api = cbcsdk_mock.api
    with pytest.raises(ApiError):
        NSXRemediationJob.start_request(api, 'NotNumeric', 'CB-NSX-Quarantine')
    with pytest.raises(ApiError):
        NSXRemediationJob.start_request(api, [4, 'StillNotNumeric', 87], 'CB-NSX-Quarantine')
    with pytest.raises(ApiError):
        NSXRemediationJob.start_request(api, 16, 'RandomStringData')
    with pytest.raises(ServerError):
        NSXRemediationJob.start_request(api, 16, 'CB-NSX-Quarantine')


def test_poll_status_lifecycle(cbcsdk_mock):
    """Tests the lifecycle of a NSXRemediationJob with the _poll_status API."""
    mockresp = MockResponseToJobStatus(NSX_LIFECYCLE_1)

    def on_get(url, qparam, default):
        nonlocal mockresp
        return mockresp.handle_get(url)

    jobs_list = mockresp.jobs_list()
    for jobid in jobs_list:
        cbcsdk_mock.mock_request("GET", f"/applianceservice/v1/orgs/test/jobs/{jobid}/status", on_get)
    api = cbcsdk_mock.api
    sut = NSXRemediationJob(api, jobs_list)
    running = True
    while running:
        running = sut._poll_status()
        assert len(sut._running_jobs) == mockresp.count_still_running()
        for jobid in jobs_list:
            sblk = sut.status.get(jobid, None)
            cur_status = sblk['status'] if sblk else None
            assert cur_status == mockresp.current_status(jobid)
        if not running:
            assert mockresp.count_still_running() == 0


def test_poll_status_await_result(cbcsdk_mock):
    """Tests the lifecycle of a NSXRemediationJob with the await_result API."""
    mockresp = MockResponseToJobStatus(NSX_LIFECYCLE_1)

    def on_get(url, qparam, default):
        nonlocal mockresp
        return mockresp.handle_get(url)

    jobs_list = mockresp.jobs_list()
    for jobid in jobs_list:
        cbcsdk_mock.mock_request("GET", f"/applianceservice/v1/orgs/test/jobs/{jobid}/status", on_get)
    api = cbcsdk_mock.api
    sut = NSXRemediationJob(api, jobs_list)
    stat = sut.await_result()
    assert mockresp.count_still_running() == 0
    assert len(stat) == len(jobs_list)
    for jobid in jobs_list:
        sblk = sut.status.get(jobid, None)
        cur_status = sblk['status'] if sblk else None
        assert cur_status == mockresp.current_status(jobid)


def test_poll_status_async_await_result(cbcsdk_mock):
    """Tests the lifecycle of a NSXRemediationJob with the async_await_result API."""
    mockresp = MockResponseToJobStatus(NSX_LIFECYCLE_1)

    def on_get(url, qparam, default):
        nonlocal mockresp
        return mockresp.handle_get(url)

    jobs_list = mockresp.jobs_list()
    for jobid in jobs_list:
        cbcsdk_mock.mock_request("GET", f"/applianceservice/v1/orgs/test/jobs/{jobid}/status", on_get)
    api = cbcsdk_mock.api
    sut = NSXRemediationJob(api, jobs_list)
    future = sut.async_await_result()
    stat = future.result()
    assert mockresp.count_still_running() == 0
    assert len(stat) == len(jobs_list)
    for jobid in jobs_list:
        sblk = sut.status.get(jobid, None)
        cur_status = sblk['status'] if sblk else None
        assert cur_status == mockresp.current_status(jobid)


@pytest.mark.parametrize("initdata, expected", [
    (NSX_DEVICE_DATA_1, True),
    (NSX_DEVICE_DATA_2, False),
    (NSX_DEVICE_DATA_3, False)
])
def test_device_nsx_available(cb, initdata, expected):
    """Tests the nsx_available property on devices."""
    dev = Device(cb, initdata['id'], copy.deepcopy(initdata))
    assert dev.nsx_available == expected


@pytest.mark.parametrize("initdata, expected", [
    (NSX_DEVICE_DATA_1, ['CB-NSX-Quarantine', 'CB-NSX-Custom']),
    (NSX_DEVICE_DATA_1A, ['CB-NSX-Isolate']),
    (NSX_DEVICE_DATA_2, []),
    (NSX_DEVICE_DATA_3, []),
    (NSX_DEVICE_DATA_3A, [])
])
def test_device_nsx_tags(cb, initdata, expected):
    """Tests the nsx_tags property on devices."""
    dev = Device(cb, initdata['id'], copy.deepcopy(initdata))
    assert dev.nsx_tags == set(expected)


def test_device_nsx_remediation_passthrough(cbcsdk_mock):
    """Tests that an nsx_remediation call to a device is properly passed through."""

    def on_post(url, body, **kwargs):
        assert body == NSX_REQUEST_2A
        return CBCSDKMock.StubResponse(NSX_RESPONSE_2A, 201)

    cbcsdk_mock.mock_request("POST", "/applianceservice/v1/orgs/test/device_actions", on_post)
    cbcsdk_mock.mock_request("GET", f"/applianceservice/v1/orgs/test/jobs/2da0bc0e-ed1e-4a98-b8fa-ccc1e30c9576/status",
                             JOB_STATUS_RUNNING)
    api = cbcsdk_mock.api
    dev = Device(api, NSX_DEVICE_DATA_1['id'], copy.deepcopy(NSX_DEVICE_DATA_1))
    output = dev.nsx_remediation("CB-NSX-Quarantine", False)
    assert len(output._running_jobs) == 1
    assert '2da0bc0e-ed1e-4a98-b8fa-ccc1e30c9576' in output._running_jobs
    assert len(output._status) == 1
    assert output._status['2da0bc0e-ed1e-4a98-b8fa-ccc1e30c9576']['status'] == "RUNNING"


def test_device_nsx_remediation_fail(cb):
    """Tests that an nsx_remediation call throws an ApiError correctly if NSX is not available."""
    dev = Device(cb, NSX_DEVICE_DATA_2['id'], copy.deepcopy(NSX_DEVICE_DATA_2))
    with pytest.raises(ApiError):
        dev.nsx_remediation("CB-NSX-Quarantine", False)
