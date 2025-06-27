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

"""Model and Query Classes for Audit and Remediation"""

from __future__ import absolute_import
from cbc_sdk.base import (UnrefreshableModel, NewBaseModel, QueryBuilder,
                          QueryBuilderSupportMixin, IterableQueryMixin, BaseQuery,
                          CriteriaBuilderSupportMixin, AsyncQueryMixin)
from cbc_sdk.platform import Job
from cbc_sdk.errors import ApiError, ServerError, TimeoutError, OperationCancelled
import io
import logging
import time


log = logging.getLogger(__name__)

MAX_RESULTS_LIMIT = 10000


"""Audit and Remediation Models"""


class Run(NewBaseModel):
    """
    Represents an Audit and Remediation run.

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
        """
        Initialize a Run object with initial_data.

        Required Permissions:
            livequery.manage(READ)

        Arguments:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the query run represented.
            initial_data (dict): Initial data used to populate the query run.
        """
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
        """
        Returns the appropriate query object for the Run type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            RunQuery: The query object for the Run type.
        """
        return RunQuery(cls, cb)

    def _refresh(self):
        """
        Rereads the Run data from the server.

        Required Permissions:
            livequery.manage(READ)

        Returns:
            bool: True if refresh was successful, False if not.
        """
        if self._is_deleted:
            raise ApiError("cannot refresh a deleted query")
        url = self.urlobject_single.format(self._cb.credentials.org_key, self.id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._last_refresh_time = time.time()
        return True

    def stop(self):
        """
        Stop a running query.

        Required Permissions:
            livequery.manage(UPDATE)

        Returns:
            bool: True if query was stopped successfully, False otherwise.

        Raises:
            ServerError: If the server response cannot be parsed as JSON.
        """
        if self._is_deleted:
            raise ApiError("cannot stop a deleted query")
        url = self.urlobject_single.format(self._cb.credentials.org_key, self.id) + "/status"
        result = self._cb.put_object(url, {'status': 'CANCELLED'})
        if result.status_code == 200:
            try:
                self._info = result.json()
                self._last_refresh_time = time.time()
                return True
            except Exception:
                raise ServerError(result.status_code, "Cannot parse response as JSON: {0:s}".format(result.content),
                                  uri=url)
        return False

    def delete(self):
        """
        Delete a query.

        Required Permissions:
            livequery.manage(DELETE)

        Returns:
            bool: True if the query was deleted successfully, False otherwise.
        """
        if self._is_deleted:
            return True  # already deleted
        url = self.urlobject_single.format(self._cb.credentials.org_key, self.id)
        result = self._cb.delete_object(url)
        if result.status_code in [200, 204]:
            self._is_deleted = True
            return True
        return False

    def query_results(self):
        """
        Create a Result query that searches for all results on this run.

        The query may be further augmented with additional criteria prior to enumerating its results.

        Returns:
            ResultQuery: A query object which will search for all results for this run.

        Raises:
            ApiError: If the query has been deleted.
        """
        if self._is_deleted:
            raise ApiError("query is deleted")
        return self._cb.select(Result).run_id(self.id)

    def query_device_summaries(self):
        """
        Create a DeviceSummary query that searches for all device summaries on this run.

        The query may be further augmented with additional criteria prior to enumerating its results.

        Returns:
            ResultQuery: A query object which will search for all device summaries for this run.

        Raises:
            ApiError: If the query has been deleted.
        """
        if self._is_deleted:
            raise ApiError("query is deleted")
        return self._cb.select(DeviceSummary).run_id(self.id)

    def query_facets(self):
        """
        Create a ResultFacet query that searches for all result facets on this run.

        The query may be further augmented with additional criteria prior to enumerating its results.

        Returns:
            FacetQuery: A query object which will search for all result facets for this run.

        Raises:
            ApiError: If the query has been deleted.
        """
        if self._is_deleted:
            raise ApiError("query is deleted")
        return self._cb.select(ResultFacet).run_id(self.id)


class RunHistory(Run):
    """Represents a historical Audit and Remediation `Run`."""
    urlobject_history = "/livequery/v1/orgs/{}/runs/_search"

    def __init__(self, cb, initial_data=None):
        """
        Initialize a RunHistory object with initial_data.

        Arguments:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            initial_data (dict): Initial data used to populate the history object.
        """
        item = initial_data
        model_unique_id = item.get("id")
        super(Run, self).__init__(cb, model_unique_id, initial_data=item, force_init=False, full_doc=True)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the RunHistory type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            RunHistoryQuery: The query object for the Run type.
        """
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
            """
            Initialize a Device Result object with initial_data.

            Arguments:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                initial_data (dict): Initial data used to populate the result.
            """
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
            """
            Initialize a Result Fields object with initial_data.

            Arguments:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                initial_data (dict): Initial data used to populate the result.
            """
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
            """
            Initialize a Result Metrics object with initial_data.

            Arguments:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                initial_data (dict): Initial data used to populate the result.
            """
            super(Result.Metrics, self).__init__(
                cb,
                model_unique_id=None,
                initial_data=initial_data,
                force_init=False,
                full_doc=True,
            )

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the Result type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            ResultQuery: The query object for the Result type.
        """
        return ResultQuery(cls, cb)

    def __init__(self, cb, initial_data):
        """
        Initialize a Result object with initial_data.

        Device, Fields, and Metrics objects are attached using initial_data.

        Arguments:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            initial_data (dict): Initial data used to populate the result.
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

    def to_json(self):
        """
        Return a json object of the response.

        Returns:
            dict: The raw json Result.
        """
        return self._info

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
        """
        Returns a ResultQuery for a DeviceSummary.

        This represents the search for a summary of results from a single device of a `Run`.  The query may be further
        augmented with additional criteria prior to enumerating its results.

        Returns:
            ResultQuery: The query object returned by this operation.
        """
        return self._cb.select(DeviceSummary).run_id(self._run_id)

    def query_result_facets(self):
        """
        Returns a ResultQuery for a ResultFacet.

        This represents the search for a summary of results from a single field of a `Run`. The query may be further
        augmented with additional criteria prior to enumerating its results.

        Returns:
            ResultQuery: The query object returned by this operation.
        """
        return self._cb.select(ResultFacet).run_id(self._run_id)

    def query_device_summary_facets(self):
        """
        Returns a ResultQuery for a DeviceSummaryFacet.

        This represents the search for a summary of a single device summary of a `Run`. The query may be further
        augmented with additional criteria prior to enumerating its results.

        Returns:
            ResultQuery: The query object returned by this operation.
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
            """
            Initialize a DeviceSummary Metrics object with initial_data.

            Arguments:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                initial_data (dict): Initial data used to populate the result.
            """
            super(DeviceSummary.Metrics, self).__init__(
                cb,
                model_unique_id=None,
                initial_data=initial_data,
                force_init=False,
                full_doc=True,
            )

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the DeviceSummary type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            ResultQuery: The query object for the DeviceSummary type.
        """
        return ResultQuery(cls, cb)

    def __init__(self, cb, initial_data):
        """
        Initialize a DeviceSummary object with initial_data.

        Arguments:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            initial_data (dict): Initial data used to populate the result.
        """
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
            """
            Initialize a ResultFacet Values object with initial_data.

            Arguments:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                initial_data (dict): Initial data used to populate the result.
            """
            super(ResultFacet.Values, self).__init__(
                cb,
                model_unique_id=None,
                initial_data=initial_data,
                force_init=False,
                full_doc=True,
            )

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the ResultFacet type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            FacetQuery: The query object for the ResultFacet type.
        """
        return FacetQuery(cls, cb)

    def __init__(self, cb, initial_data):
        """
        Initialize a ResultFacet object with initial_data.

        Arguments:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            initial_data (dict): Initial data used to populate the result.
        """
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
        """
        Initialize a DeviceSummaryFacet object with initial_data.

        Arguments:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            initial_data (dict): Initial data used to populate the result.
        """
        super(DeviceSummaryFacet, self).__init__(cb, initial_data)


class Template(Run):
    """
    Represents an Audit and Remediation Live Query Template.

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
        """
        Initialize a Template object with initial_data.

        Required Permissions:
            livequery.manage(READ)

        Arguments:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the query run represented.
            initial_data (dict): Initial data used to populate the query run.
        """
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
        """
        Stop a template.

        Required Permissions:
            livequery.manage(UPDATE)

        Returns:
            bool: True if query was stopped successfully, False otherwise.

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
                raise ServerError(result.status_code, "Cannot parse response as JSON: {0:s}".format(result.content),
                                  uri=url)
        return False

    def query_runs(self):
        """
        Create a RunHistory query that searches for all runs created by this template ID.

        The query may be further augmented with additional criteria prior to enumerating its results.

        Returns:
            RunHistoryQuery: A query object which will search for all runs based on this template.
        """
        if self._is_deleted:
            raise ApiError("cannot query runs for a deleted query")
        return self._cb.select(RunHistory).set_template_ids([self.id])


class TemplateHistory(Template):
    """Represents a historical Audit and Remediation `Template`."""
    urlobject_history = "/livequery/v1/orgs/{}/templates/_search"

    def __init__(self, cb, initial_data=None):
        """
        Initialize a Template object with initial_data.

        Required Permissions:
            livequery.manage(READ)

        Arguments:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            initial_data (dict): Initial data used to populate the query run.
        """
        item = initial_data
        model_unique_id = item.get("id")
        super(Run, self).__init__(cb,
                                  model_unique_id, initial_data=item,
                                  force_init=False, full_doc=True)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the TemplateHistory type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            TemplateHistoryQuery: The query object for the TemplateHistory type.
        """
        return TemplateHistoryQuery(cls, cb)


"""Audit and Remediation Queries"""


class RunQuery(BaseQuery, AsyncQueryMixin):
    """Represents a query that either creates or retrieves the status of a LiveQuery run."""

    def __init__(self, doc_class, cb):
        """
        Initialize the RunQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(RunQuery, self).__init__()

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

        Example RRule, Daily

            .. csv-table::
                :header: "Field", "Values"
                :widths: 20, 20

                "BYSECOND","0"
                "BYMINUTE", "0 or 30"
                "BYHOUR", "0 to 23"

            Daily at 1:30PM

            `RRULE:FREQ=DAILY;BYHOUR=13;BYMINUTE=30;BYSECOND=0`

        Example RRule, Weekly

            .. csv-table::
                :header: "Field", "Values"
                :widths: 20, 20

                "BYSECOND", "0"
                "BYMINUTE", "0"
                "BYHOUR", "0 to 23"
                "BYDAY", "One or more: SU, MO, TU, WE, TH, FR, SA"

            Monday and Friday of the week at 2:30 AM

            `RRULE:FREQ=WEEKLY;BYDAY=MO,FR;BYHOUR=13;BYMINUTE=30;BYSECOND=0`

        Example RRule, Monthly

            Note: Either (BYDAY and BYSETPOS) or BYMONTHDAY is required.

            .. csv-table::
                :header: "Field", "Values"
                :widths: 20, 20

                "BYSECOND", "0"
                "BYMINUTE", "0 or 30"
                "BYHOUR", "0 to 23"
                "BYDAY", "One or more: SU, MO, TU, WE, TH, FR, SA"
                "BYSETPOS", "-1, 1, 2, 3, 4"
                "BYMONTHDAY", "One or more: 1 to 28"

            Last Monday of the Month at 2:30 AM

            `RRULE:FREQ=MONTHLY;BYDAY=MO;BYSETPOS=-1;BYHOUR=2;BYMINUTE=30;BYSECOND=0`

            1st and 15th of the Month at 2:30 AM

            `RRULE:FREQ=DAILY;BYMONTHDAY=1,15;BYHOUR=2;BYMINUTE=30;BYSECOND=0`

        Arguments:
            rrule (string): A recurrence rule (RFC 2445) specifying the frequency and time at which the query will recur
            timezone (string): The timezone database name to use as a base for the rrule

        Returns:
            RunQuery: The RunQuery with a recurrence schedule.
        """
        self._query_body["schedule"] = {}
        self._query_body["schedule"]["rrule"] = rrule
        self._query_body["schedule"]["timezone"] = timezone
        return self

    def device_ids(self, device_ids):
        """
        Restricts the devices that this Audit and Remediation run is performed on to the given IDs.

        Arguments:
            device_ids ([int]): Device IDs to perform the Run on.

        Returns:
            RunQuery: The RunQuery with specified device_ids.
        """
        if not all(isinstance(device_id, int) for device_id in device_ids):
            raise ApiError("One or more invalid device IDs")
        self._device_filter["device_id"] = device_ids
        return self

    def device_types(self, device_types):
        """
        Restricts the devices that this Audit and Remediation run is performed on to the given OS.

        Arguments:
            device_types ([str]): Device types to perform the Run on.

        Returns:
            RunQuery: The RunQuery object with specified device_types.

        Note:
            Device type can be one of ["WINDOWS", "MAC", "LINUX"].
        """
        if not all(isinstance(device_type, str) for device_type in device_types):
            raise ApiError("device_type must be a list of strings, including"
                           " 'WINDOWS', 'MAC', and/or 'LINUX'")
        self._device_filter["os"] = device_types
        return self

    def policy_id(self, policy_id):
        """
        Restricts this Audit and Remediation run to the given policy ID.

        Arguments:
            policy_id (int) or (list[int]): Policy ID to perform the Run on.

        Returns:
            RunQuery: The RunQuery object with specified policy_id.
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
        """
        Sets this Audit and Remediation run's underlying SQL.

        Arguments:
            sql (str): The SQL to execute for the Run.

        Returns:
            RunQuery: The RunQuery object with specified sql.
        """
        self._query_body["sql"] = sql
        return self

    def name(self, name):
        """
        Sets this Audit and Remediation run's name.

        If no name is explicitly set, the run is named after its SQL.

        Arguments:
            name (str): The name for this Run.

        Returns:
            RunQuery: The RunQuery object with specified name.
        """
        self._query_body["name"] = name
        return self

    def notify_on_finish(self):
        """
        Sets the notify-on-finish flag on this Audit and Remediation run.

        Returns:
            RunQuery: The RunQuery object with `notify_on_finish` set to True.
        """
        self._query_body["notify_on_finish"] = True
        return self

    def submit(self):
        """
        Submits this Audit and Remediation run.

        Returns:
            Run: A new `Run` instance containing the run's status.

        Raises:
            ApiError: If the Run does not have SQL set, or if the Run has already been submitted.
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

    def _init_async_query(self):
        """
        Initialize an async query and return a context for running in the background. Optional.

        Returns:
            Run: Context for running in the background.
        """
        return self.submit()

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query. Must be implemented in any inheriting classes.

        Args:
            context (object): The context returned by _init_async_query. May be None.

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        context.refresh()  # always do at least one pre-check of context status
        while context.status == 'ACTIVE':
            time.sleep(.5)
            context.refresh()
        if context.status == 'COMPLETE':
            query = context.query_results()
            return query._run_async_query(query._init_async_query())
        elif context.status == 'TIMED_OUT':
            raise TimeoutError("Async query timed out")
        elif context.status == 'CANCELLED':
            raise OperationCancelled("Async query was cancelled")
        raise ApiError(f"Async query terminated with unknown status {context.status}")


class RunHistoryQuery(BaseQuery, QueryBuilderSupportMixin, IterableQueryMixin, CriteriaBuilderSupportMixin,
                      AsyncQueryMixin):
    """Represents a query that retrieves historic LiveQuery runs."""
    def __init__(self, doc_class, cb):
        """
        Initialize the RunHistoryQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(RunHistoryQuery, self).__init__()
        self._query_builder = QueryBuilder()
        self._sort = {}
        self._criteria = {}

    def set_template_ids(self, template_ids):
        """
        Sets the template_id criteria filter.

        Arguments:
            template_ids ([str]): Template IDs to filter on.

        Returns:
            RunHistoryQuery: The RunHistoryQuery with specified template_id.
        """
        if not all(isinstance(template_id, str) for template_id in template_ids):
            raise ApiError("One or more invalid template IDs")
        self._update_criteria("template_id", template_ids)
        return self

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Arguments:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            RunHistoryQuery: RunHistoryQuery object with specified sorting key and order.

        Example:

        >>> cb.select(Result).run_id(my_run).where(username="foobar").sort_by("uid")
        """
        self._sort.update({"field": key, "order": direction})
        return self

    def _build_request(self, start, rows):
        """
        Creates the request body for an API call.

        Args:
            start (int): The row to start the query at.
            rows (int): The maximum number of rows to be returned.

        Returns:
            dict: The complete request body.
        """
        request = {"start": start}

        if self._query_builder:
            query = self._query_builder._collapse()
            if query:
                request["query"] = query
        if rows != 0:
            request["rows"] = rows
        if self._criteria:
            request["criteria"] = self._criteria
        if self._sort:
            request["sort"] = [self._sort]

        return request

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Returns:
            int: The number of results from the run of this query.
        """
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

    def _perform_query(self, from_row=0, max_rows=0):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): The row to start the query at (default 0).
            max_rows (int): The maximum number of rows to be returned (default 0, meaning "all").

        Returns:
            Iterable: The iterated query.
        """
        url = self._doc_class.urlobject_history.format(
            self._cb.credentials.org_key
        )
        current = from_row
        numrows = 0
        still_querying = True
        while still_querying:
            request = self._build_request(from_row, max_rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, item)
                current += 1
                numrows += 1

                if max_rows and numrows == max_rows:
                    still_querying = False
                    break

            from_row = current
            if current >= self._total_results:
                still_querying = False
                break

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query. Must be implemented in any inheriting classes.

        Args:
            context (object): The context returned by _init_async_query. May be None.

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        url = self._doc_class.urlobject_history.format(self._cb.credentials.org_key)
        self._total_results = 0
        self._count_valid = False
        output = []
        while not self._count_valid or len(output) < self._total_results:
            request = self._build_request(len(output), -1)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            if not self._count_valid:
                self._total_results = result["num_found"]
                self._count_valid = True

            results = result.get("results", [])
            output += [self._doc_class(self._cb, item) for item in results]
        return output


class ResultQuery(BaseQuery, QueryBuilderSupportMixin, IterableQueryMixin, CriteriaBuilderSupportMixin,
                  AsyncQueryMixin):
    """Represents a query that retrieves results from a LiveQuery run."""
    def __init__(self, doc_class, cb):
        """
        Initialize the ResultQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(ResultQuery, self).__init__()

        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._sort = {}
        self._batch_size = 100
        self._run_id = None
        self.num_remaining = None
        self._search_after = None

    def set_device_ids(self, device_ids):
        """
        Sets the device.id criteria filter.

        Arguments:
            device_ids ([int]): Device IDs to filter on.

        Returns:
            ResultQuery: The ResultQuery with specified device.id.
        """
        if not all(isinstance(device_id, int) for device_id in device_ids):
            raise ApiError("One or more invalid device IDs")
        self._update_criteria("device.id", device_ids)
        return self

    def set_device_names(self, device_names):
        """
        Sets the device.name criteria filter.

        Arguments:
            device_names ([str]): Device names to filter on.

        Returns:
            ResultQuery: The ResultQuery with specified device.name.
        """
        if not all(isinstance(name, str) for name in device_names):
            raise ApiError("One or more invalid device names")
        self._update_criteria("device.name", device_names)
        return self

    def set_device_os(self, device_os):
        """
        Sets the device.os criteria.

        Arguments:
            device_os ([str]): Device OS's to filter on.

        Returns:
            ResultQuery: The ResultQuery object with specified device_os.

        Note:
            Device OS's can be one or more of ["WINDOWS", "MAC", "LINUX"].
        """
        if not all(isinstance(os, str) for os in device_os):
            raise ApiError("device_type must be a list of strings, including"
                           " 'WINDOWS', 'MAC', and/or 'LINUX'")
        self._update_criteria("device.os", device_os)
        return self

    def set_policy_ids(self, policy_ids):
        """
        Sets the device.policy_id criteria.

        Arguments:
            policy_ids ([int]): Device policy ID's to filter on.

        Returns:
            ResultQuery: The ResultQuery object with specified policy_ids.
        """
        if not all(isinstance(id, int) for id in policy_ids):
            raise ApiError("policy_ids must be a list of integers.")
        self._update_criteria("device.policy_id", policy_ids)
        return self

    def set_policy_names(self, policy_names):
        """
        Sets the device.policy_name criteria.

        Arguments:
            policy_names ([str]): Device policy names to filter on.

        Returns:
            ResultQuery: The ResultQuery object with specified policy_names.
        """
        if not all(isinstance(name, str) for name in policy_names):
            raise ApiError("policy_names must be a list of strings.")
        self._update_criteria("device.policy_name", policy_names)
        return self

    def set_statuses(self, statuses):
        """
        Sets the status criteria.

        Arguments:
            statuses ([str]): Query statuses to filter on.

        Returns:
            ResultQuery: The ResultQuery object with specified statuses.
        """
        if not all(isinstance(status, str) for status in statuses):
            raise ApiError("statuses must be a list of strings.")
        self._update_criteria("status", statuses)
        return self

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Arguments:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            ResultQuery: ResultQuery object with specified sorting key and order.

        Example:
            >>> cb.select(Result).run_id(my_run).where(username="foobar").sort_by("uid")
        """
        self._sort.update({"field": key, "order": direction})
        return self

    def run_id(self, run_id):
        """
        Sets the run ID to query results for.

        Arguments:
            run_id (str): The run ID to retrieve results for.

        Returns:
            ResultQuery: ResultQuery object with specified run_id.

        Example:
            >>> cb.select(Result).run_id(my_run)
        """
        self._run_id = run_id
        return self

    def set_run_ids(self, run_ids):
        """
        Sets the run IDs to query results for.

        Note:
            Only supported for scroll

        Arguments:
            run_ids (list[str]): The run IDs to retrieve results for.

        Returns:
            ResultQuery: ResultQuery object with specified run_id.
        """
        self._criteria["run_id"] = run_ids
        return self

    def set_time_received(self, start=None, end=None, range=None):
        """
        Set the time received to query results for.

        Note: If you are using scroll you may only specify range, or start and end. range supports max of 24hrs

        Args:
            start(str): Start time in ISO8601 UTC format
            end(str): End time in ISO8601 UTC format
            range(str): Relative time window using the following allowed time units y years, w weeks, d days, h hours,
                m minutes, s seconds

        Returns:
            ResultQuery: ResultQuery object with specified time_received.
        """
        if (start or end) and range:
            raise ApiError("You cannot specify both a fixed start/end timestamp and a range")

        self._criteria["time_received"] = {}

        if range:
            self._criteria["time_received"]["range"] = range
        else:
            self._criteria["time_received"]["start"] = start
            self._criteria["time_received"]["end"] = end

        return self

    def _build_request(self, start, rows):
        """
        Creates the request body for an API call.

        Args:
            start (int): The row to start the query at.
            rows (int): The maximum number of rows to be returned.

        Returns:
            dict: The complete request body.
        """
        request = {"start": start}
        query = self._query_builder._collapse()
        if query:
            request["query"] = query
        if rows != 0:
            request["rows"] = rows
        if self._criteria:
            request["criteria"] = self._criteria
        if self._sort:
            request["sort"] = [self._sort]

        return request

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Returns:
            int: The number of results from the run of this query.
        """
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

    def _perform_query(self, from_row=0, max_rows=0):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): The row to start the query at (default 0).
            max_rows (int): The maximum number of rows to be returned (default 0, meaning "all").

        Returns:
            Iterable: The iterated query.
        """
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")

        url = self._doc_class.urlobject.format(
            self._cb.credentials.org_key, self._run_id
        )
        current = from_row
        numrows = 0
        still_querying = True
        while still_querying:
            request = self._build_request(from_row, max_rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]
            if self._total_results > MAX_RESULTS_LIMIT:
                self._total_results = MAX_RESULTS_LIMIT
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, item)
                current += 1
                numrows += 1

                if max_rows and numrows == max_rows:
                    still_querying = False
                    break

            from_row = current
            if current >= self._total_results:
                still_querying = False
                break

    def scroll(self, rows=10000):
        """
        Iteratively fetch results across Live Query Runs or paginate all results beyond the 10k search limits.

        To fetch the next set of results repeatively call the scroll function until
        `ResultQuery.num_remaining == 0` or no results are returned.

        Note: You must specify either a set_time_received or a set_run_ids on the query before using scroll

        Args:
            rows (int): The number of rows to fetch

        Returns:
            list[Result]: The list of results
        """
        if self.num_remaining == 0:
            return []
        elif rows > 10000:
            rows = 10000

        url = f"/livequery/v1/orgs/{self._cb.credentials.org_key}/runs/results/_scroll"

        # Sort by time_received enforced
        self._sort = {}

        request = self._build_request(0, rows)
        del request["start"]

        if self._search_after is not None:
            request["search_after"] = self._search_after

        resp = self._cb.post_object(url, body=request)
        resp_json = resp.json()

        # Capture latest state
        self.num_remaining = resp_json["num_remaining"]
        self._search_after = resp_json["search_after"]

        results = []
        for item in resp_json["results"]:
            results.append(self._doc_class(self._cb, item))

        return results

    def _init_async_query(self):
        """
        Initialize an async query and return a context for running in the background. Optional.

        Returns:
            str: Context for running in the background.
        """
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")
        return self._run_id

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query. Must be implemented in any inheriting classes.

        Args:
            context (object): The context returned by _init_async_query. May be None.

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key, context)
        self._total_results = 0
        self._count_valid = False
        output = []
        while not self._count_valid or len(output) < self._total_results:
            request = self._build_request(len(output), -1)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            if not self._count_valid:
                self._total_results = min(result["num_found"], MAX_RESULTS_LIMIT)
                self._count_valid = True

            results = result.get("results", [])
            output += [self._doc_class(self._cb, item) for item in results]
        return output

    def export_csv_as_stream(self, output, compressed=False):
        """
        Export the results from the run as CSV, writing the CSV to the given stream.

        Required Permissions:
            livequery.manage(READ)

        Args:
            output (RawIOBase): Stream to write the CSV data from the request to.
            compressed (bool): True to download as a compressed ZIP file, False to download as CSV.
        """
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key, self._run_id) + '?format=csv'
        if compressed:
            url += '&download=true'
        request = self._build_request(0, -1)
        self._cb.api_request_stream('POST', url, output, data=request,
                                    headers={'Accept': 'application/octet-stream' if compressed else 'text/csv'})

    def export_csv_as_string(self):
        """
        Export the results from the run as CSV, returning the CSV data as a string.

        Required Permissions:
            livequery.manage(READ)

        Returns:
            str: The CSV data as one big string.
        """
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")
        with io.BytesIO() as buffer:
            self.export_csv_as_stream(buffer)
            return str(buffer.getvalue(), 'utf-8')

    def export_csv_as_file(self, filename):
        """
        Export the results from the run as CSV, writing the CSV to the named file.

        Required Permissions:
            livequery.manage(READ)

        Args:
            filename (str): Name of the file to write the results to.
        """
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")
        with io.open(filename, 'wb') as file:
            self.export_csv_as_stream(file)

    def export_csv_as_lines(self):
        """
        Export the results from the run as CSV, returning the CSV data as iterated lines.

        Required Permissions:
            livequery.manage(READ)

        Returns:
            iterable: An iterable that can be used to get each line of CSV text in turn as a string.
        """
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key, self._run_id) + '?format=csv'
        request = self._build_request(0, -1)
        yield from self._cb.api_request_iterate('POST', url, data=request, headers={'Accept': 'text/csv'})

    def export_zipped_csv(self, filename):
        """
        Export the results from the run as a zipped CSV, writing the zip data to the named file.

        Required Permissions:
            livequery.manage(READ)

        Args:
            filename (str): Name of the file to write the results to.
        """
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")
        with io.open(filename, 'wb') as file:
            self.export_csv_as_stream(file, True)

    def async_export(self):
        """
        Create an asynchronous job that exports the results from the run.

        This is recommended if you are expecting a very large result set.  Once the Job is created, wait for it to be
        completed, then get the results from the Job using one of the get_output methods on the
        :py:meth:`cbc_sdk.platform.jobs` object. To wait asynchronously for the results, use the Job object's
        await_completion() method.

        Required Permissions:
            livequery.manage(READ), jobs.status(READ)

        Returns:
            Job: The Job object that represents the asynchronous job.
        """
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key, self._run_id) + '?format=csv&async=true'
        request = self._build_request(0, -1)
        response = self._cb.post_object(url, request)
        ref_url = response.json().get('ref_url', None)
        try:
            job_id = int(ref_url.rsplit('/', 1)[1]) if ref_url else -1
        except ValueError:
            job_id = -1
        if job_id < 0:
            raise ApiError(f"server sent back invalid job reference URL {ref_url}")
        return Job(self._cb, job_id)


class FacetQuery(BaseQuery, QueryBuilderSupportMixin, IterableQueryMixin, CriteriaBuilderSupportMixin, AsyncQueryMixin):
    """Represents a query that receives facet information from a LiveQuery run."""
    def __init__(self, doc_class, cb):
        """
        Initialize the FacetQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(FacetQuery, self).__init__()

        self._query_builder = QueryBuilder()
        self._facet_fields = []
        self._criteria = {}
        self._run_id = None

    def facet_field(self, field):
        """
        Sets the facet fields to be received by this query.

        Arguments:
            field (str or [str]): Field(s) to be received.

        Returns:
            FacetQuery: FacetQuery that will receive field(s) facet_field.

        Example:
            >>> cb.select(ResultFacet).run_id(my_run).facet_field(["device.policy_name", "device.os"])
        """
        if isinstance(field, str):
            self._facet_fields.append(field)
        else:
            for name in field:
                self._facet_fields.append(name)
        return self

    def set_device_ids(self, device_ids):
        """
        Sets the device.id criteria filter.

        Arguments:
            device_ids ([int]): Device IDs to filter on.

        Returns:
            FacetQuery: The FacetQuery with specified device.id.
        """
        if not all(isinstance(device_id, int) for device_id in device_ids):
            raise ApiError("One or more invalid device IDs")
        self._update_criteria("device.id", device_ids)
        return self

    def set_device_names(self, device_names):
        """
        Sets the device.name criteria filter.

        Arguments:
            device_names ([str]): Device names to filter on.

        Returns:
            FacetQuery: The FacetQuery with specified device.name.
        """
        if not all(isinstance(name, str) for name in device_names):
            raise ApiError("One or more invalid device names")
        self._update_criteria("device.name", device_names)
        return self

    def set_device_os(self, device_os):
        """
        Sets the device.os criteria.

        Arguments:
            device_os ([str]): Device OS's to filter on.

        Returns:
            FacetQuery: The FacetQuery object with specified device_os.

        Note:
            Device OS's can be one or more of ["WINDOWS", "MAC", "LINUX"].
        """
        if not all(isinstance(os, str) for os in device_os):
            raise ApiError("device_type must be a list of strings, including"
                           " 'WINDOWS', 'MAC', and/or 'LINUX'")
        self._update_criteria("device.os", device_os)
        return self

    def set_policy_ids(self, policy_ids):
        """
        Sets the device.policy_id criteria.

        Arguments:
            policy_ids ([int]): Device policy ID's to filter on.

        Returns:
            FacetQuery: The FacetQuery object with specified policy_ids.
        """
        if not all(isinstance(id, int) for id in policy_ids):
            raise ApiError("policy_ids must be a list of integers.")
        self._update_criteria("device.policy_id", policy_ids)
        return self

    def set_policy_names(self, policy_names):
        """
        Sets the device.policy_name criteria.

        Arguments:
            policy_names ([str]): Device policy names to filter on.

        Returns:
            FacetQuery: The FacetQuery object with specified policy_names.
        """
        if not all(isinstance(name, str) for name in policy_names):
            raise ApiError("policy_names must be a list of strings.")
        self._update_criteria("device.policy_name", policy_names)
        return self

    def set_statuses(self, statuses):
        """
        Sets the status criteria.

        Arguments:
            statuses ([str]): Query statuses to filter on.

        Returns:
            FacetQuery: The FacetQuery object with specified statuses.
        """
        if not all(isinstance(status, str) for status in statuses):
            raise ApiError("statuses must be a list of strings.")
        self._update_criteria("status", statuses)
        return self

    def run_id(self, run_id):
        """
        Sets the run ID to query results for.

        Arguments:
            run_id (str): The run ID to retrieve results for.

        Returns:
            FacetQuery: FacetQuery object with specified run_id.

        Example:
            >>> cb.select(ResultFacet).run_id(my_run)
        """
        self._run_id = run_id
        return self

    def _build_request(self, rows):
        """
        Creates the request body for an API call.

        Args:
            rows (int): The maximum number of rows to be returned.

        Returns:
            dict: The complete request body.
        """
        terms = {"fields": self._facet_fields}
        if rows != 0:
            terms["rows"] = rows
        request = {"terms": terms}
        query = self._query_builder._collapse()
        if query:
            request["query"] = query
        if self._criteria:
            request["criteria"] = self._criteria
        return request

    def _perform_query(self, from_row=0, max_rows=0):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): Not used, inserted for compatibility.
            max_rows (int): The maximum number of rows to be returned (default 0, meaning "all").

        Returns:
            Iterable: The iterated query.
        """
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")

        url = self._doc_class.urlobject.format(
            self._cb.credentials.org_key, self._run_id
        )
        request = self._build_request(max_rows)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        results = result.get("terms", [])
        for item in results:
            yield self._doc_class(self._cb, item)

    def _init_async_query(self):
        """
        Initialize an async query and return a context for running in the background. Optional.

        Returns:
            str: Context for running in the background.
        """
        if self._run_id is None:
            raise ApiError("Can't retrieve results without a run ID")
        return self._run_id

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query. Must be implemented in any inheriting classes.

        Args:
            context (object): The context returned by _init_async_query. May be None.

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key, context)
        request = self._build_request(0)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        results = result.get("terms", [])
        return [self._doc_class(self._cb, item) for item in results]


class TemplateHistoryQuery(BaseQuery, QueryBuilderSupportMixin, IterableQueryMixin, CriteriaBuilderSupportMixin,
                           AsyncQueryMixin):
    """Represents a query that retrieves historic LiveQuery templates."""
    def __init__(self, doc_class, cb):
        """
        Initialize the TemplateHistoryQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(TemplateHistoryQuery, self).__init__()
        self._query_builder = QueryBuilder()
        self._sort = {}
        self._criteria = {}

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Arguments:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            TemplateHistoryQuery: object with specified sorting key and order.

        Example:

        >>> cb.select(Result).run_id(my_run).where(username="foobar").sort_by("uid")
        """
        self._sort.update({"field": key, "order": direction})
        return self

    def _build_request(self, start, rows):
        """
        Creates the request body for an API call.

        Args:
            start (int): The row to start the query at.
            rows (int): The maximum number of rows to be returned.

        Returns:
            dict: The complete request body.
        """
        request = {"start": start}

        if self._query_builder:
            request["query"] = self._query_builder._collapse()
        if rows != 0:
            request["rows"] = rows
        if self._criteria:
            request["criteria"] = self._criteria
        if self._sort:
            request["sort"] = [self._sort]

        return request

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Returns:
            int: The number of results from the run of this query.
        """
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

    def _perform_query(self, from_row=0, max_rows=0):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): The row to start the query at (default 0).
            max_rows (int): The maximum number of rows to be returned (default 0, meaning "all").

        Returns:
            Iterable: The iterated query.
        """
        url = self._doc_class.urlobject_history.format(
            self._cb.credentials.org_key
        )
        current = from_row
        numrows = 0
        still_querying = True
        while still_querying:
            request = self._build_request(from_row, max_rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, item)
                current += 1
                numrows += 1

                if max_rows and numrows == max_rows:
                    still_querying = False
                    break

            from_row = current
            if current >= self._total_results:
                still_querying = False
                break

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query. Must be implemented in any inheriting classes.

        Args:
            context (object): The context returned by _init_async_query. May be None.

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        url = self._doc_class.urlobject_history.format(
            self._cb.credentials.org_key
        )
        self._total_results = 0
        self._count_valid = False
        output = []
        while not self._count_valid or len(output) < self._total_results:
            request = self._build_request(len(output), -1)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            if not self._count_valid:
                self._total_results = result["num_found"]
                self._count_valid = True

            results = result.get("results", [])
            output += [self._doc_class(self._cb, item) for item in results]
        return output
