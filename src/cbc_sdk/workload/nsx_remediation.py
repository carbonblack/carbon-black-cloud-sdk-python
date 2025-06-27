#!/usr/bin/env python3

# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2025. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""NSX Remediation for Workloads"""

import time
from cbc_sdk.errors import ApiError, ServerError, NSXJobError


class NSXRemediationJob:
    """An object that runs and monitors an NSX Remediation operation."""
    VALID_TAGS = ['CB-NSX-Quarantine', 'CB-NSX-Isolate', 'CB-NSX-Custom']
    RUNNING_STATUSES = ['UNASSIGNED', 'SCHEDULED', 'RUNNING', 'RUNNING_UNDELIVERED']

    def __init__(self, cb, running_job_ids):
        """
        Creates a new NSXRemediationJob object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            running_job_ids (list[str]): The list of running job IDs.
        """
        self._cb = cb
        self._status = {job: None for job in running_job_ids}
        self._running_jobs = set(running_job_ids)
        self._poll_status()

    @classmethod
    def start_request(cls, cb, device_ids, tag, set_tag=True):
        """
        Starts an NSX Remediation request and returns the job object.

        Required Permissions:
            appliances.nsx.remediation(EXECUTE)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            device_ids (int|list): The device ID(s) to run the remediation request on.
            tag (str): The NSX tag to apply to specified devices. Valid values are "CB-NSX-Quarantine",
                       "CB-NSX-Isolate", and "CB-NSX-Custom".
            set_tag (bool): True to toggle the specified tag on, False to toggle it off. Default True.

        Returns:
            NSXRemediationJob: The object representing all running jobs.

        Raises:
            ApiError: If the parameters to start the request are incorrect.
            ServerError: If the request could not be successfully started.
        """
        if isinstance(device_ids, list):
            if not all(isinstance(device_id, int) for device_id in device_ids):
                raise ApiError("device_ids list items of invalid type")
            real_device_ids = device_ids
        elif isinstance(device_ids, int):
            real_device_ids = [device_ids]
        else:
            raise ApiError("device_ids of invalid type")
        if tag not in NSXRemediationJob.VALID_TAGS:
            raise ApiError(f"invalid tag: {tag}")

        request_body = {'device_ids': real_device_ids, 'action_type': 'NSX_REMEDIATION',
                        'options': {'toggle': 'ON' if set_tag else 'OFF', 'tag': tag}}
        url = "/applianceservice/v1/orgs/{}/device_actions".format(cb.credentials.org_key)
        response = cb.post_object(url, body=request_body)
        if response.status_code != 201:
            raise ServerError(response.status_code,
                              f"could not start remediation request, error code {response.status_code}", uri=url)
        job_ids = response.json().get('job_ids', [])
        if job_ids:
            return NSXRemediationJob(cb, job_ids)
        raise NSXJobError("No jobs started")

    def _poll_status(self):
        """
        Polls the current status of all running jobs, saves it, and eliminates all jobs that are no longer running.

        Required Permissions:
            appliances.registration(READ)

        Returns:
            bool: True if at least one job is still running, otherwise False.
        """
        done_jobs = []
        for job in self._running_jobs:
            url = "/applianceservice/v1/orgs/{}/jobs/{}/status".format(self._cb.credentials.org_key, job)
            response = self._cb.get_object(url)
            self._status[job] = response
            if response['status'] not in NSXRemediationJob.RUNNING_STATUSES:
                done_jobs.append(job)

        for job in done_jobs:
            self._running_jobs.remove(job)
        return len(self._running_jobs) > 0

    def await_result(self):
        """
        Waits for all running jobs to be completed and returns the final status.

        Required Permissions:
            appliances.registration(READ)

        Returns:
            dict: The final status, mapping individual job IDs to status value dicts.
        """
        while self._poll_status():
            time.sleep(1)
        return self._status

    def async_await_result(self):
        """
        Sets up a Future which can be used to wait asynchronously for all running jobs to be completed.

        Required Permissions:
            appliances.registration(READ)

        Returns:
            Future: A future representing the job and its results.
        """
        return self._cb._async_submit(lambda arg, kwarg: arg[0].await_result(), self)

    @property
    def status(self):
        """
        Returns the current status.

        Returns:
            dict: The current status, mapping individual job IDs to status value dicts.
        """
        return self._status
