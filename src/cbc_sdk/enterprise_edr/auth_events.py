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

"""Model and Query Classes for Auth Events"""

from cbc_sdk.base import UnrefreshableModel, NewBaseModel, FacetQuery
from cbc_sdk.base import Query
from cbc_sdk.errors import ApiError, TimeoutError, InvalidObjectError

import logging
import time
from copy import deepcopy

log = logging.getLogger(__name__)


class AuthEvent(NewBaseModel):
    """Represents an AuthEvent"""

    primary_key = "event_id"
    validation_url = "/api/investigate/v2/orgs/{}/auth_events/search_validation"
    swagger_meta_file = "enterprise_edr/models/auth_events.yaml"

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the AuthEvent object.

        Required RBAC Permissions:
            org.search.events (CREATE, READ)

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (Any): The unique ID for this particular instance of the model object.
            initial_data (dict): The data to use when initializing the model object.
            force_init (bool): True to force object initialization.
            full_doc (bool): False to mark the object as not fully initialized.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> events = cb.select(AuthEvent).where("auth_username:SYSTEM")
            >>> print(*events)
        """
        self._details_timeout = cb.credentials.default_timeout
        self._info = None
        if model_unique_id is not None and initial_data is None:
            auth_events_future = (
                cb.select(AuthEvent)
                .where(event_id=model_unique_id)
                .execute_async()
            )
            result = auth_events_future.result()
            if len(result) == 1:
                initial_data = result[0]
        super(AuthEvent, self).__init__(
            cb,
            model_unique_id=model_unique_id,
            initial_data=initial_data,
            force_init=force_init,
            full_doc=full_doc,
        )

    def _refresh(self):
        """
        Refreshes the AuthEvent object from the server by getting the details.

        Required RBAC Permissions:
            org.search.events (READ)

        Returns:
            True if the refresh was successful.
        """
        self._get_detailed_results()
        return True

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        """
        Returns the appropriate query object for this object type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            Query: The query object for this Auth Event.
        """
        return AuthEventQuery(self, cb)

    def get_details(self, timeout=0, async_mode=False):
        """Requests detailed results.

        Args:
            timeout (int): AuthEvent details request timeout in milliseconds.  This can never be greater than the
                configured default timeout.  If this is 0, the configured default timeout is used.
            async_mode (bool): True to request details in an asynchronous manner.

        Returns:
            AuthEvent: Auth Events object enriched with the details fields

        Note:
            - When using asynchronous mode, this method returns a python future.
              You can call result() on the future object to wait for completion and get the results.

        Examples:
            >>> cb = CBCloudAPI(profile="example_profile")

            >>> events = cb.select(AuthEvent).where(process_pid=2000)
            >>> print(events[0].get_details())
        """
        if timeout <= 0 or timeout > self._cb.credentials.default_timeout:
            self._details_timeout = self._cb.credentials.default_timeout
        else:
            self._details_timeout = timeout
        if not self.event_id:
            raise ApiError(
                "Trying to get auth_event details on an invalid auth_event_id"
            )
        if async_mode:
            return self._cb._async_submit(
                lambda arg, kwarg: self._get_detailed_results()
            )
        return self._get_detailed_results()

    def _get_detailed_results(self):
        """Actual get details implementation"""
        obj = AuthEvent._helper_get_details(
            self._cb,
            event_ids=[self.event_id],
            timeout=self._details_timeout,
        )
        if obj:
            self._info = deepcopy(obj._info)
        return self

    @staticmethod
    def _helper_get_details(cb, alert_id=None, event_ids=None, bulk=False, timeout=0):
        """
        Helper to get auth_event details

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            alert_id (str):  An alert id to fetch associated auth_events
            event_ids (list): A list of auth_event ids to fetch
            bulk (bool): Whether it is a bulk request
            timeout (int): AuthEvents details request timeout in milliseconds.  This can never be greater than the
                configured default timeout.  If this value is 0, the configured default timeout is used.

        Returns:
            AuthEvent or list(AuthEvent): if it is a bulk operation a list, otherwise AuthEvent

        Raises:
            ApiError: if cb is not instance of CBCloudAPI
        """
        if timeout <= 0 or timeout > cb.credentials.default_timeout:
            timeout = cb.credentials.default_timeout
        if cb.__class__.__name__ != "CBCloudAPI":
            raise ApiError("cb argument should be instance of CBCloudAPI.")
        if (alert_id and event_ids) or not (alert_id or event_ids):
            raise ApiError("Either alert_id or event_ids should be provided.")
        elif alert_id:
            args = {"alert_id": alert_id}
        else:
            args = {"event_ids": event_ids}
        url = "/api/investigate/v2/orgs/{}/auth_events/detail_jobs".format(cb.credentials.org_key)
        query_start = cb.post_object(url, body=args)
        job_id = query_start.json().get("job_id")
        timed_out = False
        submit_time = time.time() * 1000

        while True:
            result_url = "/api/investigate/v2/orgs/{}/auth_events/detail_jobs/{}/results".format(
                cb.credentials.org_key,
                job_id,
            )
            result = cb.get_object(result_url)
            contacted = result.get("contacted", 0)
            completed = result.get("completed", 0)
            log.debug("contacted = {}, completed = {}".format(contacted, completed))

            if contacted == 0 or completed < contacted:
                if (time.time() * 1000) - submit_time > timeout:
                    timed_out = True
                    break
            else:
                total_results = result.get("num_available", 0)
                found_results = result.get("num_found", 0)
                # if found is 0, then no auth_events were found
                if found_results == 0:
                    return None
                if total_results != 0:
                    results = result.get("results", [])
                    if bulk:
                        return [AuthEvent(cb, initial_data=x) for x in results]
                    return AuthEvent(cb, initial_data=results[0])

            time.sleep(0.5)

        if timed_out:
            raise TimeoutError(
                message="user-specified timeout exceeded while waiting for results"
            )

    @staticmethod
    def get_auth_events_descriptions(cb):
        """
        Returns descriptions and status messages of Auth Events.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.

        Returns:
            dict: Descriptions and status messages of Auth Events as dict objects.

        Raises:
             ApiError: if cb is not instance of CBCloudAPI

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> descriptions = AuthEvent.get_auth_events_descriptions(cb)
            >>> print(descriptions)
        """
        if cb.__class__.__name__ != "CBCloudAPI":
            message = "cb argument should be instance of CBCloudAPI."
            message += "\nExample:\ncb = CBCloudAPI(profile='example_profile')"
            message += "\ndescriptions = AuthEvent.get_auth_events_descriptions(cb)"
            raise ApiError(message)

        url = "/api/investigate/v2/orgs/{}/auth_events/descriptions".format(cb.credentials.org_key)

        return cb.get_object(url)

    @staticmethod
    def search_suggestions(cb, query, count=None):
        """
        Returns suggestions for keys and field values that can be used in a search.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            query (str): A search query to use.
            count (int): (optional) Number of suggestions to be returned

        Returns:
            list: A list of search suggestions expressed as dict objects.

        Raises:
             ApiError: if cb is not instance of CBCloudAPI

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> suggestions = AuthEvent.search_suggestions(cb, 'auth')
            >>> print(suggestions)
        """
        if cb.__class__.__name__ != "CBCloudAPI":
            message = "cb argument should be instance of CBCloudAPI."
            message += "\nExample:\ncb = CBCloudAPI(profile='example_profile')"
            message += "\nsuggestions = AuthEvent.search_suggestions(cb, 'example-value')"
            raise ApiError(message)

        query_params = {"suggest.q": query}
        if count:
            query_params["suggest.count"] = count
        url = "/api/investigate/v2/orgs/{}/auth_events/search_suggestions".format(cb.credentials.org_key)
        output = cb.get_object(url, query_params)
        return output["suggestions"]

    @staticmethod
    def bulk_get_details(cb, alert_id=None, event_ids=None, timeout=0):
        """Bulk get details

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            alert_id (str):  An alert id to fetch associated events
            event_ids (list): A list of event ids to fetch
            timeout (int): AuthEvent details request timeout in milliseconds.  This can never be greater than the
                configured default timeout.  If this value is 0, the configured default timeout is used.

        Returns:
            list: list of Auth Events

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> bulk_details = AuthEvent.bulk_get_details(cb, event_ids=['example-value'])
            >>> print(bulk_details)

        Raises:
            ApiError: if cb is not instance of CBCloudAPI
        """
        if cb.__class__.__name__ != "CBCloudAPI":
            message = "cb argument should be instance of CBCloudAPI."
            message += "\nExample:\ncb = CBCloudAPI(profile='example_profile')"
            message += "\nvalidation = AuthEvent.bulk_get_details(cb, alert_id='example-value')"
            raise ApiError(message)
        return AuthEvent._helper_get_details(
            cb,
            alert_id=alert_id,
            event_ids=event_ids,
            bulk=True,
            timeout=timeout
        )


class AuthEventFacet(UnrefreshableModel):
    """
    Represents an AuthEvent facet retrieved.

    Example:
        >>> cb = CBCloudAPI(profile="example_profile")
        >>> events_facet = cb.select(AuthEventFacet).where("auth_username:SYSTEM").add_facet_field("process_name")
        >>> print(events_facet.results)
    """

    primary_key = "job_id"
    swagger_meta_file = "enterprise_edr/models/auth_events_facet.yaml"
    submit_url = "/api/investigate/v2/orgs/{}/auth_events/facet_jobs"
    result_url = "/api/investigate/v2/orgs/{}/auth_events/facet_jobs/{}/results"

    class Terms(UnrefreshableModel):
        """Represents the facet fields and values associated with an AuthEvent Facet query."""

        def __init__(self, cb, initial_data):
            """Initialize an AuthEventFacet Terms object with initial_data."""
            super(AuthEventFacet.Terms, self).__init__(
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
        """Represents the range (bucketed) facet fields and values associated with an AuthEvent Facet query."""

        def __init__(self, cb, initial_data):
            """Initialize an AuthEventFacet Ranges object with initial_data."""
            super(AuthEventFacet.Ranges, self).__init__(
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
            """Returns the reified `AuthEventFacet.Terms._facets` for this result."""
            return self._facets

        @property
        def fields(self):
            """Returns the ranges fields for this result."""
            return [field for field in self._facets]

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        # This will emulate a synchronous auth_event facet query, for now.
        return FacetQuery(self, cb)

    def __init__(self, cb, model_unique_id, initial_data):
        """Initialize the Terms object with initial data."""
        super(AuthEventFacet, self).__init__(
            cb,
            model_unique_id=model_unique_id,
            initial_data=initial_data,
            force_init=False,
            full_doc=True,
        )
        self._terms = AuthEventFacet.Terms(cb, initial_data=initial_data["terms"])
        self._ranges = AuthEventFacet.Ranges(cb, initial_data=initial_data["ranges"])

    @property
    def terms_(self):
        """Returns the reified `AuthEventFacet.Terms` for this result."""
        return self._terms

    @property
    def ranges_(self):
        """Returns the reified `AuthEventFacet.Ranges` for this result."""
        return self._ranges


class AuthEventGroup:
    """Represents AuthEventGroup"""
    def __init__(self, cb, initial_data=None):
        """
        Initialize AuthEventGroup object

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            initial_data (dict): The data to use when initializing the model object.

        Notes:
            The constructed object will have the following data:
            - group_start_timestamp
            - group_end_timestamp
            - group_key
            - group_value
        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> groups = set(cb.select(AuthEvent).where(process_pid=2000).group_results("device_name"))
            >>> for group in groups:
            >>>     print(group._info)
        """
        if not initial_data:
            raise InvalidObjectError("Cannot create object without initial data")
        self._info = initial_data
        self._cb = cb
        self.auth_events = [AuthEvent(cb, initial_data=x) for x in initial_data.get("results", [])]

    def __getattr__(self, item):
        """
        Return an attribute of this object.

        Args:
            item (str): Name of the attribute to be returned.

        Returns:
            Any: The returned attribute value.

        Raises:
            AttributeError: If the object has no such attribute.
        """
        try:
            super(AuthEventGroup, self).__getattribute__(item)
        except AttributeError:
            pass  # fall through to the rest of the logic...

        # try looking up via self._info, if we already have it.
        if item in self._info:
            return self._info[item]
        raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                          item))

    def __getitem__(self, item):
        """
        Return an attribute of this object.

        Args:
            item (str): Name of the attribute to be returned.

        Returns:
            Any: The returned attribute value.

        Raises:
            AttributeError: If the object has no such attribute.
        """
        try:
            super(AuthEventGroup, self).__getattribute__(item)
        except AttributeError:
            pass  # fall through to the rest of the logic...

        # try looking up via self._info, if we already have it.
        if item in self._info:
            return self._info[item]
        raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                          item))


class AuthEventQuery(Query):
    """Represents the query logic for an AuthEvent query.

    This class specializes `Query` to handle the particulars of Auth Events querying.
    """

    VALID_GROUP_FIELDS = (
        "auth_domain_name", "auth_event_action", "auth_remote_port",
        "auth_username", "backend_timestamp", "childproc_count",
        "crossproc_count", "device_group_id", "device_id",
        "device_name", "device_policy_id", "device_timestamp",
        "event_id", "filemod_count", "ingress_time",
        "modload_count", "netconn_count", "org_id",
        "parent_guid", "parent_pid", "process_guid",
        "process_hash", "process_name", "process_pid",
        "process_username", "regmod_count", "scriptload_count",
        "windows_event_id"
    )

    def __init__(self, doc_class, cb):
        """
        Initialize the AuthEventQuery object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> events = cb.select(AuthEvent).where("auth_username:SYSTEM")
            >>> print(*events)
        """
        super(AuthEventQuery, self).__init__(doc_class, cb)
        self._default_args["rows"] = self._batch_size
        self._query_token = None
        self._timeout = cb.credentials.default_timeout
        self._timed_out = False

    def or_(self, **kwargs):
        """
        :meth:`or_` criteria are explicitly provided to AuthEvent queries.

        This method overrides the base class in order to provide or_() functionality rather than raising an exception.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> events = cb.select(AuthEvent).where(process_name="chrome.exe").or_(process_name="firefox.exe")
            >>> print(*events)
        """
        self._query_builder.or_(None, **kwargs)
        return self

    def set_rows(self, rows):
        """
        Sets the 'rows' query body parameter to the 'start search' API call, determining how many rows to request.

        Args:
            rows (int): How many rows to request.

        Returns:
            Query: AuthEventQuery object

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> events = cb.select(AuthEvent).where(process_name="chrome.exe").set_rows(5)
            >>> print(*events)
        """
        if not isinstance(rows, int):
            raise ApiError(f"Rows must be an integer. {rows} is a {type(rows)}.")
        if rows > 10000:
            raise ApiError("Maximum allowed value for rows is 10000")
        super(AuthEventQuery, self).set_rows(rows)
        return self

    def timeout(self, msecs):
        """Sets the timeout on a Auth Event query.

        Arguments:
            msecs (int): Timeout duration, in milliseconds.  This value can never be greater than the configured
                default timeout.  If this value is 0, the configured default timeout is used.

        Returns:
            Query (AuthEventQuery): The Query object with new milliseconds parameter.

        Example:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> events = cb.select(AuthEvent).where(process_name="chrome.exe").timeout(5000)
            >>> print(*events)
        """
        if msecs <= 0:
            self._timeout = self._cb.credentials.default_timeout
        else:
            self._timeout = min(msecs, self._cb.credentials.default_timeout)
        return self

    def _submit(self):
        """Submit the search job"""
        if self._query_token:
            raise ApiError(
                "Query already submitted: token {0}".format(self._query_token)
            )

        args = self._get_query_parameters()
        self._validate({"q": args.get("query", "")})
        url = "/api/investigate/v2/orgs/{}/auth_events/search_jobs".format(
            self._cb.credentials.org_key
        )
        query_start = self._cb.post_object(url, body=args)
        self._query_token = query_start.json().get("job_id")
        self._timed_out = False
        self._submit_time = time.time() * 1000

    def _still_querying(self):
        """Check whether there are still records to be collected."""
        assert self._timeout > 0
        if not self._query_token:
            self._submit()

        results_url = (
            "/api/investigate/v2/orgs/{}/auth_events/search_jobs/{}/results".format(
                self._cb.credentials.org_key,
                self._query_token,
            )
        )
        result = self._cb.get_object(results_url)
        contacted = result.get("contacted", 0)
        completed = result.get("completed", 0)
        log.debug("contacted = {}, completed = {}".format(contacted, completed))

        if contacted == 0 or completed < contacted:
            if (time.time() * 1000) - self._submit_time > self._timeout:
                self._timed_out = True
                return False
            return True

        return False

    def _count(self):
        """Returns the number of records."""
        if self._count_valid:
            return self._total_results

        while self._still_querying():
            time.sleep(0.5)

        if self._timed_out:
            raise TimeoutError(
                message="user-specified timeout exceeded while waiting for results"
            )

        result_url = (
            "/api/investigate/v2/orgs/{}/auth_events/search_jobs/{}/results".format(
                self._cb.credentials.org_key,
                self._query_token,
            )
        )
        result = self._cb.get_object(result_url)

        self._total_results = result.get("num_available", 0)
        self._count_valid = True

        return self._total_results

    def _search(self, start=0, rows=0):
        """Start a search job and get the results."""
        if not self._query_token:
            self._submit()

        while self._still_querying():
            time.sleep(0.5)

        if self._timed_out:
            raise TimeoutError(
                message="user-specified timeout exceeded while waiting for results"
            )

        log.debug("Pulling results, timed_out={}".format(self._timed_out))

        current = start
        rows_fetched = 0
        still_fetching = True
        query_parameters = {}
        result_url_template = (
            "/api/investigate/v2/orgs/{}/auth_events/search_jobs/{}/results".format(
                self._cb.credentials.org_key, self._query_token
            )
        )

        while still_fetching:
            result_url = "{}?start={}&rows={}".format(
                result_url_template, current, self._batch_size
            )
            result = self._cb.get_object(result_url, query_parameters=query_parameters)
            results = result.get("results", [])

            self._total_results = result.get("num_available", 0)
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

    def group_results(
        self,
        fields,
        max_events_per_group=None,
        rows=500,
        start=None,
        range_duration=None,
        range_field=None,
        range_method=None
    ):
        """
        Get group results grouped by provided fields.

        Args:
            fields (str / list): field or fields by which to perform the grouping
            max_events_per_group (int): Maximum number of events in a group, if not provided all events will be returned
            rows (int): Number of rows to request, can be paginated
            start (int): First row to use for pagination
            ranges (dict): dict with information about duration, field, method

        Returns:
            dict: grouped results

        Examples:
            >>> cb = CBCloudAPI(profile="example_profile")
            >>> groups = set(cb.select(AuthEvent).where(process_pid=2000).group_results("device_name"))
            >>> for group in groups:
            >>>     print(group._info)
        """
        if not isinstance(fields, list) and not isinstance(fields, str):
            raise ApiError("Fields should be either a single field or list of fields")

        if isinstance(fields, str):
            fields = [fields]

        if not all((gf in AuthEventQuery.VALID_GROUP_FIELDS) for gf in fields):
            raise ApiError("One or more invalid aggregation fields")

        if not self._query_token:
            self._submit()

        result_url = "/api/investigate/v2/orgs/{}/auth_events/search_jobs/{}/group_results".format(
            self._cb.credentials.org_key,
            self._query_token,
        )

        # construct the group results body, required ones are fields and rows
        data = dict(fields=fields, rows=rows)
        if max_events_per_group is not None:
            data["max_events_per_group"] = max_events_per_group
        if range_duration or range_field or range_method:
            data["range"] = {}
            if range_method:
                data["range"]["method"] = range_method
            if range_duration:
                data["range"]["duration"] = range_duration
            if range_field:
                data["range"]["field"] = range_field
        if start is not None:
            data["start"] = start

        still_fetching = True
        while still_fetching:
            result = self._cb.post_object(result_url, data).json()
            contacted = result.get("contacted", 0)
            completed = result.get("completed", 0)
            if contacted < completed:
                time.sleep(0.5)
                continue
            still_fetching = False

        for group in result.get("group_results", []):
            yield AuthEventGroup(self._cb, initial_data=group)
