Asset Groups
============

Asset Groups provide a way to organize and manage your fleet of Endpoints, VM Workloads, and VDIs.
Create groups of assets and apply policies to the groups so the protections of all similar assets are synchronized.
The ability to add one asset to multiple groups, and rank policies for precedence in application, gives added
flexibility and fine tuning for complex organizations.

You can locate the full list of operations and attributes in the
:py:mod:`AssetGroup() <cbc_sdk.platform.asset_groups.AssetGroup>` class.

Resources
---------
* `API Documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/asset-groups-api/>`_ on Developer Network
* Example script in `GitHub <https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_

Retrieve Asset Groups
---------------------

There two options for getting a list of asset groups.  The function ``get_all_groups()`` does exactly that; returns all
Asset Groups in your organization.

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import AssetGroup
    >>> api = CBCloudAPI(profile='sample')
    >>> all_asset_groups = AssetGroup.get_all_groups(api)
    >>> print("There are {} asset groups. First group: {}".format(len(all_asset_groups), all_asset_groups.first()))
    There are 1 asset groups. This is the first: AssetGroup object, bound to https://defense.conferdeploy.net.
     Partially initialized. Use .refresh() to load all attributes
    -------------------------------------------------------------------------------

         create_time: 2024-01-24T04:38:26.930Z
         description: Windows No Policy
          discovered: False
                  id: 34fc5890-caf0-400a-98ba-a81763960f6e
        member_count: 1030
         member_type: DEVICE
                name: Windows No Policy
             org_key: 7desj9gn
               query: os.equals: "WINDOWS"
              status: OK
         update_time: 2024-01-24T04:38:27.972Z

Asset groups can also be searched using ``name``, ``policy_id`` or ``group_id`` in the criteria element.

The example shows creating an ``AssetGroupQuery`` class, then adding criteria to limit the results and specifying the
field to sort by.  The query is not executed until it accessed, in this case by iterating over the results.

Summary information for each asset group is printed, and then the devices in that asset group are listed.

    >>> search_asset_group_query = api.select(AssetGroup)
    >>> search_asset_group_query.add_criteria("name", "Second demo group")
    >>> search_asset_group_query.sort_by("name", "ASC")
    >>> for ag in search_asset_group_query:
    >>>     print("\nAsset group name = {}. It has {} members".format(ag.name, ag.member_count))
    >>>     print("Policy assigned to the Asset Group is Name: {}, Id: {}".format(ag.policy_name, ag.policy_id))
    >>>     for d in ag.list_members():
    >>>         print("Device Name: {}, Id: {}".format(d.name, d.id))
    Asset group name = Second demo group. It has 3 members
    Policy assigned to the Asset Group is Name: DemoPolicy, Id: 123456
    Device Name: DemoDevice, Id: 2468642
    Device Name: SDKDemo, Id: 1357975
    Device Name: AnotherDemoMachine, Id: 19283746
    ... truncated ...

Create an Asset Group
---------------------

The only required field when creating an asset group is the Asset Group Name.

Creating a group without a policy assigned enables the use of a group for visibility of specific assets.
After creation, it is possible in use any of combination of assigning assets directly, adding a query or assigning
a policy.

    >>> new_asset_group = AssetGroup.create_group(api, "My Example Asset Group", description="Demonstrating the SDK")
    >>> print(new_asset_group)
    AssetGroup object, bound to https://defense.conferdeploy.net.
    -------------------------------------------------------------------------------

         create_time: 2024-01-24T05:47:34.378Z
         description: Demonstrating the SDK
          discovered: False
                  id: aae06712-96d4-43ea-ae67-07112d6f670e
        member_count: 0
         member_type: DEVICE
                name: My Example Asset Group
             org_key: ABCD1234
              status: OK
         update_time: 2024-01-24T05:47:34.378Z

Now add a query which will dynamically include any asset with the Windows operating system and a policy:

    >>> new_asset_group.query = "os.equals:WINDOWS"
    >>> new_asset_group.policy_id = 12345
    >>> new_asset_group.save()

Parts of Carbon Black Cloud have asynchronous processing and are eventually consistent.
When writing automated scripts, use the status field to determine when the asset group membership has
finished updating.

* ``OK`` indicates the membership evaluation is complete
* ``UPDATING`` indicates that group’s dynamic memberships are being re-evaluated

    >>> while new_asset_group.status != "OK":
    >>>     print("waiting")
    >>>     time.sleep(5)
    >>>     new_asset_group.refresh()
    >>> print("new_asset_group {}".format(new_asset_group))
    new_asset_group, bound to https://defense.conferdeploy.net.
     Last refreshed at Tue Jan 23 22:47:47 2024
    -------------------------------------------------------------------------------
         create_time: 2024-01-24T05:47:35.150Z
         description: Demonstrating the SDK
          discovered: False
                  id: ceb27e6c-7c23-4dd5-af7a-3b0c14363240
        member_count: 204
         member_type: DEVICE
                name: My Example Asset Group
             org_key: ABCD1234
           policy_id: 12345
         policy_name: DemoPolicy
               query: os.equals:WINDOWS
              status: OK
         update_time: 2024-01-24T05:47:35.585Z
    AssetGroup object, bound to https://defense.conferdeploy.net.


All attributes can also be provided to the create method:

    >>> second_asset_group = AssetGroup.create_group(api, "Second example group", "Second group description",
                                                     query = "os.equals:MAC", policy_id = 12345)

The add_member() function is used to assign a device directly to the group. (Compared to dynamically added, when the
device matches the query on the asset group.)

    >>> random_device = api.select(Device).first()
    >>> second_asset_group.add_members(random_device)

Delete an Asset Group
---------------------

To delete an Asset Group, use the delete method:

    >>> second_asset_group.delete()

Preview Policy Rank Changes
---------------------------

The effective policy on a specific device is determined by the rank of policies the device is assigned, with higher
ranked policies taking precedence.

The `example script <https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_
includes finding two policies that are likely have have impactful changes.  This snippet uses hardcoded values so the
focus is on the method being called and output.

The preview method is a static class method on Policy, since it is a policy change that is being previewed.

The result is a :py:mod:`DevicePolicyChangePreview() <cbc_sdk.platform.previewer.DevicePolicyChangePreview>` class,
which contains information about all the device that would have a change in effective policy.

    >>> api = CBCloudAPI(profile='sample')
    >>> policy_id = 1234
    >>> # to get a policy that exists in your org: policy_id = api.select(Policy).first().id
    >>> new_policy_position = 1
    >>> changes = Policy.preview_policy_rank_changes(api, [(policy_id, new_policy_position)])
    DevicePolicyChangePreview object, bound to https://defense.conferdeploy.net.
    -------------------------------------------------------------------------------
    Current policy: #98765 at rank 7
        New policy: #1234 at rank 1
       Asset count: 264
       Asset query: ((-_exists_:ag_agg_key_manual AND ag_agg_key_dynamic:9b0a62b19086bdbfcff5c62e581304a28cd445aee86d87c6d95c57483ae5e05b AND policy_id:100714 AND policy_override:false) AND (os.equals: "WINDOWS"))

This ``change`` says there's an asset group that is currently using policy id 98765 which is ranked 7.
If the change was processed the asset group would use a new policy, id 1234 which is at rank 1.  This would affect 264
Assets and the Asset query can be used to find those Assets.

The Asset Query is a class of type ``DeviceSearchQuery`` which can be executed:

    >>> devices = changes[0].asset_query
    >>> print("type of devices object is {}".format(type(devices)))
    >>> print(len(devices))
    type of devices object is <class 'cbc_sdk.platform.devices.DeviceSearchQuery'>
    264

Preview Asset Group Changes
---------------------------

Previewing the changes that would happen if an asset group was changed is very similar to the Preview Policy Rank
Changes above.

Once Asset Groups have been created and policies assigned, the preview asset group changes function can be used to
identify the devices that would have their group membership or effective policy impacted by creating or deleting an
Asset Group, or by changing the query on the asset group.

Here we're working with a random asset group and policy, using the ``first()`` function.

A new policy is assigned and the existing query is not changed.

    >>> asset_group = api.select(AssetGroup).first()
    >>> policy_id = api.select(Policy).first()
    >>> new_policy_position = 1
    >>> api = CBCloudAPI(profile='sample')
    >>> changes = AssetGroup.preview_update_asset_groups(api, [asset_group], policy_id, asset_group.query)
    >>> print("There are {} changes that would result from the proposed change. The first change:".format(len(changes)))
    >>> print(changes[0])
    DevicePolicyChangePreview object, bound to https://defense.conferdeploy.net.
    -------------------------------------------------------------------------------
    Current policy: #148443 at rank 96
        New policy: #80947 at rank 1
       Asset count: 117
       Asset query: ((-_exists_:ag_agg_key_manual AND -_exists_:ag_agg_key_dynamic AND policy_id:148443 AND policy_override:false) AND (os.equals:MAC))
