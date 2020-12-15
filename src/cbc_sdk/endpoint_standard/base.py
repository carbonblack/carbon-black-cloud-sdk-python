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

"""Model and Query Classes for Endpoint Standard"""

from cbc_sdk.base import (MutableBaseModel, UnrefreshableModel, CreatableModelMixin, NewBaseModel, FacetQuery,
                          PaginatedQuery, QueryBuilder, QueryBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin)
from cbc_sdk.platform import PlatformQueryBase
from cbc_sdk.utils import convert_query_params
from cbc_sdk.errors import ApiError
from copy import deepcopy
import logging
import json
import time

from cbc_sdk.errors import ServerError

log = logging.getLogger(__name__)

"""Endpoint Standard Models"""


class EndpointStandardMutableModel(MutableBaseModel):
    """Represents Endpoint Standard objects."""
    _change_object_http_method = "PATCH"
    _change_object_key_name = None

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """Initialize an EndpointStandardMutableModel with model_unique_id and initial_data."""
        super(EndpointStandardMutableModel, self).__init__(cb, model_unique_id=model_unique_id,
                                                           initial_data=initial_data, force_init=force_init,
                                                           full_doc=full_doc)
        if not self._change_object_key_name:
            self._change_object_key_name = self.primary_key

    def _query_implementation(cls, cb, **kwargs):
        return Query(cls, cb, kwargs.get("query_string", None))

    def _parse(self, obj):
        if type(obj) == dict and self.info_key in obj:
            return obj[self.info_key]

    def _update_object(self):
        if self._change_object_http_method != "PATCH":
            return self._update_entire_object()
        else:
            return self._patch_object()

    def _update_entire_object(self):
        if self.__class__.primary_key in self._dirty_attributes.keys() or self._model_unique_id is None:
            new_object_info = deepcopy(self._info)
            try:
                if not self._new_object_needs_primary_key:
                    del (new_object_info[self.__class__.primary_key])
            except Exception:
                pass
            log.debug("Creating a new {0:s} object".format(self.__class__.__name__))
            ret = self._cb.api_json_request(self.__class__._new_object_http_method, self.urlobject,
                                            data={self.info_key: new_object_info})
        else:
            log.debug("Updating {0:s} with unique ID {1:s}".format(self.__class__.__name__, str(self._model_unique_id)))
            ret = self._cb.api_json_request(self.__class__._change_object_http_method,
                                            self._build_api_request_uri(), data={self.info_key: self._info})

        return self._refresh_if_needed(ret)

    def _patch_object(self):
        if self.__class__.primary_key in self._dirty_attributes.keys() or self._model_unique_id is None:
            log.debug("Creating a new {0:s} object".format(self.__class__.__name__))
            ret = self._cb.api_json_request(self.__class__._new_object_http_method, self.urlobject,
                                            data=self._info)
        else:
            updates = {}
            for k in self._dirty_attributes.keys():
                updates[k] = self._info[k]
            log.debug("Updating {0:s} with unique ID {1:s}".format(self.__class__.__name__, str(self._model_unique_id)))
            ret = self._cb.api_json_request(self.__class__._change_object_http_method,
                                            self._build_api_request_uri(), data=updates)

        return self._refresh_if_needed(ret)

    def _refresh_if_needed(self, request_ret):
        refresh_required = True

        if request_ret.status_code not in range(200, 300):
            try:
                message = json.loads(request_ret.text)[0]
            except Exception:
                message = request_ret.text

            raise ServerError(request_ret.status_code, message,
                              result="Did not update {} record.".format(self.__class__.__name__))
        else:
            message = request_ret.json()
            log.debug("Received response: %s" % message)
            if not isinstance(message, dict):
                raise ServerError(request_ret.status_code, message,
                                  result="Unknown error updating {0:s} record.".format(self.__class__.__name__))
            else:
                if message.get("success", False):
                    if isinstance(message.get(self.info_key, None), dict):
                        self._info = message.get(self.info_key)
                        self._full_init = True
                        refresh_required = False
                    else:
                        if self._change_object_key_name in message.keys():
                            # if all we got back was an ID, try refreshing to get the entire record.
                            log.debug("Only received an ID back from the server, forcing a refresh")
                            self._info[self.primary_key] = message[self._change_object_key_name]
                            refresh_required = True
                else:
                    # "success" is False
                    raise ServerError(request_ret.status_code, message.get("message", ""),
                                      result="Did not update {0:s} record.".format(self.__class__.__name__))

        self._dirty_attributes = {}
        if refresh_required:
            self.refresh()
        return self._model_unique_id


class Device(EndpointStandardMutableModel):
    """Represents an Endpoint Standard Device."""
    urlobject = "/integrationServices/v3/device"
    urlobject_single = "/integrationServices/v3/device/{}"
    primary_key = "deviceId"
    info_key = "deviceInfo"
    swagger_meta_file = "endpoint_standard/models/deviceInfo.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """Initialize a Device object with model_unique_id and initial_data."""
        super(Device, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            self._refresh()

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return Query(cls, cb, kwargs.get("query_string", None))

    def lr_session(self):
        """
        Retrieve a Live Response session object for this Device.

        Returns:
            LiveResponseSession: Live Response session object.

        Raises:
            ApiError: If there is an error establishing a Live Response session for this Device.
        """
        return self._cb._request_lr_session(self._model_unique_id)


class Event(NewBaseModel):
    """Represents an Endpoint Standard Event."""
    urlobject = "/integrationServices/v3/event"
    primary_key = "eventId"
    info_key = "eventInfo"

    def _parse(self, obj):
        if type(obj) == dict and self.info_key in obj:
            return obj[self.info_key]

    def __init__(self, cb, model_unique_id, initial_data=None):
        """Initialize an Event with model_unique_id and initial_data."""
        super(Event, self).__init__(cb, model_unique_id, initial_data)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return Query(cls, cb, kwargs.get("query_string", None))


class Policy(EndpointStandardMutableModel, CreatableModelMixin):
    """Represents an Endpoint Standard Policy."""
    urlobject = "/integrationServices/v3/policy"
    info_key = "policyInfo"
    swagger_meta_file = "endpoint_standard/models/policyInfo.yaml"
    _change_object_http_method = "PUT"
    _change_object_key_name = "policyId"

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return Query(cls, cb, kwargs.get("query_string", None))

    @property
    def rules(self):
        """Returns a dictionary of rules and rule IDs for this Policy."""
        return dict([(r.get("id"), r) for r in self.policy.get("rules", [])])

    def add_rule(self, new_rule):
        """Adds a rule to this Policy.

        Arguments:
            new_rule (dict(str,str)): The new rule to add to this Policy.

        Notes:
            - The new rule must conform to this dictionary format:

                {"action": "ACTION",
                "application": {"type": "TYPE", "value": "VALUE"},
                "operation": "OPERATION",
                "required": "REQUIRED"}

            - The dictionary keys have these possible values:

                "action": ["IGNORE", "ALLOW", "DENY", "TERMINATE_PROCESS",
                           "TERMINATE_THREAD", "TERMINATE"]
                "type": ["NAME_PATH", "SIGNED_BY", "REPUTATION"]
                "value": Any string value to match on
                "operation": ["BYPASS_ALL", "INVOKE_SCRIPT", "INVOKE_SYSAPP",
                              "POL_INVOKE_NOT_TRUSTED", "INVOKE_CMD_INTERPRETER",
                              "RANSOM", "NETWORK", "PROCESS_ISOLATION", "CODE_INJECTION",
                              "MEMORY_SCRAPE", "RUN_INMEMORY_CODE", "ESCALATE", "RUN"]
                "required": [True, False]
        """
        self._cb.post_object("{0}/rule".format(self._build_api_request_uri()), {"ruleInfo": new_rule})
        self.refresh()

    def delete_rule(self, rule_id):
        """Deletes a rule from this Policy."""
        self._cb.delete_object("{0}/rule/{1}".format(self._build_api_request_uri(), rule_id))
        self.refresh()

    def replace_rule(self, rule_id, new_rule):
        """Replaces a rule in this policy."""
        self._cb.put_object("{0}/rule/{1}".format(self._build_api_request_uri(), rule_id),
                            {"ruleInfo": new_rule})
        self.refresh()


class EnrichedEvent(UnrefreshableModel):
    """Represents an enriched event retrieved by one of the Enterprise EDR endpoints."""
    default_sort = 'device_timestamp'
    primary_key = "event_id"

    @classmethod
    def _query_implementation(self, cb, **kwargs):
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
        self._details_timeout = 0
        self._info = None
        super(EnrichedEvent, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                            force_init=force_init, full_doc=full_doc)

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
        if not self.event_id:
            raise ApiError("Trying to get event details on an invalid event_id")
        if async_mode:
            return self._cb._async_submit(lambda arg, kwarg: self._get_detailed_results()._info)
        else:
            return self._get_detailed_results()._info

    def _get_detailed_results(self):
        """Actual search details implementation"""
        args = {"event_ids": [self.event_id]}
        url = "/api/investigate/v2/orgs/{}/enriched_events/detail_jobs".format(self._cb.credentials.org_key)
        query_start = self._cb.post_object(url, body=args)
        job_id = query_start.json().get("job_id")
        timed_out = False
        submit_time = time.time() * 1000

        while True:
            status_url = "/api/investigate/v2/orgs/{}/enriched_events/detail_jobs/{}".format(
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
        result_url = "/api/investigate/v2/orgs/{}/enriched_events/detail_jobs/{}/results".format(
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


class Query(PaginatedQuery, PlatformQueryBase, QueryBuilderSupportMixin, IterableQueryMixin):
    """Represents a prepared query to the Cb Endpoint Standard server.

    This object is returned as part of a `CBCloudAPI.select`
    operation on models requested from the Cb Endpoint Standard server.
    You should not have to create this class yourself.

    The query is not executed on the server until it's accessed, either as an iterator (where it will generate values
    on demand as they're requested) or as a list (where it will retrieve the entire result set and save to a list).
    You can also call the Python built-in `len() on this object to retrieve the total number of items matching
    the query.

    Example:
    >>> from cbc_sdk import CBCloudAPI
    >>> cb = CBCloudAPI()

    Notes:
        - The slicing operator only supports start and end parameters, but not step. ``[1:-1]`` is legal, but
          ``[1:2:-1]`` is not.
        - You can chain where clauses together to create AND queries; only objects that match all ``where`` clauses
          will be returned.
          - Device Queries with multiple search parameters only support AND operations, not OR. Use of
          Query.or_(myParameter='myValue') will add 'AND myParameter:myValue' to the search query.
    """

    def __init__(self, doc_class, cb, query=None):
        """Initialize a Query object."""
        super(Query, self).__init__(doc_class, cb, query)

        # max batch_size is 5000
        self._batch_size = 100
        if query is not None:
            # copy existing .where(), and_() queries
            self._query_builder = QueryBuilder()
            self._query_builder._query = query._query_builder._query
        else:
            self._query_builder = QueryBuilder()

    def _clone(self):
        nq = self.__class__(self._doc_class, self._cb, query=self)
        nq._batch_size = self._batch_size
        return nq

    def or_(self, **kwargs):
        """Unsupported. Will raise if called.

        Raises:
            ApiError: .or_() cannot be called on Endpoint Standard queries.
        """
        raise ApiError(".or_() cannot be called on Endpoint Standard queries.")

    def prepare_query(self, args):
        """Adds query parameters that are part of a `select().where()` clause to the request."""
        request = args
        params = self._query_builder._collapse()
        if params is not None:
            for query in params.split(' '):
                try:
                    # convert from str('key:value') to dict{'key': 'value'}
                    key, value = query.split(':', 1)
                    # must remove leading or trailing parentheses that were inserted by logical combinations
                    key = key.strip('(').strip(')')
                    value = value.strip('(').strip(')')
                    request[key] = value
                except ValueError:
                    # AND or OR encountered
                    pass
        return request

    def _count(self):
        if self._count_valid:
            return self._total_results

        args = {}
        args = self.prepare_query(args)

        query_args = convert_query_params(args)
        self._total_results = int(self._cb.get_object(self._doc_class.urlobject, query_parameters=query_args)
                                  .get("totalResults", 0))
        self._count_valid = True
        return self._total_results

    def _search(self, start=0, rows=0):
        # iterate over total result set, in batches of self._batch_size at a time
        # defaults to 100 results each call
        args = {}
        if start != 0:
            args['start'] = start
        args['rows'] = self._batch_size

        current = start
        numrows = 0

        args = self.prepare_query(args)
        still_querying = True

        while still_querying:
            query_args = convert_query_params(args)
            result = self._cb.get_object(self._doc_class.urlobject, query_parameters=query_args)

            self._total_results = result.get("totalResults", 0)
            self._count_valid = True

            results = result.get('results', [])

            if results is None:
                log.debug("Results are None")
                if current >= 100000:
                    log.info("Max result size exceeded. Truncated to 100k.")
                break

            for item in results:
                yield item
                current += 1
                numrows += 1
                if rows and numrows == rows:
                    still_querying = False
                    break
            # as of 6/2017, the indexing on the Cb Endpoint Standard backend is still 1-based
            args['start'] = current + 1

            if current >= self._total_results:
                break

            if not results:
                log.debug("server reported total_results overestimated the number of results for this query by {0}"
                          .format(self._total_results - current))
                log.debug("resetting total_results for this query to {0}".format(current))
                self._total_results = current
                break


class EnrichedEventQuery(Query, AsyncQueryMixin):
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
        self._sort_by = None
        self._group_by = None
        self._rows = 500
        self._default_args = {}
        self._default_args["rows"] = self._rows
        self._query_token = None
        self._timeout = 0
        self._timed_out = False
        self._sort = []
        self._time_range = {}
        self._aggregation = False
        self._aggregation_field = None

    def or_(self, **kwargs):
        """
        or_ criteria are explicitly provided to EnrichedEvent queries although they are endpoint_standard.

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

    def _get_query_parameters(self):
        """Need to override base class implementation as it sets custom (invalid) fields"""
        args = self._default_args.copy()
        args['query'] = self._query_builder._collapse()
        if self._time_range:
            args["time_range"] = self._time_range

        return args

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

        self._rows = rows
        self._default_args["rows"] = self._rows
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
            - `window` will take precedence over `start` and `end` if provided.

        Examples:
            query = api.select(EnrichedEvent).set_time_range(start="2020-10-20T20:34:07Z")
            second_query = api.select(EnrichedEvent).set_time_range(start="2020-10-20T20:34:07Z",
                end="2020-10-30T20:34:07Z")
            third_query = api.select(EnrichedEvent).set_time_range(window='-3d')
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

    def sort_by(self, key, direction="ASC"):
        """Sets the sorting behavior on a query's results.

        Arguments:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            Query (EnrichedEventQuery: The query with sorting parameters.

        Example:
        >>> cb.select(EnrichedEvent).where(process_name="cmd.exe").sort_by("device_timestamp")
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
        """Sets the timeout on a event query.

        Arguments:
            msecs (int): Timeout duration, in milliseconds.

        Returns:
            Query (EnrichedEventQuery): The Query object with new milliseconds
                parameter.

        Example:
        >>> cb.select(EnrichedEvent).where(process_name="foo.exe").timeout(5000)
        """
        self._timeout = msecs
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
        if not self._query_token:
            self._submit()

        if self._aggregation:
            return False

        status_url = "/api/investigate/v1/orgs/{}/enriched_events/search_jobs/{}".format(
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

    def _run_async_query(self, context):
        """Executed in the background to run an asynchronous query.

        Args:
            context (object): The context (query token) returned by _init_async_query.

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        return list(self._search())
