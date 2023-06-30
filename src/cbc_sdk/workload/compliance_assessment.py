#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2021-2023. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model and Query Classes for Compliance Assessment API"""

from cbc_sdk.base import (NewBaseModel, BaseQuery, QueryBuilder, QueryBuilderSupportMixin,
                          IterableQueryMixin, AsyncQueryMixin, UnrefreshableModel)
from cbc_sdk.errors import ApiError, MoreThanOneResultError, ObjectNotFoundError
import logging

log = logging.getLogger(__name__)

""" Compliance models """


class ComplianceBenchmark(NewBaseModel):
    """
    """
    urlobject = '/compliance/assessment/api/v1/orgs/{}/benchmark_sets/'
    swagger_meta_file = "workload/models/compliance.yaml"
    primary_key = "benchmark_set_id"

    def __init__(self, cb, model_unique_id=None, initial_data=None):
        """
        """
        super(ComplianceBenchmark, self).__init__(cb, model_unique_id, initial_data)

        if model_unique_id is not None and initial_data is None:
            self._refresh()
        self._full_init = True

    def _refresh(self):
        """
        """
        return True

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        """
        return ComplianceBenchmarkQuery(cls, cb)

    @staticmethod
    def get_org_compliance_schedule(cb):
        """
        Gets the compliance scan schedule and timezone for the organization associated with the specified CBCloudAPI instance.

        Args:
            cb (CBCloudAPI): An instance of CBCloudAPI representing the Carbon Black Cloud API.

        Raises:
            ApiError: If cb is not an instance of CBCloudAPI.

        Returns:
            The JSON response from the Carbon Black Cloud API as a Python dictionary.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> descriptions = AuthEvent.get_auth_events_descriptions(cb)
            >>> print(descriptions)
        """
        if cb.__class__.__name__ != "CBCloudAPI":
            message = "cb argument should be instance of CBCloudAPI."
            message += "\nExample:\ncb = CBCloudAPI(profile='example_profile')"
            message += "\nCompliance.get_org_settings(cb)"
            raise ApiError(message)

        url = f"/compliance/assessment/api/v1/orgs/{cb.credentials.org_key}/settings"

        return cb.get_object(url)

    @staticmethod
    def set_org_compliance_schedule(cb, scan_schedule, scan_timezone):
        """
        Sets the compliance scan schedule and timezone for the organization associated with the specified CBCloudAPI instance.

        Args:
            cb (CBCloudAPI): An instance of CBCloudAPI representing the Carbon Black Cloud API.
            scan_schedule (str): The scan schedule, specified in RFC 5545 format. Example: "RRULE:FREQ=DAILY;BYHOUR=17;BYMINUTE=30;BYSECOND=0".
            scan_timezone (str): The timezone in which the scan will run, specified as a timezone string. Example: "UTC".

        Raises:
            ApiError: If cb is not an instance of CBCloudAPI, or if scan_schedule or scan_timezone are not provided.

        Returns:
            The JSON response from the Carbon Black Cloud API as a Python dictionary.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> response = Compliance.set_org_compliance_schedule(cb, scan_schedule="RRULE:FREQ=DAILY;BYHOUR=17;BYMINUTE=30;BYSECOND=0", scan_timezone="UTC")
            >>> print(response)
        """
        if cb.__class__.__name__ != "CBCloudAPI":
            message = "cb argument should be instance of CBCloudAPI."
            message += "\nExample:\ncb = CBCloudAPI(profile='example_profile')"
            message += "\nCompliance.set_org_compliance_schedule(cb, scan_schedule='RRULE:FREQ=DAILY;BYHOUR=17;BYMINUTE=30;BYSECOND=0', scan_timezone='UTC')"
            raise ApiError(message)
        if not scan_schedule or not scan_timezone or scan_schedule == "" or scan_timezone == "":
            raise ApiError("scan_schedule and scan_timezone are required. http://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/latest/livequery-api/#recurrence-rules")

        args = {"scan_schedule": scan_schedule, "scan_timezone": scan_timezone}
        url = f"/compliance/assessment/api/v1/orgs/{cb.credentials.org_key}/settings"

        return cb.put_object(url, body=args).json()


class ComplianceBenchmarkQuery(BaseQuery, QueryBuilderSupportMixin,
                         IterableQueryMixin, AsyncQueryMixin):
    """
    """
    def __init__(self, doc_class, cb):
        """
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(BaseQuery, self).__init__()

        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._sortcriteria = {}
        self._total_results = 0

        self._benchmark_set_id = None
        self._rule_id = None

    def add_criteria(self, key, value, operator='EQUALS'):
        """
        """
        self._update_criteria(key, value, operator)
        return self

    def _update_criteria(self, key, value, operator, overwrite=False):
        """
        """
        if self._criteria.get(key, None) is None or overwrite:
            self._criteria[key] = dict(value=value, operator=operator)

    def _build_request(self, from_row, max_rows, add_sort=True):
        """
       Build the request dictionary for the API query.

        Args:
            from_row (int): The starting row for the query.
            max_rows (int): The maximum number of rows to retrieve.
            add_sort (bool): Flag indicating whether to add sorting criteria to the request.

        Returns:
            dict: The constructed request dictionary.
        """
        request = {
            "criteria": self._criteria,
            "query": self._query_builder._collapse(),
            "rows": 1000 if max_rows < 0 else max_rows
        }

        if from_row > 0:
            request["start"] = from_row

        if add_sort and self._sortcriteria != {}:
            request["sort"] = [self._sortcriteria]

        return request

    def _build_url(self, tail_end):
        """
        Build the URL for the API request.

        Args:
            tail_end (str): The tail end of the URL to be appended.

        Returns:
            str: The constructed URL.
        """
        return self._doc_class.urlobject.format(self._cb.credentials.org_key) + tail_end

    def _count(self):
        """
        Get the total number of results.

        Returns:
            int: The total number of results.
        """
        if self._count_valid:
            return self._total_results

        url = self._build_url("_search")
        request = self._build_request(0, -1)
        result = self._cb.post_object(url, body=request).json()

        self._total_results = result["num_found"]
        self._count_valid = True

        return self._total_results

    def _perform_query(self, from_row=0, max_rows=-1):
        """
        Perform a query and retrieve the results.

        Args:
            from_row (int): The starting row index for the query (default is 0).
            max_rows (int): The maximum number of rows to retrieve (-1 retrieves all rows).

        Yields:
            obj: An instance of the document class containing each query result.
        """
        url = self._build_url("_search")
        current = from_row
        numrows = 0
        while True:
            request = self._build_request(current, max_rows)
            if self._benchmark_set_id and self._rule_id:
                resp = self._cb.get_object(url)
            else:
                resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, initial_data=item)
                current += 1
                numrows += 1

                if max_rows > 0 and numrows == max_rows:
                    return

            if current >= self._total_results:
                return

    def _run_async_query(self, context):
        """
        Run an asynchronous query and retrieve the results.

        Args:
            context: The context for the query.

        Returns:
            dict: The JSON response containing the query results.
        """
        url = self._build_url("_search")
        request = self._build_request(0, -1)
        return self._cb.post_object(url, body=request).json()

    def sort_by(self, key, direction='ASC'):
        """
        Set the sort criteria for the search.

        Args:
            key (str): The field to sort by.
            direction (str, optional): The sort direction. Defaults to "ASC".
                Valid values are "ASC" (ascending) and "DESC" (descending).

        Returns:
            self: The current instance with the updated sort criteria.

        Raises:
            ApiError: If an invalid sort direction is specified.

        Example:
            To sort by a field in descending order:

            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark_sets = cb.select(ComplianceBenchmark).sort_by("name", direction="DESC")
            >>> print(*benchmark_sets)
        """
        if direction.upper() not in ('ASC', 'DESC', 'asc', 'desc'):
            raise ApiError('invalid sort direction specified')
        self._sortcriteria = {'field': key, 'order': direction}
        return self

    def set_benchmark_set_id(self, benchmark_set_id):
        """
        Set the benchmark set ID for the current instance.

        Args:
            benchmark_set_id (str): The ID of the benchmark set to set.

        Returns:
            self: The current instance with the updated benchmark set ID.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark_set = cb.select(ComplianceBenchmark).set_benchmark_set_id('benchmark123')
            >>> print(*benchmark_set)
        """
        self._benchmark_set_id = benchmark_set_id
        return self

    def search_rules(self, rule_id=None):
        """
        Search for rules within the benchmark set.

        Args:
            rule_id (str): Optional rule ID to search for. If provided, only the rule with the specified ID will be returned.

        Yields:
            Rule document: Yields rule documents that match the search criteria.

        Raises:
            ApiError: If the benchmark_set_id is not set.

        Returns:
            None

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark_set = cb.select(ComplianceBenchmark).set_benchmark_set_id('benchmark123')
            >>> # To return a single rule document, add the ID.
            >>> rule = benchmark_set.search_rules('FDBFA982-2EA2-4720-83CC-E515CEFB795D')
            >>> print(*rule)
            >>> # To return all rules within a benchmark set, leave empty.
            >>> rules = benchmark_set.search_rules()
            >>> print(*rules)
        """
        if not self._benchmark_set_id:
            raise ApiError("internal error: benchmark_set_id is required.")

        if rule_id is not None:
            self._rule_id = rule_id
            url = self._build_url(f"{self._benchmark_set_id}/rules/{self._rule_id}")
            result = self._cb.get_object(url)
            yield self._doc_class(self._cb, initial_data=result)
            return

        url = self._build_url(f"{self._benchmark_set_id}/rules/_search")
        current = 0
        max_rows = 1000
        while True:
            request = self._build_request(current, max_rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, initial_data=item)

            current += len(results)
            if max_rows > 0 and current >= max_rows:
                break

            if current >= self._total_results:
                break

    def get_benchmark_set_sections(self):
        """
        Retrieves the sections of a compliance benchmark set.

        Returns an iterator over the sections of the benchmark set. Each section is represented as an instance of the
        compliance benchmark section model.

        Raises:
            ApiError: If the benchmark_set_id is not set.

        Yields:
            ComplianceBenchmarkSection: An instance of the compliance benchmark section model.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark = cb.select(ComplianceBenchmark).set_benchmark_set_id('benchmark123')
            >>> for section in benchmark.get_benchmark_set_sections():
            ...     print(section.section_name, section.section_id)
        """
        if not self._benchmark_set_id:
            raise ApiError("internal error: benchmark_set_id is required.")

        url = self._build_url(f"{self._benchmark_set_id}/sections")
        results = self._cb.get_object(url)
        for item in results:
            yield self._doc_class(self._cb, initial_data=item)
