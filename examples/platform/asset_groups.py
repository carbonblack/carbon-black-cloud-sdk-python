#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2020-2024. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""
This example shows how to use the Asset Groups API and interact with related Policies and Devices.

The SDK documentation is published on Read The Docs.  An Asset Groups Guide is available there.
https://carbon-black-cloud-python-sdk.readthedocs.io

"""

import sys
from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import AssetGroup, Policy, Device

# To see the http requests being made, and the structure of the search requests enable debug logging
# import logging
# logging.basicConfig(level=logging.DEBUG)


def preview_policy_rank_change(api):
    """Demonstrate previewing the changes to effective policies on assets if policy ranking is changed.

    Once Asset Groups have been created and policies assigned, the preview functions can be used to determine
    the impact of changing asset groups or policy rankings.
    This example finds the policy in the highest rank that has assets affected, and then moves it one position lower.
    1 is the highest rank.
    """
    # Start by finding the highest ranked policy
    all_policies = list(api.select(Policy).all())
    policy_highest_rank = None
    policy_num_devices = 0

    for p in all_policies:
        tmp_policy_num_devices = len(api.select(Device).set_policy_ids([p.id]))
        if tmp_policy_num_devices > 0:
            if policy_highest_rank is None:
                policy_highest_rank = p
                policy_num_devices = tmp_policy_num_devices
            elif p.position < policy_highest_rank.position:
                policy_highest_rank = p
                policy_num_devices = tmp_policy_num_devices

    print("Policy {} with id = {}, is at rank {} and the policy affects {} members".
          format(policy_highest_rank.name, policy_highest_rank.id, policy_highest_rank.position, policy_num_devices))

    new_policy_position = policy_highest_rank.position + 1

    # preview what would change if the policy at rank 1 was moved to position 2
    changes = Policy.preview_policy_rank_changes(api, [(policy_highest_rank.id, new_policy_position)])
    if len(changes) == 0:
        print("No changes to effective policy would occur.")
    else:
        print("There are {} changes that would result from moving Policy {} from position {} to position {}."
              .format(len(changes), policy_highest_rank.name, policy_highest_rank.position, new_policy_position))
    i = 1
    for c in changes:
        print("printing change number {}".format(i))
        i = i + 1
        current_rank_1_policy = api.select(Policy, c.current_policy_id)
        future_rank_1_policy = api.select(Policy, c.new_policy_id)
        print("{} assets will be affected.".format(c.asset_count))
        print("The assets affected are:")
        assets_affected = c.asset_query.all()
        for a in assets_affected:
            print("Asset Name: {} - Asset Id {}".format(a.name, a.id))
        print("\n The currently effective policy for those assets is: name: {}, id: {}".
              format(current_rank_1_policy.name, current_rank_1_policy.id))
        print("\n The effective policy after the move would be: name: {}, id: {}".
              format(future_rank_1_policy.name, future_rank_1_policy.id))


def preview_asset_group_changes():
    """Show how to use the preview asset group function to understand the impact of changes such as changing a query"""
    print("preview_asset_group_changes(): Coming Soon")


def main():
    """This script demonstrates how to use Asset Groups in the SDK and common operations to link to related objects.

    This example does not use command line parsing in order to reduce complexity and focus on the SDK functions.
    Review the Authentication section of the Read the Docs for information about Authentication in the SDK
    https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/authentication/

    This is written for clarity of explanation, not perfect coding practices.
    """
    # CBCloudAPI is the connection to the cloud.  It holds the credentials for connectivity.
    # To execute this script, the profile must have an API key with the following permissions.
    # If you are restricted in the actions you're allowed to perform, expect a 403 response for missing permissions.
    # Permissions are set on Settings -> API Access -> Access Level and then assigned to an API Key
    # GM - Group Management - group-management - CREATE, READ, UPDATE, DELETE: For managing asset groups
    # Device - General Information - device - READ: For getting device information
    # Policies - Policies - org.policies - READ: For viewing policy information and pre-viewing the impact of changes
    #    to policy ranking and asset groups.

    api = CBCloudAPI(profile="YOUR_PROFILE_HERE")

    # to get all asset groups, a static method is available on the AssetGroup class.
    # This is useful for listing the groups configured in your org
    all_asset_groups = AssetGroup.get_all_groups(api)
    for ag in all_asset_groups:
        print("asset group name: {}, member count: {}".format(ag.name, ag.member_count))

    # Create an asset group.  The only mandatory field is the Asset Group Name.
    # It can be created without a policy, which enables the use of group for visibility of specific assets
    # It can be created without a query, which enables manual assignment of assets to the group later
    new_asset_group_name = "My Example Asset Group"
    new_asset_group = AssetGroup.create_group(api, new_asset_group_name, "Demonstrating the SDK")
    print(new_asset_group)

    # Add a query.  All assets that match this criteria will be dynamically added to the group
    new_asset_group.query = "os.equals:WINDOWS"
    # Assign a policy.  All assets in the group may have this policy applied.  If an asset is in more than one group,
    # policy ranking determines which is the effective policy.
    lowest_rank_policy = None
    for p in api.select(Policy).all():
        if lowest_rank_policy is None or p.position > lowest_rank_policy.position:
            lowest_rank_policy = p
    new_asset_group.policy = lowest_rank_policy.id
    new_asset_group.save()
    print(new_asset_group)
    # Clean up after ourselves and delete the asset group
    new_asset_group.delete()

    # An asset group can also be created with a query and / or a policy included
    second_name = "Second demo group"
    second_asset_group = AssetGroup.create_group(api, second_name, "Second group description",
                                                 query="os.equals:MAC", policy_id=lowest_rank_policy.id)
    # Asset groups can be searched
    search_asset_group_query = api.select(AssetGroup).add_criteria("name", second_name).sort_by("name", "ASC")
    for ag in search_asset_group_query:
        print("Asset group name = {}. It has {} members".format(ag.name, ag.member_count))

    # Clean up after ourselves and delete the asset group
    second_asset_group.delete()

    # Assets can be assigned manually to an asset group rather than with a query
    random_device = api.select(Device).first()
    third_asset_group = AssetGroup.create_group(api, second_name, "Manual Assignment Demo")
    third_asset_group.add_members(random_device)
    third_asset_group.refresh()
    print(third_asset_group)
    # remove the device
    third_asset_group.remove_members(random_device)
    print(third_asset_group)
    # Clean up after ourselves and delete the asset group
    third_asset_group.delete()

    # Show how the preview policy rank function can be used
    preview_policy_rank_change(api)
    # Show how the preview asset group changes function can be used
    preview_asset_group_changes()

    print("The End")


print("breakpoint")

if __name__ == "__main__":
    # Trap keyboard interrupts while running the script.
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nKeyboard interrupt\n")
        sys.exit(0)
