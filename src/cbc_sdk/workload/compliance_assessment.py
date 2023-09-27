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

from cbc_sdk.base import (NewBaseModel, BaseQuery, QueryBuilder, CriteriaBuilderSupportMixin,
                          IterableQueryMixin, AsyncQueryMixin, UnrefreshableModel)
from cbc_sdk.errors import ApiError, MoreThanOneResultError, ObjectNotFoundError
import logging

log = logging.getLogger(__name__)

""" Compliance models """


class ComplianceBenchmark(NewBaseModel):
    """
    Class representing Compliance Benchmarks.
    """
    urlobject = '/compliance/assessment/api/v1/orgs/{}/benchmark_sets/'
    swagger_meta_file = "workload/models/compliance.yaml"
    primary_key = "benchmark_set_id"

    def __init__(self, cb, initial_data, model_unique_id=None):
        """
        Initialize a ComplianceBenchmark instance.

        Args:
            cb (CBCloudAPI): Instance of CBCloudAPI.
            initial_data (dict): Initial data for the instance.
            model_unique_id (str): Unique identifier for the model.

        Returns:
            ComplianceBenchmark: An instance of ComplianceBenchmark.
        """
        super(ComplianceBenchmark, self).__init__(cb, model_unique_id, initial_data)

        if model_unique_id is not None and initial_data is None:
            self._refresh()
        self._full_init = True

    def _refresh(self):
        """
        Refresh the ComplianceBenchmark instance by making a GET request to get the benchmark.

        Returns:
            bool: True if the refresh is successful, else False.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._last_refresh_time = time.time()
        return True

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Get the query implementation for ComplianceBenchmark.

        Args:
            cb (CBCloudAPI): Instance of CBCloudAPI.

        Returns:
            ComplianceBenchmarkQuery: Query implementation for ComplianceBenchmark.
        """
        return ComplianceBenchmarkQuery(cls, cb)

    @staticmethod
    def get_compliance_schedule(cb):
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
            >>> schedule = ComplianceBenchmark.get_compliance_schedule(cb)
            >>> print(schedule)
        """
        if cb.__class__.__name__ != "CBCloudAPI":
            message = "cb argument should be instance of CBCloudAPI."
            message += "\nExample:\ncb = CBCloudAPI(profile='example_profile')"
            message += "\nComplianceBenchmark.get_compliance_schedule(cb)"
            raise ApiError(message)

        url = f"/compliance/assessment/api/v1/orgs/{cb.credentials.org_key}/settings"

        return cb.get_object(url)

    @staticmethod
    def set_compliance_schedule(cb, scan_schedule, scan_timezone):
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
            >>> schedule = ComplianceBenchmark.set_compliance_schedule(cb, scan_schedule="RRULE:FREQ=DAILY;BYHOUR=17;BYMINUTE=30;BYSECOND=0", scan_timezone="UTC")
            >>> print(schedule)
        """
        if cb.__class__.__name__ != "CBCloudAPI":
            message = "cb argument should be instance of CBCloudAPI."
            message += "\nExample:\ncb = CBCloudAPI(profile='example_profile')"
            message += "\nComplianceBenchmark.set_compliance_schedule(cb, scan_schedule='RRULE:FREQ=DAILY;BYHOUR=17;BYMINUTE=30;BYSECOND=0', scan_timezone='UTC')"
            raise ApiError(message)
        if not scan_schedule or not scan_timezone or scan_schedule == "" or scan_timezone == "":
            raise ApiError(
                "scan_schedule and scan_timezone are required. http://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/latest/livequery-api/#recurrence-rules")

        args = {"scan_schedule": scan_schedule, "scan_timezone": scan_timezone}
        url = f"/compliance/assessment/api/v1/orgs/{cb.credentials.org_key}/settings"

        return cb.put_object(url, body=args).json()

    def search_rules(self, rule_id=None):
        """
        Fetches compliance rules associated with the benchmark set.

        Args:
            rule_id (str, optional): The rule ID to fetch a specific rule. Defaults to None.

        Yields:
            ComplianceBenchmark: A Compliance object representing a compliance rule.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark_sets = cb.select(ComplianceBenchmark)
            >>> # To return all rules within a benchmark set, leave search_rules empty.
            >>> rules = list(benchmark_sets[0].search_rules())
            >>> print(*rules)
            >>> # To return a single rule document, add the rule ID.
            >>> rule = list(benchmark_sets.search_rules('00869D86-6E61-4D7D-A0A3-6F5CDE2E5753'))
            >>> print(rule)
        """
        if rule_id is not None:
            self._rule_id = rule_id
            url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/rules/{rule_id}"
            result = self._cb.get_object(url)
            yield ComplianceBenchmark(self._cb, initial_data=result)
            return

        url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/rules/_search"
        current = 0
        max_rows = 80000
        while True:
            # request = self._build_request(current, max_rows)
            resp = self._cb.post_object(url, body={})  # FIXME fix the body
            result = resp.json()

            self._total_results = result["num_found"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield ComplianceBenchmark(self._cb, initial_data=item)

            current += len(results)
            if max_rows > 0 and current >= max_rows:
                break

            if current >= self._total_results:
                break

    def get_set_sections(self):
        """
        Get Sections of the Benchmark Set.

        Returns:
            generator of ComplianceBenchmark: A generator yielding Compliance instances
                                           for each section in the benchmark set.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark = cb.select(ComplianceBenchmark).set_benchmark_set_id('benchmark123')
            >>> for section in benchmark.get_benchmark_set_sections():
            ...     print(section.section_name, section.section_id)
        """
        url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/sections"
        results = self._cb.get_object(url)
        for item in results:
            yield ComplianceBenchmark(self._cb, initial_data=item)

    def execute_action(self, action, device_ids=None):
        """
        Execute a specified action on devices within on a Benchmark Set, or specific devives
        within a Benchmark Set only.

        Args:
            action (str): The action to be executed. Available:
                'ENABLE': Enable the object.
                'DISABLE': Disable the object.
                'REASSESS': Reassess the object.

            device_ids (str or list, optional): IDs of devices on which the action will be executed.
                If specified as a string, only one device will be targeted. If specified as a list,
                the action will be executed on multiple devices. Default is None.

        Returns:
            dict: JSON response containing information about the executed action.

        Raises:
            ApiError: If the provided action is not one of the allowed actions.

        Example:
            To reassess an object:
            benchmark_sets = cb.select(ComplianceBenchmark)
            benchmark_sets[0].execute_action('REASSESS')
        """
        ACTIONS = ('ENABLE', 'DISABLE', 'REASSESS')

        if action.upper() not in ACTIONS:
            message = (
                f"\nAction type is required."
                f"\nAvailable action types: {', '.join(ACTIONS)}"
                f"\nExample:\nbenchmark_sets = cb.select(ComplianceBenchmark)"
                f"\nbenchmark_sets[0].execute_action('REASSESS')"
            )
            raise ApiError(message)

        args = {"action": action}
        if device_ids:
            args['device_ids'] = [device_ids] if isinstance(device_ids, str) else device_ids

        url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/actions"
        return self._cb.post_object(url, body=args).json()

    def get_benchmark_set_summary(self):
        """
        Fetches the compliance summary for the current benchmark set.

        This method constructs the URL for the compliance summary of the benchmark set associated with the current instance,
        fetches the summary data using the Carbon Black API, and yields Compliance objects for each item in the summary.

        Returns:
            generator of ComplianceBenchmark: A generator yielding Compliance objects, each representing a summary item.
        """
        url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/compliance/summary"
        results = self._cb.get_object(url)
        for item in results:
            yield ComplianceBenchmark(self._cb, initial_data=item)


class ComplianceBenchmarkQuery(BaseQuery, CriteriaBuilderSupportMixin,
                               IterableQueryMixin, AsyncQueryMixin):
    """
    A class representing a query for Compliance Benchmark.
    """

    def __init__(self, doc_class, cb):
        """
        Initialize a ComplianceBenchmarkQuery instance.

        Args:
            doc_class (class): The document class for this query.
            cb (CBCloudAPI): An instance of CBCloudAPI.

        Returns:
            ComplianceBenchmarkQuery: An instance of ComplianceBenchmarkQuery.
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
        Add a criteria to the query.

        Args:
            key (str): The key for the criteria.
            value: The value for the criteria.
            operator (str, optional): The operator for the criteria. Defaults to 'EQUALS'.

        Returns:
            ComplianceBenchmarkQuery: The current instance with the updated criteria.
        """
        self._update_criteria(key, value, operator)
        return self

    def _update_criteria(self, key, value, operator, overwrite=False):
        """
        Update the criteria for the query.

        Args:
            key (str): The key for the criteria.
            value: The value for the criteria.
            operator (str): The operator for the criteria.
            overwrite (bool, optional): Whether to overwrite existing criteria with the same key.
                                        Defaults to False.

        Returns:
            None
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
