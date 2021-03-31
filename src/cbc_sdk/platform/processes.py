#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model and Query Classes for Processes"""

from cbc_sdk.base import (UnrefreshableModel, BaseQuery, Query, FacetQuery,
                          QueryBuilderSupportMixin, QueryBuilder,
                          AsyncQueryMixin)
from cbc_sdk.platform import Event
from cbc_sdk.platform.reputation import ReputationOverride
from cbc_sdk.errors import ApiError, TimeoutError
from pathlib import Path

import logging
import time
import os

log = logging.getLogger(__name__)


class Process(UnrefreshableModel):
    """Represents a process retrieved by one of the Enterprise EDR endpoints.

    Examples:
        # use the Process GUID directly
        >>> process = api.select(Process, "WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb")
        # use the Process GUID in a where() clause
        >>> process_query = (api.select(Process).where(process_guid=
                             "WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb"))
        >>> process_query_results = [proc for proc in process_query]
        >>> process_2 = process_query_results[0]
    """
    default_sort = 'last_update desc'
    primary_key = "process_guid"
    validation_url = "/api/investigate/v1/orgs/{}/processes/search_validation"
    urlobject = ""

    class Summary(UnrefreshableModel):
        """Represents a summary of organization-specific information for a process.

        The preferred interface for interacting with Summary models is `Process.summary`.

        Example:
            >>> process = api.select(Process, "WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb")
            >>> summary = process.summary
        """
        urlobject = "/api/investigate/v2/orgs/{}/processes/summary_jobs"
        result_url = '/api/investigate/v2/orgs/{}/processes/summary_jobs/{}/results'
        summary_format = "summary"
        default_sort = "last_update desc"
        primary_key = "process_guid"
        SHOW_ATTR = {'process': {'type': 'single', 'fields': ['device_id', 'device_name', 'process_name',
                                                              'parent_guid', 'parent_hash', 'parent_name',
                                                              'parent_pid', 'process_hash', 'process_pid']},
                     'siblings': {'type': 'list', 'fields': ['process_name', 'process_guid', 'process_hash',
                                                             'process_pid']},
                     'parent': {'type': 'single', 'fields': ['process_name', 'process_guid', 'process_hash',
                                                             'process_pid']},
                     'children': {'type': 'list', 'fields': ['process_name', 'process_guid', 'process_hash',
                                                             'process_pid']}}

        def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=True):
            """
            Initialize the Summary object.

            Args:
                cb (CBCloudAPI): A reference to the CBCloudAPI object.
                model_unique_id (str): The unique ID for this particular instance of the model object.
                initial_data (dict): The data to use when initializing the model object.
                force_init (bool): True to force object initialization.
                full_doc (bool): True to mark the object as fully initialized.
            """
            if model_unique_id is not None and initial_data is None:
                initial_data = cb.select(Process.Summary).where(process_guid=model_unique_id).results._info
            super(Process.Summary, self).__init__(cb, model_unique_id=model_unique_id,
                                                  initial_data=initial_data, force_init=False,
                                                  full_doc=True)

        def __str__(self):
            """
            Returns a string representation of the object.

            Returns:
                str: A string representation of the object.
            """
            lines = []
            for top_level in self._info:
                if self._info[top_level] and top_level in self.SHOW_ATTR:
                    if self.SHOW_ATTR[top_level]['type'] == 'single':
                        lines.append('{}:'.format(top_level))
                    else:
                        lines.append(f"{top_level} ({len(self._info[top_level])}):")

                    if self.SHOW_ATTR[top_level]['type'] == 'single':
                        for attr in self._info[top_level]:
                            if attr in self.SHOW_ATTR[top_level]['fields']:
                                try:
                                    val = str(self._info[top_level][attr])
                                except UnicodeDecodeError:
                                    val = repr(self._info[top_level][attr])
                                lines.append(u"{0:s} {1:>20s}: {2:s}".format("    ", attr, val))
                    else:
                        for item in self._info[top_level]:
                            for attr in item:
                                if attr in self.SHOW_ATTR[top_level]['fields']:
                                    try:
                                        val = str(item[attr])
                                    except UnicodeDecodeError:
                                        val = repr(item[attr])
                                    lines.append(u"{0:s} {1:>20s}: {2:s}".format("    ", attr, val))
                            lines.append('')
            return "\n".join(lines)

        @classmethod
        def _query_implementation(self, cb, **kwargs):
            return SummaryQuery(self, cb, **kwargs)

    class Tree(UnrefreshableModel):
        """Represents a summary of organization-specific information for a process.

        The preferred interface for interacting with Tree models is `Process.tree`.

        Example:
            >>> process = api.select(Process, "WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb")
            >>> tree = process.tree
        """
        urlobject = '/api/investigate/v2/orgs/{}/processes/summary_jobs'
        result_url = '/api/investigate/v2/orgs/{}/processes/summary_jobs/{}/results'
        summary_format = 'tree'
        default_sort = "last_update desc"
        primary_key = 'process_guid'
        SHOW_ATTR = {'top': ['device_id', 'device_name', 'process_name',
                             'parent_guid', 'parent_hash', 'parent_name',
                             'parent_pid', 'process_hash', 'process_pid'],
                     'children': ['process_name', 'process_guid', 'process_hash', 'process_pid']}

        def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=True):
            """
            Initialize the Tree object.

            Args:
                cb (CBCloudAPI): A reference to the CBCloudAPI object.
                model_unique_id (str): The unique ID for this particular instance of the model object.
                initial_data (dict): The data to use when initializing the model object.
                force_init (bool): True to force object initialization.
                full_doc (bool): True to mark the object as fully initialized.
            """
            if model_unique_id is not None and initial_data is None:
                initial_data = cb.select(Process.Tree).where(process_guid=model_unique_id).results._info
            super(Process.Tree, self).__init__(
                cb, model_unique_id=model_unique_id, initial_data=initial_data,
                force_init=force_init, full_doc=full_doc
            )

        def __str__(self):
            """
            Returns a string representation of the object.

            Returns:
                str: A string representation of the object.
            """
            lines = []
            lines.append('process:')
            for attr in self._info:
                if attr in self.SHOW_ATTR['top']:
                    try:
                        val = str(self._info[attr])
                    except UnicodeDecodeError:
                        val = repr(self._info[attr])
                    lines.append(u"{0:s} {1:>20s}: {2:s}".format("    ", attr, val))

            lines.append(f"children ({len(self._info['children'])}):")
            for child in self._info['children']:
                for attr in child:
                    if attr in self.SHOW_ATTR['children']:
                        try:
                            val = str(child[attr])
                        except UnicodeDecodeError:
                            val = repr(child[attr])
                        lines.append(u"{0:s} {1:>20s}: {2:s}".format("    ", attr, val))
                lines.append('')
            return "\n".join(lines)

        @classmethod
        def _query_implementation(self, cb, **kwargs):
            return SummaryQuery(self, cb, **kwargs)

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        return AsyncProcessQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the Process object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (str): The unique ID (GUID) for this process.
            initial_data (dict): The data to use when initializing the model object.
            force_init (bool): True to force object initialization.
            full_doc (bool): True to mark the object as fully initialized.
        """
        if model_unique_id is not None and initial_data is None:
            process_future = cb.select(Process).where(process_guid=model_unique_id).execute_async()
            result = process_future.result()
            if len(result) == 1:
                initial_data = result[0]
        super(Process, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                      force_init=force_init, full_doc=full_doc)

    @property
    def summary(self):
        """Returns organization-specific information about this process."""
        return self._cb.select(Process.Summary).where(process_guid=self.process_guid).results

    @property
    def tree(self):
        """Returns a Process Tree associated with this process.

        Returns:
            Tree (cbc_sdk.enterprise_edr.Tree): Tree with children (and possibly siblings).

        Example:

        >>> tree = process.tree
        """
        return self._cb.select(Process.Tree).where(process_guid=self.process_guid).results

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

    def facets(self):
        """Returns a FacetQuery for a Process.

        This represents the search for a summary of result groupings (facets).
        The returned AsyncFacetQuery object must have facet fields or ranges specified
        before it can be submitted, using the `add_facet_field()` or `add_range()` methods.
        """
        return self._cb.select(ProcessFacet).where(process_guid=self.process_guid)

    def get_details(self, timeout=0, async_mode=False):
        """Requests detailed results.

        Args:
            timeout (int): Event details request timeout in milliseconds.
            async_mode (bool): True to request details in an asynchronous manner.

        Note:
            - When using asynchronous mode, this method returns a python future.
              You can call result() on the future object to wait for completion and get the results.
        """
        self._details_timeout = timeout
        if not self.process_guid:
            raise ApiError("Trying to get process details on an invalid process_guid")
        if async_mode:
            return self._cb._async_submit(lambda arg, kwarg: self._get_detailed_results()._info)
        else:
            return self._get_detailed_results()._info

    def _get_detailed_results(self):
        """Actual search details implementation"""
        args = {"process_guids": [self.process_guid]}
        url = "/api/investigate/v2/orgs/{}/processes/detail_jobs".format(self._cb.credentials.org_key)
        query_start = self._cb.post_object(url, body=args)
        job_id = query_start.json().get("job_id")
        timed_out = False
        submit_time = time.time() * 1000

        while True:
            status_url = "/api/investigate/v2/orgs/{}/processes/detail_jobs/{}".format(
                self._cb.credentials.org_key,
                job_id,
            )
            result = self._cb.get_object(status_url)
            searchers_contacted = result.get("contacted", 0)
            searchers_completed = result.get("completed", 0)
            log.debug("contacted = {}, completed = {}".format(searchers_contacted, searchers_completed))
            if searchers_contacted == 0:
                time.sleep(.5)
                continue
            if searchers_completed < searchers_contacted:
                if self._details_timeout != 0 and (time.time() * 1000) - submit_time > self._details_timeout:
                    timed_out = True
                    break
            else:
                break

            time.sleep(.5)

        if timed_out:
            raise TimeoutError(message="user-specified timeout exceeded while waiting for results")

        log.debug("Pulling detailed results, timed_out={}".format(timed_out))

        still_fetching = True
        result_url = "/api/investigate/v2/orgs/{}/processes/detail_jobs/{}/results".format(
            self._cb.credentials.org_key,
            job_id
        )
        query_parameters = {}
        while still_fetching:
            result = self._cb.get_object(result_url, query_parameters=query_parameters)
            total_results = result.get('num_available', 0)
            if total_results != 0:
                results = result.get('results', [])
                self._info = results[0]
                return self

    def ban_process_sha256(self, description=""):
        """Bans the application by adding the process_sha256 to the BLACK_LIST

        Args:
            description: The justification for why the application was added to the BLACK_LIST

        Returns:
            ReputationOverride (cbc_sdk.platform.ReputationOverride): ReputationOverride object
                created in the Carbon Black Cloud
        """
        return ReputationOverride.create(self._cb, {
            "description": description,
            "override_list": "BLACK_LIST",
            "override_type": "SHA256",
            "sha256_hash": self.process_sha256,
            "filename": Path(self.process_name.replace('\\', os.sep)).name})

    def approve_process_sha256(self, description=""):
        """Approves the application by adding the process_sha256 to the WHITE_LIST

        Args:
            description: The justification for why the application was added to the WHITE_LIST

        Returns:
            ReputationOverride (cbc_sdk.platform.ReputationOverride): ReputationOverride object
                created in the Carbon Black Cloud
        """
        return ReputationOverride.create(self._cb, {
            "description": description,
            "override_list": "WHITE_LIST",
            "override_type": "SHA256",
            "sha256_hash": self.process_sha256,
            "filename": Path(self.process_name.replace('\\', os.sep)).name})


class ProcessFacet(UnrefreshableModel):
    """Represents the results of an AsyncFacetQuery.

    ProcessFacet objects contain both Terms and Ranges. Each of those contain facet
    fields and values.

    Access all of the Terms facet data with ProcessFacet.terms_.facets or see just
    the field names with ProcessFacet.terms_.fields.

    Access all of the Ranges facet data with ProcessFacet.ranges_.facets or see just
    the field names with ProcessFacet.ranges_.fields.

    Process Facets can be queried for via `CBCloudAPI.select(ProcessFacet). Specify
    a Process GUID with `.where(process_guid="example_guid")`, and facet field(s)
    with `.add_facet_field("my_facet_field")`.

    Examples:
        >>> process_facet_query = (api.select(ProcessFacet).where(process_guid=
                                   "WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb"))
        >>> process_facet_query.add_facet_field("device_name")
        # retrieve results synchronously
        >>> facet = process_facet_query.results
        # retrieve results asynchronously
        >>> future = process_facet_query.execute_async()
        >>> result = future.result()
        # result is a list with one item, so access the first item
        >>> facet = result[0]
    """
    primary_key = "job_id"
    swagger_meta_file = "platform/models/process_facets.yaml"
    submit_url = "/api/investigate/v2/orgs/{}/processes/facet_jobs"
    result_url = "/api/investigate/v2/orgs/{}/processes/facet_jobs/{}/results"

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
        return FacetQuery(cls, cb)

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


class AsyncProcessQuery(Query):
    """Represents the query logic for an asychronous Process query.

    This class specializes `Query` to handle the particulars of
    process querying.
    """
    def __init__(self, doc_class, cb):
        """
        Initialize the AsyncProcessQuery object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
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


class SummaryQuery(BaseQuery, AsyncQueryMixin, QueryBuilderSupportMixin):
    """Represents the logic for a Process Summary or Process Tree query."""
    def __init__(self, doc_class, cb):
        """
        Initialize the SummaryQuery object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(SummaryQuery, self).__init__()
        self._doc_class = doc_class
        self._cb = cb
        self._query_builder = QueryBuilder()
        self._query_token = None
        self._full_init = False
        self._timeout = 0
        self._timed_out = False
        self._time_range = {}

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
        args = {}
        if self._time_range:
            args["time_range"] = self._time_range
        query = self._query_builder._collapse()
        if self._query_builder._process_guid is not None:
            args["process_guid"] = self._query_builder._process_guid
        elif 'process_guid:' in query:
            q = query.split('process_guid:', 1)[1].split(' ', 1)[0]
            args["process_guid"] = q

        if 'parent_guid:' in query:
            # extract parent_guid from where() clause
            parent_guid = query.split('parent_guid:', 1)[1].split(' ', 1)[0]
            args["parent_guid"] = parent_guid
        return args

    def _count(self):
        raise ApiError('The result is not iterable')

    def _submit(self):
        if self._query_token:
            raise ApiError("Query already submitted: token {0}".format(self._query_token))

        args = self._get_query_parameters()

        url = "/api/investigate/v2/orgs/{}/processes/summary_jobs".format(self._cb.credentials.org_key)
        query_start = self._cb.post_object(url, body=args)

        self._query_token = query_start.json().get("job_id")

        self._timed_out = False
        self._submit_time = time.time() * 1000

    def _still_querying(self):
        if not self._query_token:
            self._submit()

        status_url = "/api/investigate/v2/orgs/{}/processes/summary_jobs/{}".format(
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

    def _search(self, start=0, rows=0):
        """Execute the query, with one expected result."""
        if not self._query_token:
            self._submit()

        while self._still_querying():
            time.sleep(.5)

        if self._timed_out:
            raise TimeoutError(message="User-specified timeout exceeded while waiting for results")

        log.debug(f"Pulling results, timed_out={self._timed_out}")

        result_url = self._doc_class.result_url.format(self._cb.credentials.org_key, self._query_token)

        if self._doc_class.summary_format == "summary":
            query_parameters = {"format": "summary"}
            result = self._cb.get_object(result_url, query_parameters=query_parameters)
            if result["exception"] == "":
                yield self._doc_class(self._cb, model_unique_id=self._query_token, initial_data=result["summary"])
            else:
                raise ApiError(f"Failed to get Process Summary: {result['exception']}")
        else:
            query_parameters = {"format": "tree"}
            result = self._cb.get_object(result_url, query_parameters=query_parameters)
            if result["exception"] == "":
                yield self._doc_class(self._cb, model_unique_id=self._query_token, initial_data=result["tree"])
            else:
                raise ApiError(f"Failed to get Process Tree: {result['exception']}")

    def _perform_query(self):
        for item in self.results:
            yield item

    @property
    def results(self):
        """Save query results to self._results with self._search() method."""
        if not self._full_init:
            for item in self._search():
                self._results = item
            self._full_init = True

        return self._results

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
