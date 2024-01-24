Asset Groups
============

Asset Groups provides a way to organize and manage your fleet of Endpoints, VM Workloads, and VDIs.
Create groups of assets and apply policies to the groups so the protections of all similar assets are synchronized.
The ability to add one asset to multiple groups, and rank policies for precedence in application, gives added
flexibility and fine tuning for complex organizations.

You can locate the full list of operations and attributes in the
:py:mod:`Asset() <cbc_sdk.platform.asset_groups.AssetGroup>` class.

Resources
---------
* `API Documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/asset-groups-api/>`_ on Developer Network
* Example script in `GitHub <https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_

Retrieve Asset Groups
---------------------

By using the following the example, you can retrieve the first 5 ``[:5]`` alerts that have a minimum severity level of ``7``.

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import AssetGroup
    >>> api = CBCloudAPI(profile='sample')
    >>> all_asset_groups = AssetGroup.get_all_groups(api)
    >>> for ag in all_asset_groups:
    >>>     print("asset group name: {}, member count: {}".format(ag.name, ag.member_count))


Create an Asset Group
---------------------

The only required field when creating an asset group is the Asset Group Name.

* Creating a group without a policy assigned enables the use of a group for visibility of specific assets
* After creation, it is possible in any combination to assign assets directly, add a query or assign a policy.

    >>> new_asset_group = AssetGroup.create_group(api, "My Example Asset Group", description="Demonstrating the SDK")
    >>> print(new_asset_group)

Now add a query and a policy:

    >>> new_asset_group.query = "os.equals:WINDOWS"
    >>> new_asset_group.policy = bottom_rank_policy.id
    >>> new_asset_group.save()

All attributes can also be provided to the create method:

    >>> second_asset_group = AssetGroup.create_group(api, second_name, "Second group description",
    >>>                                          query="os.equals:MAC", policy_id=bottom_rank_policy.id)


Parts of Carbon Black Cloud have asynchronous processing and are eventually consistent.
When writing automated scripts, use the status field to determine when the asset group membership has
finished updating.

* ``OK`` indicates the membership evaluation is complete
* ``UPDATING`` indicates that group’s dynamic memberships are being re-evaluated

    >>> while second_asset_group.status != "OK":
    >>>     print("waiting")
    >>>     time.sleep(5)
    >>>     second_asset_group.refresh()
    >>> print(second_asset_group)

The add_member() function is used to assign a device directly to the group. (Compared to dynamically, when the device
matches the query on the asset group.)

    >>> random_device = api.select(Device).first()
    >>> second_asset_group.add_members(random_device)

Delete an Asset Group
---------------------

To delete an Asset Group, use the delete method:

    >>> second_asset_group.delete()

Search for an Asset Group
-------------------------

Asset groups can be searched using ``name``, ``policy_id`` or ``group_id`` in the criteria element.

The example shows creating an AssetGroupQuery class, then adding criteria to limit the results and specifying the field
to sort by.  The query is not executed until it accessed, in this case by iterating over the results.

Summary information for each asset group is printed, and then the devices in that asset group are listed.

    >>> search_asset_group_query = api.select(AssetGroup)
    >>> search_asset_group_query.add_criteria("name", second_name)
    >>> search_asset_group_query.sort_by("name", "ASC")
    >>> for ag in search_asset_group_query:
    >>>     print("\n\nAsset group name = {}. It has {} members".format(ag.name, ag.member_count))
    >>>     print("Policy assigned to the Asset Group is Name: {}, Id: {}".format(ag.policy_name, ag.policy_id))
    >>>     for d in ag.list_members():
    >>>         print("Device Name: {}, Id: {}".format(d.name, d.id))


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

The results here indicate that if policy_id 1234 was moved to the top rank, then 18 assets that currently have
policy 9876 as the effective policy would have policy 1234 as the effective policy after the change.  The asset query
can be used to get the 18 affected assets.

    >>> policy_id = 1234
    >>> -- to get a policy that exists in your org: policy_id = api.select(Policy).first().id
    >>> new_policy_position = 1
    >>> api = CBCloudAPI(profile='sample')
    >>> changes = Policy.preview_policy_rank_changes(api, [(policy_id, new_policy_position)])

TO DO NEED DEV01 TO COME BACK TO LIFE

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

TO DO NEED DEV01 TO COME BACK TO LIFE
