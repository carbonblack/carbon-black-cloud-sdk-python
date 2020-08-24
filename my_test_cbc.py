# from cbc_sdk.defense import Device, Event, Policy
from cbc_sdk.defense import Device as DefenseDevice
from cbc_sdk.defense import Event as DefenseEvent
from cbc_sdk.defense import Policy as DefensePolicy
from cbc_sdk.defense import Query as DefenseQuery
from cbc_sdk.platform import Device as PlatformDevice
from cbc_sdk.platform import DeviceSearchQuery
from cbc_sdk.threathunter import Process as ThreatHunterProcess
from cbc_sdk.threathunter import Event as ThreatHunterEvent
from cbc_sdk.threathunter import Tree as ThreatHunterTree
from cbc_sdk.threathunter import Watchlist, Feed, Report, Binary, Downloads
from cbc_sdk import CBCloudAPI

import logging

log = logging.basicConfig(level=logging.DEBUG, filename='log.txt', filemode='w')


# API type Key
cb_api_type = CBCloudAPI(profile="defense")
# Custom type Key
cb_super_admin = CBCloudAPI(profile="super_admin")

"""Defense Device Querying with .where()"""

"""Params from"""
"""https://developer.carbonblack.com/reference/carbon-black-cloud/platform/deprecated/rest-api/#device-status"""

defense_select_hostname_device_query = cb_api_type.select(DefenseDevice).where('hostName:Win7x64')
results = [result for result in defense_select_hostname_device_query._perform_query()]
assert len(results) == 1

defense_select_hostname_device_query = cb_api_type.select(DefenseDevice).where(hostName='Win7x64')
results = [result for result in defense_select_hostname_device_query._perform_query()]
assert len(results) == 1
assert defense_select_hostname_device_query._count() == len(results)
device = results[0]
assert device._model_unique_id == 43407
assert device.deviceId == 43407
assert isinstance(device, DefenseDevice)
assert device.validate()

defense_select_hostname_exact_device_query = cb_api_type.select(DefenseDevice).where('hostNameExact:Win7x64')
results = [result for result in defense_select_hostname_exact_device_query._perform_query()]
assert len(results) == 1
assert defense_select_hostname_exact_device_query._count() == len(results)
device = results[0]
assert device._model_unique_id == 43407
assert device.deviceId == 43407
assert isinstance(device, DefenseDevice)
assert device.validate()

defense_select_ownername_device_query = cb_api_type.select(DefenseDevice).where('ownerName:smultani@carbonblack.com')
results = [result for result in defense_select_ownername_device_query._perform_query()]
assert defense_select_ownername_device_query._count() == len(results)
device = results[0]
assert device.email == "smultani@carbonblack.com"
assert isinstance(device, DefenseDevice)
assert device.validate()

defense_select_ownername_exact_device_query = cb_api_type.select(DefenseDevice).where('ownerNameExact:Langly@strugholdmining.com')
results = [result for result in defense_select_ownername_exact_device_query._perform_query()]
assert len(results) == 1
assert defense_select_ownername_exact_device_query._count() == len(results)
device = results[0]
assert device._model_unique_id == 1431
assert device.deviceId == 1431
assert isinstance(device, DefenseDevice)
assert device.validate()


defense_select_ip_device_query = cb_api_type.select(DefenseDevice).where('ipAddress:10.210.34.165')
results = [result for result in defense_select_ip_device_query._perform_query()]
assert len(results) == 1
assert defense_select_ip_device_query._count() == len(results)
device = results[0]
assert device._model_unique_id == 43407
assert device.deviceId == 43407
assert isinstance(device, DefenseDevice)
assert device.validate()


"""Defense Device Querying with .where() and .and_()"""
defense_select_hostname_and_ip_device_query = cb_api_type.select(DefenseDevice).where('hostName:Win7x64').and_('ipAddress:10.210.34.165')
results = [result for result in defense_select_hostname_and_ip_device_query._perform_query()]
assert len(results) == 1
assert defense_select_hostname_and_ip_device_query._count() == len(results)
device = results[0]
assert device._model_unique_id == 43407
assert device.deviceId == 43407
assert isinstance(device, DefenseDevice)
assert device.validate()


"""Defense Device Querying with .select(Device, `device_id`)"""
defense_device_select_with_id = cb_api_type.select(DefenseDevice, 43407)
assert isinstance(defense_device_select_with_id, DefenseDevice)
defense_device_select_with_id.refresh()
assert defense_device_select_with_id._model_unique_id == 43407
assert defense_device_select_with_id.deviceId == 43407
assert isinstance(defense_device_select_with_id, DefenseDevice)
assert defense_device_select_with_id.validate()


"""Defense Device Querying for all devices"""
defense_device_select_all = cb_api_type.select(DefenseDevice)
results = [result for result in defense_device_select_all._perform_query()]
assert isinstance(defense_device_select_all, DefenseQuery)
assert len(results) == 52


"""Defense Device _search"""
defense_device_select_all = cb_api_type.select(DefenseDevice)
assert isinstance(defense_device_select_all, DefenseQuery)
query = defense_device_select_all._search(start=0, rows=100)
results = [result for result in query]
assert len(results) == 52

"""Defense Device _search with hostname and ip where clauses"""
defense_device_select_host_ip = cb_api_type.select(DefenseDevice).where('hostName:Win7x64').and_('ipAddress:10.210.34.165')
assert isinstance(defense_device_select_host_ip, DefenseQuery)
query = defense_device_select_host_ip._search(start=0, rows=100)
results = [result for result in query]
assert len(results) == 1
found_dev = results[0]
assert found_dev['deviceId'] == 43407
assert found_dev['name'] == 'Win7x64'

"""Defense Event Querying with .select(Event)"""
events = cb_api_type.select(DefenseEvent).where('hostNameExact:Win7x64')
results = [event for event in events._perform_query()]
# event_with_alert = [result for result in results if result.eventId == '125ff1f4d7ed11ea920d3d9192a785d1']
# print(event_with_alert)
# assert len(event_with_alert) == 1
event = results[0]
# assert event.eventId == '125ff1f4d7ed11ea920d3d9192a785d1'
# print(event._info)
assert event.deviceDetails['deviceId'] == 43407
assert event.deviceDetails['deviceName'] == 'Win7x64'


"""Defense Event Querying with .select(Event, `id`)"""
event = cb_api_type.select(DefenseEvent, 'a1e12604d67b11ea920d3d9192a785d1')
assert isinstance(event, DefenseEvent)
assert event.eventId == 'a1e12604d67b11ea920d3d9192a785d1'
assert event.deviceDetails['deviceId'] == 43407
assert event.deviceDetails['deviceName'] == 'Win7x64'


"""Defense Policy Querying with .select(Policy, `policy_id`)"""
# failing on modify rule with error 500
# this test adds and deletes rules live, so commented out to not tax the system
# policy = cb_api_type.select(DefensePolicy, 30241)
# assert policy.id == 30241
# policy.refresh()
#
# new_rule = {"action": "TERMINATE", "application": {"type": "REPUTATION", "value": "COMPANY_BLACK_LIST"}, "operation": "RANSOM", "required": True}
# rules = policy.rules.values()
# rule_ids = [rule.pop('id') for rule in rules]
# rules_without_ids = rules
# # policy.delete_rule(rule_ids[-1])
# print("Rules before add: ", rules)
# # the id is different each run
# assert new_rule not in rules_without_ids
#
# policy.add_rule(new_rule)
# rules = policy.rules.values()
# rule_ids = [rule.pop('id') for rule in rules]
# rules_without_ids = rules
# # print("Rules after add: ", rules_without_ids)
# assert new_rule in rules_without_ids

# modified_rule = {"action": "IGNORE", "application": {"type": "REPUTATION", "value": "COMPANY_BLACK_LIST"}, "operation": "RANSOM", "required": True}
# policy.replace_rule(rule_ids[-1], modified_rule)
# rules = policy.rules.values()
# rule_ids = [rule.pop('id') for rule in rules]
# rules_without_ids = rules
# assert modified_rule in rules_without_ids
#
# policy.delete_rule(rule_ids[-1])
# rules = policy.rules.values()
# rule_ids = [rule.pop('id') for rule in rules]
# rules_without_ids = rules
# assert new_rule not in rules_without_ids

"""Defense Policy Querying with .select(Policy)"""
# this test is failing, not sure how to add to the query with the primary key
# modified defense.base Policy.primary_key == 'id' to try workaround, delete if not using
policy = cb_api_type.select(DefensePolicy, 30241)
assert isinstance(policy, DefensePolicy)
# results = [policy for policy in policy._perform_query()]
assert policy.id == 30241
assert policy.name == "Lyon_test"

"""Platform Device Querying with .select(Device, `device_id`)"""
platform_device_select_with_id = cb_super_admin.select(PlatformDevice, 43407)
platform_device_select_with_id.refresh()
assert platform_device_select_with_id._model_unique_id == 43407
assert platform_device_select_with_id.id == 43407
assert isinstance(platform_device_select_with_id, PlatformDevice)
assert platform_device_select_with_id.validate()


"""Platform Device Querying with .where() and .and_()"""
platform_device_select_with_where_stmt = cb_super_admin.select(PlatformDevice).where(deviceId='43407').and_(name='win7x64')
assert isinstance(platform_device_select_with_where_stmt, DeviceSearchQuery)
assert platform_device_select_with_where_stmt._count() == 1
results = [res for res in platform_device_select_with_where_stmt._perform_query()]
assert results[0]._info['id'] == platform_device_select_with_id._info['id']
assert len(results[0]._info) == len(platform_device_select_with_id._info)
assert len(results[0]._info) != 0
assert results[0].validate()


"""ThreatHunter Process Querying"""
"""Yikes having trouble with querying, even with cbapi"""
guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
process = cb_super_admin.select(ThreatHunterProcess, guid)
assert isinstance(process, ThreatHunterProcess)
assert process.process_guid == guid
assert process.summary is not None
summary = cb_super_admin.select(ThreatHunterProcess.Summary, guid)
assert summary is not None

""" This returns JSON without the 'incomplete_results' key, GitLab appears to show it's no longer there
https://gitlab.bit9.local/carbonblack/cbent/-/blob/b31ce12a14f96377939aade193b916a7926511b8/code/swagger/ui/spec/models/process_guid.yaml
summ = cb.get_object('/api/investigate/v1/orgs/WNEXFKQ7/processes/summary', query_parameters={"process_guid": 'WNEXFKQ7-0000a98f-00000378-00000000-1d64432afb2dba6'})
"""


"""ThreatHunter Event Querying"""
guid = "WNEXFKQ7-0002b226-00000a58-00000000-1d66a9ca1bba500"
process = cb_super_admin.select(ThreatHunterProcess, guid)
assert isinstance(process, ThreatHunterProcess)
assert process.process_guid == guid

# events = [event for event in process.events()]
# assert events[0].process_guid == guid

guid = 'WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00'
events = cb_super_admin.select(ThreatHunterEvent).where(process_guid=guid)
results = [res for res in events._perform_query(numrows=10)]
assert len(results) == 10
first_event = results[0]
assert first_event.process_guid == guid

events = cb_super_admin.select(ThreatHunterEvent).where('process_guid:WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00')
results = [res for res in events._perform_query(numrows=10)]
assert len(results) == 10
first_event = results[0]
assert first_event.process_guid == guid

results = [result for result in events._perform_query(numrows=100)]
assert len(results) == 100
first_result = results[0]
assert first_result.process_guid == guid


"""ThreatHunter Tree Querying"""
process = cb_super_admin.select(ThreatHunterProcess, guid)
tree = process.tree()
children = tree.nodes["children"]
assert len(children) == len(tree.children)
assert len(children) > 0

procTree = cb_super_admin.select(ThreatHunterTree).where(process_guid="WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00")
results = procTree._perform_query()
assert results is not None
assert results["nodes"]["children"] is not None
assert results["incomplete_results"] is False


"""Watchlist Querying"""
watchlist = cb_super_admin.select(Watchlist)
results = [res for res in watchlist._perform_query()]
assert results is not None
assert isinstance(results[0], Watchlist)


"""Report Querying"""
reports = cb_super_admin.select(Report).where(feed_id="rEVxDoWRAucNZI8utPRrQ")
results = [res for res in reports._perform_query()]
assert results is not None
assert isinstance(results[0], Report)
assert reports[0].iocs_ is not None


"""Feed Querying"""
feed = cb_super_admin.select(Feed).where(include_public=True)
results = [res for res in feed._perform_query()]
assert results is not None

feed = cb_super_admin.select(Feed).where(feed_id="rEVxDoWRAucNZI8utPRrQ")
results = [res for res in feed._perform_query()]
assert results is not None

feed = cb_super_admin.select(Feed, "rEVxDoWRAucNZI8utPRrQ")
assert isinstance(feed, Feed)
assert feed.id == "rEVxDoWRAucNZI8utPRrQ"


"""Binary Querying"""
bin = cb_super_admin.select(Binary, "00a16c806ff694b64e566886bba5122655eff89b45226cddc8651df7860e4524")
assert isinstance(bin, Binary)
summary = bin.summary
url = bin.download_url
assert summary is not None
assert url is not None


"""Downloads Querying"""
dl = cb_super_admin.select(Downloads, ["00a16c806ff694b64e566886bba5122655eff89b45226cddc8651df7860e4524"])
assert isinstance(dl, Downloads)
found_items = dl.found
assert found_items[0].sha256 == "00a16c806ff694b64e566886bba5122655eff89b45226cddc8651df7860e4524"
assert len(found_items) == 1





print("Done")
