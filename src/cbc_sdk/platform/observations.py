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

"""Model and Query Classes for Observations"""

from cbc_sdk.base import UnrefreshableModel, FacetQuery
from cbc_sdk.base import Query
from cbc_sdk.errors import ApiError, TimeoutError

import logging
import time

log = logging.getLogger(__name__)


class Observation(UnrefreshableModel):
    """Represents an observations"""
    primary_key = "observation_id"
    swagger_meta_file = "platform/models/observation.yaml"

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
        # This will emulate a synchronous observation query, for now.
        return ObservationQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=True):
        """
        Initialize the Observation object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (Any): The unique ID for this particular instance of the model object.
            initial_data (dict): The data to use when initializing the model object.
            force_init (bool): True to force object initialization.
            full_doc (bool): True to mark the object as fully initialized.
        """
        self._details_timeout = 0
        self._info = None
        if model_unique_id is not None and initial_data is None:
            observations_future = cb.select(Observation).where(observation_id=model_unique_id).execute_async()
            result = observations_future.result()
            if len(result) == 1:
                initial_data = result[0]
        super(Observation, self).__init__(
            cb,
            model_unique_id=model_unique_id,
            initial_data=initial_data,
            force_init=force_init,
            full_doc=full_doc
        )

    def get_details(self, timeout=0, async_mode=False):
        """Requests detailed results.

        Args:
            timeout (int): Observations details request timeout in milliseconds.
            async_mode (bool): True to request details in an asynchronous manner.

        Note:
            - When using asynchronous mode, this method returns a python future.
              You can call result() on the future object to wait for completion and get the results.
        """
        self._details_timeout = timeout
        if not self.observation_id:
            raise ApiError("Trying to get observation details on an invalid observation_id")
        if async_mode:
            return self._cb._async_submit(lambda arg, kwarg: self._get_detailed_results())
        else:
            return self._get_detailed_results()

    def _get_detailed_results(self):
        """Actual search details implementation"""
        args = {"observation_ids": [self.observation_id]}
        url = "/api/investigate/v2/orgs/{}/observations/detail_jobs".format(self._cb.credentials.org_key)
        query_start = self._cb.post_object(url, body=args)
        job_id = query_start.json().get("job_id")
        timed_out = False
        submit_time = time.time() * 1000

        while True:
            status_url = "/api/investigate/v2/orgs/{}/observations/detail_jobs/{}/results".format(
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
        result_url = "/api/investigate/v2/orgs/{}/observations/detail_jobs/{}/results".format(
            self._cb.credentials.org_key,
            job_id
        )
        query_parameters = {}
        while still_fetching:
            result = self._cb.get_object(result_url, query_parameters=query_parameters)
            total_results = result.get('num_available', 0)
            found_results = result.get('num_found', 0)
            # if found is 0, then no observations were found
            if found_results == 0:
                return self
            if total_results != 0:
                results = result.get('results', [])
                self._info = results[0]
                return self


class ObservationFacet(UnrefreshableModel):
    """Represents an observation retrieved."""
    primary_key = "job_id"
    swagger_meta_file = "platform/models/observation_facet.yaml"
    submit_url = "/api/investigate/v2/orgs/{}/observations/facet_jobs"
    result_url = "/api/investigate/v2/orgs/{}/observations/facet_jobs/{}/results"

    class Terms(UnrefreshableModel):
        """Represents the facet fields and values associated with an Observation Facet query."""
        def __init__(self, cb, initial_data):
            """Initialize an ObservationFacet Terms object with initial_data."""
            super(ObservationFacet.Terms, self).__init__(
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
        """Represents the range (bucketed) facet fields and values associated with an Observation Facet query."""
        def __init__(self, cb, initial_data):
            """Initialize an ObservationFacet Ranges object with initial_data."""
            super(ObservationFacet.Ranges, self).__init__(
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
            """Returns the reified `ObservationFacet.Terms._facets` for this result."""
            return self._facets

        @property
        def fields(self):
            """Returns the ranges fields for this result."""
            return [field for field in self._facets]

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        # This will emulate a synchronous observation facet query, for now.
        return FacetQuery(self, cb)

    def __init__(self, cb, model_unique_id, initial_data):
        """Initialize the Terms object with initial data."""
        super(ObservationFacet, self).__init__(
            cb,
            model_unique_id=model_unique_id,
            initial_data=initial_data,
            force_init=False,
            full_doc=True
        )
        self._terms = ObservationFacet.Terms(cb, initial_data=initial_data["terms"])
        self._ranges = ObservationFacet.Ranges(cb, initial_data=initial_data["ranges"])

    @property
    def terms_(self):
        """Returns the reified `ObservationFacet.Terms` for this result."""
        return self._terms

    @property
    def ranges_(self):
        """Returns the reified `ObservationFacet.Ranges` for this result."""
        return self._ranges


class ObservationQuery(Query):
    """Represents the query logic for an Observation query.

    This class specializes `Query` to handle the particulars of observations querying.
    """
    VALID_GROUP_FIELDS = ["observation_type", "device_name", "process_username", "attack_tactic"]

    def __init__(self, doc_class, cb):
        """
        Initialize the ObservationQuery object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(ObservationQuery, self).__init__(doc_class, cb)
        self._default_args["rows"] = self._batch_size
        self._query_token = None
        self._timeout = 0
        self._timed_out = False

        self._aggregation = False
        self._aggregate_fields = None
        self._max_events_per_group = None
        self._range = None
        self._rows = None
        self._start = None

    def or_(self, **kwargs):
        """
        :meth:`or_` criteria are explicitly provided to Observation queries.

        This method overrides the base class in order to provide or_() functionality rather than raising an exception.
        """
        self._query_builder.or_(None, **kwargs)
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
        super(ObservationQuery, self).set_rows(rows)
        return self

    def timeout(self, msecs):
        """Sets the timeout on a observation query.

        Arguments:
            msecs (int): Timeout duration, in milliseconds.

        Returns:
            Query (ObservationQuery): The Query object with new milliseconds
                parameter.

        Example:
            >>> cb.select(Observation).where(process_name="foo.exe").timeout(5000)
        """
        self._timeout = msecs
        return self

    def _submit(self):
        if self._query_token:
            raise ApiError("Query already submitted: token {0}".format(self._query_token))

        args = self._get_query_parameters()
        url = "/api/investigate/v2/orgs/{}/observations/search_jobs".format(self._cb.credentials.org_key)
        query_start = self._cb.post_object(url, body=args)
        self._query_token = query_start.json().get("job_id")
        self._timed_out = False
        self._submit_time = time.time() * 1000

    def _still_querying(self):
        if not self._query_token:
            self._submit()

        if self._aggregation:
            return False

        status_url = "/api/investigate/v2/orgs/{}/observations/search_jobs/{}/results".format(
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

        if self._aggregation:
            result_url = "/api/investigate/v1/orgs/{}/observations/search_jobs/{}/group_results".format(
                self._cb.credentials.org_key,
                self._query_token,
            )
            result = self._cb.post_object(result_url, self._build_aggregated_body()).json()
        else:
            result_url = "/api/investigate/v2/orgs/{}/observations/search_jobs/{}/results".format(
                self._cb.credentials.org_key,
                self._query_token,
            )
            result = self._cb.get_object(result_url)

        self._total_results = result.get('num_available', 0)
        self._count_valid = True

        return self._total_results

    def aggregation(self, fields):
        """
        Performs an aggregation search where results are grouped by an aggregation field

        Args:
            fields (str or list): The aggregation field or fields, valid ones are:
                observation_type, device_name, process_username, attack_tactic
        """
        if not isinstance(fields, list) and not isinstance(fields, str):
            raise ApiError("Fields should be either a single field or list of fields")

        if isinstance(fields, str):
            fields = [fields]

        if not all((gt in ObservationQuery.VALID_GROUP_FIELDS) for gt in fields):
            raise ApiError("One or more invalid aggregation fields")

        self._aggregation = True
        self._aggregate_fields = fields
        return self

    def max_events_per_group(self, max_events_per_group):
        """
        Sets the max events per aggregate for aggregated results

        Args:
            max_events_per_group (int): Max events per aggregate
        """
        if not self._aggregation:
            raise ApiError("You should first aggregate the records.")
        self._max_events_per_group = max_events_per_group
        return self

    def rows(self, rows):
        """
        Sets the rows for aggregated results

        Args:
            rows (int): Max events per group
        """
        if not self._aggregation:
            raise ApiError("You should first aggregate the records.")
        self._rows = rows
        return self

    def start(self, start):
        """
        Sets the start for the aggregated results

        Args:
            start (int): start index
        """
        if not self._aggregation:
            raise ApiError("You should first aggregate the records.")
        self._start = start
        return self

    def range(self, duration, field, method="interval"):
        """
        Describes a time window to restrict the search.

        Args:
            duration (str): duration for the range e.g. -2w
            field (str): field
            method (str): either bucket or inteval
        """
        if not self._aggregation:
            raise ApiError("You should first aggregate the records.")
        self._range = dict(duration=duration, field=field, method=method)
        return self

    def _build_aggregated_body(self):
        """
        Helper to build the group results body:

        {
          "fields": ["string"],
          "max_events_per_group": integer,
          "range": {
            "duration": "string",
            "field": "string",
            "method": "string"
          },
          "rows": integer,
          "start": integer
        }
        """
        data = dict(fields=self._aggregate_fields)
        if self._max_events_per_group:
            data["max_events_per_group"] = self._max_events_per_group
        if self._range:
            data["ranges"] = self._range
        if self._rows:
            data["rows"] = self._rows
        if self._start:
            data["start"] = self._start
        return data

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
        query_parameters = {}
        result_url_template = "/api/investigate/v2/orgs/{}/observations/search_jobs/{}/results".format(
            self._cb.credentials.org_key,
            self._query_token
        )
        while still_fetching:
            if self._aggregation:
                result_url = "/api/investigate/v1/orgs/{}/observations/search_jobs/{}/group_results".format(
                    self._cb.credentials.org_key,
                    self._query_token,
                )
                result = self._cb.post_object(result_url, self._build_aggregated_body()).json()
                results = []
                for group in result["group_results"]:
                    results.extend(group["results"])
            else:
                result_url = '{}?start={}&rows={}'.format(
                    result_url_template,
                    current,
                    self._batch_size
                )
                result = self._cb.get_object(result_url, query_parameters=query_parameters)
                results = result.get('results', [])

            self._total_results = result.get('num_available', 0)
            self._count_valid = True

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
