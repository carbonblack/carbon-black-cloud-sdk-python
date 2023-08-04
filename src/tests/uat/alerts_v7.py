#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2020-2023. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Working test script for Alert v7 updates targeted for SDK 1.5.0 release.

Status: working script to user test functionality incrementally during development.
May evolve to something automated and/or easily run manually.
"""

import sys
# from datetime import datetime, timedelta, timezone
from cbc_sdk import CBCloudAPI
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import BaseAlert, CBAnalyticsAlert, ContainerRuntimeAlert, DeviceControlAlert, WatchlistAlert

def search_alert_no_criteria(cb, print_detail):
    """get a list of alerts, no criteria"""
    alert_list = cb.select(BaseAlert)
    print("Search returned {} alerts.".format(len(alert_list)))
    if print_detail:
        if len(alert_list) > 0:
            print("First alert is: {}".format(alert_list.first()))

    return alert_list.first()
        # TO DO - Extension
    # For each alert type, get list of alerts


def get_alert_by_id(cb, alert, print_detail):
    """Get a single alert by identifier"""
    alert_list = cb.select(BaseAlert).set_alert_ids([alert.id])
    found_alert = alert_list.first()
    found_alert.refresh()
    print("Search returned {} alerts for alert_id.".format(len(alert_list)))
    if print_detail:
        for a in alert_list:
            print(a)


def verify_v6_v7_field_mappings_base_alert(alert):
    """Check that fields from v6 Alert that have a different name in v7 are mapped correctly"""
    try:
        # category is deprecated and should throw an exception
        print("Print alert category: should throw an exception: {}".format(alert.category))
        print("Nooooooooooooooo!  Should have got an exception - category")
    except:
        print("Got exception for category. This is correct")

    try:
        if alert.create_time == alert.backend_timestamp:
            print("ok - create_time")
        else:
            print("Nooooooooooooooo! Fields do not match - create_time")
    except:
        print("Something unexpected went wrong in create_time")


    # following fields have no change, so null operations to check
    print("device id: {}".format(alert.device_id))
    print("device_name: {}".format(alert.device_name))
    print("device_os: {}".format(alert.device_os))
    print("device_os_version: {}".format(alert.device_os_version))
    print("device_username: {}".format(alert.device_username))

    try:
        if alert.first_event_time == alert.first_event_timestamp:
            print("ok - first_event_time")
        else:
            print("Nooooooooooooooo! Fields do not match - first_event_time")
    except:
        print("Something unexpected went wrong in first_event_time")

    try:
        # group_details is deprecated and should throw an exception
        print("Print group details: should throw an exception: {}".format(alert.group_details))
        print("Nooooooooooooooo!  Should have got an exception - group_details")
    except:
        print("Got exception for group_details. This is correct")

    print("id: {}".format(alert.id))


    try:
        if alert.last_event_time == alert.last_event_timestamp:
            if alert.last_event_time == alert.last_event_timestamp:
                print("ok - last_event_time")
        else:
            print("Nooooooooooooooo! Fields do not match - last_event_time")
    except:
        print("Something unexpected went wrong in last_event_time")

    try:
        if alert.last_update_time == alert.change_timestamp:
            print("ok - last_update_time")
        else:
            print("Nooooooooooooooo! Fields do not match - last_update_time")
    except:
        print("Something unexpected went wrong in last_update_time")

    try:
        if alert.legacy_alert_id == alert.id:
            print("ok - legacy_alert_id")
        else:
            print("Nooooooooooooooo! Fields do not match - legacy_alert_id")
    except:
        print("Something unexpected went wrong in legacy_alert_id")

    try:
        if alert.notes_present == alert.alert_notes_present:
            print("ok - notes_present")
        else:
            print("Nooooooooooooooo! Fields do not match - notes_present")
    except:
        print("Something unexpected went wrong in notes_present")

    print("org_key: {}".format(alert.org_key))


    try:
        if alert.policy_id == alert.device_policy_id:
            print("ok - policy_id")
        else:
            print("Nooooooooooooooo! Fields do not match - policy_id")
    except:
        print("Something unexpected went wrong in policy_id")

    try:
        if alert.policy_name == alert.device_policy:
            print("ok - policy_name")
        else:
            print("Nooooooooooooooo! Fields do not match - policy_name")
    except:
        print("Something unexpected went wrong in policy_name")

    print("severit: {}".format(alert.severity))
    print("tags: {}".format(alert.tags))

    try:
        if alert.target_value == alert.device_target_value:
            print("ok - target_value")
        else:
            print("Nooooooooooooooo! Fields do not match - target_value")
    except:
        print("Something unexpected went wrong in target_value")

    print("threat_id: {}".format(alert.threat_id))
    print("type: {}".format(alert.type))
    print("workflow: {}".format(alert.workflow))
    return alert


def verify_v6_v7_field_mappings_cb_analytics_alert(cb):
    """No additional fields.  get_events() method and check the type can be selected"""
    alert_list = cb.select(CBAnalyticsAlert)
    alert = alert_list.first()
    print(alert)
    # TO DO - behaviour of this under discussion
    alert.get_events()
    if alert.type != "CB_ANALYTICS":
        print("Nooooooooooo! Wrong type in verify_v6_v7_field_mappings_cb_analytics_alert")

    return alert

def verify_v6_v7_field_mappings_container_runtime_alert(cb):
    """No additional fields or methods, just check the type can be selected"""
    alert = cb.select(ContainerRuntimeAlert).first()
    print(alert)
    if alert.type != "CONTAINER_RUNTIME":
        print("Nooooooooooo! Wrong type in verify_v6_v7_field_mappings_container_runtime_alert")

    return alert

def verify_v6_v7_field_mappings_device_control_alert(cb):
    """No additional fields or methods, just check the type can be selected"""
    "TO DO - waiting on timerange to work"
    alert_list = cb.select(DeviceControlAlert).set_backend_timestamp(range="-20d")
    alert = alert_list.first()
    print(alert)
    if alert.type != "DEVICE_CONTROL":
        print("Nooooooooooo! Wrong type in verify_v6_v7_field_mappings_device_control_alert")

    return alert

def verify_v6_v7_field_mappings_watchlist_alert(cb):
    """No additional fields.  Test get_process methods and that the type can be selected"""
    alert = cb.select(WatchlistAlert).first()
    if alert.type != "WATCHLIST":
        print("Nooooooooooo! Wrong type in verify_v6_v7_field_mappings_watchlist_alert")
    print(alert)
    return alert

def verify_tojson(alert):
    """Check to json for each alert type, v6 and v7"""
    print("v7 Alert to Json:")
    print(alert.to_json())
    print("\n\n\n v6 Alert to Json: \n\n\n")
    print(alert.to_json("v6"))



def main():
    """Main function for Alerts - Demonstrate UAE features script."""

    parser = build_cli_parser("Test Alert Functions")

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)
    cb_container = CBCloudAPI(profile="CONTAINER_RUNTIME")
    alert = search_alert_no_criteria(cb, False)
    get_alert_by_id(cb, alert, False)
    base_alert = verify_v6_v7_field_mappings_base_alert(alert)
    cb_analytics_alert = verify_v6_v7_field_mappings_cb_analytics_alert(alert)
    container_runtime_alert = verify_v6_v7_field_mappings_container_runtime_alert(cb_container)
    device_control_alert = verify_v6_v7_field_mappings_device_control_alert(cb)
    watchlist_alert = verify_v6_v7_field_mappings_watchlist_alert(cb)
    verify_tojson(base_alert)


    return 0


if __name__ == "__main__":
    sys.exit(main())
