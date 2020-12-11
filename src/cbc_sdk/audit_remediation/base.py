#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model and Query Classes for Audit and Remediation"""

from __future__ import absolute_import
from cbc_sdk.base import UnrefreshableModel, NewBaseModel, QueryBuilder, QueryBuilderSupportMixin, IterableQueryMixin
from cbc_sdk.platform import PlatformQueryBase
from cbc_sdk.errors import ApiError, ServerError
import logging
import time


log = logging.getLogger(__name__)


"""Audit and Remediation Models"""


class Run(NewBaseModel):
    """Represents an Audit and Remediation run.

    Example:
    >>> run = cb.select(Run, run_id)
    >>> print(run.name, run.sql, run.create_time)
    >>> print(run.status, run.match_count)
    >>> run.refresh()
    """
    primary_key = "id"
    swagger_meta_file = "audit_remediation/models/run.yaml"
    urlobject = "/livequery/v1/orgs/{}/runs"
    urlobject_single = "/livequery/v1/orgs/{}/runs/{}"
    _is_deleted = False

    def __init__(self, cb, model_unique_id=None, initial_data=None):
        """Initialize a Run object with initial_data."""
        if initial_data is not None:
            item = initial_data
        elif model_unique_id is not None:
            url = self.urlobject_single.format(cb.credentials.org_key, model_unique_id)
            item = cb.get_object(url)

        model_unique_id = item.get("id")

        super(Run, self).__init__(
            cb,
            model_unique_id=model_unique_id,
            initial_data=item,
            force_init=False,
            full_doc=True,
        )

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return RunQuery(cls, cb)

    def _refresh(self):
        if self._is_deleted:
            raise ApiError("cannot refresh a deleted query")
        url = self.urlobject_single.format(self._cb.credentials.org_key, self.id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._last_refresh_time = time.time()
        return True

    def stop(self):
        """Stop a running query.

        Returns:
            (bool): True if query was stopped successfully, False otherwise.

        Raises:
            ServerError: If the server response cannot be parsed as JSON.
        """
        if self._is_deleted:
            raise ApiError("cannot stop a deleted query")
        url = self.urlobject_single.format(self._cb.credentials.org_key, self.id) + "/status"
        result = self._cb.put_object(url, {'status': 'CANCELLED'})
        if (result.status_code == 200):
            try:
                self._info = result.json()
                self._last_refresh_time = time.time()
                return True
            except Exception:
                raise ServerError(result.status_code, "Cannot parse response as JSON: {0:s}".format(result.content))
        return False

    def delete(self):
        """Delete a query.

        Returns:
            (bool): True if the query was deleted successfully, False otherwise.
        """
        if self._is_deleted:
            return True  # already deleted
        url = self.urlobject_single.format(self._cb.credentials.org_key, self.id)
        result = self._cb.delete_object(url)
        if result.status_code in [200, 204]:
            self._is_deleted = True
            return True
        return False


class RunHistory(Run):
    """Represents a historical Audit and Remediation `Run`."""
    urlobject_history = "/livequery/v1/orgs/{}/runs/_search"

    def __init__(self, cb, initial_data=None):
        """Initialize a RunHistory object with initial_data."""
        item = initial_data
        model_unique_id = item.get("id")
        super(Run, self).__init__(cb,
                                  model_unique_id, initial_data=item,
                                  force_init=False, full_doc=True)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return RunHistoryQuery(cls, cb)


class Result(UnrefreshableModel):
    """Represents a single result from an Audit and Remediation `Run`."""
    primary_key = "id"
    swagger_meta_file = "audit_remediation/models/result.yaml"
    urlobject = "/livequery/v1/orgs/{}/runs/{}/results/_search"

    class Device(UnrefreshableModel):
        """Represents device information for a result."""
        primary_key = "id"

        def __init__(self, cb, initial_data):
            """Initialize a Device Result object with initial_data."""
            super(Result.Device, self).__init__(
                cb,
                model_unique_id=initial_data["id"],
                initial_data=initial_data,
                force_init=False,
                full_doc=True,
            )

    class Fields(UnrefreshableModel):
        """Represents the fields of a result."""
        def __init__(self, cb, initial_data):
            """Initialize a Result Fields object with initial_data."""
            super(Result.Fields, self).__init__(
                cb,
                model_unique_id=None,
                initial_data=initial_data,
                force_init=False,
                full_doc=True,
            )

    class Metrics(UnrefreshableModel):
        """Represents the metrics of a result."""
        def __init__(self, cb, initial_data):
            """Initialize a Result Metrics object with initial_data."""
            super(Result.Metrics, self).__init__(
                cb,
                model_unique_id=None,
                initial_data=initial_data,
                force_init=False,
                full_doc=True,
            )

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return ResultQuery(cls, cb)

    def __init__(self, cb, initial_data):
        """Initialize a Result object with initial_data.

        Device, Fields, and Metrics objects are attached using initial_data.
        """
        super(Result, self).__init__(
            cb,
            model_unique_id=initial_data["id"],
            initial_data=initial_data,
            force_init=False,
            full_doc=True,
        )
        self._run_id = initial_data["id"]
        self._device = Result.Device(cb, initial_data=initial_data["device"])
        self._fields = Result.Fields(cb, initial_data=initial_data["fields"])
        if "metrics" in initial_data:
            self._metrics = Result.Metrics(cb, initial_data=initial_data["metrics"])
        else:
            self._metrics = Result.Metrics(cb, initial_data=None)

    @property
    def device_(self):
        """Returns the reified `Result.Device` for this result."""
        return self._device

    @property
    def fields_(self):
        """Returns the reified `Result.Fields` for this result."""
        return self._fields

    @property
    def metrics_(self):
        """Returns the reified `Result.Metrics` for this result."""
        return self._metrics

    def query_device_summaries(self):
        """Returns a ResultQuery for a DeviceSummary.

        This represents the search for a summary of results from a single device of a `Run`.
        """
        return self._cb.select(DeviceSummary).run_id(self._run_id)

    def query_result_facets(self):
        """Returns a ResultQuery for a ResultFacet.

        This represents the search for a summary of results from a single field of a `Run`.
        """
        return self._cb.select(ResultFacet).run_id(self._run_id)

    def query_device_summary_facets(self):
        """Returns a ResultQuery for a DeviceSummaryFacet.

        This represents the search for a summary of a single device summary of a `Run`.
        """
        return self._cb.select(DeviceSummaryFacet).run_id(self._run_id)


class DeviceSummary(UnrefreshableModel):
    """Represents the summary of results from a single device during a single Audit and Remediation `Run`."""
    primary_key = "device_id"
    swagger_meta_file = "audit_remediation/models/device_summary.yaml"
    urlobject = "/livequery/v1/orgs/{}/runs/{}/results/device_summaries/_search"

    class Metrics(UnrefreshableModel):
        """Represents the metrics for a result."""
        def __init__(self, cb, initial_data):
            """Initialize a DeviceSummary Metrics object with initial_data."""
            super(DeviceSummary.Metrics, self).__init__(
                cb,
                model_unique_id=None,
                initial_data=initial_data,
                force_init=False,
                full_doc=True,
            )

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return ResultQuery(cls, cb)

    def __init__(self, cb, initial_data):
        """Initialize a DeviceSummary object with initial_data."""
        super(DeviceSummary, self).__init__(
            cb,
            model_unique_id=initial_data["device"]["id"],
            initial_data=initial_data["device"],
            force_init=False,
            full_doc=True,
        )
        self._metrics = DeviceSummary.Metrics(cb, initial_data=initial_data["metrics"])

    @property
    def metrics_(self):
        """Returns the reified `DeviceSummary.Metrics` for this result."""
        return self._metrics


class ResultFacet(UnrefreshableModel):
    """Represents the summary of results for a single field in an Audit and Remediation `Run`."""
    primary_key = "field"
    swagger_meta_file = "audit_remediation/models/facet.yaml"
    urlobject = "/livequery/v1/orgs/{}/runs/{}/results/_facet"

    class Values(UnrefreshableModel):
        """Represents the values associated with a field."""
        def __init__(self, cb, initial_data):
            """Initialize a ResultFacet Values object with initial_data."""
            super(ResultFacet.Values, self).__init__(
                cb,
                model_unique_id=None,
                initial_data=initial_data,
                force_init=False,
                full_doc=True,
            )

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return FacetQuery(cls, cb)

    def __init__(self, cb, initial_data):
        """Initialize a ResultFacet object with initial_data."""
        super(ResultFacet, self).__init__(
            cb,
            model_unique_id=None,
            initial_data=initial_data,
            force_init=False,
            full_doc=True
        )
        self._values = ResultFacet.Values(cb, initial_data=initial_data["values"])

    @property
    def values_(self):
        """Returns the reified `ResultFacet.Values` for this result."""
        return self._values


class DeviceSummaryFacet(ResultFacet):
    """Represents the summary of results for a single device summary in an Audit and Remediation `Run`."""
    urlobject = "/livequery/v1/orgs/{}/runs/{}/results/device_summaries/_facet"

    def __init__(self, cb, initial_data):
        """Initialize a DeviceSummaryFacet object with initial_data."""
        super(DeviceSummaryFacet, self).__init__(cb, initial_data)


"""Audit and Remediation Queries"""


class RunQuery(PlatformQueryBase):
    """Represents a query that either creates or retrieves the status of a LiveQuery run."""

    def __init__(self, doc_class, cb):
        """Initialize a RunQuery object."""
        super().__init__(doc_class, cb)
        self._query_token = None
        self._query_body = {"device_filter": {}}
        self._device_filter = self._query_body["device_filter"]

    def schedule(self, rrule, timezone):
        """
        Sets a schedule for the SQL Query to recur

        A schedule requires an rrule and a timezone to determine the time to rerun the SQL query. rrule
        is defined in RFC 2445 however only a subset of the functionality is supported here. If a Run
        is created with a schedule then the Run will contain a template_id to the corresponding template
        and a new Run will be created each time the schedule is met.

        DAILY

        | Field    | Values  |
        | -------- | ------- |
        | BYSECOND | 0       |
        | BYMINUTE | 0 or 30 |
        | BYHOUR   | 0 to 23 |

        # Daily at 1:30PM
        RRULE:FREQ=DAILY;BYHOUR=13;BYMINUTE=30;BYSECOND=0

        WEEKLY

        | Field    | Values                                  |
        | -------- | --------------------------------------- |
        | BYSECOND | 0                                       |
        | BYMINUTE | 0 or 30                                 |
        | BYHOUR   | 0 to 23                                 |
        | BYDAY    | One or more: SU, MO, TU, WE, TH, FR, SA |

        # Monday and Friday of the week at 2:30 AM
        RRULE:FREQ=WEEKLY;BYDAY=MO,FR;BYHOUR=13;BYMINUTE=30;BYSECOND=0

        MONTHLY

        Note: Either (BYDAY and BYSETPOS) or BYMONTHDAY is required.

        | Field      | Values                                  |
        | ---------- | --------------------------------------- |
        | BYSECOND   | 0                                       |
        | BYMINUTE   | 0 or 30                                 |
        | BYHOUR     | 0 to 23                                 |
        | BYDAY      | One or more: SU, MO, TU, WE, TH, FR, SA |
        | BYSETPOS   | -1, 1, 2, 3, 4                          |
        | BYMONTHDAY | One or more: 1 to 28                    |

        # Last Monday of the Month at 2:30 AM
        RRULE:FREQ=MONTHLY;BYDAY=MO;BYSETPOS=-1;BYHOUR=2;BYMINUTE=30;BYSECOND=0

        # 1st and 15th of the Month at 2:30 AM
        RRULE:FREQ=DAILY;BYMONTHDAY=1,15;BYHOUR=2;BYMINUTE=30;BYSECOND=0

        Arguments:
            rrule (string): A recurrence rule (RFC 2445) specifying the frequency and time at which the query will recur
            timezone (string): The timezone database name to use as a base for the rrule

        Returns:
            The RunQuery with a recurrence schedule.
        """
        self._query_body["schedule"] = {}
        self._query_body["schedule"]["rrule"] = rrule
        self._query_body["schedule"]["timezone"] = timezone
        return self

    def device_ids(self, device_ids):
        """Restricts the devices that this Audit and Remediation run is performed on to the given IDs.

        Arguments:
            device_ids ([int]): Device IDs to perform the Run on.

        Returns:
            The RunQuery with specified device_ids.
        """
        if not all(isinstance(device_id, int) for device_id in device_ids):
            raise ApiError("One or more invalid device IDs")
        self._device_filter["device_id"] = device_ids
        return self

    def device_types(self, device_types):
        """Restricts the devices that this Audit and Remediation run is performed on to the given OS.

        Arguments:
            device_types ([str]): Device types to perform the Run on.

        Returns:
            The RunQuery object with specified device_types.

        Note:
            Device type can be one of ["WINDOWS", "MAC", "LINUX"].
        """
        if not all(isinstance(device_type, str) for device_type in device_types):
            raise ApiError("device_type must be a list of strings, including"
                           " 'WINDOWS', 'MAC', and/or 'LINUX'")
        self._device_filter["os"] = device_types
        return self

    def policy_id(self, policy_id):
        """Restricts this Audit and Remediation run to the given policy ID.

        Arguments:
            policy_id (int) or (list[int]): Policy ID to perform the Run on.

        Returns:
            The RunQuery object with specified policy_id.
        """
        if isinstance(policy_id, list) and isinstance(policy_id[0], int):
            self._device_filter["policy_id"] = policy_id
        elif isinstance(policy_id, int):
            self._device_filter["policy_id"] = [policy_id]
        else:
            raise ApiError("Policy ID must be an integer or a list containing one"
                           f"integer. Type is {type(policy_id)}")
        return self

    def where(self, sql):
        """Sets this Audit and Remediation run's underlying SQL.

        Arguments:
            sql (str): The SQL to execute for the Run.

        Returns:
            The RunQuery object with specified sql.
        """
        self._query_body["sql"] = sql
        return self

    def name(self, name):
        """Sets this Audit and Remediation run's name.

        If no name is explicitly set, the run is named after its SQL.

        Arguments:
            name (str): The name for this Run.

        Returns:
            The RunQuery object with specified name.
        """
        self._query_body["name"] = name
        return self

    def notify_on_finish(self):
        """Sets the notify-on-finish flag on this Audit and Remediation run.

        Returns:
            The RunQuery object with `notify_on_finish` set to True.
        """
        self._query_body["notify_on_finish"] = True
        return self

    def submit(self):
        """Submits this Audit and Remediation run.

        Returns:
            A new `Run` instance containing the run's status.

        Raises:
            ApiError: If the Run does not have SQL set, or if the Run
                has already been submitted.
        """
        if self._query_token is not None:
            raise ApiError(
                "Query already submitted: token {0}".format(self._query_token)
            )

        if "sql" not in self._query_body:
            raise ApiError("Missing Audit and Remediation SQL")

        url = self._doc_class.urlobject.format(self._cb.credentials.org_key)
        resp = self._cb.post_object(url, body=self._query_body)

        self._query_token = resp.json().get("id")

        return self._doc_class(self._cb, initial_data=resp.json())


class RunHistoryQuery(PlatformQueryBase, QueryBuilderSupportMixin, IterableQueryMixin):
    """Represents a query that retrieves historic LiveQuery runs."""
    def __init__(self, doc_class, cb):
        """Initialize a RunHistoryQuery object."""
        super().__init__(doc_class, cb)
        self._query_builder = QueryBuilder()
        self._sort = {}

    def sort_by(self, key, direction="ASC"):
        """Sets the sorting behavior on a query's results.

        Arguments:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            RunHistoryQuery object with specified sorting key and order.

        Example:

        >>> cb.select(Result).run_id(my_run).where(username="foobar").sort_by("uid")
        """
        self._sort.update({"field": key, "order": direction})
        return self

    def _build_request(self, start, rows):
        request = {"start": start}

        if self._query_builder:
            request["query"] = self._query_builder._collapse()
        if rows != 0:
            request["rows"] = rows
        if self._sort:
            request["sort"] = [self._sort]

        return request

    def _count(self):
        if self._count_valid:
            return self._total_results

        url = self._doc_class.urlobject_history.format(
            self._cb.credentials.org_key
        )
        request = self._build_request(start=0, rows=0)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()

        self._total_results = result["num_found"]
        self._count_valid = True

        return self._total_results

    def _perform_query(self, start=0, rows=0):
        url = self._doc_class.urlobject_history.format(
            self._cb.credentials.org_key
        )
        current = start
        numrows = 0
        still_querying = True
        while still_querying:
            request = self._build_request(start, rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, item)
                current += 1
                numrows += 1

                if rows and numrows == rows:
                    still_querying = False
                    break

            start = current
            if current >= self._total_results:
                still_querying = False
                break


class ResultQuery(PlatformQueryBase, QueryBuilderSupportMixin, IterableQueryMixin):
    """Represents a query that retrieves results from a LiveQuery run."""
    def __init__(self, doc_class, cb):
        """Initialize a ResultQuery object."""
        super().__init__(doc_class, cb)
        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._sort = {}
        self._batch_size = 100
        self._run_id = None

    def update_criteria(self, key, newlist):
        """Update the criteria on this query with a custom criteria key.

        Args:
            key (str): The key for the criteria item to be set.
            newlist (list): List of values to be set for the criteria item.

        Returns:
            The ResultQuery with specified custom criteria.

        Example:
            query = api.select(Alert).update_criteria("my.criteria.key", ["criteria_value"])

        Note: Use this method if there is no implemented method for your desired criteria.
        """
        self._update_criteria(key, newlist)
        return self

    def _update_criteria(self, key, newlist):
        """
        Updates a list of criteria being collected for a query, by setting or appending items.

        Args:
            key (str): The key for the criteria item to be set.
            newlist (list): List of values to be set for the criteria item.
        """
        oldlist = self._criteria.get(key, [])
        self._criteria[key] = oldlist + newlist

    def set_device_ids(self, device_ids):
        """Sets the device.id criteria filter.

        Arguments:
            device_ids ([int]): Device IDs to filter on.

        Returns:
            The ResultQuery with specified device.id.
        """
        if not all(isinstance(device_id, int) for device_id in device_ids):
            raise ApiError("One or more invalid device IDs")
        self._update_criteria("device.id", device_ids)
        return self

    def set_device_names(self, device_names):
        """Sets the device.name criteria filter.

        Arguments:
            device_names ([str]): Device names to filter on.

        Returns:
            The ResultQuery with specified device.name.
        """
        if not all(isinstance(name, str) for name in device_names):
            raise ApiError("One or more invalid device names")
        self._update_criteria("device.name", device_names)
        return self

    def set_device_os(self, device_os):
        """Sets the device.os criteria.

        Arguments:
            device_os ([str]): Device OS's to filter on.

        Returns:
            The ResultQuery object with specified device_os.

        Note:
            Device OS's can be one or more of ["WINDOWS", "MAC", "LINUX"].
        """
        if not all(isinstance(os, str) for os in device_os):
            raise ApiError("device_type must be a list of strings, including"
                           " 'WINDOWS', 'MAC', and/or 'LINUX'")
        self._update_criteria("device.os", device_os)
        return self

    def set_policy_ids(self, policy_ids):
        """Sets the device.policy_id criteria.

        Arguments:
            policy_ids ([int]): Device policy ID's to filter on.

        Returns:
            The ResultQuery object with specified policy_ids.
        """
        if not all(isinstance(id, int) for id in policy_ids):
            raise ApiError("policy_ids must be a list of integers.")
        self._update_criteria("device.policy_id", policy_ids)
        return self

    def set_policy_names(self, policy_names):
        """Sets the device.policy_name criteria.

        Arguments:
            policy_names ([str]): Device policy names to filter on.

        Returns:
            The ResultQuery object with specified policy_names.
        """
        if not all(isinstance(name, str) for name in policy_names):
            raise ApiError("policy_names must be a list of strings.")
        self._update_criteria("device.policy_name", policy_names)
        return self

    def set_statuses(self, statuses):
        """Sets the status criteria.

        Arguments:
            statuses ([str]): Query statuses to filter on.

        Returns:
            The ResultQuery object with specified statuses.
        """
        if not all(isinstance(status, str) for status in statuses):
            raise ApiError("statuses must be a list of strings.")
        self._update_criteria("status", statuses)
        return self

    def sort_by(self, key, direction="ASC"):
        """Sets the sorting behavior on a query's results.

        Arguments:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            ResultQuery object with specified sorting key and order.

        Example:

        >>> cb.select(Result).run_id(my_run).where(username="foobar").sort_by("uid")
        """
        self._sort.update({"field": key, "order": direction})
        return self

    def run_id(self, run_id):
        """Sets the run ID to query results for.

        Arguments:
            run_id (int): The run ID to retrieve results for.

        Returns:
            ResultQuery object with specified run_id.

        Example:

        >>> cb.select(Result).run_id(my_run)
        """
        self._run_id = run_id
        return self

    def _build_request(self, start, rows):
        request = {"start": start, "query": self._query_builder._collapse()}

        if rows != 0:
            request["rows"] = rows
        if self._criteria:
            request["criteria"] = self._criteria
        if self._sort:
            request["sort"] = [self._sort]

        return request

    def _count(self):
        if self._count_valid:
            return self._total_results

        if self._run_id is None:
            raise ApiError("Can't retrieve count without a run ID")

        url = self._doc_class.urlobject.format(
            self._cb.credentials.org_key, self._run_id
        )
        request = self._build_request(start=0, rows=0)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()

        self._total_results = result["num_found"]
        self._count_valid = True

        return self._total_results

    def _perform_query(self, start=0, rows=0):
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")

        url = self._doc_class.urlobject.format(
            self._cb.credentials.org_key, self._run_id
        )
        current = start
        numrows = 0
        still_querying = True
        while still_querying:
            request = self._build_request(start, rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, item)
                current += 1
                numrows += 1

                if rows and numrows == rows:
                    still_querying = False
                    break

            start = current
            if current >= self._total_results:
                still_querying = False
                break


class FacetQuery(PlatformQueryBase, QueryBuilderSupportMixin, IterableQueryMixin):
    """Represents a query that receives facet information from a LiveQuery run."""
    def __init__(self, doc_class, cb):
        """Initialize a FacetQuery object."""
        super().__init__(doc_class, cb)
        self._query_builder = QueryBuilder()
        self._facet_fields = []
        self._criteria = {}
        self._run_id = None

    def facet_field(self, field):
        """Sets the facet fields to be received by this query.

        Arguments:
            field (str or [str]): Field(s) to be received.

        Returns:
            FacetQuery that will receive field(s) facet_field.

        Example:

        >>> cb.select(ResultFacet).run_id(my_run).facet_field(["device.policy_name", "device.os"])
        """
        if isinstance(field, str):
            self._facet_fields.append(field)
        else:
            for name in field:
                self._facet_fields.append(name)
        return self

    def update_criteria(self, key, newlist):
        """Update the criteria on this query with a custom criteria key.

        Args:
            key (str): The key for the criteria item to be set.
            newlist (list): List of values to be set for the criteria item.

        Returns:
            The FacetQuery with specified custom criteria.

        Example:
            query = api.select(ResultFacet).update_criteria("my.criteria.key", ["criteria_value"])

        Note: Use this method if there is no implemented method for your desired criteria.
        """
        self._update_criteria(key, newlist)
        return self

    def _update_criteria(self, key, newlist):
        """
        Updates a list of criteria being collected for a query, by setting or appending items.

        Args:
            key (str): The key for the criteria item to be set.
            newlist (list): List of values to be set for the criteria item.
        """
        oldlist = self._criteria.get(key, [])
        self._criteria[key] = oldlist + newlist

    def set_device_ids(self, device_ids):
        """Sets the device.id criteria filter.

        Arguments:
            device_ids ([int]): Device IDs to filter on.

        Returns:
            The FacetQuery with specified device.id.
        """
        if not all(isinstance(device_id, int) for device_id in device_ids):
            raise ApiError("One or more invalid device IDs")
        self._update_criteria("device.id", device_ids)
        return self

    def set_device_names(self, device_names):
        """Sets the device.name criteria filter.

        Arguments:
            device_names ([str]): Device names to filter on.

        Returns:
            The FacetQuery with specified device.name.
        """
        if not all(isinstance(name, str) for name in device_names):
            raise ApiError("One or more invalid device names")
        self._update_criteria("device.name", device_names)
        return self

    def set_device_os(self, device_os):
        """Sets the device.os criteria.

        Arguments:
            device_os ([str]): Device OS's to filter on.

        Returns:
            The FacetQuery object with specified device_os.

        Note:
            Device OS's can be one or more of ["WINDOWS", "MAC", "LINUX"].
        """
        if not all(isinstance(os, str) for os in device_os):
            raise ApiError("device_type must be a list of strings, including"
                           " 'WINDOWS', 'MAC', and/or 'LINUX'")
        self._update_criteria("device.os", device_os)
        return self

    def set_policy_ids(self, policy_ids):
        """Sets the device.policy_id criteria.

        Arguments:
            policy_ids ([int]): Device policy ID's to filter on.

        Returns:
            The FacetQuery object with specified policy_ids.
        """
        if not all(isinstance(id, int) for id in policy_ids):
            raise ApiError("policy_ids must be a list of integers.")
        self._update_criteria("device.policy_id", policy_ids)
        return self

    def set_policy_names(self, policy_names):
        """Sets the device.policy_name criteria.

        Arguments:
            policy_names ([str]): Device policy names to filter on.

        Returns:
            The FacetQuery object with specified policy_names.
        """
        if not all(isinstance(name, str) for name in policy_names):
            raise ApiError("policy_names must be a list of strings.")
        self._update_criteria("device.policy_name", policy_names)
        return self

    def set_statuses(self, statuses):
        """Sets the status criteria.

        Arguments:
            statuses ([str]): Query statuses to filter on.

        Returns:
            The FacetQuery object with specified statuses.
        """
        if not all(isinstance(status, str) for status in statuses):
            raise ApiError("statuses must be a list of strings.")
        self._update_criteria("status", statuses)
        return self

    def run_id(self, run_id):
        """Sets the run ID to query results for.

        Arguments:
            run_id (int): The run ID to retrieve results for.

        Returns:
            FacetQuery object with specified run_id.

        Example:
        >>> cb.select(ResultFacet).run_id(my_run)
        """
        self._run_id = run_id
        return self

    def _build_request(self, rows):
        terms = {"fields": self._facet_fields}
        if rows != 0:
            terms["rows"] = rows
        request = {"query": self._query_builder._collapse(), "terms": terms}
        if self._criteria:
            request["criteria"] = self._criteria
        return request

    def _perform_query(self, rows=0):
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")

        url = self._doc_class.urlobject.format(
            self._cb.credentials.org_key, self._run_id
        )
        request = self._build_request(rows)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        results = result.get("terms", [])
        for item in results:
            yield self._doc_class(self._cb, item)


class Template(Run):
    """Represents an Audit and Remediation Live Query Template .

    Example:
    >>> template = cb.select(Template, template_id)
    >>> print(template.name, template.sql, template.create_time)
    >>> print(template.status, template.match_count, template.schedule)
    >>> template.refresh()
    """
    primary_key = "id"
    swagger_meta_file = "audit_remediation/models/template.yaml"
    urlobject = "/livequery/v1/orgs/{}/templates"
    urlobject_single = "/livequery/v1/orgs/{}/templates/{}"
    _is_deleted = False

    def __init__(self, cb, model_unique_id=None, initial_data=None):
        """Initialize a Template object with initial_data."""
        if initial_data is not None:
            item = initial_data
        elif model_unique_id is not None:
            url = self.urlobject_single.format(cb.credentials.org_key, model_unique_id)
            item = cb.get_object(url)

        model_unique_id = item.get("id")

        super(Template, self).__init__(
            cb,
            model_unique_id=model_unique_id,
            initial_data=item
        )

    def stop(self):
        """Stop a template.

        Returns:
            (bool): True if query was stopped successfully, False otherwise.

        Raises:
            ServerError: If the server response cannot be parsed as JSON.
        """
        if self._is_deleted:
            raise ApiError("cannot stop a deleted query")
        url = self.urlobject_single.format(self._cb.credentials.org_key, self.id)
        self._info['schedule']['status'] = 'CANCELLED'

        result = self._cb.put_object(url, self._info)
        if (result.status_code == 200):
            try:
                self._info = result.json()
                self._last_refresh_time = time.time()
                return True
            except Exception:
                raise ServerError(result.status_code, "Cannot parse response as JSON: {0:s}".format(result.content))
        return False
