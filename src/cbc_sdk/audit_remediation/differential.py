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

"""Model and Query Classes for Differential Analysis"""

from cbc_sdk.base import NewBaseModel, IterableQueryMixin, BaseQuery, CriteriaBuilderSupportMixin
from cbc_sdk.platform import Job
from cbc_sdk.errors import ApiError


# Rate limits per 5 mins on an org basis
SYNC_RATE_LIMIT = 350
ASYNC_RATE_LIMIT = 100


"""Differential Analysis Models"""


class Differential(NewBaseModel):
    """Represents a Differential Analysis run.

    Example:
        >>> query = cb.select(Differential).newer_run_id(newer_run_id)
        >>> run = query.submit()
        >>> print(run)
        >>> print(run.diff_results)
    """

    swagger_meta_file = "audit_remediation/models/differential.yaml"
    urlobject = "/livequery/v1/orgs/{}/differential/runs/_search"

    def __init__(self, cb, initial_data=None):
        """
        Initialize a Differential object with initial_data.

        Required Permissions for CBC:
            livequery.manage(READ)
        Required Permissions for CSP:
            _API.Live.Query:livequery.Manage.read

        Arguments:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            initial_data (dict): Initial data used to populate the query run.
        """
        super(Differential, self).__init__(
            cb,
            initial_data=initial_data,
            force_init=False,
            full_doc=True,
        )

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the Differential type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            DifferentialQuery: The query object for the Differential type.
        """
        return DifferentialQuery(cls, cb)


"""Differential Analysis Queries"""


class DifferentialQuery(BaseQuery, IterableQueryMixin, CriteriaBuilderSupportMixin):
    """Query used to compare two Live Query runs."""

    def __init__(self, doc_class, cb):
        """
        Initialize the DifferentialQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        super(DifferentialQuery, self).__init__()
        self._cb = cb
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

        Example:
            >>> query = cb.select(Differential).newer_run_id(newer_run_id)
            >>> run = query.submit()

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
        it is a recurring one. If comparing two individual runs, this is required.

        Example:
            >>> query = cb.select(Differential).newer_run_id(newer_run_id).older_run_id(older_run_id)
            >>> run = query.submit()

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

        Example:
            >>> query = cb.select(Differential).newer_run_id(newer_run_id).set_device_ids([12345, 56789])
            >>> run = query.submit()

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

        Example:
            >>> query = cb.select(Differential).newer_run_id(newer_run_id).count_only(True)
            >>> run = query.submit()

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

    def submit(self):
        """
        Submits this Differential Analysis run.

        Returns:
            Run: A new `Differential` instance containing the run's content.
        """
        url = self._build_url()
        request = self._build_request()
        results = self._cb.post_object(url, body=request).json()

        # The result always contains a single item
        result = results.get("results")[0]

        return self._doc_class(self._cb, initial_data=result)

    def async_export(self):
        """
        Create an asynchronous job that exports the results from the run.

        This is recommended if you are expecting a very large result set. Once the Job is created, wait for it to be
        completed, then get the results from the Job using one of the get_output methods on the
        `cbc_sdk.platform.jobs` object. To wait for the results, use the Job object's
        await_completion() method.

        Example:
            >>> # Get the differential
            >>> query = cb.select(Differential).newer_run_id(newer_run_id)
            >>> export = query.async_export()
            >>> # wait for the export to finish
            >>> export.await_completion()
            >>> # write the results to a file
            >>> export.get_output_as_file("example_data.json")

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
