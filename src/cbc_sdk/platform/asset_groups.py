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

"""Asset groups implementation as part of Platform API"""

from cbc_sdk.base import MutableBaseModel


class AssetGroup(MutableBaseModel):
    """
    Represents an asset group within the organization.
    """
    urlobject = "/asset_groups/v1beta/orgs/{0}/groups"
    urlobject_single = "/asset_groups/v1beta/orgs/{0}/groups/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/asset_groups.yaml"

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the AssetGroup object.

        Required Permissions:
            gm.group-set (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (int): ID of the policy.
            initial_data (dict): Initial data used to populate the policy.
            force_init (bool): If True, forces the object to be refreshed after constructing.  Default False.
            full_doc (bool): If True, object is considered "fully" initialized. Default False.
        """
        super(AssetGroup, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                         force_init=force_init if initial_data else True, full_doc=full_doc)

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
    def create_group(cls, cb, name, description, policy_id):
        """
        Create a new asset group.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            name (str): Name for the new asset group.
            description (str): Description for the new asset group.
            policy_id (int): ID of the policy to be associated with this asset group.

        Returns:
            AssetGroup: The new asset group.
        """
        group_data = {"name": name, "description": description, "member_type": "DEVICE", "policy_id": policy_id}
        group = AssetGroup(cb, None, group_data, False, True)
        group.save()
        return group
