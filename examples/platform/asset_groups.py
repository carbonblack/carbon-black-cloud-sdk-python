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
import time
from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import AssetGroup, Policy, Device

# To see the http requests being made, and the structure of the search requests enable debug logging
# import logging
# logging.basicConfig(level=logging.DEBUG)


def demo_preview_policy_rank_change(api):
    """Demonstrate previewing the changes to effective policies on assets if policy ranking is changed.

    Once Asset Groups have been created and policies assigned, the policy rank preview function can be used to determine
    the impact of changing policy rankings.
    This example finds the policy in the highest rank that has assets affected, and then moves it one position lower.
    1 is the highest rank.
    """
    # Start by finding the highest ranked policy
    print("\n\n Starting preview_policy_rank_change \n\n")
    all_policies = list(api.select(Policy).all())
    policy_top_rank = None
    policy_num_devices = 0

    for policy in all_policies:
        tmp_policy_num_devices = len(api.select(Device).set_policy_ids([policy.id]))
        if tmp_policy_num_devices > 0:
            if policy_top_rank is None:
                policy_top_rank = policy
                policy_num_devices = tmp_policy_num_devices
            elif policy.position < policy_top_rank.position:
                policy_top_rank = policy
                policy_num_devices = tmp_policy_num_devices

    # This is the highest ranking policy that has devices associated.
    # Since this is the highest ranked policy, it will be the effective policy for those assets.
    print("Policy {} with id = {}, is at rank {} and the policy affects {} members".
          format(policy_top_rank.name, policy_top_rank.id, policy_top_rank.position, policy_num_devices))

    # We're going to preview the impacts of moving the policy one position down the ranking (1 is the top)
    new_policy_position = policy_top_rank.position + 1

    # preview what would change if the policy at the top position moved down one rank.
    changes = Policy.preview_policy_rank_changes(api, [(policy_top_rank.id, new_policy_position)])
    print_changes(changes)
    print("\n\n Finished preview_policy_rank_change \n\n")


def demo_preview_asset_group_changes(api):
    """Show how to use the preview asset group function to understand the impact of changes such as changing a query

    Once Asset Groups have been created and policies assigned, the preview asset group changes function can be used to
    identify the devices that would have their group membership or effective policy impacted.
    """
    print("\n\n Starting preview_asset_group_change \n\n")
    # Get an asset group to work with
    asset_group_1 = api.select(AssetGroup).first()
    # Get the top and second ranked policies
    top_policy = None
    second_policy = None
    for policy in api.select(Policy):
        if policy.position == 1:
            top_policy = policy
        if policy.position == 2:
            second_policy = policy

    changes = None
    # Preview the changes that would happen if the policy is changed to the top rank.
    # In the case where it already has the top ranked policy, change it to the second ranked policy.
    # Send in the exising query - not changing.
    if asset_group_1.policy_id is None or asset_group_1.policy_id != top_policy.id:
        changes = AssetGroup.preview_update_asset_groups(api, [asset_group_1], top_policy.id, asset_group_1.query)
    else:
        changes = AssetGroup.preview_update_asset_groups(api, [asset_group_1], second_policy.id, asset_group_1.query)
    print("Changes from setting a new policy on the asset group")
    print_changes(changes)

    # Preview adding a member to a group.  Note that if the device is already in the group, there will be no changes
    device = api.select(Device).first()
    changes = AssetGroup.preview_add_members_to_groups(api, [device.id], [asset_group_1])
    print("Changes from adding a device to the asset group")
    print_changes(changes)

    # Preview the changes to devices if a new asset group is created
    changes = AssetGroup.preview_create_asset_group(api, top_policy.id, "os.equals:MAC")
    print("Changes from creating a new asset group")
    print_changes(changes)

    changes = AssetGroup.preview_delete_asset_groups(api, [asset_group_1])
    print("Changes from deleting an asset group")
    print_changes(changes)


def print_changes(changes):
    """Iterate through the changes object and print the content with contextual information."""
    if len(changes) == 0:
        print("No changes would occur.")
    else:
        print("There are {} changes that would result from the proposed change".format(len(changes)))

    for change_counter, change in enumerate(changes, 1):
        print("printing change number {}".format(change_counter))
        print("{} assets will be affected.".format(change.asset_count))
        print("The assets affected are:")
        assets_affected = change.asset_query.all()
        for asset in assets_affected:
            print("Asset Name: {} - Asset Id {}".format(asset.name, asset.id))
        print("\n The currently effective policy for those assets is: name: {}, id: {}".
              format(change.current_policy.name, change.current_policy.id))
        print("\n The effective policy after the move would be: name: {}, id: {}".
              format(change.new_policy.name, change.new_policy.id))
    print("\n\n")


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
    new_asset_group = AssetGroup.create_group(api, "My Example Asset Group", description="Demonstrating the SDK")
    print(new_asset_group)

    # Add a query.  All assets that match this criteria will be dynamically added to the group
    new_asset_group.query = "os.equals:WINDOWS"
    # Assign a policy.  All assets in the group may have this policy applied.  If an asset is in more than one group,
    # policy ranking determines which is the effective policy.
    # Choosing the lowest ranked policy as this is the least likely to actually change the behaviour while experimenting
    # with a script.
    bottom_rank_policy = None
    for p in api.select(Policy).all():
        if bottom_rank_policy is None or p.position > bottom_rank_policy.position:
            bottom_rank_policy = p
    new_asset_group.policy_id = bottom_rank_policy.id
    new_asset_group.save()
    print("\n\n new_asset_group {}".format(new_asset_group))
    # Clean up after ourselves and delete the asset group
    new_asset_group.delete()

    # An asset group can also be created with a query and / or a policy included
    print("\n\n Second asset group with policy and query")
    second_name = "Second demo group"
    second_asset_group = AssetGroup.create_group(api, second_name, "Second group description",
                                                 query="os.equals:MAC", policy_id=bottom_rank_policy.id)
    second_asset_group.refresh()
    # The system is asynchronous and eventually consistent. When writing automated scripts, use the status field to
    # determine when the asset group membership has finished updating.
    # OK indicates the membership evaluation is complete
    # UPDATING indicates that group’s dynamic memberships are being re-evaluated
    while second_asset_group.status != "OK":
        print("waiting")
        time.sleep(10)
        second_asset_group.refresh()
    # Asset groups can be searched
    search_asset_group_query = api.select(AssetGroup).add_criteria("name", second_name).sort_by("name", "ASC")
    for ag in search_asset_group_query:
        print("\n\nAsset group name = {}. It has {} members".format(ag.name, ag.member_count))
        print("Policy assigned to the Asset Group is Name: {}, Id: {}".format(ag.policy_name, ag.policy_id))
        # These are the assets that are now part of the dynamic asset group
        for d in ag.list_members():
            print("Device Name: {}, Id: {}".format(d.name, d.id))
            if d.policy_id == bottom_rank_policy.id:
                print("The effective policy is from the asset group")
            else:
                print("This asset group does not determine the effective policy The effective policy is {} - {}"
                      .format(d.policy_id, d.policy_name))

    # Asset groups can have members from a query, and also direct (manual) assignment.
    # Assign a device directly to the second asset group
    random_device = api.select(Device).first()
    second_asset_group.add_members(random_device)
    second_asset_group.refresh()
    while second_asset_group.status != "OK":
        print("waiting")
        time.sleep(10)
        second_asset_group.refresh()
    # The number of assets in the group may not change, if the randomly selected one is already a member of that group.
    print("\n\nsecond_asset_group with device assigned {}".format(second_asset_group))
    # remove the device
    second_asset_group.remove_members(random_device)
    print(second_asset_group)
    # Clean up after ourselves and delete the asset group
    second_asset_group.delete()

    # Step into the method to see the steps to select a policy and preview the impact changing it's rank would have
    demo_preview_policy_rank_change(api)
    # Step into the method to see methods available to preview the impact changing things such as the assigned policy
    # on an asset group or creating a new asset group would have.
    demo_preview_asset_group_changes(api)

    print("The End")


if __name__ == "__main__":
    # Trap keyboard interrupts while running the script.
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nKeyboard interrupt\n")
        sys.exit(0)
