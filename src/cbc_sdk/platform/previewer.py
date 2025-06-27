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

"""This module contains the ``DevicePolicyChangePreview`` object.

When methods on ``Device``, ``Policy``, or ``AssetGroup`` are called to "preview" changes in device policy,
a list of these objects is returned.  Each object represents a change in "effective" policy on one or more
devices.
"""


class DevicePolicyChangePreview:
    """
    Contains data previewing a change in device policies.

    Changes to policies may happen via asset group memberships, policy rank changes, device policy overrides,
    or other causes.

    Each one of these objects shows, for a given group of assets, the current policy that is the "effective policy"
    for those assets, the new policy that will be the "effective policy" for those assets, the number of assets
    affected, and which assets they are.
    """
    def __init__(self, cb, preview_data):
        """
        Creates a new instance of ``AssetGroupChangePreview``.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            preview_data (dict): Contains the preview data returned by the server API.
        """
        self._cb = cb
        self._preview_data = preview_data

    def __str__(self):  # pragma: no cover
        """Returns a string representation of the object."""
        lines = [f"{self.__class__.__name__} object, bound to {self._cb.session.server}.", '-' * 79, '']
        p = self._preview_data
        lines.append(f"Current policy: #{p['current_policy']['id']} at rank {p['current_policy']['position']}")
        lines.append(f"    New policy: #{p['new_policy']['id']} at rank {p['new_policy']['position']}")
        lines.append(f"   Asset count: {p['asset_count']}")
        lines.append(f"   Asset query: {p['asset_query']}")
        return "\n".join(lines)

    @property
    def current_policy_id(self):
        """The ID of the policy that is the current "effective" policy for a group of assets."""
        return self._preview_data['current_policy']['id']

    @property
    def current_policy(self):
        """The ``Policy`` object that is the current "effective" policy for a group of assets."""
        return self._cb.select("Policy", self._preview_data['current_policy']['id'])

    @property
    def current_policy_position(self):
        """The position, or rank, of the policy that is the current "effective" policy for a group of assets."""
        return self._preview_data['current_policy']['position']

    @property
    def new_policy_id(self):
        """The ID of the policy that will become the new "effective" policy for a group of assets."""
        return self._preview_data['new_policy']['id']

    @property
    def new_policy(self):
        """The ``Policy`` object that will become the new "effective" policy for a group of assets."""
        return self._cb.select("Policy", self._preview_data['new_policy']['id'])

    @property
    def new_policy_position(self):
        """The position, or rank, of the policy that will become the new "effective" policy for a group of assets."""
        return self._preview_data['new_policy']['position']

    @property
    def asset_count(self):
        """The number of assets to be affected by the change in their effective policy."""
        return self._preview_data['asset_count']

    @property
    def asset_query(self):
        """
        A ``Device`` query which looks up the assets that are to be affected by the change in their effective policy.

        Once the query is created, it can be modified with additional criteria or options before it is executed.
        """
        return self._cb.select("Device").where(self._preview_data['asset_query'])

    @property
    def assets(self):  # pragma: no cover
        """
        The list of assets, i.e. ``Device`` objects, to be affected by the change in their effective policy.

        Required Permissions:
            device (READ)
        """
        return list(self.asset_query)
