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
                          IterableQueryMixin)
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

        This represents the search for a summary of results from a single field of a `Run`.
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
        return Query(self, cb)

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
    """Represents the summary of results for a Process."""
    primary_key = "field"
    swagger_meta_file = "audit_remediation/models/facet.yaml"
    urlobject = "/livequery/v1/orgs/{}/runs/{}/results/_facet"

    class Values(UnrefreshableModel):
        """Represents the values associated with a field."""
        def __init__(self, cb, initial_data):
            """Initialize a ProcessFacet Values object with initial_data."""
            super(ProcessFacet.Values, self).__init__(
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
        super(ProcessFacet, self).__init__(
            cb,
            model_unique_id=None,
            initial_data=initial_data,
            force_init=False,
            full_doc=True
        )
        self._values = ProcessFacet.Values(cb, initial_data=initial_data["values"])

    @property
    def values_(self):
        """Returns the reified `ProcessFacet.Values` for this result."""
        return self._values


"""Queries"""


class Query(PaginatedQuery, QueryBuilderSupportMixin, IterableQueryMixin):
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


class FacetQuery(Query):
    """Represents a prepared query for Process Facets."""
    def __init__(self, doc_class, cb):
        """Initialize a FacetQuery object."""
        super().__init__(doc_class, cb)
        self._query_builder = QueryBuilder()
        self._facet_fields = []
        self._criteria = {}

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
