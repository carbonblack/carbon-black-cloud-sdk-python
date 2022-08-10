#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020-2022. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model and Query Classes for Differential Analysis"""

from __future__ import absolute_import
import logging
from cbc_sdk.base import (NewBaseModel, IterableQueryMixin, BaseQuery, CriteriaBuilderSupportMixin)
from cbc_sdk.platform import Job
from cbc_sdk.errors import ApiError


log = logging.getLogger(__name__)

# Rate limits per 5 mins on an org basis
SYNC_RATE_LIMIT = 350
ASYNC_RATE_LIMIT = 100


"""Differential Analysis Models"""


class Differential(NewBaseModel):
    """
    Represents a Differential Analysis run.

    Example:
        >>> run = cbc.select(Differential).newer_run_id(newer_run_id)
        >>> print(*run)
        >>> print(resp[0]._info)
    """
    swagger_meta_file = "audit_remediation/models/differential.yaml"
    urlobject = "/livequery/v1/orgs/{}/differential/runs/_search"

    def __init__(self, cbc, model_unique_id=None, initial_data=None):
        """
        Initialize a Differential object with initial_data.

        Required Permissions for CBC:
            livequery.manage(READ)
        Required Permissions for CSP:
            _API.Live.Query:livequery.Manage.read

        Arguments:
            cbc (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the query run represented.
            initial_data (dict): Initial data used to populate the query run.
        """
        model_unique_id = initial_data.get("newer_run_id")

        super(Differential, self).__init__(
            cbc,
            model_unique_id=model_unique_id,
            initial_data=initial_data,
            force_init=False,
            full_doc=True,
        )

    @classmethod
    def _query_implementation(cls, cbc, **kwargs):
        """
        Returns the appropriate query object for the Differential type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            DifferentialQuery: The query object for the Differential type.
        """
        return DifferentialQuery(cls, cbc)


"""Differential Analysis Queries"""


class DifferentialQuery(BaseQuery, IterableQueryMixin, CriteriaBuilderSupportMixin):
    """Query used to compare two Live Query runs."""

    def __init__(self, doc_class, cbc):
        """
        Initialize the DifferentialQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cbc (BaseAPI): Reference to API object used to communicate with the server.
        """
        super(DifferentialQuery, self).__init__()
        self._cb = cbc
        self._criteria = {}
        self._doc_class = doc_class
        self._count_only = True
        self._count_valid = True
        self._newer_run_id = None
        self._older_run_id = None
        self._total_results = 0

    def newer_run_id(self, newer_run_id):
        """
        Set the id against which the older_run_id results will be compared.

        Args:
            newer_run_id (string): id against which the older_run_id results will be compared.

        Returns:
            DifferentialQuery: This instance.

        Raises:
            ApiError: If invalid values are passed.
        """
        if newer_run_id == "" or not isinstance(newer_run_id, str):
            raise ApiError("Invalid newer_run_id")
        self._newer_run_id = newer_run_id
        return self

    def older_run_id(self, older_run_id):
        """
        This can be optional.

        If not specified, the previous run as compared to the primary will be chosen if
        it is a reccuring one. If comparing two individual runs, this is required.

        Args:
            older_run_id (string): id against which the newer_run_id results will be compared.

        Returns:
            DifferentialQuery: This instance.

        Raises:
            ApiError: If invalid values are passed.
        """
        if older_run_id == "" or not isinstance(older_run_id, str):
            raise ApiError("Invalid older_run_id")
        self._older_run_id = older_run_id
        return self

    def set_device_ids(self, device_ids):
        """
        Restricts the query on to the specified devices only.

        Args:
            device_ids (list): List of device id(s)

        Returns:
            DifferentialQuery: This instance.

        Raises:
            ApiError: If invalid values are passed in the list.
        """
        if not all(isinstance(device_id, int) for device_id in device_ids):
            raise ApiError("One or more invalid device IDs")
        self._update_criteria("device_id", device_ids)
        return self

    def count_only(self, count_only):
        """
        Return only count of diff results per device or complete diff metadata result.

        The default value is true, which means only the count will be returned.

        Args:
            count_only (string): Boolean that indicates whether to return actual metadata
                or return just the count of differances

        Returns:
            DifferentialQuery: This instance.

        Raises:
            ApiError: If invalid values are passed in the list.
        """
        if str(count_only).lower() not in ["true", "false"]:
            raise ApiError("Invalid boolean value for count_only")
        if str(count_only).lower() == "false":
            self._count_only = False
        return self

    def _build_request(self):
        """
        Creates the request body for an API call.

        Returns:
            dict: The complete request body.
        """
        request = {"newer_run_id": self._newer_run_id}

        if self._older_run_id:
            request["older_run_id"] = self._older_run_id
        if self._criteria:
            request["criteria"] = self._criteria
        if self._count_only is False:
            request["count_only"] = False
        return request

    def _build_url(self, tail_end=None):
        """
        Creates the URL to be used for an API call.

        Args:
            tail_end (str): String to be appended to the end of the generated URL.

        Returns:
            str: The complete URL.
        """
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key)
        if tail_end is not None:
            url += tail_end
        return url

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Returns:
            int: The number of results from the run of this query.
        """
        return self._total_results

    def _perform_query(self, from_row=None, max_rows=None):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): Not used; retained for compatibility.
            max_rows (int): Not used; retained for compatibility.

        Returns:
            Iterable: The iterated query.
        """
        url = self._build_url()
        request = self._build_request()
        results = self._cb.post_object(url, body=request).json()
        result = results.get("results")[0]

        self._count_valid = True
        self._total_results = len(results["results"])

        yield self._doc_class(self._cb, result["newer_run_id"], result)

    def async_export(self):
        """
        Create an asynchronous job that exports the results from the run.

        This is recommended if you are expecting a very large result set. Once the Job is created, wait for it to be
        completed, then get the results from the Job using one of the get_output methods on the
        `cbc_sdk.platform.jobs` object. To wait asynchronously for the results, use the Job object's
        await_completion() method.

        Example:
            >>> run = cbc.select(Differential).newer_run_id(newer_run_id)
            >>> job = run.async_export()
            >>> # show the status in progress
            >>> print(job.status)
            IN_PROGRESS
            >>> # wait for it to finish and refresh the information in the SDK
            >>> job_future = job.await_completion()
            >>> finished_job = job_future.result()
            >>> finished_job.refresh()
            >>> # show the job has completed
            >>> print(finished_job.status)
            COMPLETED
            >>> # write the results to a csv file
            >>> finished_job.get_output_as_file("example_data.json")

        Required CBC Permissions:
            livequery.manage(READ), jobs.status(READ)
        Required CSP Permissions:
            _API.Live.Query:livequery.Manage.read, _API.Background_Tasks.jobs.status.read

        Returns:
            Job: The Job object that represents the asynchronous job.
        """
        url = self._build_url("?async=true&format=json")
        request = self._build_request()
        response = self._cb.post_object(url, request).json()
        ref_url, job_id = response['ref_url'], response['job_id']

        if job_id < 0:
            raise ApiError(f"Server sent back invalid job reference URL {ref_url}")
        return Job(self._cb, job_id)
