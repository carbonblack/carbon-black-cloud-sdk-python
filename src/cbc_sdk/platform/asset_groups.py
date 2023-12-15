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
from cbc_sdk.platform.devices import Device, DeviceSearchQuery


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

    """The valid values for the 'filter' parameter to list_members()."""
    VALID_MEMBER_FILTERS = ("ALL", "DYNAMIC", "MANUAL")

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

    def list_member_ids(self, rows=20, start=0):
        """
        Gets a list of all member IDs in the group, optionally constrained by membership type.

        Required Permissions:
            group-management(READ)

        Args:
            rows (int): Maximum number of rows to retrieve from the server. The function may return fewer member IDs
                        if filtering is applied to the output. Default is 20.
            start (int): Starting row to retrieve from the server; used to implement pagination. Default is 0.

        Returns:
            list[dict]: List of dictionaries that contain the integer element ``external_member_id`` for the device ID,
                        the boolean element ``dynamic`` which is ``True`` if the group member is there due to the
                        group's dynamic query, and the boolean element ``manual`` which is ``True`` if the group member
                        was manually added.  (It is possible for both ``dynamic`` and ``manual`` to be ``True``.)
        """
        query_params = {"rows": rows, "start": start}
        member_data = self._cb.get_object(self._build_api_request_uri() + "/members", query_params)
        return [{"external_member_id": int(m["external_member_id"]), "dynamic": m["dynamic"], "manual": m["manual"]}
                for m in member_data["members"]]

    def list_members(self, rows=20, start=0, membership="ALL"):
        """
        Gets a list of all member devices in the group, optionally constrained by membership type.

        Required Permissions:
            group-management(READ)

        Args:
            rows (int): Maximum number of rows to retrieve from the server. The function may return fewer member IDs
                        if filtering is applied to the output. Default is 20.
            start (int): Starting row to retrieve from the server; used to implement pagination. Default is 0.
            membership (str): Can restrict the types of members that are returned by this method.  Values are "ALL"
                              to return all members, "DYNAMIC" to return only members that were added via the asset
                              group query, or "MANUAL" to return only manually-added members.  Default is "ALL".

        Returns:
            list[Device]: List of ``Device`` objects comprising the membership of the group.``
        """
        if membership not in AssetGroup.VALID_MEMBER_FILTERS:
            raise ApiError(f"invalid filter value: {membership}")
        id_list = self.list_member_ids(rows, start)
        if membership == "ALL":
            return [self._cb.select(Device, m["external_member_id"]) for m in id_list]
        elif membership == "DYNAMIC":
            return [self._cb.select(Device, m["external_member_id"]) for m in id_list if m["dynamic"]]
        elif membership == "MANUAL":
            return [self._cb.select(Device, m["external_member_id"]) for m in id_list if m["manual"]]

    def add_members(self, members):
        """
        Adds additional members to this asset group.

        Required Permissions:
            group-management(CREATE)

        Args:
            members (int, Device, or list): The members to be added to the group. This may be an integer device ID,
                                            a ``Device`` object, or a list of either integers or ``Device`` objects.
        """
        member_ids = []
        if isinstance(members, int):
            member_ids = [str(members)]
        elif isinstance(members, Device):
            member_ids = [str(members.id)]
        else:
            for m in members:
                if isinstance(m, int):
                    member_ids.append(str(m))
                elif isinstance(m, Device):
                    member_ids.append(str(m.id))
        if len(member_ids) > 0:
            self._cb.post_object(self._build_api_request_uri() + "/members",
                                 {"action": "CREATE", "external_member_ids": member_ids})

    def remove_members(self, members):
        """
        Removes members from this asset group.

        Required Permissions:
            group-management(DELETE)

        Args:
            members (int, Device, or list): The members to be added to the group. This may be an integer device ID,
                                            a ``Device`` object, or a list of either integers or ``Device`` objects.
        """
        member_ids = []
        if isinstance(members, int):
            member_ids = [str(members)]
        elif isinstance(members, Device):
            member_ids = [str(members.id)]
        else:
            for m in members:
                if isinstance(m, int):
                    member_ids.append(str(m))
                elif isinstance(m, Device):
                    member_ids.append(str(m.id))
        if len(member_ids) > 0:
            self._cb.post_object(self._build_api_request_uri() + "/members",
                                 {"action": "REMOVE", "external_member_ids": member_ids})

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
        self._default_rows = 100
        self._count_valid = False
        self._total_results = 0

    def set_rows(self, rows):
        """
        Sets the number of query rows to fetch in each batch from the server.

        Args:
             rows (int): The number of rows to be fetched fromt hes erver at a time. Default is 100.

        Returns:
            AssetGroupQuery: This instance.
        """
        self._default_rows = rows
        return self

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
        request = {"rows": self._default_rows}
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
