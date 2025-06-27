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

"""Model and Query Classes for Compliance Assessment API"""

from cbc_sdk.base import (BaseQuery, QueryBuilder, QueryBuilderSupportMixin, CriteriaBuilderSupportMixin,
                          IterableQueryMixin, AsyncQueryMixin, UnrefreshableModel)
from cbc_sdk.errors import ApiError
import logging

log = logging.getLogger(__name__)

""" Compliance models """


class ComplianceBenchmark(UnrefreshableModel):
    """Class representing Compliance Benchmarks."""
    urlobject = '/compliance/assessment/api/v1/orgs/{}/benchmark_sets/'
    swagger_meta_file = "workload/models/compliance_benchmark.yaml"
    primary_key = "id"

    def __init__(self, cb, model_unique_id, initial_data=None):
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
            benchmark = cb.select(ComplianceBenchmark).add_criteria("id", [model_unique_id]).first()
            if benchmark is None:
                raise ApiError(f"Benchmark {model_unique_id} not found")
            self._info = benchmark._info
        self._full_init = True

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
        Gets the compliance scan schedule and timezone configured for the Organization.

        Args:
            cb (CBCloudAPI): An instance of CBCloudAPI representing the Carbon Black Cloud API.

        Required Permissions:
            complianceAssessment.data(READ)

        Raises:
            ApiError: If cb is not an instance of CBCloudAPI.

        Returns:
            dict: The configured organization settings for Compliance Assessment.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> schedule = ComplianceBenchmark.get_compliance_schedule(cb)
            >>> print(schedule)
        """
        if cb.__class__.__name__ != "CBCloudAPI":
            raise ApiError("cb argument should be instance of CBCloudAPI")

        url = f"/compliance/assessment/api/v1/orgs/{cb.credentials.org_key}/settings"

        return cb.get_object(url)

    @staticmethod
    def set_compliance_schedule(cb, scan_schedule, scan_timezone):
        """
        Sets the compliance scan schedule and timezone for the organization.

        Required Permissions:
            complianceAssessment.data(UPDATE)

        Args:
            cb (CBCloudAPI): An instance of CBCloudAPI representing the Carbon Black Cloud API.
            scan_schedule (str): The scan schedule, specified in RFC 5545 format.
                Example: "RRULE:FREQ=DAILY;BYHOUR=17;BYMINUTE=30;BYSECOND=0".
            scan_timezone (str): The timezone in which the scan will run,
                specified as a timezone string. Example: "UTC".

        Raises:
            ApiError: If cb is not an instance of CBCloudAPI, or if scan_schedule or scan_timezone are not provided.

        Returns:
            dict: The configured organization settings for Compliance Assessment.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> schedule = ComplianceBenchmark.set_compliance_schedule(cb,
                                scan_schedule="RRULE:FREQ=DAILY;BYHOUR=17;BYMINUTE=30;BYSECOND=0",
                                scan_timezone="UTC")
            >>> print(schedule)
        """
        if cb.__class__.__name__ != "CBCloudAPI":
            raise ApiError("cb argument should be instance of CBCloudAPI")
        if not scan_schedule or not scan_timezone or scan_schedule == "" or scan_timezone == "":
            raise ApiError("scan_schedule and scan_timezone are required")

        args = {"scan_schedule": scan_schedule, "scan_timezone": scan_timezone}
        url = f"/compliance/assessment/api/v1/orgs/{cb.credentials.org_key}/settings"

        return cb.put_object(url, body=args).json()

    def get_sections(self):
        """
        Get Sections of the Benchmark Set.

        Required Permissions:
            complianceAssessment.data(READ)

        Returns:
            list[dict]: List of sections within the Benchmark Set.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark = cb.select(ComplianceBenchmark).first()
            >>> for section in benchmark.get_sections():
            ...     print(section.section_name, section.section_id)
        """
        url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/sections"
        results = self._cb.get_object(url)
        return results

    def get_rules(self, rule_id=None):
        """
        Fetches compliance rules associated with the benchmark set.

        Required Permissions:
            complianceAssessment.data(READ)

        Args:
            rule_id (str, optional): The rule ID to fetch a specific rule. Defaults to None.

        Returns:
            [dict]: List of Benchmark Rules

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark_set = cb.select(ComplianceBenchmark).first()
            >>> # To return all rules within a benchmark set, leave get_rules empty.
            >>> rules = benchmark_set.get_rules()
        """
        if rule_id is not None:
            self._rule_id = rule_id
            url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/rules/{rule_id}"
            return [self._cb.get_object(url)]

        url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/rules/_search"
        current = 0
        rules = []
        while True:
            resp = self._cb.post_object(url, body={
                "rows": 10000,
                "start": current,
                "sort": [
                    {
                        "field": "section_name",
                        "order": "DESC"
                    }
                ]
            })
            result = resp.json()

            rules.extend(result.get("results", []))
            current = len(rules)
            if current >= result["num_found"]:
                break

        return rules

    def update_rules(self, rule_ids, enabled):
        """
        Update compliance rules associated with the benchmark set.

        Required Permissions:
            complianceAssessment.data(UPDATE)

        Args:
            rule_ids (list[str]): The rule IDs to update their enabled/disabled status.
            enabled (bool): Whether the rule is enabled or disabled.

        Returns:
            [dict]: List of Updated Benchmark Rules

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark_set = cb.select(ComplianceBenchmark).first()
            >>> # To return all rules within a benchmark set, leave get_rules empty.
            >>> rules = benchmark_set.update_rules(["2A65B63E-89D9-4844-8290-5042FDF2A27B"], True)
        """
        request = []
        for rule_id in rule_ids:
            request.append({
                "rule_id": rule_id,
                "enabled": enabled
            })
        url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/rules"
        return self._cb.put_object(url, body=request).json()

    def execute_action(self, action, device_ids=None):
        """
        Execute a specified action for the Benchmark Set for all devices or a specified subset.

        Required Permissions:
            complianceAssessment.data(EXECUTE)

        Args:
            action (str): The action to be executed. Options: ENABLE, DISABLE, REASSESS

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
            raise ApiError("Action is not supported. Options: ENABLE, DISABLE, REASSESS")

        args = {"action": action.upper()}
        url = ""
        if device_ids:
            args['device_ids'] = [device_ids] if isinstance(device_ids, str) else device_ids
            url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/compliance/device_actions"
        else:
            url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/actions"

        return self._cb.post_object(url, body=args).json()

    def get_device_compliances(self, query=""):
        """
        Fetches devices compliance summaries associated with the benchmark set.

        Required Permissions:
            complianceAssessment.data(READ)

        Args:
            query (str, optional): The query to filter results.

        Returns:
            [dict]: List of Device Compliances

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark_set = cb.select(ComplianceBenchmark).first()
            >>> device_compliances = benchmark_set.get_device_compliance()
        """
        url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/compliance/devices/_search"
        current = 0
        device_compliances = []
        while True:
            resp = self._cb.post_object(url, body={
                "query": query,
                "rows": 10000,
                "start": current,
                "sort": [
                    {
                        "field": "device_name",
                        "order": "DESC"
                    }
                ]
            })
            result = resp.json()

            device_compliances.extend(result.get("results", []))
            current = len(device_compliances)

            if current >= result["num_found"]:
                break

        return device_compliances

    def get_rule_compliances(self, query=""):
        """
        Fetches rule compliance summaries associated with the benchmark set.

        Required Permissions:
            complianceAssessment.data(READ)

        Args:
            query (str, optional): The query to filter results.

        Returns:
            [dict]: List of Rule Compliances

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark_set = cb.select(ComplianceBenchmark).first()
            >>> rules = benchmark_set.get_rule_compliance()
        """
        url = self.urlobject.format(self._cb.credentials.org_key) + f"{self.id}/compliance/rules/_search"
        current = 0
        rule_compliances = []
        while True:
            resp = self._cb.post_object(url, body={
                "query": query,
                "rows": 10000,
                "start": current,
                "sort": [
                    {
                        "field": "section_name",
                        "order": "DESC"
                    }
                ]
            })
            result = resp.json()

            rule_compliances.extend(result.get("results", []))
            current = len(rule_compliances)

            if current >= result["num_found"]:
                break

        return rule_compliances

    def get_device_rule_compliances(self, device_id, query=""):
        """
        Fetches rule compliances for specific device.

        Required Permissions:
            complianceAssessment.data(READ)

        Args:
            device_id (int): Device id to fetch benchmark rule compliance
            query (str, optional): The query to filter results.

        Returns:
            [dict]: List of Rule Compliances

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark_set = cb.select(ComplianceBenchmark).first()
            >>> rules = benchmark_set.get_device_rule_compliance(123)
        """
        url = self.urlobject.format(self._cb.credentials.org_key)
        url += f"{self.id}/compliance/devices/{device_id}/rules/_search"

        current = 0
        rule_compliances = []
        while True:
            resp = self._cb.post_object(url, body={
                "query": query,
                "rows": 10000,
                "start": current,
                "sort": [
                    {
                        "field": "section_name",
                        "order": "DESC"
                    }
                ]
            })
            result = resp.json()

            rule_compliances.extend(result.get("results", []))
            current = len(rule_compliances)

            if current >= result["num_found"]:
                break

        return rule_compliances

    def get_rule_compliance_devices(self, rule_id, query=""):
        """
        Fetches device compliances for a specific rule.

        Required Permissions:
            complianceAssessment.data(READ)

        Args:
            rule_id (str): Rule id to fetch device compliances
            query (str, optional): The query to filter results.

        Returns:
            [dict]: List of Device Compliances

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark_set = cb.select(ComplianceBenchmark).first()
            >>> rules = benchmark_set.get_rule_compliance_devices("BCCAAACA-F0BE-4C0F-BE0A-A09FC1641EE2")
        """
        url = self.urlobject.format(self._cb.credentials.org_key) + \
            f"{self.id}/compliance/rules/{rule_id}/devices/_search"

        current = 0
        device_compliances = []
        while True:
            resp = self._cb.post_object(url, body={
                "query": query,
                "rows": 10000,
                "start": current,
                "sort": [
                    {
                        "field": "device_name",
                        "order": "DESC"
                    }
                ]
            })
            result = resp.json()

            device_compliances.extend(result.get("results", []))
            current = len(device_compliances)

            if current >= result["num_found"]:
                break

        return device_compliances


class ComplianceBenchmarkQuery(BaseQuery, QueryBuilderSupportMixin, CriteriaBuilderSupportMixin,
                               IterableQueryMixin, AsyncQueryMixin):
    """A class representing a query for Compliance Benchmark."""

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

    def sort_by(self, key, direction='ASC'):
        """
        Sets the sorting behavior on a query's results.

        Arguments:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            Query: The query with sorting parameters.

        Raises:
            ApiError: If an invalid sort direction is specified.

        Example:
            To sort by a field in descending order:

            >>> cb = CBCloudAPI(profile="example_profile")
            >>> benchmark_sets = cb.select(ComplianceBenchmark).sort_by("name", direction="DESC")
            >>> print(*benchmark_sets)
        """
        if direction.upper() not in ('ASC', 'DESC'):
            raise ApiError('invalid sort direction specified')
        self._sortcriteria = {'field': key, 'order': direction}
        return self

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
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, item[self._doc_class.primary_key], initial_data=item)
                current += 1
                numrows += 1

                if max_rows > 0 and numrows == max_rows:
                    break

            if current >= self._total_results:
                break

    def _run_async_query(self, context):
        """
        Run an asynchronous query and retrieve the results.

        Args:
            context: The context for the query.

        Returns:
            dict: The JSON response containing the query results.
        """
        url = self._build_url("_search")
        output = []
        while not self._count_valid or len(output) < self._total_results:
            request = self._build_request(len(output), -1)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            if not self._count_valid:
                self._total_results = result["num_found"]
                self._count_valid = True

            results = result.get("results", [])
            output += [self._doc_class(self._cb, item[self._doc_class.primary_key], item) for item in results]
        return output
