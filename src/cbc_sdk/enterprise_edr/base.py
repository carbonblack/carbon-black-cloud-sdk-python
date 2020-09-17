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
        self._sort_by = None
        self._group_by = None
        self._batch_size = 100
        self._default_args = {}

    def _get_query_parameters(self):
        args = self._default_args.copy()
        args['query'] = self._query_builder._collapse()
        if self._query_builder._process_guid is not None:
            args["process_guid"] = self._query_builder._process_guid
        if 'process_guid:' in args['query']:
            q = args['query'].split('process_guid:', 1)
            args["process_guid"] = q[1]
        args["fields"] = [
            "*",
            "parent_hash",
            "parent_name",
            "process_cmdline",
            "backend_timestamp",
            "device_external_ip",
            "device_group",
            "device_internal_ip",
            "device_os",
            "device_policy",
            "process_effective_reputation",
            "process_reputation",
            "process_start_time",
            "ttp"
        ]

        return args

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
        self._sort = []

    def sort_by(self, key, direction="ASC"):
        """Sets the sorting behavior on a query's results.

        Arguments:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            Query (AsyncProcessQuery: The query with sorting parameters.

        Example:

        >>> cb.select(Process).where(process_name="cmd.exe").sort_by("device_timestamp")
        """
        found = False

        for sort_item in self._sort:
            if sort_item['field'] == key:
                sort_item['order'] = direction
                found = True

        if not found:
            self._sort.append({'field': key, 'order': direction})

        self._default_args['sort'] = self._sort

        return self

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
