#!/usr/bin/env python3

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

"""Model and Query Classes for Platform Auditing"""

import datetime
from cbc_sdk.base import (UnrefreshableModel, BaseQuery, QueryBuilder, QueryBuilderSupportMixin,
                          CriteriaBuilderSupportMixin, ExclusionBuilderSupportMixin, IterableQueryMixin,
                          AsyncQueryMixin)
from cbc_sdk.errors import ApiError

from backports._datetime_fromisoformat import datetime_fromisoformat

"""Model Class"""


class AuditLogRecord(UnrefreshableModel):
    """Model class which represents audit log events. Mostly for future implementation."""
    urlobject = "/audit_log/v1/orgs/{0}/logs"
    swagger_meta_file = "platform/models/audit_log_record.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Creates a new ``AuditLogRecord``.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (int): Not used.
            initial_data (dict): Initial data to fill in the audit log record details.
        """
        super(AuditLogRecord, self).__init__(cb, model_unique_id, initial_data, force_init=False, full_doc=True)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the ``AuditLogRecord`` type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.
        """
        return AuditLogRecordQuery(cls, cb)

    @staticmethod
    def get_auditlogs(cb):
        """
        Retrieve queued audit logs from the Carbon Black Cloud server.

        Required Permissions:
            org.audits (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.

        Returns:
            list[dict]: List of dictionary objects representing the audit logs, or an empty list if none available.
        """
        res = cb.get_object("/integrationServices/v3/auditlogs")
        return res.get("notifications", [])


"""Query Class"""


class AuditLogRecordQuery(BaseQuery, QueryBuilderSupportMixin, CriteriaBuilderSupportMixin,
                          ExclusionBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin):
    """
    Query object that is used to locate ``AuditLogRecord`` objects.

    The ``AuditLogRecordQuery`` is constructed via SDK functions like the ``select()`` method on ``CBCloudAPI``.
    The user would then add a query and/or criteria to it before iterating over the results.

    The following criteria may be added to the query via the standard ``add_criteria()`` method, or added to query
    exclusions via the standard ``add_exclusions()`` method:

    * ``actor_ip`` - IP address of the entity that caused the creation of this audit log.
    * ``actor`` - Name of the entity that caused the creation of this audit log.
    * ``request_url`` - URL of the request that caused the creation of this audit log.
    * ``description`` - Text description of this audit log.
    """

    def __init__(self, doc_class, cb):
        """
        Initialize the ``AuditLogRecordQuery``.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(AuditLogRecordQuery, self).__init__()

        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._exclusions = {}
        self._sortcriteria = {}
        self._search_after = None
        self.num_remaining = None
        self.num_found = None
        self.max_rows = -1

    @staticmethod
    def _create_valid_time_filter(kwargs):
        """
        Verifies that an alert criteria key has the timerange functionality

        Args:
            kwargs (dict): Used to specify start= for start time, end= for end time, and range= for range. Values are
                either timestamp ISO 8601 strings or datetime objects for start and end time. For range, the time range
                to execute the result search, ending on the current time. Should be in the form "-2w",
                where y=year, w=week, d=day, h=hour, m=minute, s=second.

        Returns:
            dict: A new filter object.

        Raises:
            ApiError: If the argument format is incorrect.
        """
        time_filter = {}
        if kwargs.get("start", None) and kwargs.get("end", None):
            if kwargs.get("range", None):
                raise ApiError("cannot specify range= in addition to start= and end=")
            stime = kwargs["start"]
            etime = kwargs["end"]
            try:
                if isinstance(stime, str):
                    stime = datetime_fromisoformat(stime)
                if isinstance(etime, str):
                    etime = datetime_fromisoformat(etime)
                if isinstance(stime, datetime.datetime) and isinstance(etime, datetime.datetime):
                    time_filter = {"start": stime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                   "end": etime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}
            except:
                raise ApiError(f"Start and end time must be a string in ISO 8601 format or an object of datetime. "
                               f"Start time {stime} is a {type(stime)}. End time {etime} is a {type(etime)}.")
        elif kwargs.get("range", None):
            if kwargs.get("start", None) or kwargs.get("end", None):
                raise ApiError("cannot specify start= or end= in addition to range=")
            time_filter = {"range": kwargs["range"]}
        else:
            raise ApiError("must specify either start= and end= or range=")
        return time_filter

    def add_time_criteria(self, **kwargs):
        """
        Adds a ``create_time`` criteria value to either criteria or exclusions.

        Args:
            kwargs (dict): Keyword arguments to this method.

        Keyword Args:
            start (str/datetime): Starting time for the time interval to include in the criteria. Must be either a
                ``datetime`` object or a string in ISO 8601 format.  Both ``start`` and ``end`` must be specified
                if they are to be used.
            end (str/datetime): Ending time for the time interval to include in the criteria. Must be either a
                ``datetime`` object or a string in ISO 8601 format.  Both ``start`` and ``end`` must be specified
                if they are to be used.
            range (str): Range for the time interval, to be measured backwards from the current time.  Cannot
                be specified if ``start`` or ``end`` are specified.  Must be in the format "-NX", where ``N`` is an
                integer value, and ``X`` is a single character specifying the time unit: "y" for years, "w" for weeks,
                "d" for days, "h" for hours, "m" for minutes, or "s" for seconds.
            exclude (bool): ``True`` if this value is to be applied to exclusions, ``False`` if this value is to be
                applied to search criteria.  Default ``False.``

        Returns:
            AuditLogRecordQuery: This instance.

        Raises:
            ApiError: If the argument format is incorrect.
        """
        if kwargs.get("exclude", False):
            self._exclusions['create_time'] = self._create_valid_time_filter(kwargs)
        else:
            self._criteria['create_time'] = self._create_valid_time_filter(kwargs)
        return self

    def add_boolean_criteria(self, criteria_name, value, exclude=False):
        """
        Adds a Boolean value to either the criteria or exclusions.

        Args:
            criteria_name (str): The criteria name to set. May be either "flagged" (to set whether or not the audit
                record has been flagged) or "verbose" (so set whether or not the audit record has been marked verbose).
            value (bool): The value of the criteria to be set.
            exclude (bool): ``True`` if this value is to be applied to exclusions, ``False`` if this value is to be
                applied to search criteria.  Default ``False.``

        Returns:
            AuditLogRecordQuery: This instance.
        """
        if exclude:
            self._exclusions[criteria_name] = value
        else:
            self._criteria[criteria_name] = value
        return self

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Example:
            >>> cb.select(AuditLogRecord).sort_by("name")

        Args:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            AuditLogRecordQuery: This instance.
        """
        if direction not in CriteriaBuilderSupportMixin.VALID_DIRECTIONS:
            raise ApiError("invalid sort direction specified")
        self._sortcriteria = {"field": key, "order": direction}
        return self

    def _build_request(self, from_row, max_rows):
        """
        Creates the request body for an API call.

        Args:
            from_row (int): The row to start the query at.
            max_rows (int): The maximum number of rows to be returned.

        Returns:
            dict: The complete request body.
        """
        request = {}
        if self._criteria:
            request['criteria'] = self._criteria
        if self._exclusions:
            request['exclusions'] = self._exclusions
        query = self._query_builder._collapse()
        if query:
            request['query'] = query
        if max_rows > 0:
            request['rows'] = max_rows
        if from_row > 0:
            request['start'] = from_row
        if self._sortcriteria:
            request['sort'] = [self._sortcriteria]
        return request

    def _build_url(self, tail_end):
        """
        Creates the URL to be used for an API call.

        Args:
            tail_end (str): String to be appended to the end of the generated URL.

        Returns:
            str: The complete URL.
        """
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key) + tail_end
        return url

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Returns:
            int: The number of results from the run of this query.
        """
        if self._count_valid:
            return self._total_results

        url = self._build_url("/_search")
        request = self._build_request(0, -1)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()

        self._total_results = result["num_found"]
        self._count_valid = True

        return self._total_results

    def _perform_query(self, from_row=0, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): The row to start the query at (default 0).
            max_rows (int): The maximum number of rows to be returned (default -1, meaning "all").

        Yields:
            AuditLogRecord: The audit log records resulting from the search.
        """
        url = self._build_url("/_search")
        current = from_row
        numrows = 0
        still_querying = True
        while still_querying:
            request = self._build_request(current, max_rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, 0, item)
                current += 1
                numrows += 1

                if max_rows > 0 and numrows == max_rows:
                    still_querying = False
                    break

            from_row = current
            if current >= self._total_results:
                still_querying = False
                break

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Args:
            context (object): Not used.

        Returns:
            list[AuditLogRecord]: The results of the query.
        """
        url = self._build_url("/_search")
        request = self._build_request(0, -1)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        results = result.get("results", [])
        return [self._doc_class(self._cb, 0, item) for item in results]
