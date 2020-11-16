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
from cbc_sdk.base import (UnrefreshableModel,
                          BaseQuery,
                          PaginatedQuery,
                          QueryBuilder,
                          QueryBuilderSupportMixin,
                          IterableQueryMixin,
                          AsyncQueryMixin)
from cbc_sdk.errors import ApiError, TimeoutError

import logging
import time

log = logging.getLogger(__name__)

"""Models"""


class Process(UnrefreshableModel):
    """Represents a process retrieved by one of the Enterprise EDR endpoints."""
    default_sort = 'last_update desc'
    primary_key = "process_guid"
    validation_url = "/api/investigate/v1/orgs/{}/processes/search_validation"

    class Summary(UnrefreshableModel):
        """Represents a summary of organization-specific information for a process."""
        default_sort = "last_update desc"
        primary_key = "process_guid"
        urlobject = "/api/investigate/v1/orgs/{}/processes/summary"

        def __init__(self, cb, model_unique_id):
            url = self.urlobject.format(cb.credentials.org_key)

            summary = cb.get_object(url, query_parameters={"process_guid": model_unique_id})

            super(Process.Summary, self).__init__(cb, model_unique_id=model_unique_id,
                                                  initial_data=summary, force_init=False,
                                                  full_doc=True)

        @classmethod
        def _query_implementation(self, cb, **kwargs):
            return Query(self, cb, **kwargs)

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        # This will emulate a synchronous process query, for now.
        return AsyncProcessQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=True):
        super(Process, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                      force_init=force_init, full_doc=full_doc)

    @property
    def summary(self):
        """Returns organization-specific information about this process."""
        return self._cb.select(Process.Summary, self.process_guid)

    def events(self, **kwargs):
        """Returns a query for events associated with this process's process GUID.

        Args:
            kwargs: Arguments to filter the event query with.

        Returns:
            query (cbc_sdk.enterprise_edr.Query): Query object with the appropriate
                search parameters for events

        Example:

        >>> [print(event) for event in process.events()]
        >>> [print(event) for event in process.events(event_type="modload")]
        """
        query = self._cb.select(Event).where(process_guid=self.process_guid)

        if kwargs:
            query = query.and_(**kwargs)

        return query

    def tree(self):
        """Returns a Process Tree associated with this process.

        Returns:
            Tree (cbc_sdk.enterprise_edr.Tree): Tree with children (and possibly siblings).

        Example:

        >>> tree = process.tree()
        """
        data = self._cb.select(Tree).where(process_guid=self.process_guid).all()
        return Tree(self._cb, initial_data=data)

    @property
    def parents(self):
        """Returns a parent process associated with this process.

        Returns:
            parent (Process): Parent Process if one exists, None if the process has no recorded parent.
        """
        if "parent_guid" in self._info:
            return self._cb.select(Process, self.parent_guid)
        elif self.summary.parent:
            return Process(self._cb, initial_data=self.summary.parent)
        else:
            return []

    @property
    def children(self):
        """Returns a list of child processes for this process.

        Returns:
            children ([Process]): List of Processes, one for each child of the
                parent Process.
        """
        if isinstance(self.summary.children, list):
            return [
                Process(self._cb, initial_data=child)
                for child in self.summary.children
            ]
        else:
            return []

    @property
    def siblings(self):
        """Returns a list of sibling processes for this process.

        Returns:
            siblings ([Process]): List of Processes, one for each sibling of the
                parent Process.
        """
        return [
            Process(self._cb, initial_data=sibling)
            for sibling in self.summary.siblings
        ]

    @property
    def process_md5(self):
        """Returns a string representation of the MD5 hash for this process.

        Returns:
            hash (str): MD5 hash of the process.
        """
        # NOTE: We have to check _info instead of poking the attribute directly
        # to avoid the missing attrbute login in NewBaseModel.
        if "process_hash" in self._info:
            return next((hsh for hsh in self.process_hash if len(hsh) == 32), None)
        elif "process_hash" in self.summary._info["process"]:
            return next((hash for hash in self.summary._info["process"]["process_hash"] if len(hash) == 32), None)
        else:
            return None

    @property
    def process_sha256(self):
        """Returns a string representation of the SHA256 hash for this process.

        Returns:
            hash (str): SHA256 hash of the process.
        """
        if "process_hash" in self._info:
            return next((hsh for hsh in self.process_hash if len(hsh) == 64), None)
        elif "process_hash" in self.summary._info["process"]:
            return next((hash for hash in self.summary._info["process"]["process_hash"] if len(hash) == 64), None)
        else:
            return None

    @property
    def process_pids(self):
        """Returns a list of PIDs associated with this process.

        Returns:
            pids ([int]): List of integer PIDs.
            None if there are no associated PIDs.
        """
        # NOTE(ww): This exists because the API returns the list as "process_pid",
        # which is misleading. We just give a slightly clearer name.
        if "process_pid" in self._info:
            return self.process_pid
        elif "process_pid" in self.summary._info["process"]:
            return self.summary._info["process"]["process_pid"]
        else:
            return None

    def facets(self):
        """Returns a FacetQuery for a Process.

        This represents the search for a summary of result groupings (facets).
        The returned AsyncFacetQuery object must have facet fields or ranges specified
        before it can be submitted, using the `add_facet_field()` or `add_range()` methods.
        """
        return self._cb.select(ProcessFacet).where(process_guid=self.process_guid)


class Event(UnrefreshableModel):
    """Events can be queried for via `CBCloudAPI.select` or an already selected process with `Process.events`."""
    urlobject = '/api/investigate/v2/orgs/{}/events/{}/_search'
    validation_url = '/api/investigate/v1/orgs/{}/events/search_validation'
    default_sort = 'last_update desc'
    primary_key = "process_guid"

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        return EventQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=True):
        super(Event, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                    force_init=force_init, full_doc=full_doc)


class Tree(UnrefreshableModel):
    """The preferred interface for interacting with Tree models is `Process.tree()`."""
    urlobject = '/api/investigate/v1/orgs/{}/processes/tree'
    primary_key = 'process_guid'

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        return TreeQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=True):
        super(Tree, self).__init__(
            cb, model_unique_id=model_unique_id, initial_data=initial_data,
            force_init=force_init, full_doc=full_doc
        )

    @property
    def children(self):
        """Returns all of the children of the process that this tree is centered around.

        Returns:
            children ([Process]): List of children for the Tree's parent process.
        """
        return [Process(self._cb, initial_data=child) for child in self.nodes["children"]]


class ProcessFacet(UnrefreshableModel):
    """Represents the results of an AsyncFacetQuery.

    ProcessFacet objects contain both Terms and Ranges. Each of those contain facet
    fields and values.

    Access all of the Terms facet data with ProcessFacet.terms_.facets or see just
    the field names with ProcessFacet.terms_.fields.

    Access all of the Ranges facet data with ProcessFacet.ranges_.facets or see just
    the field names with ProcessFacet.ranges_.fields.
    """
    primary_key = "job_id"
    swagger_meta_file = "enterprise_edr/models/process_facets.yaml"
    urlobject = "/api/investigate/v2/orgs/{}/processes/facet_jobs"

    class Terms(UnrefreshableModel):
        """Represents the facet fields and values associated with a Process Facet query."""
        def __init__(self, cb, initial_data):
            """Initialize a ProcessFacet Terms object with initial_data."""
            super(ProcessFacet.Terms, self).__init__(
                cb,
                model_unique_id=None,
                initial_data=initial_data,
                force_init=False,
                full_doc=True,
            )
            self._facets = {}
            for facet_term_data in initial_data:
                field = facet_term_data["field"]
                values = facet_term_data["values"]
                self._facets[field] = values

        @property
        def facets(self):
            """Returns the terms' facets for this result."""
            return self._facets

        @property
        def fields(self):
            """Returns the terms facets' fields for this result."""
            return [field for field in self._facets]

    class Ranges(UnrefreshableModel):
        """Represents the range (bucketed) facet fields and values associated with a Process Facet query."""
        def __init__(self, cb, initial_data):
            """Initialize a ProcessFacet Ranges object with initial_data."""
            super(ProcessFacet.Ranges, self).__init__(
                cb,
                model_unique_id=None,
                initial_data=initial_data,
                force_init=False,
                full_doc=True,
            )
            self._facets = {}
            for facet_range_data in initial_data:
                field = facet_range_data["field"]
                values = facet_range_data["values"]
                self._facets[field] = values

        @property
        def facets(self):
            """Returns the reified `ProcessFacet.Terms._facets` for this result."""
            return self._facets

        @property
        def fields(self):
            """Returns the ranges fields for this result."""
            return [field for field in self._facets]

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return AsyncFacetQuery(cls, cb)

    def __init__(self, cb, model_unique_id, initial_data):
        """Initialize a ResultFacet object with initial_data."""
        super(ProcessFacet, self).__init__(
            cb,
            model_unique_id=model_unique_id,
            initial_data=initial_data,
            force_init=False,
            full_doc=True
        )
        self._terms = ProcessFacet.Terms(cb, initial_data=initial_data["terms"])
        self._ranges = ProcessFacet.Ranges(cb, initial_data=initial_data["ranges"])

    @property
    def terms_(self):
        """Returns the reified `ProcessFacet.Terms` for this result."""
        return self._terms

    @property
    def ranges_(self):
        """Returns the reified `ProcessFacet.Ranges` for this result."""
        return self._ranges


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

    >>> from cbc_sdk.enterprise_edr import CBCloudAPI,Process
    >>> cb = CBCloudAPI()
    >>> query = cb.select(Process)
    >>> query = query.where(process_name="notepad.exe")
    >>> # alternatively:
    >>> query = query.where("process_name:notepad.exe")

    Notes:
        - The slicing operator only supports start and end parameters, but not step. ``[1:-1]`` is legal, but
          ``[1:2:-1]`` is not.
        - You can chain where clauses together to create AND queries; only objects that match all ``where`` clauses
          will be returned.
    """

    def __init__(self, doc_class, cb):
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


class AsyncProcessQuery(Query):
    """Represents the query logic for an asychronous Process query.

    This class specializes `Query` to handle the particulars of
    process querying.
    """
    def __init__(self, doc_class, cb):
        super(AsyncProcessQuery, self).__init__(doc_class, cb)
        self._query_token = None
        self._timeout = 0
        self._timed_out = False

    def timeout(self, msecs):
        """Sets the timeout on a process query.

        Arguments:
            msecs (int): Timeout duration, in milliseconds.

        Returns:
            Query (AsyncProcessQuery): The Query object with new milliseconds
                parameter.

        Example:

        >>> cb.select(Process).where(process_name="foo.exe").timeout(5000)
        """
        self._timeout = msecs
        return self

    def _submit(self):
        if self._query_token:
            raise ApiError("Query already submitted: token {0}".format(self._query_token))

        args = self._get_query_parameters()
        self._validate(args)

        url = "/api/investigate/v2/orgs/{}/processes/search_jobs".format(self._cb.credentials.org_key)
        query_start = self._cb.post_object(url, body=args)

        self._query_token = query_start.json().get("job_id")

        self._timed_out = False
        self._submit_time = time.time() * 1000

    def _still_querying(self):
        if not self._query_token:
            self._submit()

        status_url = "/api/investigate/v1/orgs/{}/processes/search_jobs/{}".format(
            self._cb.credentials.org_key,
            self._query_token,
        )
        result = self._cb.get_object(status_url)

        searchers_contacted = result.get("contacted", 0)
        searchers_completed = result.get("completed", 0)
        log.debug("contacted = {}, completed = {}".format(searchers_contacted, searchers_completed))
        if searchers_contacted == 0:
            return True
        if searchers_completed < searchers_contacted:
            if self._timeout != 0 and (time.time() * 1000) - self._submit_time > self._timeout:
                self._timed_out = True
                return False
            return True

        return False

    def _count(self):
        if self._count_valid:
            return self._total_results

        while self._still_querying():
            time.sleep(.5)

        if self._timed_out:
            raise TimeoutError(message="user-specified timeout exceeded while waiting for results")

        result_url = "/api/investigate/v2/orgs/{}/processes/search_jobs/{}/results".format(
            self._cb.credentials.org_key,
            self._query_token,
        )
        result = self._cb.get_object(result_url)

        self._total_results = result.get('num_available', 0)
        self._count_valid = True

        return self._total_results

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
        if not self._query_token:
            self._submit()

        while self._still_querying():
            time.sleep(.5)

        if self._timed_out:
            raise TimeoutError(message="user-specified timeout exceeded while waiting for results")

        log.debug("Pulling results, timed_out={}".format(self._timed_out))

        current = start
        rows_fetched = 0
        still_fetching = True
        result_url_template = "/api/investigate/v2/orgs/{}/processes/search_jobs/{}/results".format(
            self._cb.credentials.org_key,
            self._query_token
        )
        query_parameters = {}
        while still_fetching:
            result_url = '{}?start={}&rows={}'.format(
                result_url_template,
                current,
                10  # Batch gets to reduce API calls
            )

            result = self._cb.get_object(result_url, query_parameters=query_parameters)

            self._total_results = result.get('num_available', 0)
            self._count_valid = True

            results = result.get('results', [])

            for item in results:
                yield item
                current += 1
                rows_fetched += 1

                if rows and rows_fetched >= rows:
                    still_fetching = False
                    break

            if current >= self._total_results:
                still_fetching = False

            log.debug("current: {}, total_results: {}".format(current, self._total_results))

    def _init_async_query(self):
        """
        Initialize an async query and return a context for running in the background.

        Returns:
            object: Context for running in the background (the query token).
        """
        self._submit()
        return self._query_token

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Args:
            context (object): The context (query token) returned by _init_async_query.

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        if context != self._query_token:
            raise ApiError("Async query not properly started")
        return list(self._search())


class AsyncFacetQuery(Query):
    """Represents a prepared query for Process Facets."""
    def __init__(self, doc_class, cb):
        super(AsyncFacetQuery, self).__init__(doc_class, cb)
        self._query_token = None
        self._timeout = 0
        self._timed_out = False
        self._limit = None
        self._facet_fields = []
        self._ranges = []
        self._facet_rows = None

    def timeout(self, msecs):
        """Sets the timeout on an ProcessFacet query.

        Arguments:
            msecs (int): Timeout duration, in milliseconds.

        Returns:
            Query (AsyncFacetQuery): The Query object with new milliseconds
                parameter.

        Example:

        >>> cb.select(ProcessFacet).where(process_name="foo.exe").timeout(5000)
        """
        self._timeout = msecs
        return self

    def limit(self, limit):
        """Sets the maximum number of facets per category (i.e. any Process Search Fields in self._fields).

        The default limit for Process Facet searches in the Carbon Black Cloud backend is 100.

        Arguments:
            limit (int): Maximum number of facets per category.

        Returns:
            Query (AsyncFacetQuery): The Query object with new limit parameter.

        Example:
        >>> cb.select(ProcessFacet).where(process_name="foo.exe").limit(50)
        """
        self._limit = limit
        return self

    def set_rows(self, rows):
        """Sets the number of facet results to return with the query.

        Args:
            rows (int): Number of rows to return.

        Returns:
            Query (AsyncFacetQuery): The Query object with the new rows parameter.

        Example:
        >>> cb.select(ProcessFacet).set_rows(50)
        """
        self._facet_rows = rows
        return self

    def add_facet_field(self, field):
        """Sets the facet fields to be received by this query.

        Arguments:
            field (str or [str]): Field(s) to be received.

        Returns:
            Query (AsyncFacetQuery): The Query object that will receive the specified field(s).

        Example:
        >>> cb.select(ProcessFacet).add_facet_field(["process_name", "process_username"])
        """
        if isinstance(field, str):
            self._facet_fields.append(field)
        else:
            for name in field:
                self._facet_fields.append(name)
        return self

    def _check_range(self, range):
        """Checks if range has all required keys."""
        if "start" not in range.keys():
            raise ApiError("No 'start' parameter in range")
        if "end" not in range.keys():
            raise ApiError("No 'end' parameter in range")
        if "bucket_size" not in range.keys():
            raise ApiError("No 'bucket_size' parameter in range")
        if "field" not in range.keys():
            raise ApiError("No 'field' parameter in range")

        start = range["start"]
        end = range["end"]
        field = range["field"]
        bucket_size = range["bucket_size"]

        if not isinstance(start, int) and not isinstance(start, str):
            raise ApiError("start parameter should be either int or ISO8601 timestamp string")
        if not isinstance(end, int) and not isinstance(end, str):
            raise ApiError("end parameter should be either int or ISO8601 timestamp string")
        if not isinstance(field, str):
            raise ApiError("field parameter should be a string")
        if not isinstance(bucket_size, int) and not isinstance(bucket_size, str):
            raise ApiError("bucket_size should be either int or ISO8601 timestamp string")

    def add_range(self, range):
        """Sets the facet ranges to be received by this query.

        Arguments:
            range (dict or [dict]): Range(s) to be received.

        Returns:
            Query (AsyncFacetQuery): The Query object that will receive the specified range(s).

        Note: The range parameter must be in this dictionary format:
            {
                "bucket_size": "<object>",
                "start": "<object>",
                "end": "<object>",
                "field": "<string>"
            },
            where "bucket_size", "start", and "end" can be numbers or ISO 8601 timestamps.

        Examples:
        >>> cb.select(ProcessFacet).add_range({"bucket_size": 5, "start": 0, "end": 10, "field": "netconn_count"})
        >>> cb.select(ProcessFacet).add_range({"bucket_size": "+1DAY", "start": "2020-11-01T00:00:00Z",
                                               "end": "2020-11-12T00:00:00Z", "field": "backend_timestamp"})
        """
        if isinstance(range, dict):
            self._check_range(range)
            self._ranges.append(range)
        else:
            for r in range:
                self._check_range(r)
                self._ranges.append(r)
        return self

    def _get_query_parameters(self):
        args = self._default_args.copy()
        if not (self._facet_fields or self._ranges):
            raise ApiError("Process Facet Queries require at least one field or range to be requested. "
                           "Use add_facet_field(['my_facet_field']) to add fields to the request.")
        terms = {}
        if self._facet_fields:
            terms["fields"]: self._facet_fields
        if self._facet_rows:
            terms["rows"] = self._facet_rows
        args["terms"] = terms
        if self._ranges:
            args["ranges"] = self._ranges
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

    def _submit(self):
        if self._query_token:
            raise ApiError(f"Query already submitted: token {self._query_token}")

        args = self._get_query_parameters()
        self._validate(args)

        url = f"/api/investigate/v2/orgs/{self._cb.credentials.org_key}/processes/facet_jobs"
        query_start = self._cb.post_object(url, body=args)

        self._query_token = query_start.json().get("job_id")

        self._timed_out = False
        self._submit_time = time.time() * 1000

    def _still_querying(self):
        if not self._query_token:
            self._submit()

        result_url = (f"/api/investigate/v2/orgs/{self._cb.credentials.org_key}/processes"
                      f"/facet_jobs/{self._query_token}/results")
        result = self._cb.get_object(result_url)

        searchers_contacted = result.get("contacted", 0)
        searchers_completed = result.get("completed", 0)
        log.debug("contacted = {}, completed = {}".format(searchers_contacted, searchers_completed))
        if searchers_contacted == 0:
            return True
        if searchers_completed < searchers_contacted:
            if self._timeout != 0 and (time.time() * 1000) - self._submit_time > self._timeout:
                self._timed_out = True
                return False
            return True

        return False

    def _count(self):
        if self._count_valid:
            return self._total_results

        while self._still_querying():
            time.sleep(.5)

        if self._timed_out:
            raise TimeoutError(message="user-specified timeout exceeded while waiting for results")

        result_url = (f"/api/investigate/v2/orgs/{self._cb.credentials.org_key}/processes"
                      f"/facet_jobs/{self._query_token}/results")
        result = self._cb.get_object(result_url)

        self._total_results = result.get('num_found', 0)
        self._count_valid = True

        return self._total_results

    def _search(self):
        """Execute the query, iterating over results 500 rows at a time."""
        if not self._query_token:
            self._submit()

        while self._still_querying():
            time.sleep(.5)

        if self._timed_out:
            raise TimeoutError(message="User-specified timeout exceeded while waiting for results")

        log.debug(f"Pulling results, timed_out={self._timed_out}")

        result_url = (f"/api/investigate/v2/orgs/{self._cb.credentials.org_key}/processes"
                      f"/facet_jobs/{self._query_token}/results")
        if self._limit:
            query_parameters = {"limit": self._limit}
        else:
            query_parameters = {}

        result = self._cb.get_object(result_url, query_parameters=query_parameters)
        yield self._doc_class(self._cb, model_unique_id=self._query_token, initial_data=result)

    def _init_async_query(self):
        """Initialize an async query and return a context for running in the background.

        Returns:
            object: Context for running in the background (the query token).
        """
        self._submit()
        return self._query_token

    def _run_async_query(self, context):
        """Executed in the background to run an asynchronous query.

        Args:
            context (object): The context (query token) returned by _init_async_query.

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        if context != self._query_token:
            raise ApiError("Async query not properly started")
        return list(self._search())


class TreeQuery(BaseQuery, QueryBuilderSupportMixin, IterableQueryMixin):
    """Represents the logic for a Tree query."""
    def __init__(self, doc_class, cb):
        super(TreeQuery, self).__init__()
        self._doc_class = doc_class
        self._cb = cb
        self._args = {}

    def where(self, **kwargs):
        """Adds a conjunctive filter to this TreeQuery.

        Arguments:
            **kwargs: Arguments to invoke the TreeQuery with.

        Returns:
            Query (TreeQuery): TreeQuery with added arguments.

        Example:

        >>> cb.select(Tree).where(process_guid="...")
        """
        self._args = dict(self._args, **kwargs)
        return self

    def and_(self, **kwargs):
        """Adds a conjunctive filter to this TreeQuery.

        Arguments:
            **kwargs: Arguments to invoke the TreeQuery with.

        Returns:
            Query (TreeQuery): TreeQuery with added arguments.
        """




        self.where(**kwargs)
        return self

    def or_(self, **kwargs):
        """Unsupported. Will raise if called.

        Raises:
            APIError: TreeQueries do not support _or() filters.
        """
        raise ApiError(".or_() cannot be called on Tree queries")

    def _perform_query(self):
        if "process_guid" not in self._args:
            raise ApiError("required parameter process_guid missing")

        log.debug("Fetching process tree")

        url = self._doc_class.urlobject.format(self._cb.credentials.org_key)
        results = self._cb.get_object(url, query_parameters=self._args)

        while results["incomplete_results"]:
            result = self._cb.get_object(url, query_parameters=self._args)
            results["nodes"]["children"].extend(result["nodes"]["children"])
            results["incomplete_results"] = result["incomplete_results"]

        return results


class EventQuery(Query):
    """Represents the logic for an Event query."""
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
        # iterate over total result set, 100 at a time
        args = self._get_query_parameters()
        self._validate(args)

        if start != 0:
            args['start'] = start
        args['rows'] = self._batch_size

        current = start
        numrows = 0

        still_querying = True

        while still_querying:
            url = self._doc_class.urlobject.format(
                self._cb.credentials.org_key,
                args["process_guid"]
            )
            resp = self._cb.post_object(url, body=args)
            result = resp.json()

            self._total_results = result.get("num_available", 0)
            self._total_segments = result.get("total_segments", 0)
            self._processed_segments = result.get("processed_segments", 0)
            self._count_valid = True
            if self._processed_segments != self._total_segments:
                continue  # loop until we get all segments back

            results = result.get('results', [])

            for item in results:
                yield item
                current += 1

                numrows += 1
                if rows and numrows == rows:
                    still_querying = False
                    break

            args['start'] = current + 1  # as of 6/2017, the indexing on the Cb Endpoint Standard backend is still 1-based

            if current >= self._total_results:
                break
            if not results:
                log.debug("server reported total_results overestimated the number of results for this query by {0}"
                          .format(self._total_results - current))
                log.debug("resetting total_results for this query to {0}".format(current))
                self._total_results = current
                break
