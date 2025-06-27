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
from cbc_sdk.platform.previewer import DevicePolicyChangePreview


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
            group-management(READ), devices(READ)

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
            members (int, Device, or list): The members to be removed from the group. This may be an integer device ID,
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

    def get_statistics(self):
        """
        For this group, return statistics about its group membership.

        The statistics include how many of the group's members belong to other groups, and how many members
        belong to groups without policy association.

        See
        `this page <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/asset-groups-api/#get-asset-group-stats>`_
        for more details on the structure of the return value from this method.

        Required Permissions:
            group-management(READ)

        Returns:
             dict: A dict with two elements. The "intersections" element contains elements detailing which groups share
                   members with this group, and which members they are.  The "unassigned_properties" element contains
                   elements showing which members belong to groups without policy association.
        """    # noqa: E501 W505
        return self._cb.get_object(self._build_api_request_uri() + "/membership_summary")

    def preview_add_members(self, devices):
        """
        Previews changes to the effective policies for devices which result from adding them to this asset group.

        Required Permissions:
            org.policies (READ)

        Args:
            devices (list): The devices which will be added to this asset group. Each entry in this list is either
                an integer device ID or a ``Device`` object.

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        return AssetGroup.preview_add_members_to_groups(self._cb, devices, [self])

    def preview_remove_members(self, devices):
        """
        Previews changes to the effective policies for devices which result from removing them from this asset group.

        Required Permissions:
            org.policies (READ)

        Args:
            devices (list): The devices which will be removed from this asset group. Each entry in this list is either
                an integer device ID or a ``Device`` object.

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        return AssetGroup.preview_remove_members_from_groups(self._cb, devices, [self])

    def preview_save(self):
        """
        Previews changes to the effective policies for devices which result from unsaved changes to this asset group.

        Required Permissions:
            org.policies (READ)

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        policy_id = None
        query = None
        remove_policy_id = False
        remove_query = False
        if "policy_id" in self._dirty_attributes:
            if self._info["policy_id"] is None:
                remove_policy_id = True
            else:
                policy_id = self._info["policy_id"]
        if "query" in self._dirty_attributes:
            if self._info["query"] is None:
                remove_query = True
            else:
                query = self._info["query"]
        return AssetGroup.preview_update_asset_groups(self._cb, [self], policy_id=policy_id, query=query,
                                                      remove_policy_id=remove_policy_id, remove_query=remove_query)

    def preview_delete(self):
        """
        Previews changes to the effective policies for devices which result from this asset group being deleted.

        Required Permissions:
            org.policies (READ)

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        return AssetGroup.preview_delete_asset_groups(self._cb, [self])

    @classmethod
    def create_group(cls, cb, name, description=None, policy_id=None, query=None):
        """
        Create a new asset group.

        Required Permissions:
            group-management(CREATE)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            name (str): Name for the new asset group.
            description (str): Description for the new asset group. Default is ``None``.
            policy_id (int): ID of the policy to be associated with this asset group. Default is ``None``.
            query (str): Query string to be used to dynamically populate this group. Default is ``None``,
                which means devices _must_ be manually assigned to the group.

        Returns:
            AssetGroup: The new asset group.
        """
        group_data = {"name": name, "member_type": "DEVICE"}
        if description:
            group_data["description"] = description
        if policy_id:
            group_data["policy_id"] = policy_id
        if query:
            group_data["query"] = query
        group = AssetGroup(cb, None, group_data, False, True)
        group.save()
        return group

    @classmethod
    def get_all_groups(cls, cb):
        """
        Retrieve all asset groups in the organization.

        Required Permissions:
            group-management(READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.

        Returns:
            list[AssetGroup]: List of ``AssetGroup`` objects corresponding to the asset groups in the organization.
        """
        return_data = cb.get_object(AssetGroup.urlobject.format(cb.credentials.org_key))
        return [AssetGroup(cb, v['id'], v) for v in return_data['results']]

    @classmethod
    def _collect_groups(cls, groups):
        """
        Collects a list of asset groups as IDs.

        Args:
            groups (list): A list of items, each of which may be either string group IDs or ``AssetGroup`` objects.

        Returns:
            list[str]: A list of string group IDs.
        """
        group_list = []
        for group in groups:
            if isinstance(group, AssetGroup):
                group_list.append(group.id)
            elif isinstance(group, str):
                group_list.append(group)
        return group_list

    @classmethod
    def _preview_asset_group_member_change(cls, cb, action, members, groups):
        """
        Internal function which handles asset group change previews.

        Required Permissions:
            org.policies (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            action (str): The action to be passed to the server.
            members (list): A list of either integer device IDs or ``Device`` objects.
            groups (list): A list of either string asset group IDs or ``AssetGroup`` objects.

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        ret = cb.post_object(f"/policy-assignment/v1/orgs/{cb.credentials.org_key}/asset-groups/preview",
                             {"action": action, "asset_ids": Device._collect_devices(members),
                              "asset_group_ids": AssetGroup._collect_groups(groups)})
        return [DevicePolicyChangePreview(cb, p) for p in ret.json()["preview"]]

    @classmethod
    def preview_add_members_to_groups(cls, cb, members, groups):
        """
        Previews changes to the effective policies for devices which result from adding them to asset groups.

        Required Permissions:
            org.policies (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            members (list): The devices which will be added to new asset groups. Each entry in this list is either
                an integer device ID or a ``Device`` object.
            groups (list): The asset groups to which the devices will be added.  Each entry in this list is either
                a string asset group ID or an ``AssetGroup`` object.

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        return cls._preview_asset_group_member_change(cb, "ADD_MEMBERS", members, groups)

    @classmethod
    def preview_remove_members_from_groups(cls, cb, members, groups):
        """
        Previews changes to the effective policies for devices which result from removing them from asset groups.

        Required Permissions:
            org.policies (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            members (list): The devices which will be removed from asset groups. Each entry in this list is either
                an integer device ID or a ``Device`` object.
            groups (list): The asset groups from which the devices will be removed.  Each entry in this list is either
                a string asset group ID or an ``AssetGroup`` object.

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        return cls._preview_asset_group_member_change(cb, "REMOVE_MEMBERS", members, groups)

    @classmethod
    def preview_create_asset_group(cls, cb, policy_id, query):
        """
        Previews changes to the effective policies for devices which result from creating a new asset group.

        Required Permissions:
            org.policies (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            policy_id (int): The ID of the policy to be added to the new asset group.
            query (str): The query string to be used for the new asset group.

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        ret = cb.post_object(f"/policy-assignment/v1/orgs/{cb.credentials.org_key}/asset-groups/preview",
                             {"action": "ASSET_GROUPS_CREATE", "asset_group_query": query, "policy_id": policy_id})
        return [DevicePolicyChangePreview(cb, p) for p in ret.json()["preview"]]

    @classmethod
    def preview_update_asset_groups(cls, cb, groups, policy_id=None, query=None, remove_policy_id=False,
                                    remove_query=False):
        """
        Previews changes to the effective policies for devices which result from changes to asset groups.

        Required Permissions:
            org.policies (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            groups (list): The asset groups which will be updated.  Each entry in this list is either
                a string asset group ID or an ``AssetGroup`` object.
            policy_id (int): If this is not ``None`` and ``remove_policy_id`` is ``False``, contains the ID of the
                policy to be assigned to the specified groups. Default is ``None``.
            query (str): If this is not ``None`` and ``remove_query`` is ``False``, contains the new query string
                to be assigned to the specified groups. Default is ``None``.
            remove_policy_id (bool): If this is ``True``, indicates that the specified groups will have their policy
                ID removed entirely. Default is ``False``.
            remove_query (bool):  If this is ``True``, indicates that the specified groups will have their query
                strings removed entirely. Default is ``False``.

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        if not (remove_policy_id or remove_query) and policy_id is None and query is None:
            return []
        body = {"action": "ASSET_GROUPS_UPDATE", "asset_group_ids": AssetGroup._collect_groups(groups)}
        if remove_policy_id:
            body["policy_id"] = None
        elif policy_id is not None:
            body["policy_id"] = policy_id
        if remove_query:
            body["asset_group_query"] = None
        elif query is not None:
            body["asset_group_query"] = query
        ret = cb.post_object(f"/policy-assignment/v1/orgs/{cb.credentials.org_key}/asset-groups/preview", body)
        return [DevicePolicyChangePreview(cb, p) for p in ret.json()["preview"]]

    @classmethod
    def preview_delete_asset_groups(cls, cb, groups):
        """
        Previews changes to the effective policies for devices which result from deleting asset groups.

        Required Permissions:
            org.policies (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            groups (list): The asset groups which will be deleted.  Each entry in this list is either
                a string asset group ID or an ``AssetGroup`` object.

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        ret = cb.post_object(f"/policy-assignment/v1/orgs/{cb.credentials.org_key}/asset-groups/preview",
                             {"action": "ASSET_GROUPS_DELETE", "asset_group_ids": AssetGroup._collect_groups(groups)})
        return [DevicePolicyChangePreview(cb, p) for p in ret.json()["preview"]]


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
