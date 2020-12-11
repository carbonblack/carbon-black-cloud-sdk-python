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

"""Model Classes for Enterprise Endpoint Detection and Response"""

from __future__ import absolute_import
from cbc_sdk.base import (PaginatedQuery,
                          QueryBuilder,
                          QueryBuilderSupportMixin,
                          IterableQueryMixin,
                          AsyncQueryMixin)
from cbc_sdk.errors import ApiError

import logging

log = logging.getLogger(__name__)


"""Queries"""


class Query(PaginatedQuery, QueryBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin):
    """Represents a prepared query to the Cb Enterprise EDR backend.

    This object is returned as part of a `CbEnterpriseEDRAPI.select`
    operation on models requested from the Cb Enterprise EDR backend. You should not have to create this class yourself.

    The query is not executed on the server until it's accessed, either as an iterator (where it will generate values
    on demand as they're requested) or as a list (where it will retrieve the entire result set and save to a list).
    You can also call the Python built-in ``len()`` on this object to retrieve the total number of items matching
    the query.

    Examples::

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.enterprise_edr import Report
    >>> cb = CBCloudAPI()
    >>> query = cb.select(Report)
    >>> query = query.where(report_id="ABCDEFG1234")
    >>> # alternatively:
    >>> query = query.where("report_id:ABCDEFG1234")

    Notes:
        - The slicing operator only supports start and end parameters, but not step. ``[1:-1]`` is legal, but
          ``[1:2:-1]`` is not.
        - You can chain where clauses together to create AND queries; only objects that match all ``where`` clauses
          will be returned.
    """

    def __init__(self, doc_class, cb):
        """
        Initialize the Query object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(Query, self).__init__(doc_class, cb, None)

        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._exclusions = {}
        self._sort_by = []
        self._group_by = None
        self._batch_size = 500
        self._start = 0
        self._time_range = {}
        self._fields = ["*"]
        self._default_args = {}

    def add_criteria(self, key, newlist):
        """Add to the criteria on this query with a custom criteria key.

        Args:
            key (str): The key for the criteria item to be set.
            newlist (str or list[str]): Value or list of values to be set for the criteria item.

        Returns:
            The ResultQuery with specified custom criteria.

        Example:
            query = api.select(Event).add_criteria("event_type", ["filemod", "scriptload"])
            query = api.select(Event).add_criteria("event_type", "filemod")
        """
        if not isinstance(newlist, list):
            if not isinstance(newlist, str):
                raise ApiError("Criteria value(s) must be a string or list of strings. "
                               f"{newlist} is a {type(newlist)}.")
            self._add_criteria(key, [newlist])
        else:
            self._add_criteria(key, newlist)
        return self

    def _add_criteria(self, key, newlist):
        """
        Updates a list of criteria being collected for a query, by setting or appending items.

        Args:
            key (str): The key for the criteria item to be set.
            newlist (list): List of values to be set for the criteria item.
        """
        oldlist = self._criteria.get(key, [])
        self._criteria[key] = oldlist + newlist

    def add_exclusions(self, key, newlist):
        """Add to the excluions on this query with a custom exclusion key.

        Args:
            key (str): The key for the exclusion item to be set.
            newlist (str or list[str]): Value or list of values to be set for the exclusion item.

        Returns:
            The ResultQuery with specified custom exclusion.

        Example:
            query = api.select(Event).add_exclusions("netconn_domain", ["www.google.com"])
            query = api.select(Event).add_exclusions("netconn_domain", "www.google.com")
        """
        if not isinstance(newlist, list):
            if not isinstance(newlist, str):
                raise ApiError("Exclusion value(s) must be a string or list of strings. "
                               f"{newlist} is a {type(newlist)}.")
            self._add_exclusions(key, [newlist])
        else:
            self._add_exclusions(key, newlist)
        return self

    def _add_exclusions(self, key, newlist):
        """
        Updates a list of exclusion being collected for a query, by setting or appending items.

        Args:
            key (str): The key for the exclusion item to be set.
            newlist (list): List of values to be set for the exclusion item.
        """
        oldlist = self._exclusions.get(key, [])
        self._exclusions[key] = oldlist + newlist

    def set_fields(self, fields):
        """
        Sets the fields to be returned with the response.

        Args:
            fields (str or list[str]): Field or list of fields to be returned.
        """
        if not isinstance(fields, list):
            if not isinstance(fields, str):
                raise ApiError(f"Fields must be a string or list of strings. {fields} is a {type(fields)}.")
            self._fields = [fields]
        else:
            self._fields = fields
        self._default_args["fields"] = self._fields
        return self

    def set_start(self, start):
        """
        Sets the 'start' query body parameter, determining where to begin retrieving results from.

        Args:
            start (int): Where to start results from.
        """
        if not isinstance(start, int):
            raise ApiError(f"Start must be an integer. {start} is a {type(start)}.")
        self._start = start
        self._default_args["start"] = self._start
        return self

    def set_rows(self, rows):
        """
        Sets the 'rows' query body parameter, determining how many rows of results to request.

        Args:
            rows (int): How many rows to request.
        """
        if not isinstance(rows, int):
            raise ApiError(f"Rows must be an integer. {rows} is a {type(rows)}.")
        self._batch_size = rows
        self._default_args["rows"] = self._batch_size
        return self

    def set_time_range(self, start=None, end=None, window=None):
        """
        Sets the 'time_range' query body parameter, determining a time window based on 'device_timestamp'.

        Args:
            start (str in ISO 8601 timestamp): When to start the result search.
            end (str in ISO 8601 timestamp): When to end the result search.
            window (str): Time window to execute the result search, ending on the current time.
                Should be in the form "-2w", where y=year, w=week, d=day, h=hour, m=minute, s=second.

        Note:
            - `window` will take precendent over `start` and `end` if provided.

        Examples:
            query = api.select(Event).set_time_range(start="2020-10-20T20:34:07Z")
            second_query = api.select(Event).set_time_range(start="2020-10-20T20:34:07Z", end="2020-10-30T20:34:07Z")
            third_query = api.select(Event).set_time_range(window='-3d')
        """
        if start:
            if not isinstance(start, str):
                raise ApiError(f"Start time must be a string in ISO 8601 format. {start} is a {type(start)}.")
            self._time_range["start"] = start
        if end:
            if not isinstance(end, str):
                raise ApiError(f"End time must be a string in ISO 8601 format. {end} is a {type(end)}.")
            self._time_range["end"] = end
        if window:
            if not isinstance(window, str):
                raise ApiError(f"Window must be a string. {window} is a {type(window)}.")
            self._time_range["window"] = window
        return self

    def _get_query_parameters(self):
        args = self._default_args.copy()
        if self._criteria:
            args["criteria"] = self._criteria
        if self._exclusions:
            args["exclusions"] = self._exclusions
        if self._time_range:
            args["time_range"] = self._time_range
        args['query'] = self._query_builder._collapse()
        if self._query_builder._process_guid is not None:
            args["process_guid"] = self._query_builder._process_guid
        if 'process_guid:' in args['query']:
            q = args['query'].split('process_guid:', 1)[1].split(' ', 1)[0]
            args["process_guid"] = q
        return args

    def sort_by(self, key, direction="ASC"):
        """Sets the sorting behavior on a query's results.

        Arguments:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            Query: The query with sorting parameters.

        Example:

        >>> cb.select(Process).where(process_name="cmd.exe").sort_by("device_timestamp")
        """
        found = False

        for sort_item in self._sort_by:
            if sort_item['field'] == key:
                sort_item['order'] = direction
                found = True

        if not found:
            self._sort_by.append({'field': key, 'order': direction})

        self._default_args['sort'] = self._sort_by

        return self

    def _count(self):
        args = self._get_query_parameters()

        log.debug("args: {}".format(str(args)))

        result = self._cb.post_object(
            self._doc_class.urlobject.format(
                self._cb.credentials.org_key,
                args["process_guid"]
            ), body=args
        ).json()

        self._total_results = int(result.get('num_available', 0))
        self._count_valid = True

        return self._total_results

    def _validate(self, args):
        if not hasattr(self._doc_class, "validation_url"):
            return

        url = self._doc_class.validation_url.format(self._cb.credentials.org_key)

        if args.get('query', False):
            args['q'] = args['query']

        # v2 search sort key does not work with v1 validation
        args.pop('sort', None)

        validated = self._cb.get_object(url, query_parameters=args)

        if not validated.get("valid"):
            raise ApiError("Invalid query: {}: {}".format(args, validated["invalid_message"]))

    def _search(self, start=0, rows=0):
        """
        Execute the query, iterating over results 500 rows at a time.

        Args:
           start (int): What index to begin retrieving results from.
           rows (int): Total number of results to be retrieved.
                       If `start` is not specified, the default of 0 will be used.
                       If `rows` is not specified, the query will continue until all available results have
                       been retrieved, getting results in batches of 500.
        """
        raise NotImplementedError("_search() method must be implemented in subclass")

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Args:
            context (object): The context (always None in this case).

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        return list(self._search())
