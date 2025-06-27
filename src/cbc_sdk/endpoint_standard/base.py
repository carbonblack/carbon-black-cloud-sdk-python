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

"""Model and Query Classes for Endpoint Standard"""

from cbc_sdk.base import UnrefreshableModel, FacetQuery
from cbc_sdk.base import Query as BaseEventQuery
from cbc_sdk.errors import ApiError, TimeoutError, FunctionalityDecommissioned
from cbc_sdk.platform.reputation import ReputationOverride
from pathlib import Path

import logging
import time
import os

log = logging.getLogger(__name__)

"""Endpoint Standard Models"""


class Event:
    """
    Represents an Endpoint Standard Event.

    This functionality has been decommissioned.  Please use EnrichedEvent instead.  More information may be found
    here:
    https://community.carbonblack.com/t5/Developer-Relations/Migration-Guide-Carbon-Black-Cloud-Events-API/m-p/95915/thread-id/2519
    """
    urlobject = "/integrationServices/v3/event"
    primary_key = "eventId"
    info_key = "eventInfo"

    def _parse(self, obj):
        if isinstance(obj, dict) and self.info_key in obj:
            return obj[self.info_key]

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        This functionality has been decommissioned.  Do not use.

        Args:
            cb (BaseAPI): Unused.
            model_unique_id (int): Unused.
            initial_data (dict): Unused.

        Raises:
            FunctionalityDecommissioned: Always.
        """
        raise FunctionalityDecommissioned("Endpoint Standard events", "Platform enriched events")

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        This functionality has been decommissioned.  Do not use.

        Args:
            cb (BaseAPI): Unused.
            **kwargs (dict): Unused.

        Raises:
            FunctionalityDecommissioned: Always.
        """
        raise FunctionalityDecommissioned("Endpoint Standard events", "Platform enriched events")


class EnrichedEvent(UnrefreshableModel):
    """Represents an enriched event retrieved by one of the Enterprise EDR endpoints."""
    default_sort = 'device_timestamp'
    primary_key = "event_id"

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        """
        Returns the appropriate query object for this object type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            Query: The query object for this alert type.
        """
        # This will emulate a synchronous enriched event query, for now.
        return EnrichedEventQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=True):
        """
        Initialize the EnrichedEvent object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (Any): The unique ID for this particular instance of the model object.
            initial_data (dict): The data to use when initializing the model object.
            force_init (bool): True to force object initialization.
            full_doc (bool): True to mark the object as fully initialized.
        """
        self._details_timeout = cb.credentials.default_timeout
        self._info = None
        if model_unique_id is not None and initial_data is None:
            enriched_event_future = cb.select(EnrichedEvent).where(event_id=model_unique_id).execute_async()
            result = enriched_event_future.result()
            if len(result) == 1:
                initial_data = result[0]
        super(EnrichedEvent, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                            force_init=force_init, full_doc=full_doc)

    @property
    def process_sha256(self):
        """Returns a string representation of the SHA256 hash for this process.

        Returns:
            hash (str): SHA256 hash of the process.
        """
        if "process_hash" in self._info:
            return next((hsh for hsh in self.process_hash if len(hsh) == 64), None)
        elif "process_sha256" in self._info:
            return self._info.get("process_sha256", None)
        else:
            return None

    def get_details(self, timeout=0, async_mode=False):
        """Requests detailed results.

        Args:
            timeout (int): Event details request timeout in milliseconds.  This value can never be greater than
                the configured default timeout.  If this value is 0, the configured default timeout is used.
            async_mode (bool): True to request details in an asynchronous manner.

        Note:
            - When using asynchronous mode, this method returns a python future.
              You can call result() on the future object to wait for completion and get the results.
        """
        if timeout <= 0:
            self._details_timeout = self._cb.credentials.default_timeout
        else:
            self._details_timeout = min(timeout, self._cb.credentials.default_timeout)
        if not self.event_id:
            raise ApiError("Trying to get event details on an invalid event_id")
        if async_mode:
            return self._cb._async_submit(lambda arg, kwarg: self._get_detailed_results())
        else:
            return self._get_detailed_results()

    def _get_detailed_results(self):
        """Actual search details implementation"""
        assert self._details_timeout > 0
        args = {"event_ids": [self.event_id]}
        url = "/api/investigate/v2/orgs/{}/enriched_events/detail_jobs".format(self._cb.credentials.org_key)
        query_start = self._cb.post_object(url, body=args)
        job_id = query_start.json().get("job_id")
        timed_out = False
        submit_time = time.time() * 1000

        while True:
            status_url = "/api/investigate/v2/orgs/{}/enriched_events/detail_jobs/{}/results".format(
                self._cb.credentials.org_key,
                job_id,
            )
            result = self._cb.get_object(status_url)
            searchers_contacted = result.get("contacted", 0)
            searchers_completed = result.get("completed", 0)
            message = result.get("message", "")
            log.debug("contacted = {}, completed = {}".format(searchers_contacted, searchers_completed))
            if "No data available" in message:
                log.warning(message)
                return False
            if searchers_contacted == 0 or searchers_completed < searchers_contacted:
                if (time.time() * 1000) - submit_time > self._details_timeout:
                    timed_out = True
                    break
            else:
                break

            time.sleep(.5)

        if timed_out:
            raise TimeoutError(message="user-specified timeout exceeded while waiting for results")

        log.debug("Pulling detailed results, timed_out={}".format(timed_out))

        still_fetching = True
        result_url = "/api/investigate/v2/orgs/{}/enriched_events/detail_jobs/{}/results".format(
            self._cb.credentials.org_key,
            job_id
        )
        query_parameters = {}
        while still_fetching:
            result = self._cb.get_object(result_url, query_parameters=query_parameters)
            total_results = result.get('num_available', 0)
            found_results = result.get('num_found', 0)
            # if found is 0, then no enriched events
            if found_results == 0:
                return self
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


class EnrichedEventFacet(UnrefreshableModel):
    """Represents an enriched event retrieved by one of the Enterprise EDR endpoints."""
    primary_key = "job_id"
    swagger_meta_file = "endpoint_standard/models/enriched_event_facet.yaml"
    submit_url = "/api/investigate/v2/orgs/{}/enriched_events/facet_jobs"
    result_url = "/api/investigate/v2/orgs/{}/enriched_events/facet_jobs/{}/results"

    class Terms(UnrefreshableModel):
        """Represents the facet fields and values associated with an Enriched Event Facet query."""
        def __init__(self, cb, initial_data):
            """Initialize an EnrichedEventFacet Terms object with initial_data."""
            super(EnrichedEventFacet.Terms, self).__init__(
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
        """Represents the range (bucketed) facet fields and values associated with an Enriched Event Facet query."""
        def __init__(self, cb, initial_data):
            """Initialize an EnrichedEventFacet Ranges object with initial_data."""
            super(EnrichedEventFacet.Ranges, self).__init__(
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
            """Returns the reified `EnrichedEventFacet.Terms._facets` for this result."""
            return self._facets

        @property
        def fields(self):
            """Returns the ranges fields for this result."""
            return [field for field in self._facets]

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        # This will emulate a synchronous enricehd event facet query, for now.
        return FacetQuery(self, cb)

    def __init__(self, cb, model_unique_id, initial_data):
        """Initialize the Terms object with initial data."""
        super(EnrichedEventFacet, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                                 force_init=False, full_doc=True)
        self._terms = EnrichedEventFacet.Terms(cb, initial_data=initial_data["terms"])
        self._ranges = EnrichedEventFacet.Ranges(cb, initial_data=initial_data["ranges"])

    @property
    def terms_(self):
        """Returns the reified `EnrichedEventFacet.Terms` for this result."""
        return self._terms

    @property
    def ranges_(self):
        """Returns the reified `EnrichedEventFacet.Ranges` for this result."""
        return self._ranges


"""Endpoint Standard Queries"""


class EnrichedEventQuery(BaseEventQuery):
    """Represents the query logic for an Enriched Event query.

    This class specializes `Query` to handle the particulars of enriched events querying.
    """

    def __init__(self, doc_class, cb):
        """
        Initialize the EnrichedEventQuery object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(EnrichedEventQuery, self).__init__(doc_class, cb)
        self._default_args["rows"] = self._batch_size
        self._query_token = None
        self._timeout = cb.credentials.default_timeout
        self._timed_out = False
        self._aggregation = False
        self._aggregation_field = None

    def or_(self, **kwargs):
        """
        :meth:`or_` criteria are explicitly provided to EnrichedEvent queries.

        This method overrides the base class in order to provide or_() functionality rather than raising an exception.
        """
        self._query_builder.or_(None, **kwargs)
        return self

    def aggregation(self, field):
        """
        Performs an aggregation search where results are grouped by an aggregation field

        Args:
            field (str): The aggregation field, either 'process_sha256' or 'device_id'
        """
        if field not in ['process_sha256', 'device_id']:
            raise ApiError("Aggregation field must be either 'device_id' or 'process_sha256'")

        self._aggregation = True
        self._aggregation_field = field
        return self

    def set_rows(self, rows):
        """
        Sets the 'rows' query body parameter to the 'start search' API call, determining how many rows to request.

        Args:
            rows (int): How many rows to request.
        """
        if not isinstance(rows, int):
            raise ApiError(f"Rows must be an integer. {rows} is a {type(rows)}.")
        if rows > 10000:
            raise ApiError("Maximum allowed value for rows is 10000")
        super(EnrichedEventQuery, self).set_rows(rows)
        return self

    def timeout(self, msecs):
        """Sets the timeout on a event query.

        Arguments:
            msecs (int): Timeout duration, in milliseconds.  This value can cever be greater than the configured
                default timeout.  If this value is 0, the configured default timeout is used.

        Returns:
            Query (EnrichedEventQuery): The Query object with new milliseconds parameter.

        Example:
            >>> cb.select(EnrichedEvent).where(process_name="foo.exe").timeout(5000)
        """
        if msecs <= 0:
            self._timeout = self._cb.credentials.default_timeout
        else:
            self._timeout = min(msecs, self._cb.credentials.default_timeout)
        return self

    def _submit(self):
        if self._query_token:
            raise ApiError("Query already submitted: token {0}".format(self._query_token))

        args = self._get_query_parameters()

        if self._aggregation:
            url = "/api/investigate/v1/orgs/{}/enriched_events/aggregation_jobs/{}"
            url = url.format(self._cb.credentials.org_key, self._aggregation_field)
        else:
            url = "/api/investigate/v2/orgs/{}/enriched_events/search_jobs".format(self._cb.credentials.org_key)
        query_start = self._cb.post_object(url, body=args)
        self._query_token = query_start.json().get("job_id")
        self._timed_out = False
        self._submit_time = time.time() * 1000

    def _still_querying(self):
        assert self._timeout > 0
        if not self._query_token:
            self._submit()

        if self._aggregation:
            return False

        status_url = "/api/investigate/v2/orgs/{}/enriched_events/search_jobs/{}/results?start=0&rows=0".format(
            self._cb.credentials.org_key,
            self._query_token,
        )
        result = self._cb.get_object(status_url)
        searchers_contacted = result.get("contacted", 0)
        searchers_completed = result.get("completed", 0)
        message = result.get("message", "")
        log.debug("contacted = {}, completed = {}".format(searchers_contacted, searchers_completed))
        if "No data available" in message:
            log.warning(message)
            return False
        if searchers_contacted == 0 or searchers_completed < searchers_contacted:
            if (time.time() * 1000) - self._submit_time > self._timeout:
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

        if self._aggregation:
            result_url = "/api/investigate/v1/orgs/{}/enriched_events/aggregation_jobs/{}/results".format(
                self._cb.credentials.org_key,
                self._query_token,
            )
        else:
            result_url = "/api/investigate/v2/orgs/{}/enriched_events/search_jobs/{}/results".format(
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
        result_url_template = "/api/investigate/v2/orgs/{}/enriched_events/search_jobs/{}/results".format(
            self._cb.credentials.org_key,
            self._query_token
        )
        query_parameters = {}
        while still_fetching:
            if self._aggregation:
                result_url = "/api/investigate/v1/orgs/{}/enriched_events/aggregation_jobs/{}/results".format(
                    self._cb.credentials.org_key,
                    self._query_token,
                )
            else:
                result_url = '{}?start={}&rows={}'.format(
                    result_url_template,
                    current,
                    self._batch_size
                )

            result = self._cb.get_object(result_url, query_parameters=query_parameters)
            if self._aggregation:
                contacted = result.get('contacted', 0)
                completed = result.get('completed', 0)
                if contacted < completed:
                    time.sleep(.5)
                    still_fetching = True
                    continue
                else:
                    still_fetching = False
                    results = result.get('results', [])
                    for item in results:
                        yield item
            else:
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
