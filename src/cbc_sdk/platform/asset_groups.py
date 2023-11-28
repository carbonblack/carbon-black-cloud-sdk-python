#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020-2022. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""
The model and query classes for referencing asset groups.

An *asset group* represents a group of devices (endpoints, VM workloads, and/or VDIs) that can have a single policy
applied to it so the protections of all similar assets are synchronized with one another.  Policies carry a "position"
value as one of their attributes, so that, between the policy attached directly to the device, and the policies
attached to any asset groups the device is a member of, the one with the highest "position" is the one that applies to
that device.  Devices may be added to an asset group either explicitly, or implicitly by specifying a query on the
asset group, such that all devices matching that search criteria are considered part of the asset group.

Typical usage example::

    # assume "cb" is an instance of CBCloudAPI
    query = cb.select(AssetGroup).where('name:"HQ Devices"')
    group = query.first()
"""

from cbc_sdk.base import (MutableBaseModel, BaseQuery, QueryBuilder, QueryBuilderSupportMixin, IterableQueryMixin,
                          CriteriaBuilderSupportMixin, AsyncQueryMixin)
from cbc_sdk.errors import ApiError
from cbc_sdk.platform.devices import DeviceSearchQuery


class AssetGroup(MutableBaseModel):
    """
    Represents an asset group within the current organization in the Carbon Black Cloud.

    ``AssetGroup`` objects are typically located via a search (using ``AssetGroupQuery``) before they can be operated
     on. They may also be created on the Carbon Black Cloud by using the ``create_group()`` class method.
    """
    urlobject = "/asset_groups/v1/orgs/{0}/groups"
    urlobject_single = "/asset_groups/v1/orgs/{0}/groups/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/asset_group.yaml"

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the ``AssetGroup`` object.

        Required Permissions:
            group-management(READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (int): ID of the policy.
            initial_data (dict): Initial data used to populate the policy.
            force_init (bool): If True, forces the object to be refreshed after constructing.  Default False.
            full_doc (bool): If True, object is considered "fully" initialized. Default False.
        """
        super(AssetGroup, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                         force_init=force_init if initial_data else True, full_doc=full_doc)
        if model_unique_id is None:
            self.touch(True)

    def _build_api_request_uri(self, http_method="GET"):
        """
        Create the URL to be used to access instances of AssetGroup.

        Args:
            http_method (str): Unused.

        Returns:
            str: The actual URL
        """
        uri = AssetGroup.urlobject.format(self._cb.credentials.org_key)
        if self._model_unique_id is not None:
            return f"{uri}/{self._model_unique_id}"
        return uri

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the asset group type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            AssetGroupQuery: The query object for the asset group type.
        """
        return AssetGroupQuery(cls, cb)

    @classmethod
    def create_group(cls, cb, name, description, **kwargs):
        """
        Create a new asset group.

        Required Permissions:
            group-management(CREATE)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            name (str): Name for the new asset group.
            description (str): Description for the new asset group.
            kwargs (dict): Keyword arguments, as defined below.

        Keyword Args:
            policy_id (int): ID of the policy to be associated with this asset group. Default is ``None``.
            query (str): Query string to be used to dynamically populate this group. Default is ``None``,
                which means devices _must_ be manually assigned to the group.

        Returns:
            AssetGroup: The new asset group.
        """
        group_data = {"name": name, "description": description, "member_type": "DEVICE"}
        policy_id = kwargs.get("policy_id", None)
        if policy_id:
            group_data["policy_id"] = policy_id
        query = kwargs.get("query", None)
        if query:
            group_data["query"] = query
        group = AssetGroup(cb, None, group_data, False, True)
        group.save()
        return group


class AssetGroupQuery(BaseQuery, QueryBuilderSupportMixin, IterableQueryMixin, CriteriaBuilderSupportMixin,
                      AsyncQueryMixin):
    """
    Query object that is used to locate ``AssetGroup`` objects.

    The ``AssetGroupQuery`` is constructed via SDK functions like the ``select()`` method on ``CBCloudAPI``.
    The user would then add a query and/or criteria to it before iterating over the results.

    The following criteria are supported on ``AssetGroupQuery`` via the standard ``add_criteria()`` method:

    * ``discovered: bool`` - Whether the asset group has been discovered or not.
    * ``name: str`` - The asset group name to be matched.
    * ``policy_id: int`` - The policy ID to be matched, expressed as an integer.
    * ``group_id: str`` - The asset group ID to be matched, expressed as a GUID.
    """
    def __init__(self, doc_class, cb):
        """
        Initialize the ``AssetGroupQuery``.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        super(AssetGroupQuery, self).__init__()

        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._sortcriteria = {}
        self._count_valid = False
        self._total_results = 0

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Example:
            >>> cb.select(AssetGroup).sort_by("name")

        Args:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            AssetGroupQuery: This instance.
        """
        if direction not in DeviceSearchQuery.VALID_DIRECTIONS:
            raise ApiError("invalid sort direction specified")
        self._sortcriteria = {"field": key, "order": direction}
        return self

    def _build_request(self, from_row, max_rows, add_sort=True):
        """
        Creates the request body for an API call.

        Args:
            from_row (int): The row to start the query at.
            max_rows (int): The maximum number of rows to be returned.
            add_sort (bool): If ``True`` (default), the sort criteria will be added as part of the request.

        Returns:
            dict: The complete request body.
        """
        # Fetch 100 rows per page (instead of 10 by default) for better performance
        request = {"rows": 100}
        if len(self._criteria) > 0:
            request["criteria"] = self._criteria
        query = self._query_builder._collapse()
        if query:
            request["query"] = query
        if from_row >= 0:
            request["start"] = from_row
        if max_rows >= 0:
            request["rows"] = max_rows
        if add_sort and self._sortcriteria != {}:
            request["sort"] = [self._sortcriteria]
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
        """Returns the number of results from the run of this query."""
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

        Required Permissions:
            group-management(READ)

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
                yield self._doc_class(self._cb, item["id"], item, False, True)
                current += 1
                numrows += 1

                if max_rows > 0 and numrows == max_rows:
                    still_querying = False
                    break

            from_row = current
            if current >= self._total_results:
                still_querying = False
                break

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Required Permissions:
            group-management(READ)

        Args:
            context (object): Not used; always ``None``.

        Returns:
            list[AssetGroup]: Result of the async query, as a list of ``AssetGroup`` objects.
        """
        url = self._build_url("/_search")
        request = self._build_request(0, -1)
        resp = self._cb.post_object(url, body=request)
        return_data = resp.json()["results"]
        output = [AssetGroup(self._cb, item['id'], item, False, True) for item in return_data]
        self._total_results = len(output)
        self._count_valid = True
        return output
