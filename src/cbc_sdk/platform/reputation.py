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

"""Model and Query Classes for Reputation"""

from cbc_sdk.errors import ApiError, ServerError
from cbc_sdk.platform import PlatformModel
from cbc_sdk.base import (BaseQuery, QueryBuilder, QueryBuilderSupportMixin,
                          IterableQueryMixin, AsyncQueryMixin)

import time
import json

""""Reputation Override Models"""


class ReputationOverride(PlatformModel):
    """Represents a reputation override."""
    urlobject = "/appservices/v6/orgs/{0}/reputations/overrides"
    urlobject_single = "/appservices/v6/orgs/{0}/reputations/overrides/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/reputation_override.yaml"
    _is_deleted = False

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the ReputationOverride object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the alert represented.
            initial_data (dict): Initial data used to populate the alert.
        """
        super(ReputationOverride, self).__init__(cb, model_unique_id, initial_data, full_doc=True)
        if model_unique_id is not None and initial_data is None:
            self._refresh()

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the ReputationOverride.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            ReputationOverrideQuery: The query object for this alert type.
        """
        return ReputationOverrideQuery(cls, cb)

    def _refresh(self):
        """
        Rereads the device data from the server.

        Returns:
            bool: True if refresh was successful, False if not.
        """
        if self._is_deleted:
            raise ApiError("Cannot refresh a deleted ReputationOverride")
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._last_refresh_time = time.time()
        self._full_init = True
        return True

    def delete(self):
        """Delete this object."""
        if self._model_unique_id is None:
            return

        resp = self._cb.delete_object(self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id))
        if resp.status_code not in (200, 204):
            try:
                message = json.loads(resp.text)[0]
            except Exception:
                message = resp.text
            raise ServerError(resp.status_code, message, result="Did not delete {0:s}.".format(str(self)))
        self._is_deleted = True

    @classmethod
    def create(cls, cb, initial_data):
        """
        Returns all vendors and products that have been seen for the organization.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            initial_data (Object): The initial data for a ReputationOverride

        Example:
            {
                "description": "Banned as known malware",
                "override_list": "BLACK_LIST",
                "override_type": "SHA256",
                "sha256_hash": "dd191a5b23df92e13a8852291f9fb5ed594b76a28a5a464418442584afd1e048",
                "filename": "foo.exe"
            }

        Returns:
            ReputationOverride: The created ReputationOverride object based on the specified properties

        """
        resp = cb.post_object(cls.urlobject.format(cb.credentials.org_key), body=initial_data)
        resp_json = resp.json()
        return cls(cb, resp_json["id"], resp_json)

    @classmethod
    def bulk_delete(cls, cb, overrides):
        """
        Deletes reputation overrides in bulk by id.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            overrides (List): List if reputation override ids

        Example:
            [
                "e9410b754ea011ebbfd0db2585a41b07"
            ]

        """
        resp = cb.post_object(cls.urlobject.format(cb.credentials.org_key) + "/_delete", overrides)
        if resp.status_code not in (200, 204):
            try:
                message = json.loads(resp.text)[0]
            except Exception:
                message = resp.text
            raise ServerError(resp.status_code, message, result="Did not delete overrides.")

        return resp.json()


class ReputationOverrideQuery(BaseQuery, QueryBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin):
    """Represents a query that is used to locate ReputationOverride objects."""
    VALID_DIRECTIONS = ["ASC", "DESC", "asc", "desc"]

    def __init__(self, doc_class, cb):
        """
        Initialize the ReputationOverrideQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(ReputationOverrideQuery, self).__init__()

        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._sortcriteria = {}

    def set_override_list(self, override_list):
        """Sets the override_list criteria filter.

        Arguments:
            override_list (str): Override List to filter on.

        Returns:
            The ReputationOverrideQuery with specified override_list.
        """
        if not isinstance(override_list, str) and override_list in ["WHITE_LIST", "BLACK_LIST"]:
            raise ApiError("Invalid override_list must be one of WHITE_LIST, BLACK_LIST")
        self._criteria["override_list"] = override_list
        return self

    def set_override_type(self, override_type):
        """Sets the override_type criteria filter.

        Arguments:
            override_type (str): Override List to filter on.

        Returns:
            The ReputationOverrideQuery with specified override_type.
        """
        if not isinstance(override_type, str) and override_type in ["SHA256", "CERT", "IT_TOOL"]:
            raise ApiError("Invalid override_type must be one of SHA256, CERT, IT_TOOL")
        self._criteria["override_type"] = override_type
        return self

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Example:
            >>> cb.select(ReputationOverride).sort_by("create_time")

        Args:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            ReputationOverrideQuery: This instance.

        Raises:
            ApiError: If an invalid direction value is passed.
        """
        if direction not in ReputationOverrideQuery.VALID_DIRECTIONS:
            raise ApiError("invalid sort direction specified")
        self._sortcriteria = {"sort_field": key, "sort_order": direction}
        return self

    def _build_request(self, from_row, max_rows):
        """
        Creates the request body for an API call.

        Args:
            from_row (int): The row to start the query at.
            max_rows (int): The maximum number of rows to be returned.

        Returns:
            dict: The complete request body.
        """
        request = {
            "criteria": self._criteria,
            "query": self._query_builder._collapse()
        }
        if from_row > 0:
            request["start"] = from_row
        if max_rows >= 0:
            request["rows"] = max_rows
        if self._sortcriteria != {}:
            request.update(self._sortcriteria)
        return request

    def _build_url(self, tail_end):
        """
        Creates the URL to be used for an API call.

        Args:
            tail_end (str): String to be appended to the end of the generated URL.

        Returns:
            str: The complete URL.
        """
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key) + tail_end
        return url

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Returns:
            int: The number of results from the run of this query.
        """
        if self._count_valid:
            return self._total_results

        url = self._build_url("/_search")
        request = self._build_request(0, -1)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()

        self._total_results = result["num_found"]
        self._count_valid = True

        return self._total_results

    def _perform_query(self, from_row=0, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): The row to start the query at (default 0).
            max_rows (int): The maximum number of rows to be returned (default -1, meaning "all").

        Returns:
            Iterable: The iterated query.
        """
        url = self._build_url("/_search")
        current = from_row
        numrows = 0
        still_querying = True
        while still_querying:
            request = self._build_request(current, max_rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, item["id"], item)
                current += 1
                numrows += 1

                if max_rows > 0 and numrows == max_rows:
                    still_querying = False
                    break

            if current >= self._total_results:
                break

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Args:
            context (object): Not used, always None.

        Returns:
            list: Result of the async query, which is then returned by the future.
        """
        url = self._build_url("/_search")
        request = self._build_request(0, -1)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        self._total_results = result["num_found"]
        self._count_valid = True
        results = result.get("results", [])
        return [self._doc_class(self._cb, item["id"], item) for item in results]
