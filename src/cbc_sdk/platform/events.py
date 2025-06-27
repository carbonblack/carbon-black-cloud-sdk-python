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

"""Model and Query Classes for Events"""

from cbc_sdk.base import UnrefreshableModel, Query, FacetQuery
from cbc_sdk.errors import ApiError, TimeoutError

import logging
import time

log = logging.getLogger(__name__)

MAX_EVENT_SEARCH_RETRIES = 10


class Event(UnrefreshableModel):
    """Events can be queried for via `CBCloudAPI.select` or an already selected process with `Process.events()`.

    Examples:
        >>> events_query = (api.select(Event).where(process_guid=
                            "WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb"))
        # retrieve results synchronously
        >>> events = [event for event in events_query]
        # retrieve results asynchronously
        >>> future = events_query.execute_async()
        >>> events = future.result()
        # use an already selected process
        >>> process = api.select(Process, "WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb")
        >>> events_query = process.events()
        >>> events = [event for event in events_query]
    """
    urlobject = '/api/investigate/v2/orgs/{}/events/{}/_search'
    validation_url = '/api/investigate/v1/orgs/{}/events/search_validation'
    validation_method = 'POST'
    default_sort = 'last_update desc'
    primary_key = "process_guid"

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        return EventQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=True):
        """
        Initialize the Event object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (str): The unique ID for this particular instance of the model object.
            initial_data (dict): The data to use when initializing the model object.
            force_init (bool): True to force object initialization.
            full_doc (bool): True to mark the object as fully initialized.
        """
        super(Event, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                    force_init=force_init, full_doc=full_doc)


class EventFacet(UnrefreshableModel):
    """Represents the results of an EventFacetQuery.

    EventFacet objects contain both Terms and Ranges. Each of those contain facet
    fields and values.

    Access all of the Terms facet data with :func:`EventFacet.Terms.facets` or see just
    the field names with :func:`EventFacet.Terms.fields`.

    Access all of the Ranges facet data with :meth:`EventFacet.Ranges.facets` or see just
    the field names with :func:`EventFacet.Ranges.fields`.

    Event Facets can be queried for via `CBCloudAPI.select(EventFacet). Specify
    a Process GUID with `.where(process_guid="example_guid")`, and facet field(s)
    with `.add_facet_field("my_facet_field")`.

    Examples:
        >>> event_facet_query = (api.select(EventFacet).where(process_guid=
        "WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb"))
        >>> event_facet_query.add_facet_field("event_type")
        # retrieve results synchronously
        >>> facet = event_facet_query.results
        # retrieve results asynchronously
        >>> future = event_facet_query.execute_async()
        >>> result = future.result()
        # result is a list with one item, so access the first item
        >>> facet = result[0]
    """
    primary_key = "process_guid"
    urlobject = "/api/investigate/v2/orgs/{}/events/{}/_facet"

    class Terms(UnrefreshableModel):
        """Represents the facet fields and values associated with an Event Facet query."""
        def __init__(self, cb, initial_data):
            """Initialize a ProcessFacet Terms object with initial_data."""
            super(EventFacet.Terms, self).__init__(
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
        """Represents the range (bucketed) facet fields and values associated with an Event Facet query."""
        def __init__(self, cb, initial_data):
            """Initialize a ProcessFacet Ranges object with initial_data."""
            super(EventFacet.Ranges, self).__init__(
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
            """Returns the reified `EventFacet.Terms._facets` for this result."""
            return self._facets

        @property
        def fields(self):
            """Returns the ranges fields for this result."""
            return [field for field in self._facets]

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return EventFacetQuery(cls, cb)

    def __init__(self, cb, model_unique_id, initial_data):
        """Initialize an EventFacet object with initial_data."""
        super(EventFacet, self).__init__(
            cb,
            model_unique_id=model_unique_id,
            initial_data=initial_data,
            force_init=False,
            full_doc=True
        )
        self._terms = EventFacet.Terms(cb, initial_data=initial_data["terms"])
        self._ranges = EventFacet.Ranges(cb, initial_data=initial_data["ranges"])

    @property
    def terms_(self):
        """Returns the reified `EventFacet.Terms` for this result."""
        return self._terms

    @property
    def ranges_(self):
        """Returns the reified `EventFacet.Ranges` for this result."""
        return self._ranges


# Event Queries


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

        still_querying, last_processed_segments, retry_counter = (True, -1, 0)

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
            if self._processed_segments != self._total_segments \
                    and len(result.get('results', [])) != self._total_results:
                retry_counter = 0 if self._processed_segments > last_processed_segments else retry_counter + 1
                last_processed_segments = max(last_processed_segments, self._processed_segments)
                if retry_counter == MAX_EVENT_SEARCH_RETRIES:
                    raise TimeoutError(url, resp.status_code, "excessive number of retries in event query")
                time.sleep(1 + retry_counter / 10)
                continue  # loop until we get all segments back

            results = result.get('results', [])

            for item in results:
                yield item
                current += 1

                numrows += 1
                if rows and numrows == rows:
                    still_querying = False
                    break

            args['start'] = current

            if current >= self._total_results:
                break
            if not results:
                log.debug("server reported total_results overestimated the number of results for this query by {0}"
                          .format(self._total_results - current))
                log.debug("resetting total_results for this query to {0}".format(current))
                self._total_results = current
                break


class EventFacetQuery(FacetQuery):
    """Represents the logic for an Event Facet query."""
    def _get_query_parameters(self):
        args = self._default_args.copy()
        if not (self._facet_fields or self._ranges):
            raise ApiError("Event Facet Queries require at least one field or range to be requested. "
                           "Use add_facet_field(['my_facet_field']) to add fields to the request, "
                           "or use add_range({}) to add ranges to the request.")
        terms = {}
        if self._facet_fields:
            terms["fields"] = self._facet_fields
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
        query = self._query_builder._collapse()
        if query:
            args['query'] = query
        if self._query_builder._process_guid is not None:
            args["process_guid"] = self._query_builder._process_guid
        if 'process_guid:' in args.get('query', ""):
            q = args['query'].split('process_guid:', 1)[1].split(' ', 1)[0]
            args["process_guid"] = q
        return args

    def _perform_query(self, from_row=0, max_rows=-1):
        if max_rows > 0:
            return self.results[from_row:from_row + max_rows]
        elif from_row > 0:
            return self.results[from_row:]
        else:
            return self.results

    def _submit(self):
        args = self._get_query_parameters()
        # args["process_guid"] is used in the URL but not the args
        process_guid = args.pop("process_guid", None)
        # a GUID is required for this API call
        if process_guid is None:
            raise ApiError("Specify a Process GUID to search Event Facets for "
                           "with cb.select(EventFacet).where(process_guid='example_guid')")

        url = self._doc_class.urlobject.format(
            self._cb.credentials.org_key,
            process_guid
        )
        resp = self._cb.post_object(url, body=args)
        return url, resp.status_code, resp.json()

    def _search(self):
        """Execute the query until 'processed_segments' == 'total_segments'"""
        args = self._get_query_parameters()
        self._validate(args)
        still_querying, last_processed_segments, retry_counter = (True, -1, 0)
        while still_querying:
            url, code, result = self._submit()

            self._total_results = result.get("num_available", 0)
            self._total_segments = result.get("total_segments", 0)
            self._processed_segments = result.get("processed_segments", 0)
            self._count_valid = True
            if self._processed_segments != self._total_segments:
                retry_counter = 0 if self._processed_segments > last_processed_segments else retry_counter + 1
                last_processed_segments = max(last_processed_segments, self._processed_segments)
                if retry_counter == MAX_EVENT_SEARCH_RETRIES:
                    raise TimeoutError(url, code, "excessive number of retries in event facet query")
                time.sleep(1 + retry_counter / 10)
                continue  # loop until we get all segments back

            # processed_segments == total_segments, end the search
            return self._doc_class(self._cb, model_unique_id=self._query_token, initial_data=result)
